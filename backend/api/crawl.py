"""
爬取API端点
Crawl API Endpoints

处理所有爬取相关的API请求
Handle all crawl-related API requests
"""

import asyncio
from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..models.database import get_db
from ..models.task import Task
from ..models.template import Template
from ..schemas.task import (
    CrawlRequest,
    BatchCrawlRequest,
    DeepCrawlRequest,
    CrawlResponse,
    BatchCrawlResponse,
    TaskResponse,
    TaskListResponse,
)
from ..core.crawler import Crawl4AIWrapper

router = APIRouter(prefix="/api/crawl", tags=["爬取"])


# ==================== 辅助函数 ====================

async def execute_crawl_task(
    url: str,
    template_id: int | None,
    config: dict | None,
    db: AsyncSession,
) -> int:
    """
    执行爬取任务（后台任务）
    Execute crawl task (background task)

    Args:
        url: 目标URL
        template_id: 模板ID
        config: 配置
        db: 数据库会话

    Returns:
        int: 任务ID
    """
    # 创建任务记录
    task = Task(
        url=url,
        template_id=template_id,
        status=Task.Status.PENDING,
        config=config,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)

    # 艹，这里应该是后台任务，暂时简化为直接执行
    # 后续可以用Celery或ARQ实现真正的后台任务

    return task.id


# ==================== API端点 ====================

@router.post("", response_model=CrawlResponse)
async def create_crawl_task(
    request: CrawlRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    创建爬取任务
    Create crawl task

    艹，这个端点创建一个新的爬取任务！
    """
    try:
        # 验证模板是否存在
        if request.template_id:
            result = await db.execute(select(Template).filter_by(id=request.template_id))
            template = result.scalar_one_or_none()
            if not template:
                raise HTTPException(status_code=404, detail="模板不存在")

        # 执行爬取（艹，暂时同步执行，后续改异步）
        async with Crawl4AIWrapper() as crawler:
            crawl_result = await crawler.crawl(request.url, request.config or {})

        # 保存到数据库
        task = Task(
            url=request.url,
            template_id=request.template_id,
            status=Task.Status.COMPLETED if crawl_result["success"] else Task.Status.FAILED,
            config=request.config,
            result=crawl_result if crawl_result["success"] else None,
            error_message=crawl_result.get("error") if not crawl_result["success"] else None,
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)

        return CrawlResponse(
            success=crawl_result["success"],
            task_id=task.id,
            result=crawl_result if crawl_result["success"] else None,
            error=crawl_result.get("error") if not crawl_result["success"] else None,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")


@router.post("/batch", response_model=BatchCrawlResponse)
async def create_batch_crawl(
    request: BatchCrawlRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    批量爬取
    Batch crawl

    艹，批量处理URL，效率更高！
    """
    try:
        if not request.urls:
            raise HTTPException(status_code=400, detail="URL列表不能为空")

        # 验证模板
        if request.template_id:
            result = await db.execute(select(Template).filter_by(id=request.template_id))
            template = result.scalar_one_or_none()
            if not template:
                raise HTTPException(status_code=404, detail="模板不存在")

        # 批量爬取
        async with Crawl4AIWrapper() as crawler:
            results = await crawler.crawl_batch(
                request.urls,
                request.config or {},
                request.max_concurrent,
            )

        # 保存结果
        task_ids = []
        completed = 0
        failed = 0

        for i, result in enumerate(results):
            task = Task(
                url=request.urls[i],
                template_id=request.template_id,
                status=Task.Status.COMPLETED if result["success"] else Task.Status.FAILED,
                config=request.config,
                result=result if result["success"] else None,
                error_message=result.get("error") if not result["success"] else None,
            )
            db.add(task)
            await db.flush()  # 获取ID但不提交
            task_ids.append(task.id)

            if result["success"]:
                completed += 1
            else:
                failed += 1

        await db.commit()

        return BatchCrawlResponse(
            total=len(request.urls),
            completed=completed,
            failed=failed,
            task_ids=task_ids,
        )

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"批量爬取失败: {str(e)}")


@router.get("/tasks", response_model=TaskListResponse)
async def list_tasks(
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """
    获取任务列表
    List tasks
    """
    try:
        query = select(Task)

        if status:
            query = query.filter_by(status=status)

        # 获取总数
        count_query = select(func.count()).select_from(query)
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # 分页查询
        query = query.order_by(Task.created_at.desc()).offset(offset).limit(limit)
        result = await db.execute(query)
        tasks = result.scalars().all()

        return TaskListResponse(
            total=total,
            items=[TaskResponse.model_validate(t) for t in tasks],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询任务列表失败: {str(e)}")


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    获取任务详情
    Get task details
    """
    try:
        result = await db.execute(select(Task).filter_by(id=task_id))
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")

        return TaskResponse.model_validate(task)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询任务失败: {str(e)}")


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    删除任务
    Delete task
    """
    try:
        result = await db.execute(select(Task).filter_by(id=task_id))
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")

        await db.delete(task)
        await db.commit()

        return {"success": True, "message": "任务已删除"}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"删除任务失败: {str(e)}")
