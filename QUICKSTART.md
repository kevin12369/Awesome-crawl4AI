# Awesome-crawl4AI 快速参考指南

## 项目概览

**Awesome-crawl4AI** 是一个专为 AI 应用优化的智能化网页数据采集框架。

### 核心特性
- 智能数据提取和解析
- AI 友好的输出格式（Markdown、JSON）
- JavaScript 渲染支持
- 高性能异步并发
- 可扩展的插件系统

## 项目结构

```
awesome-crawl4ai/
├── packages/
│   ├── crawler/          # 核心爬虫引擎
│   ├── extractors/       # 数据提取器
│   ├── processors/       # 数据处理器
│   └── integrations/     # 第三方集成
├── tests/                # 测试套件
├── examples/             # 示例代码
├── docs/                 # 详细文档
├── CLAUDE.md             # AI 上下文文档
├── README.md             # 项目说明
└── pyproject.toml        # 项目配置
```

## 快速开始

### 1. 安装

```bash
# 克隆项目
git clone <repository-url>
cd Awesome-crawl4AI

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -e .
```

### 2. 基础使用

```python
from crawl4ai import WebCrawler

# 创建爬虫实例
crawler = WebCrawler()

# 爬取网页
result = crawler.crawl("https://example.com")

# 获取结果
print(result.markdown)  # Markdown 格式
print(result.text)      # 纯文本
print(result.metadata)  # 元数据
```

### 3. 批量爬取

```python
urls = ["https://site1.com", "https://site2.com", "https://site3.com"]

results = crawler.crawl_batch(urls)
for result in results:
    print(f"{result.url}: {result.status_code}")
```

### 4. 自定义提取

```python
from crawl4ai.extractors import CSSExtractor

extractor = CSSExtractor({
    "title": "h1",
    "content": "article p",
    "author": ".author",
    "date": "time[datetime]"
})

result = crawler.crawl("https://blog.example.com", extractor=extractor)
print(result.data)  # {"title": "...", "content": [...], ...}
```

## 配置说明

### 环境变量配置

复制 `.env.example` 到 `.env` 并配置：

```bash
# 基础配置
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# 爬虫配置
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=30
MAX_RETRIES=3
DOWNLOAD_DELAY=1

# 代理配置（可选）
USE_PROXY=false
HTTP_PROXY=
HTTPS_PROXY=

# AI 服务（可选）
OPENAI_API_KEY=sk-...
```

### 代码配置

```python
from crawl4ai.crawler import CrawlerConfig

config = CrawlerConfig(
    max_concurrent=10,
    timeout=30,
    retries=3,
    use_proxy=False,
    rate_limit=5
)

crawler = WebCrawler(config)
```

## 开发指南

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/crawler/test_core.py

# 带覆盖率报告
pytest --cov=packages --cov-report=html
```

### 代码格式化

```bash
# 格式化代码
black .
isort .

# 检查代码
flake8 .
mypy .
```

### 预提交钩子

```bash
# 安装预提交钩子
pip install pre-commit
pre-commit install
```

## 模块详解

### Crawler（爬虫引擎）
- **职责**：网页爬取、请求调度、并发控制
- **主要类**：`WebCrawler`, `Scheduler`, `Middleware`
- **文档**：[packages/crawler/CLAUDE.md](packages/crawler/CLAUDE.md)

### Extractors（数据提取）
- **职责**：HTML 解析、文本提取、格式转换
- **主要类**：`HTMLExtractor`, `MarkdownExtractor`, `CSSExtractor`
- **文档**：[packages/extractors/CLAUDE.md](packages/extractors/CLAUDE.md)

### Processors（数据处理）
- **职责**：数据清洗、去重、质量检查、AI 优化
- **主要类**：`TextProcessor`, `MarkdownProcessor`, `AIProcessor`
- **文档**：[packages/processors/CLAUDE.md](packages/processors/CLAUDE.md)

### Integrations（服务集成）
- **职责**：存储、AI 服务、消息队列、监控
- **主要类**：`PostgreSQLStorage`, `OpenAIIntegration`, `RedisQueue`
- **文档**：[packages/integrations/CLAUDE.md](packages/integrations/CLAUDE.md)

## 常见用例

### 爬取博客文章

```python
from crawl4ai import WebCrawler
from crawl4ai.extractors import CSSExtractor

crawler = WebCrawler()

extractor = CSSExtractor({
    "title": "h1.post-title",
    "content": ".post-content p",
    "tags": ".tags a",
    "date": ".post-date"
})

result = crawler.crawl(
    url="https://blog.example.com/post/123",
    extractor=extractor
)

# 保存为 Markdown
with open("article.md", "w") as f:
    f.write(result.markdown)
```

### 批量采集数据

```python
from crawl4ai import WebCrawler
import csv

crawler = WebCrawler()
urls = [line.strip() for line in open("urls.txt")]

results = crawler.crawl_batch(urls, max_concurrent=5)

with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Title", "Text"])

    for result in results:
        if result.success:
            writer.writerow([
                result.url,
                result.metadata.get("title", ""),
                result.text[:500]  # 前 500 字符
            ])
```

### AI 数据准备

```python
from crawl4ai import WebCrawler
from crawl4ai.processors import AIProcessor

crawler = WebCrawler()
processor = AIProcessor(
    target_model="gpt-4",
    max_tokens=8000,
    include_metadata=True
)

result = crawler.crawl("https://example.com/article")
processed = await processor.process(result)

# 获取 AI 优化的内容
ai_content = processed.ai_ready_content
print(ai_content)
```

## 故障排除

### 问题：爬取失败
- 检查网络连接
- 增加超时时间
- 使用代理池
- 检查目标网站是否需要 JavaScript 渲染

### 问题：被网站封禁
- 降低并发数
- 增加请求延迟
- 轮换 User-Agent
- 使用代理池
- 尊重 robots.txt

### 问题：提取不准确
- 检查 CSS 选择器是否正确
- 使用浏览器开发者工具检查 DOM 结构
- 考虑使用 XPath 提取器
- 检查是否需要 JavaScript 渲染

## 相关资源

- **完整文档**：[CLAUDE.md](CLAUDE.md)
- **模块文档**：各模块目录下的 `CLAUDE.md`
- **示例代码**：[examples/](examples/)
- **API 参考**：[docs/api-reference.md](docs/api-reference.md)
- **贡献指南**：[CONTRIBUTING.md](CONTRIBUTING.md)

## 下一步

1. 阅读 [CLAUDE.md](CLAUDE.md) 了解完整项目架构
2. 查看模块文档了解各模块详细信息
3. 运行示例代码：`python examples/quickstart.py`
4. 开始构建你的第一个爬虫！

---

**需要帮助？** 查看 [FAQ](CLAUDE.md#常见问题-faq) 或提交 Issue。
