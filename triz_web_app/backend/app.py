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
            return jsonify({'error': triz_engine.get_text('no_solutions')}), 400
        
        # 调用TRIZ分析
        solutions = triz_engine.analyze_problem(problem, improving, worsening)
        
        # 转换为JSON格式
        result = {
            'problem': problem,
            'improving_param': improving,
            'worsening_param': worsening,
            'solutions': [sol.to_dict() for sol in solutions],
            'timestamp': datetime.datetime.now().isoformat(),
            'solution_count': len(solutions),
            'language': triz_engine.current_language
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
            return jsonify({'error': triz_engine.get_text('no_solutions')}), 400
        
        # 调用头脑风暴
        solutions = triz_engine.brainstorm(problem, num_solutions)
        
        result = {
            'problem': problem,
            'solutions': [sol.to_dict() for sol in solutions],
            'timestamp': datetime.datetime.now().isoformat(),
            'solution_count': len(solutions),
            'mode': 'brainstorm',
            'language': triz_engine.current_language
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'头脑风暴失败: {str(e)}'}), 500

@app.route('/api/language', methods=['GET', 'POST'])
def manage_language():
    """语言管理API"""
    try:
        if request.method == 'GET':
            return jsonify({
                'current_language': triz_engine.current_language,
                'available_languages': ['zh', 'en'],
                'texts': {
                    'app_title': triz_engine.get_text('app_title'),
                    'language_toggle': triz_engine.get_text('language_toggle'),
                    'analyze_button': triz_engine.get_text('analyze_button'),
                    'brainstorm_button': triz_engine.get_text('brainstorm_button'),
                    'export_button': triz_engine.get_text('export_button'),
                    'problem_placeholder': triz_engine.get_text('problem_placeholder'),
                    'improving_param': triz_engine.get_text('improving_param'),
                    'worsening_param': triz_engine.get_text('worsening_param'),
                    'loading': triz_engine.get_text('loading'),
                    'no_solutions': triz_engine.get_text('no_solutions'),
                    'principle': triz_engine.get_text('principle'),
                    'description': triz_engine.get_text('description'),
                    'examples': triz_engine.get_text('examples'),
                    'confidence': triz_engine.get_text('confidence'),
                    'category': triz_engine.get_text('category')
                }
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            new_language = data.get('language', 'zh')
            
            if new_language in ['zh', 'en']:
                triz_engine.set_language(new_language)
                return jsonify({
                    'success': True,
                    'current_language': triz_engine.current_language,
                    'message': f'Language switched to {new_language}'
                })
            else:
                return jsonify({'error': 'Invalid language'}), 400
    
    except Exception as e:
        return jsonify({'error': f'语言设置失败: {str(e)}'}), 500

@app.route('/api/principles')
def get_principles():
    """获取所有原理API"""
    try:
        principles = []
        for pid, data in triz_engine.principles.items():
            principles.append({
                'id': pid,
                'name': triz_engine.get_principle_text(data, 'name'),
                'description': triz_engine.get_principle_text(data, 'description'),
                'category': triz_engine.get_principle_text(data, 'category'),
                'examples': triz_engine.get_principle_text(data, 'examples'),
                'detailed': triz_engine.get_principle_text(data, 'detailed')
            })
        return jsonify({
            'principles': principles,
            'total_count': len(principles),
            'language': triz_engine.current_language
        })
    
    except Exception as e:
        return jsonify({'error': f'获取原理失败: {str(e)}'}), 500

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
            'filename': f'triz_solutions_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.{format_type}',
            'language': triz_engine.current_language
        })
    
    except Exception as e:
        return jsonify({'error': f'导出失败: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0',
        'environment': 'vercel' if os.environ.get('VERCEL') else 'local',
        'language': triz_engine.current_language,
        'principles_count': len(triz_engine.principles)
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