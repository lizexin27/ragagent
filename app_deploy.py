import streamlit as st
import os

# -------------------------- 关键修改：直接在这里读取API Key --------------------------
# 1. 优先从 Streamlit Secrets 读取
DASHSCOPE_API_KEY = st.secrets.get("DASHSCOPE_API_KEY")
# 2. 备用：从环境变量读取
if not DASHSCOPE_API_KEY:
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

# 3. 直接在这里检查，不用依赖config.py
if not DASHSCOPE_API_KEY:
    st.error("❌ API Key 未配置！请在 Streamlit Secrets 中配置 DASHSCOPE_API_KEY")
    st.stop()

# -------------------------- 其他导入 --------------------------
# 现在再导入rag，就不会被前面的错误卡住了
from rag import RagService

# -------------------------- 页面配置 --------------------------
st.set_page_config(
    page_title="服装知识库问答系统",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
if 'rag' not in st.session_state:
    st.session_state.rag = None

# 页面标题
st.title("👔 服装知识库问答系统")
st.markdown("---")

# 侧边栏 - 配置和知识库管理
with st.sidebar:
    st.header("⚙️ 控制面板")

    # API Key 配置状态检查
    if DASHSCOPE_API_KEY:
        st.success(f"✅ API Key 已配置")
        st.info(f"Key: {DASHSCOPE_API_KEY[:10]}...")
    else:
        st.error("❌ API Key 未配置")
        st.warning("请在左侧设置环境变量或使用 Streamlit Secrets")

    # 知识库路径
    kb_path = st.text_input(
        "知识库路径",
        value="./chroma_db",
        help="向量数据库存储路径"
    )

    # 初始化按钮
    if st.button("🚀 初始化系统", type="primary"):
        try:
            # 初始化 RAG 服务
            st.session_state.rag = RagService()
            st.success("✅ 系统初始化成功！")
        except Exception as e:
            st.error(f"❌ 初始化失败: {str(e)}")
            st.stop()


    # 显示系统信息
    st.markdown("---")
    st.subheader("📊 系统信息")

    if st.session_state.rag:
        st.write("🤖 RAG 系统: 已就绪")
        st.write("🗂️ 向量数据库: ChromaDB")
        st.write("🔧 模型: 通义千问 Turbo")

# 主界面
if 'rag' not in st.session_state or st.session_state.rag is None:
    st.warning("请在左侧控制面板初始化系统")
    st.markdown("""
    ### 📖 使用说明

    1. **配置 API Key**：
       - 在左侧设置 DASHSCOPE_API_KEY
       - 或使用 Streamlit Secrets

    2. **初始化系统**：点击"初始化系统"按钮

    3. **上传知识文档**：将服装相关文档放入 `data/` 目录
       - 支持 .txt 格式
       - 多文件批量上传

    4. **开始问答**：在下方输入框输入问题

    ### 🔑 配置方法

    #### 方法一：环境变量
    ```bash
    export DASHSCOPE_API_KEY=your_api_key_here
    ```

    #### 方法二：Streamlit Secrets
    在 secrets.toml 中：
    ```toml
    DASHSCOPE_API_KEY = "your_api_key_here"
    ```
    """)
else:
    # 问答界面
    st.subheader("💬 服装知识问答")

    # 聊天历史
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "你好！我是服装知识助手，请告诉我您想了解什么服装相关的问题？"}
        ]

    # 显示聊天历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 用户输入
    prompt = st.chat_input("请输入您关于服装的问题...")

    if prompt:
        # 添加用户消息到聊天历史
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)

        # 获取 AI 回复
        with st.chat_message("assistant"):
            with st.spinner("正在思考..."):
                try:
                    # 调用 RAG 系统获取回答
                    response = st.session_state.rag.query(prompt)

                    # 显示回答
                    st.markdown(response)

                    # 添加到聊天历史
                    st.session_state.messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    error_msg = f"抱歉，回答问题时出现错误：{str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # 知识库管理
    st.markdown("---")
    st.subheader("📚 知识库管理")

    # 文档上传区域
    uploaded_files = st.file_uploader(
        "上传服装知识文档",
        type=["txt"],
        accept_multiple_files=True,
        help="支持 .txt 格式的文档文件"
    )

    if uploaded_files:
        st.success(f"📁 已上传 {len(uploaded_files)} 个文件")

        # 保存文件
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        for uploaded_file in uploaded_files:
            file_path = data_dir / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ 保存：{uploaded_file.name}")

        # 提示重新初始化
        st.info("💡 上传完成后，请重新初始化系统以加载新文档")

    # 重建知识库按钮
    if st.button("🔄 重建知识库"):
        try:
            with st.spinner("正在重建知识库..."):
                # 重新初始化 RAG 系统
                st.session_state.rag = RagService(
                    api_key=DASHSCOPE_API_KEY
                )
                st.success("✅ 知识库重建完成！")
        except Exception as e:
            st.error(f"❌ 重建失败：{str(e)}")

    # 清空对话按钮
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = [
            {"role": "assistant", "content": "对话已清空，有什么可以帮您的？"}
        ]
        st.success("✅ 对话已清空")

# 页脚
st.markdown("---")
st.markdown(
    "💡 提示：系统基于 LangChain + 通义千问 + ChromaDB 构建 | "
    "部署于 Streamlit Cloud"
)
