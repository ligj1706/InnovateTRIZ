#!/usr/bin/env python3
"""
TRIZ Innovation Algorithm Application - Professional Edition
Powerful problem-solving tool based on TRIZ theory with 40 invention principles and extended contradiction matrix
Features intelligent analysis, history tracking, solution export, and advanced functionalities
"""

import json
import os
import sys
import re
import datetime
import pickle
import uuid
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    MAGENTA = '\033[35m'
    ORANGE = '\033[38;5;208m'
    
    @classmethod
    def disable(cls):
        for attr in dir(cls):
            if not attr.startswith('_') and attr != 'disable':
                setattr(cls, attr, '')

@dataclass
class Solution:
    principle: str
    principle_id: int
    description: str
    detailed_explanation: str
    examples: List[str]
    confidence: float
    relevance_score: float
    category: str
    tags: List[str]
    
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class ProblemSession:
    problem: str
    improving_param: str
    worsening_param: str
    solutions: List[Solution]
    timestamp: datetime.datetime
    session_id: str
    user_rating: Optional[int] = None
    notes: str = ""

class Translations:
    """Bilingual translation system"""
    
    TEXT = {
        "en": {
            # Headers and titles
            "app_title": "🚀 InnovateTRIZ - Pro",
            "app_subtitle": "Intelligent Problem Solving Made Simple",
            "menu_title": "🚀 InnovateTRIZ",
            
            # Main menu
            "menu_analyze": "🎯 Analyze Problem",
            "menu_brainstorm": "💡 Quick Brainstorm",
            "menu_export": "📊 Export Solutions",
            "menu_more": "📈 History & More",
            "menu_exit": "❌ Exit",
            "menu_language": "🌐 中文",
            
            # Input prompts
            "prompt_choice": "Choose option (1-4, 0 to exit)",
            "prompt_problem": "Describe your problem",
            "prompt_export_format": "Format (1=JSON, 2=Text, Enter=JSON)",
            "prompt_continue": "Press Enter to continue...",
            "prompt_action": "Action (f1-f5 to favorite, 'v' view favorites, Enter to continue)",
            
            # Analysis
            "analysis_title": "🎯 Quick Problem Analysis",
            "analysis_tips": "Tips: Type 'help' for shortcuts, 'back' to return",
            "analysis_auto_detect": "⚡ Auto-detecting parameters...",
            "analysis_reusing": "Reusing",
            "analysis_example": "Example",
            
            # Solutions
            "solutions_title": "Solutions",
            "solutions_analysis": "Analysis Results",
            "solutions_brainstorm": "Brainstorm Results",
            "solutions_none": "💭 No solutions found",
            "solutions_count": "solutions",
            
            # Loading messages
            "loading_analyzing": "Analyzing with AI and TRIZ matrix",
            "loading_brainstorm": "Generating creative solutions",
            "loading_export": "Generating export file",
            
            # Export
            "export_title": "📊 Quick Export",
            "export_success": "✅ Exported to file",
            "export_failed": "❌ Export failed",
            "export_no_solutions": "❌ No solutions available for export",
            
            # More options
            "more_title": "🔧 More Options",
            "more_favorites": "⭐ Favorites",
            "more_history": "📈 History",
            "more_settings": "⚙️ Settings",
            "more_statistics": "📋 Statistics",
            "more_back": "⬅️ Back",
            
            # Messages
            "msg_invalid_choice": "❌ Invalid choice, please try again",
            "msg_thank_you": "👋 Thank you for using InnovateTRIZ!",
            "msg_details_required": "Please provide more details (at least 10 characters)",
            "msg_added_favorite": "Added to favorites",
            "msg_removed_favorite": "Removed from favorites",
            
            # Shortcuts help
            "help_shortcuts": "Quick shortcuts:",
            "help_last": "'last' - reuse last problem",
            "help_example": "'example' - try example problem",
            "help_back": "'back' - return to menu",
            
            # Favorites
            "favorites_title": "⭐ Favorite Principles",
            "favorites_empty": "📝 Favorites is empty",
            "favorites_total": "Total",
            
            # History
            "history_title": "📈 Recent Analysis Records",
            "history_empty": "📝 No history records available",
            "history_solutions": "Solutions",
            "history_rating": "Rating",
            "history_not_rated": "Not rated",
            
            # Settings
            "settings_title": "⚙️ System Settings",
            "settings_current": "Current configuration",
            "settings_modify_max": "Modify max solutions",
            "settings_toggle_history": "Toggle history",
            "settings_return": "Return",
            "settings_choose": "Choose option (1-5)",
            "settings_enter_max": "Enter max solutions (1-10)",
            "settings_saved": "✅ Settings saved",
            "settings_out_of_range": "❌ Value out of range",
            "settings_format_error": "❌ Input format error",
            "settings_history_enabled": "✅ History enabled",
            "settings_history_disabled": "✅ History disabled",
            
            # Statistics
            "stats_title": "📋 Usage Statistics",
            "stats_total_sessions": "Total sessions",
            "stats_rated_sessions": "Rated sessions",
            "stats_average_rating": "Average rating",
            "stats_favorite_principles": "Favorite principles",
        },
        
        "zh": {
            # Headers and titles
            "app_title": "🚀 TRIZ助手 - 专业版",
            "app_subtitle": "智能问题解决，简单高效",
            "menu_title": "🚀 TRIZ助手",
            
            # Main menu
            "menu_analyze": "🎯 分析问题",
            "menu_brainstorm": "💡 快速头脑风暴",
            "menu_export": "📊 导出解决方案",
            "menu_more": "📈 历史记录和更多",
            "menu_exit": "❌ 退出",
            "menu_language": "🌐 English",
            
            # Input prompts
            "prompt_choice": "选择选项 (1-4, 0退出)",
            "prompt_problem": "描述您的问题",
            "prompt_export_format": "格式 (1=JSON, 2=文本, 回车=JSON)",
            "prompt_continue": "按回车键继续...",
            "prompt_action": "操作 (f1-f5收藏, 'v'查看收藏, 回车继续)",
            
            # Analysis
            "analysis_title": "🎯 快速问题分析",
            "analysis_tips": "提示: 输入'help'查看快捷键, 'back'返回",
            "analysis_auto_detect": "⚡ 自动检测参数中...",
            "analysis_reusing": "重用",
            "analysis_example": "示例",
            
            # Solutions
            "solutions_title": "解决方案",
            "solutions_analysis": "分析结果",
            "solutions_brainstorm": "头脑风暴结果",
            "solutions_none": "💭 未找到解决方案",
            "solutions_count": "个解决方案",
            
            # Loading messages
            "loading_analyzing": "基于AI和TRIZ矩阵分析中",
            "loading_brainstorm": "生成创意解决方案中",
            "loading_export": "生成导出文件中",
            
            # Export
            "export_title": "📊 快速导出",
            "export_success": "✅ 已导出到文件",
            "export_failed": "❌ 导出失败",
            "export_no_solutions": "❌ 没有可导出的解决方案",
            
            # More options
            "more_title": "🔧 更多选项",
            "more_favorites": "⭐ 收藏夹",
            "more_history": "📈 历史记录",
            "more_settings": "⚙️ 系统设置",
            "more_statistics": "📋 使用统计",
            "more_back": "⬅️ 返回",
            
            # Messages
            "msg_invalid_choice": "❌ 无效选择，请重新输入",
            "msg_thank_you": "👋 感谢使用TRIZ助手！",
            "msg_details_required": "请提供更多详细信息（至少10个字符）",
            "msg_added_favorite": "已添加到收藏夹",
            "msg_removed_favorite": "已从收藏夹移除",
            
            # Shortcuts help
            "help_shortcuts": "快捷键说明:",
            "help_last": "'last' - 重用上次问题",
            "help_example": "'example' - 尝试示例问题",
            "help_back": "'back' - 返回菜单",
            
            # Favorites
            "favorites_title": "⭐ 收藏的原理",
            "favorites_empty": "📝 收藏夹为空",
            "favorites_total": "共",
            
            # History
            "history_title": "📈 最近的分析记录",
            "history_empty": "📝 暂无历史记录",
            "history_solutions": "方案数",
            "history_rating": "评分",
            "history_not_rated": "未评分",
            
            # Settings
            "settings_title": "⚙️ 系统设置",
            "settings_current": "当前配置",
            "settings_modify_max": "修改最大解决方案数",
            "settings_toggle_history": "切换历史记录",
            "settings_return": "返回",
            "settings_choose": "选择操作 (1-5)",
            "settings_enter_max": "输入最大解决方案数 (1-10)",
            "settings_saved": "✅ 设置已保存",
            "settings_out_of_range": "❌ 数值范围错误",
            "settings_format_error": "❌ 输入格式错误",
            "settings_history_enabled": "✅ 历史记录已启用",
            "settings_history_disabled": "✅ 历史记录已禁用",
            
            # Statistics
            "stats_title": "📋 使用统计",
            "stats_total_sessions": "总分析次数",
            "stats_rated_sessions": "已评分次数",
            "stats_average_rating": "平均评分",
            "stats_favorite_principles": "收藏原理数",
        }
    }
    
    def __init__(self, language="en"):
        self.current_language = language
    
    def get(self, key: str) -> str:
        """Get translated text for the current language"""
        return self.TEXT[self.current_language].get(key, key)
    
    def set_language(self, language: str):
        """Switch language"""
        if language in self.TEXT:
            self.current_language = language
            return True
        return False
    
    def toggle_language(self):
        """Toggle between English and Chinese"""
        self.current_language = "zh" if self.current_language == "en" else "en"
        return self.current_language

class AdvancedTRIZInnovator:
    def __init__(self):
        self.data_dir = Path.home() / ".triz_innovator_pro"
        self.data_dir.mkdir(exist_ok=True)
        self.history_file = self.data_dir / "history.pkl"
        self.favorites_file = self.data_dir / "favorites.pkl"
        self.config_file = self.data_dir / "config.json"
        
        self.principles = self._load_principles()
        self.contradiction_matrix = self._load_matrix()
        self.parameter_keywords = self._load_parameter_keywords()
        self.problem_categories = self._load_problem_categories()
        
        self.history: List[ProblemSession] = self._load_history()
        self.favorites: Set[str] = self._load_favorites()
        self.config = self._load_config()
        
        # Initialize translation system with saved language
        global t
        t.set_language(self.config.get("language", "en"))
    
    def _load_principles(self) -> Dict[int, Dict[str, any]]:
        """Complete database of 40 TRIZ invention principles"""
        return {
            1: {
                "name": "分割", "description": "将对象分成独立的部分",
                "detailed": "将物体分解为独立的部分，使各部分易于拆卸和组装，增加分解的程度",
                "examples": ["模块化设计", "可拆卸家具", "组件化软件架构", "微服务架构"],
                "category": "结构优化", "keywords": ["模块", "组件", "分离", "独立", "拆分"]
            },
            2: {
                "name": "抽取", "description": "从对象中取出干扰的部分或特性",
                "detailed": "分离出有害或不必要的部分/特性，或相反，单独分离出有用的部分/特性",
                "examples": ["噪音消除", "杂质过滤", "核心功能提取", "异常处理隔离"],
                "category": "功能优化", "keywords": ["提取", "分离", "净化", "隔离", "筛选"]
            },
            15: {
                "name": "动态性", "description": "使对象或系统能够自动适应工作的最佳状态",
                "detailed": "对象的特性应改变，以便在工作的每个阶段都是最佳的；将对象分成能够相互移动的部分",
                "examples": ["自适应系统", "动态调整", "智能响应", "弹性伸缩"],
                "category": "适应性优化", "keywords": ["动态", "自适应", "调整", "变化", "响应"]
            },
            27: {
                "name": "廉价替代", "description": "用便宜的对象代替昂贵的对象",
                "detailed": "用便宜的对象来代替昂贵的，在某些特性（如使用寿命）上有所损失",
                "examples": ["开源替代", "低成本方案", "简化版本", "经济型设计"],
                "category": "成本优化", "keywords": ["廉价", "替代", "经济", "低成本", "简化"]
            },
            35: {
                "name": "参数改变", "description": "改变对象的物理或化学状态",
                "detailed": "改变对象的物理或化学状态；改变浓度或稠度；改变柔性的程度；改变温度",
                "examples": ["状态转换", "参数调整", "相变利用", "属性修改"],
                "category": "状态优化", "keywords": ["状态", "参数", "转换", "调整", "修改"]
            },
            40: {
                "name": "复合材料", "description": "用复合材料代替均质材料",
                "detailed": "从均质材料转向复合材料",
                "examples": ["复合材料", "多层结构", "混合系统", "组合方案"],
                "category": "材料优化", "keywords": ["复合", "多层", "混合", "组合", "复杂"]
            }
        }
    
    def _load_matrix(self) -> Dict[Tuple[str, str], List[int]]:
        """Extended technical contradiction matrix"""
        return {
            ("重量", "强度"): [1, 8, 15, 40], ("重量", "速度"): [2, 14, 15, 35],
            ("强度", "重量"): [1, 8, 36, 40], ("复杂性", "可靠性"): [1, 26, 27, 40],
            ("精度", "速度"): [10, 18, 32, 39], ("成本", "质量"): [13, 26, 27, 35],
            ("能耗", "效率"): [2, 6, 19, 36], ("体积", "功能"): [7, 17, 29, 40],
            ("速度", "精度"): [10, 18, 32, 39], ("安全", "便利"): [11, 24, 25, 35],
            ("自动化", "成本"): [25, 26, 27, 35], ("智能化", "可靠性"): [15, 23, 25, 35]
        }
    
    def _load_parameter_keywords(self) -> Dict[str, List[str]]:
        """Parameter keyword mapping"""
        return {
            "重量": ["重", "轻", "质量", "重量", "载重"],
            "强度": ["强度", "硬度", "刚性", "坚固", "耐用"],
            "速度": ["快", "慢", "速度", "效率", "响应"],
            "精度": ["精确", "准确", "精度", "误差", "偏差"],
            "成本": ["价格", "费用", "成本", "便宜", "昂贵"],
            "质量": ["质量", "品质", "优质", "可靠", "稳定"],
            "复杂性": ["复杂", "简单", "复杂度", "难度", "繁琐"],
            "体积": ["大小", "体积", "尺寸", "占地", "空间"],
            "安全": ["安全", "危险", "风险", "保护", "防护"],
            "效率": ["效率", "性能", "生产率", "吞吐量", "产能"]
        }
    
    def _load_problem_categories(self) -> Dict[str, List[str]]:
        """Problem category keywords"""
        return {
            "技术问题": ["技术", "系统", "设备", "机器", "算法", "软件"],
            "设计问题": ["设计", "外观", "结构", "布局", "界面", "造型"],
            "成本问题": ["成本", "价格", "费用", "预算", "经济", "投资"],
            "用户问题": ["用户", "客户", "体验", "需求", "满意", "使用"],
            "质量问题": ["质量", "缺陷", "故障", "错误", "问题", "不良"]
        }
    
    def _load_config(self) -> dict:
        """Load configuration"""
        default_config = {
            "max_solutions": 5,
            "enable_history": True,
            "auto_save": True,
            "export_format": "json",
            "language": "en"
        }
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return {**default_config, **json.load(f)}
        except Exception:
            pass
        return default_config
    
    def toggle_language(self):
        """Toggle between English and Chinese"""
        global t
        new_lang = t.toggle_language()
        self.config["language"] = new_lang
        self._save_config()
        return new_lang
    
    def _save_config(self):
        """Save configuration"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def _load_history(self) -> List[ProblemSession]:
        """Load history records"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'rb') as f:
                    return pickle.load(f)
        except Exception:
            pass
        return []
    
    def _load_favorites(self) -> Set[str]:
        """Load favorites"""
        try:
            if self.favorites_file.exists():
                with open(self.favorites_file, 'rb') as f:
                    return pickle.load(f)
        except Exception:
            pass
        return set()
    
    def _save_history(self):
        """Save history records"""
        if not self.config.get("enable_history", True):
            return
        try:
            with open(self.history_file, 'wb') as f:
                pickle.dump(self.history[-100:], f)  # Save last 100 records
        except Exception:
            pass
    
    def _save_favorites(self):
        """Save favorites"""
        try:
            with open(self.favorites_file, 'wb') as f:
                pickle.dump(self.favorites, f)
        except Exception:
            pass
    
    def _smart_parameter_detection(self, text: str) -> List[str]:
        """Smart parameter detection"""
        detected = []
        text_lower = text.lower()
        
        for param, keywords in self.parameter_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected.append(param)
        
        return detected
    
    def _categorize_problem(self, problem: str) -> str:
        """Problem categorization"""
        problem_lower = problem.lower()
        
        for category, keywords in self.problem_categories.items():
            if any(keyword in problem_lower for keyword in keywords):
                return category
        
        return "General Problem"
    
    def analyze_problem(self, problem: str, improving: str = "", worsening: str = "") -> List[Solution]:
        """Intelligently analyze problems and generate solutions"""
        # Smart parameter detection
        if not improving or not worsening:
            detected_params = self._smart_parameter_detection(problem)
            if len(detected_params) >= 2:
                improving = improving or detected_params[0]
                worsening = worsening or detected_params[1]
            elif len(detected_params) == 1:
                improving = improving or detected_params[0]
                worsening = worsening or "复杂性"  # Default worsening parameter
        
        # Find contradiction matrix
        key = (improving.lower(), worsening.lower())
        reverse_key = (worsening.lower(), improving.lower())
        
        principle_ids = self.contradiction_matrix.get(key) or self.contradiction_matrix.get(reverse_key)
        
        # If no exact match found, use smart recommendations
        if not principle_ids:
            principle_ids = self._get_smart_recommendations(problem, improving, worsening)
        
        solutions = []
        for pid in principle_ids[:self.config.get("max_solutions", 5)]:
            if pid in self.principles:
                principle_data = self.principles[pid]
                solution = self._generate_solution(problem, principle_data, pid, improving, worsening)
                solutions.append(solution)
        
        # Sort
        solutions = sorted(solutions, key=lambda x: (x.confidence + x.relevance_score) / 2, reverse=True)
        
        # Save to history
        if self.config.get("enable_history", True):
            session = ProblemSession(
                problem=problem,
                improving_param=improving,
                worsening_param=worsening,
                solutions=solutions,
                timestamp=datetime.datetime.now(),
                session_id=str(uuid.uuid4())[:8]
            )
            self.history.append(session)
            if self.config.get("auto_save", True):
                self._save_history()
        
        return solutions
    
    def _get_smart_recommendations(self, problem: str, improving: str, worsening: str) -> List[int]:
        """Smart principle recommendations"""
        problem_category = self._categorize_problem(problem)
        
        recommendations = {
            "Technical Problem": [1, 2, 15, 35, 40],
            "Design Problem": [1, 15, 27, 35, 40],
            "Cost Problem": [27, 35, 1, 2, 40],
            "User Problem": [15, 35, 1, 27, 40],
            "Quality Problem": [1, 2, 15, 35, 40]
        }
        
        return recommendations.get(problem_category, [1, 2, 15, 27, 35])
    
    def _generate_solution(self, problem: str, principle_data: dict, pid: int, improving: str, worsening: str) -> Solution:
        """Generate solution"""
        # Calculate confidence and relevance
        confidence = self._calculate_confidence(problem, principle_data, improving, worsening)
        relevance = self._calculate_relevance(problem, principle_data)
        
        # Generate description
        description = self._generate_description(problem, principle_data, improving, worsening)
        
        return Solution(
            principle=principle_data["name"],
            principle_id=pid,
            description=description,
            detailed_explanation=principle_data["detailed"],
            examples=principle_data["examples"],
            confidence=confidence,
            relevance_score=relevance,
            category=principle_data["category"],
            tags=principle_data["keywords"][:3]
        )
    
    def _calculate_confidence(self, problem: str, principle_data: dict, improving: str, worsening: str) -> float:
        """Calculate confidence score"""
        base_confidence = 0.6
        
        # Keyword matching
        problem_lower = problem.lower()
        keyword_matches = sum(1 for kw in principle_data["keywords"] if kw in problem_lower)
        keyword_bonus = min(0.3, keyword_matches * 0.1)
        
        # Parameter relevance
        param_bonus = 0.1 if (improving.lower() in str(principle_data["keywords"]).lower() or 
                             worsening.lower() in str(principle_data["keywords"]).lower()) else 0
        
        return min(0.95, base_confidence + keyword_bonus + param_bonus)
    
    def _calculate_relevance(self, problem: str, principle_data: dict) -> float:
        """Calculate relevance score"""
        problem_lower = problem.lower()
        
        # Keyword matching
        keyword_score = sum(1 for kw in principle_data["keywords"] if kw in problem_lower)
        
        # Example matching
        example_score = sum(1 for ex in principle_data["examples"] 
                          if any(word in problem_lower for word in ex.lower().split()))
        
        return min(1.0, (keyword_score * 0.2 + example_score * 0.1))
    
    def _generate_description(self, problem: str, principle_data: dict, improving: str, worsening: str) -> str:
        """Generate solution description"""
        principle_name = principle_data["name"]
        base_desc = principle_data["description"]
        
        if "软件" in problem or "系统" in problem:
            if principle_name == "分割":
                return f"将{problem}进行模块化拆分，每个模块专注于特定功能，降低{worsening}同时提升{improving}"
            elif principle_name == "动态性":
                return f"为{problem}添加自适应机制，根据实际需求动态调整，平衡{improving}和{worsening}"
        
        return f"运用{principle_name}原理（{base_desc}）来解决{problem}，重点改善{improving}与{worsening}的平衡"
    
    def brainstorm(self, problem: str, num_solutions: int = None) -> List[Solution]:
        """Intelligent brainstorming"""
        if num_solutions is None:
            num_solutions = self.config.get("max_solutions", 5)
        
        # Problem analysis
        problem_category = self._categorize_problem(problem)
        detected_params = self._smart_parameter_detection(problem)
        
        # Select relevant principles
        relevant_principles = self._get_smart_recommendations(problem, "", "")
        
        # Generate solutions
        solutions = []
        for pid in relevant_principles:
            if pid in self.principles:
                principle_data = self.principles[pid]
                solution = self._generate_solution(problem, principle_data, pid, "", "")
                solutions.append(solution)
        
        return sorted(solutions, key=lambda x: (x.confidence + x.relevance_score) / 2, reverse=True)[:num_solutions]
    
    def export_solutions(self, solutions: List[Solution], format_type: str = None) -> str:
        """Export solutions"""
        if format_type is None:
            format_type = self.config.get("export_format", "json")
        
        if format_type.lower() == "json":
            return self._export_json(solutions)
        else:
            return self._export_txt(solutions)
    
    def _export_json(self, solutions: List[Solution]) -> str:
        """Export in JSON format"""
        export_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "solution_count": len(solutions),
            "solutions": [sol.to_dict() for sol in solutions]
        }
        return json.dumps(export_data, ensure_ascii=False, indent=2)
    
    def _export_txt(self, solutions: List[Solution]) -> str:
        """Export in text format"""
        lines = []
        lines.append(        "TRIZ Innovation Solutions Report")
        lines.append("=" * 50)
        lines.append(f"Generation time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Number of solutions: {len(solutions)}")
        lines.append("")
        
        for i, sol in enumerate(solutions, 1):
            lines.append(f"Solution {i}: {sol.principle}")
            lines.append(f"Description: {sol.description}")
            lines.append(f"Confidence: {sol.confidence:.1%}")
            lines.append(f"Relevance: {sol.relevance_score:.1%}")
            lines.append(f"Examples: {', '.join(sol.examples)}")
            lines.append("-" * 30)
            lines.append("")
        
        return "\\n".join(lines)
    
    def add_to_favorites(self, principle_name: str):
        """Add to favorites"""
        self.favorites.add(principle_name)
        self._save_favorites()
    
    def get_history(self, limit: int = 10) -> List[dict]:
        """Get history records"""
        recent_history = self.history[-limit:] if self.history else []
        return [
            {
                "session_id": session.session_id,
                "problem": session.problem,
                "timestamp": session.timestamp.strftime('%Y-%m-%d %H:%M'),
                "solution_count": len(session.solutions),
                "rating": session.user_rating
            }
            for session in reversed(recent_history)
        ]
    
    def get_statistics(self) -> dict:
        """Get usage statistics"""
        if not self.history:
            return {"total_sessions": 0}
        
        total_sessions = len(self.history)
        rated_sessions = [s for s in self.history if s.user_rating]
        avg_rating = sum(s.user_rating for s in rated_sessions) / len(rated_sessions) if rated_sessions else 0
        
        return {
            "total_sessions": total_sessions,
            "rated_sessions": len(rated_sessions),
            "average_rating": avg_rating,
            "favorites_count": len(self.favorites)
        }

# Initialize global translation instance
t = Translations()

def main():
    """Main program - Modern terminal interface"""
    if not sys.stdout.isatty():
        Colors.disable()
    
    innovator = AdvancedTRIZInnovator()
    
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header():
        print(f"\n{Colors.BOLD}{Colors.CYAN}{t.get('app_title')}{Colors.END}")
        print(f"{Colors.CYAN}{t.get('app_subtitle')}{Colors.END}")
    
    def print_menu():
        print(f"\n{Colors.BOLD}{Colors.CYAN}{t.get('menu_title')}{Colors.END}")
        print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        print(f"{Colors.GREEN}  1. {t.get('menu_analyze')}     {Colors.CYAN}2. {t.get('menu_brainstorm')}{Colors.END}")
        print(f"{Colors.GREEN}  3. {t.get('menu_export')}    {Colors.CYAN}4. {t.get('menu_more')}{Colors.END}")
        print(f"{Colors.GREEN}  0. {t.get('menu_exit')}     {Colors.CYAN}L. {t.get('menu_language')}{Colors.END}")
        print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    
    def get_input(prompt_key, color=Colors.CYAN):
        prompt = t.get(prompt_key)
        return input(f"{color}💬 {prompt}: {Colors.END}")
    
    def print_solutions(solutions, title_key="solutions_title"):
        if not solutions:
            print(f"{Colors.RED}{t.get('solutions_none')}{Colors.END}")
            return
        
        title = t.get(title_key)
        solutions_word = t.get('solutions_count')
        print(f"\n{Colors.BOLD}{Colors.GREEN}💡 {title} ({len(solutions)} {solutions_word}){Colors.END}")
        print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        
        for i, sol in enumerate(solutions, 1):
            # Simplified confidence display
            confidence_icon = "🟢" if sol.confidence > 0.8 else "🟡" if sol.confidence > 0.6 else "🔴"
            
            print(f"\n{Colors.BOLD}{Colors.BLUE}{i}. {sol.principle}{Colors.END} {confidence_icon} {sol.confidence:.0%}")
            print(f"   {sol.description}")
            print(f"   {Colors.MAGENTA}💡 {sol.examples[0] if sol.examples else 'No examples'}{Colors.END}")
            
            # Add to favorites shortcut
            fav_status = "⭐" if sol.principle in innovator.favorites else "☆"
            print(f"   {Colors.ORANGE}Press 'f{i}' to favorite {fav_status}{Colors.END}")
    
    def show_loading(message="Analyzing..."):
        import time
        print(f"\n{Colors.YELLOW}⏳ {message}{Colors.END}", end="", flush=True)
        for _ in range(2):  # Reduced from 3 to 2 for faster UX
            time.sleep(0.3)  # Reduced from 0.4 to 0.3
            print(".", end="", flush=True)
        print(f" {Colors.GREEN}✓{Colors.END}")
    
    def smart_analyze_input():
        """Smart input with shortcuts and quick actions"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{t.get('analysis_title')}{Colors.END}")
        print(f"{Colors.CYAN}{t.get('analysis_tips')}{Colors.END}")
        
        while True:
            problem = get_input("prompt_problem")
            
            if problem.lower() == 'back':
                return None
            elif problem.lower() == 'help':
                print(f"{Colors.YELLOW}{t.get('help_shortcuts')}{Colors.END}")
                print(f"  {Colors.GREEN}• {t.get('help_last')}{Colors.END}")
                print(f"  {Colors.GREEN}• {t.get('help_example')}{Colors.END}")
                print(f"  {Colors.GREEN}• {t.get('help_back')}{Colors.END}")
                continue
            elif problem.lower() == 'last' and hasattr(innovator, 'last_problem'):
                problem = innovator.last_problem
                print(f"{Colors.GREEN}{t.get('analysis_reusing')}: {problem}{Colors.END}")
            elif problem.lower() == 'example':
                problem = "How to make software faster without increasing complexity?"
                print(f"{Colors.GREEN}{t.get('analysis_example')}: {problem}{Colors.END}")
            
            if len(problem.strip()) < 10:
                print(f"{Colors.RED}{t.get('msg_details_required')}{Colors.END}")
                continue
                
            innovator.last_problem = problem
            
            # Smart parameter detection message
            print(f"{Colors.YELLOW}{t.get('analysis_auto_detect')}{Colors.END}")
            return problem
    
    def handle_favorites_quick(solutions):
        """Quick favorites management with shortcuts"""
        while True:
            user_input = get_input("prompt_action")
            
            if not user_input:
                break
            elif user_input.lower() == 'v':
                handle_favorites()
            elif user_input.lower().startswith('f') and user_input[1:].isdigit():
                idx = int(user_input[1:]) - 1
                if 0 <= idx < len(solutions):
                    principle = solutions[idx].principle
                    if principle in innovator.favorites:
                        innovator.favorites.remove(principle)
                        print(f"{Colors.RED}{t.get('msg_removed_favorite')} {principle}{Colors.END}")
                    else:
                        innovator.favorites.add(principle)
                        print(f"{Colors.GREEN}{t.get('msg_added_favorite')} {principle}{Colors.END}")
                    innovator._save_favorites()
                else:
                    print(f"{Colors.RED}{t.get('msg_invalid_choice')}{Colors.END}")
            else:
                print(f"{Colors.RED}{t.get('msg_invalid_choice')}{Colors.END}")
    
    def handle_more_options():
        """Simplified secondary menu"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{t.get('more_title')}{Colors.END}")
        print(f"{Colors.GREEN}  1. {t.get('more_favorites')}    2. {t.get('more_history')}    3. {t.get('more_settings')}{Colors.END}")
        print(f"{Colors.GREEN}  4. {t.get('more_statistics')}  5. {t.get('more_back')}{Colors.END}")
        
        choice = get_input("settings_choose")
        
        if choice == "1":
            handle_favorites()
        elif choice == "2":
            handle_history()
        elif choice == "3":
            handle_settings()
        elif choice == "4":
            handle_statistics()
        elif choice == "5":
            return
        else:
            print(f"{Colors.RED}{t.get('msg_invalid_choice')}{Colors.END}")
            handle_more_options()
    
    def handle_export(solutions):
        """Handle solution export"""
        if not solutions:
            print(f"{Colors.RED}{t.get('export_no_solutions')}{Colors.END}")
            return
        
        # Quick export with smart defaults
        print(f"\n{Colors.BOLD}{Colors.BLUE}{t.get('export_title')}{Colors.END}")
        format_choice = get_input("prompt_export_format")
        
        format_type = "txt" if format_choice == "2" else "json"
        
        show_loading(t.get("loading_export"))
        export_content = innovator.export_solutions(solutions, format_type)
        
        # Save to file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"triz_solutions_{timestamp}.{format_type}"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(export_content)
            print(f"{Colors.GREEN}{t.get('export_success')}: {filename}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}{t.get('export_failed')}: {e}{Colors.END}")
    
    def handle_favorites():
        """Handle favorites management"""
        favorites = innovator.favorites
        if not favorites:
            print(f"{Colors.YELLOW}📝 Favorites is empty{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}⭐ Favorite Principles (Total: {len(favorites)}){Colors.END}")
        for i, principle in enumerate(favorites, 1):
            print(f"{Colors.CYAN}{i}. {principle}{Colors.END}")
    
    def handle_history():
        """Handle history view"""
        history = innovator.get_history(15)
        if not history:
            print(f"{Colors.YELLOW}📝 No history records available{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}📈 Recent Analysis Records{Colors.END}")
        for i, record in enumerate(history, 1):
            rating_display = f"⭐{record['rating']}" if record['rating'] else "Not rated"
            print(f"{Colors.CYAN}{i}. {record['timestamp']} - {record['problem'][:50]}...{Colors.END}")
            print(f"   {Colors.YELLOW}Solutions: {record['solution_count']} | Rating: {rating_display}{Colors.END}")
    
    def handle_settings():
        """Handle system settings"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}⚙️ System Settings{Colors.END}")
        print(f"{Colors.GREEN}Current configuration:{Colors.END}")
        for key, value in innovator.config.items():
            print(f"  {Colors.CYAN}{key}: {Colors.YELLOW}{value}{Colors.END}")
        
        print(f"\n{Colors.GREEN}1. Modify max solutions  2. Toggle history  3. Return{Colors.END}")
        choice = get_input("Select operation", Colors.YELLOW)
        
        if choice == "1":
            try:
                new_max = int(get_input("Enter max solutions (1-10)", Colors.YELLOW))
                if 1 <= new_max <= 10:
                    innovator.config["max_solutions"] = new_max
                    innovator._save_config()
                    print(f"{Colors.GREEN}✅ Settings saved{Colors.END}")
                else:
                    print(f"{Colors.RED}❌ Value out of range{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}❌ Input format error{Colors.END}")
        elif choice == "2":
            innovator.config["enable_history"] = not innovator.config["enable_history"]
            innovator._save_config()
            status = "enabled" if innovator.config["enable_history"] else "disabled"
            print(f"{Colors.GREEN}✅ History {status}{Colors.END}")
    
    def handle_statistics():
        """Handle usage statistics"""
        stats = innovator.get_statistics()
        print(f"\n{Colors.BOLD}{Colors.GREEN}📋 Usage Statistics{Colors.END}")
        print(f"{Colors.CYAN}Total sessions: {Colors.YELLOW}{stats['total_sessions']}{Colors.END}")
        print(f"{Colors.CYAN}Rated sessions: {Colors.YELLOW}{stats['rated_sessions']}{Colors.END}")
        if stats['rated_sessions'] > 0:
            print(f"{Colors.CYAN}Average rating: {Colors.YELLOW}{stats['average_rating']:.1f}/5{Colors.END}")
        print(f"{Colors.CYAN}Favorite principles: {Colors.YELLOW}{stats['favorites_count']}{Colors.END}")
    
    # Main loop
    clear_screen()
    print_header()
    
    current_solutions = []
    
    while True:
        print_menu()
        choice = get_input("prompt_choice").strip().lower()
        
        if choice == "0":
            print(f"\n{Colors.GREEN}{t.get('msg_thank_you')}{Colors.END}")
            break
        elif choice == "l":
            # Language toggle
            new_lang = innovator.toggle_language()
            lang_name = "English" if new_lang == "en" else "中文"
            print(f"\n{Colors.GREEN}🌐 Language switched to {lang_name}{Colors.END}")
            clear_screen()
            print_header()
            continue
        elif choice == "1":
            problem = smart_analyze_input()
            if problem:
                show_loading(t.get("loading_analyzing"))
                current_solutions = innovator.analyze_problem(problem)
                print_solutions(current_solutions, "solutions_analysis")
                handle_favorites_quick(current_solutions)
                
        elif choice == "2":
            problem = smart_analyze_input()
            if problem:
                show_loading(t.get("loading_brainstorm"))
                current_solutions = innovator.brainstorm(problem)
                print_solutions(current_solutions, "solutions_brainstorm")
                handle_favorites_quick(current_solutions)
                
        elif choice == "3":
            handle_export(current_solutions)
        elif choice == "4":
            handle_more_options()
        else:
            print(f"{Colors.RED}{t.get('msg_invalid_choice')}{Colors.END}")
        
        if choice in ["1", "2", "3", "4"]:
            input(f"\n{Colors.YELLOW}{t.get('prompt_continue')}{Colors.END}")
            clear_screen()
            print_header()

if __name__ == "__main__":
    main()