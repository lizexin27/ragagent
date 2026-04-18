# 服装知识库问答系统

基于 LangChain + 通义千问的 RAG（检索增强生成）服装知识库问答系统。

## 🎯 项目功能

- **服装知识问答**：基于服装专业知识库的智能问答
- **RAG 技术**：结合向量数据库实现精准的知识检索
- **Web 界面**：使用 Streamlit 构建的交互式问答界面
- **多兼容性**：支持本地环境变量和 Streamlit Secrets 配置

## 🛠️ 技术栈

- **前端框架**：Streamlit
- **AI 框架**：LangChain, LangChain Community, LangChain Core
- **大模型**：通义千问（DashScope）
- **向量数据库**：ChromaDB
- **文档处理**：LangChain 文档加载器

## 📁 项目结构

```
D:\ragagent\
├── app_qa.py              # 主入口文件（Streamlit 应用）
├── rag.py                 # RAG 核心模块
├── knowledge_base.py      # 知识库管理模块
├── config.py              # 配置管理文件
├── requirements.txt       # 依赖包列表
├── .gitignore             # Git 忽略文件
├── README.md              # 项目说明文档
├── chroma_db/            # ChromaDB 向量数据库存储
├── data/                 # 示例数据文件（.txt）
├── .env                  # 环境变量文件（不提交到 Git）
├── .env.example          # 环境变量示例文件
├── LICENSE               # MIT 许可证
├── setup.py              # 安装脚本
├── Dockerfile            # Docker 部署文件
└── config_data.py        # 原有配置文件
```

## 🚀 本地运行步骤

### 1. 进入项目目录

```bash
cd D:\ragagent
```

### 2. 创建虚拟环境

```bash
# Python 3.8+
python -m venv venv
# Windows
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 API Key

#### 方法一：本地环境变量（推荐）

创建 `.env` 文件：

```bash
echo DASHSCOPE_API_KEY=your_api_key_here > .env
```

#### 方法二：Streamlit Secrets

在项目根目录创建 `.streamlit/secrets.toml` 文件：

```toml
DASHSCOPE_API_KEY = "your_api_key_here"
```

### 5. 准备知识库数据

将服装知识文档（.txt 文件）放入 `data/` 目录下。

### 6. 运行应用

```bash
streamlit run app_qa.py
```

访问 `http://localhost:8501` 即可使用。

## ⚙️ 依赖包

主要依赖包括：

- `streamlit`: Web 应用框架
- `langchain`: AI 应用开发框架
- `langchain-community`: LangChain 社区组件
- `langchain-core`: LangChain 核心组件
- `dashscope`: 通义千问 API
- `chromadb`: 向量数据库
- `python-dotenv`: 环境变量管理

## 🔑 API Key 配置

### 获取通义千问 API Key

1. 访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 注册/登录阿里云账号
3. 开通通义千问服务
4. 在 API-KEY 管理中创建新的 API Key

### 配置方式

#### 本地环境变量方式（开发环境）

```bash
# 设置环境变量（Windows）
set DASHSCOPE_API_KEY=your_api_key_here
# 或者在 .env 文件中配置
```

#### Streamlit Secrets 方式（生产环境）

在 `.streamlit/secrets.toml` 中配置：

```toml
DASHSCOPE_API_KEY = "your_api_key_here"
```

## 📝 使用说明

1. **上传知识文档**：将服装相关的文档文件（支持 .txt 格式）放入 `data/` 目录
2. **构建知识库**：首次运行会自动构建向量数据库
3. **开始问答**：在 Web 界面输入问题，获取基于服装知识的智能回答

## 🔒 安全注意事项

- **切勿将 API Key 提交到 Git**
- **使用 .gitignore 确保敏感信息不被上传**
- **定期轮换 API Key**
- **不要在代码中硬编码敏感信息**

## 🚀 Docker 部署

### 构建 Docker 镜像

```bash
docker build -t rag-agent .
```

### 运行容器

```bash
docker run -p 8501:8501 -e DASHSCOPE_API_KEY=your_api_key rag-agent
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过 GitHub Issues 提交。