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

class TRIZTranslations:
    """TRIZ双语翻译系统"""
    
    TEXTS = {
        "en": {
            "app_title": "🚀 InnovateTRIZ",
            "app_subtitle": "AI-powered intelligent problem-solving solution generator",
            "language_toggle": "中文",
            "analyze_button": "Analyze Problem",
            "brainstorm_button": "Brainstorm Solutions", 
            "export_button": "Export Results",
            "problem_placeholder": "Describe your technical problem here...",
            "improving_param": "Parameter to improve (optional)",
            "worsening_param": "Parameter that might worsen (optional)",
            "no_solutions": "No solutions found",
            "loading": "Analyzing...",
            "principle": "Principle",
            "description": "Description",
            "examples": "Examples",
            "confidence": "Confidence",
            "category": "Category",
            "analysis_complete": "Analysis complete!",
            "analysis_failed": "Analysis failed",
            "brainstorm_complete": "Brainstorm complete!",
            "brainstorm_failed": "Brainstorm failed",
            "network_error": "Network error, please try again later",
            "enter_problem": "Please enter problem description",
            "no_solutions_to_export": "No solutions available for export",
            "export_success": "Export successful!",
            "export_failed": "Export failed",
            "export_error": "Export error occurred",
            "select_export_format": "Select Export Format",
            "json_format": "JSON Format",
            "text_format": "Text Format",
            "cancel": "Cancel",
            "operation_failed": "Operation failed",
            "no_history": "No history available",
            "solutions": " solutions",
            "detailed_explanation": "Detailed Explanation",
            "relevance": "Relevance",
            "nav_analyze": "Smart Analysis",
            "nav_brainstorm": "Brainstorm",
            "nav_history": "History",
            "nav_principles": "Principles",
            "feature_analysis": "Smart Analysis",
            "feature_analysis_desc": "AI automatically detects technical parameters and precisely matches contradiction matrix",
            "feature_innovation": "Innovation Solutions",
            "feature_innovation_desc": "Generate multi-dimensional solutions based on 40 TRIZ principles",
            "feature_scoring": "Smart Scoring",
            "feature_scoring_desc": "Dual scoring system for confidence and relevance",
            "btn_start_analysis": "Start Analysis",
            "btn_browse_principles": "Browse Principles",
            "loading_analyzing": "Analyzing with AI and TRIZ matrix...",
            "loading_brainstorm": "Generating creative solutions...",
            "language_switched": "Language switched successfully",
            "analyze_title": "Smart Contradiction Analysis",
            "analyze_desc": "Enter your technical problem, AI will automatically identify parameters and generate solutions",
            "problem_label": "Problem Description",
            "improving_label": "Parameter to improve",
            "worsening_label": "Parameter that might worsen",
            "analyze_btn_text": "Start Analysis",
            "solutions_title": "Solutions",
            "export_text": "Export",
            "brainstorm_title": "AI Brainstorm",
            "brainstorm_desc": "Quickly generate multi-angle innovative solutions",
            "brainstorm_problem_label": "Problem Description",
            "solution_count_label": "Number of Solutions",
            "brainstorm_btn_text": "Start Brainstorm",
            "innovation_title": "Innovation Solutions",
            "export_brainstorm_text": "Export",
            "history_title": "History",
            "history_desc": "View your analysis history and statistics",
            "total_sessions_label": "Total Sessions",
            "avg_rating_label": "Average Rating",
            "favorites_label": "Favorite Principles",
            "recent_analysis": "Recent Analysis Records",
            "principles_title": "TRIZ Principles Library",
            "principles_desc": "Browse complete 40 TRIZ invention principles",
            "loading_text": "AI is analyzing...",
            "improving_placeholder": "e.g.: battery life, performance, quality (optional auto-detect)",
            "worsening_placeholder": "e.g.: thickness, cost, complexity (optional auto-detect)",
            "brainstorm_placeholder": "Describe the problem you need to solve...",
            "search_placeholder": "Search principles...",
            "option_3_solutions": "3 solutions",
            "option_5_solutions": "5 solutions",
            "option_8_solutions": "8 solutions",
            "option_10_solutions": "10 solutions"
        },
        "zh": {
            "app_title": "🚀 TRIZ助手",
            "app_subtitle": "基于AI和TRIZ理论的智能问题解决方案生成器",
            "language_toggle": "English",
            "analyze_button": "分析问题",
            "brainstorm_button": "头脑风暴",
            "export_button": "导出结果", 
            "problem_placeholder": "请描述您的技术问题...",
            "improving_param": "需要改善的参数（可选）",
            "worsening_param": "可能恶化的参数（可选）",
            "no_solutions": "未找到解决方案",
            "loading": "分析中...",
            "principle": "原理",
            "description": "描述", 
            "examples": "示例",
            "confidence": "置信度",
            "category": "类别",
            "analysis_complete": "分析完成！",
            "analysis_failed": "分析失败",
            "brainstorm_complete": "头脑风暴完成！",
            "brainstorm_failed": "头脑风暴失败",
            "network_error": "网络错误，请稍后重试",
            "enter_problem": "请输入问题描述",
            "no_solutions_to_export": "没有可导出的解决方案",
            "export_success": "导出成功！",
            "export_failed": "导出失败",
            "export_error": "导出时发生错误",
            "select_export_format": "选择导出格式",
            "json_format": "JSON格式",
            "text_format": "文本格式",
            "cancel": "取消",
            "operation_failed": "操作失败",
            "no_history": "暂无历史记录",
            "solutions": "个解决方案",
            "detailed_explanation": "详细说明",
            "relevance": "相关性",
            "nav_analyze": "智能分析",
            "nav_brainstorm": "头脑风暴",
            "nav_history": "历史记录",
            "nav_principles": "原理库",
            "feature_analysis": "智能分析",
            "feature_analysis_desc": "AI自动检测技术参数，精准匹配矛盾矩阵",
            "feature_innovation": "创新方案",
            "feature_innovation_desc": "基于40个TRIZ原理生成多维度解决方案",
            "feature_scoring": "智能评分",
            "feature_scoring_desc": "置信度和相关性双重评分体系",
            "btn_start_analysis": "开始分析",
            "btn_browse_principles": "浏览原理",
            "loading_analyzing": "基于AI和TRIZ矩阵分析中...",
            "loading_brainstorm": "生成创意解决方案中...",
            "language_switched": "语言切换成功",
            "analyze_title": "智能矛盾分析",
            "analyze_desc": "输入您的技术问题，AI将自动识别参数并生成解决方案",
            "problem_label": "问题描述",
            "improving_label": "需要改善的参数",
            "worsening_label": "可能恶化的参数",
            "analyze_btn_text": "开始分析",
            "solutions_title": "解决方案",
            "export_text": "导出",
            "brainstorm_title": "AI头脑风暴",
            "brainstorm_desc": "快速生成多角度创新解决方案",
            "brainstorm_problem_label": "问题描述",
            "solution_count_label": "解决方案数量",
            "brainstorm_btn_text": "开始头脑风暴",
            "innovation_title": "创新方案",
            "export_brainstorm_text": "导出",
            "history_title": "历史记录",
            "history_desc": "查看您的分析历史和统计信息",
            "total_sessions_label": "总分析次数",
            "avg_rating_label": "平均评分",
            "favorites_label": "收藏原理",
            "recent_analysis": "最近的分析记录",
            "principles_title": "TRIZ原理库",
            "principles_desc": "浏览完整的40个TRIZ发明原理",
            "loading_text": "AI正在分析中...",
            "improving_placeholder": "例如：续航、性能、质量（可留空自动检测）",
            "worsening_placeholder": "例如：厚度、成本、复杂性（可留空自动检测）",
            "brainstorm_placeholder": "描述您需要解决的问题...",
            "search_placeholder": "搜索原理...",
            "option_3_solutions": "3个方案",
            "option_5_solutions": "5个方案",
            "option_8_solutions": "8个方案",
            "option_10_solutions": "10个方案"
        }
    }

class AdvancedTRIZInnovator:
    def __init__(self, language="zh"):
        # 在Vercel环境中，避免写入文件系统
        self.is_serverless = os.environ.get('VERCEL') or os.environ.get('LAMBDA_RUNTIME_DIR')
        self.current_language = language
        
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
                "language": language
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
        """完整的40个TRIZ发明原理数据库（双语）"""
        return {
            1: {
                "name": {"zh": "分割", "en": "Segmentation"},
                "description": {"zh": "将对象分成独立的部分", "en": "Divide an object into independent parts"},
                "detailed": {"zh": "将物体分解为独立的部分，使各部分易于拆卸和组装，增加分解的程度", "en": "Divide an object into independent parts, make parts easy to disassemble and assemble"},
                "examples": {"zh": ["模块化设计", "可拆卸家具", "组件化软件架构", "微服务架构"], "en": ["Modular design", "Detachable furniture", "Component architecture", "Microservices"]},
                "category": {"zh": "结构优化", "en": "Structure Optimization"},
                "keywords": ["模块", "组件", "分离", "独立", "拆分"]
            },
            2: {
                "name": {"zh": "抽取", "en": "Taking out"},
                "description": {"zh": "从对象中取出干扰的部分或特性", "en": "Separate an interfering part or property from an object"},
                "detailed": {"zh": "分离出有害或不必要的部分/特性，或相反，单独分离出有用的部分/特性", "en": "Separate harmful or unnecessary parts, or conversely, separate useful parts"},
                "examples": {"zh": ["噪音消除", "杂质过滤", "核心功能提取", "异常处理隔离"], "en": ["Noise cancellation", "Impurity filtering", "Core function extraction", "Exception isolation"]},
                "category": {"zh": "功能优化", "en": "Function Optimization"},
                "keywords": ["提取", "分离", "净化", "隔离", "筛选"]
            },
            3: {
                "name": {"zh": "局部质量", "en": "Local quality"},
                "description": {"zh": "使对象的不同部分具有不同功能", "en": "Make different parts of an object have different functions"},
                "detailed": {"zh": "从均匀结构转变为非均匀结构，使对象或系统的各个部分具有各自最适合的功能", "en": "Change from uniform to non-uniform structure, make each part optimal for its function"},
                "examples": {"zh": ["人体工学设计", "差异化服务", "定制化功能", "局部优化"], "en": ["Ergonomic design", "Differentiated services", "Customized functions", "Local optimization"]},
                "category": {"zh": "结构优化", "en": "Structure Optimization"},
                "keywords": ["差异", "定制", "局部", "专用", "适配"]
            },
            4: {
                "name": {"zh": "不对称", "en": "Asymmetry"},
                "description": {"zh": "从对称转变为不对称", "en": "Change from symmetrical to asymmetrical"},
                "detailed": {"zh": "如果对象已经是不对称的，增加其不对称程度", "en": "If an object is already asymmetrical, increase its degree of asymmetry"},
                "examples": {"zh": ["不对称设计", "差异化布局", "非均匀分布", "倾斜结构"], "en": ["Asymmetric design", "Differential layout", "Non-uniform distribution", "Tilted structure"]},
                "category": {"zh": "结构优化", "en": "Structure Optimization"},
                "keywords": ["不对称", "倾斜", "偏移", "非均匀", "差异"]
            },
            5: {
                "name": {"zh": "合并", "en": "Merging"},
                "description": {"zh": "合并相同或相似的对象", "en": "Merge identical or similar objects"},
                "detailed": {"zh": "在空间上合并相同的对象或设计用于相同操作的对象", "en": "Merge identical objects spatially or design objects for identical operations"},
                "examples": {"zh": ["功能合并", "资源整合", "统一接口", "集成设计"], "en": ["Function merging", "Resource integration", "Unified interface", "Integrated design"]},
                "category": {"zh": "结构优化", "en": "Structure Optimization"},
                "keywords": ["合并", "整合", "统一", "集成", "融合"]
            },
            6: {
                "name": {"zh": "通用性", "en": "Universality"},
                "description": {"zh": "使对象能够执行多种功能", "en": "Make an object perform multiple functions"},
                "detailed": {"zh": "使对象能执行多种功能，从而不需要其他对象", "en": "Make an object perform multiple functions, eliminating the need for other objects"},
                "examples": {"zh": ["多功能工具", "通用接口", "平台化设计", "标准化组件"], "en": ["Multi-function tools", "Universal interface", "Platform design", "Standardized components"]},
                "category": {"zh": "功能优化", "en": "Function Optimization"},
                "keywords": ["通用", "多功能", "万能", "标准", "兼容"]
            },
            7: {
                "name": {"zh": "嵌套", "en": "Nesting"},
                "description": {"zh": "将一个对象放置在另一个对象内部", "en": "Place one object inside another"},
                "detailed": {"zh": "将一个对象放在另一个对象的内部，后者再放在第三个对象的内部，以此类推", "en": "Place one object inside another, which is placed inside a third, and so on"},
                "examples": {"zh": ["嵌套结构", "层次设计", "递归调用", "分层架构"], "en": ["Nested structure", "Hierarchical design", "Recursive calls", "Layered architecture"]},
                "category": {"zh": "结构优化", "en": "Structure Optimization"},
                "keywords": ["嵌套", "层次", "递归", "包含", "内嵌"]
            },
            8: {
                "name": {"zh": "反重量", "en": "Anti-weight"},
                "description": {"zh": "通过与其他对象合并来补偿重量", "en": "Compensate for weight by merging with other objects"},
                "detailed": {"zh": "通过与具有升力的其他对象合并来补偿对象的重量", "en": "Compensate for the weight of an object by merging with other objects that provide lift"},
                "examples": {"zh": ["重量平衡", "浮力利用", "反向力", "平衡设计"], "en": ["Weight balance", "Buoyancy utilization", "Counter force", "Balanced design"]},
                "category": {"zh": "力学优化", "en": "Mechanical Optimization"},
                "keywords": ["平衡", "浮力", "反向", "补偿", "抵消"]
            },
            9: {
                "name": {"zh": "预先反作用", "en": "Preliminary anti-action"},
                "description": {"zh": "提前进行反作用", "en": "Perform anti-action in advance"},
                "detailed": {"zh": "如果需要同时进行一个作用和它的反作用，预先进行反作用", "en": "If an action and its counter-action are needed, perform the counter-action in advance"},
                "examples": {"zh": ["预防措施", "预先补偿", "反向操作", "提前处理"], "en": ["Preventive measures", "Pre-compensation", "Reverse operation", "Advance processing"]},
                "category": {"zh": "控制优化", "en": "Control Optimization"},
                "keywords": ["预先", "反向", "预防", "补偿", "提前"]
            },
            10: {
                "name": {"zh": "预先作用", "en": "Preliminary action"},
                "description": {"zh": "预先进行所需的变化", "en": "Perform required changes in advance"},
                "detailed": {"zh": "预先进行对象的全部或部分所需变化", "en": "Perform the required change of an object (fully or partially) in advance"},
                "examples": {"zh": ["预处理", "预配置", "预加载", "提前准备"], "en": ["Preprocessing", "Pre-configuration", "Preloading", "Advance preparation"]},
                "category": {"zh": "控制优化", "en": "Control Optimization"},
                "keywords": ["预先", "提前", "预处理", "准备", "预配置"]
            },
            11: {
                "name": {"zh": "事先缓解", "en": "Beforehand cushioning"},
                "description": {"zh": "事先准备应急手段", "en": "Prepare emergency means beforehand"},
                "detailed": {"zh": "通过事先准备应急手段来补偿对象相对较低的可靠性", "en": "Compensate for relatively low reliability of an object by emergency means prepared beforehand"},
                "examples": {"zh": ["备份系统", "应急预案", "故障转移", "冗余设计"], "en": ["Backup systems", "Emergency plans", "Failover", "Redundant design"]},
                "category": {"zh": "可靠性优化", "en": "Reliability Optimization"},
                "keywords": ["备份", "应急", "冗余", "故障转移", "预案"]
            },
            12: {
                "name": {"zh": "等势", "en": "Equipotentiality"},
                "description": {"zh": "在重力场中改变工作条件", "en": "Change working conditions in gravitational field"},
                "detailed": {"zh": "在重力场中改变工作条件，以消除升降对象的需要", "en": "Change working conditions in gravitational field to eliminate the need to raise or lower objects"},
                "examples": {"zh": ["水平移动", "等高设计", "重力平衡", "水平传输"], "en": ["Horizontal movement", "Level design", "Gravity balance", "Horizontal transport"]},
                "category": {"zh": "力学优化", "en": "Mechanical Optimization"},
                "keywords": ["水平", "等高", "平衡", "重力", "传输"]
            },
            13: {
                "name": {"zh": "反向", "en": "Inversion"},
                "description": {"zh": "颠倒行动或过程", "en": "Invert the action or process"},
                "detailed": {"zh": "颠倒用来解决问题的行动：使可动部分固定，使固定部分可动", "en": "Invert the action used to solve the problem: make movable parts fixed and fixed parts movable"},
                "examples": {"zh": ["反向思维", "逆向工程", "颠倒顺序", "反向操作"], "en": ["Reverse thinking", "Reverse engineering", "Inverted order", "Reverse operation"]},
                "category": {"zh": "思维优化", "en": "Thinking Optimization"},
                "keywords": ["反向", "逆向", "颠倒", "相反", "倒置"]
            },
            14: {
                "name": {"zh": "球面化", "en": "Spheroidality"},
                "description": {"zh": "用球面代替线性部分", "en": "Replace linear parts with spherical ones"},
                "detailed": {"zh": "用弯曲的表面代替直线部分；用球体、椭球体、抛物面等代替立方体", "en": "Replace linear parts with curved surfaces; replace cubes with spheres, ellipsoids, paraboloids"},
                "examples": {"zh": ["圆滑设计", "球形结构", "曲面界面", "圆角处理"], "en": ["Smooth design", "Spherical structure", "Curved interface", "Rounded corners"]},
                "category": {"zh": "结构优化", "en": "Structure Optimization"},
                "keywords": ["球形", "圆滑", "曲面", "圆角", "弯曲"]
            },
            15: {
                "name": {"zh": "动态性", "en": "Dynamics"},
                "description": {"zh": "使对象或系统能够自动适应工作的最佳状态", "en": "Make an object or system adapt automatically to optimal working conditions"},
                "detailed": {"zh": "对象的特性应改变，以便在工作的每个阶段都是最佳的；将对象分成能够相互移动的部分", "en": "Characteristics of an object should change to be optimal in each stage of operation; divide an object into parts capable of movement"},
                "examples": {"zh": ["自适应系统", "动态调整", "智能响应", "弹性伸缩"], "en": ["Adaptive systems", "Dynamic adjustment", "Smart response", "Elastic scaling"]},
                "category": {"zh": "适应性优化", "en": "Adaptability Optimization"},
                "keywords": ["动态", "自适应", "调整", "变化", "响应"]
            },
            16: {
                "name": {"zh": "部分或过度的行动", "en": "Partial or excessive actions"},
                "description": {"zh": "采用部分或过度的行动", "en": "Use partial or excessive actions"},
                "detailed": {"zh": "如果很难获得100%的期望效果，应该获得稍多一点或稍少一点", "en": "If it's hard to get 100% of desired effect, get slightly more or slightly less"},
                "examples": {"zh": ["过度设计", "分步实现", "渐进优化", "阶段达成"], "en": ["Over-engineering", "Step-by-step implementation", "Progressive optimization", "Phased achievement"]},
                "category": {"zh": "控制优化", "en": "Control Optimization"},
                "keywords": ["部分", "过度", "渐进", "阶段", "分步"]
            },
            17: {
                "name": {"zh": "另一个维度", "en": "Another dimension"},
                "description": {"zh": "移到另一个维度", "en": "Move to another dimension"},
                "detailed": {"zh": "沿着垂直于给定方向的路径移动或布置对象", "en": "Move or arrange objects along a path perpendicular to the given direction"},
                "examples": {"zh": ["三维思维", "垂直布局", "立体设计", "多维空间"], "en": ["3D thinking", "Vertical layout", "Spatial design", "Multi-dimensional space"]},
                "category": {"zh": "空间优化", "en": "Spatial Optimization"},
                "keywords": ["维度", "垂直", "立体", "空间", "方向"]
            },
            18: {
                "name": {"zh": "机械振动", "en": "Mechanical vibration"},
                "description": {"zh": "使对象振动", "en": "Make an object oscillate"},
                "detailed": {"zh": "使对象振动；增加其振动频率；使用超声频率；使用共振频率", "en": "Make an object oscillate; increase its frequency; use ultrasonic frequency; use resonant frequency"},
                "examples": {"zh": ["振动清理", "超声波", "共振技术", "振动传输"], "en": ["Vibration cleaning", "Ultrasonic", "Resonance technology", "Vibration transmission"]},
                "category": {"zh": "物理优化", "en": "Physical Optimization"},
                "keywords": ["振动", "频率", "超声", "共振", "波动"]
            },
            19: {
                "name": {"zh": "周期性行动", "en": "Periodic action"},
                "description": {"zh": "用周期性行动代替连续行动", "en": "Replace continuous action with periodic action"},
                "detailed": {"zh": "用周期性或脉冲行动代替连续行动；如果行动已经是周期性的，改变其周期性", "en": "Replace continuous action with periodic or pulsing action; if already periodic, change the periodicity"},
                "examples": {"zh": ["定期维护", "脉冲信号", "周期检查", "间歇操作"], "en": ["Regular maintenance", "Pulse signals", "Periodic checks", "Intermittent operation"]},
                "category": {"zh": "时间优化", "en": "Time Optimization"},
                "keywords": ["周期", "脉冲", "间歇", "定期", "循环"]
            },
            20: {
                "name": {"zh": "有用行动的连续性", "en": "Continuity of useful action"},
                "description": {"zh": "连续进行有用的行动", "en": "Carry on useful action continuously"},
                "detailed": {"zh": "连续进行工作，使对象的所有部分始终以全负荷工作", "en": "Carry on work continuously; make all parts of an object work at full load all the time"},
                "examples": {"zh": ["持续运行", "全负荷工作", "连续生产", "不间断服务"], "en": ["Continuous operation", "Full load work", "Continuous production", "Uninterrupted service"]},
                "category": {"zh": "效率优化", "en": "Efficiency Optimization"},
                "keywords": ["连续", "持续", "全负荷", "不间断", "满载"]
            },
            21: {
                "name": {"zh": "急速", "en": "Skipping"},
                "description": {"zh": "高速执行有害或危险的过程", "en": "Conduct a process or certain stages at high speed"},
                "detailed": {"zh": "高速执行有害或危险的过程", "en": "Conduct a process, or certain stages (e.g., harmful or hazardous ones) at high speed"},
                "examples": {"zh": ["快速处理", "高速通过", "急速完成", "瞬间操作"], "en": ["Rapid processing", "High-speed transit", "Quick completion", "Instant operation"]},
                "category": {"zh": "速度优化", "en": "Speed Optimization"},
                "keywords": ["快速", "高速", "急速", "瞬间", "迅速"]
            },
            22: {
                "name": {"zh": "变害为利", "en": "Blessing in disguise"},
                "description": {"zh": "利用有害因素获得积极效果", "en": "Use harmful factors to achieve positive effects"},
                "detailed": {"zh": "利用有害因素获得积极效果；通过有害因素与其他有害因素结合来消除有害性", "en": "Use harmful factors to achieve positive effects; eliminate harm by combining with other harmful factors"},
                "examples": {"zh": ["废物利用", "负负得正", "转危为机", "化害为益"], "en": ["Waste utilization", "Two negatives make positive", "Turn crisis into opportunity", "Transform harm into benefit"]},
                "category": {"zh": "转化优化", "en": "Transformation Optimization"},
                "keywords": ["转化", "利用", "废物", "化害", "变废"]
            },
            23: {
                "name": {"zh": "反馈", "en": "Feedback"},
                "description": {"zh": "引入反馈", "en": "Introduce feedback"},
                "detailed": {"zh": "引入反馈以改进过程或行动；如果反馈已经存在，改变其幅度或影响", "en": "Introduce feedback to improve a process or action; if feedback exists, change its magnitude or influence"},
                "examples": {"zh": ["反馈控制", "闭环系统", "自我调节", "监控反馈"], "en": ["Feedback control", "Closed-loop system", "Self-regulation", "Monitoring feedback"]},
                "category": {"zh": "控制优化", "en": "Control Optimization"},
                "keywords": ["反馈", "闭环", "监控", "调节", "回路"]
            },
            24: {
                "name": {"zh": "中介", "en": "Intermediary"},
                "description": {"zh": "使用中介对象或过程", "en": "Use an intermediary object or process"},
                "detailed": {"zh": "使用中介对象或过程；暂时将对象与另一个容易去除的对象合并", "en": "Use an intermediary object or process; merge one object temporarily with another easily removed one"},
                "examples": {"zh": ["中间层", "代理模式", "缓冲区", "转接器"], "en": ["Intermediate layer", "Proxy pattern", "Buffer", "Adapter"]},
                "category": {"zh": "结构优化", "en": "Structure Optimization"},
                "keywords": ["中介", "代理", "缓冲", "中间", "转接"]
            },
            25: {
                "name": {"zh": "自服务", "en": "Self-service"},
                "description": {"zh": "对象应该自己为自己服务", "en": "Make an object serve itself"},
                "detailed": {"zh": "使对象自己为自己服务，执行辅助和维修操作", "en": "Make an object serve itself by performing auxiliary and repair operations"},
                "examples": {"zh": ["自动化", "自修复", "自适应", "自主管理"], "en": ["Automation", "Self-repair", "Self-adaptation", "Self-management"]},
                "category": {"zh": "自动化优化", "en": "Automation Optimization"},
                "keywords": ["自动", "自主", "自服务", "自修复", "自适应"]
            },
            26: {
                "name": {"zh": "复制", "en": "Copying"},
                "description": {"zh": "使用简单而廉价的复制品", "en": "Use simple and inexpensive copies"},
                "detailed": {"zh": "使用简单而廉价的复制品代替不可获得、昂贵或脆弱的对象", "en": "Use simple and inexpensive copies instead of unavailable, expensive, or fragile objects"},
                "examples": {"zh": ["模拟器", "虚拟现实", "数字孪生", "仿真模型"], "en": ["Simulator", "Virtual reality", "Digital twin", "Simulation model"]},
                "category": {"zh": "替代优化", "en": "Substitution Optimization"},
                "keywords": ["复制", "模拟", "仿真", "虚拟", "孪生"]
            },
            27: {
                "name": {"zh": "廉价替代", "en": "Cheap short-living objects"},
                "description": {"zh": "用便宜的对象代替昂贵的对象", "en": "Replace expensive objects with cheap ones"},
                "detailed": {"zh": "用便宜的对象来代替昂贵的，在某些特性（如使用寿命）上有所损失", "en": "Replace expensive objects with cheap ones, compromising on certain qualities (like service life)"},
                "examples": {"zh": ["开源替代", "低成本方案", "简化版本", "经济型设计"], "en": ["Open source alternatives", "Low-cost solutions", "Simplified versions", "Economy design"]},
                "category": {"zh": "成本优化", "en": "Cost Optimization"},
                "keywords": ["廉价", "替代", "经济", "低成本", "简化"]
            },
            28: {
                "name": {"zh": "机械系统替代", "en": "Mechanics substitution"},
                "description": {"zh": "用其他感知系统替代机械系统", "en": "Replace mechanical systems with sensory ones"},
                "detailed": {"zh": "用光学、声学或嗅觉系统替代机械系统", "en": "Replace mechanical systems with optical, acoustic, or olfactory systems"},
                "examples": {"zh": ["传感器检测", "光学识别", "声音监控", "智能感知"], "en": ["Sensor detection", "Optical recognition", "Sound monitoring", "Smart sensing"]},
                "category": {"zh": "技术替代", "en": "Technology Substitution"},
                "keywords": ["传感器", "光学", "声学", "感知", "检测"]
            },
            29: {
                "name": {"zh": "气动和液压结构", "en": "Pneumatics and hydraulics"},
                "description": {"zh": "使用气动和液压结构", "en": "Use pneumatic and hydraulic constructions"},
                "detailed": {"zh": "用气体和液体部分代替对象的固体部分", "en": "Use gas and liquid parts instead of solid parts of an object"},
                "examples": {"zh": ["气动控制", "液压系统", "流体驱动", "软体机器人"], "en": ["Pneumatic control", "Hydraulic systems", "Fluid drive", "Soft robotics"]},
                "category": {"zh": "物理替代", "en": "Physical Substitution"},
                "keywords": ["气动", "液压", "流体", "软体", "柔性"]
            },
            30: {
                "name": {"zh": "柔性壳体和薄膜", "en": "Flexible shells and thin films"},
                "description": {"zh": "使用柔性壳体和薄膜", "en": "Use flexible shells and thin films"},
                "detailed": {"zh": "用柔性壳体和薄膜代替通常的结构", "en": "Use flexible shells and thin films instead of three-dimensional structures"},
                "examples": {"zh": ["薄膜材料", "柔性屏幕", "软包装", "弹性外壳"], "en": ["Film materials", "Flexible screens", "Soft packaging", "Elastic shells"]},
                "category": {"zh": "材料优化", "en": "Material Optimization"},
                "keywords": ["柔性", "薄膜", "软包装", "弹性", "膜结构"]
            },
            31: {
                "name": {"zh": "多孔材料", "en": "Porous materials"},
                "description": {"zh": "使对象多孔或添加多孔元素", "en": "Make objects porous or add porous elements"},
                "detailed": {"zh": "使对象多孔或添加多孔元素；如果对象已经多孔，预先用某种物质填充孔隙", "en": "Make objects porous or add porous elements; if already porous, fill pores with some substance"},
                "examples": {"zh": ["多孔结构", "蜂窝材料", "泡沫材料", "过滤材料"], "en": ["Porous structure", "Honeycomb materials", "Foam materials", "Filter materials"]},
                "category": {"zh": "材料优化", "en": "Material Optimization"},
                "keywords": ["多孔", "蜂窝", "泡沫", "过滤", "透气"]
            },
            32: {
                "name": {"zh": "颜色改变", "en": "Color changes"},
                "description": {"zh": "改变对象或其环境的颜色", "en": "Change the color of an object or its external environment"},
                "detailed": {"zh": "改变对象或其环境的颜色；改变对象或其环境的透明度", "en": "Change the color of an object or its environment; change the transparency of an object or its environment"},
                "examples": {"zh": ["颜色编码", "状态指示", "可视化反馈", "透明度调节"], "en": ["Color coding", "Status indication", "Visual feedback", "Transparency adjustment"]},
                "category": {"zh": "视觉优化", "en": "Visual Optimization"},
                "keywords": ["颜色", "透明", "可视", "编码", "指示"]
            },
            33: {
                "name": {"zh": "同质性", "en": "Homogeneity"},
                "description": {"zh": "使与主要对象相互作用的对象由相同的材料制成", "en": "Make objects interacting with a given object of the same material"},
                "detailed": {"zh": "使与主要对象相互作用的对象由相同的材料制成", "en": "Make objects interacting with a given object of the same material or material with identical properties"},
                "examples": {"zh": ["材料统一", "兼容性设计", "同质化", "一致性"], "en": ["Material unification", "Compatibility design", "Homogenization", "Consistency"]},
                "category": {"zh": "材料优化", "en": "Material Optimization"},
                "keywords": ["同质", "统一", "兼容", "一致", "相同"]
            },
            34: {
                "name": {"zh": "丢弃和再生", "en": "Discarding and recovering"},
                "description": {"zh": "使完成功能的部分消失", "en": "Make portions of an object disappear after fulfilling their functions"},
                "detailed": {"zh": "使完成功能的对象部分消失或在过程中直接修改", "en": "Make portions of an object that have fulfilled their functions disappear or modify them during the process"},
                "examples": {"zh": ["一次性组件", "可降解材料", "临时结构", "消耗性部件"], "en": ["Disposable components", "Degradable materials", "Temporary structures", "Consumable parts"]},
                "category": {"zh": "生命周期优化", "en": "Lifecycle Optimization"},
                "keywords": ["一次性", "降解", "临时", "消耗", "消失"]
            },
            35: {
                "name": {"zh": "参数改变", "en": "Parameter changes"},
                "description": {"zh": "改变对象的物理或化学状态", "en": "Change the physical or chemical state of an object"},
                "detailed": {"zh": "改变对象的物理或化学状态；改变浓度或稠度；改变柔性的程度；改变温度", "en": "Change physical or chemical state; change concentration or consistency; change degree of flexibility; change temperature"},
                "examples": {"zh": ["状态转换", "参数调整", "相变利用", "属性修改"], "en": ["State transition", "Parameter adjustment", "Phase change utilization", "Property modification"]},
                "category": {"zh": "状态优化", "en": "State Optimization"},
                "keywords": ["状态", "参数", "转换", "调整", "修改"]
            },
            36: {
                "name": {"zh": "相变", "en": "Phase transitions"},
                "description": {"zh": "利用相变现象", "en": "Use phenomena occurring during phase transitions"},
                "detailed": {"zh": "利用相变过程中发生的现象，如体积变化、热量释放或吸收", "en": "Use phenomena occurring during phase transitions: volume changes, heat liberation or absorption"},
                "examples": {"zh": ["相变材料", "热管技术", "蒸发冷却", "凝固成型"], "en": ["Phase change materials", "Heat pipe technology", "Evaporative cooling", "Solidification forming"]},
                "category": {"zh": "物理优化", "en": "Physical Optimization"},
                "keywords": ["相变", "体积", "热量", "蒸发", "凝固"]
            },
            37: {
                "name": {"zh": "热膨胀", "en": "Thermal expansion"},
                "description": {"zh": "利用材料的热膨胀或收缩", "en": "Use thermal expansion or contraction of materials"},
                "detailed": {"zh": "利用材料的热膨胀或收缩；如果已经使用热膨胀，使用各种材料的不同热膨胀系数", "en": "Use thermal expansion or contraction; if already using thermal expansion, use different coefficients of thermal expansion"},
                "examples": {"zh": ["热敏元件", "双金属片", "热补偿", "温控开关"], "en": ["Thermal elements", "Bimetallic strips", "Thermal compensation", "Temperature switches"]},
                "category": {"zh": "热学优化", "en": "Thermal Optimization"},
                "keywords": ["热膨胀", "收缩", "热敏", "双金属", "温控"]
            },
            38: {
                "name": {"zh": "强氧化剂", "en": "Strong oxidants"},
                "description": {"zh": "使用强氧化剂", "en": "Use strong oxidants"},
                "detailed": {"zh": "用富氧空气代替普通空气；用氧气代替富氧空气；用电离辐射作用于空气或氧气", "en": "Replace common air with oxygen-enriched air; replace enriched air with oxygen; use ionizing radiation on air or oxygen"},
                "examples": {"zh": ["氧化处理", "富氧燃烧", "等离子体", "电离辐射"], "en": ["Oxidation treatment", "Oxygen-enriched combustion", "Plasma", "Ionizing radiation"]},
                "category": {"zh": "化学优化", "en": "Chemical Optimization"},
                "keywords": ["氧化", "富氧", "等离子", "电离", "辐射"]
            },
            39: {
                "name": {"zh": "惰性气氛", "en": "Inert atmosphere"},
                "description": {"zh": "用惰性气氛代替普通环境", "en": "Replace a normal environment with an inert one"},
                "detailed": {"zh": "用惰性气氛代替普通环境；在真空中进行过程", "en": "Replace a normal environment with an inert one; add neutral parts or inert additives to an object"},
                "examples": {"zh": ["惰性保护", "真空环境", "充氮保护", "无氧处理"], "en": ["Inert protection", "Vacuum environment", "Nitrogen protection", "Oxygen-free processing"]},
                "category": {"zh": "环境优化", "en": "Environment Optimization"},
                "keywords": ["惰性", "真空", "充氮", "无氧", "保护"]
            },
            40: {
                "name": {"zh": "复合材料", "en": "Composite materials"},
                "description": {"zh": "用复合材料代替均质材料", "en": "Replace homogeneous materials with composite ones"},
                "detailed": {"zh": "从均质材料转向复合材料", "en": "Change from homogeneous to composite materials"},
                "examples": {"zh": ["复合材料", "多层结构", "混合系统", "组合方案"], "en": ["Composite materials", "Multi-layer structure", "Hybrid systems", "Combined solutions"]},
                "category": {"zh": "材料优化", "en": "Material Optimization"},
                "keywords": ["复合", "多层", "混合", "组合", "复杂"]
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
            ("维护", "复杂性"): [1, 2, 25, 35], ("可靠性", "复杂性"): [1, 11, 25, 27],
            ("性能", "成本"): [1, 2, 27, 35], ("效率", "安全"): [11, 23, 25, 35]
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
            "可靠性": ["可靠", "稳定", "故障", "失效", "持久"],
            "维护": ["维护", "保养", "修理", "维修", "检修"],
            "自动化": ["自动", "手动", "机械", "智能", "控制"],
            "功能性": ["功能", "特性", "能力", "用途", "作用"]
        }
    
    def _load_problem_categories(self) -> Dict[str, List[str]]:
        """问题分类关键词"""
        return {
            "Technical Problem": ["技术", "系统", "设备", "机器", "算法", "软件"],
            "Design Problem": ["设计", "外观", "结构", "布局", "界面", "造型"],
            "Cost Problem": ["成本", "价格", "费用", "预算", "经济", "投资"],
            "User Problem": ["用户", "客户", "体验", "需求", "满意", "使用"],
            "Quality Problem": ["质量", "缺陷", "故障", "错误", "问题", "不良"]
        }
    
    def set_language(self, language: str):
        """设置语言"""
        if language in ["zh", "en"]:
            self.current_language = language
            self.config["language"] = language
            if not self.is_serverless:
                self._save_config()
    
    def get_text(self, key: str) -> str:
        """获取当前语言的文本"""
        return TRIZTranslations.TEXTS[self.current_language].get(key, key)
    
    def get_principle_text(self, principle_data: dict, field: str) -> str:
        """获取原理的当前语言文本"""
        if isinstance(principle_data[field], dict):
            return principle_data[field].get(self.current_language, principle_data[field].get("zh", ""))
        return principle_data[field]
    
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
    
    def _save_config(self):
        """保存配置"""
        if self.is_serverless:
            return
            
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
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
        
        return "General Problem"
    
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
            "Technical Problem": [1, 2, 15, 35, 40],
            "Design Problem": [1, 3, 15, 27, 35],
            "Cost Problem": [27, 35, 1, 2, 40],
            "User Problem": [6, 15, 25, 27, 35],
            "Quality Problem": [1, 2, 15, 35, 40]
        }
        
        return recommendations.get(problem_category, [1, 2, 15, 27, 35])
    
    def _generate_solution(self, problem: str, principle_data: dict, pid: int, improving: str, worsening: str) -> Solution:
        """生成解决方案"""
        confidence = self._calculate_confidence(problem, principle_data, improving, worsening)
        relevance = self._calculate_relevance(problem, principle_data)
        description = self._generate_description(problem, principle_data, improving, worsening)
        
        return Solution(
            principle=self.get_principle_text(principle_data, "name"),
            principle_id=pid,
            description=description,
            detailed_explanation=self.get_principle_text(principle_data, "detailed"),
            examples=self.get_principle_text(principle_data, "examples"),
            confidence=confidence,
            relevance_score=relevance,
            category=self.get_principle_text(principle_data, "category"),
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
        
        examples = self.get_principle_text(principle_data, "examples")
        if isinstance(examples, list):
            example_score = sum(1 for ex in examples 
                              if any(word in problem_lower for word in ex.lower().split()))
        else:
            example_score = 0
        
        return min(1.0, (keyword_score * 0.2 + example_score * 0.1))
    
    def _generate_description(self, problem: str, principle_data: dict, improving: str, worsening: str) -> str:
        """生成解决方案描述"""
        principle_name = self.get_principle_text(principle_data, "name")
        base_desc = self.get_principle_text(principle_data, "description")
        
        if "软件" in problem or "系统" in problem or "software" in problem.lower() or "system" in problem.lower():
            if "分割" in principle_name or "Segmentation" in principle_name:
                if self.current_language == "zh":
                    return f"将{problem}进行模块化拆分，每个模块专注于特定功能，降低{worsening}同时提升{improving}"
                else:
                    return f"Apply modular decomposition to {problem}, with each module focusing on specific functions, reducing {worsening} while improving {improving}"
            elif "动态性" in principle_name or "Dynamics" in principle_name:
                if self.current_language == "zh":
                    return f"为{problem}添加自适应机制，根据实际需求动态调整，平衡{improving}和{worsening}"
                else:
                    return f"Add adaptive mechanisms to {problem}, dynamically adjusting according to actual needs, balancing {improving} and {worsening}"
        
        if self.current_language == "zh":
            return f"运用{principle_name}原理（{base_desc}）来解决{problem}，重点改善{improving}与{worsening}的平衡"
        else:
            return f"Apply {principle_name} principle ({base_desc}) to solve {problem}, focusing on improving the balance between {improving} and {worsening}"
    
    def brainstorm(self, problem: str, num_solutions: int = None) -> List[Solution]:
        """智能头脑风暴"""
        if num_solutions is None:
            num_solutions = self.config.get("max_solutions", 5)
        
        problem_category = self._categorize_problem(problem)
        detected_params = self._smart_parameter_detection(problem)
        
        relevant_principles = self._get_smart_recommendations(problem, "", "")
        
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
            "language": self.current_language,
            "solutions": [sol.to_dict() for sol in solutions]
        }
        return json.dumps(export_data, ensure_ascii=False, indent=2)
    
    def _export_txt(self, solutions: List[Solution]) -> str:
        """导出为文本格式"""
        lines = []
        title = "TRIZ Innovation Solutions Report" if self.current_language == "en" else "TRIZ创新解决方案报告"
        lines.append(title)
        lines.append("=" * 50)
        lines.append(f"Generation time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Solutions: {len(solutions)}")
        lines.append(f"Language: {self.current_language}")
        lines.append("")
        
        for i, sol in enumerate(solutions, 1):
            solution_label = f"Solution {i}" if self.current_language == "en" else f"方案 {i}"
            lines.append(f"{solution_label}: {sol.principle}")
            lines.append(f"{self.get_text('description')}: {sol.description}")
            lines.append(f"{self.get_text('confidence')}: {sol.confidence:.1%}")
            lines.append(f"{self.get_text('examples')}: {', '.join(sol.examples) if isinstance(sol.examples, list) else sol.examples}")
            lines.append("-" * 30)
            lines.append("")
        
        return "\n".join(lines)
    
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