"""
教程数据模型
Tutorial data model

交互式教程的数据库模型
Database model for interactive tutorials
"""

from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.json import JSON

from .database import Base


class Tutorial(Base):
    """
    教程模型
    Tutorial Model

    存储交互式教程的步骤内容
    Stores interactive tutorial step content
    """

    __tablename__ = "tutorials"

    # 教程分类
    class Category:
        """教程分类常量"""
        BEGINNER = "beginner"       # 入门
        INTERMEDIATE = "intermediate"  # 进阶
        ADVANCED = "advanced"       # 高级

    # 主键ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 教程标题
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    # 教程内容（Markdown格式）
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # 步骤顺序（用于排序）
    step_order: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    # 分类（入门/进阶/高级）
    category: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True, default=Category.BEGINNER
    )

    # 代码示例（JSON格式存储代码块）
    # 格式：{"python": "import asyncio...", "bash": "crawl4ai-setup"}
    code_example: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # 额外数据（JSON格式，灵活扩展）
    # 可存储：练习题、答案、提示等
    extra_data: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # 创建时间
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return (
            f"<Tutorial(id={self.id}, title='{self.title}', "
            f"category='{self.category}', step={self.step_order})>"
        )

    def to_dict(self) -> dict[str, Any]:
        """
        转换为字典格式
        Convert to dictionary format

        Returns:
            dict: 教程数据的字典表示
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "step_order": self.step_order,
            "category": self.category,
            "code_example": self.code_example,
            "extra_data": self.extra_data,
            "created_at": self.created_at.isoformat(),
        }

    @property
    def python_code(self) -> str | None:
        """获取Python代码示例"""
        if self.code_example:
            return self.code_example.get("python")
        return None

    @property
    def bash_code(self) -> str | None:
        """获取Bash代码示例"""
        if self.code_example:
            return self.code_example.get("bash")
        return None

    def is_beginner(self) -> bool:
        """是否为入门教程"""
        return self.category == self.Category.BEGINNER

    def is_intermediate(self) -> bool:
        """是否为进阶教程"""
        return self.category == self.Category.INTERMEDIATE

    def is_advanced(self) -> bool:
        """是否为高级教程"""
        return self.category == self.Category.ADVANCED
