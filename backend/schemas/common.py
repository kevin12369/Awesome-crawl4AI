"""
通用Pydantic模式
Common Pydantic Schemas
"""

from pydantic import BaseModel


class ApiResponse(BaseModel):
    """通用API响应"""
    success: bool
    message: str | None = None
    data: dict | list | None = None
    error: str | None = None


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    version: str
    database_connected: bool


class StatsResponse(BaseModel):
    """系统统计响应"""
    total_tasks: int
    running_tasks: int
    completed_tasks: int
    failed_tasks: int
    total_templates: int
    custom_templates: int
