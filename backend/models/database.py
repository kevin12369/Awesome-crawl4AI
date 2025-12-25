"""
数据库连接管理模块
Database connection management module

这个SB模块负责SQLite数据库的连接和会话管理
This module manages SQLite database connection and sessions
"""

import asyncio
from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool

# 声明式基类 - 所有模型都继承这个
Base = declarative_base()

# 数据库文件路径
DB_DIR = Path(__file__).parent.parent.parent / "data"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "app.db"

# 全局引擎和会话工厂（艹，懒加载模式）
_engine: AsyncEngine | None = None
_async_session_factory: async_sessionmaker | None = None


def get_database_url() -> str:
    """
    获取数据库URL
    Get database URL

    Returns:
        str: SQLite异步连接URL
    """
    return f"sqlite+aiosqlite:///{DB_PATH}"


def get_engine() -> AsyncEngine:
    """
    获取数据库引擎（单例模式）
    Get database engine (singleton pattern)

    艹，全局唯一引擎，别tm到处创建新引擎！

    Returns:
        AsyncEngine: SQLAlchemy异步引擎
    """
    global _engine

    if _engine is None:
        _engine = create_async_engine(
            get_database_url(),
            connect_args={"check_same_thread": False},  # SQLite特有配置
            poolclass=StaticPool,  # SQLite不需要连接池
            echo=False,  # 生产环境关闭SQL日志
        )

    return _engine


def get_session_factory() -> async_sessionmaker:
    """
    获取会话工厂（单例模式）
    Get session factory (singleton pattern)

    Returns:
        async_sessionmaker: 异步会话工厂
    """
    global _async_session_factory

    if _async_session_factory is None:
        _async_session_factory = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,  # 提交后不过期对象，方便后续访问
            autocommit=False,
            autoflush=False,
        )

    return _async_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    依赖注入：获取数据库会话
    Dependency injection: Get database session

    这个SB函数给FastAPI依赖注入用的，每次请求一个新会话

    Yields:
        AsyncSession: 数据库会话
    """
    async_session = get_session_factory()
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    初始化数据库
    Initialize database

    创建所有表（如果不存在的话）
    Create all tables if they don't exist
    """
    engine = get_engine()

    # 导入所有模型（艹，必须先导入才能创建表！）
    from .template import Template  # noqa: F401
    from .task import Task  # noqa: F401
    from .tutorial import Tutorial  # noqa: F401

    async with engine.begin() as conn:
        # 艹，drop_existing=False别tm乱改成True！会删数据的！
        await conn.run_sync(Base.metadata.create_all)

    print(f"✅ 数据库初始化完成: {DB_PATH}")


async def close_db() -> None:
    """
    关闭数据库连接
    Close database connection

    应用退出时调用，优雅关闭
    """
    global _engine, _async_session_factory

    if _engine:
        await _engine.dispose()
        _engine = None
        _async_session_factory = None
        print("✅ 数据库连接已关闭")


if __name__ == "__main__":
    """
    测试代码：单独运行此文件可以初始化数据库
    Test: Run this file directly to initialize database
    """
    async def test_init():
        await init_db()
        print("🎉 数据库初始化测试成功！")

    asyncio.run(test_init())
