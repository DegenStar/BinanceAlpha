"""
AI模块 - 提供基于大模型的分析和建议功能

此模块包含:
1. OpenAI Chat Completions 兼容接口
2. 提示词生成功能
3. 投资建议生成功能

支持的模型:
- OpenAI、DeepSeek、Moonshot、通义兼容模式及本地 Ollama/vLLM 等
- AlphaAdvisor: 专门分析币安Alpha项目数据，提供投资建议
"""

# 导出主要类供外部使用
from .alpha_advisor import AlphaAdvisor

# 定义包的公共接口
__all__ = [
    'AlphaAdvisor'
]
