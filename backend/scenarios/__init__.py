"""
场景模块初始化
Scenario Module Initialization

自动注册所有内置场景
Auto-register all built-in scenarios
"""

from .news_crawler import NewsCrawler
from .docs_archiver import DocsArchiver
from .ecommerce_monitor import EcommerceMonitor
from .academic_collector import AcademicCollector
from .table_extractor import TableExtractor

__all__ = [
    "NewsCrawler",
    "DocsArchiver",
    "EcommerceMonitor",
    "AcademicCollector",
    "TableExtractor",
]
