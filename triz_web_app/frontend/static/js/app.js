// TRIZ Web App JavaScript
class TRIZApp {
    constructor() {
        this.currentSolutions = [];
        this.currentLanguage = 'zh';
        this.translations = {};
        this.init();
    }

    init() {
        this.loadLanguage();
        this.bindEvents();
        this.loadStatistics();
        this.loadHistory();
        this.loadPrinciples();
        this.showSection('home');
    }

    async loadLanguage() {
        try {
            const response = await fetch('/api/language');
            const data = await response.json();
            
            if (response.ok) {
                this.currentLanguage = data.current_language;
                this.translations = data.texts;
                this.updateUITexts();
            }
        } catch (error) {
            console.error('Language loading error:', error);
        }
    }


    getText(key) {
        return this.translations[key] || key;
    }

    updateUITexts() {
        const textElements = {
            'app-title': 'app_title',
            'hero-title': 'app_title',
            'hero-subtitle': 'app_subtitle',
            'nav-analyze': 'nav_analyze',
            'nav-brainstorm': 'nav_brainstorm',
            'nav-history': 'nav_history',
            'nav-principles': 'nav_principles',
            'feature-analysis': 'feature_analysis',
            'feature-analysis-desc': 'feature_analysis_desc',
            'feature-innovation': 'feature_innovation',
            'feature-innovation-desc': 'feature_innovation_desc',
            'feature-scoring': 'feature_scoring',
            'feature-scoring-desc': 'feature_scoring_desc',
            'btn-start-analysis': 'btn_start_analysis',
            'btn-browse-principles': 'btn_browse_principles',
            'analyze-title': 'analyze_title',
            'analyze-desc': 'analyze_desc',
            'problem-label': 'problem_label',
            'improving-label': 'improving_label',
            'worsening-label': 'worsening_label',
            'analyze-btn-text': 'analyze_btn_text',
            'solutions-title': 'solutions_title',
            'export-text': 'export_text',
            'brainstorm-title': 'brainstorm_title',
            'brainstorm-desc': 'brainstorm_desc',
            'brainstorm-problem-label': 'brainstorm_problem_label',
            'solution-count-label': 'solution_count_label',
            'brainstorm-btn-text': 'brainstorm_btn_text',
            'innovation-title': 'innovation_title',
            'export-brainstorm-text': 'export_brainstorm_text',
            'history-title': 'history_title',
            'history-desc': 'history_desc',
            'total-sessions-label': 'total_sessions_label',
            'avg-rating-label': 'avg_rating_label',
            'favorites-label': 'favorites_label',
            'recent-analysis': 'recent_analysis',
            'principles-title': 'principles_title',
            'principles-desc': 'principles_desc',
            'loading-text': 'loading_text',
            'about-triz-title': 'about_triz_title',
            'about-triz-desc': 'about_triz_desc',
            'stat-principles': 'stat_principles',
            'stat-matrix': 'stat_matrix',
            'stat-ai': 'stat_ai',
            'core-advantages-title': 'core_advantages_title',
            'feature-ai-title': 'feature_ai_title',
            'feature-ai-desc': 'feature_ai_desc',
            'feature-fast-title': 'feature_fast_title',
            'feature-fast-desc': 'feature_fast_desc',
            'feature-database-title': 'feature_database_title',
            'feature-database-desc': 'feature_database_desc',
            'feature-scoring-title': 'feature_scoring_title',
            'feature-scoring-desc': 'feature_scoring_desc',
            'feature-export-title': 'feature_export_title',
            'feature-export-desc': 'feature_export_desc',
            'feature-brainstorm-title': 'feature_brainstorm_title',
            'feature-brainstorm-desc': 'feature_brainstorm_desc',
            'footer-title': 'app_title',
            'footer-description': 'footer_simple_description',
            'footer-analyze': 'nav_analyze',
            'footer-brainstorm': 'nav_brainstorm',
            'footer-principles': 'nav_principles',
            'footer-history': 'nav_history',
            'footer-copyright-text': 'footer_simple_copyright',
            'footer-version': 'footer_version',
            'ai-enhanced-label': 'ai_enhanced_label',
            'ai-enhanced-desc': 'ai_enhanced_desc'
        };
        
        Object.entries(textElements).forEach(([elementId, textKey]) => {
            const element = document.getElementById(elementId);
            if (element) {
                element.textContent = this.getText(textKey);
            }
        });
        
        // Update placeholders
        const placeholderElements = {
            'problem-input': 'problem_placeholder',
            'improving-input': 'improving_placeholder',
            'worsening-input': 'worsening_placeholder',
            'brainstorm-input': 'brainstorm_placeholder',
            'principles-search': 'search_placeholder'
        };
        
        Object.entries(placeholderElements).forEach(([elementId, textKey]) => {
            const element = document.getElementById(elementId);
            if (element) {
                element.placeholder = this.getText(textKey);
            }
        });
        
        // Update option texts
        const optionElements = {
            'option-3': 'option_3_solutions',
            'option-5': 'option_5_solutions', 
            'option-8': 'option_8_solutions',
            'option-10': 'option_10_solutions'
        };
        
        Object.entries(optionElements).forEach(([elementId, textKey]) => {
            const element = document.getElementById(elementId);
            if (element) {
                element.textContent = this.getText(textKey);
            }
        });
        
        // Update language toggle
        this.updateLanguageToggle();
    }

    updateLanguageToggle() {
        const currentLang = document.getElementById('current-lang');
        const dropdown = document.querySelector('.language-dropdown');
        const options = dropdown.querySelectorAll('.language-option');
        
        // Update current language display
        if (currentLang) {
            currentLang.textContent = this.currentLanguage === 'zh' ? '中文' : 'English';
        }
        
        // Update dropdown options active state
        options.forEach(option => {
            const lang = option.dataset.lang;
            if (lang === this.currentLanguage) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });
    }

    bindEvents() {
        // 语言切换下拉菜单事件
        const languageToggle = document.getElementById('language-toggle');
        const dropdown = document.querySelector('.language-dropdown');
        const options = document.querySelectorAll('.language-option');
        
        // 点击切换显示/隐藏下拉菜单
        languageToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdown.classList.toggle('show');
        });
        
        // 点击语言选项
        options.forEach(option => {
            option.addEventListener('click', (e) => {
                e.stopPropagation();
                const selectedLang = option.dataset.lang;
                if (selectedLang !== this.currentLanguage) {
                    this.switchLanguage(selectedLang);
                }
                dropdown.classList.remove('show');
            });
        });
        
        // 点击外部关闭下拉菜单
        document.addEventListener('click', () => {
            dropdown.classList.remove('show');
        });

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
    
    async switchLanguage(newLanguage) {
        try {
            const response = await fetch('/api/language', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ language: newLanguage })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.currentLanguage = newLanguage;
                await this.loadLanguage();
                this.loadPrinciples(); // Reload principles in new language
                this.showNotification(this.getText('language_switched'));
            }
        } catch (error) {
            console.error('Language switch error:', error);
        }
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
        
        // 如果不是home页面，激活对应的导航链接
        if (sectionId !== 'home') {
            const activeLink = document.querySelector(`[data-section="${sectionId}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
            }
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
        const aiEnhanced = document.getElementById('ai-enhanced').checked;

        if (!problem) {
            this.showNotification(this.getText('enter_problem'), 'error');
            return;
        }

        // 根据AI增强开关选择不同的API端点
        const apiEndpoint = aiEnhanced ? '/api/ai-analyze' : '/api/analyze';
        const loadingText = aiEnhanced ? this.getText('loading_ai_analyzing') : this.getText('loading_analyzing');
        
        this.showLoading(true, loadingText);

        try {
            const response = await fetch(apiEndpoint, {
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
                
                // 如果是AI增强分析，显示特殊提示
                if (data.ai_enhanced) {
                    this.showNotification(this.getText('ai_analysis_complete'), 'success');
                } else {
                    this.showNotification(this.getText('analysis_complete'), 'success');
                }
            } else {
                this.showNotification(data.error || this.getText('analysis_failed'), 'error');
            }
        } catch (error) {
            this.showNotification(this.getText('network_error'), 'error');
            console.error('Analysis error:', error);
        } finally {
            this.showLoading(false);
        }
    }

    async brainstormProblem() {
        const problem = document.getElementById('brainstorm-input').value.trim();
        const numSolutions = parseInt(document.getElementById('solution-count').value);

        if (!problem) {
            this.showNotification(this.getText('enter_problem'), 'error');
            return;
        }

        this.showLoading(true, this.getText('loading_brainstorm'));

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
                this.showNotification(this.getText('brainstorm_complete'));
            } else {
                this.showNotification(data.error || this.getText('brainstorm_failed'), 'error');
            }
        } catch (error) {
            this.showNotification(this.getText('network_error'), 'error');
            console.error('Brainstorm error:', error);
        } finally {
            this.showLoading(false);
        }
    }

    displaySolutions(solutions, containerId, listId) {
        const container = document.getElementById(containerId);
        const list = document.getElementById(listId);

        if (!solutions || solutions.length === 0) {
            list.innerHTML = `<p class="no-results">${this.getText('no_solutions')}</p>`;
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
                        <span>${this.getText('confidence')}:</span>
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: ${solution.confidence * 100}%"></div>
                        </div>
                        <span>${(solution.confidence * 100).toFixed(0)}%</span>
                    </div>
                    <div class="metric">
                        <span>${this.getText('relevance')}:</span>
                        <div class="relevance-bar">
                            <div class="relevance-fill" style="width: ${solution.relevance_score * 100}%"></div>
                        </div>
                        <span>${(solution.relevance_score * 100).toFixed(0)}%</span>
                    </div>
                </div>
                
                <div class="solution-examples">
                    <h4>${this.getText('examples')}:</h4>
                    <div class="example-tags">
                        ${solution.examples.slice(0, 4).map(example => 
                            `<span class="example-tag">${example}</span>`
                        ).join('')}
                    </div>
                </div>
                
                <details style="margin-top: 1rem;">
                    <summary style="cursor: pointer; font-weight: 500;">${this.getText('detailed_explanation')}</summary>
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
            this.showNotification(this.getText('no_solutions_to_export'), 'error');
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
                this.showNotification(this.getText('export_success'));
            } else {
                this.showNotification(data.error || this.getText('export_failed'), 'error');
            }
        } catch (error) {
            this.showNotification(this.getText('export_error'), 'error');
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
                    <h3 style="margin-bottom: 1rem;">${this.getText('select_export_format')}</h3>
                    <div style="display: flex; gap: 1rem;">
                        <button class="btn btn-primary" onclick="selectFormat('json')">${this.getText('json_format')}</button>
                        <button class="btn btn-secondary" onclick="selectFormat('txt')">${this.getText('text_format')}</button>
                        <button class="btn" onclick="selectFormat(null)" style="background: #6b7280; color: white;">${this.getText('cancel')}</button>
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
                this.showNotification(data.error || this.getText('operation_failed'), 'error');
            }
        } catch (error) {
            this.showNotification(this.getText('network_error'), 'error');
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
            container.innerHTML = `<p class="no-results">${this.getText('no_history')}</p>`;
            return;
        }

        container.innerHTML = history.map(item => `
            <div class="history-item">
                <div class="history-content">
                    <div class="history-problem">${item.problem}</div>
                    <div class="history-meta">
                        ${item.timestamp} · ${item.solution_count}${this.getText('solutions')}
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
                <div class="principle-header">
                    <div class="principle-id">${principle.id}</div>
                    <div class="principle-name">${principle.name}</div>
                </div>
                
                <div class="principle-content">
                    <div class="principle-description">${principle.description}</div>
                    <div class="principle-category">${principle.category}</div>
                    
                    <div class="principle-section">
                        <h5>${this.getText('examples')}:</h5>
                        <div class="example-tags">
                            ${principle.examples.slice(0, 4).map(example => 
                                `<span class="example-tag">${example}</span>`
                            ).join('')}
                        </div>
                    </div>
                    
                    ${principle.applications ? `
                        <div class="principle-section">
                            <h5>${this.getText('applications')}:</h5>
                            <div class="application-list">
                                ${principle.applications.slice(0, 3).map(app => 
                                    `<div class="application-item">• ${app}</div>`
                                ).join('')}
                            </div>
                        </div>
                    ` : ''}
                    
                    <details class="principle-details">
                        <summary>${this.getText('detailed_explanation')}</summary>
                        <div class="details-content">
                            <p>${principle.detailed}</p>
                            
                            ${principle.implementation ? `
                                <div class="implementation-section">
                                    <h6>${this.getText('implementation_steps')}:</h6>
                                    <ol class="implementation-list">
                                        ${principle.implementation.map(step => 
                                            `<li>${step}</li>`
                                        ).join('')}
                                    </ol>
                                </div>
                            ` : ''}
                            
                            ${principle.benefits ? `
                                <div class="benefits-section">
                                    <h6>${this.getText('benefits')}:</h6>
                                    <ul class="benefits-list">
                                        ${principle.benefits.map(benefit => 
                                            `<li>${benefit}</li>`
                                        ).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                        </div>
                    </details>
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