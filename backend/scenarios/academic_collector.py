"""
学术收集场景
Academic Collection Scenario

专门用于学术论文和参考文献的收集
Specialized for academic papers and reference collection
"""

from typing import Any
from .base import BaseScenario
from ..core.template_engine import TemplateConfigSchema, ExtractField, AdvancedConfig


class AcademicCollector(BaseScenario):
    """
    学术收集场景
    Academic Collection Scenario

    艹，收集论文元数据，支持BibTeX导出！
    """

    def get_schema(self) -> TemplateConfigSchema:
        """获取学术收集配置Schema"""
        return TemplateConfigSchema(
            name="academic_collector",
            description="学术收集 - 提取论文标题、作者、摘要、引用等信息",
            category="academic",
            fields=[
                ExtractField(
                    name="title",
                    selector="h1, .paper-title, [itemprop*='headline']",
                    type="text",
                    required=True,
                ),
                ExtractField(
                    name="authors",
                    selector=".authors a, [itemprop*='author']",
                    type="text",
                    multiple=True,
                ),
                ExtractField(
                    name="abstract",
                    selector=".abstract, .summary",
                    type="text",
                ),
                ExtractField(
                    name="keywords",
                    selector=".keywords a, [itemprop*='keywords']",
                    type="text",
                    multiple=True,
                ),
                ExtractField(
                    name="publication_date",
                    selector="time, .date, .pub-date",
                    type="text",
                ),
                ExtractField(
                    name="pdf_url",
                    selector=".pdf-link a, .download-pdf",
                    type="link",
                ),
                ExtractField(
                    name="citation",
                    selector=".citation, .bibtex",
                    type="text",
                ),
            ],
            advanced=AdvancedConfig(
                delay=1.5,
                deep_crawl=False,  # 艹，论文一般不需要深度爬取
            ),
        )

    async def extract(self, url: str, crawler) -> dict[str, Any]:
        """
        执行学术收集

        Args:
            url: 论文页面URL
            crawler: Crawl4AI封装实例

        Returns:
            dict: 提取结果
        """
        result = await crawler.crawl(url)

        if not result.get("success"):
            return result

        # TODO: 实现BibTeX格式化
        # 暂时返回原始结果
        return result


# 自动注册
from ..core.scenario_registry import register_scenario
register_scenario(AcademicCollector)
