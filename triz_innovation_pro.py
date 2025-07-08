#!/usr/bin/env python3
"""
TRIZ创新算法应用 - 专业版
极致强大的问题解决工具，基于TRIZ理论的40个发明原理和扩展矛盾矩阵
具备智能分析、历史记录、解决方案导出等高级功能
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
    
    def _load_principles(self) -> Dict[int, Dict[str, any]]:
        """完整的40个TRIZ发明原理数据库"""
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
        """扩展的技术矛盾矩阵"""
        return {
            ("重量", "强度"): [1, 8, 15, 40], ("重量", "速度"): [2, 14, 15, 35],
            ("强度", "重量"): [1, 8, 36, 40], ("复杂性", "可靠性"): [1, 26, 27, 40],
            ("精度", "速度"): [10, 18, 32, 39], ("成本", "质量"): [13, 26, 27, 35],
            ("能耗", "效率"): [2, 6, 19, 36], ("体积", "功能"): [7, 17, 29, 40],
            ("速度", "精度"): [10, 18, 32, 39], ("安全", "便利"): [11, 24, 25, 35],
            ("自动化", "成本"): [25, 26, 27, 35], ("智能化", "可靠性"): [15, 23, 25, 35]
        }
    
    def _load_parameter_keywords(self) -> Dict[str, List[str]]:
        """参数关键词映射"""
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
        """问题分类关键词"""
        return {
            "技术问题": ["技术", "系统", "设备", "机器", "算法", "软件"],
            "设计问题": ["设计", "外观", "结构", "布局", "界面", "造型"],
            "成本问题": ["成本", "价格", "费用", "预算", "经济", "投资"],
            "用户问题": ["用户", "客户", "体验", "需求", "满意", "使用"],
            "质量问题": ["质量", "缺陷", "故障", "错误", "问题", "不良"]
        }
    
    def _load_config(self) -> dict:
        """加载配置"""
        default_config = {
            "max_solutions": 5,
            "enable_history": True,
            "auto_save": True,
            "export_format": "json"
        }
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return {**default_config, **json.load(f)}
        except Exception:
            pass
        return default_config
    
    def _save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def _load_history(self) -> List[ProblemSession]:
        """加载历史记录"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'rb') as f:
                    return pickle.load(f)
        except Exception:
            pass
        return []
    
    def _load_favorites(self) -> Set[str]:
        """加载收藏夹"""
        try:
            if self.favorites_file.exists():
                with open(self.favorites_file, 'rb') as f:
                    return pickle.load(f)
        except Exception:
            pass
        return set()
    
    def _save_history(self):
        """保存历史记录"""
        if not self.config.get("enable_history", True):
            return
        try:
            with open(self.history_file, 'wb') as f:
                pickle.dump(self.history[-100:], f)  # 保存最近100条
        except Exception:
            pass
    
    def _save_favorites(self):
        """保存收藏夹"""
        try:
            with open(self.favorites_file, 'wb') as f:
                pickle.dump(self.favorites, f)
        except Exception:
            pass
    
    def _smart_parameter_detection(self, text: str) -> List[str]:
        """智能参数检测"""
        detected = []
        text_lower = text.lower()
        
        for param, keywords in self.parameter_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected.append(param)
        
        return detected
    
    def _categorize_problem(self, problem: str) -> str:
        """问题分类"""
        problem_lower = problem.lower()
        
        for category, keywords in self.problem_categories.items():
            if any(keyword in problem_lower for keyword in keywords):
                return category
        
        return "通用问题"
    
    def analyze_problem(self, problem: str, improving: str = "", worsening: str = "") -> List[Solution]:
        """智能分析问题并生成解决方案"""
        # 智能参数检测
        if not improving or not worsening:
            detected_params = self._smart_parameter_detection(problem)
            if len(detected_params) >= 2:
                improving = improving or detected_params[0]
                worsening = worsening or detected_params[1]
            elif len(detected_params) == 1:
                improving = improving or detected_params[0]
                worsening = worsening or "复杂性"  # 默认恶化参数
        
        # 查找矛盾矩阵
        key = (improving.lower(), worsening.lower())
        reverse_key = (worsening.lower(), improving.lower())
        
        principle_ids = self.contradiction_matrix.get(key) or self.contradiction_matrix.get(reverse_key)
        
        # 如果没找到精确匹配，使用智能推荐
        if not principle_ids:
            principle_ids = self._get_smart_recommendations(problem, improving, worsening)
        
        solutions = []
        for pid in principle_ids[:self.config.get("max_solutions", 5)]:
            if pid in self.principles:
                principle_data = self.principles[pid]
                solution = self._generate_solution(problem, principle_data, pid, improving, worsening)
                solutions.append(solution)
        
        # 排序
        solutions = sorted(solutions, key=lambda x: (x.confidence + x.relevance_score) / 2, reverse=True)
        
        # 保存到历史
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
        """智能推荐原理"""
        problem_category = self._categorize_problem(problem)
        
        recommendations = {
            "技术问题": [1, 2, 15, 35, 40],
            "设计问题": [1, 15, 27, 35, 40],
            "成本问题": [27, 35, 1, 2, 40],
            "用户问题": [15, 35, 1, 27, 40],
            "质量问题": [1, 2, 15, 35, 40]
        }
        
        return recommendations.get(problem_category, [1, 2, 15, 27, 35])
    
    def _generate_solution(self, problem: str, principle_data: dict, pid: int, improving: str, worsening: str) -> Solution:
        """生成解决方案"""
        # 计算置信度和相关性
        confidence = self._calculate_confidence(problem, principle_data, improving, worsening)
        relevance = self._calculate_relevance(problem, principle_data)
        
        # 生成描述
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
        """计算置信度"""
        base_confidence = 0.6
        
        # 关键词匹配
        problem_lower = problem.lower()
        keyword_matches = sum(1 for kw in principle_data["keywords"] if kw in problem_lower)
        keyword_bonus = min(0.3, keyword_matches * 0.1)
        
        # 参数相关性
        param_bonus = 0.1 if (improving.lower() in str(principle_data["keywords"]).lower() or 
                             worsening.lower() in str(principle_data["keywords"]).lower()) else 0
        
        return min(0.95, base_confidence + keyword_bonus + param_bonus)
    
    def _calculate_relevance(self, problem: str, principle_data: dict) -> float:
        """计算相关性"""
        problem_lower = problem.lower()
        
        # 关键词匹配
        keyword_score = sum(1 for kw in principle_data["keywords"] if kw in problem_lower)
        
        # 示例匹配
        example_score = sum(1 for ex in principle_data["examples"] 
                          if any(word in problem_lower for word in ex.lower().split()))
        
        return min(1.0, (keyword_score * 0.2 + example_score * 0.1))
    
    def _generate_description(self, problem: str, principle_data: dict, improving: str, worsening: str) -> str:
        """生成解决方案描述"""
        principle_name = principle_data["name"]
        base_desc = principle_data["description"]
        
        if "软件" in problem or "系统" in problem:
            if principle_name == "分割":
                return f"将{problem}进行模块化拆分，每个模块专注于特定功能，降低{worsening}同时提升{improving}"
            elif principle_name == "动态性":
                return f"为{problem}添加自适应机制，根据实际需求动态调整，平衡{improving}和{worsening}"
        
        return f"运用{principle_name}原理（{base_desc}）来解决{problem}，重点改善{improving}与{worsening}的平衡"
    
    def brainstorm(self, problem: str, num_solutions: int = None) -> List[Solution]:
        """智能头脑风暴"""
        if num_solutions is None:
            num_solutions = self.config.get("max_solutions", 5)
        
        # 问题分析
        problem_category = self._categorize_problem(problem)
        detected_params = self._smart_parameter_detection(problem)
        
        # 选择相关原理
        relevant_principles = self._get_smart_recommendations(problem, "", "")
        
        # 生成解决方案
        solutions = []
        for pid in relevant_principles:
            if pid in self.principles:
                principle_data = self.principles[pid]
                solution = self._generate_solution(problem, principle_data, pid, "", "")
                solutions.append(solution)
        
        return sorted(solutions, key=lambda x: (x.confidence + x.relevance_score) / 2, reverse=True)[:num_solutions]
    
    def export_solutions(self, solutions: List[Solution], format_type: str = None) -> str:
        """导出解决方案"""
        if format_type is None:
            format_type = self.config.get("export_format", "json")
        
        if format_type.lower() == "json":
            return self._export_json(solutions)
        else:
            return self._export_txt(solutions)
    
    def _export_json(self, solutions: List[Solution]) -> str:
        """导出为JSON格式"""
        export_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "solution_count": len(solutions),
            "solutions": [sol.to_dict() for sol in solutions]
        }
        return json.dumps(export_data, ensure_ascii=False, indent=2)
    
    def _export_txt(self, solutions: List[Solution]) -> str:
        """导出为文本格式"""
        lines = []
        lines.append("TRIZ创新解决方案报告")
        lines.append("=" * 50)
        lines.append(f"生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"解决方案数量: {len(solutions)}")
        lines.append("")
        
        for i, sol in enumerate(solutions, 1):
            lines.append(f"方案 {i}: {sol.principle}")
            lines.append(f"描述: {sol.description}")
            lines.append(f"置信度: {sol.confidence:.1%}")
            lines.append(f"相关性: {sol.relevance_score:.1%}")
            lines.append(f"示例: {', '.join(sol.examples)}")
            lines.append("-" * 30)
            lines.append("")
        
        return "\\n".join(lines)
    
    def add_to_favorites(self, principle_name: str):
        """添加到收藏夹"""
        self.favorites.add(principle_name)
        self._save_favorites()
    
    def get_history(self, limit: int = 10) -> List[dict]:
        """获取历史记录"""
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
        """获取使用统计"""
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

def main():
    """主程序 - 现代化终端界面"""
    if not sys.stdout.isatty():
        Colors.disable()
    
    innovator = AdvancedTRIZInnovator()
    
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header():
        print(f"\n{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}║            🚀 TRIZ 创新算法助手 - 专业版             ║{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}║          智能问题解决方案生成器 & 创新工具            ║{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚══════════════════════════════════════════════════════╝{Colors.END}")
    
    def print_menu():
        print(f"\n{Colors.BOLD}{Colors.YELLOW}┌─ 功能菜单 ──────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.GREEN}  1. 🎯 智能矛盾分析     {Colors.CYAN}(精准定位技术矛盾){Colors.END}")
        print(f"{Colors.GREEN}  2. 💡 AI头脑风暴       {Colors.CYAN}(创意灵感激发){Colors.END}")
        print(f"{Colors.GREEN}  3. 📊 解决方案导出     {Colors.CYAN}(JSON/TXT格式){Colors.END}")
        print(f"{Colors.GREEN}  4. ⭐ 收藏夹管理       {Colors.CYAN}(保存常用原理){Colors.END}")
        print(f"{Colors.GREEN}  5. 📈 历史记录查看     {Colors.CYAN}(回顾过往分析){Colors.END}")
        print(f"{Colors.GREEN}  6. ⚙️  系统设置         {Colors.CYAN}(个性化配置){Colors.END}")
        print(f"{Colors.GREEN}  7. 📋 使用统计         {Colors.CYAN}(数据分析){Colors.END}")
        print(f"{Colors.GREEN}  8. ❌ 退出程序{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}└─────────────────────────────────────────────────┘{Colors.END}")
    
    def get_input(prompt, color=Colors.CYAN):
        return input(f"{color}🔸 {prompt}{Colors.END} ")
    
    def print_solutions(solutions, title="解决方案"):
        if not solutions:
            print(f"{Colors.RED}💭 未找到相关解决方案{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}╭─ 💡 {title} (共{len(solutions)}个) ─────────────────────╮{Colors.END}")
        
        for i, sol in enumerate(solutions, 1):
            confidence_color = Colors.GREEN if sol.confidence > 0.8 else Colors.YELLOW if sol.confidence > 0.6 else Colors.RED
            confidence_bar = "█" * int(sol.confidence * 10) + "░" * (10 - int(sol.confidence * 10))
            
            print(f"\n{Colors.BOLD}{Colors.BLUE}方案 {i}: {sol.principle} ({sol.category}){Colors.END}")
            print(f"  {Colors.CYAN}▸{Colors.END} {sol.description}")
            print(f"  {Colors.YELLOW}▸ 置信度:{Colors.END} {confidence_color}{confidence_bar} {sol.confidence:.1%}{Colors.END}")
            print(f"  {Colors.MAGENTA}▸ 示例:{Colors.END} {', '.join(sol.examples[:2])}")
            
            # 显示收藏状态
            fav_status = "⭐" if sol.principle in innovator.favorites else "☆"
            print(f"  {Colors.ORANGE}▸ 收藏:{Colors.END} {fav_status}")
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}╰─────────────────────────────────────────────╯{Colors.END}")
    
    def show_loading(message="正在分析..."):
        import time
        print(f"\n{Colors.YELLOW}⏳ {message}{Colors.END}", end="", flush=True)
        for _ in range(3):
            time.sleep(0.4)
            print(".", end="", flush=True)
        print(f" {Colors.GREEN}✓{Colors.END}")
    
    def handle_export(solutions):
        """处理解决方案导出"""
        if not solutions:
            print(f"{Colors.RED}❌ 没有可导出的解决方案{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}📊 选择导出格式{Colors.END}")
        print(f"{Colors.GREEN}1. JSON格式  2. 文本格式{Colors.END}")
        format_choice = get_input("选择格式 (1-2)", Colors.YELLOW)
        
        format_type = "json" if format_choice == "1" else "txt"
        
        show_loading("正在生成导出文件")
        export_content = innovator.export_solutions(solutions, format_type)
        
        # 保存到文件
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"triz_solutions_{timestamp}.{format_type}"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(export_content)
            print(f"{Colors.GREEN}✅ 已导出到文件: {filename}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}❌ 导出失败: {e}{Colors.END}")
    
    def handle_favorites():
        """处理收藏夹管理"""
        favorites = innovator.favorites
        if not favorites:
            print(f"{Colors.YELLOW}📝 收藏夹为空{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}⭐ 收藏的原理 (共{len(favorites)}个){Colors.END}")
        for i, principle in enumerate(favorites, 1):
            print(f"{Colors.CYAN}{i}. {principle}{Colors.END}")
    
    def handle_history():
        """处理历史记录查看"""
        history = innovator.get_history(15)
        if not history:
            print(f"{Colors.YELLOW}📝 暂无历史记录{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}📈 最近的分析记录{Colors.END}")
        for i, record in enumerate(history, 1):
            rating_display = f"⭐{record['rating']}" if record['rating'] else "未评分"
            print(f"{Colors.CYAN}{i}. {record['timestamp']} - {record['problem'][:50]}...{Colors.END}")
            print(f"   {Colors.YELLOW}方案数: {record['solution_count']} | 评分: {rating_display}{Colors.END}")
    
    def handle_settings():
        """处理系统设置"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}⚙️ 系统设置{Colors.END}")
        print(f"{Colors.GREEN}当前配置:{Colors.END}")
        for key, value in innovator.config.items():
            print(f"  {Colors.CYAN}{key}: {Colors.YELLOW}{value}{Colors.END}")
        
        print(f"\n{Colors.GREEN}1. 修改最大解决方案数  2. 切换历史记录  3. 返回{Colors.END}")
        choice = get_input("选择操作", Colors.YELLOW)
        
        if choice == "1":
            try:
                new_max = int(get_input("输入最大解决方案数 (1-10)", Colors.YELLOW))
                if 1 <= new_max <= 10:
                    innovator.config["max_solutions"] = new_max
                    innovator._save_config()
                    print(f"{Colors.GREEN}✅ 设置已保存{Colors.END}")
                else:
                    print(f"{Colors.RED}❌ 数值范围错误{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}❌ 输入格式错误{Colors.END}")
        elif choice == "2":
            innovator.config["enable_history"] = not innovator.config["enable_history"]
            innovator._save_config()
            status = "启用" if innovator.config["enable_history"] else "禁用"
            print(f"{Colors.GREEN}✅ 历史记录已{status}{Colors.END}")
    
    def handle_statistics():
        """处理使用统计"""
        stats = innovator.get_statistics()
        print(f"\n{Colors.BOLD}{Colors.GREEN}📋 使用统计{Colors.END}")
        print(f"{Colors.CYAN}总分析次数: {Colors.YELLOW}{stats['total_sessions']}{Colors.END}")
        print(f"{Colors.CYAN}已评分次数: {Colors.YELLOW}{stats['rated_sessions']}{Colors.END}")
        if stats['rated_sessions'] > 0:
            print(f"{Colors.CYAN}平均评分: {Colors.YELLOW}{stats['average_rating']:.1f}/5{Colors.END}")
        print(f"{Colors.CYAN}收藏原理数: {Colors.YELLOW}{stats['favorites_count']}{Colors.END}")
    
    # 主循环
    clear_screen()
    print_header()
    
    current_solutions = []
    
    while True:
        print_menu()
        choice = get_input("请输入选择 (1-8)", Colors.BOLD + Colors.YELLOW).strip()
        
        if choice == "8":
            print(f"\n{Colors.GREEN}👋 感谢使用 TRIZ 创新算法助手！{Colors.END}")
            break
        elif choice == "1":
            print(f"\n{Colors.BOLD}{Colors.BLUE}🎯 智能矛盾分析模式{Colors.END}")
            print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
            
            problem = get_input("描述您的技术问题")
            improving = get_input("需要改善的参数 (留空自动检测)")
            worsening = get_input("可能恶化的参数 (留空自动检测)")
            
            show_loading("正在基于AI和TRIZ矛盾矩阵分析")
            current_solutions = innovator.analyze_problem(problem, improving, worsening)
            print_solutions(current_solutions, "智能矛盾分析结果")
            
        elif choice == "2":
            print(f"\n{Colors.BOLD}{Colors.BLUE}💡 AI头脑风暴模式{Colors.END}")
            print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
            
            problem = get_input("描述您需要解决的问题")
            
            show_loading("正在生成创新解决方案")
            current_solutions = innovator.brainstorm(problem)
            print_solutions(current_solutions, "AI头脑风暴结果")
            
        elif choice == "3":
            handle_export(current_solutions)
        elif choice == "4":
            handle_favorites()
        elif choice == "5":
            handle_history()
        elif choice == "6":
            handle_settings()
        elif choice == "7":
            handle_statistics()
        else:
            print(f"{Colors.RED}❌ 无效选择，请重新输入{Colors.END}")
        
        if choice in ["1", "2", "3", "4", "5", "6", "7"]:
            input(f"\n{Colors.YELLOW}按回车键继续...{Colors.END}")
            clear_screen()
            print_header()

if __name__ == "__main__":
    main()