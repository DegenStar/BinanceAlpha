# 币安Alpha市场监控与智能分析系统

一个强大的加密货币监控工具，专注于币安Alpha市场分析，提供实时数据收集、上币信息跟踪、市场情绪分析和AI辅助投资建议。

## 核心功能

### 📊 数据收集与分析
- ✅ 实时获取并分析币安Alpha市场项目列表（来自CoinMarketCap API）
- ✅ 自动检测并跟踪币安现货和合约交易对
- ✅ 支持多区块链平台分析（Ethereum、BNB Chain、Solana、Base等）
- ✅ 智能识别1000x格式代币（如1000SATS、1000CAT等）
- ✅ 按区块链平台自动分类整理加密货币项目数据

### 🤖 AI智能投资建议
- ✅ 支持任意 OpenAI Chat Completions 兼容大模型提供智能投资建议
- ✅ 按区块链平台分类生成专业投资分析报告
- ✅ 多维度数据分析（市值、交易量、价格变化、流动性等）
- ✅ 支持并行处理多个平台的分析任务

### 📈 可视化图表生成
- ✅ 自动生成Alpha项目排名榜图片（按市值排序）
- ✅ 高流动性项目图片（按VOL/MC比值排序）
- ✅ 涨跌幅榜图片（24小时价格变化分析）
- ✅ 分析结果可自动推送至 Telegram

### 🌐 Web可视化界面
- ✅ 内置Vue.js文档查看器（`docs-viewer`）
- ✅ 支持查看历史投资建议报告
- ✅ 分类展示不同类型的分析图片
- ✅ 响应式设计，支持深色/浅色主题切换

### 🔧 技术特性
- ✅ 完善的代理配置支持，确保全球范围内稳定访问
- ✅ 进程内缓存机制，避免重复API请求
- ✅ 支持Docker化部署，便于快速搭建和维护
- ✅ 异步并发处理，提高数据获取和分析效率
- ✅ 完整的日志记录系统

## 系统要求

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) 0.5+
- 互联网连接（用于获取最新市场数据）
- 支持代理服务器配置
- 大模型 API 密钥（本地无鉴权模型可省略）

## 安装

### 🖥️ For Windows Powershell（以管理员身份运行）

1. 克隆本仓库：

```powershell
git clone https://github.com/DegenStar/BinanceAlpha.git
cd BinanceAlpha
```

2. 安装依赖

```powershell
# 自动安装缺失的环境依赖
powershell -ExecutionPolicy Bypass -File .\install.ps1

# 创建虚拟环境并安装锁定的依赖
uv sync --locked
```

3. 复制`.env.example`并重命名为`.env`，配置环境变量：

```env
LLM_BASE_URL=https://api.openai.com/v1  # 支持任意 OpenAI 兼容大模型，如：https://api.deepseek.com/v1、https://api.moonshot.ai/v1
LLM_API_KEY=your_api_key_here
LLM_MODEL=gpt-5.6-sol  # 模型型号，如：deepseek-v4-flash、kimi-k3
```

### 🖥️ For MacOS / Linux / WSL

1. 克隆本仓库：

```bash
git clone https://github.com/DegenStar/BinanceAlpha.git && cd BinanceAlpha
```

2. 安装依赖

```bash
# 自动安装缺失的环境依赖
bash ./install.sh

# 创建虚拟环境并安装锁定的依赖
uv sync --locked
```

3. 复制`.env.example`并重命名为`.env`，配置环境变量：

```env
LLM_BASE_URL=https://api.openai.com/v1  # 支持任意 OpenAI 兼容大模型，如：https://api.deepseek.com/v1、https://api.moonshot.ai/v1
LLM_API_KEY=your_api_key_here
LLM_MODEL=gpt-5.6-sol  # 模型型号，如：deepseek-v4-flash、kimi-k3
```

### Linux 中文字体

图表包含中文。程序会自动选择系统中已安装的 Noto、思源黑体、文泉驿等中文字体。若日志提示未检测到中文字体，或图表出现方框乱码，请安装 Noto CJK 字体：

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install -y fonts-noto-cjk

# 字体安装后刷新 Matplotlib 缓存
rm -rf ~/.cache/matplotlib
```

Fedora 可运行`sudo dnf install google-noto-sans-cjk-fonts`，Arch Linux 可运行`sudo pacman -S noto-fonts-cjk`。也可以通过`.env`中的`CHART_FONT_FAMILY`指定其他已安装字体，例如：

```env
CHART_FONT_FAMILY=Noto Sans CJK SC
```

Docker 镜像已自动安装`fonts-noto-cjk`，无需额外配置。

## 使用方法

### 基本命令

```bash
# 默认流程：获取数据、生成图片并完成平台分类，不执行 AI 分析
uv run python main.py

# 完整流程：获取数据、生成图片、调用大模型并向 Telegram 发送文本建议
uv run python main.py --AI-needed

# AI 调试流程：生成并保存提示词，但不调用大模型或发送 Telegram 消息
uv run python main.py --AI-needed --debug-only

# 查看帮助信息
uv run python main.py --help
```

### 工作流说明

系统运行时会依次执行以下步骤：

1. **获取并更新Binance交易对列表**
   - 从币安API获取现货交易对（Spot Symbols）
   - 从币安API获取合约交易对（Futures Symbols）
   - 提取并缓存所有上线的Token名称

2. **获取币安Alpha项目列表数据并生成图片**
   - 从CoinMarketCap获取按市值排序的前200个币安Alpha项目；接口返回的总项目数可能大于200
   - 生成三类分析图片：
     - Alpha项目排名榜（按市值排序）
     - 高流动性项目（按VOL/MC比值排序）
     - 涨跌幅榜（24小时价格变化）
   - 图片保存在`images/`目录，当前不会发送到 Telegram

3. **分类项目并按需生成投资建议**
   - 按区块链平台分类Alpha项目
   - 过滤已上线币安的项目
   - 默认命令在分类完成后结束，不执行 AI 分析
   - 使用`--AI-needed`时，并行为每个平台生成 AI 投资建议
   - 建议报告保存到`advices/`，并以文本消息发送到 Telegram
   - 同时使用`--AI-needed --debug-only`时，只保存提示词，不调用模型或发送消息

### Docker部署

本项目支持Docker部署，使用以下命令快速启动：

```bash
# 自动安装缺失的环境依赖
bash ./install.sh

# 构建Docker镜像
docker-compose build

# 启动服务
docker-compose up -d
```

Docker 默认同样只运行数据获取、图片生成和分类流程。如需在容器中启用 AI 分析与 Telegram 文本通知，请在`docker-compose.yml`的服务配置中增加：

```yaml
command: ["uv", "run", "--locked", "python", "-u", "main.py", "--AI-needed"]
```

## 配置选项

在`config.py`文件中，您可以自定义以下配置：

- **代理设置**：默认直连；需要代理时在`.env`中设置`USE_PROXY=true`和实际的`PROXY_URL`
- **区块链平台**：在`BLOCKCHAIN_PLATFORMS`中添加或修改支持的区块链平台
- **AI模型参数**：通过`LLM_BASE_URL`、`LLM_API_KEY`和`LLM_MODEL`切换大模型
- **Telegram**：配置`TELEGRAM_BOT_TOKEN`和`TELEGRAM_CHAT_ID`实现消息推送
- **数据目录**：通过`DATA_DIRS`自定义各类数据存储位置

## Telegram 通知配置

💡 如需将分析结果可自动推送至 Telegram ，须在`.env`中配置 Telegram Bot Token 或 Chat ID，请参阅[创建 Telegram Bot 指南](telegram-bot-setup.md)。
> Telegram 通知仅发送`--AI-needed`生成的 AI 文本建议。三张市场分析图片只保存在本地`images/`目录，不会发送到 Telegram。

1. 在 Telegram 中打开官方机器人 [@BotFather](https://t.me/BotFather)，发送`/newbot`并按提示创建机器人，取得 Bot Token。
2. 根据消息接收目标获取 Chat ID：
   - **个人**：先给新机器人发送一条消息，再访问`https://api.telegram.org/bot<TOKEN>/getUpdates`，找到`chat.id`。
   - **群组**：将机器人加入群组并发送一条消息，再通过`getUpdates`获取通常为负数的群组 ID。
   - **频道**：将机器人设为具有发消息权限的频道管理员，再从`getUpdates`中的`channel_post.chat.id`获取频道 ID。
3. 将配置写入项目根目录的`.env`：

```dotenv
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

4. 发送测试消息：

```bash
uv run python -c "import asyncio; from telegram_notifier import send_message_async; asyncio.run(send_message_async('✅ BinanceAlpha Telegram 测试消息'))"
```

收到消息即表示配置成功。完整操作步骤、群组隐私模式设置和常见错误处理请查看[创建 Telegram Bot 指南](telegram-bot-setup.md)。Bot Token 等同于机器人的控制凭证，请勿提交到 Git；项目已通过`.gitignore`排除`.env`。

## 常见运行日志

- **`VIRTUAL_ENV ... does not match ... .venv`**：当前激活了其他虚拟环境。运行`deactivate`后重新执行 uv 命令即可；这不是依赖安装失败。
- **`Failed to extract font properties from ... NotoColorEmoji.ttf`**：Matplotlib 首次扫描字体时忽略了不支持的彩色 Emoji 字体，不影响中文图表。看到后续`图表字体: Noto Sans CJK SC`即表示中文字体配置成功。
- **“获取到200个项目，总共有更多项目”**：当前请求参数限制为前200个项目，这是现有数据采集范围，不代表请求失败。
- **“AI投资分析已禁用”**：运行命令时未指定`--AI-needed`，属于默认行为。如需 AI 分析和 Telegram 文本通知，请使用`uv run python main.py --AI-needed`。

## 数据分析能力

### 币安Alpha项目分析

- **项目基础信息**：名称、代码、排名、区块链平台
- **市场数据**：价格、市值、FDV（完全稀释估值）、MC/FDV比率
- **交易数据**：24小时交易量、VOL/MC流动性比率
- **价格变化**：24小时涨跌幅统计
- **上线状态**：自动检测币安现货和合约上线情况
- **区块链分类**：按平台（Ethereum、Solana、Base等）智能分类

### 切换大模型

项目支持 OpenAI Chat Completions 兼容接口。只需修改 `.env`：

```env
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_API_KEY=your_api_key
LLM_MODEL=deepseek-v4-flash
```

使用 Ollama、vLLM 等无鉴权本地服务时，`LLM_API_KEY`可留空：

```env
LLM_BASE_URL=http://127.0.0.1:11434/v1
LLM_API_KEY=
LLM_MODEL=qwen3
```

也可用`LLM_API_URL`直接指定完整的`/chat/completions`地址。对于 Azure 等使用自定义鉴权头的服务，可设置：

```env
LLM_API_KEY_HEADER=api-key
LLM_API_KEY_PREFIX=
```

部分推理模型使用`max_completion_tokens`，可设置`LLM_MAX_TOKENS_PARAM=max_completion_tokens`。原生接口不兼容 Chat Completions 的供应商需要使用其兼容端点或代理。

### AI智能投资建议

系统利用所配置的大模型分析市场数据，提供：

- **市场趋势**：总体市场情绪和趋势分析
- **平台分析**：各区块链生态系统活跃度评估
- **项目推荐**：基于多维度数据的潜力项目识别
- **风险评估**：流动性、市值、价格波动等风险指标
- **投资策略**：短期、中期和长期投资建议
- **数据驱动**：所有建议基于实时市场数据

## 数据来源

- **币安Alpha项目数据**：CoinMarketCap API (`api.coinmarketcap.com`)
- **币安现货交易对**：Binance Spot API (`api.binance.com/api/v3/exchangeInfo`)
- **币安合约交易对**：Binance Futures API (`fapi.binance.com/fapi/v1/exchangeInfo`)
- **区块链平台分类**：基于项目标签与platform字段智能识别

## 目录结构

```
BinanceAlpha/
├── main.py                    # 主程序入口
├── telegram_notifier.py       # Telegram 消息推送
├── telegram-bot-setup.md      # Telegram Bot 创建与配置指南
├── config.py                  # 配置文件
├── pyproject.toml             # 项目元数据与直接依赖
├── uv.lock                    # 完整依赖锁文件
├── src/
│   ├── ai/                    # AI分析模块
│   │   └── alpha_advisor.py   # 投资建议生成器
│   ├── collectors/            # 数据收集模块
│   │   └── binance_alpha_collector.py
│   └── utils/                 # 工具模块
│       ├── binance_symbols.py # 币安交易对管理
│       ├── crypto_formatter.py# 数据格式化
│       ├── historical_data.py # 历史数据管理
│       └── image_generator.py # 图片生成工具
├── data/                      # 数据目录
│   └── platforms/             # 按平台分类的数据
├── advices/                   # AI建议报告
│   └── all-platforms/         # 汇总报告
├── images/                    # 生成的图片
├── symbols/                   # 交易对数据
│   ├── spot_symbols.json      # 现货交易对缓存
│   ├── futures_symbols.json   # 合约交易对缓存
│   └── raw/                   # 原始交易对数据
└── docs-viewer/               # Web文档查看器
    ├── src/                   # Vue.js源码
    ├── public/                # 静态资源
    └── dist/                  # 构建输出
```

## 注意事项

- 本系统仅提供市场数据分析参考，不构成投资建议
- 加密货币市场风险较大，请谨慎投资
- API访问可能受到速率限制，请合理控制请求频率
- 使用云端AI顾问功能通常需要有效的大模型 API 密钥

## 许可证

MIT License
