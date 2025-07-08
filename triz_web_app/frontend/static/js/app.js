// TRIZ Web App JavaScript
class TRIZApp {
    constructor() {
        this.currentSolutions = [];
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadStatistics();
        this.loadHistory();
        this.loadPrinciples();
        this.showSection('home');
    }

    bindEvents() {
        // 导航点击事件
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = link.dataset.section;
                this.showSection(section);
            });
        });

        // 分析按钮事件
        document.getElementById('analyze-btn').addEventListener('click', () => {
            this.analyzeProblem();
        });

        // 头脑风暴按钮事件
        document.getElementById('brainstorm-btn').addEventListener('click', () => {
            this.brainstormProblem();
        });

        // 导出按钮事件
        document.getElementById('export-btn').addEventListener('click', () => {
            this.exportSolutions(this.currentSolutions);
        });

        document.getElementById('export-brainstorm-btn').addEventListener('click', () => {
            this.exportSolutions(this.currentSolutions);
        });

        // 搜索原理事件
        document.getElementById('principles-search').addEventListener('input', (e) => {
            this.searchPrinciples(e.target.value);
        });

        // 回车提交事件
        document.getElementById('problem-input').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.analyzeProblem();
            }
        });

        document.getElementById('brainstorm-input').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.brainstormProblem();
            }
        });
    }

    showSection(sectionId) {
        // 隐藏所有章节
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });

        // 显示目标章节
        document.getElementById(sectionId).classList.add('active');

        // 更新导航状态
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        
        const activeLink = document.querySelector(`[data-section="${sectionId}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        // 根据章节加载特定数据
        if (sectionId === 'history') {
            this.loadHistory();
            this.loadStatistics();
        } else if (sectionId === 'principles') {
            this.loadPrinciples();
        }
    }

    async analyzeProblem() {
        const problem = document.getElementById('problem-input').value.trim();
        const improving = document.getElementById('improving-input').value.trim();
        const worsening = document.getElementById('worsening-input').value.trim();

        if (!problem) {
            this.showNotification('请输入问题描述', 'error');
            return;
        }

        this.showLoading(true);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    problem: problem,
                    improving: improving,
                    worsening: worsening
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.currentSolutions = data.solutions;
                this.displaySolutions(data.solutions, 'analysis-results', 'solutions-list');
                this.showNotification('分析完成！');
            } else {
                this.showNotification(data.error || '分析失败', 'error');
            }
        } catch (error) {
            this.showNotification('网络错误，请稍后重试', 'error');
            console.error('Analysis error:', error);
        } finally {
            this.showLoading(false);
        }
    }

    async brainstormProblem() {
        const problem = document.getElementById('brainstorm-input').value.trim();
        const numSolutions = parseInt(document.getElementById('solution-count').value);

        if (!problem) {
            this.showNotification('请输入问题描述', 'error');
            return;
        }

        this.showLoading(true, '正在生成创新方案...');

        try {
            const response = await fetch('/api/brainstorm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    problem: problem,
                    num_solutions: numSolutions
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.currentSolutions = data.solutions;
                this.displaySolutions(data.solutions, 'brainstorm-results', 'brainstorm-solutions-list');
                this.showNotification('头脑风暴完成！');
            } else {
                this.showNotification(data.error || '头脑风暴失败', 'error');
            }
        } catch (error) {
            this.showNotification('网络错误，请稍后重试', 'error');
            console.error('Brainstorm error:', error);
        } finally {
            this.showLoading(false);
        }
    }

    displaySolutions(solutions, containerId, listId) {
        const container = document.getElementById(containerId);
        const list = document.getElementById(listId);

        if (!solutions || solutions.length === 0) {
            list.innerHTML = '<p class="no-results">未找到解决方案</p>';
            container.style.display = 'block';
            return;
        }

        list.innerHTML = solutions.map((solution, index) => `
            <div class="solution-card" data-index="${index}">
                <div class="solution-header">
                    <div>
                        <div class="solution-title">${solution.principle}</div>
                        <div class="solution-category">${solution.category}</div>
                    </div>
                    <button class="favorite-btn" onclick="app.toggleFavorite('${solution.principle}', this)">
                        <i class="fas fa-star"></i>
                    </button>
                </div>
                
                <div class="solution-description">
                    ${solution.description}
                </div>
                
                <div class="solution-metrics">
                    <div class="metric">
                        <span>置信度:</span>
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: ${solution.confidence * 100}%"></div>
                        </div>
                        <span>${(solution.confidence * 100).toFixed(0)}%</span>
                    </div>
                    <div class="metric">
                        <span>相关性:</span>
                        <div class="relevance-bar">
                            <div class="relevance-fill" style="width: ${solution.relevance_score * 100}%"></div>
                        </div>
                        <span>${(solution.relevance_score * 100).toFixed(0)}%</span>
                    </div>
                </div>
                
                <div class="solution-examples">
                    <h4>应用示例:</h4>
                    <div class="example-tags">
                        ${solution.examples.slice(0, 4).map(example => 
                            `<span class="example-tag">${example}</span>`
                        ).join('')}
                    </div>
                </div>
                
                <details style="margin-top: 1rem;">
                    <summary style="cursor: pointer; font-weight: 500;">详细说明</summary>
                    <p style="margin-top: 0.5rem; color: var(--text-secondary);">
                        ${solution.detailed_explanation}
                    </p>
                </details>
            </div>
        `).join('');

        container.style.display = 'block';
        container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    async exportSolutions(solutions) {
        if (!solutions || solutions.length === 0) {
            this.showNotification('没有可导出的解决方案', 'error');
            return;
        }

        const format = await this.selectExportFormat();
        if (!format) return;

        try {
            const response = await fetch('/api/export', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    solutions: solutions,
                    format: format
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.downloadFile(data.content, data.filename, format);
                this.showNotification('导出成功！');
            } else {
                this.showNotification(data.error || '导出失败', 'error');
            }
        } catch (error) {
            this.showNotification('导出时发生错误', 'error');
            console.error('Export error:', error);
        }
    }

    async selectExportFormat() {
        return new Promise((resolve) => {
            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.5); display: flex; align-items: center;
                justify-content: center; z-index: 10000;
            `;
            
            modal.innerHTML = `
                <div style="background: white; padding: 2rem; border-radius: 12px; max-width: 400px;">
                    <h3 style="margin-bottom: 1rem;">选择导出格式</h3>
                    <div style="display: flex; gap: 1rem;">
                        <button class="btn btn-primary" onclick="selectFormat('json')">JSON格式</button>
                        <button class="btn btn-secondary" onclick="selectFormat('txt')">文本格式</button>
                        <button class="btn" onclick="selectFormat(null)" style="background: #6b7280; color: white;">取消</button>
                    </div>
                </div>
            `;

            window.selectFormat = (format) => {
                document.body.removeChild(modal);
                delete window.selectFormat;
                resolve(format);
            };

            document.body.appendChild(modal);
        });
    }

    downloadFile(content, filename, format) {
        const blob = new Blob([content], { 
            type: format === 'json' ? 'application/json' : 'text/plain' 
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    async toggleFavorite(principle, button) {
        try {
            const icon = button.querySelector('i');
            const isActive = button.classList.contains('active');
            
            const response = await fetch('/api/favorites', {
                method: isActive ? 'DELETE' : 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ principle: principle })
            });

            const data = await response.json();

            if (response.ok) {
                button.classList.toggle('active');
                icon.className = isActive ? 'fas fa-star' : 'fas fa-star';
                this.showNotification(data.message);
            } else {
                this.showNotification(data.error || '操作失败', 'error');
            }
        } catch (error) {
            this.showNotification('网络错误', 'error');
            console.error('Favorite error:', error);
        }
    }

    async loadStatistics() {
        try {
            const response = await fetch('/api/statistics');
            const stats = await response.json();

            if (response.ok) {
                document.getElementById('total-sessions').textContent = stats.total_sessions || 0;
                document.getElementById('avg-rating').textContent = (stats.average_rating || 0).toFixed(1);
                document.getElementById('favorites-count').textContent = stats.favorites_count || 0;
            }
        } catch (error) {
            console.error('Statistics error:', error);
        }
    }

    async loadHistory() {
        try {
            const response = await fetch('/api/history?limit=10');
            const data = await response.json();

            if (response.ok) {
                this.displayHistory(data.history);
            }
        } catch (error) {
            console.error('History error:', error);
        }
    }

    displayHistory(history) {
        const container = document.getElementById('history-items');
        
        if (!history || history.length === 0) {
            container.innerHTML = '<p class="no-results">暂无历史记录</p>';
            return;
        }

        container.innerHTML = history.map(item => `
            <div class="history-item">
                <div class="history-content">
                    <div class="history-problem">${item.problem}</div>
                    <div class="history-meta">
                        ${item.timestamp} · ${item.solution_count}个方案
                        ${item.rating ? `· <span class="history-rating">⭐${item.rating}</span>` : ''}
                    </div>
                </div>
            </div>
        `).join('');
    }

    async loadPrinciples() {
        try {
            const response = await fetch('/api/principles');
            const data = await response.json();

            if (response.ok) {
                this.allPrinciples = data.principles;
                this.displayPrinciples(data.principles);
            }
        } catch (error) {
            console.error('Principles error:', error);
        }
    }

    displayPrinciples(principles) {
        const container = document.getElementById('principles-grid');
        
        container.innerHTML = principles.map(principle => `
            <div class="principle-card">
                <div class="principle-id">${principle.id}</div>
                <div class="principle-name">${principle.name}</div>
                <div class="principle-description">${principle.description}</div>
                <div class="principle-category">${principle.category}</div>
                
                <div class="solution-examples" style="margin-top: 1rem;">
                    <h4>应用示例:</h4>
                    <div class="example-tags">
                        ${principle.examples.slice(0, 3).map(example => 
                            `<span class="example-tag">${example}</span>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `).join('');
    }

    async searchPrinciples(query) {
        if (!query.trim()) {
            this.displayPrinciples(this.allPrinciples || []);
            return;
        }

        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();

            if (response.ok) {
                this.displayPrinciples(data.results);
            }
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    showLoading(show, message = 'AI正在分析中...') {
        const loading = document.getElementById('loading');
        const loadingText = loading.querySelector('p');
        
        if (show) {
            loadingText.textContent = message;
            loading.style.display = 'flex';
        } else {
            loading.style.display = 'none';
        }
    }

    showNotification(message, type = 'success') {
        const notification = document.getElementById('notification');
        notification.textContent = message;
        notification.className = `notification ${type}`;
        notification.style.display = 'block';
        
        // 触发显示动画
        setTimeout(() => notification.classList.add('show'), 10);
        
        // 3秒后自动隐藏
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.style.display = 'none', 300);
        }, 3000);
    }
}

// 全局函数
window.showSection = function(sectionId) {
    app.showSection(sectionId);
};

// 初始化应用
const app = new TRIZApp();

// 页面加载完成后的额外设置
document.addEventListener('DOMContentLoaded', () => {
    // 添加键盘快捷键
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case '1':
                    e.preventDefault();
                    app.showSection('analyze');
                    break;
                case '2':
                    e.preventDefault();
                    app.showSection('brainstorm');
                    break;
                case '3':
                    e.preventDefault();
                    app.showSection('history');
                    break;
                case '4':
                    e.preventDefault();
                    app.showSection('principles');
                    break;
            }
        }
    });

    // 添加平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});