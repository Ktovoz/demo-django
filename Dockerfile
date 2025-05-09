# 使用Python 3.9作为基础镜像
FROM python:3.9-slim-buster AS builder

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# 最终阶段
FROM python:3.9-slim-buster

# 创建非root用户
RUN useradd -m appuser

WORKDIR /app

# 复制之前构建的wheels
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建必要的目录
RUN mkdir -p /app/demo/static /app/staticfiles /app/media /app/data && \
    chown -R appuser:appuser /app

# 复制项目文件
COPY . .

# 添加执行权限到启动脚本
RUN chmod +x entrypoint.sh && \
    chown -R appuser:appuser /app

# 切换到非root用户
USER appuser

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["./entrypoint.sh"]