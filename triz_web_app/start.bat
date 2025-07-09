@echo off
chcp 65001 >nul

echo 🚀 TRIZ助手 - Web版启动中...

REM 检查Python版本
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

REM 检查并创建虚拟环境
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 📚 安装依赖包...
pip install -r requirements.txt

REM 启动应用
echo 🌐 启动Web应用...
echo 📱 访问地址: http://localhost:5000
echo ⚠️  按 Ctrl+C 停止服务
echo.

cd backend && python app.py