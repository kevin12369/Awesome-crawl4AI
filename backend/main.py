"""
FastAPI应用入口
FastAPI Application Entry Point

艹，一切从这开始！
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .models.database import init_db, close_db
from .api import crawl, templates, monitor


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    Application lifespan management
    """
    # 启动时初始化
    print("🚀 正在启动 Awesome-crawl4AI 后端服务...")
    await init_db()
    print("✅ 数据库初始化完成")

    yield

    # 关闭时清理
    print("🛑 正在关闭服务...")
    await close_db()
    print("✅ 服务已关闭")


# 创建FastAPI应用
app = FastAPI(
    title="Awesome-crawl4AI",
    description="可视化爬虫平台API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS配置（艹，开发环境允许所有来源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境要限制！
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(crawl.router)
app.include_router(templates.router)
app.include_router(monitor.router)


# ==================== 根路径 ====================

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "Awesome-crawl4AI API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }


# ==================== 异常处理 ====================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": f"服务器错误: {str(exc)}",
        },
    )


# ==================== 启动命令 ====================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式自动重载
        log_level="info",
    )
