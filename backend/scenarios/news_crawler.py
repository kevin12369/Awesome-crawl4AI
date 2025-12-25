"""
新闻爬取场景
News Crawler Scenario

专门用于新闻网站的爬取
Specialized for news website crawling
"""

from typing import Any
from .base import BaseScenario
from ..core.template_engine import TemplateConfigSchema, ExtractField, AdvancedConfig


class NewsCrawler(BaseScenario):
    """
    新闻爬取场景
    News Crawler Scenario

    艹，专门爬取新闻文章，提取标题、正文、作者等信息！
    """

    def get_schema(self) -> TemplateConfigSchema:
        """获取新闻爬取配置Schema"""
        return TemplateConfigSchema(
            name="news_crawler",
            description="新闻文章爬取 - 自动提取标题、正文、作者、日期和标签",
            category="news",
            fields=[
                ExtractField(
                    name="title",
                    selector="h1",
                    type="text",
                    required=True,
                ),
                ExtractField(
                    name="content",
                    selector="article p, .content, .article-body",
                    type="text",
                    required=True,
                    multiple=True,
                ),
                ExtractField(
                    name="author",
                    selector=".author, [itemprop*='author'], .byline",
                    type="text",
                ),
                ExtractField(
                    name="publish_date",
                    selector="time, .date, [datetime], .publish-date",
                    type="text",
                ),
                ExtractField(
                    name="tags",
                    selector=".tags a, .category",
                    type="text",
                    multiple=True,
                ),
            ],
            advanced=AdvancedConfig(
                delay=1.0,  # 艹，新闻网站要友好点，加1秒延迟
                scroll_to_load=False,
            ),
        )

    async def extract(self, url: str, crawler) -> dict[str, Any]:
        """
        执行新闻爬取

        Args:
            url: 目标URL
            crawler: Crawl4AI封装实例

        Returns:
            dict: 提取结果
        """
        # 艹，先爬取原始内容
        result = await crawler.crawl(url)

        if not result.get("success"):
            return result

        # TODO: 实现智能字段提取
        # 暂时返回原始结果
        return result


# 自动注册
from ..core.scenario_registry import register_scenario
register_scenario(NewsCrawler)
