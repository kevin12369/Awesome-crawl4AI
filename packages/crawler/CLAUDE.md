# Crawler 模块

[根目录](../../CLAUDE.md) > [packages](../) > **crawler**

---

## 模块职责

Crawler 模块是 Awesome-crawl4AI 的核心引擎，负责网页爬取的主要逻辑。它提供了高性能、可扩展的爬取能力，支持并发、重试、代理等企业级特性。

### 核心功能

- **请求调度**：智能的请求队列和调度器
- **并发控制**：异步并发爬取，支持大规模任务
- **错误处理**：自动重试、异常捕获、降级策略
- **速率限制**：尊重网站规则，避免被封禁
- **代理管理**：支持代理池和轮换策略
- **中间件系统**：可插拔的请求/响应处理

## 入口和启动

### 主要入口文件

```
crawler/
├── __init__.py           # 包入口，导出公共接口
├── core.py               # 核心爬虫类
├── scheduler.py          # 任务调度器
├── middleware.py         # 中间件基类和内置中间件
└── config.py             # 配置管理
```

### 核心类设计

```python
# packages/crawler/core.py
class WebCrawler:
    """主要的爬虫类"""

    def __init__(self, config: CrawlerConfig):
        """初始化爬虫"""

    async def crawl(self, url: str, **kwargs) -> CrawlResult:
        """爬取单个页面"""

    async def crawl_batch(self, urls: List[str], **kwargs) -> List[CrawlResult]:
        """批量爬取多个页面"""

    def crawl_sync(self, url: str, **kwargs) -> CrawlResult:
        """同步爬取接口"""
```

## 外部接口

### 公共 API

```python
from crawl4ai import WebCrawler

# 基础使用
crawler = WebCrawler()
result = await crawler.crawl("https://example.com")

# 带配置
from crawl4ai.crawler import CrawlerConfig

config = CrawlerConfig(
    max_concurrent=10,
    timeout=30,
    retries=3
)
crawler = WebCrawler(config)
```

### 中间件接口

```python
from crawl4ai.crawler import Middleware

class CustomMiddleware(Middleware):
    async def process_request(self, request):
        # 修改请求
        request.headers['X-Custom'] = 'value'
        return request

    async def process_response(self, response):
        # 处理响应
        return response
```

## 关键依赖和配置

### 依赖项

- **httpx/aiohttp**：异步 HTTP 客户端
- **tenacity**：重试逻辑
- **pydantic**：配置验证
- **redis**（可选）：任务队列和缓存

### 配置参数

```python
class CrawlerConfig(BaseModel):
    # 并发控制
    max_concurrent: int = 10
    max_retries: int = 3
    timeout: int = 30

    # 速率限制
    rate_limit: int = 5  # 每秒请求数
    delay_range: tuple = (1, 3)

    # 代理
    use_proxy: bool = False
    proxy_pool: Optional[str] = None

    # 中间件
    middlewares: List[Middleware] = []

    # User-Agent
    user_agent: str = "Awesome-crawl4AI/0.1.0"
```

## 数据模型

### CrawlResult

```python
class CrawlResult(BaseModel):
    """爬取结果"""

    url: str                          # 目标 URL
    status_code: int                  # HTTP 状态码
    success: bool                     # 是否成功
    content: str                      # HTML 内容
    text: str                         # 提取的文本
    metadata: Dict[str, Any]          # 元数据
    error: Optional[str] = None       # 错误信息
    crawl_time: float = 0.0           # 爬取耗时
```

### CrawlRequest

```python
class CrawlRequest(BaseModel):
    """爬取请求"""

    url: str
    method: str = "GET"
    headers: Dict[str, str] = {}
    params: Dict[str, Any] = {}
    data: Optional[Dict[str, Any]] = None
    proxy: Optional[str] = None
    timeout: int = 30
    callback: Optional[str] = None
```

## 测试和质量

### 测试结构

```
tests/unit/crawler/
├── test_core.py           # 核心功能测试
├── test_scheduler.py      # 调度器测试
├── test_middleware.py     # 中间件测试
└── fixtures/              # 测试固件
    ├── mock_responses.py
    └── test_pages.html
```

### 测试覆盖重点

- [ ] 异步爬取功能
- [ ] 并发控制
- [ ] 错误重试机制
- [ ] 代理轮换
- [ ] 速率限制
- [ ] 中间件处理流程
- [ ] 配置验证

### 性能指标

- 单次请求延迟：< 100ms（本地测试）
- 并发 100 请求吞吐量：> 50 req/s
- 内存占用：< 500MB（1000 并发）

## 常见问题 (FAQ)

### Q1: 如何处理动态 JavaScript 网站？
**A:** 可以配置使用 Playwright 或 Selenium 渲染引擎。示例：
```python
config = CrawlerConfig(use_playwright=True, page_load_timeout=5000)
crawler = WebCrawler(config)
```

### Q2: 如何避免被封禁？
**A:** 建议使用以下策略组合：
- 设置合理的速率限制（rate_limit）
- 使用代理池轮换（proxy_pool）
- 随机化请求延迟（delay_range）
- 轮换 User-Agent
- 管理 Cookie 和会话

### Q3: 如何监控爬取进度？
**A:** 可以使用回调函数或事件系统：
```python
def on_progress(current, total):
    print(f"Progress: {current}/{total}")

crawler.crawl_batch(urls, on_progress=on_progress)
```

### Q4: 支持哪些认证方式？
**A:** 支持 Basic Auth、Bearer Token、Cookie 认证、自定义 Header 认证等。

## 相关文件列表

### 核心文件
- `packages/crawler/__init__.py` - 包入口
- `packages/crawler/core.py` - 核心爬虫实现
- `packages/crawler/scheduler.py` - 任务调度器
- `packages/crawler/middleware.py` - 中间件系统
- `packages/crawler/config.py` - 配置管理
- `packages/crawler/proxy.py` - 代理管理
- `packages/crawler/retry.py` - 重试策略

### 测试文件
- `tests/unit/crawler/test_core.py`
- `tests/unit/crawler/test_scheduler.py`
- `tests/unit/crawler/test_middleware.py`
- `tests/integration/test_crawler_integration.py`

## 更改日志 (Change Log)

### 2025-12-25
- 初始化模块设计文档
- 定义核心接口和数据模型
- 规划测试策略
