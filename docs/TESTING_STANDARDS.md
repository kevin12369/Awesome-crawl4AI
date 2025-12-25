# Awesome-crawl4AI 测试规范文档

> 版本：1.0.0
> 更新日期：2024-12-25
> 目标：构建高质量、可维护的测试体系

---

## 目录

1. [测试策略](#1-测试策略)
2. [单元测试规范](#2-单元测试规范)
3. [集成测试规范](#3-集成测试规范)
4. [测试命名和组织](#4-测试命名和组织)
5. [测试最佳实践](#5-测试最佳实践)
6. [CI/CD 集成](#6-cicd-集成)
7. [测试示例](#7-测试示例)
8. [测试工具和命令](#8-测试工具和命令)

---

## 1. 测试策略

### 1.1 测试金字塔

我们采用经典的测试金字塔策略，确保在合适的层次进行测试：

```
        /\
       /  \        端到端测试 (E2E)
      /____\       - 10% 比例
     /      \
    /        \      集成测试
   /__________\     - 30% 比例
  /            \
 /              \   单元测试
/________________\  - 60% 比例
```

#### 各层次测试说明

**单元测试 (60%)**
- 测试单个函数、方法、类的行为
- 快速执行（毫秒级）
- 无外部依赖（使用 Mock）
- 高覆盖率要求

**集成测试 (30%)**
- 测试模块间的交互
- 测试与外部服务的集成
- 适度使用真实依赖
- 中等执行速度（秒级）

**端到端测试 (10%)**
- 测试完整用户场景
- 使用真实浏览器和网络
- 较慢执行（分钟级）
- 覆盖关键业务流程

### 1.2 测试覆盖率要求

| 模块类型 | 覆盖率目标 | 说明 |
|---------|-----------|------|
| 核心引擎 | 90%+ | `packages/crawler/` 核心逻辑 |
| 提取器 | 85%+ | `packages/extractors/` 数据提取 |
| 处理器 | 85%+ | `packages/processors/` 数据处理 |
| 集成模块 | 75%+ | `packages/integrations/` 第三方集成 |
| 工具类 | 80%+ | 辅助工具函数 |
| **整体目标** | **80%+** | 项目整体覆盖率 |

### 1.3 测试优先级

**P0 - 必须测试（关键功能）**
- 爬虫核心引擎（启动、停止、状态管理）
- 异步并发控制
- 错误处理和重试机制
- 数据提取核心逻辑

**P1 - 应该测试（重要功能）**
- 各类提取器（CSS、XPath、AI 提取）
- 反爬虫机制
- 缓存系统
- 日志记录

**P2 - 可以测试（辅助功能）**
- 命令行工具
- 辅助函数
- 文档示例代码

---

## 2. 单元测试规范

### 2.1 pytest 基础配置

项目使用 `pytest` 作为测试框架，配置文件 `pyproject.toml`：

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

### 2.2 异步代码测试

使用 `pytest-asyncio` 测试异步代码：

```python
import pytest
from packages.crawler.engine import AsyncCrawler

# 方式1：使用 async def
@pytest.mark.asyncio
async def test_async_crawler_basic():
    """测试异步爬虫基本功能"""
    crawler = AsyncCrawler()
    result = await crawler.crawl("https://example.com")
    assert result.status == 200
    assert result.content is not None

# 方式2：使用 pytest.fixture
@pytest.fixture
async def crawler():
    """提供爬虫实例的 fixture"""
    crawler = AsyncCrawler()
    yield crawler
    await crawler.close()

@pytest.mark.asyncio
async def test_with_fixture(crawler):
    """使用 fixture 的异步测试"""
    result = await crawler.crawl("https://example.com")
    assert result.success
```

### 2.3 Mock 使用策略

使用 `unittest.mock` 进行依赖隔离：

```python
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import pytest
from packages.crawler.http_client import HttpClient

# 同步函数 Mock
def test_http_client_with_mock():
    """测试使用 Mock 的 HTTP 客户端"""
    client = HttpClient()

    # Mock 响应
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html>Test</html>"
    mock_response.json.return_value = {"data": "test"}

    # Patch 外部依赖
    with patch.object(client, 'request', return_value=mock_response):
        result = client.fetch("https://example.com")
        assert result.status_code == 200
        assert result.text == "<html>Test</html>"

# 异步函数 Mock
@pytest.mark.asyncio
async def test_async_http_client():
    """测试异步 HTTP 客户端"""
    client = HttpClient()

    # 创建 AsyncMock
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.text = "<html>Async Test</html>"

    with patch.object(client, 'async_fetch', return_value=mock_response):
        result = await client.fetch_async("https://example.com")
        assert result.status == 200
```

### 2.4 Fixture 设计模式

#### 基础 Fixture

```python
import pytest
from packages.crawler import WebCrawler
from packages.extractors import CSSExtractor

@pytest.fixture
def crawler():
    """提供爬虫实例"""
    crawler = WebCrawler()
    yield crawler
    crawler.close()

@pytest.fixture
def sample_extractor():
    """提供示例提取器"""
    return CSSExtractor(
        title="h1",
        content="article p",
        metadata=".meta-info"
    )

@pytest.fixture
def sample_html():
    """提供示例 HTML 内容"""
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Main Title</h1>
            <article>
                <p>First paragraph</p>
                <p>Second paragraph</p>
            </article>
            <div class="meta-info">
                <span class="author">Author Name</span>
                <time>2024-12-25</time>
            </div>
        </body>
    </html>
    """
```

#### 带参数的 Fixture

```python
@pytest.fixture
def mock_response():
    """工厂模式 fixture，创建不同的 mock 响应"""
    def _create_response(status_code, text):
        mock = Mock()
        mock.status_code = status_code
        mock.text = text
        mock.ok = status_code < 400
        return mock
    return _create_response

def test_with_factory_fixture(mock_response):
    """使用工厂 fixture"""
    success_response = mock_response(200, "OK")
    error_response = mock_response(404, "Not Found")

    assert success_response.ok
    assert not error_response.ok
```

#### Fixture 作用域

```python
# 作用域：function（默认）、class、module、session
@pytest.fixture(scope="session")
def database():
    """整个测试会话共享一个数据库连接"""
    db = Database.connect()
    yield db
    db.close()

@pytest.fixture(scope="module")
def config():
    """模块级配置，模块内测试共享"""
    return load_config("test_config.yaml")

@pytest.fixture(scope="class")
class TestClassFixture:
    """类级 fixture，类内所有测试方法共享"""
    def setup_method(self):
        self.resource = Resource()

    def teardown_method(self):
        self.resource.cleanup()
```

---

## 3. 集成测试规范

### 3.1 集成测试范围

集成测试应覆盖：

1. **模块间交互**
   - 爬虫引擎 + 提取器
   - 提取器 + 处理器
   - 缓存系统 + 核心逻辑

2. **外部服务集成**
   - HTTP 客户端（使用测试服务器）
   - 浏览器自动化（Playwright/Selenium）
   - 数据库连接

3. **完整工作流**
   - 端到端爬取流程
   - 数据处理管道

### 3.2 测试环境准备

```python
import pytest
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

@pytest.fixture(scope="session")
def test_server():
    """启动测试 HTTP 服务器"""
    class TestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body>Test Server</body></html>")

    server = HTTPServer(('localhost', 8765), TestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    yield "http://localhost:8765"

    server.shutdown()
```

### 3.3 外部依赖 Mock 策略

```python
# 使用 pytest-responses（推荐）
import pytest
import responses

@responses.activate
def test_with_responses():
    """使用 responses 库 Mock HTTP 请求"""
    responses.add(
        responses.GET,
        "https://api.example.com/data",
        json={"result": "success"},
        status=200
    )

    client = ApiClient()
    result = client.fetch_data()
    assert result == {"result": "success"}

# 使用 aioresponses（异步）
import pytest
import aioresponses

@pytest.mark.asyncio
async def test_async_with_aioresponses():
    """测试异步 HTTP 客户端"""
    with aioresponses.aioresponses() as m:
        m.get("https://api.example.com/data", payload={"result": "success"})

        client = AsyncApiClient()
        result = await client.fetch_data()
        assert result == {"result": "success"}
```

### 3.4 测试数据管理

```python
import pytest
import json
from pathlib import Path

@pytest.fixture
def test_data_dir():
    """测试数据目录"""
    return Path(__file__).parent / "data"

@pytest.fixture
def sample_pages(test_data_dir):
    """加载示例网页数据"""
    data_file = test_data_dir / "sample_pages.json"
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# 使用 pytest-datafiles 插件
@pytest.fixture
def html_files(datafiles):
    """自动加载测试文件"""
    return {
        'page1': (datafiles / "page1.html").read_text(),
        'page2': (datafiles / "page2.html").read_text()
    }
```

---

## 4. 测试命名和组织

### 4.1 测试文件命名

遵循以下命名规范：

```
tests/
├── test_crawler.py              # 模块级测试文件
├── test_extractors/
│   ├── test_css_extractor.py    # 具体组件测试
│   ├── test_xpath_extractor.py
│   └── test_ai_extractor.py
├── test_integration/
│   ├── test_crawler_extractor_integration.py
│   └── test_browser_integration.py
└── test_e2e/
    ├── test_full_workflow.py
    └── test_batch_crawling.py
```

**命名规则**：
- 文件名：`test_<module_name>.py`
- 类名：`Test<ClassName>`
- 方法名：`test_<function_name>_<scenario>`

### 4.2 Given-When-Then 命名模式

```python
class TestCSSExtractor:
    """测试 CSS 提取器"""

    def test_extract_title_from_simple_html(self):
        """
        Given: 简单的 HTML 结构
        When: 使用 CSS 选择器提取标题
        Then: 正确返回标题内容
        """
        # Given - 准备测试数据
        html = "<html><body><h1>Test Title</h1></body></html>"
        extractor = CSSExtractor(title="h1")

        # When - 执行测试操作
        result = extractor.extract(html)

        # Then - 验证结果
        assert result.title == "Test Title"

    def test_extract_content_when_article_has_multiple_paragraphs(self):
        """
        Given: 包含多个段落的文章
        When: 提取文章内容
        Then: 返回所有段落内容
        """
        html = """
        <article>
            <p>First paragraph</p>
            <p>Second paragraph</p>
            <p>Third paragraph</p>
        </article>
        """
        extractor = CSSExtractor(content="article p")

        result = extractor.extract(html)

        assert len(result.content) == 3
        assert result.content[0] == "First paragraph"
```

### 4.3 测试目录结构

```
tests/
├── unit/                       # 单元测试
│   ├── test_crawler/
│   │   ├── test_engine.py
│   │   ├── test_scheduler.py
│   │   └── test_retry.py
│   ├── test_extractors/
│   │   ├── test_css_extractor.py
│   │   ├── test_xpath_extractor.py
│   │   └── test_llm_extractor.py
│   └── test_processors/
│       ├── test_cleaner.py
│       └── test_formatter.py
├── integration/                # 集成测试
│   ├── test_crawler_extractor.py
│   ├── test_cache_integration.py
│   └── test_browser_integration.py
├── e2e/                        # 端到端测试
│   ├── test_full_workflow.py
│   ├── test_batch_crawling.py
│   └── test_real_websites.py
├── fixtures/                   # 共享 fixtures
│   ├── __init__.py
│   ├── crawler_fixtures.py
│   └── data_fixtures.py
├── data/                       # 测试数据
│   ├── html/
│   ├── responses/
│   └── expected_results/
├── conftest.py                 # 全局 fixtures
└── __init__.py
```

### 4.4 测试分组和标记

```python
import pytest

# 定义标记
pytestmark = [
    pytest.mark.unit,           # 单元测试
    pytest.mark.fast,           # 快速测试
]

# 类级别标记
@pytest.mark.integration
class TestCrawlerIntegration:
    """集成测试类"""

    @pytest.mark.slow
    def test_crawl_large_website(self):
        """慢速测试（爬取大型网站）"""
        pass

    @pytest.mark.network
    def test_with_real_network(self):
        """需要真实网络的测试"""
        pass

# 函数级别标记
@pytest.mark.asyncio
@pytest.mark.browser
async def test_with_playwright():
    """需要浏览器的异步测试"""
    pass
```

**运行特定标记的测试**：

```bash
# 只运行快速测试
pytest -m fast

# 排除慢速测试
pytest -m "not slow"

# 运行集成测试
pytest -m integration

# 运行需要网络的测试
pytest -m "network and not slow"
```

---

## 5. 测试最佳实践

### 5.1 AAA 模式（Arrange-Act-Assert）

```python
def test_user_login_with_valid_credentials():
    """测试用户登录"""
    # Arrange（准备）：设置测试数据和环境
    user = User(username="testuser", password="password123")
    login_service = LoginService()

    # Act（执行）：调用被测试的功能
    result = login_service.login(user.username, user.password)

    # Assert（断言）：验证结果
    assert result.success is True
    assert result.token is not None
    assert result.user_id == user.id
```

### 5.2 测试独立性

```python
# ❌ 错误：测试之间有依赖
class TestBadExample:
    def test_step1_create_user(self):
        self.user = create_user("test")

    def test_step2_update_user(self):
        self.user.name = "updated"  # 依赖 test_step1

# ✅ 正确：每个测试独立
class TestGoodExample:
    def test_create_user(self):
        user = create_user("test")
        assert user.id is not None

    def test_update_user(self):
        user = create_user("test")  # 自己创建数据
        user.name = "updated"
        assert user.name == "updated"
```

### 5.3 边界条件测试

```python
class TestListProcessor:
    """测试列表处理器"""

    @pytest.mark.parametrize("input_list,expected", [
        ([], []),                           # 空列表
        ([1], [1]),                         # 单元素
        ([1, 2, 3], [1, 2, 3]),            # 正常情况
        ([None, 1, None], [1]),            # 包含 None
        (list(range(1000)), list(range(1000))),  # 大数据量
    ])
    def test_process_various_inputs(self, input_list, expected):
        """测试各种边界条件"""
        processor = ListProcessor()
        result = processor.process(input_list)
        assert result == expected

    def test_process_with_special_characters(self):
        """测试特殊字符"""
        processor = StringProcessor()
        result = processor.clean("!@#$%^&*()")
        assert result == ""

    def test_process_with_unicode(self):
        """测试 Unicode 字符"""
        processor = StringProcessor()
        result = processor.clean("你好世界🌍")
        assert "你好" in result
```

### 5.4 异常情况测试

```python
import pytest
from packages.crawler.exceptions import CrawlerError, TimeoutError

def test_crawler_with_invalid_url():
    """测试无效 URL"""
    crawler = WebCrawler()
    with pytest.raises(ValueError) as exc_info:
        crawler.crawl("not-a-valid-url")
    assert "Invalid URL" in str(exc_info.value)

def test_crawler_timeout():
    """测试超时处理"""
    crawler = WebCrawler(timeout=1)
    with pytest.raises(TimeoutError):
        crawler.crawl("https://slow-website.com")

@pytest.mark.asyncio
async def test_async_crawler_network_error():
    """测试网络错误"""
    crawler = AsyncCrawler()

    with patch.object(crawler, '_fetch', side_effect=ConnectionError):
        with pytest.raises(CrawlerError) as exc_info:
            await crawler.crawl("https://unreachable.com")
        assert "network" in str(exc_info.value).lower()
```

### 5.5 性能测试基础

```python
import time
import pytest

@pytest.mark.benchmark
class TestPerformance:
    """性能测试"""

    def test_crawl_performance_small_page(self):
        """测试小页面爬取性能"""
        crawler = WebCrawler()
        start_time = time.time()

        result = crawler.crawl("https://example.com")

        elapsed = time.time() - start_time
        assert result.success
        assert elapsed < 2.0  # 应该在 2 秒内完成

    @pytest.mark.parametrize("concurrency", [1, 5, 10, 20])
    def test_concurrent_crawling_performance(self, concurrency):
        """测试并发爬取性能"""
        crawler = WebCrawler(max_concurrency=concurrency)
        urls = ["https://example.com"] * 10

        start_time = time.time()
        results = crawler.crawl_batch(urls)
        elapsed = time.time() - start_time

        assert all(r.success for r in results)
        # 并发应该比顺序快
        assert elapsed < 10 * 0.5  # 假设每个请求 0.5 秒
```

### 5.6 参数化测试

```python
@pytest.mark.parametrize("url,status,expected_title", [
    ("https://example.com", 200, "Example Domain"),
    ("https://example.org", 200, "Example Organization"),
    ("https://example.net", 200, "Example Network"),
])
def test_crawl_various_websites(url, status, expected_title):
    """参数化测试多个网站"""
    crawler = WebCrawler()
    result = crawler.crawl(url)

    assert result.status_code == status
    assert expected_title in result.title

# 组合参数化
@pytest.mark.parametrize("url", ["https://site1.com", "https://site2.com"])
@pytest.mark.parametrize("format", ["markdown", "html", "json"])
def test_crawl_with_different_formats(url, format):
    """测试 URL 和输出格式的组合"""
    crawler = WebCrawler()
    result = crawler.crawl(url, output_format=format)

    assert result.success
    assert result.format == format
```

---

## 6. CI/CD 集成

### 6.1 GitHub Actions 工作流

创建 `.github/workflows/test.yml`：

```yaml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Lint with flake8
      run: |
        flake8 packages tests --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 packages tests --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics

    - name: Type check with mypy
      run: mypy packages

    - name: Run tests with pytest
      run: |
        pytest --cov=packages --cov-report=xml --cov-report=html --cov-report=term

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

    - name: Archive coverage reports
      uses: actions/upload-artifact@v3
      with:
        name: coverage-report-${{ matrix.os }}-${{ matrix.python-version }}
        path: htmlcov/
```

### 6.2 测试报告生成

#### pytest-html 插件

```bash
pip install pytest-html
```

```bash
pytest --html=report.html --self-contained-html
```

#### allure 报告

```bash
pip install allure-pytest

pytest --alluredir=allure-results
allure generate allure-results -o allure-report
```

### 6.3 覆盖率报告

```bash
# 生成覆盖率报告
pytest --cov=packages --cov-report=html --cov-report=term

# 查看覆盖率阈值
pytest --cov=packages --cov-fail-under=80
```

### 6.4 测试失败处理

```python
# conftest.py

def pytest_configure(config):
    """配置 pytest"""
    marker_map = {
        "slow": "标记慢速测试",
        "network": "需要网络连接",
        "browser": "需要浏览器",
    }

    for marker, description in marker_map.items():
        config.addinivalue_line("markers", f"{marker}: {description}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """在每个测试执行后生成报告"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # 记录测试失败信息
        if report.failed:
            print(f"\n❌ 测试失败: {item.nodeid}")
            print(f"   位置: {item.location}")
        else:
            print(f"✅ 测试通过: {item.nodeid}")
```

---

## 7. 测试示例

### 7.1 单元测试完整示例

```python
"""
test_css_extractor.py
测试 CSS 提取器的单元测试
"""
import pytest
from packages.extractors.css_extractor import CSSExtractor
from packages.extractors.exceptions import ExtractionError


class TestCSSExtractorInit:
    """测试 CSSExtractor 初始化"""

    def test_init_with_valid_selectors(self):
        """测试使用有效的选择器初始化"""
        extractor = CSSExtractor(
            title="h1",
            content="article p",
            metadata=".metadata"
        )
        assert extractor.title_selector == "h1"
        assert extractor.content_selector == "article p"

    def test_init_with_empty_selector(self):
        """测试空选择器"""
        extractor = CSSExtractor(title="")
        assert extractor.title_selector == ""

    def test_init_with_invalid_type(self):
        """测试无效类型"""
        with pytest.raises(TypeError):
            CSSExtractor(title=123)


class TestCSSExtractorExtract:
    """测试 CSSExtractor 提取功能"""

    @pytest.fixture
    def sample_html(self):
        """提供示例 HTML"""
        return """
        <html>
            <body>
                <h1>Main Title</h1>
                <article>
                    <p>First paragraph</p>
                    <p>Second paragraph</p>
                </article>
                <div class="metadata">
                    <span class="author">Author Name</span>
                    <time>2024-12-25</time>
                </div>
            </body>
        </html>
        """

    @pytest.fixture
    def extractor(self):
        """提供提取器实例"""
        return CSSExtractor(
            title="h1",
            content="article p",
            metadata=".metadata"
        )

    def test_extract_title_successfully(self, sample_html, extractor):
        """Given: 包含标题的 HTML
        When: 提取标题
        Then: 返回正确的标题文本
        """
        result = extractor.extract(sample_html)

        assert result.title == "Main Title"

    def test_extract_content_as_list(self, sample_html, extractor):
        """Given: 包含多个段落的 HTML
        When: 提取内容
        Then: 返回段落列表
        """
        result = extractor.extract(sample_html)

        assert len(result.content) == 2
        assert result.content[0] == "First paragraph"
        assert result.content[1] == "Second paragraph"

    def test_extract_metadata(self, sample_html, extractor):
        """Given: 包含元数据的 HTML
        When: 提取元数据
        Then: 返回元数据字典
        """
        result = extractor.extract(sample_html)

        assert result.metadata is not None
        assert "author" in result.metadata
        assert result.metadata["author"] == "Author Name"

    def test_extract_with_empty_html(self, extractor):
        """Given: 空 HTML 字符串
        When: 执行提取
        Then: 抛出 ExtractionError
        """
        with pytest.raises(ExtractionError):
            extractor.extract("")

    def test_extract_with_no_matching_elements(self):
        """Given: 没有匹配元素的 HTML
        When: 执行提取
        Then: 返回空结果
        """
        html = "<html><body><p>No title here</p></body></html>"
        extractor = CSSExtractor(title="h1")

        result = extractor.extract(html)

        assert result.title is None

    @pytest.mark.parametrize("html,expected_title", [
        ("<h1>Title1</h1>", "Title1"),
        ("<h1>Title2</h1>", "Title2"),
        ("<h1>  Title3  </h1>", "Title3"),  # 去除空格
    ])
    def test_extract_various_titles(self, html, expected_title):
        """参数化测试各种标题"""
        extractor = CSSExtractor(title="h1")
        result = extractor.extract(html)

        assert result.title == expected_title


class TestCSSExtractorEdgeCases:
    """测试边界情况"""

    def test_extract_with_malformed_html(self):
        """测试格式错误的 HTML"""
        malformed_html = "<h1>Title</p><div>Content</div>"
        extractor = CSSExtractor(title="h1", content="div")

        result = extractor.extract(malformed_html)

        assert result.title == "Title"
        assert result.content == ["Content"]

    def test_extract_with_unicode_content(self):
        """测试 Unicode 内容"""
        html = "<h1>你好世界 🌍</h1><p>测试内容</p>"
        extractor = CSSExtractor(title="h1", content="p")

        result = extractor.extract(html)

        assert result.title == "你好世界 🌍"
        assert result.content == ["测试内容"]

    def test_extract_with_nested_elements(self):
        """测试嵌套元素"""
        html = """
        <article>
            <div>
                <p>Nested paragraph 1</p>
            </div>
            <p>Nested paragraph 2</p>
        </article>
        """
        extractor = CSSExtractor(content="article p")

        result = extractor.extract(html)

        assert len(result.content) == 2
```

### 7.2 异步测试示例

```python
"""
test_async_crawler.py
测试异步爬虫
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from packages.crawler.async_crawler import AsyncCrawler
from packages.crawler.models import CrawlResult


@pytest.mark.asyncio
class TestAsyncCrawlerBasic:
    """测试异步爬虫基础功能"""

    async def test_crawl_single_url(self):
        """测试爬取单个 URL"""
        crawler = AsyncCrawler()

        with patch.object(crawler, '_fetch', return_value="<html>Test</html>"):
            result = await crawler.crawl("https://example.com")

            assert result.success
            assert result.url == "https://example.com"
            assert result.content == "<html>Test</html>"

    async def test_crawl_with_timeout(self):
        """测试超时处理"""
        crawler = AsyncCrawler(timeout=0.1)

        async def slow_fetch(*args, **kwargs):
            await asyncio.sleep(1)
            return "<html>Slow</html>"

        with patch.object(crawler, '_fetch', side_effect=slow_fetch):
            with pytest.raises(asyncio.TimeoutError):
                await crawler.crawl("https://slow-site.com")

    async def test_crawl_with_retry(self):
        """测试重试机制"""
        crawler = AsyncCrawler(max_retries=3)
        call_count = 0

        async def flaky_fetch(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Network error")
            return "<html>Success</html>"

        with patch.object(crawler, '_fetch', side_effect=flaky_fetch):
            result = await crawler.crawl("https://flaky-site.com")

            assert result.success
            assert call_count == 3


@pytest.mark.asyncio
class TestAsyncCrawlerBatch:
    """测试批量异步爬取"""

    async def test_crawl_multiple_urls(self):
        """测试爬取多个 URL"""
        crawler = AsyncCrawler(max_concurrency=3)
        urls = [
            "https://site1.com",
            "https://site2.com",
            "https://site3.com"
        ]

        async def mock_fetch(url):
            return f"<html>{url}</html>"

        with patch.object(crawler, '_fetch', side_effect=mock_fetch):
            results = await crawler.crawl_batch(urls)

            assert len(results) == 3
            assert all(r.success for r in results)
            assert results[0].url == urls[0]

    async def test_crawl_batch_with_partial_failures(self):
        """测试批量爬取部分失败"""
        crawler = AsyncCrawler()
        urls = ["https://success.com", "https://fail.com", "https://success2.com"]

        async def selective_fetch(url):
            if "fail" in url:
                raise ConnectionError("Failed")
            return f"<html>{url}</html>"

        with patch.object(crawler, '_fetch', side_effect=selective_fetch):
            results = await crawler.crawl_batch(urls)

            assert len(results) == 3
            assert results[0].success
            assert not results[1].success
            assert results[2].success


@pytest.mark.asyncio
@pytest.mark.slow
class TestAsyncCrawlerRealWorld:
    """真实世界的异步爬虫测试（慢速）"""

    async def test_crawl_with_rate_limiting(self):
        """测试速率限制"""
        crawler = AsyncCrawler(rate_limit=2)  # 每秒 2 个请求
        urls = [f"https://example.com/page{i}" for i in range(5)]

        start_time = asyncio.get_event_loop().time()

        with patch.object(crawler, '_fetch', return_value="<html>Test</html>"):
            await crawler.crawl_batch(urls)

        elapsed = asyncio.get_event_loop().time() - start_time
        assert elapsed >= 2.0  # 至少需要 2 秒
```

### 7.3 Mock 使用示例

```python
"""
test_http_client.py
测试 HTTP 客户端（包含各种 Mock 场景）
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from packages.crawler.http_client import HttpClient
from packages.crawler.exceptions import HttpError


class TestHttpClientWithMock:
    """使用 Mock 测试 HTTP 客户端"""

    def test_get_request_success(self):
        """测试成功的 GET 请求"""
        client = HttpClient()

        # 创建 mock 响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>Success</html>"
        mock_response.json.return_value = {"status": "ok"}

        # 使用 patch 替换 requests.get
        with patch('requests.get', return_value=mock_response) as mock_get:
            result = client.get("https://example.com")

            # 验证调用
            mock_get.assert_called_once_with(
                "https://example.com",
                headers=None,
                timeout=30
            )

            # 验证结果
            assert result.status_code == 200
            assert result.text == "<html>Success</html>"

    def test_post_request_with_data(self):
        """测试 POST 请求"""
        client = HttpClient()

        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 123}

        with patch('requests.post', return_value=mock_response) as mock_post:
            result = client.post(
                "https://api.example.com/data",
                json={"name": "test"}
            )

            mock_post.assert_called_once()
            assert result.status_code == 201
            assert result.json()["id"] == 123

    def test_request_with_retry_logic(self):
        """测试重试逻辑"""
        client = HttpClient(max_retries=3)

        # 第一次失败，第二次成功
        fail_response = Mock()
        fail_response.status_code = 500

        success_response = Mock()
        success_response.status_code = 200
        success_response.text = "<html>Success</html>"

        with patch('requests.get', side_effect=[fail_response, success_response]):
            result = client.get("https://flaky.com")

            assert result.status_code == 200
            assert requests.get.call_count == 2

    def test_request_timeout(self):
        """测试请求超时"""
        client = HttpClient(timeout=1)

        with patch('requests.get', side_effect=pytest.raises(TimeoutError)):
            with pytest.raises(HttpError):
                client.get("https://slow-server.com")

    def test_request_with_headers(self):
        """测试带自定义头的请求"""
        client = HttpClient()
        custom_headers = {
            "User-Agent": "TestAgent/1.0",
            "Authorization": "Bearer token123"
        }

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "OK"

        with patch('requests.get', return_value=mock_response) as mock_get:
            result = client.get(
                "https://api.example.com",
                headers=custom_headers
            )

            # 验证请求头
            call_kwargs = mock_get.call_args[1]
            assert call_kwargs['headers'] == custom_headers

            assert result.status_code == 200


class TestHttpClientWithPatchObject:
    """使用 patch.object 进行局部 mock"""

    def test_session_reuse(self):
        """测试会话重用"""
        client = HttpClient()

        mock_session = MagicMock()
        mock_session.get.return_value = Mock(status_code=200, text="OK")

        with patch.object(client, 'session', mock_session):
            client.get("https://example.com")
            client.get("https://example.org")

            # 验证使用同一个 session
            assert mock_session.get.call_count == 2

    def test_session_close_on_cleanup(self):
        """测试清理时关闭会话"""
        client = HttpClient()

        mock_session = MagicMock()

        with patch.object(client, 'session', mock_session):
            client.close()

            mock_session.close.assert_called_once()
```

### 7.4 Fixture 示例

```python
"""
conftest.py
全局 fixtures 配置
"""
import pytest
import asyncio
from pathlib import Path
from packages.crawler import WebCrawler, AsyncCrawler
from packages.extractors import CSSExtractor, XPathExtractor


# ==================== 爬虫 Fixtures ====================

@pytest.fixture
def crawler():
    """同步爬虫实例"""
    crawler = WebCrawler()
    yield crawler
    crawler.close()


@pytest.fixture
async def async_crawler():
    """异步爬虫实例"""
    crawler = AsyncCrawler()
    yield crawler
    await crawler.close()


# ==================== 提取器 Fixtures ====================

@pytest.fixture
def css_extractor():
    """CSS 提取器"""
    return CSSExtractor(
        title="h1",
        content="article p",
        metadata=".metadata"
    )


@pytest.fixture
def xpath_extractor():
    """XPath 提取器"""
    return XPathExtractor(
        title="//h1",
        content="//article//p",
        metadata="//div[@class='metadata']"
    )


# ==================== 测试数据 Fixtures ====================

@pytest.fixture
def test_html_dir():
    """测试 HTML 文件目录"""
    return Path(__file__).parent / "data" / "html"


@pytest.fixture
def sample_html_file(test_html_dir):
    """提供示例 HTML 文件路径"""
    return test_html_dir / "sample.html"


@pytest.fixture
def simple_html():
    """简单的 HTML 内容"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <h1>Main Title</h1>
        <article>
            <p>First paragraph</p>
            <p>Second paragraph</p>
        </article>
    </body>
    </html>
    """


@pytest.fixture
def complex_html():
    """复杂的 HTML 内容"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Complex Page</title>
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="/home">Home</a></li>
                    <li><a href="/about">About</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <article class="post">
                <h1>Article Title</h1>
                <div class="metadata">
                    <span class="author">John Doe</span>
                    <time datetime="2024-12-25">2024-12-25</time>
                </div>
                <div class="content">
                    <p>Paragraph 1</p>
                    <p>Paragraph 2</p>
                    <blockquote>Quote</blockquote>
                    <p>Paragraph 3</p>
                </div>
            </article>
        </main>
        <footer>
            <p>Copyright 2024</p>
        </footer>
    </body>
    </html>
    """


@pytest.fixture
def various_urls():
    """各种测试 URL"""
    return [
        "https://example.com",
        "https://example.org",
        "https://example.net",
        "http://httpbin.org/html",
    ]


# ==================== Mock Fixtures ====================

@pytest.fixture
def mock_response():
    """创建 mock 响应的工厂函数"""
    def _create_response(status_code, text, json_data=None):
        mock = Mock()
        mock.status_code = status_code
        mock.text = text
        mock.ok = status_code < 400
        if json_data:
            mock.json.return_value = json_data
        return mock
    return _create_response


@pytest.fixture
def mock_http_response():
    """预配置的 mock 响应"""
    mock = Mock()
    mock.status_code = 200
    mock.text = "<html><body>Test</body></html>"
    mock.ok = True
    mock.json.return_value = {"status": "success"}
    return mock


# ==================== 事件循环 Fixtures ====================

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ==================== 数据库 Fixtures ====================

@pytest.fixture(scope="session")
def test_database():
    """测试数据库连接"""
    from packages.crawler.database import Database

    db = Database.connect(":memory:")
    yield db
    db.close()


@pytest.fixture
def clean_db(test_database):
    """清空数据库的 fixture"""
    test_database.delete_all()
    yield test_database


# ==================== 测试服务器 Fixtures ====================

@pytest.fixture(scope="session")
def test_server_url():
    """测试服务器 URL（需要单独实现）"""
    return "http://localhost:8765"


# ==================== 参数化 Fixtures ====================

@pytest.fixture(params=["markdown", "html", "json"])
def output_format(request):
    """参数化的输出格式"""
    return request.param


@pytest.fixture(params=[10, 50, 100, 500])
def batch_size(request):
    """参数化的批次大小"""
    return request.param
```

### 7.5 集成测试示例

```python
"""
test_crawler_extractor_integration.py
爬虫与提取器集成测试
"""
import pytest
from packages.crawler import WebCrawler
from packages.extractors import CSSExtractor
from packages.processors import MarkdownProcessor


@pytest.mark.integration
class TestCrawlerExtractorIntegration:
    """爬虫和提取器集成测试"""

    def test_crawl_and_extract(self, crawler, css_extractor, sample_html_file):
        """测试爬取并提取数据"""
        # 使用测试服务器
        url = "http://localhost:8765/test.html"

        # 爬取网页
        crawl_result = crawler.crawl(url)

        assert crawl_result.success
        assert crawl_result.html is not None

        # 提取数据
        extract_result = css_extractor.extract(crawl_result.html)

        assert extract_result.title is not None
        assert len(extract_result.content) > 0

    def test_full_pipeline(self, crawler, css_extractor):
        """测试完整的数据处理管道"""
        url = "http://localhost:8765/complex.html"

        # 爬取
        crawl_result = crawler.crawl(url)
        assert crawl_result.success

        # 提取
        extract_result = css_extractor.extract(crawl_result.html)
        assert extract_result.title

        # 处理为 Markdown
        processor = MarkdownProcessor()
        markdown = processor.process(
            title=extract_result.title,
            content=extract_result.content
        )

        assert f"# {extract_result.title}" in markdown
        assert len(markdown) > 0


@pytest.mark.integration
@pytest.mark.asyncio
class TestAsyncIntegration:
    """异步集成测试"""

    async def test_async_crawl_and_extract(self, async_crawler, css_extractor):
        """测试异步爬取和提取"""
        url = "http://localhost:8765/async-test.html"

        # 异步爬取
        crawl_result = await async_crawler.crawl(url)
        assert crawl_result.success

        # 提取（同步操作）
        extract_result = css_extractor.extract(crawl_result.html)
        assert extract_result.title

    async def test_batch_crawl_and_extract(self, async_crawler, css_extractor):
        """测试批量爬取和提取"""
        urls = [
            "http://localhost:8765/page1.html",
            "http://localhost:8765/page2.html",
            "http://localhost:8765/page3.html",
        ]

        # 批量爬取
        crawl_results = await async_crawler.crawl_batch(urls)
        assert len(crawl_results) == 3
        assert all(r.success for r in crawl_results)

        # 提取所有结果
        extracted_data = []
        for result in crawl_results:
            extracted = css_extractor.extract(result.html)
            extracted_data.append(extracted)

        assert len(extracted_data) == 3
        assert all(d.title for d in extracted_data)
```

---

## 8. 测试工具和命令

### 8.1 常用 pytest 命令

```bash
# 基础运行
pytest                              # 运行所有测试
pytest tests/unit/                  # 运行特定目录
pytest test_crawler.py              # 运行特定文件
pytest test_crawler.py::TestClass   # 运行特定类
pytest test_crawler.py::test_func   # 运行特定测试

# 显示详细输出
pytest -v                           # 详细模式
pytest -vv                          # 更详细（包含 print 输出）
pytest -s                           # 不捕获输出

# 运行失败的测试
pytest --lf                         # 只运行上次失败的测试
pytest --ff                         # 先运行失败的测试

# 覆盖率
pytest --cov=packages               # 显示覆盖率
pytest --cov=packages --cov-report=html  # 生成 HTML 报告
pytest --cov-fail-under=80          # 覆盖率低于 80% 则失败

# 并行运行
pytest -n auto                      # 使用所有 CPU
pytest -n 4                         # 使用 4 个进程

# 标记
pytest -m "not slow"                # 排除慢速测试
pytest -m "integration"             # 只运行集成测试
pytest -m "network and not browser" # 组合标记

# 调试
pytest --pdb                        # 失败时进入调试器
pytest --trace                      # 每个测试后进入调试器
pytest -l                           # 显示局部变量
```

### 8.2 测试开发工作流

```bash
# 开发新功能时
1. 编写测试
2. 运行测试: pytest tests/unit/test_new_feature.py -v
3. 编写实现代码
4. 重新运行: pytest tests/unit/test_new_feature.py -v
5. 检查覆盖率: pytest --cov=packages/new_module

# 提交前检查
1. 运行所有测试: pytest
2. 检查覆盖率: pytest --cov=packages --cov-report=html
3. 代码格式化: black . && isort .
4. 类型检查: mypy packages
5. Linting: flake8 packages tests
```

### 8.3 pytest 插件推荐

```bash
# 核心插件
pytest-asyncio          # 异步测试支持
pytest-cov              # 覆盖率
pytest-xdist            # 并行测试
pytest-mock             # Mock 支持
pytest-html             # HTML 报告
pytest-timeout          # 超时控制

# 高级插件
pytest-benchmark        # 性能测试
pytest-randomly         # 随机化测试顺序
pytest-rerunfailures    # 失败重试
pytest-env              # 环境变量管理
pytest-django           # Django 集成
pytest-asyncio          # 异步测试
```

### 8.4 代码模板

#### 测试文件模板

```python
"""
test_<module_name>.py
<简短描述>
"""
import pytest
from packages.<module_name> import <ClassName>


class Test<ClassName>:
    """测试 <ClassName>"""

    @pytest.fixture
    def instance(self):
        """提供测试实例"""
        return <ClassName>()

    def test_<scenario>_when_<condition>_then_<expected_result>(self, instance):
        """测试场景描述"""
        # Given
        input_data = ...

        # When
        result = instance.method(input_data)

        # Then
        assert result == expected_output
```

#### conftest.py 模板

```python
"""
conftest.py
全局测试配置和 fixtures
"""
import pytest
from packages.crawler import WebCrawler


@pytest.fixture(scope="session")
def global_config():
    """全局配置"""
    return {
        "timeout": 30,
        "max_retries": 3,
    }


def pytest_configure(config):
    """pytest 配置钩子"""
    config.addinivalue_line("markers", "slow: 标记慢速测试")
    config.addinivalue_line("markers", "integration: 集成测试")
    config.addinivalue_line("markers", "network: 需要网络")


@pytest.fixture(autouse=True)
def reset_state():
    """每个测试前重置状态"""
    yield
    # 清理代码
```

---

## 附录

### A. 测试检查清单

在提交代码前，确保：

- [ ] 所有测试通过（`pytest`）
- [ ] 覆盖率达到要求（`pytest --cov`）
- [ ] 代码通过格式检查（`black`, `isort`）
- [ ] 类型检查通过（`mypy`）
- [ ] Linting 通过（`flake8`）
- [ ] 添加了必要的测试文档
- [ ] 测试命名清晰、具有描述性
- [ ] 异步代码使用了 `@pytest.mark.asyncio`
- [ ] Mock 使用正确
- [ ] Fixture 作用域合理

### B. 常见问题

**Q: 如何测试私有方法？**
A: 通过公共接口测试，不应直接测试私有方法。如果必须测试，考虑将其设为 protected 或重构代码。

**Q: Mock 太多怎么办？**
A: 如果 Mock 太多，可能说明代码设计有问题。考虑：
- 提取接口
- 使用依赖注入
- 改进代码结构

**Q: 如何测试随机性？**
A: 使用固定的种子：
```python
import random
random.seed(42)
```

**Q: 异步测试很慢怎么办？**
A: 使用 Mock 或 fixture 避免真实 I/O：
```python
@pytest.mark.asyncio
async def test_with_mock():
    with patch('asyncio.sleep', return_value=AsyncMock()):
        # 测试代码
```

### C. 参考资料

- [pytest 官方文档](https://docs.pytest.org/)
- [pytest-asyncio 文档](https://pytest-asyncio.readthedocs.io/)
- [unittest.mock 文档](https://docs.python.org/3/library/unittest.mock.html)
- [Python 测试最佳实践](https://docs.python-guide.org/writing/tests/)

---

**最后更新**：2024-12-25
**维护者**：Awesome-crawl4AI Team
**反馈**：请在 GitHub Issues 提出问题和建议
