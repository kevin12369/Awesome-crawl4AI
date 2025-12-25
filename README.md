# Awesome-crawl4AI

> 基于 Crawl4AI 的可视化个人爬取平台 - 艹，让网页数据采集变得简单！

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.4+-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-red.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Beta-success.svg)]()

## 🎯 项目简介

**Awesome-crawl4AI** 是一个基于开源项目 [Crawl4AI](https://github.com/unclecode/crawl4ai) 构建的个人可视化爬取平台，专为非商业化场景设计。它提供了人性化的Web界面，让你无需编程即可轻松采集网页数据。

**核心定位：** 个人项目，永不商业化，注重用户体验和功能优化。

---

## ✨ 核心特性

### 🎨 可视化界面
- **现代化 Dashboard**：实时监控爬取任务状态
- **场景模板管理**：预置 5 种常见场景，可视化编辑器自定义场景
- **结果展示**：Markdown 预览、JSON 视图、数据导出

### 🤖 智能场景模板
| 场景 | 用途 | 分类 |
|------|------|------|
| NewsCrawler | 新闻文章爬取 | news |
| DocsArchiver | 技术文档归档 | docs |
| EcommerceMonitor | 电商价格监控 | ecommerce |
| AcademicCollector | 学术论文收集 | academic |
| TableExtractor | 表格数据提取 | table |

### 🔧 高级功能
- **无代码场景编辑器**：拖拽式字段配置，自动验证
- **批量爬取**：支持多URL并发爬取
- **深度爬取**：BFS/DFS 策略，自动发现页面链接
- **智能提取**：CSS 选择器、XPath、正则表达式支持

### 🚀 技术亮点
- **异步架构**：FastAPI + Vue 3 全栈异步
- **零配置数据库**：SQLite 开箱即用
- **Docker 部署**：一行命令启动全部服务
- **类型安全**：Python Type Hints + TypeScript

---

## 📦 快速开始

### 方式一：Docker 部署（推荐）⭐

```bash
# 1. 克隆项目 / Clone the project
git clone https://github.com/kevin12369/Awesome-crawl4AI.git
cd Awesome-crawl4AI

# 2. 启动服务 / Start services
docker-compose up -d

# 3. 访问应用 / Access application
# 浏览器打开 http://localhost:8000
```

**就这么简单！** 艹，Docker 真香！

### 方式二：本地开发部署

**后端设置：**
```bash
cd backend

# 创建虚拟环境 / Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖 / Install dependencies
pip install -r requirements.txt

# 初始化数据库 / Initialize database
python -c "from models.database import init_db; import asyncio; asyncio.run(init_db())"

# 启动后端 / Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**前端设置（新终端）：**
```bash
cd frontend

# 安装依赖 / Install dependencies
npm install

# 启动前端 / Start frontend
npm run dev
```

访问：
- **前端界面**：http://localhost:5173
- **后端 API**：http://localhost:8000
- **API 文档**：http://localhost:8000/docs

---

## 🎮 使用指南

### 1️⃣ 快速爬取

1. 打开 **Dashboard** 页面
2. 输入目标 URL
3. 选择场景模板（或使用默认）
4. 点击 **「开始爬取」**

### 2️⃣ 使用场景模板

1. 进入 **场景模板** 页面
2. 浏览内置场景（NewsCrawler、DocsArchiver 等）
3. 点击 **「应用」** 使用模板

### 3️⃣ 创建自定义场景

1. 点击 **「+ 新建模板」**
2. 填写基本信息（名称、描述、分类）
3. 添加提取字段（名称、CSS 选择器、类型）
4. 配置高级选项（延迟、深度爬取等）
5. 验证并保存

**详细教程：** [场景开发指南](docs/SCENARIO_GUIDE.md)

---

## 📁 项目结构

```
Awesome-crawl4AI/
├── backend/                    # 后端代码 / Backend
│   ├── api/                   # API 端点 / API endpoints
│   │   ├── crawl.py          # 爬取相关接口
│   │   ├── templates.py      # 模板管理接口
│   │   └── monitor.py        # 监控接口
│   ├── core/                  # 核心模块 / Core modules
│   │   ├── crawler.py        # Crawl4AI 封装
│   │   ├── template_engine.py # 模板引擎
│   │   └── scenario_registry.py # 场景注册表
│   ├── models/                # 数据模型 / Data models
│   │   ├── database.py       # 数据库连接
│   │   ├── template.py       # 模板模型
│   │   └── task.py           # 任务模型
│   ├── scenarios/             # 内置场景 / Built-in scenarios
│   │   ├── base.py           # 基类
│   │   ├── news_crawler.py   # 新闻爬取
│   │   ├── docs_archiver.py  # 文档归档
│   │   ├── ecommerce_monitor.py # 电商监控
│   │   ├── academic_collector.py # 学术收集
│   │   └── table_extractor.py # 表格提取
│   ├── schemas/               # Pydantic 模式
│   └── main.py               # FastAPI 应用入口
│
├── frontend/                   # 前端代码 / Frontend
│   ├── src/
│   │   ├── api/              # API 客户端
│   │   ├── components/       # Vue 组件
│   │   ├── stores/           # Pinia 状态管理
│   │   ├── types/            # TypeScript 类型
│   │   ├── views/            # 页面视图
│   │   │   ├── Dashboard.vue        # 主控面板
│   │   │   ├── ScenarioTemplates.vue # 场景模板
│   │   │   ├── TemplateEditor.vue   # 模板编辑器
│   │   │   ├── Results.vue          # 结果展示
│   │   │   ├── Tutorial.vue         # 交互教程
│   │   │   └── Settings.vue         # 系统设置
│   │   ├── router/           # Vue Router 配置
│   │   └── main.ts           # 应用入口
│   └── package.json
│
├── docs/                       # 文档 / Documentation
│   ├── API.md               # API 接口文档
│   ├── SCENARIO_GUIDE.md    # 场景开发指南
│   └── DEPLOYMENT.md        # 部署指南
│
├── docker-compose.yml         # Docker 编排配置
├── Dockerfile                 # Docker 镜像构建
└── README.md                  # 本文件
```

---

## 🔌 API 文档

### 核心接口

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/crawl` | POST | 创建爬取任务 |
| `/api/crawl/batch` | POST | 批量创建任务 |
| `/api/crawl/tasks` | GET | 获取任务列表 |
| `/api/crawl/tasks/{id}` | GET | 获取任务详情 |
| `/api/templates` | GET | 获取模板列表 |
| `/api/templates` | POST | 创建自定义模板 |
| `/api/health` | GET | 健康检查 |

**完整 API 文档：** [API.md](docs/API.md)

---

## 🛠️ 开发指南

### 环境要求

| 组件 | 版本要求 |
|------|----------|
| Python | 3.11+ |
| Node.js | 20+ |
| Docker | 20.10+（可选） |

### 代码规范

**后端（Python）：**
- 遵循 PEP 8
- 使用 Black 格式化
- 添加类型注解（Type Hints）
- 编写 Docstring（Google Style）

**前端（TypeScript/Vue）：**
- 使用 Composition API
- TypeScript 严格模式
- ESLint + Prettier

### 测试

```bash
# 后端测试 / Backend tests
cd backend
pytest

# 前端测试 / Frontend tests
cd frontend
npm run test
```

---

## 📊 系统截图

> TODO: 添加截图

---

## 🗺️ 开发路线图

### ✅ 已完成 / Completed

- [x] 项目架构设计
- [x] 基础 UI 框架（Vue 3 + Element Plus）
- [x] Crawl4AI 封装层
- [x] 模板引擎和场景系统
- [x] 5 个内置场景模板
- [x] 可视化模板编辑器
- [x] 任务管理和结果展示
- [x] Docker 部署配置
- [x] 完整文档

### 🚧 进行中 / In Progress

- [ ] 交互式教程系统
- [ ] 单元测试覆盖

### 📋 计划中 / Planned

- [ ] 用户认证系统
- [ ] 任务调度和定时执行
- [ ] 数据导出（CSV、Excel）
- [ ] 性能监控和日志
- [ ] 更多内置场景
- [ ] 移动端适配

---

## 🤝 贡献指南

欢迎贡献代码、报告 Bug 或提出新功能建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

**注意：** 本项目为个人非商业项目，请遵守项目定位。

---

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证。

---

## 🔗 相关资源

- **Crawl4AI 官方仓库：** [https://github.com/unclecode/crawl4ai](https://github.com/unclecode/crawl4ai)
- **项目文档：**
  - [API 文档](docs/API.md)
  - [场景开发指南](docs/SCENARIO_GUIDE.md)
  - [部署指南](docs/DEPLOYMENT.md)
- **问题反馈：** [GitHub Issues](https://github.com/kevin12369/Awesome-crawl4AI/issues)

---

## ⚠️ 免责声明

本项目仅供学习和个人使用，请勿用于商业目的。使用本项目爬取数据时，请遵守：

- 目标网站的 robots.txt 规则
- 相关法律法规
- 网站服务条款

**艹，别tm拿这个干违法的事！**

---

## 💬 致谢

感谢以下开源项目：

- [Crawl4AI](https://github.com/unclecode/crawl4ai) - 核心爬取引擎
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化 Python Web 框架
- [Vue 3](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Element Plus](https://element-plus.org/) - 优秀的 Vue 3 UI 组件库

---

<div align="center">

**如果这个项目对你有帮助，请给个 Star ⭐**

**Built with ❤️ by [kevin12369](https://github.com/kevin12369)**

</div>
