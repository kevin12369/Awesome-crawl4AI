"""
模板相关的Pydantic模式
Template-related Pydantic Schemas

用于API请求和响应的数据验证
Data validation for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ==================== 请求模式 ====================

class TemplateCreateRequest(BaseModel):
    """创建模板请求"""
    name: str = Field(..., description="模板名称（唯一）")
    description: Optional[str] = Field(None, description="模板描述")
    category: str = Field(..., description="分类：news/docs/ecommerce/academic/table/custom")
    config_schema: Dict[str, Any] = Field(..., description="配置Schema（JSON）")


class TemplateUpdateRequest(BaseModel):
    """更新模板请求"""
    name: Optional[str] = Field(None, description="模板名称")
    description: Optional[str] = Field(None, description="模板描述")
    category: Optional[str] = Field(None, description="分类")
    config_schema: Optional[Dict[str, Any]] = Field(None, description="配置Schema")


class TemplateValidateRequest(BaseModel):
    """验证模板配置请求"""
    config_schema: Dict[str, Any] = Field(..., description="待验证的配置Schema")


# ==================== 响应模式 ====================

class TemplateResponse(BaseModel):
    """模板响应"""
    id: int
    name: str
    description: Optional[str]
    category: str
    config_schema: Dict[str, Any]
    is_builtin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2: 支持ORM模式


class TemplateListResponse(BaseModel):
    """模板列表响应"""
    total: int
    items: List[TemplateResponse]


class TemplateValidateResponse(BaseModel):
    """模板验证响应"""
    valid: bool
    message: str
    errors: Optional[List[str]] = None
