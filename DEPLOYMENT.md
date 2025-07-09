# 部署配置说明

## 1. 基础配置（必须）

### 依赖包
项目已经配置好所有必要的依赖，无需额外安装。

### 环境变量
- 无需任何环境变量即可运行
- 系统会自动降级到标准TRIZ分析模式

## 2. AI增强配置（可选）

### 获取OpenRouter API密钥
1. 访问 [OpenRouter.ai](https://openrouter.ai)
2. 注册并获取API密钥
3. 在Vercel中设置环境变量：
   - 变量名：`OPENROUTER_API_KEY`
   - 值：你的API密钥

### 测试AI功能
```bash
# 设置API密钥
export OPENROUTER_API_KEY="your-api-key"

# 测试连接
python test_openrouter.py
```

## 3. Vercel部署步骤

### 1. 连接GitHub仓库
- 在Vercel中导入你的GitHub仓库
- 选择`InnovateTRIZ`项目

### 2. 配置环境变量（可选）
如果要启用AI功能：
- 在Vercel设置中添加环境变量
- 名称：`OPENROUTER_API_KEY`
- 值：你的OpenRouter API密钥

### 3. 部署设置
- 构建命令：留空（自动检测）
- 输出目录：留空（自动检测）
- 安装命令：`pip install -r requirements.txt`

### 4. 部署
点击"Deploy"按钮，Vercel会自动：
- 安装Python依赖
- 构建应用
- 部署到全球CDN

## 4. 功能说明

### 标准功能（无需API）
- ✅ 完整的40个TRIZ原理
- ✅ 技术矛盾矩阵分析
- ✅ 智能参数检测
- ✅ 头脑风暴模式
- ✅ 双语界面支持
- ✅ 结果导出功能

### AI增强功能（需要API）
- 🤖 自动参数识别
- 🤖 智能问题分析
- 🤖 解决方案优化
- 🤖 上下文感知建议

## 5. 容错机制

系统具有完善的容错机制：
- 如果没有API密钥 → 自动使用标准TRIZ分析
- 如果API失效 → 降级到标准分析模式
- 如果网络问题 → 显示友好错误提示

## 6. 开源配置

### 许可证
项目使用MIT许可证，可以自由使用、修改和分发。

### 贡献指南
欢迎提交Issue和Pull Request！

### 代码结构
```
InnovateTRIZ/
├── triz_web_app/
│   ├── backend/
│   │   ├── app.py              # Flask后端
│   │   └── triz_core.py        # TRIZ核心
│   └── frontend/
│       ├── templates/index.html # 前端页面
│       └── static/             # CSS/JS资源
├── requirements.txt            # 依赖包
├── vercel.json                # Vercel配置
└── README.md                  # 项目说明
```

## 7. 成本说明

### 基础功能：完全免费
- 所有TRIZ分析功能
- 无需任何API费用
- 可以正常部署和使用

### AI增强功能：低成本
- OpenRouter提供多种免费模型
- 当前使用`deepseek-r1t2-chimera:free`
- 即使收费模型，成本也很低（每1000token约$0.001）

## 8. 监控和维护

### 健康检查
访问 `/api/health` 查看系统状态

### 日志监控
在Vercel控制台查看应用日志

### 性能监控
Vercel提供内置的性能监控工具

---

**总结：你无需任何额外配置即可部署和使用本项目。AI功能是完全可选的增强功能！**