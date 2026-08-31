# 消息通知配置
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 添加默认值和类型检查
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')  # Discord webhook

# 根据环境变量判断是否在Docker中运行
IS_DOCKER = os.getenv('IS_DOCKER', 'false').lower() == 'true'

# 根据运行环境选择代理地址
PROXY_URL = 'http://host.docker.internal:7890' if IS_DOCKER else 'http://127.0.0.1:7890'
USE_PROXY = True

# 文件路径配置
DATA_DIRS = {
    'prompts': 'prompts',           # 提示词保存目录
    'responses': 'responses',       # AI响应内容保存目录
    'advices': 'advices',           # AI建议保存目录
    'all-platforms': 'advices/all-platforms', # 所有平台建议保存目录
    'records': 'investment_records', # 投资建议记录保存目录
    'debug': 'debug_logs',          # 调试日志保存目录
    'data': 'data',                 # 市场数据保存目录
    'images': 'images',             # 图片保存目录
    'symbols': 'symbols'            # 符号保存目录
}

# 区块链平台配置
BLOCKCHAIN_PLATFORMS = {
    "BNB Chain": ["BNB", "BSC", "BEP20", "BEP-20", "Binance Smart Chain", "币安智能链", "bnb-chain-ecosystem", "binance-chain"],
    "Solana": ["SOL", "Solana", "SPL", "索拉纳", "solana-ecosystem"], 
    "Ethereum": ["ETH", "ERC20", "Ethereum", "ERC-20", "ERC 20", "以太坊", "ethereum-ecosystem"],
    "Base": ["Base", "Base-Ecosystem", "base-ecosystem"],
}

# 要查询的区块链平台
# 留空数组表示查询所有BLOCKCHAIN_PLATFORMS中定义的平台
# 填入平台名数组则只查询指定的平台，例如: ["Ethereum", "Solana"]
PLATFORMS_TO_QUERY = []

# 数据保留策略配置（天数）
DATA_RETENTION = {
    'images': 30,               # images/ 下的 PNG 图片保留天数
    'filtered_crypto_list': 30, # data/filtered_crypto_list_*.json
    'alpha_crypto_list': 30,    # data/alpha_crypto_list_*.json
    'trend_signals': 60,        # data/trend_signals_*.json（趋势数据保留更久）
    'platforms': 30,            # data/platforms/*_projects_*.json
    # advices 由 git 追踪管理，不自动清理
    'prompts': 30,              # prompts/ 下的提示词文件
}

# 需要屏蔽的代币列表
# 可以使用符号(symbol)、名称(name)或ID进行匹配
# 例如: ["BTC", "Bitcoin", "ETH", "Ethereum"]
BLOCK_TOKEN_LIST = ["KOGE"]

# 市场情绪指标配置
MARKET_SENTIMENT = {
    # API端点
    'binance_alpha_url': 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing',  # 币安Alpha项目列表API
}

def _optional_number(name, converter):
    value = os.getenv(name)
    return converter(value) if value not in (None, '') else None


def _env_with_legacy(name, legacy_name, default=''):
    if name in os.environ:
        return os.environ[name]
    return os.getenv(legacy_name, default)


def _resolve_llm_api_url():
    api_url = os.getenv('LLM_API_URL')
    if api_url:
        return api_url

    base_url = os.getenv('LLM_BASE_URL')
    if base_url:
        return f"{base_url.rstrip('/')}/chat/completions"

    # 兼容旧版 DeepSeek 配置。
    return os.getenv(
        'DEEPSEEK_API_URL',
        'https://api.deepseek.com/v1/chat/completions',
    )


# 通用 OpenAI Chat Completions 兼容接口配置。
LLM_CONFIG = {
    'api_url': _resolve_llm_api_url(),
    'model': _env_with_legacy('LLM_MODEL', 'DEEPSEEK_MODEL', 'deepseek-reasoner'),
    'api_key': _env_with_legacy('LLM_API_KEY', 'DEEPSEEK_API_KEY'),
    'api_key_header': os.getenv('LLM_API_KEY_HEADER', 'Authorization'),
    'api_key_prefix': os.getenv('LLM_API_KEY_PREFIX', 'Bearer'),
    'temperature': _optional_number('LLM_TEMPERATURE', float),
    'max_tokens': _optional_number('LLM_MAX_TOKENS', int),
    'max_tokens_param': os.getenv('LLM_MAX_TOKENS_PARAM', 'max_tokens'),
    'top_p': _optional_number('LLM_TOP_P', float),
    'timeout': int(
        os.getenv('LLM_API_TIMEOUT')
        or os.getenv('DEEPSEEK_API_TIMEOUT', '900')
    ),
}

# 为引用旧配置名称的外部代码保留兼容别名。
DEEPSEEK_AI = LLM_CONFIG
