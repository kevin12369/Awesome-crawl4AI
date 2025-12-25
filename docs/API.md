# Awesome-crawl4AI API 文档

艹，这是完整的API接口文档，看不懂就来问Kevin！

---

## 基础信息 / Base Information

**Base URL（开发环境）：**
```
http://localhost:8000
```

**Base URL（生产环境）：**
```
http://your-domain.com
```

**响应格式 / Response Format：**
所有接口返回 JSON 格式
All endpoints return JSON format

**通用响应结构 / Common Response Structure：**
```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

---

## 目录 / Table of Contents

- [爬取相关 API (Crawl)](#crawl-api)
- [模板相关 API (Templates)](#templates-api)
- [监控相关 API (Monitor)](#monitor-api)

---

## 1. Crawl API - 爬取相关接口 / Crawl Endpoints

### 1.1 创建爬取任务 / Create Crawl Task

创建单个URL的爬取任务
Create a crawl task for a single URL

**请求 / Request：**
```http
POST /api/crawl
Content-Type: application/json
```

**请求体 / Request Body：**
```json
{
  "url": "https://example.com",
  "template_id": "news_crawler",
  "config": {
    "word_count_threshold": 10,
    "bypass_cache": true,
    "delay": 1.0
  }
}
```

**参数说明 / Parameters：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | ✅ | 目标URL / Target URL |
| template_id | string | ❌ | 模板ID / Template ID (默认使用通用模板) |
| config | object | ❌ | Crawl4AI配置 / Crawl4AI config |

**config 可选参数 / config Optional Fields：**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| word_count_threshold | number | 10 | 字数阈值 / Word count threshold |
| bypass_cache | boolean | false | 绕过缓存 / Bypass cache |
| delay | number | 0.5 | 请求延迟（秒）/ Request delay (seconds) |
| scroll_to_load | boolean | false | 滚动加载 / Scroll to load |
| max_scrolls | number | 5 | 最大滚动次数 / Max scroll count |

**响应 / Response：**
```json
{
  "code": 200,
  "message": "任务创建成功",
  "data": {
    "id": 1,
    "url": "https://example.com",
    "template_id": "news_crawler",
    "status": "pending",
    "created_at": "2025-12-25T10:00:00Z"
  }
}
```

---

### 1.2 批量创建爬取任务 / Batch Create Crawl Tasks

批量创建多个URL的爬取任务
Create crawl tasks for multiple URLs

**请求 / Request：**
```http
POST /api/crawl/batch
Content-Type: application/json
```

**请求体 / Request Body：**
```json
{
  "urls": [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
  ],
  "template_id": "docs_archiver",
  "config": {
    "delay": 0.5
  }
}
```

**参数说明 / Parameters：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| urls | string[] | ✅ | URL列表 / URL list (最多100个 / max 100) |
| template_id | string | ❌ | 模板ID / Template ID |
| config | object | ❌ | Crawl4AI配置 / Crawl4AI config |

**响应 / Response：**
```json
{
  "code": 200,
  "message": "批量任务创建成功",
  "data": {
    "total": 3,
    "tasks": [
      {"id": 1, "url": "https://example.com/page1", "status": "pending"},
      {"id": 2, "url": "https://example.com/page2", "status": "pending"},
      {"id": 3, "url": "https://example.com/page3", "status": "pending"}
    ]
  }
}
```

---

### 1.3 深度爬取 / Deep Crawl

深度爬取整个网站（多页）
Deep crawl an entire website (multi-page)

**请求 / Request：**
```http
POST /api/crawl/deep
Content-Type: application/json
```

**请求体 / Request Body：**
```json
{
  "url": "https://docs.example.com",
  "strategy": "bfs",
  "max_pages": 50,
  "config": {
    "delay": 0.5,
    "bypass_cache": true
  }
}
```

**参数说明 / Parameters：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | ✅ | 起始URL / Starting URL |
| strategy | string | ❌ | 爬取策略：bfs/dfs (默认bfs) / Crawl strategy |
| max_pages | number | ❌ | 最大页面数 (默认50) / Max pages |
| config | object | ❌ | Crawl4AI配置 / Crawl4AI config |

**响应 / Response：**
```json
{
  "code": 200,
  "message": "深度爬取任务创建成功",
  "data": {
    "id": 1,
    "url": "https://docs.example.com",
    "strategy": "bfs",
    "max_pages": 50,
    "status": "pending",
    "created_at": "2025-12-25T10:00:00Z"
  }
}
```

---

### 1.4 获取任务列表 / Get Task List

获取爬取任务列表（支持分页和过滤）
Get list of crawl tasks (supports pagination and filtering)

**请求 / Request：**
```http
GET /api/crawl/tasks?page=1&page_size=20&status=completed
```

**参数说明 / Parameters：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | number | ❌ | 页码 (默认1) / Page number |
| page_size | number | ❌ | 每页数量 (默认20) / Items per page |
| status | string | ❌ | 状态过滤 / Status filter |
| template_id | string | ❌ | 模板过滤 / Template filter |

**status 可选值 / status Options：**
- `pending` - 待处理 / Pending
- `running` - 运行中 / Running
- `completed` - 已完成 / Completed
- `failed` - 失败 / Failed

**响应 / Response：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 100,
    "page": 1,
    "page_size": 20,
    "tasks": [
      {
        "id": 1,
        "url": "https://example.com",
        "template_id": "news_crawler",
        "status": "completed",
        "created_at": "2025-12-25T10:00:00Z",
        "completed_at": "2025-12-25T10:00:05Z"
      }
    ]
  }
}
```

---

### 1.5 获取任务详情 / Get Task Detail

获取单个任务的详细信息和结果
Get detailed information and result of a single task

**请求 / Request：**
```http
GET /api/crawl/tasks/1
```

**参数说明 / Parameters：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | ✅ | 任务ID / Task ID |

**响应 / Response：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "url": "https://example.com",
    "template_id": "news_crawler",
    "status": "completed",
    "config": {},
    "result": {
      "success": true,
      "markdown": "# Article Title\n\nContent here...",
      "extracted_content": {
        "title": "Article Title",
        "content": "Content here..."
      },
      "links": [
        {"url": "https://example.com/page2", "text": "Link Text"}
      ],
      "media": [],
      "metadata": {
        "title": "Page Title",
        "description": "Page description",
        "keywords": ["keyword1", "keyword2"]
      },
      "screenshot": "data:image/png;base64,..."
    },
    "error_message": null,
    "created_at": "2025-12-25T10:00:00Z",
    "completed_at": "2025-12-25T10:00:05Z"
  }
}
```

---

### 1.6 删除任务 / Delete Task

删除指定的爬取任务
Delete a specific crawl task

**请求 / Request：**
```http
DELETE /api/crawl/tasks/1
```

**参数说明 / Parameters：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | ✅ | 任务ID / Task ID |

**响应 / Response：**
```json
{
  "code": 200,
  "message": "任务删除成功",
  "data": null
}
```

---

## 2. Templates API - 模板相关接口 / Template Endpoints

### 2.1 获取模板列表 / Get Template List

获取所有可用的场景模板
Get all available scenario templates

**请求 / Request：**
```http
GET /api/templates?category=news
```

**参数说明 / Parameters：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category | string | ❌ | 分类过滤 / Category filter |
| is_builtin | boolean | ❌ | 是否内置 / Is builtin |

**category 可选值 / category Options：**
- `news` - 新闻 / News
- `docs` - 文档 / Documentation
- `ecommerce` - 电商 / E-commerce
- `academic` - 学术 / Academic
- `table` - 表格 / Table
- `custom` - 自定义 / Custom

**响应 / Response：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 5,
    "templates": [
      {
        "id": 1,
        "name": "news_crawler",
        "description": "新闻爬取 - 提取新闻文章的标题、内容、作者等信息",
        "category": "news",
        "config_schema": {
          "name": "news_crawler",
          "description": "新闻爬取",
          "category": "news",
          "fields": [
            {
              "name": "title",
              "selector": "h1",
              "type": "text",
              "required": true
            }
          ],
          "advanced": {
            "delay": 1.0,
            "deep_crawl": false
          }
        },
        "is_builtin": true,
        "created_at": "2025-12-25T10:00:00Z"
      }
    ]
  }
}
```

---

### 2.2 获取模板详情 / Get Template Detail

获取单个模板的详细配置
Get detailed configuration of a single template

**请求 / Request：**
```http
GET /api/templates/1
```

**参数说明 / Parameters：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | ✅ | 模板ID / Template ID |

**响应 / Response：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "name": "news_crawler",
    "description": "新闻爬取 - 提取新闻文章的标题、内容、作者等信息",
    "category": "news",
    "config_schema": {
      "name": "news_crawler",
      "description": "新闻爬取",
      "category": "news",
      "fields": [
        {
          "name": "title",
          "selector": "h1",
          "type": "text",
          "required": true,
          "multiple": false
        },
        {
          "name": "content",
          "selector": "article p",
          "type": "text",
          "required": true,
          "multiple": false
        }
      ],
      "advanced": {
        "delay": 1.0,
        "deep_crawl": false,
        "max_pages": 10,
        "strategy": "bfs"
      }
    },
    "is_builtin": true,
    "created_at": "2025-12-25T10:00:00Z",
    "updated_at": "2025-12-25T10:00:00Z"
  }
}
```

---

### 2.3 创建模板 / Create Template

创建自定义场景模板
Create a custom scenario template

**请求 / Request：**
```http
POST /api/templates
Content-Type: application/json
```

**请求体 / Request Body：**
```json
{
  "name": "my_custom_crawler",
  "description": "我的自定义爬虫",
  "category": "custom",
  "config_schema": {
    "name": "my_custom_crawler",
    "description": "我的自定义爬虫",
    "category": "custom",
    "fields": [
      {
        "name": "product_name",
        "selector": ".product-title",
        "type": "text",
        "required": true
      },
      {
        "name": "price",
        "selector": ".price",
        "type": "text",
        "required": true
      }
    ],
    "advanced": {
      "delay": 2.0,
      "deep_crawl": false
    }
  }
}
```

**参数说明 / Parameters：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✅ | 模板名称（唯一）/ Template name (unique) |
| description | string | ✅ | 模板描述 / Template description |
| category | string | ✅ | 模板分类 / Template category |
| config_schema | object | ✅ | 配置Schema / Config schema |

**config_schema.fields 字段说明 / config_schema.fields Specification：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✅ | 字段名 / Field name |
| selector | string | ✅ | CSS选择器 / CSS selector |
| type | string | ✅ | 字段类型 / Field type |
| required | boolean | ❌ | 是否必填 / Is required |
| multiple | boolean | ❌ | 是否多值 / Is multiple |

**type 可选值 / type Options：**
- `text` - 文本 / Text
- `number` - 数字 / Number
- `link` - 链接 / Link
- `image` - 图片 / Image
- `attribute` - 属性 / Attribute

**响应 / Response：**
```json
{
  "code": 200,
  "message": "模板创建成功",
  "data": {
    "id": 10,
    "name": "my_custom_crawler",
    "description": "我的自定义爬虫",
    "category": "custom",
    "is_builtin": false,
    "created_at": "2025-12-25T10:00:00Z"
  }
}
```

---

### 2.4 更新模板 / Update Template

更新自定义模板（内置模板不可修改）
Update a custom template (builtin templates cannot be modified)

**请求 / Request：**
```http
PUT /api/templates/10
Content-Type: application/json
```

**请求体 / Request Body：**
```json
{
  "name": "my_custom_crawler_v2",
  "description": "我的自定义爬虫 V2",
  "category": "custom",
  "config_schema": {
    "name": "my_custom_crawler_v2",
    "fields": []
  }
}
```

**参数说明 / Parameters：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | ✅ | 模板ID / Template ID |
| name | string | ❌ | 新模板名称 / New template name |
| description | string | ❌ | 新描述 / New description |
| category | string | ❌ | 新分类 / New category |
| config_schema | object | ❌ | 新配置 / New config |

**响应 / Response：**
```json
{
  "code": 200,
  "message": "模板更新成功",
  "data": {
    "id": 10,
    "name": "my_custom_crawler_v2",
    "updated_at": "2025-12-25T10:00:00Z"
  }
}
```

---

### 2.5 删除模板 / Delete Template

删除自定义模板（内置模板不可删除）
Delete a custom template (builtin templates cannot be deleted)

**请求 / Request：**
```http
DELETE /api/templates/10
```

**参数说明 / Parameters：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | ✅ | 模板ID / Template ID |

**响应 / Response：**
```json
{
  "code": 200,
  "message": "模板删除成功",
  "data": null
}
```

---

### 2.6 验证模板 / Validate Template

验证模板配置是否有效
Validate if a template configuration is valid

**请求 / Request：**
```http
POST /api/templates/validate
Content-Type: application/json
```

**请求体 / Request Body：**
```json
{
  "config_schema": {
    "name": "test_template",
    "fields": [
      {
        "name": "title",
        "selector": "h1",
        "type": "text"
      }
    ]
  }
}
```

**响应 / Response：**
```json
{
  "code": 200,
  "message": "验证通过",
  "data": {
    "valid": true,
    "errors": []
  }
}
```

**验证失败响应 / Validation Failed Response：**
```json
{
  "code": 400,
  "message": "验证失败",
  "data": {
    "valid": false,
    "errors": [
      "字段 'title' 缺少必需的 'selector' 属性"
    ]
  }
}
```

---

## 3. Monitor API - 监控相关接口 / Monitor Endpoints

### 3.1 健康检查 / Health Check

检查服务健康状态
Check service health status

**请求 / Request：**
```http
GET /api/health
```

**响应 / Response：**
```json
{
  "code": 200,
  "message": "healthy",
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "timestamp": "2025-12-25T10:00:00Z"
  }
}
```

---

### 3.2 获取统计信息 / Get Statistics

获取系统统计信息
Get system statistics

**请求 / Request：**
```http
GET /api/stats
```

**响应 / Response：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "tasks": {
      "total": 1000,
      "pending": 50,
      "running": 10,
      "completed": 900,
      "failed": 40
    },
    "templates": {
      "total": 15,
      "builtin": 5,
      "custom": 10
    },
    "urls_crawled": 50000,
    "success_rate": 0.96
  }
}
```

---

## 错误码 / Error Codes

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 / Success |
| 400 | 请求参数错误 / Bad request |
| 404 | 资源不存在 / Not found |
| 500 | 服务器内部错误 / Internal server error |

**错误响应格式 / Error Response Format：**
```json
{
  "code": 400,
  "message": "请求参数错误",
  "data": {
    "detail": "URL格式不正确"
  }
}
```

---

## 使用示例 / Usage Examples

### Python 示例 / Python Example

```python
import requests
import json

# 基础URL / Base URL
BASE_URL = "http://localhost:8000"

# 创建爬取任务 / Create crawl task
response = requests.post(
    f"{BASE_URL}/api/crawl",
    json={
        "url": "https://example.com",
        "template_id": "news_crawler"
    }
)
task = response.json()
print(f"任务ID: {task['data']['id']}")

# 获取任务结果 / Get task result
result = requests.get(f"{BASE_URL}/api/crawl/tasks/{task['data']['id']}")
print(json.dumps(result.json(), indent=2, ensure_ascii=False))
```

### JavaScript 示例 / JavaScript Example

```javascript
const BASE_URL = 'http://localhost:8000';

// 创建爬取任务 / Create crawl task
async function createCrawlTask(url) {
  const response = await fetch(`${BASE_URL}/api/crawl`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url: url,
      template_id: 'news_crawler'
    })
  });
  return await response.json();
}

// 获取任务列表 / Get task list
async function getTasks() {
  const response = await fetch(`${BASE_URL}/api/crawl/tasks`);
  return await response.json();
}
```

---

艹，文档写完了！有问题找Kevin！

**文档版本 / Version：** 1.0.0
**最后更新 / Last Updated：** 2025-12-25
