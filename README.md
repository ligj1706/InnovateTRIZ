# 🚀 InnovateTRIZ - AI-Enhanced TRIZ Innovation Tool

*[English](README.md) | [中文](README.zh-CN.md)*

---

## English Version

### 📖 About InnovateTRIZ

**InnovateTRIZ** is an AI-enhanced TRIZ (Theory of Inventive Problem Solving) innovation tool that combines classical TRIZ methodology with modern artificial intelligence to provide intelligent problem-solving solutions.

### ✨ Key Features

- **🧠 AI-Enhanced Analysis**: Automatic parameter detection and contradiction matrix matching
- **💡 Smart Brainstorming**: Multi-dimensional solution generation based on problem classification
- **📱 Modern Web Interface**: Responsive design with beautiful UI/UX
- **📊 Intelligent Scoring**: Dual scoring system with confidence and relevance metrics
- **📈 Data Management**: History tracking, favorites, and usage statistics
- **🔍 Smart Search**: Intelligent TRIZ principles search and filtering
- **📤 Export Functions**: JSON/TXT format export capabilities
- **🎯 40 TRIZ Principles**: Complete database with detailed explanations and examples

### 🏗️ Project Structure

```
InnovateTRIZ/
├── triz_innovation_pro.py      # Professional CLI version
├── triz_web_app/               # Web application
│   ├── backend/                # Flask backend
│   │   ├── app.py             # Main application
│   │   └── triz_core.py       # TRIZ core algorithms
│   ├── frontend/              # Frontend files
│   │   ├── templates/         # HTML templates
│   │   └── static/            # CSS/JS assets
│   ├── requirements.txt       # Python dependencies
│   ├── start.sh              # Linux/Mac startup script
│   └── start.bat             # Windows startup script
└── README.md                  # This documentation
```

### 🚀 Quick Start

#### Option 1: Web Version (Recommended)

**Linux/Mac:**
```bash
cd triz_web_app
./start.sh
```

**Windows:**
```cmd
cd triz_web_app
start.bat
```

Then open your browser and visit: **http://localhost:5000**

#### Option 2: CLI Version

```bash
python3 triz_innovation_pro.py
```

### 💻 Usage Guide

#### 🎯 Smart Contradiction Analysis

1. Navigate to "Smart Analysis"
2. Describe your technical problem
3. Optionally specify improving/worsening parameters (auto-detection available)
4. Click "Start Analysis" to get solutions

**Example Problems:**
- "Mobile phone needs larger battery but must remain thin"
- "Software has rich features but users find it complex"
- "High quality requirements but need to control costs"

#### 💡 AI Brainstorming

1. Go to "Brainstorming" tab
2. Describe your problem
3. Select number of solutions needed
4. Click "Start Brainstorming"

#### 📊 Solution Interpretation

Each solution includes:
- **TRIZ Principle Name**: Based on 40 classical inventive principles
- **Confidence Score**: AI-assessed solution feasibility
- **Relevance Score**: Match degree with the problem
- **Application Examples**: Real-world use cases
- **Detailed Explanation**: In-depth principle description

### 🛠️ Technology Stack

#### Backend
- **Flask**: Lightweight web framework
- **Python**: Core algorithm implementation
- **TRIZ Algorithms**: 40 inventive principles + extended contradiction matrix
- **AI Enhancement**: Smart parameter detection and recommendation

#### Frontend
- **HTML5**: Semantic structure
- **CSS3**: Modern styling and animations
- **JavaScript ES6+**: Interactive logic
- **Responsive Design**: Multi-device support
- **REST API**: Frontend-backend separation

### 📝 API Documentation

#### Analyze Problem
```http
POST /api/analyze
Content-Type: application/json

{
  "problem": "Problem description",
  "improving": "Improving parameter",
  "worsening": "Worsening parameter"
}
```

#### Brainstorm
```http
POST /api/brainstorm
Content-Type: application/json

{
  "problem": "Problem description",
  "num_solutions": 5
}
```

### 🌟 Advantages Over Traditional TRIZ Tools

| Feature | Traditional Tools | InnovateTRIZ |
|---------|------------------|--------------|
| Parameter Detection | Manual lookup | AI auto-detection |
| Interface | Legacy desktop software | Modern web interface |
| Learning Curve | Steep | Gentle |
| Real-time Analysis | Offline use | Real-time analysis |
| Data Analytics | None | Smart scoring + statistics |
| Cross-platform | Limited | Any device |

### 🎯 Use Cases

- **Product Innovation**: New product design and feature optimization
- **Technical Problem Solving**: Engineering challenges and technical bottlenecks
- **Software Development**: Architecture design and performance optimization
- **User Experience**: Interface and interaction improvements
- **Business Innovation**: Service models and process optimization
- **Education & Research**: TRIZ theory learning and practice

### 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

### 📄 License

This project is licensed under the MIT License.

---

## 中文版本

### 📖 关于 InnovateTRIZ

**InnovateTRIZ** 是一个AI增强的TRIZ（发明问题解决理论）创新工具，将经典TRIZ方法论与现代人工智能技术相结合，提供智能化的问题解决方案。

### ✨ 核心特性

- **🧠 AI智能分析**: 自动参数检测和矛盾矩阵匹配
- **💡 智能头脑风暴**: 基于问题分类的多维度方案生成
- **📱 现代Web界面**: 响应式设计，精美的用户界面
- **📊 智能评分**: 置信度+相关性双重评分体系
- **📈 数据管理**: 历史记录、收藏夹、使用统计
- **🔍 智能搜索**: TRIZ原理的智能搜索和筛选
- **📤 导出功能**: 支持JSON/TXT格式导出
- **🎯 40个TRIZ原理**: 完整的原理库，包含详细说明和示例

### 🏗️ 项目结构

```
InnovateTRIZ/
├── triz_innovation_pro.py      # 专业命令行版本
├── triz_web_app/               # Web应用程序
│   ├── backend/                # Flask后端
│   │   ├── app.py             # 主应用程序
│   │   └── triz_core.py       # TRIZ核心算法
│   ├── frontend/              # 前端文件
│   │   ├── templates/         # HTML模板
│   │   └── static/            # CSS/JS资源
│   ├── requirements.txt       # Python依赖包
│   ├── start.sh              # Linux/Mac启动脚本
│   └── start.bat             # Windows启动脚本
└── README.md                  # 项目文档
```

### 🚀 快速开始

#### 方式1: Web版本（推荐）

**Linux/Mac用户:**
```bash
cd triz_web_app
./start.sh
```

**Windows用户:**
```cmd
cd triz_web_app
start.bat
```

然后打开浏览器访问: **http://localhost:5000**

#### 方式2: 命令行版本

```bash
python3 triz_innovation_pro.py
```

### 💻 使用指南

#### 🎯 智能矛盾分析

1. 点击"智能分析"选项卡
2. 输入您的技术问题描述
3. 可选择输入改善/恶化参数（支持自动检测）
4. 点击"开始分析"获得解决方案

**示例问题:**
- "手机需要更大电池但要保持轻薄"
- "软件功能丰富但用户觉得复杂"
- "产品质量要求高但成本要控制"

#### 💡 AI头脑风暴

1. 进入"头脑风暴"选项卡
2. 描述您的问题
3. 选择需要的解决方案数量
4. 点击"开始头脑风暴"

#### 📊 解决方案解读

每个解决方案包含：
- **TRIZ原理名称**: 基于40个经典发明原理
- **置信度**: AI评估的方案可行性
- **相关性**: 与问题的匹配程度
- **应用示例**: 实际应用案例
- **详细说明**: 原理的深入解释

### 🛠️ 技术架构

#### 后端技术
- **Flask**: 轻量级Web框架
- **Python**: 核心算法实现
- **TRIZ算法**: 40个发明原理 + 扩展矛盾矩阵
- **AI增强**: 智能参数检测和推荐

#### 前端技术
- **HTML5**: 语义化结构
- **CSS3**: 现代样式和动画
- **JavaScript ES6+**: 交互逻辑
- **响应式设计**: 多设备支持
- **REST API**: 前后端分离架构

### 📝 API文档

#### 分析问题
```http
POST /api/analyze
Content-Type: application/json

{
  "problem": "问题描述",
  "improving": "改善参数",
  "worsening": "恶化参数"
}
```

#### 头脑风暴
```http
POST /api/brainstorm
Content-Type: application/json

{
  "problem": "问题描述",
  "num_solutions": 5
}
```

### 🌟 相比传统TRIZ工具的优势

| 特性 | 传统工具 | InnovateTRIZ |
|------|----------|--------------|
| 参数检测 | 手动查表 | AI自动检测 |
| 界面设计 | 传统桌面软件 | 现代Web界面 |
| 学习曲线 | 陡峭 | 平缓 |
| 实时分析 | 离线使用 | 实时分析 |
| 数据分析 | 无 | 智能评分+统计 |
| 跨平台 | 限制 | 任何设备 |

### 🎯 适用场景

- **产品创新**: 新产品设计和功能优化
- **技术攻关**: 工程技术难题解决
- **软件开发**: 架构设计和性能优化
- **用户体验**: 界面和交互改进
- **商业创新**: 服务模式和流程优化
- **教学研究**: TRIZ理论学习和实践

### 🤝 贡献指南

欢迎贡献代码！请随时提交issues和pull requests。

### 📄 许可证

本项目采用MIT许可证。

---

**🚀 Start your innovation journey with InnovateTRIZ! | 开始您的创新之旅！**