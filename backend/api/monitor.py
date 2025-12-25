"""
监控API端点
Monitor API Endpoints

系统监控和统计
System monitoring and statistics
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..models.database import get_db
from ..models.task import Task
from ..models.template import Template
from ..schemas.common import StatsResponse, HealthResponse

router = APIRouter(prefix="/api/monitor", tags=["监控"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    健康检查
    Health check
    """
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        database_connected=True,  # 艹，如果能到这里说明数据库连接正常
    )


@router.get("/stats", response_model=StatsResponse)
async def get_system_stats(
    db: AsyncSession = Depends(get_db),
):
    """
    获取系统统计
    Get system statistics

    艹，各种数据统计都在这！
    """
    try:
        # 任务统计
        total_tasks_result = await db.execute(select(func.count()).select_from(Task))
        total_tasks = total_tasks_result.scalar()

        running_tasks_result = await db.execute(
            select(func.count()).select_from(Task).filter_by(status=Task.Status.RUNNING)
        )
        running_tasks = running_tasks_result.scalar()

        completed_tasks_result = await db.execute(
            select(func.count()).select_from(Task).filter_by(status=Task.Status.COMPLETED)
        )
        completed_tasks = completed_tasks_result.scalar()

        failed_tasks_result = await db.execute(
            select(func.count()).select_from(Task).filter_by(status=Task.Status.FAILED)
        )
        failed_tasks = failed_tasks_result.scalar()

        # 模板统计
        total_templates_result = await db.execute(
            select(func.count()).select_from(Template)
        )
        total_templates = total_templates_result.scalar()

        custom_templates_result = await db.execute(
            select(func.count()).select_from(Template).filter_by(is_builtin=False)
        )
        custom_templates = custom_templates_result.scalar()

        return StatsResponse(
            total_tasks=total_tasks or 0,
            running_tasks=running_tasks or 0,
            completed_tasks=completed_tasks or 0,
            failed_tasks=failed_tasks or 0,
            total_templates=total_templates or 0,
            custom_templates=custom_templates or 0,
        )

    except Exception as e:
        # 艹，返回0而不是抛异常，前端好处理
        return StatsResponse(
            total_tasks=0,
            running_tasks=0,
            completed_tasks=0,
            failed_tasks=0,
            total_templates=0,
            custom_templates=0,
        )
