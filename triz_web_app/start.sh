#!/bin/bash

# TRIZ Web App 启动脚本

echo "🚀 TRIZ创新算法助手 - Web版启动中..."

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3，请先安装 Python 3.7+"
    exit 1
fi

# 检查并创建虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📚 安装依赖包..."
pip install -r requirements.txt

# 启动应用
echo "🌐 启动Web应用..."
echo "📱 访问地址: http://localhost:5000"
echo "⚠️  按 Ctrl+C 停止服务"
echo ""

cd backend && python app.py