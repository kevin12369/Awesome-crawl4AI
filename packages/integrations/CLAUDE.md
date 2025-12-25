# Integrations 模块

[根目录](../../CLAUDE.md) > [packages](../) > **integrations**

---

## 模块职责

Integrations 模块提供与第三方服务和平台的集成能力，扩展爬虫的功能和应用场景。

### 核心功能

- **存储集成**：数据库、对象存储
- **AI 服务**：OpenAI、Anthropic、Cohere
- **消息队列**：Redis、RabbitMQ、Kafka
- **监控告警**：Sentry、DataDog、Prometheus
- **CI/CD**：GitHub Actions、GitLab CI
- **搜索引擎**：Elasticsearch、Meilisearch

## 入口和启动

### 文件结构

```
integrations/
├── __init__.py              # 包入口
├── storage/                 # 存储集成
│   ├── __init__.py
│   ├── base.py
│   ├── postgresql.py
│   ├── mongodb.py
│   ├── sqlite.py
│   └── s3.py
├── ai_services/             # AI 服务集成
│   ├── __init__.py
│   ├── openai.py
│   ├── anthropic.py
│   └── cohere.py
├── queues/                  # 消息队列
│   ├── __init__.py
│   ├── redis.py
│   └── rabbitmq.py
└── monitoring/              # 监控集成
    ├── __init__.py
    ├── sentry.py
    └── prometheus.py
```

### 核心类设计

```python
class BaseIntegration:
    """集成基类"""

    def __init__(self, config: Dict[str, Any]):
        """初始化集成"""

    async def connect(self):
        """建立连接"""

    async def disconnect(self):
        """断开连接"""

    async def health_check(self) -> bool:
        """健康检查"""
```

## 外部接口

### PostgreSQL 存储

```python
from crawl4ai.integrations.storage import PostgreSQLStorage

storage = PostgreSQLStorage(
    host="localhost",
    port=5432,
    database="crawl4ai",
    user="user",
    password="password"
)

await storage.connect()
await storage.save_result(crawl_result)
results = await storage.query(url="https://example.com")
```

### MongoDB 存储

```python
from crawl4ai.integrations.storage import MongoDBStorage

storage = MongoDBStorage(
    connection_string="mongodb://localhost:27017/",
    database="crawl4ai"
)

await storage.connect()
await storage.save_result(crawl_result)
```

### OpenAI 集成

```python
from crawl4ai.integrations.ai_services import OpenAIIntegration

ai = OpenAIIntegration(api_key="your-api-key")
summary = await ai.summarize(text)
embeddings = await ai.get_embeddings([text1, text2])
```

### Redis 队列

```python
from crawl4ai.integrations.queues import RedisQueue

queue = RedisQueue(host="localhost", port=6379)
await queue.enqueue_urls(url_list)
url = await queue.dequeue_url()
```

### Sentry 监控

```python
from crawl4ai.integrations.monitoring import SentryIntegration

sentry = SentryIntegration(dsn="your-sentry-dsn")
sentry.setup()
# 错误会自动报告到 Sentry
```

## 关键依赖和配置

### 可选依赖项

```toml
[project.optional-dependencies]
postgresql = ["asyncpg>=0.29.0"]
mongodb = ["motor>=3.3.0"]
redis = ["redis>=5.0.0"]
s3 = ["boto3>=1.34.0"]
openai = ["openai>=1.0.0"]
sentry = ["sentry-sdk>=1.39.0"]
```

### 配置示例

```python
from crawl4ai.integrations import IntegrationConfig

config = IntegrationConfig(
    # 存储
    storage_type="postgresql",
    postgresql_config={
        "host": "localhost",
        "port": 5432,
        "database": "crawl4ai"
    },

    # AI 服务
    openai_api_key="sk-...",
    openai_model="gpt-4",

    # 队列
    queue_type="redis",
    redis_config={"host": "localhost", "port": 6379},

    # 监控
    sentry_dsn="https://...",
    enable_monitoring=True
)
```

## 数据模型

### StorageAdapter

```python
class StorageAdapter(ABC):
    """存储适配器基类"""

    @abstractmethod
    async def save_result(self, result: CrawlResult) -> str:
        """保存爬取结果，返回 ID"""

    @abstractmethod
    async def get_result(self, id: str) -> Optional[CrawlResult]:
        """获取结果"""

    @abstractmethod
    async def query(self, **filters) -> List[CrawlResult]:
        """查询结果"""
```

### AIIntegration

```python
class AIIntegration(ABC):
    """AI 集成基类"""

    @abstractmethod
    async def summarize(self, text: str, **kwargs) -> str:
        """文本摘要"""

    @abstractmethod
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """获取文本嵌入"""
```

## 测试和质量

### 测试结构

```
tests/unit/integrations/
├── storage/
│   ├── test_postgresql.py
│   ├── test_mongodb.py
│   └── test_sqlite.py
├── ai_services/
│   ├── test_openai.py
│   └── test_anthropic.py
├── queues/
│   └── test_redis.py
└── monitoring/
    └── test_sentry.py
```

### 测试策略

- 使用 mock 或测试容器进行集成测试
- 测试连接和重连逻辑
- 验证数据序列化和反序列化
- 检查错误处理和降级

## 常见问题 (FAQ)

### Q1: 如何同时使用多个存储后端？
**A:** 可以组合多个存储适配器：
```python
postgres = PostgreSQLStorage(...)
s3 = S3Storage(...)

# 同时保存到多个后端
await postgres.save_result(result)
await s3.save_result(result)
```

### Q2: AI 集成需要 API 密钥吗？
**A:** 是的，需要相应的 API 密钥。建议通过环境变量配置：
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Q3: 如何处理集成服务的故障？
**A:** 所有集成都有降级策略：
```python
storage = PostgreSQLStorage(..., fallback=None)
# 如果连接失败，会优雅降级而不是抛出异常
```

### Q4: 支持哪些云存储服务？
**A:** 支持 AWS S3、Google Cloud Storage、Azure Blob Storage，通过统一的 S3 兼容接口。

## 相关文件列表

### 核心文件
- `packages/integrations/__init__.py`
- `packages/integrations/storage/base.py`
- `packages/integrations/storage/postgresql.py`
- `packages/integrations/storage/mongodb.py`
- `packages/integrations/ai_services/openai.py`
- `packages/integrations/queues/redis.py`
- `packages/integrations/monitoring/sentry.py`

### 测试文件
- `tests/integrations/test_storage.py`
- `tests/integrations/test_ai_services.py`
- `tests/integrations/test_queues.py`

## 更改日志 (Change Log)

### 2025-12-25
- 初始化集成模块设计
- 定义存储、AI、队列集成接口
- 规划监控和告警功能
