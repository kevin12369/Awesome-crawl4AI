"""
模板数据模型
Template data model

场景模板的数据库模型，存储爬取配置
Database model for scenario templates, storing crawl configurations
"""

from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.json import JSON

from .database import Base


class Template(Base):
    """
    场景模板模型
    Scenario Template Model

    存储爬取场景的配置，包括内置模板和用户自定义模板
    Stores crawl scenario configurations, including built-in and custom templates
    """

    __tablename__ = "templates"

    # 主键ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 模板名称（唯一标识）
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)

    # 模板描述
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 分类：news, docs, ecommerce, academic, table, custom
    category: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True, default="custom"
    )

    # 配置Schema（JSON格式存储完整的场景配置）
    # 包含：fields（提取字段）、advanced（高级配置）等
    config_schema: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    # 是否为内置模板（内置模板不能被删除）
    is_builtin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # 创建时间
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # 更新时间
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return (
            f"<Template(id={self.id}, name='{self.name}', "
            f"category='{self.category}', is_builtin={self.is_builtin})>"
        )

    def to_dict(self) -> dict[str, Any]:
        """
        转换为字典格式
        Convert to dictionary format

        Returns:
            dict: 模板数据的字典表示
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "config_schema": self.config_schema,
            "is_builtin": self.is_builtin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @property
    def fields(self) -> list[dict[str, Any]]:
        """
        获取提取字段列表
        Get extraction fields list

        Returns:
            list: 提取字段配置列表
        """
        return self.config_schema.get("fields", [])

    @property
    def advanced_config(self) -> dict[str, Any]:
        """
        获取高级配置
        Get advanced configuration

        Returns:
            dict: 高级配置字典
        """
        return self.config_schema.get("advanced", {})

    def is_customizable(self) -> bool:
        """
        是否可自定义（用户创建的模板才能编辑/删除）
        Whether the template is customizable (user-created templates can be edited/deleted)

        Returns:
            bool: 如果是用户自定义模板返回True
        """
        return not self.is_builtin
