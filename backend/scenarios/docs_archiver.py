"""
文档归档场景
Documentation Archiver Scenario

专门用于技术文档网站的完整归档
Specialized for archiving technical documentation websites
"""

from typing import Any
from .base import BaseScenario
from ..core.template_engine import TemplateConfigSchema, ExtractField, AdvancedConfig


class DocsArchiver(BaseScenario):
    """
    文档归档场景
    Documentation Archiver Scenario

    艹，深度爬取整个文档网站，保持目录结构！
    """

    def get_schema(self) -> TemplateConfigSchema:
        """获取文档归档配置Schema"""
        return TemplateConfigSchema(
            name="docs_archiver",
            description="文档归档 - 深度爬取技术文档，转换为Markdown格式",
            category="docs",
            fields=[
                ExtractField(
                    name="title",
                    selector="h1",
                    type="text",
                    required=True,
                ),
                ExtractField(
                    name="content",
                    selector="article, .content, .docs-content, main",
                    type="text",
                    required=True,
                ),
                ExtractField(
                    name="breadcrumbs",
                    selector=".breadcrumbs a, .breadcrumb a",
                    type="text",
                    multiple=True,
                ),
            ],
            advanced=AdvancedConfig(
                deep_crawl=True,  # 艹，文档必须深度爬取
                max_pages=100,     # 最多100页
                strategy="bfs",     # BFS策略
                delay=0.5,
            ),
        )

    async def extract(self, url: str, crawler) -> dict[str, Any]:
        """
        执行文档归档

        Args:
            url: 起始URL
            crawler: Crawl4AI封装实例

        Returns:
            dict: 归档结果
        """
        # 艹，文档归档需要深度爬取
        result = await crawler.deep_crawl(
            url,
            strategy="bfs",
            max_pages=50,
            config={"cache_mode": "bypass"},
        )

        return result


# 自动注册
from ..core.scenario_registry import register_scenario
register_scenario(DocsArchiver)
