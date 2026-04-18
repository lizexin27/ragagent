# Streamlit Cloud 部署指南

## 快速部署步骤

### 1. 准备代码

确保您的项目包含以下文件：
- `app_deploy.py` - 部署版本的应用入口
- `rag.py` - RAG 核心模块
- `knowledge_base.py` - 知识库管理
- `config.py` - 配置管理
- `requirements_deploy.txt` - 部署依赖

### 2. 提交到 GitHub

```bash
# 1. 初始化 Git
cd D:\ragagent
git init

# 2. 添加所有文件
git add .
git commit -m "Ready for Streamlit Cloud deployment"

# 3. 关联远程仓库
git remote add origin https://github.com/yourusername/rag-agent-deploy.git

# 4. 推送到 GitHub
git push -u origin main
```

### 3. Streamlit Cloud 部署

1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 点击 "New app"（右上角）
3. 选择您的 GitHub 仓库
4. 选择分支（通常是 main）
5. 应用入口点选择：`app_deploy.py`
6. 点击 "Deploy!"

### 4. 配置 Secrets

部署完成后，需要配置 API Key：

1. 进入您的应用页面
2. 点击 "Settings"（左侧菜单）
3. 向下滚动到 "Secrets" 部分
4. 添加以下内容：
   ```
   DASHSCOPE_API_KEY=your_actual_api_key_here
   ```
5. 点击 "Save"

### 5. 上传数据文件

1. 在应用运行后，点击左侧的 "Upload data" 按钮
2. 将您的服装知识文档（.txt 文件）上传到 `data/` 文件夹
3. 或者直接修改代码，将文档放入项目根目录的 `data/` 文件夹中

## 注意事项

### 1. 文件权限
- Streamlit Cloud 只读访问您的代码
- 数据文件需要通过 Web 上传或使用 Git 管理

### 2. 免费额度
- Streamlit Cloud 有免费的计算资源
- 但长期使用可能需要付费

### 3. API Key 安全
- 不要在代码中硬编码 API Key
- 一定要使用 Streamlit Secrets 管理

### 4. 性能优化
- 首次启动可能较慢
- 文档处理可能需要时间

## 故障排除

### 1. 应用无法启动
- 检查 `requirements_deploy.txt` 是否包含所有依赖
- 查看 Streamlit Cloud 的日志

### 2. API Key 错误
- 确认 Secrets 中 DASHSCOPE_API_KEY 正确
- 检查 API Key 是否有效

### 3. 知识库问题
- 确保已上传数据文件
- 重新初始化系统

### 4. 部署后更新
- 更新代码后重新推送 GitHub
- Streamlit Cloud 会自动重新部署

## 其他部署选项

### Docker 部署
```bash
# 构建镜像
docker build -t rag-agent .

# 运行容器
docker run -p 8501:8501 -e DASHSCOPE_API_KEY=your_key rag-agent
```

### 云服务器部署
- 使用 AWS/GCP/Azure 云服务器
- 安装 Python 和 Streamlit
- 使用 systemd 管理服务