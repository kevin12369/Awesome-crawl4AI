# 艹，多阶段构建Docker镜像 - 先构建前端，再构建后端
# Multi-stage Dockerfile - Build frontend first, then backend

# ============================================
# 阶段1: 构建前端 / Stage 1: Build Frontend
# ============================================
FROM node:20-alpine AS frontend-builder

# 设置工作目录 / Set working directory
WORKDIR /app/frontend

# 复制前端依赖文件 / Copy frontend dependency files
COPY frontend/package*.json ./

# 安装依赖 / Install dependencies
RUN npm ci --only=production

# 复制前端源码 / Copy frontend source
COPY frontend/ ./

# 构建前端 / Build frontend
RUN npm run build

# ============================================
# 阶段2: 准备Python后端环境 / Stage 2: Python Backend
# ============================================
FROM python:3.11-slim

# 设置工作目录 / Set working directory
WORKDIR /app

# 安装系统依赖 / Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    playwright-driver \
    && rm -rf /var/lib/apt/lists/*

# 安装Playwright浏览器依赖 / Install Playwright browser dependencies
RUN playwright install --with-deps chromium

# 复制requirements.txt / Copy requirements.txt
COPY backend/requirements.txt ./backend/requirements.txt

# 安装Python依赖 / Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# 复制后端代码 / Copy backend code
COPY backend/ ./backend/

# 从frontend-builder阶段复制构建产物 / Copy build artifacts from frontend stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# 创建数据目录 / Create data directories
RUN mkdir -p /app/data

# 设置环境变量 / Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 暴露端口 / Expose port
EXPOSE 8000

# 健康检查 / Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# 启动命令 / Startup command
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
