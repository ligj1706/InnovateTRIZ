from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import datetime
import os
import sys
from pathlib import Path

# 修复Vercel部署的路径问题
current_dir = os.path.dirname(os.path.abspath(__file__))
# 在Vercel环境中，需要正确设置路径
if 'VERCEL' in os.environ:
    # Vercel环境
    backend_dir = '/var/task/triz_web_app/backend'
    frontend_dir = '/var/task/triz_web_app/frontend'
else:
    # 本地环境
    backend_dir = current_dir
    frontend_dir = os.path.join(os.path.dirname(current_dir), 'frontend')

sys.path.append(backend_dir)

try:
    from triz_core import AdvancedTRIZInnovator
except ImportError:
    # 如果导入失败，创建一个简单的替代品
    class AdvancedTRIZInnovator:
        def __init__(self):
            self.favorites = set()
        
        def analyze_problem(self, problem, improving="", worsening=""):
            return []
        
        def brainstorm(self, problem, num_solutions=5):
            return []
        
        def export_solutions(self, solutions, format_type="json"):
            return "{}"
        
        def add_to_favorites(self, principle):
            self.favorites.add(principle)
        
        def get_history(self, limit=20):
            return []
        
        def get_statistics(self):
            return {"total_sessions": 0}

app = Flask(__name__, 
           template_folder=os.path.join(frontend_dir, 'templates'),
           static_folder=os.path.join(frontend_dir, 'static'))
CORS(app)

# 初始化TRIZ引擎
try:
    triz_engine = AdvancedTRIZInnovator()
except Exception as e:
    print(f"Warning: Failed to initialize TRIZ engine: {e}")
    triz_engine = AdvancedTRIZInnovator()  # 使用备用版本

@app.route('/')
def index():
    """主页"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>TRIZ Innovation Assistant</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .error {{ color: red; background: #fee; padding: 20px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 TRIZ Innovation Assistant</h1>
                <div class="error">
                    <h3>Template Loading Error</h3>
                    <p>Error: {str(e)}</p>
                    <p>The application is running, but templates cannot be loaded.</p>
                </div>
                <h3>Available API Endpoints:</h3>
                <ul>
                    <li>POST /api/analyze - Analyze problems</li>
                    <li>POST /api/brainstorm - Brainstorm solutions</li>
                    <li>GET /api/principles - Get all principles</li>
                </ul>
            </div>
        </body>
        </html>
        """

@app.route('/api/analyze', methods=['POST'])
def analyze_problem():
    """分析问题API"""
    try:
        data = request.get_json()
        problem = data.get('problem', '')
        improving = data.get('improving', '')
        worsening = data.get('worsening', '')
        
        if not problem:
            return jsonify({'error': '问题描述不能为空'}), 400
        
        # 调用TRIZ分析
        solutions = triz_engine.analyze_problem(problem, improving, worsening)
        
        # 转换为JSON格式
        result = {
            'problem': problem,
            'improving_param': improving,
            'worsening_param': worsening,
            'solutions': [sol.to_dict() if hasattr(sol, 'to_dict') else {} for sol in solutions],
            'timestamp': datetime.datetime.now().isoformat(),
            'solution_count': len(solutions)
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'分析失败: {str(e)}'}), 500

@app.route('/api/brainstorm', methods=['POST'])
def brainstorm():
    """头脑风暴API"""
    try:
        data = request.get_json()
        problem = data.get('problem', '')
        num_solutions = data.get('num_solutions', 5)
        
        if not problem:
            return jsonify({'error': '问题描述不能为空'}), 400
        
        # 调用头脑风暴
        solutions = triz_engine.brainstorm(problem, num_solutions)
        
        result = {
            'problem': problem,
            'solutions': [sol.to_dict() if hasattr(sol, 'to_dict') else {} for sol in solutions],
            'timestamp': datetime.datetime.now().isoformat(),
            'solution_count': len(solutions),
            'mode': 'brainstorm'
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'头脑风暴失败: {str(e)}'}), 500

@app.route('/api/export', methods=['POST'])
def export_solutions():
    """导出解决方案API"""
    try:
        data = request.get_json()
        solutions_data = data.get('solutions', [])
        format_type = data.get('format', 'json')
        
        # 简化导出功能
        export_content = json.dumps(solutions_data, ensure_ascii=False, indent=2)
        
        return jsonify({
            'content': export_content,
            'format': format_type,
            'filename': f'triz_solutions_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.{format_type}'
        })
    
    except Exception as e:
        return jsonify({'error': f'导出失败: {str(e)}'}), 500

@app.route('/api/favorites', methods=['GET', 'POST', 'DELETE'])
def manage_favorites():
    """收藏夹管理API"""
    try:
        if request.method == 'GET':
            favorites = list(triz_engine.favorites)
            return jsonify({'favorites': favorites})
        
        elif request.method == 'POST':
            data = request.get_json()
            principle = data.get('principle', '')
            if principle:
                triz_engine.add_to_favorites(principle)
                return jsonify({'message': f'已添加 {principle} 到收藏夹'})
            return jsonify({'error': '原理名称不能为空'}), 400
        
        elif request.method == 'DELETE':
            data = request.get_json()
            principle = data.get('principle', '')
            if principle:
                if hasattr(triz_engine, 'remove_from_favorites'):
                    triz_engine.remove_from_favorites(principle)
                else:
                    triz_engine.favorites.discard(principle)
                return jsonify({'message': f'已从收藏夹移除 {principle}'})
            return jsonify({'error': '原理名称不能为空'}), 400
    
    except Exception as e:
        return jsonify({'error': f'收藏夹操作失败: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0'
    })

# Vercel需要这个变量
app_handler = app

if __name__ == '__main__':
    print("🚀 TRIZ创新算法助手 - Web版启动中...")
    print("📱 访问地址: http://localhost:5001")
    print("🎯 API文档: http://localhost:5001/api")
    app.run(debug=True, host='0.0.0.0', port=5001)