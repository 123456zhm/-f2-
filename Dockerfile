FROM python:3.10-slim

WORKDIR /app

# 先复制依赖文件，利用 Docker 缓存
COPY f2/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目
COPY . .

# 确保 f2 包目录在 Python 路径中
ENV PYTHONPATH=/app/f2

# CloudBase 注入 PORT 环境变量，默认 8000
EXPOSE 8000

CMD ["sh", "-c", "cd /app/f2 && python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
