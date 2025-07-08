# 将原有的TRIZ核心代码提取为模块
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
        # 在Vercel环境中，避免写入文件系统
        self.is_serverless = os.environ.get('VERCEL') or os.environ.get('LAMBDA_RUNTIME_DIR')
        
        if self.is_serverless:
            # 无服务器环境：不创建文件，使用内存存储
            self.data_dir = None
            self.history_file = None
            self.favorites_file = None
            self.config_file = None
            self.history = []
            self.favorites = set()
            self.config = {
                "max_solutions": 5,
                "enable_history": False,  # 无服务器环境禁用历史
                "auto_save": False,
                "export_format": "json",
                "language": "en"
            }
        else:
            # 本地环境：正常文件操作
            self.data_dir = Path.home() / ".triz_innovator_web"
            self.data_dir.mkdir(exist_ok=True)
            self.history_file = self.data_dir / "history.pkl"
            self.favorites_file = self.data_dir / "favorites.pkl"
            self.config_file = self.data_dir / "config.json"
            self.history: List[ProblemSession] = self._load_history()
            self.favorites: Set[str] = self._load_favorites()
            self.config = self._load_config()
        
        self.principles = self._load_principles()
        self.contradiction_matrix = self._load_matrix()
        self.parameter_keywords = self._load_parameter_keywords()
        self.problem_categories = self._load_problem_categories()
    
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
            3: {
                "name": "局部质量", "description": "使对象的不同部分具有不同功能",
                "detailed": "从均匀结构转变为非均匀结构，使对象或系统的各个部分具有各自最适合的功能",
                "examples": ["人体工学设计", "差异化服务", "定制化功能", "局部优化"],
                "category": "结构优化", "keywords": ["差异", "定制", "局部", "专用", "适配"]
            },
            6: {
                "name": "通用性", "description": "使对象能够执行多种功能",
                "detailed": "使对象能执行多种功能，从而不需要其他对象",
                "examples": ["多功能工具", "通用接口", "平台化设计", "标准化组件"],
                "category": "功能优化", "keywords": ["通用", "多功能", "万能", "标准", "兼容"]
            },
            15: {
                "name": "动态性", "description": "使对象或系统能够自动适应工作的最佳状态",
                "detailed": "对象的特性应改变，以便在工作的每个阶段都是最佳的；将对象分成能够相互移动的部分",
                "examples": ["自适应系统", "动态调整", "智能响应", "弹性伸缩"],
                "category": "适应性优化", "keywords": ["动态", "自适应", "调整", "变化", "响应"]
            },
            25: {
                "name": "自服务", "description": "对象应该自己为自己服务",
                "detailed": "使对象自己为自己服务，执行辅助和维修操作",
                "examples": ["自动化", "自修复", "自适应", "自主管理"],
                "category": "自动化优化", "keywords": ["自动", "自主", "自服务", "自修复", "自适应"]
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
            ("自动化", "成本"): [25, 26, 27, 35], ("智能化", "可靠性"): [15, 23, 25, 35],
            ("易用性", "功能性"): [6, 15, 27, 32], ("灵活性", "稳定性"): [15, 32, 35, 40]
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
            "效率": ["效率", "性能", "生产率", "吞吐量", "产能"],
            "易用性": ["易用", "简单", "直观", "友好", "便捷"],
            "功能性": ["功能", "特性", "能力", "用途", "作用"]
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
        
        if self.is_serverless:
            return default_config
            
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return {**default_config, **json.load(f)}
        except Exception:
            pass
        return default_config
    
    def _load_history(self) -> List[ProblemSession]:
        """加载历史记录"""
        if self.is_serverless:
            return []
            
        try:
            if self.history_file.exists():
                with open(self.history_file, 'rb') as f:
                    return pickle.load(f)
        except Exception:
            pass
        return []
    
    def _load_favorites(self) -> Set[str]:
        """加载收藏夹"""
        if self.is_serverless:
            return set()
            
        try:
            if self.favorites_file.exists():
                with open(self.favorites_file, 'rb') as f:
                    return pickle.load(f)
        except Exception:
            pass
        return set()
    
    def _save_history(self):
        """保存历史记录"""
        if self.is_serverless or not self.config.get("enable_history", True):
            return
            
        try:
            with open(self.history_file, 'wb') as f:
                pickle.dump(self.history[-100:], f)
        except Exception:
            pass
    
    def _save_favorites(self):
        """保存收藏夹"""
        if self.is_serverless:
            return
            
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
                worsening = worsening or "复杂性"
        
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
            "设计问题": [1, 3, 15, 27, 35],
            "成本问题": [27, 35, 1, 2, 40],
            "用户问题": [6, 15, 25, 27, 35],
            "质量问题": [1, 2, 15, 35, 40]
        }
        
        return recommendations.get(problem_category, [1, 2, 15, 27, 35])
    
    def _generate_solution(self, problem: str, principle_data: dict, pid: int, improving: str, worsening: str) -> Solution:
        """生成解决方案"""
        confidence = self._calculate_confidence(problem, principle_data, improving, worsening)
        relevance = self._calculate_relevance(problem, principle_data)
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
        
        problem_lower = problem.lower()
        keyword_matches = sum(1 for kw in principle_data["keywords"] if kw in problem_lower)
        keyword_bonus = min(0.3, keyword_matches * 0.1)
        
        param_bonus = 0.1 if (improving.lower() in str(principle_data["keywords"]).lower() or 
                             worsening.lower() in str(principle_data["keywords"]).lower()) else 0
        
        return min(0.95, base_confidence + keyword_bonus + param_bonus)
    
    def _calculate_relevance(self, problem: str, principle_data: dict) -> float:
        """计算相关性"""
        problem_lower = problem.lower()
        
        keyword_score = sum(1 for kw in principle_data["keywords"] if kw in problem_lower)
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
        
        problem_category = self._categorize_problem(problem)
        relevant_principles = self._get_smart_recommendations(problem, "", "")
        
        solutions = []
        for pid in relevant_principles:
            if pid in self.principles:
                principle_data = self.principles[pid]
                solution = self._generate_solution(problem, principle_data, pid, "", "")
                solutions.append(solution)
        
        return sorted(solutions, key=lambda x: (x.confidence + x.relevance_score) / 2, reverse=True)[:num_solutions]
    
    def export_solutions(self, solutions: List[Solution], format_type: str = "json") -> str:
        """导出解决方案"""
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
    
    def remove_from_favorites(self, principle_name: str):
        """从收藏夹移除"""
        self.favorites.discard(principle_name)
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
    
    def search_principles(self, query: str) -> List[dict]:
        """搜索原理"""
        results = []
        query_lower = query.lower()
        
        for pid, principle_data in self.principles.items():
            if (query_lower in principle_data["name"].lower() or
                query_lower in principle_data["description"].lower() or
                any(query_lower in keyword.lower() for keyword in principle_data["keywords"]) or
                any(query_lower in example.lower() for example in principle_data["examples"])):
                
                results.append({
                    "id": pid,
                    "name": principle_data["name"],
                    "description": principle_data["description"],
                    "category": principle_data["category"],
                    "relevance": self._calculate_search_relevance(query_lower, principle_data)
                })
        
        return sorted(results, key=lambda x: x["relevance"], reverse=True)
    
    def _calculate_search_relevance(self, query: str, principle_data: dict) -> float:
        """计算搜索相关性"""
        score = 0.0
        
        if query in principle_data["name"].lower():
            score += 1.0
        if query in principle_data["description"].lower():
            score += 0.5
        
        keyword_matches = sum(1 for keyword in principle_data["keywords"] if query in keyword.lower())
        score += keyword_matches * 0.3
        
        example_matches = sum(1 for example in principle_data["examples"] if query in example.lower())
        score += example_matches * 0.2
        
        return score