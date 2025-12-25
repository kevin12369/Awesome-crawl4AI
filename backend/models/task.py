"""
任务数据模型
Task data model

爬取任务的数据库模型，存储任务状态和结果
Database model for crawl tasks, storing task status and results
"""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, Text, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Task(Base):
    """
    爬取任务模型
    Crawl Task Model

    存储每次爬取任务的信息、状态和结果
    Stores information, status, and results of each crawl task
    """

    __tablename__ = "tasks"

    # 任务状态枚举
    class Status:
        """任务状态常量"""
        PENDING = "pending"       # 待执行
        RUNNING = "running"       # 执行中
        COMPLETED = "completed"   # 已完成
        FAILED = "failed"         # 失败

    # 主键ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 目标URL
    url: Mapped[str] = mapped_column(String(2048), nullable=False, index=True)

    # 使用的模板ID（可为空，表示直接爬取）
    template_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("templates.id", ondelete="SET NULL"), nullable=True
    )

    # 任务状态
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=Status.PENDING, index=True
    )

    # 爬取配置（JSON格式）
    # 存储：browser_config, crawler_config等
    config: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # 爬取结果（JSON格式）
    # 存储：markdown, extracted_content, links, metadata等
    result: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # 错误信息（失败时记录）
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 创建时间
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    # 完成时间
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<Task(id={self.id}, url='{self.url[:50]}...', "
            f"status='{self.status}')>"
        )

    def to_dict(self) -> dict[str, Any]:
        """
        转换为字典格式
        Convert to dictionary format

        Returns:
            dict: 任务数据的字典表示
        """
        return {
            "id": self.id,
            "url": self.url,
            "template_id": self.template_id,
            "status": self.status,
            "config": self.config,
            "result": self.result,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    def is_running(self) -> bool:
        """是否正在执行"""
        return self.status == self.Status.RUNNING

    def is_completed(self) -> bool:
        """是否已完成"""
        return self.status == self.Status.COMPLETED

    def is_failed(self) -> bool:
        """是否失败"""
        return self.status == self.Status.FAILED

    def is_pending(self) -> bool:
        """是否待执行"""
        return self.status == self.Status.PENDING

    def mark_running(self) -> None:
        """标记为执行中"""
        self.status = self.Status.RUNNING

    def mark_completed(self, result: dict[str, Any]) -> None:
        """
        标记为已完成
        Mark as completed with result

        Args:
            result: 爬取结果字典
        """
        self.status = self.Status.COMPLETED
        self.result = result
        self.completed_at = datetime.utcnow()

    def mark_failed(self, error_message: str) -> None:
        """
        标记为失败
        Mark as failed with error message

        Args:
            error_message: 错误信息
        """
        self.status = self.Status.FAILED
        self.error_message = error_message
        self.completed_at = datetime.utcnow()
