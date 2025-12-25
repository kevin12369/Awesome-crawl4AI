"""
Pytest 配置文件
Pytest Configuration and Fixtures

艹，所有测试的公共 fixtures 都在这里！
"""

import asyncio
import os
import sys
import tempfile
from pathlib import Path
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到路径 / Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入应用和模型 / Import app and models
from main import app
from models.database import Base, get_db
from models.template import Template
from models.task import Task


# ============================================
# 测试数据库配置 / Test Database Configuration
# ============================================

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环 / Create event loop"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_engine():
    """创建测试数据库引擎 / Create test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

    # 创建所有表 / Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # 清理：删除所有表 / Cleanup: drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """创建测试数据库会话 / Create test database session"""
    async_session_maker = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        yield session


# ============================================
# API 测试 Fixtures / API Test Fixtures
# ============================================


@pytest.fixture(scope="function")
async def client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """创建测试客户端 / Create test client"""

    async def override_get_db():
        yield test_session

    # 覆盖数据库依赖 / Override database dependency
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    # 清理依赖覆盖 / Clean up dependency override
    app.dependency_overrides.clear()


# ============================================
# Mock Fixtures / Mock Fixtures
# ============================================


@pytest.fixture
def mock_crawl_result():
    """Mock 爬取结果 / Mock crawl result"""
    from tests import MOCK_CRAWL_RESULT
    return MOCK_CRAWL_RESULT.copy()


@pytest.fixture
def mock_template_data():
    """Mock 模板数据 / Mock template data"""
    from tests import MOCK_TEMPLATE_DATA
    return MOCK_TEMPLATE_DATA.copy()


@pytest.fixture
def mock_crawler():
    """Mock Crawler 实例 / Mock Crawler instance"""
    crawler = AsyncMock()
    crawler.crawl = AsyncMock(return_value={
        "success": True,
        "markdown": "# Test\n\nContent",
        "extracted_content": {},
        "links": [],
        "media": [],
        "metadata": {},
    })
    crawler.crawl_batch = AsyncMock(return_value=[
        {"success": True, "url": url}
        for url in ["https://example1.com", "https://example2.com"]
    ])
    crawler.deep_crawl = AsyncMock(return_value={
        "success": True,
        "pages": [],
    })
    return crawler


# ============================================
# 测试数据 Fixtures / Test Data Fixtures
# ============================================


@pytest.fixture
async def test_template(test_session: AsyncSession):
    """创建测试模板 / Create test template"""
    template = Template(
        name="test_template",
        description="A test template",
        category="test",
        config_schema={
            "name": "test_template",
            "description": "A test template",
            "category": "test",
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
        is_builtin=False,
    )
    test_session.add(template)
    await test_session.commit()
    await test_session.refresh(template)
    return template


@pytest.fixture
async def test_task(test_session: AsyncSession, test_template: Template):
    """创建测试任务 / Create test task"""
    task = Task(
        url="https://example.com",
        template_id=test_template.id,
        status="completed",
        config={},
        result={
            "success": True,
            "markdown": "# Test\n\nContent",
        },
        error_message=None,
    )
    test_session.add(task)
    await test_session.commit()
    await test_session.refresh(task)
    return task


# ============================================
# Pytest 钩子 / Pytest Hooks
# ============================================


def pytest_configure(config):
    """Pytest 配置钩子 / Pytest configuration hook"""
    config.addinivalue_line(
        "markers",
        "unit: Unit tests (fast, isolated)",
    )
    config.addinivalue_line(
        "markers",
        "integration: Integration tests (slower, may use external services)",
    )
    config.addinivalue_line(
        "markers",
        "slow: Slow running tests",
    )
    config.addinivalue_line(
        "markers",
        "crawl: Crawl-related tests (requires network)",
    )


@pytest.fixture(autouse=True)
def clean_environment():
    """自动清理环境变量 / Auto clean environment variables"""
    # 测试前保存原始环境变量 / Save original env vars before test
    original_env = os.environ.copy()

    yield

    # 测试后恢复环境变量 / Restore env vars after test
    os.environ.clear()
    os.environ.update(original_env)


# ============================================
# 测试工具函数 / Test Utility Functions
# ============================================


def assert_valid_response(response, expected_status_code=200):
    """断言有效响应 / Assert valid response"""
    assert response.status_code == expected_status_code
    data = response.json()
    assert "code" in data
    assert "message" in data
    return data


async def create_test_template(
    session: AsyncSession,
    name: str = "test_template",
    category: str = "test",
) -> Template:
    """快速创建测试模板 / Quick create test template"""
    template = Template(
        name=name,
        description=f"Test template {name}",
        category=category,
        config_schema={
            "name": name,
            "description": f"Test template {name}",
            "category": category,
            "fields": [],
            "advanced": {},
        },
        is_builtin=False,
    )
    session.add(template)
    await session.commit()
    await session.refresh(template)
    return template


async def create_test_task(
    session: AsyncSession,
    url: str = "https://example.com",
    status: str = "pending",
) -> Task:
    """快速创建测试任务 / Quick create test task"""
    task = Task(
        url=url,
        template_id=None,
        status=status,
        config={},
        result=None,
        error_message=None,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
