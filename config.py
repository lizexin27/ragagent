"""
配置管理模块
支持本地环境变量和 Streamlit Secrets 双兼容
"""

import os
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """配置类，统一管理所有配置项"""

    # 通义千问 API Key
    DASHSCOPE_API_KEY: Optional[str] = None

    def __init__(self):
        """初始化配置，优先级：环境变量 > Streamlit Secrets > 默认值"""

        # 尝试从环境变量获取
        self.DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

        # 如果环境变量没有，尝试从 Streamlit Secrets 获取
        if not self.DASHSCOPE_API_KEY:
            try:
                # 检查是否在 Streamlit 环境中
                import streamlit as st
                if hasattr(st, 'secrets'):
                    self.DASHSCOPE_API_KEY = st.secrets.get("DASHSCOPE_API_KEY")
            except (ImportError, AttributeError):
                pass

        # 验证 API Key 是否配置
        if not self.DASHSCOPE_API_KEY:
            raise ValueError(
                "通义千问 API Key 未配置！\n"
                "请通过以下方式之一配置：\n"
                "1. 设置环境变量：export DASHSCOPE_API_KEY='your_key'\n"
                "2. 或创建 .env 文件：echo DASHSCOPE_API_KEY='your_key' > .env\n"
                "3. 或使用 Streamlit Secrets：在 .streamlit/secrets.toml 中配置"
            )

        print(f"✅ 通义千问 API Key 已配置: {self.DASHSCOPE_API_KEY[:10]}...")

    @classmethod
    def get_api_key(cls) -> str:
        """获取通义千问 API Key 的类方法"""
        if cls.DASHSCOPE_API_KEY is None:
            # 第一次调用时初始化
            cls.DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

            if not cls.DASHSCOPE_API_KEY:
                try:
                    import streamlit as st
                    if hasattr(st, 'secrets'):
                        cls.DASHSCOPE_API_KEY = st.secrets.get("DASHSCOPE_API_KEY")
                except (ImportError, AttributeError):
                    pass

            if not cls.DASHSCOPE_API_KEY:
                raise ValueError(
                    "通义千问 API Key 未配置！\n"
                    "请查看 README.md 了解配置方法"
                )

        return cls.DASHSCOPE_API_KEY


# 创建全局配置实例
config = Config()

# 导出配置供其他模块使用
DASHSCOPE_API_KEY = config.DASHSCOPE_API_KEY