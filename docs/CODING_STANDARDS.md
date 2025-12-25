# Awesome-crawl4AI 编码规范

> 项目代码风格与最佳实践指南

## 目录

- [1. 代码风格](#1-代码风格)
- [2. Python 特定规范](#2-python-特定规范)
- [3. 代码组织](#3-代码组织)
- [4. 代码质量工具](#4-代码质量工具)
- [5. 示例代码](#5-示例代码)
- [6. 检查清单](#6-检查清单)

---

## 1. 代码风格

### 1.1 基本规范

遵循 **PEP 8** 标准，使用以下配置：

- **行长度**: 100 字符（配置见 `pyproject.toml`）
- **缩进**: 4 空格
- **编码**: UTF-8
- **换行**: Unix 风格（LF）

### 1.2 导入顺序

严格遵循以下导入顺序，使用空行分隔：

```python
# 1. 标准库导入
import asyncio
from pathlib import Path
from typing import Dict, List, Optional

# 2. 第三方库导入
import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel

# 3. 本地模块导入
from crawl4ai.crawler import WebCrawler
from crawl4ai.extractors.base import BaseExtractor
```

### 1.3 命名约定

#### 类名（PascalCase）

```python
# ✅ 好的示例
class WebCrawler:
    pass

class AsyncWebCrawler:
    pass

# ❌ 坏的示例
class web_crawler:
    pass

class Webcrawler:
    pass
```

#### 函数和变量（snake_case）

```python
# ✅ 好的示例
def crawl_url(url: str) -> str:
    pass

max_retries = 3
current_page = 1

# ❌ 坏的示例
def CrawlUrl(url):
    pass

maxRetries = 3
CurrentPage = 1
```

#### 常量（UPPER_SNAKE_CASE）

```python
# ✅ 好的示例
DEFAULT_TIMEOUT = 30
MAX_RETRY_COUNT = 3
USER_AGENT = "Mozilla/5.0 ..."

# ❌ 坏的示例
default_timeout = 30
MaxRetryCount = 3
```

#### 私有成员（单下划线前缀）

```python
# ✅ 好的示例
class WebCrawler:
    def __init__(self):
        self._session: Optional[httpx.AsyncClient] = None
        self._cache: Dict[str, str] = {}

    def _validate_url(self, url: str) -> bool:
        """私有方法：验证 URL 格式"""
        return True

# ❌ 坏的示例
class WebCrawler:
    def __init__(self):
        self.session = None  # 应该使用私有成员
```

#### 受保护成员（双下划线前缀，不常用）

```python
class BaseExtractor:
    def __init__(self):
        self.__config: Dict[str, Any] = {}  # 名字修饰
```

### 1.4 类型注解

**强制要求**：所有公共 API 必须有类型注解

```python
# ✅ 好的示例
from typing import List, Optional, Dict, Any

async def fetch_page(
    url: str,
    timeout: int = 30,
    headers: Optional[Dict[str, str]] = None
) -> str:
    """获取网页内容

    Args:
        url: 目标 URL
        timeout: 超时时间（秒）
        headers: 自定义请求头

    Returns:
        网页 HTML 内容

    Raises:
        TimeoutError: 请求超时
        httpx.HTTPError: HTTP 请求错误
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=timeout, headers=headers)
        return response.text

# ❌ 坏的示例
async def fetch_page(url, timeout=30, headers=None):
    """缺少类型注解，难以理解和维护"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=timeout, headers=headers)
        return response.text
```

#### 复杂类型使用 `typing` 模块

```python
from typing import List, Dict, Optional, Union, Tuple, AsyncIterator

# 列表
def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

# 字典
def get_config() -> Dict[str, Union[str, int, bool]]:
    return {"timeout": 30, "enabled": True, "mode": "fast"}

# 可选类型
def find_user(user_id: int) -> Optional[Dict[str, Any]]:
    return None if user_id < 0 else {"id": user_id, "name": "test"}

# 元组
def get_coordinates() -> Tuple[float, float]:
    return 39.9042, 116.4074

# 异步迭代器
async def stream_pages(urls: List[str]) -> AsyncIterator[str]:
    for url in urls:
        yield await fetch_page(url)
```

#### 使用 `TypeAlias` 提高可读性

```python
from typing import TypeAlias, Dict, List, Optional

# 定义类型别名
JSON: TypeAlias = Dict[str, Any]
URL: TypeAlias = str
Headers: TypeAlias = Dict[str, str]
ExtractedData: TypeAlias = Dict[str, Optional[Union[str, List[str]]]]

def process_result(data: JSON) -> ExtractedData:
    """类型别名使签名更清晰"""
    return {
        "title": data.get("title"),
        "content": data.get("content", []).split("\n")
    }
```

### 1.5 文档字符串

使用 **Google 风格**的文档字符串：

```python
# ✅ 好的示例
def extract_content(
    html: str,
    selector: str,
    clean_html: bool = True
) -> Dict[str, Any]:
    """从 HTML 中提取内容

    这个函数使用 CSS 选择器从 HTML 中提取指定内容，
    并可选择性地清理 HTML 标签。

    Args:
        html: 原始 HTML 字符串
        selector: CSS 选择器
        clean_html: 是否清理 HTML 标签，默认为 True

    Returns:
        包含提取结果的字典，结构为：
        {
            "text": str,           # 提取的文本
            "html": str,           # 原始 HTML
            "metadata": dict       # 元数据
        }

    Raises:
        ValueError: 选择器无效
        ParserError: HTML 解析失败

    Examples:
        >>> html = "<div class='content'>Hello</div>"
        >>> result = extract_content(html, ".content")
        >>> print(result["text"])
        'Hello'
    """
    soup = BeautifulSoup(html, "lxml")
    elements = soup.select(selector)
    if not elements:
        raise ValueError(f"未找到匹配选择器的元素: {selector}")
    # ...
    return {"text": "", "html": "", "metadata": {}}

# ❌ 坏的示例
def extract_content(html, selector, clean_html=True):
    """提取内容

    参数:
        html: html
        selector: selector
        clean_html: clean

    返回:
        dict
    """
    # 缺少详细说明、类型信息、异常说明
```

#### 类文档字符串

```python
class AsyncWebCrawler:
    """异步网页爬虫

    提供高性能的异步网页爬取功能，支持并发请求、自动重试、
    代理切换等特性。

    Attributes:
        max_concurrent: 最大并发数
        timeout: 默认超时时间
        session: httpx 异步会话

    Examples:
        >>> crawler = AsyncWebCrawler(max_concurrent=10)
        >>> result = await crawler.crawl("https://example.com")
        >>> print(result.status)
        200
    """

    def __init__(self, max_concurrent: int = 5, timeout: int = 30):
        """初始化爬虫实例

        Args:
            max_concurrent: 最大并发请求数
            timeout: 请求超时时间（秒）
        """
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self._session: Optional[httpx.AsyncClient] = None
```

---

## 2. Python 特定规范

### 2.1 异步代码最佳实践

#### async/await 使用规范

```python
# ✅ 好的示例
import asyncio
from typing import List, Optional
import httpx

async def fetch_single_page(url: str, client: httpx.AsyncClient) -> str:
    """获取单个页面

    Args:
        url: 目标 URL
        client: httpx 异步客户端

    Returns:
        页面内容
    """
    response = await client.get(url, timeout=30.0)
    response.raise_for_status()
    return response.text

async def fetch_multiple_pages(urls: List[str]) -> Dict[str, str]:
    """并发获取多个页面

    使用 asyncio.gather 实现并发请求，提高效率。

    Args:
        urls: URL 列表

    Returns:
        URL 到内容的映射字典
    """
    async with httpx.AsyncClient() as client:
        tasks = [fetch_single_page(url, client) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            url: result if not isinstance(result, Exception) else ""
            for url, result in zip(urls, results)
        }

# ❌ 坏的示例 - 串行执行，效率低
async def fetch_multiple_pages_bad(urls: List[str]) -> Dict[str, str]:
    """不推荐：串行请求，性能差"""
    results = {}
    async with httpx.AsyncClient() as client:
        for url in urls:
            try:
                results[url] = await client.get(url)
            except Exception as e:
                results[url] = str(e)
    return results
```

#### 异步上下文管理器

```python
# ✅ 好的示例 - 使用异步上下文管理器
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed_session(headers: Dict[str, str]):
    """管理 httpx 会话的生命周期

    Args:
        headers: 请求头

    Yields:
        httpx.AsyncClient 实例
    """
    client = httpx.AsyncClient(headers=headers)
    try:
        yield client
    finally:
        await client.aclose()

# 使用示例
async def main():
    async with managed_session({"User-Agent": "Crawler"}) as client:
        response = await client.get("https://example.com")
        return response.text

# ❌ 坏的示例 - 忘记关闭会话
async def bad_example():
    client = httpx.AsyncClient()
    response = await client.get("https://example.com")
    return response.text
    # 警告：会话未正确关闭！
```

#### 信号量控制并发

```python
# ✅ 好的示例 - 使用信号量控制并发
import asyncio

class AsyncCrawler:
    """带并发控制的异步爬虫"""

    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def crawl(self, url: str) -> str:
        """爬取单个 URL

        使用信号量限制并发数，防止资源耗尽。
        """
        async with self._semaphore:
            # 信号量确保最多 max_concurrent 个协程同时执行
            return await self._fetch(url)

    async def _fetch(self, url: str) -> str:
        """实际的获取逻辑"""
        # 实现略
        pass
```

#### 异常处理

```python
# ✅ 好的示例 - 完善的异常处理
import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def robust_fetch(
    url: str,
    max_retries: int = 3,
    timeout: float = 30.0
) -> Optional[str]:
    """健壮的异步请求函数

    Args:
        url: 目标 URL
        max_retries: 最大重试次数
        timeout: 超时时间

    Returns:
        成功返回内容，失败返回 None
    """
    last_error = None

    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=timeout)
                response.raise_for_status()
                return response.text

        except httpx.TimeoutException as e:
            last_error = e
            logger.warning(f"超时（尝试 {attempt + 1}/{max_retries}）: {url}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避

        except httpx.HTTPStatusError as e:
            last_error = e
            logger.error(f"HTTP 错误: {e.response.status_code} - {url}")
            # 4xx 错误不重试
            if 400 <= e.response.status_code < 500:
                break
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)

        except Exception as e:
            last_error = e
            logger.error(f"未知错误: {e}")
            break

    logger.error(f"请求失败: {url} - {last_error}")
    return None

# ❌ 坏的示例 - 缺少异常处理
async def bad_fetch(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
    # 没有处理超时、网络错误、HTTP 错误等
```

### 2.2 上下文管理器使用

#### 资源管理

```python
# ✅ 好的示例 - 使用上下文管理器确保资源释放
class FileProcessor:
    """文件处理器示例"""

    def process_file(self, file_path: Path) -> List[str]:
        """处理文件，确保文件句柄正确关闭

        Args:
            file_path: 文件路径

        Returns:
            处理后的行列表
        """
        # 上下文管理器自动关闭文件
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def process_multiple_files(self, paths: List[Path]) -> Dict[str, List[str]]:
        """处理多个文件

        使用嵌套上下文管理器处理多个文件。
        """
        results = {}
        for path in paths:
            try:
                results[str(path)] = self.process_file(path)
            except IOError as e:
                logger.error(f"文件处理失败: {path} - {e}")
                results[str(path)] = []
        return results

# ❌ 坏的示例 - 未使用上下文管理器
def bad_process_file(file_path: Path) -> List[str]:
    f = open(file_path, "r", encoding="utf-8")
    lines = f.readlines()
    # 如果这里抛出异常，文件不会被关闭！
    return [line.strip() for line in lines]
```

#### 自定义上下文管理器

```python
# ✅ 好的示例 - 自定义上下文管理器
from contextlib import contextmanager
import time

@contextmanager
def timer(operation_name: str):
    """计时上下文管理器

    Args:
        operation_name: 操作名称

    Yields:
        None
    """
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        logger.info(f"{operation_name} 耗时: {elapsed:.2f} 秒")

# 使用示例
def process_data():
    with timer("数据提取"):
        data = extract_data()
    # 输出: "数据提取 耗时: 1.23 秒"
```

### 2.3 异常处理策略

#### 异常捕获原则

```python
# ✅ 好的示例 - 精确捕获异常
from httpx import TimeoutException, HTTPStatusError, NetworkError

async def safe_request(url: str) -> Optional[str]:
    """安全的请求函数

    只捕获预期的异常，让其他异常传播。
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.text

    except TimeoutException:
        logger.warning(f"请求超时: {url}")
        return None

    except HTTPStatusError as e:
        logger.error(f"HTTP 错误 {e.response.status_code}: {url}")
        return None

    except NetworkError as e:
        logger.error(f"网络错误: {e}")
        return None

    # 其他异常（如 KeyboardInterrupt）会正常传播

# ❌ 坏的示例 - 过于宽泛的异常捕获
async def unsafe_request(url: str) -> Optional[str]:
    try:
        async with httpx.AsyncClient() as client:
            return await client.get(url)
    except Exception:
        # 问题：捕获了所有异常，包括 KeyboardInterrupt
        return None
```

#### 自定义异常

```python
# ✅ 好的示例 - 定义清晰的异常层次结构
class CrawlerError(Exception):
    """爬虫基础异常"""

class ConfigurationError(CrawlerError):
    """配置错误"""

class ExtractionError(CrawlerError):
    """数据提取错误"""

class FetchError(CrawlerError):
    """网页获取错误"""

    def __init__(self, url: str, status_code: int, message: str):
        self.url = url
        self.status_code = status_code
        super().__init__(f"{url} 返回 {status_code}: {message}")

# 使用自定义异常
def fetch_page(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 404:
        raise FetchError(url, 404, "页面未找到")
    if response.status_code >= 400:
        raise FetchError(url, response.status_code, "请求失败")
    return response.text
```

#### 异常链（Exception Chaining）

```python
# ✅ 好的示例 - 使用 raise ... from 保留异常链
def process_html(html: str) -> Dict[str, Any]:
    """处理 HTML，保留原始异常信息"""
    try:
        soup = BeautifulSoup(html, "lxml")
        content = soup.find("div", class_="content")
        if not content:
            raise ValueError("未找到内容区域")
        return {"text": content.get_text(strip=True)}

    except Exception as e:
        # 使用 from 保留原始异常
        raise ExtractionError("HTML 处理失败") from e

# ❌ 坏的示例 - 丢失原始异常
def process_html_bad(html: str) -> Dict[str, Any]:
    try:
        soup = BeautifulSoup(html, "lxml")
        # ...
    except Exception:
        # 丢失了原始异常信息，难以调试
        raise ExtractionError("HTML 处理失败")
```

### 2.4 资源管理

#### 网络连接管理

```python
# ✅ 好的示例 - 复用连接池
class HttpClient:
    """HTTP 客户端封装"""

    def __init__(self, max_connections: int = 100):
        self.max_connections = max_connections
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """进入上下文时创建连接池"""
        limits = httpx.Limits(max_connections=self.max_connections)
        self._client = httpx.AsyncClient(limits=limits)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时关闭连接池"""
        if self._client:
            await self._client.aclose()

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """发送 GET 请求"""
        if not self._client:
            raise RuntimeError("客户端未初始化")
        return await self._client.get(url, **kwargs)

# 使用示例
async def main():
    async with HttpClient(max_connections=50) as client:
        # 复用同一个连接池
        response1 = await client.get("https://example.com")
        response2 = await client.get("https://example.org")

# ❌ 坏的示例 - 每次请求创建新连接
async def bad_request(url: str) -> str:
    # 每次都创建新连接，效率低
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.text
```

#### 文件和内存管理

```python
# ✅ 好的示例 - 使用生成器处理大数据
def process_large_file(file_path: Path) -> Iterator[Dict[str, Any]]:
    """逐行处理大文件，避免内存溢出

    Args:
        file_path: 大文件路径

    Yields:
        处理后的数据项
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                yield process_item(data)
            except json.JSONDecodeError as e:
                logger.warning(f"跳过无效行: {e}")
                continue

# ❌ 坏的示例 - 一次性加载大文件
def bad_process_large_file(file_path: Path) -> List[Dict[str, Any]]:
    # 将整个文件加载到内存，可能导致内存溢出
    with open(file_path, "r", encoding="utf-8") as f:
        all_lines = f.readlines()
    return [process_item(json.loads(line)) for line in all_lines]
```

---

## 3. 代码组织

### 3.1 文件和目录结构

#### 推荐的项目结构

```
packages/
├── crawler/                  # 核心爬虫模块
│   ├── __init__.py          # 模块导出
│   ├── base.py              # 基础类和抽象接口
│   ├── async_crawler.py     # 异步爬虫实现
│   ├── sync_crawler.py      # 同步爬虫实现
│   ├── config.py            # 配置类
│   └── utils.py             # 工具函数
├── extractors/              # 数据提取器
│   ├── __init__.py
│   ├── base.py              # 基础提取器
│   ├── css_extractor.py     # CSS 选择器提取
│   ├── xpath_extractor.py   # XPath 提取
│   └── ai_extractor.py      # AI 智能提取
├── processors/              # 数据处理器
│   ├── __init__.py
│   ├── cleaner.py           # 数据清洗
│   ├── formatter.py         # 格式化输出
│   └── validator.py         # 数据验证
└── utils/                   # 公共工具
    ├── __init__.py
    ├── http_utils.py        # HTTP 工具
    ├── parser_utils.py      # 解析工具
    └── retry.py             # 重试逻辑
```

#### 模块组织原则

```python
# ✅ 好的示例 - 清晰的模块职责
# packages/crawler/base.py
"""基础爬虫类和抽象接口

这个模块定义了所有爬虫类的抽象基类和接口规范。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseCrawler(ABC):
    """爬虫抽象基类

    定义了所有爬虫必须实现的核心接口。
    """

    @abstractmethod
    async def crawl(self, url: str, **kwargs) -> Dict[str, Any]:
        """爬取指定 URL

        Args:
            url: 目标 URL
            **kwargs: 额外参数

        Returns:
            爬取结果字典
        """
        pass

# packages/crawler/async_crawler.py
"""异步爬虫实现

这个模块提供了高性能的异步爬虫实现。
"""

from .base import BaseCrawler

class AsyncWebCrawler(BaseCrawler):
    """异步网页爬虫实现"""

    async def crawl(self, url: str, **kwargs) -> Dict[str, Any]:
        # 实现略
        pass

# packages/crawler/__init__.py
"""爬虫模块导出

从这里导出公共 API，隐藏内部实现。
"""

from .base import BaseCrawler
from .async_crawler import AsyncWebCrawler
from .sync_crawler import SyncWebCrawler

__all__ = [
    "BaseCrawler",
    "AsyncWebCrawler",
    "SyncWebCrawler",
]

# ❌ 坏的示例 - 职责不清
# packages/crawler/everything.py
"""所有东西混在一起"""
# 包含了爬虫、提取器、处理器、工具函数等
# 违反单一职责原则
```

### 3.2 导入顺序和分组

#### 严格遵循导入顺序

```python
# ✅ 好的示例 - 标准导入顺序
# 1. 标准库导入（按字母顺序）
import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

# 2. 第三方库导入（按字母顺序）
import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel

# 3. 本地模块导入（按字母顺序）
from crawl4ai.crawler.base import BaseCrawler
from crawl4ai.extractors.css import CSSExtractor
from crawl4ai.utils.http import get_headers

# 使用类型检查时，可以导入类型专用模块
if TYPE_CHECKING:
    from mypy_modules import SomeType

# ❌ 坏的示例 - 导入混乱
from crawl4ai.crawler.base import BaseCrawler  # 本地
import httpx  # 第三方
import asyncio  # 标准库
from typing import Dict
from bs4 import BeautifulSoup  # 第三方
```

#### 避免循环导入

```python
# ✅ 好的示例 - 使用 TYPE_CHECKING 避免循环导入
# crawler/__init__.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from extractors.base import BaseExtractor

class WebCrawler:
    def __init__(self, extractor: Optional["BaseExtractor"] = None):
        # TYPE_CHECKING 确保类型注解可用，但运行时不导入
        self.extractor = extractor

# ✅ 或者使用延迟导入
def process_data(data: Dict[str, Any]) -> str:
    """延迟导入避免循环依赖"""
    from crawl4ai.processors.formatter import format_data
    return format_data(data)

# ❌ 坏的示例 - 直接导入导致循环依赖
# crawler/__init__.py
from extractors.base import BaseExtractor  # 可能导致循环导入

# extractors/base.py
from crawler import WebCrawler  # 循环依赖！
```

### 3.3 类和方法组织

#### 类成员排序

```python
# ✅ 好的示例 - 标准类成员顺序
class WebCrawler:
    """网页爬虫类

    类成员按以下顺序组织：
    1. 类变量和常量
    2. 特殊方法（__init__, __repr__ 等）
    3. 属性（@property）
    4. 公共方法
    5. 受保护方法（_ 前缀）
    6. 私有方法（__ 前缀）
    """

    # 1. 类变量和常量
    DEFAULT_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    VERSION: str = "1.0.0"

    # 2. 特殊方法
    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        """初始化爬虫实例"""
        self.timeout = timeout
        self._session: Optional[httpx.AsyncClient] = None
        self._cache: Dict[str, str] = {}

    def __repr__(self) -> str:
        """对象表示"""
        return f"WebCrawler(timeout={self.timeout})"

    def __enter__(self):
        """进入上下文"""
        self._session = httpx.AsyncClient()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        if self._session:
            self._session.close()

    # 3. 属性
    @property
    def is_connected(self) -> bool:
        """是否已连接"""
        return self._session is not None

    # 4. 公共方法
    async def crawl(self, url: str) -> Dict[str, Any]:
        """爬取网页"""
        await self._ensure_session()
        return await self._fetch(url)

    async def crawl_batch(self, urls: List[str]) -> List[Dict[str, Any]]:
        """批量爬取"""
        results = []
        for url in urls:
            result = await self.crawl(url)
            results.append(result)
        return results

    # 5. 受保护方法
    async def _ensure_session(self) -> None:
        """确保会话已创建"""
        if not self._session:
            self._session = httpx.AsyncClient()

    async def _fetch(self, url: str) -> Dict[str, Any]:
        """获取网页内容"""
        response = await self._session.get(url, timeout=self.timeout)
        return {"url": url, "content": response.text}

    # 6. 私有方法
    def __validate_url(self, url: str) -> bool:
        """验证 URL 格式（私有）"""
        return url.startswith(("http://", "https://"))

# ❌ 坏的示例 - 成员顺序混乱
class BadWebCrawler:
    def _fetch(self, url: str):
        pass  # 私有方法在最前面

    DEFAULT_TIMEOUT = 30  # 类变量在方法后面

    def __init__(self):
        pass

    @property
    def is_connected(self):
        pass  # 属性在公共方法后面

    async def crawl(self, url: str):
        pass
```

#### 方法长度控制

```python
# ✅ 好的示例 - 拆分长方法
class DataExtractor:
    """数据提取器"""

    def extract_article(self, html: str) -> Dict[str, Any]:
        """提取文章数据

        将复杂逻辑拆分为多个小方法，提高可读性和可测试性。
        """
        soup = BeautifulSoup(html, "lxml")

        title = self._extract_title(soup)
        content = self._extract_content(soup)
        metadata = self._extract_metadata(soup)

        return {
            "title": title,
            "content": content,
            "metadata": metadata
        }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取标题"""
        title_tag = soup.find("h1", class_="article-title")
        return title_tag.get_text(strip=True) if title_tag else ""

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """提取正文"""
        content_tag = soup.find("div", class_="article-content")
        return content_tag.get_text(strip=True) if content_tag else ""

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """提取元数据"""
        return {
            "author": self._get_meta(soup, "author"),
            "date": self._get_meta(soup, "date"),
            "tags": self._get_tags(soup)
        }

    def _get_meta(self, soup: BeautifulSoup, name: str) -> str:
        """获取单个元数据"""
        meta_tag = soup.find("meta", attrs={"name": name})
        return meta_tag.get("content", "") if meta_tag else ""

    def _get_tags(self, soup: BeautifulSoup) -> List[str]:
        """获取标签"""
        tag_tags = soup.find_all("a", class_="tag")
        return [tag.get_text(strip=True) for tag in tag_tags]

# ❌ 坏的示例 - 过长的方法
class BadDataExtractor:
    def extract_article(self, html: str) -> Dict[str, Any]:
        # 一个方法包含所有逻辑，难以理解和测试
        soup = BeautifulSoup(html, "lxml")
        title_tag = soup.find("h1", class_="article-title")
        title = title_tag.get_text(strip=True) if title_tag else ""
        content_tag = soup.find("div", class_="article-content")
        content = content_tag.get_text(strip=True) if content_tag else ""
        meta_author = soup.find("meta", attrs={"name": "author"})
        author = meta_author.get("content", "") if meta_author else ""
        # ... 更多代码，总行数超过 100 行
        return {"title": title, "content": content, "author": author}
```

### 3.4 模块级变量和常量

#### 常量定义

```python
# ✅ 好的示例 - 集中管理常量
# packages/crawler/constants.py
"""爬虫模块常量定义"""

# HTTP 相关
DEFAULT_TIMEOUT: int = 30
MAX_RETRIES: int = 3
DEFAULT_USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# 并发控制
DEFAULT_MAX_CONCURRENT: int = 10
MIN_CONCURRENT: int = 1
MAX_CONCURRENT: int = 100

# 重试策略
RETRY_BACKOFF_FACTOR: float = 0.5
RETRY_STATUS_CODES = {500, 502, 503, 504}

# 输出格式
SUPPORTED_OUTPUT_FORMATS = {"text", "html", "markdown", "json"}

# 使用示例
from crawl4ai.crawler.constants import (
    DEFAULT_TIMEOUT,
    MAX_RETRIES,
    DEFAULT_USER_AGENT
)

# ❌ 坏的示例 - 魔法数字散落在代码中
async def fetch(url: str):
    timeout = 30  # 魔法数字
    retries = 3   # 魔法数字
    backoff = 0.5 # 魔法数字
    # ...
```

#### 配置类

```python
# ✅ 好的示例 - 使用配置类
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class CrawlerConfig:
    """爬虫配置类

    使用类型提示和默认值，提供清晰的配置接口。
    """
    timeout: int = 30
    max_retries: int = 3
    max_concurrent: int = 10
    user_agent: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    proxy: Optional[str] = None

    def __post_init__(self):
        """初始化后处理"""
        if self.user_agent is None:
            self.user_agent = DEFAULT_USER_AGENT
        if self.headers is None:
            self.headers = {"User-Agent": self.user_agent}

# 使用示例
config = CrawlerConfig(
    timeout=60,
    max_retries=5,
    proxy="http://proxy.example.com:8080"
)
crawler = AsyncWebCrawler(config=config)

# ❌ 坏的示例 - 使用字典作为配置
def bad_init_crawler(config: Dict[str, Any]):
    """字典缺少类型检查和文档"""
    timeout = config.get("timeout", 30)
    retries = config.get("max_retries", 3)
    # 无法自动补全，容易拼写错误
```

---

## 4. 代码质量工具

### 4.1 Black 代码格式化

#### 安装和配置

```bash
# 安装
pip install black

# 配置（已在 pyproject.toml 中）
[tool.black]
line-length = 100
target-version = ["py39", "py310", "py311", "py312"]
```

#### 使用示例

```bash
# 格式化单个文件
black crawler/async_crawler.py

# 格式化整个项目
black packages/

# 检查格式但不修改
black --check packages/

# 显示差异
black --diff packages/
```

#### 格式化效果示例

```python
# ❌ 格式化前
def process_data(data:Dict[str,Any],max_items:int=10)->List[str]:
    results=[]
    for item in data['items']:
        if item.get('valid'):
            results.append(item['value'])
    return results[:max_items]

# ✅ 格式化后
def process_data(data: Dict[str, Any], max_items: int = 10) -> List[str]:
    results = []
    for item in data["items"]:
        if item.get("valid"):
            results.append(item["value"])
    return results[:max_items]
```

### 4.2 isort 导入排序

#### 安装和配置

```bash
# 安装
pip install isort

# 配置（已在 pyproject.toml 中）
[tool.isort]
profile = "black"
line_length = 100
```

#### 使用示例

```bash
# 排序导入
isort crawler/async_crawler.py

# 检查导入顺序
isort --check-only crawler/

# 显示差异
isort --diff crawler/
```

#### 排序效果示例

```python
# ❌ 排序前
import asyncio
from typing import Dict
from crawl4ai.crawler import WebCrawler
import httpx
from bs4 import BeautifulSoup
import json

# ✅ 排序后
import asyncio
import json

import httpx
from bs4 import BeautifulSoup
from typing import Dict

from crawl4ai.crawler import WebCrawler
```

### 4.3 Flake8 代码检查

#### 安装和配置

```bash
# 安装
pip install flake8

# 配置（已在 pyproject.toml 中）
[tool.flake8]
max-line-length = 100
extend-ignore = ["E203", "W503"]
```

#### 使用示例

```bash
# 检查文件
flake8 crawler/async_crawler.py

# 检查整个项目
flake8 packages/

# 显示详细错误信息
flake8 --show-source packages/

# 统计错误
flake8 --statistics packages/
```

#### 常见错误和修复

```python
# ❌ E501: 行太长
def very_long_function_name(parameter_one, parameter_two, parameter_three, parameter_four, parameter_five):
    pass

# ✅ 修复：换行
def very_long_function_name(
    parameter_one: str,
    parameter_two: str,
    parameter_three: str,
    parameter_four: str,
    parameter_five: str,
) -> None:
    pass

# ❌ F401: 导入但未使用
import os  # 未使用
import json

# ✅ 修复：删除未使用的导入
import json

# ❌ E225: 操作符周围缺少空格
x=1+2
if x>3:

# ✅ 修复：添加空格
x = 1 + 2
if x > 3:
```

### 4.4 MyPy 类型检查

#### 安装和配置

```bash
# 安装
pip install mypy

# 配置（已在 pyproject.toml 中）
[tool.mypy]
python_version = "3.9"
disallow_untyped_defs = true
```

#### 使用示例

```bash
# 类型检查文件
mypy crawler/async_crawler.py

# 检查整个项目
mypy packages/

# 生成 HTML 报告
mypy --html-report ./mypy-report packages/

# 严格模式
mypy --strict packages/
```

#### 类型错误示例

```python
# ❌ 缺少类型注解
def add(a, b):
    return a + b

# ✅ 添加类型注解
def add(a: int, b: int) -> int:
    return a + b

# ❌ 类型不匹配
def process(items: List[str]) -> int:
    return items  # 错误：应返回 int，返回了 List[str]

# ✅ 修复类型错误
def process(items: List[str]) -> int:
    return len(items)

# ❌ Optional 未处理
def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    return find_user(user_id)

user = get_user(1)
print(user["name"])  # 错误：user 可能为 None

# ✅ 处理 Optional
def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    return find_user(user_id)

user = get_user(1)
if user is not None:
    print(user["name"])
```

### 4.5 Pre-commit Hooks

#### 配置

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

#### 安装和使用

```bash
# 安装 pre-commit
pip install pre-commit

# 安装 hooks
pre-commit install

# 手动运行所有 hooks
pre-commit run --all-files

# 跳过 hooks（不推荐）
git commit --no-verify -m "message"
```

---

## 5. 示例代码

### 5.1 类定义

```python
# ✅ 好的示例
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class CrawlResult:
    """爬取结果数据类

    使用 dataclass 简化数据类的定义，自动生成 __init__ 等方法。

    Attributes:
        url: 爬取的 URL
        status: HTTP 状态码
        content: 网页内容
        metadata: 元数据
    """
    url: str
    status: int
    content: str
    metadata: Dict[str, Any]

    @property
    def is_success(self) -> bool:
        """是否成功"""
        return 200 <= self.status < 300

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "url": self.url,
            "status": self.status,
            "content": self.content,
            "metadata": self.metadata,
        }


class AsyncWebCrawler:
    """异步网页爬虫

    提供 HTTP 请求、内容提取、结果缓存等功能。
    """

    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3

    def __init__(
        self,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
        user_agent: Optional[str] = None,
    ):
        """初始化爬虫

        Args:
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
            user_agent: 自定义 User-Agent
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.user_agent = user_agent or "Mozilla/5.0"
        self._cache: Dict[str, CrawlResult] = {}

    async def crawl(self, url: str, use_cache: bool = True) -> CrawlResult:
        """爬取指定 URL

        Args:
            url: 目标 URL
            use_cache: 是否使用缓存

        Returns:
            爬取结果对象

        Raises:
            ValueError: URL 无效
            TimeoutError: 请求超时
        """
        if use_cache and url in self._cache:
            logger.info(f"从缓存读取: {url}")
            return self._cache[url]

        if not self._validate_url(url):
            raise ValueError(f"无效的 URL: {url}")

        result = await self._fetch_with_retry(url)
        if use_cache:
            self._cache[url] = result

        return result

    def _validate_url(self, url: str) -> bool:
        """验证 URL 格式

        Args:
            url: 待验证的 URL

        Returns:
            是否有效
        """
        return url.startswith(("http://", "https://"))

    async def _fetch_with_retry(self, url: str) -> CrawlResult:
        """带重试的请求

        Args:
            url: 目标 URL

        Returns:
            爬取结果
        """
        import httpx
        import asyncio

        last_error = None

        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        url,
                        timeout=self.timeout,
                        headers={"User-Agent": self.user_agent}
                    )
                    return CrawlResult(
                        url=url,
                        status=response.status_code,
                        content=response.text,
                        metadata={"response_time": response.elapsed.total_seconds()}
                    )

            except httpx.TimeoutError as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"超时重试 ({attempt + 1}/{self.max_retries}): {url}")
                    await asyncio.sleep(wait_time)

            except Exception as e:
                last_error = e
                logger.error(f"请求失败: {url} - {e}")
                break

        raise TimeoutError(f"请求超时: {url}") from last_error


# ❌ 坏的示例
class badcrawler:
    def __init__(self, timeout=30):
        self.t = timeout

    def crawl(self, url):
        import requests
        r = requests.get(url, timeout=self.t)
        return r.text

# 问题：
# 1. 类名不符合命名规范
# 2. 缺少类型注解
# 3. 缺少文档字符串
# 4. 没有异常处理
# 5. 同步方法，性能差
```

### 5.2 异步函数

```python
# ✅ 好的示例
import asyncio
from typing import List, Dict, Any
import httpx
import logging

logger = logging.getLogger(__name__)


async def fetch_page(
    url: str,
    client: httpx.AsyncClient,
    timeout: float = 30.0
) -> Dict[str, Any]:
    """获取单个页面

    Args:
        url: 目标 URL
        client: HTTP 客户端
        timeout: 超时时间

    Returns:
        包含响应数据的字典

    Raises:
        httpx.TimeoutError: 请求超时
        httpx.HTTPStatusError: HTTP 错误
    """
    try:
        response = await client.get(url, timeout=timeout)
        response.raise_for_status()

        return {
            "url": url,
            "status": response.status_code,
            "content": response.text,
            "headers": dict(response.headers),
        }

    except httpx.TimeoutError as e:
        logger.error(f"请求超时: {url}")
        raise

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP 错误 {e.response.status_code}: {url}")
        raise


async def fetch_multiple_pages(
    urls: List[str],
    max_concurrent: int = 10
) -> List[Dict[str, Any]]:
    """并发获取多个页面

    使用信号量控制并发数，避免资源耗尽。

    Args:
        urls: URL 列表
        max_concurrent: 最大并发数

    Returns:
        响应列表
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def bounded_fetch(url: str) -> Dict[str, Any]:
        """带并发限制的获取函数"""
        async with semaphore:
            async with httpx.AsyncClient() as client:
                return await fetch_page(url, client)

    tasks = [bounded_fetch(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 过滤掉异常
    return [
        result for result in results
        if not isinstance(result, Exception)
    ]


# 使用示例
async def main():
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net",
    ]

    results = await fetch_multiple_pages(urls, max_concurrent=5)
    for result in results:
        print(f"{result['url']}: {result['status']}")


# ❌ 坏的示例
async def bad_fetch(url):
    # 缺少类型注解
    # 缺少文档字符串
    # 缺少异常处理
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
    return r.text
```

### 5.3 数据处理

```python
# ✅ 好的示例
from typing import List, Dict, Any, Optional
import re
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class ContentExtractor:
    """内容提取器

    从 HTML 中提取结构化内容。
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化提取器

        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.title_selector = self.config.get("title_selector", "h1")
        self.content_selector = self.config.get("content_selector", "article")

    def extract(self, html: str) -> Dict[str, Any]:
        """提取内容

        Args:
            html: HTML 字符串

        Returns:
            提取的结构化数据
        """
        soup = BeautifulSoup(html, "lxml")

        return {
            "title": self._extract_title(soup),
            "content": self._extract_content(soup),
            "author": self._extract_author(soup),
            "date": self._extract_date(soup),
            "tags": self._extract_tags(soup),
        }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取标题

        Args:
            soup: BeautifulSoup 对象

        Returns:
            标题文本
        """
        element = soup.select_one(self.title_selector)
        if not element:
            logger.warning(f"未找到标题元素: {self.title_selector}")
            return ""

        return element.get_text(strip=True)

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """提取正文

        Args:
            soup: BeautifulSoup 对象

        Returns:
            正文文本
        """
        element = soup.select_one(self.content_selector)
        if not element:
            logger.warning(f"未找到内容元素: {self.content_selector}")
            return ""

        # 清理空白
        text = element.get_text(separator="\n", strip=True)
        # 移除多余空行
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text

    def _extract_author(self, soup: BeautifulSoup) -> str:
        """提取作者"""
        meta = soup.find("meta", attrs={"name": "author"})
        if meta:
            return meta.get("content", "")

        # 尝试从 CSS 选择器获取
        element = soup.select_one(".author")
        if element:
            return element.get_text(strip=True)

        return ""

    def _extract_date(self, soup: BeautifulSoup) -> str:
        """提取日期"""
        meta = soup.find("meta", attrs={"name": "date"})
        if meta:
            return meta.get("content", "")

        element = soup.select_one(".date, .publish-date")
        if element:
            return element.get_text(strip=True)

        return ""

    def _extract_tags(self, soup: BeautifulSoup) -> List[str]:
        """提取标签

        Args:
            soup: BeautifulSoup 对象

        Returns:
            标签列表
        """
        elements = soup.select(".tag, .category")
        return [elem.get_text(strip=True) for elem in elements]


# ❌ 坏的示例
def bad_extract(html):
    # 所有逻辑混在一起
    soup = BeautifulSoup(html, "lxml")
    title = soup.find("h1")
    content = soup.find("article")
    author = soup.find("meta", {"name": "author"})

    result = {}
    if title:
        result["title"] = title.get_text()
    if content:
        result["content"] = content.get_text()
    if author:
        result["author"] = author.get("content")

    return result

# 问题：
# 1. 缺少类型注解
# 2. 没有封装成类
# 3. 缺少文档字符串
# 4. 没有清理和验证
# 5. 难以扩展和测试
```

---

## 6. 检查清单

### 提交代码前检查

- [ ] **代码格式化**
  - [ ] 运行 `black .` 格式化代码
  - [ ] 运行 `isort .` 排序导入
  - [ ] 确认没有多余的空白行

- [ ] **代码检查**
  - [ ] 运行 `flake8` 检查代码风格
  - [ ] 运行 `mypy` 检查类型注解
  - [ ] 修复所有警告和错误

- [ ] **测试**
  - [ ] 编写单元测试
  - [ ] 运行 `pytest` 确保测试通过
  - [ ] 检查测试覆盖率

- [ ] **文档**
  - [ ] 所有公共 API 有文档字符串
  - [ ] 使用 Google 风格的文档
  - [ ] 包含使用示例

- [ ] **代码审查**
  - [ ] 遵循命名规范
  - [ ] 没有魔法数字，使用常量
  - [ ] 异常处理完善
  - [ ] 资源正确释放

### 代码审查要点

- [ ] **可读性**
  - [ ] 函数和变量命名清晰
  - [ ] 复杂逻辑有注释说明
  - [ ] 代码结构合理

- [ ] **性能**
  - [ ] 避免不必要的循环
  - [ ] 使用异步 I/O
  - [ ] 合理使用缓存

- [ ] **安全性**
  - [ ] 输入验证
  - [ ] SQL 注入防护
  - [ ] XSS 防护

- [ ] **可维护性**
  - [ ] 单一职责原则
  - [ ] 避免过度耦合
  - [ ] 易于扩展

---

## 快速参考

### 常用命令

```bash
# 代码格式化
black packages/
isort packages/

# 代码检查
flake8 packages/
mypy packages/

# 运行测试
pytest tests/
pytest --cov=packages tests/

# 类型检查
mypy --strict packages/

# Pre-commit
pre-commit install
pre-commit run --all-files
```

### 类型注解速查

```python
from typing import (
    List, Dict, Set, Tuple, Optional, Union,
    Callable, Iterator, AsyncIterator, TypeAlias
)

# 基础类型
def func(x: int, y: str) -> bool:
    pass

# 容器类型
def func1(items: List[str]) -> Dict[str, int]:
    pass

def func2(coords: Tuple[float, float]) -> Set[int]:
    pass

# 可选类型
def func3(value: Optional[str]) -> str:
    return value or ""

# 联合类型
def func4(value: Union[int, str]) -> str:
    return str(value)

# 函数类型
def func5(callback: Callable[[int, int], bool]) -> None:
    pass

# 迭代器类型
def func6() -> Iterator[str]:
    yield "test"

async def func7() -> AsyncIterator[str]:
    yield "test"

# 类型别名
JSON: TypeAlias = Dict[str, Any]
URL: TypeAlias = str
```

---

## 版本历史

- **v1.0.0** (2024-01-01): 初始版本

---

**注意**: 本文档会根据项目发展持续更新，请定期查看最新版本。
