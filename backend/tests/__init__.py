"""
测试模块初始化
Test Module Initialization

艹，所有测试的公共东西都在这里！
"""

# 测试用的常量 / Test constants
TEST_URL = "https://example.com"
TEST_TEMPLATE_NAME = "test_template"
TEST_TEMPLATE_CATEGORY = "test"

# 测试用的Mock数据 / Test mock data
MOCK_CRAWL_RESULT = {
    "success": True,
    "url": TEST_URL,
    "markdown": "# Test Page\n\nThis is a test page.",
    "extracted_content": {
        "title": "Test Page",
        "content": "This is a test page.",
    },
    "links": [
        {"url": "https://example.com/page1", "text": "Page 1"},
        {"url": "https://example.com/page2", "text": "Page 2"},
    ],
    "media": [],
    "metadata": {
        "title": "Test Page",
        "description": "A test page",
    },
}

MOCK_TEMPLATE_DATA = {
    "name": TEST_TEMPLATE_NAME,
    "description": "A test template",
    "category": TEST_TEMPLATE_CATEGORY,
    "config_schema": {
        "name": TEST_TEMPLATE_NAME,
        "description": "A test template",
        "category": TEST_TEMPLATE_CATEGORY,
        "fields": [
            {
                "name": "title",
                "selector": "h1",
                "type": "text",
                "required": True,
                "multiple": False,
            }
        ],
        "advanced": {
            "delay": 1.0,
            "deep_crawl": False,
        },
    },
}
