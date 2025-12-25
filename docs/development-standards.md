# Awesome-crawl4AI 开发规范标准

> 版本：1.0.0
> 更新日期：2025-12-25
> 目标：建立统一、高质量的代码开发规范

---

## 目录

1. [项目概述](#1-项目概述)
2. [编码规范](#2-编码规范)
3. [项目结构规范](#3-项目结构规范)
4. [开发工具配置规范](#4-开发工具配置规范)
5. [Git 工作流规范](#5-git-工作流规范)
6. [测试规范](#6-测试规范)
7. [文档规范](#7-文档规范)
8. [安全规范](#8-安全规范)
9. [性能优化规范](#9-性能优化规范)
10. [代码审查规范](#10-代码审查规范)

---

## 1. 项目概述

### 1.1 项目简介

Awesome-crawl4AI 是一个专注于为 AI 应用提供高质量网页数据采集解决方案的项目。

**核心特性：**
- 智能化网页数据采集
- AI 友好的数据格式输出
- 现代化技术栈和架构设计
- 高性能异步处理

### 1.2 设计原则

项目遵循以下核心设计原则：

#### SOLID 原则

- **单一职责原则 (SRP)**：每个类/函数只负责一件事
- **开闭原则 (OCP)**：对扩展开放，对修改封闭
- **里氏替换原则 (LSP)**：子类可以替换父类
- **接口隔离原则 (ISP)**：不应强迫实现不使用的接口
- **依赖倒置原则 (DIP)**：依赖抽象而非具体实现

#### KISS 原则 (Keep It Simple, Stupid)

- 保持代码简单明了
- 避免过度设计
- 优先选择简单的解决方案

#### DRY 原则 (Don't Repeat Yourself)

- 避免代码重复
- 提取公共逻辑到函数/类
- 使用继承和组合复用代码

#### YAGNI 原则 (You Aren't Gonna Need It)

- 只实现当前需要的功能
- 避免预想需求
- 保持代码精简

### 1.3 技术栈

**主要技术：**
- Python 3.9+ (主要开发语言)
- httpx (HTTP 客户端)
- BeautifulSoup4/lxml (HTML 解析)
- Playwright/Selenium (浏览器自动化)
- Pydantic (数据验证)

**辅助技术：**
- Markdownify (HTML 转 Markdown)
- Tenacity (重试机制)
- Python-dotenv (环境变量管理)

---

## 2. 编码规范

### 2.1 Python 代码风格

#### 基本规范

遵循 **PEP 8** 标准：

| 配置项 | 值 | 说明 |
|--------|-----|------|
| 行长度 | 100 字符 | 可配置，见 `pyproject.toml` |
| 缩进 | 4 空格 | 使用空格而非 Tab |
| 编码 | UTF-8 | 所有源文件使用 UTF-8 编码 |
| 换行 | LF (Unix) | 避免使用 CRLF (Windows) |

#### 命名规范

**类名（PascalCase）**
```python
class WebCrawler:
    """网页爬虫基类"""
    pass

class AsyncWebCrawler:
    """异步网页爬虫"""
    pass
```

**函数和变量（snake_case）**
```python
def crawl_url(url: str) -> Dict[str, Any]:
    """爬取指定 URL"""
    pass

max_retries = 3
current_page = 1
```

**常量（UPPER_SNAKE_CASE）**
```python
DEFAULT_TIMEOUT = 30
MAX_RETRY_COUNT = 3
USER_AGENT = "Mozilla/5.0 ..."
```

**私有成员（单下划线前缀）**
```python
class WebCrawler:
    def __init__(self):
        self._session = None  # 私有实例变量
        self._cache = {}

    def _validate_url(self, url: str) -> bool:
        """私有方法"""
        return True
```

**受保护成员（双下划线前缀，名字修饰）**
```python
class BaseExtractor:
    def __init__(self):
        self.__config = {}  # 名字修饰，防止子类覆盖
```

### 2.2 类型注解规范

#### 强制类型注解

所有公共 API 必须包含类型注解：

```python
from typing import List, Dict, Optional, Union

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
    pass
```

#### 复杂类型注解

```python
from typing import List, Dict, Optional, Union, Tuple, AsyncIterator, TypeAlias

# 类型别名
JSON: TypeAlias = Dict[str, Any]
URL: TypeAlias = str
Headers: TypeAlias = Dict[str, str]

# 函数类型注解
def process_items(items: List[str]) -> Dict[str, int]:
    """处理字符串列表"""
    return {item: len(item) for item in items}

def get_config() -> Dict[str, Union[str, int, bool]]:
    """获取配置"""
    return {"timeout": 30, "enabled": True, "mode": "fast"}

def find_user(user_id: int) -> Optional[Dict[str, Any]]:
    """查找用户，可能不存在"""
    return None if user_id < 0 else {"id": user_id}

def get_coordinates() -> Tuple[float, float]:
    """获取坐标"""
    return 39.9042, 116.4074

async def stream_pages(urls: List[str]) -> AsyncIterator[str]:
    """异步流式处理页面"""
    for url in urls:
        yield await fetch_page(url)
```

### 2.3 Docstring 规范

使用 **Google Style** 文档字符串：

```python
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
    pass
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
    pass
```

### 2.4 导入规范

#### 导入顺序

严格按照以下顺序导入，使用空行分隔：

```python
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
from crawl4ai.crawler import WebCrawler
from crawl4ai.extractors.base import BaseExtractor
from crawl4ai.utils.http import get_headers
```

#### 避免循环导入

使用 `TYPE_CHECKING` 避免循环导入：

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from extractors.base import BaseExtractor

class WebCrawler:
    def __init__(self, extractor: Optional["BaseExtractor"] = None):
        self.extractor = extractor
```

### 2.5 异步代码规范

#### async/await 使用

```python
# ✅ 好的示例 - 并发执行
async def fetch_multiple_pages(urls: List[str]) -> Dict[str, str]:
    """并发获取多个页面"""
    async with httpx.AsyncClient() as client:
        tasks = [fetch_single_page(url, client) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            url: result if not isinstance(result, Exception) else ""
            for url, result in zip(urls, results)
        }

# ❌ 坏的示例 - 串行执行
async def fetch_multiple_pages_bad(urls: List[str]) -> Dict[str, str]:
    """串行请求，性能差"""
    results = {}
    async with httpx.AsyncClient() as client:
        for url in urls:
            results[url] = await client.get(url)
    return results
```

#### 异步上下文管理器

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed_session(headers: Dict[str, str]):
    """管理 httpx 会话的生命周期"""
    client = httpx.AsyncClient(headers=headers)
    try:
        yield client
    finally:
        await client.aclose()

# 使用
async with managed_session({"User-Agent": "Crawler"}) as client:
    response = await client.get("https://example.com")
```

#### 并发控制

```python
class AsyncCrawler:
    """带并发控制的异步爬虫"""

    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def crawl(self, url: str) -> str:
        """使用信号量限制并发数"""
        async with self._semaphore:
            return await self._fetch(url)
```

### 2.6 异常处理规范

#### 精确捕获异常

```python
# ✅ 好的示例 - 精确捕获
async def safe_request(url: str) -> Optional[str]:
    """只捕获预期的异常"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.text

    except httpx.TimeoutException:
        logger.warning(f"请求超时: {url}")
        return None

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP 错误 {e.response.status_code}: {url}")
        return None

    # 其他异常正常传播

# ❌ 坏的示例 - 过于宽泛
async def unsafe_request(url: str) -> Optional[str]:
    try:
        async with httpx.AsyncClient() as client:
            return await client.get(url)
    except Exception:
        # 捕获了所有异常，包括 KeyboardInterrupt
        return None
```

#### 自定义异常

```python
class CrawlerError(Exception):
    """爬虫基础异常"""
    pass

class ConfigurationError(CrawlerError):
    """配置错误"""
    pass

class ExtractionError(CrawlerError):
    """数据提取错误"""
    pass

class FetchError(CrawlerError):
    """网页获取错误"""

    def __init__(self, url: str, status_code: int, message: str):
        self.url = url
        self.status_code = status_code
        super().__init__(f"{url} 返回 {status_code}: {message}")
```

#### 异常链

```python
# ✅ 使用 raise ... from 保留异常链
def process_html(html: str) -> Dict[str, Any]:
    try:
        soup = BeautifulSoup(html, "lxml")
        content = soup.find("div", class_="content")
        if not content:
            raise ValueError("未找到内容区域")
        return {"text": content.get_text(strip=True)}

    except Exception as e:
        # 保留原始异常
        raise ExtractionError("HTML 处理失败") from e

# ❌ 丢失原始异常
def process_html_bad(html: str) -> Dict[str, Any]:
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        # 丢失了原始异常信息
        raise ExtractionError("HTML 处理失败")
```

---

## 3. 项目结构规范

### 3.1 目录组织标准

```
awesome-crawl4ai/
├── docs/                         # 项目文档
│   ├── development-standards.md  # 开发规范（本文档）
│   ├── CODING_STANDARDS.md       # 编码规范
│   ├── TESTING_STANDARDS.md      # 测试规范
│   └── api/                      # API 文档
├── examples/                     # 示例代码
│   ├── basic/                    # 基础示例
│   ├── advanced/                 # 高级示例
│   └── integrations/             # 集成示例
├── packages/                     # 核心包
│   ├── crawler/                  # 爬虫引擎
│   │   ├── __init__.py
│   │   ├── base.py               # 基础类
│   │   ├── async_crawler.py      # 异步实现
│   │   ├── sync_crawler.py       # 同步实现
│   │   ├── config.py             # 配置
│   │   ├── constants.py          # 常量
│   │   └── utils.py              # 工具函数
│   ├── extractors/               # 数据提取器
│   │   ├── __init__.py
│   │   ├── base.py               # 基础提取器
│   │   ├── css_extractor.py      # CSS 提取
│   │   ├── xpath_extractor.py    # XPath 提取
│   │   └── ai_extractor.py       # AI 智能提取
│   ├── processors/               # 数据处理器
│   │   ├── __init__.py
│   │   ├── cleaner.py            # 数据清洗
│   │   ├── formatter.py          # 格式化
│   │   └── validator.py          # 数据验证
│   └── integrations/             # 第三方集成
│       ├── __init__.py
│       ├── playwright.py         # Playwright 集成
│       └── selenium.py           # Selenium 集成
├── tests/                        # 测试套件
│   ├── unit/                     # 单元测试
│   ├── integration/              # 集成测试
│   ├── e2e/                      # 端到端测试
│   ├── fixtures/                 # 测试数据
│   └── conftest.py               # pytest 配置
├── tools/                        # 开发工具
│   ├── scripts/                  # 脚本
│   └── benchmarks/               # 性能测试
├── .github/                      # GitHub 配置
│   └── workflows/                # CI/CD 工作流
├── .env.example                  # 环境变量示例
├── .gitignore                    # Git 忽略配置
├── .pre-commit-config.yaml       # Pre-commit 配置
├── pyproject.toml                # 项目配置
├── README.md                     # 项目说明
└── LICENSE                       # 许可证
```

### 3.2 模块划分原则

#### 单一职责

每个模块应有明确的单一职责：

```python
# ✅ 好的示例 - 职责清晰
# packages/crawler/base.py - 定义基础接口
# packages/crawler/async_crawler.py - 异步实现
# packages/crawler/sync_crawler.py - 同步实现

# ❌ 坏的示例 - 职责混乱
# packages/crawler/everything.py - 包含所有功能
```

#### 依赖方向

依赖应指向稳定的抽象层：

```
┌─────────────────┐
│   应用层        │  examples/
├─────────────────┤
│   业务层        │  integrations/
├─────────────────┤
│   核心层        │  crawler/, extractors/, processors/
├─────────────────┤
│   工具层        │  utils/
└─────────────────┘
```

### 3.3 配置文件管理

#### 环境变量

使用 `.env` 文件管理环境变量：

```bash
# .env.example
# 复制此文件为 .env 并填写实际值

# 基础配置
PYTHON_VERSION=3.9
LOG_LEVEL=INFO

# HTTP 配置
DEFAULT_TIMEOUT=30
MAX_RETRIES=3
MAX_CONCURRENT=10

# 代理配置（可选）
HTTP_PROXY=
HTTPS_PROXY=

# API 密钥（如需要）
OPENAI_API_KEY=
```

#### 配置类

使用 Pydantic 管理配置：

```python
from pydantic import BaseSettings, Field

class CrawlerConfig(BaseSettings):
    """爬虫配置类"""

    # 基础配置
    timeout: int = Field(30, gt=0, description="请求超时时间")
    max_retries: int = Field(3, ge=0, le=10, description="最大重试次数")
    max_concurrent: int = Field(10, gt=0, le=100, description="最大并发数")

    # 代理配置
    proxy: Optional[str] = Field(None, description="代理地址")

    # 日志配置
    log_level: str = Field("INFO", regex="^(DEBUG|INFO|WARNING|ERROR)$")

    class Config:
        env_file = ".env"
        env_prefix = "CRAWLER_"

# 使用
config = CrawlerConfig()
print(config.timeout)
```

---

## 4. 开发工具配置规范

### 4.1 Black 配置（代码格式化）

#### 配置文件

配置已在 `pyproject.toml` 中：

```toml
[tool.black]
line-length = 100
target-version = ["py39", "py310", "py311", "py312"]
include = '\.pyi?$'
extend-exclude = '''
/(
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

#### 使用方法

```bash
# 格式化代码
black packages/

# 检查格式（不修改）
black --check packages/

# 显示差异
black --diff packages/
```

### 4.2 isort 配置（导入排序）

#### 配置文件

```toml
[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
```

#### 使用方法

```bash
# 排序导入
isort packages/

# 检查导入
isort --check-only packages/

# 显示差异
isort --diff packages/
```

### 4.3 Flake8 配置（代码检查）

#### 配置文件

```toml
[tool.flake8]
max-line-length = 100
extend-ignore = ["E203", "W503"]
exclude = [
    ".git",
    "__pycache__",
    "build",
    "dist",
    ".eggs",
    "*.egg-info",
    ".venv",
    "venv",
]
```

#### 使用方法

```bash
# 检查代码
flake8 packages/

# 显示详细错误
flake8 packages/ --show-source

# 统计错误
flake8 packages/ --statistics
```

### 4.4 mypy 配置（类型检查）

#### 配置文件

```toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
follow_imports = "normal"
strict_equality = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

#### 使用方法

```bash
# 类型检查
mypy packages/

# 生成 HTML 报告
mypy --html-report ./mypy-report packages/

# 严格模式
mypy --strict packages/
```

### 4.5 pytest 配置（测试框架）

#### 配置文件

```toml
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-ra",                      # 显示摘要信息
    "--strict-markers",         # 严格标记模式
    "--strict-config",          # 严格配置模式
    "--showlocals",             # 失败时显示局部变量
]
asyncio_mode = "auto"           # 自动检测异步测试
```

#### 使用方法

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/test_crawler.py

# 覆盖率报告
pytest --cov=packages --cov-report=html

# 并行运行
pytest -n auto
```

### 4.6 pre-commit 配置

#### 配置文件

创建 `.pre-commit-config.yaml`：

```yaml
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

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

#### 使用方法

```bash
# 安装 pre-commit
pip install pre-commit

# 安装 hooks
pre-commit install

# 手动运行
pre-commit run --all-files
```

---

## 5. Git 工作流规范

### 5.1 提交信息规范（Conventional Commits）

#### 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | feat(crawler): 添加异步爬虫支持 |
| fix | 修复 bug | fix(extractor): 修复 CSS 选择器解析错误 |
| docs | 文档变更 | docs: 更新 API 文档 |
| style | 代码格式（不影响功能） | style: 统一代码缩进 |
| refactor | 重构（不是新功能也不是修复） | refactor(crawler): 重构请求处理逻辑 |
| perf | 性能优化 | perf(crawler): 优化并发请求性能 |
| test | 测试相关 | test(extractor): 添加单元测试 |
| chore | 构建过程或辅助工具变动 | chore: 更新依赖版本 |

#### 示例

```bash
# 简单提交
git commit -m "feat(crawler): 添加并发控制"

# 详细提交
git commit -m "feat(extractor): 添加 AI 智能提取功能

- 集成 OpenAI API
- 支持自定义提示词
- 添加错误处理和重试机制

Closes #123"
```

### 5.2 分支管理策略

#### 主要分支

- `main`: 主分支，稳定版本
- `develop`: 开发分支，最新功能

#### 功能分支

```
feat/<feature-name>
```

示例：
```
feat/async-crawler
feat/ai-extractor
feat/proxy-support
```

#### 修复分支

```
fix/<bug-description>
```

示例：
```
fix/css-selector-parse-error
fix/memory-leak-in-cache
```

#### 工作流程

```bash
# 1. 从 develop 创建功能分支
git checkout develop
git pull origin develop
git checkout -b feat/new-feature

# 2. 开发并提交
git add .
git commit -m "feat: 添加新功能"

# 3. 推送到远程
git push origin feat/new-feature

# 4. 创建 Pull Request 到 develop

# 5. 代码审查通过后合并

# 6. 删除功能分支
git branch -d feat/new-feature
```

### 5.3 代码审查清单

#### 功能性

- [ ] 代码实现了预期功能
- [ ] 边界条件处理正确
- [ ] 错误处理完善

#### 代码质量

- [ ] 遵循编码规范
- [ ] 命名清晰准确
- [ ] 逻辑简洁明了
- [ ] 没有代码重复

#### 测试

- [ ] 单元测试覆盖充分
- [ ] 测试用例有意义
- [ ] 所有测试通过

#### 文档

- [ ] 公共 API 有文档字符串
- [ ] 复杂逻辑有注释
- [ ] 更新了相关文档

#### 性能

- [ ] 没有明显的性能问题
- [ ] 资源使用合理
- [ ] 异步使用正确

---

## 6. 测试规范

### 6.1 测试策略

#### 测试金字塔

```
        /\
       /  \        端到端测试 (10%)
      /____\
     /      \      集成测试 (30%)
    /________\
   /          \   单元测试 (60%)
  /______________\
```

#### 覆盖率要求

| 模块 | 覆盖率目标 |
|------|-----------|
| 核心引擎 | 90%+ |
| 提取器 | 85%+ |
| 处理器 | 85%+ |
| 集成模块 | 75%+ |
| 整体目标 | 80%+ |

### 6.2 单元测试规范

#### 测试文件命名

```
tests/unit/test_crawler.py
tests/unit/test_extractors/
tests/unit/test_extractors/test_css_extractor.py
```

#### 测试结构（AAA 模式）

```python
def test_extract_title_when_html_has_title(self):
    """Given: HTML 包含标题
    When: 提取标题
    Then: 返回正确标题
    """
    # Arrange（准备）
    html = "<html><body><h1>Test Title</h1></body></html>"
    extractor = CSSExtractor(title="h1")

    # Act（执行）
    result = extractor.extract(html)

    # Assert（断言）
    assert result.title == "Test Title"
```

### 6.3 异步测试规范

```python
import pytest

@pytest.mark.asyncio
async def test_async_crawler():
    """测试异步爬虫"""
    crawler = AsyncCrawler()
    result = await crawler.crawl("https://example.com")
    assert result.success
```

### 6.4 Mock 使用规范

```python
from unittest.mock import Mock, patch

def test_with_mock():
    """使用 Mock 测试"""
    client = HttpClient()

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html>Test</html>"

    with patch.object(client, 'request', return_value=mock_response):
        result = client.fetch("https://example.com")
        assert result.status_code == 200
```

### 6.5 Fixture 使用

```python
@pytest.fixture
def crawler():
    """提供爬虫实例"""
    crawler = WebCrawler()
    yield crawler
    crawler.close()

def test_with_fixture(crawler):
    """使用 fixture"""
    result = crawler.crawl("https://example.com")
    assert result.success
```

---

## 7. 文档规范

### 7.1 README 标准

项目 README 应包含：

```markdown
# 项目名称

简短描述项目

## 功能特性

- 特性 1
- 特性 2

## 快速开始

### 安装

\`\`\`bash
pip install awesome-crawl4ai
\`\`\`

### 基本使用

\`\`\`python
from crawl4ai import WebCrawler

crawler = WebCrawler()
result = crawler.crawl("https://example.com")
\`\`\`

## 文档

- [API 文档](docs/api/)
- [开发指南](docs/development-standards.md)
- [贡献指南](CONTRIBUTING.md)

## 许可证

MIT License
```

### 7.2 API 文档生成

使用 Sphinx 生成 API 文档：

```bash
# 安装 Sphinx
pip install sphinx sphinx-rtd-theme

# 生成文档
cd docs
sphinx-apidoc -o api ../packages
make html
```

### 7.3 代码注释规范

#### 行内注释

```python
# 使用信号量限制并发数，防止资源耗尽
async with self._semaphore:
    result = await self._fetch(url)
```

#### 块注释

```python
"""
这个函数实现了智能重试机制。

重试策略：
1. 首次失败后等待 1 秒
2. 第二次失败后等待 2 秒
3. 第三次失败后等待 4 秒
4. 最多重试 3 次
"""
```

---

## 8. 安全规范

### 8.1 密钥管理

#### 使用环境变量

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY 环境变量未设置")
```

#### .gitignore

```
.env
*.key
*.pem
credentials.json
```

### 8.2 输入验证

```python
def validate_url(url: str) -> bool:
    """验证 URL 格式"""
    if not url:
        return False

    # 白名单协议
    allowed_schemes = ["http", "https"]
    from urllib.parse import urlparse
    parsed = urlparse(url)

    return parsed.scheme in allowed_schemes
```

### 8.3 SQL 注入防护

```python
# ✅ 使用参数化查询
cursor.execute("SELECT * FROM pages WHERE url = ?", (url,))

# ❌ 避免字符串拼接
cursor.execute(f"SELECT * FROM pages WHERE url = '{url}'")
```

### 8.4 XSS 防护

```python
import html

def sanitize_input(text: str) -> str:
    """清理用户输入"""
    return html.escape(text)
```

---

## 9. 性能优化规范

### 9.1 异步优先

```python
# ✅ 使用异步
async def fetch_multiple(urls: List[str]) -> List[str]:
    tasks = [fetch(url) for url in urls]
    return await asyncio.gather(*tasks)

# ❌ 避免同步
def fetch_multiple(urls: List[str]) -> List[str]:
    return [fetch(url) for url in urls]
```

### 9.2 连接池复用

```python
# ✅ 复用连接
class HttpClient:
    def __init__(self):
        self._client = httpx.AsyncClient()

    async def close(self):
        await self._client.aclose()

# ❌ 每次创建新连接
async def bad_fetch(url: str):
    async with httpx.AsyncClient() as client:
        return await client.get(url)
```

### 9.3 缓存策略

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def parse_selector(selector: str):
    """缓存解析后的选择器"""
    return CSSSelector(selector)
```

### 9.4 大数据处理

```python
# ✅ 使用生成器
def process_large_file(file_path: Path) -> Iterator[Dict]:
    with open(file_path) as f:
        for line in f:
            yield json.loads(line)

# ❌ 一次性加载
def bad_process(file_path: Path) -> List[Dict]:
    with open(file_path) as f:
        return [json.loads(line) for line in f]
```

---

## 10. 代码审查规范

### 10.1 审查流程

1. **自动检查**
   - [ ] Pre-commit hooks 通过
   - [ ] CI/CD 检查通过
   - [ ] 测试覆盖率达标

2. **人工审查**
   - [ ] 功能正确性
   - [ ] 代码质量
   - [ ] 性能考虑
   - [ ] 安全性

### 10.2 审查要点

#### 可读性

- 命名是否清晰
- 逻辑是否简洁
- 注释是否充分

#### 可维护性

- 是否遵循 DRY 原则
- 是否易于扩展
- 是否有单元测试

#### 性能

- 是否有性能瓶颈
- 是否正确使用异步
- 资源使用是否合理

#### 安全性

- 是否有输入验证
- 是否正确处理敏感信息
- 是否有注入风险

---

## 附录

### A. 快速参考

```bash
# 代码格式化
black packages/
isort packages/

# 代码检查
flake8 packages/
mypy packages/

# 运行测试
pytest
pytest --cov=packages

# Pre-commit
pre-commit run --all-files
```

### B. 常用命令

```bash
# 安装依赖
pip install -e ".[dev]"

# 运行示例
python examples/basic/simple_crawler.py

# 生成文档
cd docs && make html

# 性能测试
pytest tests/benchmarks/ -v
```

### C. 相关资源

- [Python PEP 8](https://peps.python.org/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [pytest 文档](https://docs.pytest.org/)
- [Sphinx 文档](https://www.sphinx-doc.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**文档版本**：1.0.0
**最后更新**：2025-12-25
**维护者**：Awesome-crawl4AI Team
**反馈**：请在 GitHub Issues 提出问题和建议
