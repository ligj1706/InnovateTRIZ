from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import datetime
import os
import sys

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 导入TRIZ核心模块
from triz_core import AdvancedTRIZInnovator

app = Flask(__name__, 
           template_folder='../frontend/templates',
           static_folder='../frontend/static')
CORS(app)

# 初始化TRIZ引擎
triz_engine = AdvancedTRIZInnovator()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

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
            'solutions': [sol.to_dict() for sol in solutions],
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
            'solutions': [sol.to_dict() for sol in solutions],
            'timestamp': datetime.datetime.now().isoformat(),
            'solution_count': len(solutions),
            'mode': 'brainstorm'
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'头脑风暴失败: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0',
        'environment': 'vercel' if os.environ.get('VERCEL') else 'local'
    })

@app.route('/api/favorites', methods=['GET', 'POST'])
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
                triz_engine.favorites.add(principle)
                triz_engine._save_favorites()
                return jsonify({'message': f'已添加 {principle} 到收藏夹'})
            return jsonify({'error': '原理名称不能为空'}), 400
    
    except Exception as e:
        return jsonify({'error': f'收藏夹操作失败: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 TRIZ创新算法助手 - Web版启动中...")
    print("📱 访问地址: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)