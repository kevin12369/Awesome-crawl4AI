"""
任务相关的Pydantic模式
Task-related Pydantic Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


# ==================== 请求模式 ====================

class CrawlRequest(BaseModel):
    """基础爬取请求"""
    url: str = Field(..., description="目标URL", min_length=1, max_length=2048)
    template_id: Optional[int] = Field(None, description="使用的模板ID（可选）")
    config: Optional[Dict[str, Any]] = Field(None, description="爬取配置覆盖")


class BatchCrawlRequest(BaseModel):
    """批量爬取请求"""
    urls: List[str] = Field(..., description="URL列表", min_length=1, max_length=100)
    template_id: Optional[int] = Field(None, description="使用的模板ID（可选）")
    config: Optional[Dict[str, Any]] = Field(None, description="爬取配置覆盖")
    max_concurrent: int = Field(5, description="最大并发数", ge=1, le=20)


class DeepCrawlRequest(BaseModel):
    """深度爬取请求"""
    url: str = Field(..., description="起始URL")
    strategy: str = Field("bfs", description="爬取策略：bfs/dfs")
    max_pages: int = Field(10, description="最大页面数", ge=1, le=1000)
    max_depth: int = Field(3, description="最大深度", ge=1, le=10)
    config: Optional[Dict[str, Any]] = Field(None, description="爬取配置")


# ==================== 响应模式 ====================

class TaskResponse(BaseModel):
    """任务响应"""
    id: int
    url: str
    template_id: Optional[int]
    status: str
    config: Optional[Dict[str, Any]]
    result: Optional[Dict[str, Any]]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """任务列表响应"""
    total: int
    items: List[TaskResponse]


class CrawlResponse(BaseModel):
    """爬取响应（同步）"""
    success: bool
    task_id: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class BatchCrawlResponse(BaseModel):
    """批量爬取响应"""
    total: int
    completed: int
    failed: int
    task_ids: List[int]
