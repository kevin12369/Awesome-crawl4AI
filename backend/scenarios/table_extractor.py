"""
表格提取场景
Table Extraction Scenario

专门用于网页表格的智能提取
Specialized for intelligent table extraction from web pages
"""

from typing import Any
from .base import BaseScenario
from ..core.template_engine import TemplateConfigSchema, ExtractField, AdvancedConfig


class TableExtractor(BaseScenario):
    """
    表格提取场景
    Table Extraction Scenario

    艹，智能识别和提取网页中的表格数据！
    """

    def get_schema(self) -> TemplateConfigSchema:
        """获取表格提取配置Schema"""
        return TemplateConfigSchema(
            name="table_extractor",
            description="表格提取 - 智能识别网页表格，转换为结构化数据",
            category="table",
            fields=[
                ExtractField(
                    name="table_title",
                    selector="caption, .table-title, figcaption",
                    type="text",
                ),
                ExtractField(
                    name="table_headers",
                    selector="thead th",
                    type="text",
                    multiple=True,
                ),
                ExtractField(
                    name="table_rows",
                    selector="tbody tr",
                    type="text",
                    multiple=True,
                ),
            ],
            advanced=AdvancedConfig(
                delay=0.5,
            ),
        )

    async def extract(self, url: str, crawler) -> dict[str, Any]:
        """
        执行表格提取

        Args:
            url: 包含表格的页面URL
            crawler: Crawl4AI封装实例

        Returns:
            dict: 提取结果（包含表格数据）
        """
        # 艹，表格提取需要使用Crawl4AI的表格功能
        config = {
            "word_count_threshold": 1,
        }

        result = await crawler.crawl(url, config)

        if not result.get("success"):
            return result

        # TODO: 实现智能表格解析（处理合并单元格等）
        # 暂时返回原始结果
        return result


# 自动注册
from ..core.scenario_registry import register_scenario
register_scenario(TableExtractor)
