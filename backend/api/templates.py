"""
模板API端点
Template API Endpoints

处理场景模板的CRUD操作
Handle CRUD operations for scenario templates
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..models.database import get_db
from ..models.template import Template
from ..schemas.template import (
    TemplateCreateRequest,
    TemplateUpdateRequest,
    TemplateValidateRequest,
    TemplateResponse,
    TemplateListResponse,
    TemplateValidateResponse,
)
from ..core.template_engine import TemplateEngine, TemplateConfigSchema

router = APIRouter(prefix="/api/templates", tags=["模板"])


# ==================== API端点 ====================

@router.get("", response_model=TemplateListResponse)
async def list_templates(
    category: str | None = None,
    is_builtin: bool | None = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """
    获取模板列表
    List templates

    艹，可以按分类过滤！
    """
    try:
        query = select(Template)

        if category:
            query = query.filter_by(category=category)

        if is_builtin is not None:
            query = query.filter_by(is_builtin=is_builtin)

        # 获取总数
        count_query = select(func.count()).select_from(query)
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # 分页查询
        query = query.order_by(Template.created_at.desc()).offset(offset).limit(limit)
        result = await db.execute(query)
        templates = result.scalars().all()

        return TemplateListResponse(
            total=total,
            items=[TemplateResponse.model_validate(t) for t in templates],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询模板列表失败: {str(e)}")


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    获取单个模板详情
    Get template details
    """
    try:
        result = await db.execute(select(Template).filter_by(id=template_id))
        template = result.scalar_one_or_none()

        if not template:
            raise HTTPException(status_code=404, detail="模板不存在")

        return TemplateResponse.model_validate(template)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询模板失败: {str(e)}")


@router.post("", response_model=TemplateResponse)
async def create_template(
    request: TemplateCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    创建自定义模板
    Create custom template

    艹，用户可以创建自己的场景模板！
    """
    try:
        # 验证配置
        engine = TemplateEngine()
        valid, error_msg, schema = engine.validate_template_config(request.config_schema)

        if not valid:
            raise HTTPException(status_code=400, detail=f"配置验证失败: {error_msg}")

        # 检查名称是否重复
        result = await db.execute(select(Template).filter_by(name=request.name))
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail=f"模板名称 '{request.name}' 已存在")

        # 创建模板
        template = Template(
            name=request.name,
            description=request.description,
            category=request.category,
            config_schema=request.config_schema,
            is_builtin=False,  # 用户创建的模板都不是内置的
        )

        db.add(template)
        await db.commit()
        await db.refresh(template)

        return TemplateResponse.model_validate(template)

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"创建模板失败: {str(e)}")


@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: int,
    request: TemplateUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    更新模板
    Update template

    注意：内置模板不能修改！
    """
    try:
        result = await db.execute(select(Template).filter_by(id=template_id))
        template = result.scalar_one_or_none()

        if not template:
            raise HTTPException(status_code=404, detail="模板不存在")

        if template.is_builtin:
            raise HTTPException(status_code=403, detail="内置模板不能修改")

        # 验证新配置（如果有）
        if request.config_schema:
            engine = TemplateEngine()
            valid, error_msg, _ = engine.validate_template_config(request.config_schema)
            if not valid:
                raise HTTPException(status_code=400, detail=f"配置验证失败: {error_msg}")

        # 更新字段
        if request.name is not None:
            template.name = request.name
        if request.description is not None:
            template.description = request.description
        if request.category is not None:
            template.category = request.category
        if request.config_schema is not None:
            template.config_schema = request.config_schema

        await db.commit()
        await db.refresh(template)

        return TemplateResponse.model_validate(template)

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"更新模板失败: {str(e)}")


@router.delete("/{template_id}")
async def delete_template(
    template_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    删除模板
    Delete template

    注意：内置模板不能删除！
    """
    try:
        result = await db.execute(select(Template).filter_by(id=template_id))
        template = result.scalar_one_or_none()

        if not template:
            raise HTTPException(status_code=404, detail="模板不存在")

        if template.is_builtin:
            raise HTTPException(status_code=403, detail="内置模板不能删除")

        await db.delete(template)
        await db.commit()

        return {"success": True, "message": "模板已删除"}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"删除模板失败: {str(e)}")


@router.post("/validate", response_model=TemplateValidateResponse)
async def validate_template(request: TemplateValidateRequest):
    """
    验证模板配置
    Validate template configuration

    艹，这个端点不保存配置，只做验证！
    """
    try:
        engine = TemplateEngine()
        valid, error_msg, schema = engine.validate_template_config(request.config_schema)

        if valid:
            return TemplateValidateResponse(
                valid=True,
                message="配置验证通过",
            )
        else:
            return TemplateValidateResponse(
                valid=False,
                message="配置验证失败",
                errors=[error_msg],
            )

    except Exception as e:
        return TemplateValidateResponse(
            valid=False,
            message="验证过程异常",
            errors=[str(e)],
        )
