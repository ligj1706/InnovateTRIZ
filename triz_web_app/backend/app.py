from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import datetime
import os
import sys
from pathlib import Path

# 导入我们的TRIZ核心模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
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

@app.route('/api/export', methods=['POST'])
def export_solutions():
    """导出解决方案API"""
    try:
        data = request.get_json()
        solutions_data = data.get('solutions', [])
        format_type = data.get('format', 'json')
        
        # 重建Solution对象
        from triz_core import Solution
        solutions = []
        for sol_data in solutions_data:
            solution = Solution(**sol_data)
            solutions.append(solution)
        
        # 导出
        export_content = triz_engine.export_solutions(solutions, format_type)
        
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
                triz_engine.remove_from_favorites(principle)
                return jsonify({'message': f'已从收藏夹移除 {principle}'})
            return jsonify({'error': '原理名称不能为空'}), 400
    
    except Exception as e:
        return jsonify({'error': f'收藏夹操作失败: {str(e)}'}), 500

@app.route('/api/history')
def get_history():
    """获取历史记录API"""
    try:
        limit = request.args.get('limit', 20, type=int)
        history = triz_engine.get_history(limit)
        return jsonify({'history': history})
    
    except Exception as e:
        return jsonify({'error': f'获取历史失败: {str(e)}'}), 500

@app.route('/api/statistics')
def get_statistics():
    """获取统计信息API"""
    try:
        stats = triz_engine.get_statistics()
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': f'获取统计失败: {str(e)}'}), 500

@app.route('/api/search')
def search_principles():
    """搜索原理API"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': '搜索关键词不能为空'}), 400
        
        results = triz_engine.search_principles(query)
        return jsonify({'results': results, 'count': len(results)})
    
    except Exception as e:
        return jsonify({'error': f'搜索失败: {str(e)}'}), 500

@app.route('/api/principles')
def get_all_principles():
    """获取所有原理API"""
    try:
        principles = []
        for pid, data in triz_engine.principles.items():
            principles.append({
                'id': pid,
                'name': data['name'],
                'description': data['description'],
                'category': data['category'],
                'examples': data['examples']
            })
        return jsonify({'principles': principles})
    
    except Exception as e:
        return jsonify({'error': f'获取原理失败: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 TRIZ创新算法助手 - Web版启动中...")
    print("📱 访问地址: http://localhost:5001")
    print("🎯 API文档: http://localhost:5001/api")
    app.run(debug=True, host='0.0.0.0', port=5001)