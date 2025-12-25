# Awesome-crawl4AI 场景开发指南

艹，这是完整的场景开发教程，跟着Kevin一步步来！

---

## 目录 / Table of Contents

- [什么是场景 / What is a Scenario](#什么是场景)
- [两种创建方式 / Two Creation Methods](#两种创建方式)
- [方式一：可视化编辑器 / Method 1: Visual Editor](#方式一可视化编辑器)
- [方式二：代码开发 / Method 2: Code Development](#方式二代码开发)
- [场景示例 / Scenario Examples](#场景示例)
- [最佳实践 / Best Practices](#最佳实践)

---

## 什么是场景 / What is a Scenario

**场景（Scenario）** 是针对特定网站类型或数据提取需求设计的预配置模板。

**A Scenario** is a pre-configured template designed for specific website types or data extraction needs.

### 内置场景 / Built-in Scenarios

| 场景名称 | 分类 | 用途 |
|---------|------|------|
| `NewsCrawler` | news | 新闻文章爬取 |
| `DocsArchiver` | docs | 技术文档归档 |
| `EcommerceMonitor` | ecommerce | 电商价格监控 |
| `AcademicCollector` | academic | 学术论文收集 |
| `TableExtractor` | table | 表格数据提取 |

---

## 两种创建方式 / Two Creation Methods

### 🎨 方式一：可视化编辑器 / Method 1: Visual Editor（推荐）

**适合：** 快速创建简单场景，无需编程
**Suitable for:** Quick creation of simple scenarios, no coding required

### 💻 方式二：代码开发 / Method 2: Code Development

**适合：** 复杂场景，需要自定义逻辑
**Suitable for:** Complex scenarios requiring custom logic

---

## 方式一：可视化编辑器 / Method 1: Visual Editor

### 步骤 1：打开模板编辑器

1. 访问 `http://localhost:8000`
2. 点击左侧菜单 **「场景模板」**
3. 点击右上角 **「+ 新建模板」**

### 步骤 2：填写基本信息

**必填字段 / Required Fields：**

| 字段 | 说明 | 示例 |
|------|------|------|
| 模板名称 | 唯一标识符 | `blog_crawler` |
| 描述 | 模板用途说明 | `博客文章爬取 - 提取标题、内容、标签` |
| 分类 | 选择分类 | `custom` |

### 步骤 3：添加提取字段

点击 **「+ 添加字段」**，填写每个字段的配置：

**字段配置示例 / Field Configuration Example：**

```
字段1：标题
- 名称：title
- CSS选择器：h1, .post-title, [itemprop='headline']
- 类型：text
- 必填：✅

字段2：内容
- 名称：content
- CSS选择器：article .content, .post-body
- 类型：text
- 必填：✅

字段3：标签
- 名称：tags
- CSS选择器：.tags a, .post-tags li
- 类型：text
- 多值：✅
```

### 步骤 4：高级配置（可选）

展开 **「高级配置」** 设置：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| 请求延迟 | 0.5秒 | 两次请求之间的间隔（礼貌爬取） |
| 深度爬取 | false | 是否爬取链接页面 |
| 最大页面数 | 50 | 深度爬取时的页面限制 |
| 爬取策略 | bfs | BFS（广度优先）或 DFS（深度优先） |
| 滚动加载 | false | 是否滚动页面加载更多内容 |
| 最大滚动次数 | 5 | 滚动次数限制 |

### 步骤 5：验证并保存

1. 点击 **「验证」** 按钮检查配置
2. 验证通过后点击 **「保存」**

### 使用新创建的模板

在 **Dashboard** 或 **场景模板** 页面：
1. 找到你创建的模板
2. 点击 **「应用」**
3. 输入目标URL
4. 开始爬取！

---

## 方式二：代码开发 / Method 2: Code Development

### 完整代码示例 / Complete Code Example

```python
"""
博客爬取场景
Blog Crawler Scenario

专门用于个人博客文章的提取
Specialized for personal blog post extraction
"""

from typing import Any
from .base import BaseScenario
from ..core.template_engine import TemplateConfigSchema, ExtractField, AdvancedConfig


class BlogCrawler(BaseScenario):
    """
    博客爬取场景
    Blog Crawler Scenario

    艹，提取博客文章的标题、内容、作者、发布日期和标签！
    """

    def get_schema(self) -> TemplateConfigSchema:
        """获取博客爬取配置Schema"""
        return TemplateConfigSchema(
            name="blog_crawler",
            description="博客爬取 - 提取博客文章的标题、内容、作者、发布日期和标签",
            category="custom",  # 自定义分类
            fields=[
                # 艹，标题字段 - 支持多种选择器
                ExtractField(
                    name="title",
                    selector="h1, .post-title, .entry-title, [itemprop*='headline']",
                    type="text",
                    required=True,
                ),
                # 艹，内容字段 - 优先article标签
                ExtractField(
                    name="content",
                    selector="article .content, .post-body, .entry-content",
                    type="text",
                    required=True,
                ),
                # 艹，作者字段
                ExtractField(
                    name="author",
                    selector=".author, .post-author, [itemprop*='author']",
                    type="text",
                ),
                # 艹，发布日期
                ExtractField(
                    name="publish_date",
                    selector="time, .date, .publish-date, [itemprop*='datePublished']",
                    type="text",
                ),
                # 艹，标签 - 多值字段
                ExtractField(
                    name="tags",
                    selector=".tags a, .post-tags li, [rel*='tag']",
                    type="text",
                    multiple=True,
                ),
            ],
            advanced=AdvancedConfig(
                delay=1.0,  # 艹，博客网站友好，延迟1秒
                deep_crawl=False,  # 不需要深度爬取
            ),
        )

    async def extract(self, url: str, crawler) -> dict[str, Any]:
        """
        执行博客爬取

        Args:
            url: 博客文章URL
            crawler: Crawl4AI封装实例

        Returns:
            dict: 提取结果
        """
        # 艹，使用默认配置
        result = await crawler.crawl(url)

        if not result.get("success"):
            return result

        # TODO: 在这里添加自定义处理逻辑
        # 例如：清理Markdown格式、提取图片等

        return result


# 艹，自动注册到场景注册表！
from ..core.scenario_registry import register_scenario
register_scenario(BlogCrawler)
```

### 代码结构说明 / Code Structure Explanation

#### 1. 导入依赖 / Import Dependencies

```python
from typing import Any
from .base import BaseScenario  # 艹，所有场景必须继承BaseScenario
from ..core.template_engine import TemplateConfigSchema, ExtractField, AdvancedConfig
```

#### 2. 定义场景类 / Define Scenario Class

```python
class BlogCrawler(BaseScenario):
    """类名要清晰表达用途 / Class name should clearly express purpose"""
```

#### 3. 实现 get_schema() / Implement get_schema()

```python
def get_schema(self) -> TemplateConfigSchema:
    """返回场景配置Schema / Return scenario configuration schema"""
    return TemplateConfigSchema(
        name="blog_crawler",          # 唯一名称 / Unique name
        description="博客爬取",        # 描述 / Description
        category="custom",            # 分类 / Category
        fields=[...],                 # 提取字段 / Extract fields
        advanced=AdvancedConfig(...)  # 高级配置 / Advanced config
    )
```

#### 4. 实现 extract() / Implement extract()

```python
async def extract(self, url: str, crawler) -> dict[str, Any]:
    """
    执行爬取的异步方法
    Async method to execute crawling

    Args:
        url: 目标URL / Target URL
        crawler: Crawl4AIWrapper实例 / Crawl4AIWrapper instance

    Returns:
        dict: 提取结果 / Extraction result
    """
    result = await crawler.crawl(url)
    return result
```

#### 5. 自动注册 / Auto Registration

```python
from ..core.scenario_registry import register_scenario
register_scenario(BlogCrawler)
```

### 放置文件位置 / File Placement

将文件保存到：`backend/scenarios/blog_crawler.py`

然后在 `backend/scenarios/__init__.py` 中导入：

```python
from .blog_crawler import BlogCrawler

__all__ = [
    # ... 其他场景
    "BlogCrawler",
]
```

### 重启服务生效 / Restart to Take Effect

```bash
# 停止服务 / Stop service
# Ctrl+C

# 重新启动 / Restart
cd backend
python -m uvicorn main:app --reload
```

---

## 场景示例 / Scenario Examples

### 示例1：社交媒体帖子 / Social Media Post

```python
class SocialMediaPost(BaseScenario):
    def get_schema(self) -> TemplateConfigSchema:
        return TemplateConfigSchema(
            name="social_media_post",
            description="社交媒体帖子提取",
            category="custom",
            fields=[
                ExtractField(
                    name="username",
                    selector=".username, .user-name, [data-user]",
                    type="text",
                    required=True,
                ),
                ExtractField(
                    name="post_content",
                    selector=".post-content, .tweet-text, .message",
                    type="text",
                    required=True,
                ),
                ExtractField(
                    name="likes",
                    selector=".likes-count, .like-count",
                    type="number",
                ),
                ExtractField(
                    name="comments",
                    selector=".comment .text",
                    type="text",
                    multiple=True,
                ),
                ExtractField(
                    name="images",
                    selector=".post-image img",
                    type="image",
                    multiple=True,
                ),
            ],
            advanced=AdvancedConfig(
                delay=2.0,  # 艹，社交媒体反爬严格
                scroll_to_load=True,
                max_scrolls=3,
            ),
        )
```

### 示例2：房产信息 / Real Estate Listing

```python
class RealEstateListing(BaseScenario):
    def get_schema(self) -> TemplateConfigSchema:
        return TemplateConfigSchema(
            name="real_estate_listing",
            description="房产信息提取",
            category="custom",
            fields=[
                ExtractField(
                    name="property_title",
                    selector="h1, .listing-title",
                    type="text",
                    required=True,
                ),
                ExtractField(
                    name="price",
                    selector=".price, .listing-price",
                    type="text",
                    required=True,
                ),
                ExtractField(
                    name="address",
                    selector=".address, .property-address",
                    type="text",
                ),
                ExtractField(
                    name="bedrooms",
                    selector=".bedrooms, .bd",
                    type="number",
                ),
                ExtractField(
                    name="bathrooms",
                    selector=".bathrooms, .ba",
                    type="number",
                ),
                ExtractField(
                    name="area",
                    selector=".area, .sqft",
                    type="number",
                ),
                ExtractField(
                    name="description",
                    selector=".description, .listing-desc",
                    type="text",
                ),
                ExtractField(
                    name="images",
                    selector=".gallery img, .property-image img",
                    type="image",
                    multiple=True,
                ),
            ],
        )
```

### 示例3：招聘信息 / Job Posting

```python
class JobPosting(BaseScenario):
    def get_schema(self) -> TemplateConfigSchema:
        return TemplateConfigSchema(
            name="job_posting",
            description="招聘信息提取",
            category="custom",
            fields=[
                ExtractField(
                    name="job_title",
                    selector="h1, .job-title",
                    type="text",
                    required=True,
                ),
                ExtractField(
                    name="company",
                    selector=".company-name, [itemprop='hiringOrganization']",
                    type="text",
                ),
                ExtractField(
                    name="location",
                    selector=".location, [itemprop='jobLocation']",
                    type="text",
                ),
                ExtractField(
                    name="salary",
                    selector=".salary, .compensation",
                    type="text",
                ),
                ExtractField(
                    name="description",
                    selector=".job-description, .description",
                    type="text",
                ),
                ExtractField(
                    name="requirements",
                    selector=".requirements li",
                    type="text",
                    multiple=True,
                ),
                ExtractField(
                    name="benefits",
                    selector=".benefits li",
                    type="text",
                    multiple=True,
                ),
            ],
        )
```

---

## 高级用法 / Advanced Usage

### 自定义数据处理 / Custom Data Processing

```python
async def extract(self, url: str, crawler) -> dict[str, Any]:
    """执行自定义数据处理"""
    result = await crawler.crawl(url)

    if not result.get("success"):
        return result

    # 艹，自定义处理：清理Markdown
    markdown = result.get("markdown", "")
    cleaned_markdown = self._clean_markdown(markdown)
    result["markdown"] = cleaned_markdown

    # 艹，提取所有图片链接
    images = result.get("media", {}).get("images", [])
    image_urls = [img.get("src") for img in images if img.get("src")]
    result["extracted_content"]["image_urls"] = image_urls

    return result

def _clean_markdown(self, markdown: str) -> str:
    """清理Markdown格式"""
    # 移除多余空行
    lines = [line for line in markdown.split("\n") if line.strip()]
    return "\n\n".join(lines)
```

### 使用深度爬取 / Using Deep Crawl

```python
async def extract(self, url: str, crawler) -> dict[str, Any]:
    """深度爬取整个文档网站"""
    result = await crawler.deep_crawl(
        url,
        strategy="bfs",  # BFS或DFS
        max_pages=100,   # 最多100页
        config={"bypass_cache": True},
    )
    return result
```

### 添加重试逻辑 / Add Retry Logic

```python
async def extract(self, url: str, crawler) -> dict[str, Any]:
    """带重试的爬取"""
    max_retries = 3
    for attempt in range(max_retries):
        result = await crawler.crawl(url)

        if result.get("success"):
            return result

        # 艹，最后一次尝试失败
        if attempt == max_retries - 1:
            result["error_message"] = f"重试{max_retries}次后仍失败"
            return result

        # 等待后重试
        await asyncio.sleep(2 ** attempt)  # 指数退避

    return {"success": False, "error_message": "未知错误"}
```

---

## 最佳实践 / Best Practices

### ✅ DO - 应该做的

1. **使用多个CSS选择器** - 提高兼容性
   ```python
   selector="h1, .title, [itemprop='headline']"
   ```

2. **设置合理的延迟** - 礼貌爬取
   ```python
   advanced=AdvancedConfig(delay=1.0)  # 至少1秒
   ```

3. **添加详细注释** - 方便后续维护
   ```python
   # 艹，标题字段 - 支持多种常见HTML结构
   ExtractField(name="title", selector="h1, .post-title")
   ```

4. **使用required标记** - 确保关键数据
   ```python
   ExtractField(name="title", required=True)
   ```

5. **测试多个网站** - 确保通用性

### ❌ DON'T - 不应该做的

1. **不要设置太短的延迟** - 会被封IP
   ```python
   # ❌ 错误 / Wrong
   advanced=AdvancedConfig(delay=0.1)

   # ✅ 正确 / Correct
   advanced=AdvancedConfig(delay=1.0)
   ```

2. **不要过度爬取** - 遵守robots.txt
   ```python
   # ❌ 错误 / Wrong
   max_pages=10000

   # ✅ 正确 / Correct
   max_pages=100
   ```

3. **不要忽略错误处理**
   ```python
   # ❌ 错误 / Wrong
   result = await crawler.crawl(url)
   return result

   # ✅ 正确 / Correct
   result = await crawler.crawl(url)
   if not result.get("success"):
       return {"success": False, "error": result.get("error")}
   return result
   ```

4. **不要使用过于具体的选择器**
   ```python
   # ❌ 错误 / Wrong
   selector="#post-12345 .title"  # 太具体

   # ✅ 正确 / Correct
   selector=".post-title, h1"  # 通用
   ```

---

## CSS选择器技巧 / CSS Selector Tips

### 基本选择器 / Basic Selectors

```css
/* 元素选择器 */
h1, p, div

/* 类选择器 */
.title, .content

/* ID选择器 */
#main-title

/* 属性选择器 */
[itemprop='headline']
[data-id]
```

### 组合选择器 / Combinators

```css
/* 后代选择器 */
article .content

/* 子选择器 */
article > .content

/* 多个选择器（或） */
h1, .title, [itemprop='headline']
```

### 伪类 / Pseudo-classes

```css
/* 第一个子元素 */
ul li:first-child

/* 最后一个子元素 */
ul li:last-child

/* 第N个子元素 */
ul li:nth-child(2)
```

---

## 调试技巧 / Debugging Tips

### 1. 使用浏览器开发者工具

1. 打开目标网页
2. 按 `F12` 打开开发者工具
3. 点击元素选择器（左上角箭头图标）
4. 点击页面元素查看其HTML结构
5. 右键 → Copy → Copy selector

### 2. 测试CSS选择器

在浏览器控制台运行：
```javascript
// 测试单个选择器
document.querySelector("h1")

// 测试多个选择器
document.querySelectorAll(".tags a")

// 查看元素内容
document.querySelector("h1").textContent
```

### 3. 查看爬取结果

```python
# 在extract方法中添加调试输出
import json

async def extract(self, url: str, crawler) -> dict[str, Any]:
    result = await crawler.crawl(url)

    # 艹，打印调试信息
    print("=" * 50)
    print(f"URL: {url}")
    print(f"Success: {result.get('success')}")
    print(f"Extracted: {json.dumps(result.get('extracted_content'), indent=2)}")
    print("=" * 50)

    return result
```

---

## 常见问题 / FAQ

### Q1: 为什么提取不到数据？

**A:** 可能的原因：
1. CSS选择器不正确 → 使用浏览器开发者工具验证
2. 页面是JavaScript动态渲染 → 启用 `scroll_to_load`
3. 网站有反爬机制 → 增加 `delay` 延迟

### Q2: 如何处理JavaScript渲染的页面？

**A:** Crawl4AI会自动处理，但可能需要滚动加载：
```python
advanced=AdvancedConfig(
    scroll_to_load=True,
    max_scrolls=5,
)
```

### Q3: 如何提取图片的alt属性？

**A:** 使用 `attribute` 类型并指定属性名：
```python
ExtractField(
    name="image_alt",
    selector=".main-image",
    type="attribute",
    attribute="alt",
)
```

### Q4: 可以爬取需要登录的网站吗？

**A:** 目前版本不支持，需要使用Crawl4AI的Session功能（高级用法）

### Q5: 如何避免被封IP？

**A:**
1. 设置合理的延迟（至少1秒）
2. 使用代理池（在AdvancedConfig中配置）
3. 遵守网站的robots.txt

---

艹，场景开发指南写完了！有问题找Kevin！

**文档版本 / Version：** 1.0.0
**最后更新 / Last Updated：** 2025-12-25
