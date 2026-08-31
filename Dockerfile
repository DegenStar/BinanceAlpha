FROM ghcr.io/astral-sh/uv:0.11.6 AS uv
FROM python:3.12-slim

COPY --from=uv /uv /uvx /bin/

# 设置环境变量，禁用Python的输出缓冲
ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv

# 设置构建时的代理环境变量
ARG HTTP_PROXY
ARG HTTPS_PROXY

WORKDIR /app

# 先复制依赖声明以利用 Docker 构建缓存
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

# 复制程序文件
COPY . .

# 设置运行时的代理环境变量
ENV HTTP_PROXY=${HTTP_PROXY:-""}
ENV HTTPS_PROXY=${HTTPS_PROXY:-""}

# 运行程序
CMD ["uv", "run", "--locked", "python", "-u", "main.py"]
