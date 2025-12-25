# Awesome-crawl4AI 部署文档

艹，这是完整的部署指南，跟着Kevin一步步来，保证能跑起来！

---

## 目录 / Table of Contents

- [系统要求 / System Requirements](#系统要求)
- [方式一：Docker 部署（推荐）](#方式一docker-部署推荐)
- [方式二：本地开发部署](#方式二本地开发部署)
- [验证部署 / Verify Deployment](#验证部署)
- [常见问题 / Troubleshooting](#常见问题)
- [生产环境配置 / Production Configuration](#生产环境配置)

---

## 系统要求 / System Requirements

### 最低配置 / Minimum Requirements

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| 操作系统 | Windows 10+ / macOS 10.15+ / Linux | 任意主流Linux发行版 |
| CPU | 2核心 | 4核心+ |
| 内存 | 4GB | 8GB+ |
| 磁盘空间 | 5GB | 20GB+ |
| 网络 | 稳定的互联网连接 | 稳定的互联网连接 |

### 软件依赖 / Software Dependencies

**Docker 部署（推荐）：**
- Docker Engine 20.10+
- Docker Compose 2.0+

**本地开发部署：**
- Python 3.11+
- Node.js 20+
- npm 或 yarn

---

## 方式一：Docker 部署（推荐）/ Method 1: Docker Deployment (Recommended)

### 为什么选择 Docker / Why Docker

✅ 一键启动，无需配置环境
✅ 隔离环境，不影响系统
✅ 跨平台，Windows/macOS/Linux 通用
✅ 易于升级和维护

### 步骤 1：安装 Docker

**Windows / macOS：**
1. 访问 [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. 下载并安装
3. 启动 Docker Desktop
4. 验证安装：
   ```bash
   docker --version
   docker-compose --version
   ```

**Linux (Ubuntu/Debian)：**
```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo apt-get install docker-compose-plugin

# 验证安装
docker --version
docker compose version
```

### 步骤 2：获取项目代码

```bash
# 克隆项目 / Clone the project
git clone https://github.com/your-username/Awesome-crawl4AI.git
cd Awesome-crawl4AI
```

或者直接下载 ZIP 文件并解压。

### 步骤 3：配置环境变量

```bash
# 复制环境变量模板 / Copy environment template
cp .env.example .env

# 编辑 .env 文件（可选，使用默认值也可以）/ Edit .env (optional)
nano .env
```

**.env 文件说明 / .env File Explanation：**

```bash
# 数据库配置 / Database configuration
DATABASE_URL=sqlite+aiosqlite:///./data/crawl4ai.db

# CORS 配置 / CORS configuration
CORS_ORIGINS=http://localhost:8000,http://localhost:3000

# 日志级别 / Log level (debug, info, warning, error)
LOG_LEVEL=info

# API 配置 / API configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### 步骤 4：启动服务

**基础启动（仅主应用）/ Basic Start (Main App Only)：**

```bash
# 构建并启动 / Build and start
docker-compose up -d

# 查看日志 / View logs
docker-compose logs -f app

# 停止服务 / Stop services
docker-compose down
```

**完整启动（含 Nginx）/ Full Start (With Nginx)：**

```bash
# 启动主应用 + Nginx
docker-compose --profile production up -d
```

**带任务队列（含 Redis）/ With Task Queue (With Redis)：**

```bash
# 启动主应用 + Redis
docker-compose --profile with-redis up -d
```

**使用 PostgreSQL 替代 SQLite / Use PostgreSQL Instead of SQLite：**

```bash
# 启动主应用 + PostgreSQL
docker-compose --profile with-postgres up -d

# 修改 .env 中的 DATABASE_URL
DATABASE_URL=postgresql+asyncpg://crawl4ai:crawl4ai_password@postgres:5432/crawl4ai
```

### 步骤 5：验证服务

```bash
# 检查容器状态 / Check container status
docker-compose ps

# 应该看到 / Should see:
# awesome-crawl4ai-app      running
# awesome-crawl4ai-nginx    running (如果启用 / if enabled)
```

访问 `http://localhost:8000`，应该能看到 Dashboard 页面！

### 步骤 6：初始化数据库（首次运行）

```bash
# 进入容器 / Enter container
docker-compose exec app bash

# 初始化数据库 / Initialize database
cd backend
python -c "from models.database import init_db; import asyncio; asyncio.run(init_db())"

# 退出容器 / Exit container
exit
```

### 常用 Docker 命令 / Common Docker Commands

```bash
# 查看日志 / View logs
docker-compose logs -f app              # 实时日志 / Real-time logs
docker-compose logs --tail=100 app      # 最近100行 / Last 100 lines

# 重启服务 / Restart service
docker-compose restart app

# 重新构建 / Rebuild
docker-compose up -d --build

# 清理所有数据（危险操作）/ Clean all data (DANGEROUS)
docker-compose down -v
rm -rf data/

# 进入容器调试 / Enter container for debugging
docker-compose exec app bash

# 更新镜像 / Update images
docker-compose pull
docker-compose up -d
```

---

## 方式二：本地开发部署 / Method 2: Local Development Deployment

### 步骤 1：安装 Python 3.11+

**Windows：**
1. 访问 [Python.org](https://www.python.org/downloads/)
2. 下载 Python 3.11+ 安装包
3. 安装时勾选 **"Add Python to PATH"**

**macOS：**
```bash
# 使用 Homebrew
brew install python@3.11

# 验证安装
python3 --version
```

**Linux (Ubuntu/Debian)：**
```bash
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3-pip
```

### 步骤 2：安装 Node.js 20+

**使用 nvm（推荐）/ Using nvm (Recommended)：**

```bash
# 安装 nvm / Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 重新加载 Shell / Reload shell
source ~/.bashrc  # Linux
# 或
source ~/.zshrc   # macOS

# 安装 Node.js / Install Node.js
nvm install 20
nvm use 20
```

**Windows：**
1. 访问 [Node.js.org](https://nodejs.org/)
2. 下载 LTS 版本安装包

### 步骤 3：安装 Playwright 浏览器

```bash
# 安装 Playwright 及浏览器 / Install Playwright and browsers
pip install playwright
playwright install --with-deps chromium
```

### 步骤 4：后端设置

```bash
# 进入后端目录 / Enter backend directory
cd backend

# 创建虚拟环境 / Create virtual environment
python -m venv venv

# 激活虚拟环境 / Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 安装依赖 / Install dependencies
pip install -r requirements.txt

# 复制环境变量 / Copy environment variables
cp .env.example .env

# 初始化数据库 / Initialize database
python -c "from models.database import init_db; import asyncio; asyncio.run(init_db())"
```

### 步骤 5：前端设置

**新开一个终端 / Open a new terminal：**

```bash
# 进入前端目录 / Enter frontend directory
cd frontend

# 安装依赖 / Install dependencies
npm install
# 或
yarn install

# 复制环境变量 / Copy environment variables
cp .env.example .env
```

### 步骤 6：启动服务

**启动后端（第一个终端）/ Start Backend (First Terminal)：**

```bash
cd backend
# 确保虚拟环境已激活 / Make sure venv is activated
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**启动前端（第二个终端）/ Start Frontend (Second Terminal)：**

```bash
cd frontend
npm run dev
# 或
yarn dev
```

### 步骤 7：访问应用

- **前端开发服务器：** http://localhost:5173
- **后端 API：** http://localhost:8000
- **API 文档：** http://localhost:8000/docs

---

## 验证部署 / Verify Deployment

### 1. 健康检查 / Health Check

```bash
# 方式1：浏览器访问 / Method 1: Browser
访问 http://localhost:8000/api/health

# 方式2：curl 命令 / Method 2: curl command
curl http://localhost:8000/api/health

# 应该返回 / Should return:
{
  "code": 200,
  "message": "healthy",
  "data": {
    "status": "healthy",
    "version": "1.0.0"
  }
}
```

### 2. 测试爬取功能 / Test Crawl Function

1. 打开浏览器访问 `http://localhost:8000`
2. 在 Dashboard 页面输入测试URL：
   ```
   https://example.com
   ```
3. 点击 **「开始爬取」**
4. 等待几秒，查看结果

### 3. 检查日志 / Check Logs

**Docker 部署：**
```bash
docker-compose logs -f app
```

**本地部署：**
查看终端输出，应该没有错误信息。

---

## 常见问题 / Troubleshooting

### Q1: Docker 启动失败

**错误信息：**
```
Error: Cannot connect to the Docker daemon
```

**解决方案：**
```bash
# 启动 Docker Desktop / Start Docker Desktop
# 或 Linux 上启动 Docker 服务 / Or start Docker service on Linux
sudo systemctl start docker
sudo systemctl enable docker
```

---

### Q2: 端口被占用

**错误信息：**
```
Error: Port 8000 is already in use
```

**解决方案：**

**方法1：停止占用端口的进程 / Method 1: Stop the process**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <进程ID> /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

**方法2：修改端口 / Method 2: Change port**

编辑 `docker-compose.yml` 或 `.env`：
```yaml
ports:
  - "8001:8000"  # 改用8001端口
```

---

### Q3: 数据库初始化失败

**错误信息：**
```
sqlite3.OperationalError: unable to open database file
```

**解决方案：**
```bash
# 创建数据目录 / Create data directory
mkdir -p data

# 检查权限 / Check permissions
chmod 755 data
```

---

### Q4: Playwright 浏览器未安装

**错误信息：**
```
Executable doesn't exist at /path/to/chromium
```

**解决方案：**
```bash
# 安装 Playwright 浏览器 / Install Playwright browsers
playwright install --with-deps chromium
```

---

### Q5: 前端无法连接后端

**错误信息：**
```
Network Error / ERR_CONNECTION_REFUSED
```

**解决方案：**

1. **检查后端是否运行 / Check if backend is running**
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **检查前端代理配置 / Check frontend proxy config**

   查看 `frontend/vite.config.ts`：
   ```typescript
   server: {
     proxy: {
       '/api': {
         target: 'http://localhost:8000',
         changeOrigin: true,
       }
     }
   }
   ```

3. **检查 CORS 配置 / Check CORS config**

   查看 `backend/.env`：
   ```bash
   CORS_ORIGINS=http://localhost:5173,http://localhost:8000
   ```

---

### Q6: 爬取失败，返回空结果

**可能原因 / Possible Causes：**

1. **网站有反爬机制 / Website has anti-scraping**
   - 解决方案：增加延迟时间
   ```python
   advanced=AdvancedConfig(delay=2.0)
   ```

2. **JavaScript 动态渲染 / JavaScript rendering**
   - 解决方案：启用滚动加载
   ```python
   advanced=AdvancedConfig(scroll_to_load=True, max_scrolls=5)
   ```

3. **CSS 选择器不正确 / Incorrect CSS selector**
   - 解决方案：使用浏览器开发者工具验证选择器

---

## 生产环境配置 / Production Configuration

### 使用 Nginx 反向代理

**1. 创建 Nginx 配置文件 / Create Nginx config**

创建 `nginx/nginx.conf`：

```nginx
events {
    worker_connections 1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    upstream backend {
        server app:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        # 前端静态文件 / Frontend static files
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }

        # API 代理 / API proxy
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket 支持 / WebSocket support
        location /ws {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

**2. 启动生产环境 / Start production**

```bash
docker-compose --profile production up -d
```

### 配置 HTTPS（使用 Let's Encrypt）

**1. 安装 Certbot / Install Certbot**

```bash
# 在宿主机上安装 / Install on host machine
sudo apt-get install certbot
```

**2. 获取证书 / Get certificate**

```bash
sudo certbot certonly --standalone -d your-domain.com
```

**3. 修改 Nginx 配置 / Modify Nginx config**

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # ... 其他配置
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### 使用 PostgreSQL 数据库

**1. 修改 docker-compose.yml**

```yaml
services:
  postgres:
    image: postgres:15-alpine
    container_name: awesome-crawl4ai-postgres
    environment:
      POSTGRES_DB: crawl4ai
      POSTGRES_USER: crawl4ai
      POSTGRES_PASSWORD: your_secure_password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - crawl4ai-network
    profiles:
      - with-postgres

volumes:
  postgres-data:
```

**2. 修改 .env**

```bash
DATABASE_URL=postgresql+asyncpg://crawl4ai:your_secure_password@postgres:5432/crawl4ai
```

**3. 启动服务 / Start services**

```bash
docker-compose --profile with-postgres up -d
```

### 配置自动备份

**创建备份脚本 / Create backup script**

`scripts/backup.sh`：

```bash
#!/bin/bash

# 艹，数据库备份脚本 / Database backup script

BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_FILE="./data/crawl4ai.db"

# 创建备份目录 / Create backup directory
mkdir -p $BACKUP_DIR

# 备份数据库 / Backup database
cp $DB_FILE $BACKUP_DIR/crawl4ai_$DATE.db

# 压缩备份 / Compress backup
gzip $BACKUP_DIR/crawl4ai_$DATE.db

# 删除7天前的备份 / Delete backups older than 7 days
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: crawl4ai_$DATE.db.gz"
```

**添加定时任务 / Add cron job**

```bash
# 编辑 crontab
crontab -e

# 每天凌晨2点备份 / Backup daily at 2 AM
0 2 * * * cd /path/to/Awesome-crawl4AI && ./scripts/backup.sh
```

### 监控和日志

**查看实时日志 / View real-time logs**

```bash
docker-compose logs -f app
```

**日志持久化 / Log persistence**

修改 `docker-compose.yml`：

```yaml
services:
  app:
    volumes:
      - ./logs:/app/logs
    environment:
      - LOG_LEVEL=info
      - LOG_FILE=/app/logs/app.log
```

**使用日志管理工具 / Use log management tools**

```bash
# 安装 Loki/ Promtail（可选）/ Install Loki/Promtail (optional)
docker-compose -f docker-compose.logging.yml up -d
```

---

## 性能优化 / Performance Optimization

### 1. 启用缓存 / Enable Caching

```python
# 在爬取配置中启用缓存 / Enable cache in crawl config
config = {
    "cache_mode": "enabled"  # 或 "bypass" 绕过缓存
}
```

### 2. 并发爬取 / Concurrent Crawling

```bash
# 启动多个工作进程 / Start multiple worker processes
uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
```

### 3. 使用 Redis 任务队列 / Use Redis Task Queue

```bash
docker-compose --profile with-redis up -d
```

### 4. 数据库优化 / Database Optimization

```sql
-- 添加索引 / Add indexes
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

---

## 安全建议 / Security Recommendations

### 1. 修改默认端口

```bash
# .env
API_PORT=8888  # 不使用默认的8000
```

### 2. 启用 API 认证（未来版本）

```python
# TODO: 实现 JWT 认证
```

### 3. 限制访问频率

使用 Nginx 限流：

```nginx
http {
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    server {
        location /api {
            limit_req zone=api_limit burst=20;
        }
    }
}
```

### 4. 定期更新依赖

```bash
# 后端依赖更新 / Backend dependencies update
pip install --upgrade -r requirements.txt

# 前端依赖更新 / Frontend dependencies update
npm update
```

---

艹，部署文档写完了！有问题找Kevin！

**文档版本 / Version：** 1.0.0
**最后更新 / Last Updated：** 2025-12-25
