# 🚀 InnovateTRIZ - AI-Enhanced TRIZ Innovation Tool

*[English](README.md) | [中文](README.zh-CN.md)*

---

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

**🚀 Start your innovation journey with InnovateTRIZ! | 开始您的创新之旅！**