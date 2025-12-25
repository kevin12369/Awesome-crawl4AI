# Extractors 模块

[根目录](../../CLAUDE.md) > [packages](../) > **extractors**

---

## 模块职责

Extractors 模块负责从网页内容中提取结构化数据。它提供了多种提取策略，能够将原始 HTML 转换为 AI 友好的格式。

### 核心功能

- **HTML 解析**：使用 BeautifulSoup 和 lxml 解析 DOM
- **文本提取**：智能提取主要内容，去除噪音
- **结构化提取**：CSS 选择器、XPath、正则表达式
- **格式转换**：转 Markdown、JSON、CSV 等
- **AI 优化**：专门为 LLM 优化的输出格式
- **元数据提取**：作者、日期、标签等信息

## 入口和启动

### 主要文件结构

```
extractors/
├── __init__.py           # 包入口
├── base.py               # 提取器基类
├── html_extractor.py     # HTML 提取器
├── markdown_extractor.py # Markdown 转换器
├── json_extractor.py     # JSON 结构化提取
├── css_extractor.py      # CSS 选择器提取
├── xpath_extractor.py    # XPath 提取器
└── metadata.py           # 元数据提取
```

### 核心类设计

```python
class BaseExtractor:
    """提取器基类"""

    def extract(self, content: str, url: str = "") -> ExtractResult:
        """提取数据的抽象方法"""

    def validate(self) -> bool:
        """验证提取器配置"""
```

## 外部接口

### 基础使用

```python
from crawl4ai.extractors import HTMLExtractor, MarkdownExtractor

# HTML 提取
html_extractor = HTMLExtractor()
result = html_extractor.extract(html_content)
print(result.text)        # 提取的文本
print(result.markdown)    # Markdown 格式

# Markdown 转换
md_extractor = MarkdownExtractor()
result = md_extractor.extract(html_content)
print(result.markdown)
```

### CSS 选择器提取

```python
from crawl4ai.extractors import CSSExtractor

extractor = CSSExtractor({
    "title": "h1",
    "content": "article p",
    "author": ".author-name",
    "date": "time[datetime]"
})

result = extractor.extract(html_content)
print(result.data)  # {"title": "...", "content": [...], ...}
```

### JSON 结构化提取

```python
from crawl4ai.extractors import JSONExtractor

schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "selector": "h1"},
        "items": {
            "type": "array",
            "selector": "li",
            "properties": {
                "text": {"type": "string", "selector": "span"}
            }
        }
    }
}

extractor = JSONExtractor(schema)
result = extractor.extract(html_content)
print(result.json)  # JSON 字符串
```

## 关键依赖和配置

### 依赖项

- **beautifulsoup4**：HTML 解析
- **lxml**：高性能 XML/HTML 处理
- **markdownify**：HTML 转 Markdown
- **readability-lxml**（可选）：主要内容提取
- **pydantic**：数据验证

### 配置示例

```python
from crawl4ai.extractors import ExtractorConfig

config = ExtractorConfig(
    remove_scripts=True,
    remove_styles=True,
    simplify_html=True,
    extract_metadata=True,
    markdown_options={
        "heading_style": "ATX",
        "bullets": "*",
        "strip": ["script", "style"]
    }
)
```

## 数据模型

### ExtractResult

```python
class ExtractResult(BaseModel):
    """提取结果"""

    url: str                          # 来源 URL
    text: str                         # 纯文本内容
    markdown: str                     # Markdown 格式
    html: str                         # 清理后的 HTML
    data: Dict[str, Any]              # 结构化数据
    json: str                         # JSON 字符串
    metadata: Dict[str, Any]          # 元数据
    links: List[str] = []             # 提取的链接
    images: List[str] = []            # 提取的图片
    extraction_time: float = 0.0      # 提取耗时
```

### Metadata

```python
class WebMetadata(BaseModel):
    """网页元数据"""

    title: str = ""
    description: str = ""
    author: str = ""
    publish_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    tags: List[str] = []
    categories: List[str] = []
    language: str = ""
    canonical_url: str = ""
    og_type: str = ""
    og_image: str = ""
```

## 测试和质量

### 测试结构

```
tests/unit/extractors/
├── test_html_extractor.py
├── test_markdown_extractor.py
├── test_css_extractor.py
├── test_xpath_extractor.py
└── test_json_extractor.py
```

### 测试用例

- [ ] 基本 HTML 解析
- [ ] Markdown 转换准确性
- [ ] CSS 选择器匹配
- [ ] XPath 表达式
- [ ] 嵌套数据提取
- [ ] 元数据提取
- [ ] 链接和图片提取
- [ ] 特殊字符处理
- [ ] 编码问题处理

### 性能指标

- HTML 解析速度：> 100 pages/s
- Markdown 转换：< 10ms per page
- 内存占用：< 100MB for 1000 pages

## 常见问题 (FAQ)

### Q1: 如何提取 JavaScript 渲染的内容？
**A:** 需要配合 Crawler 模块的浏览器渲染功能，或者使用 API 端点。

### Q2: 如何处理复杂的嵌套结构？
**A:** 可以组合使用多个提取器，或定义嵌套的 JSON schema：
```python
schema = {
    "article": {
        "selector": "article",
        "properties": {
            "title": {"selector": "h1"},
            "comments": {
                "selector": ".comment",
                "properties": {
                    "user": ".user",
                    "text": ".text"
                }
            }
        }
    }
}
```

### Q3: 如何自定义提取逻辑？
**A:** 继承 BaseExtractor 并实现 extract 方法：
```python
class CustomExtractor(BaseExtractor):
    def extract(self, content, url=""):
        # 自定义提取逻辑
        return ExtractResult(...)
```

### Q4: 支持哪些 Markdown 格式？
**A:** 支持 CommonMark 和 GitHub Flavored Markdown，可配置标题样式、列表符号等。

## 相关文件列表

### 核心文件
- `packages/extractors/__init__.py`
- `packages/extractors/base.py`
- `packages/extractors/html_extractor.py`
- `packages/extractors/markdown_extractor.py`
- `packages/extractors/css_extractor.py`
- `packages/extractors/xpath_extractor.py`
- `packages/extractors/json_extractor.py`
- `packages/extractors/metadata.py`

### 测试文件
- `tests/unit/extractors/test_html_extractor.py`
- `tests/unit/extractors/test_markdown_extractor.py`
- `tests/unit/extractors/test_css_extractor.py`
- `tests/unit/extractors/test_json_extractor.py`
- `tests/integration/test_extraction_pipeline.py`

## 更改日志 (Change Log)

### 2025-12-25
- 初始化模块设计
- 定义提取器接口
- 规划数据模型和测试策略
