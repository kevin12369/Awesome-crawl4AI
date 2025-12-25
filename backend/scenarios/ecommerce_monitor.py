"""
电商监控场景
E-commerce Monitoring Scenario

专门用于电商网站的价格和库存监控
Specialized for e-commerce price and inventory monitoring
"""

from typing import Any
from .base import BaseScenario
from ..core.template_engine import TemplateConfigSchema, ExtractField, AdvancedConfig


class EcommerceMonitor(BaseScenario):
    """
    电商监控场景
    E-commerce Monitoring Scenario

    艹，监控商品价格、库存变化，支持历史对比！
    """

    def get_schema(self) -> TemplateConfigSchema:
        """获取电商监控配置Schema"""
        return TemplateConfigSchema(
            name="ecommerce_monitor",
            description="电商监控 - 提取商品价格、库存、评分等信息",
            category="ecommerce",
            fields=[
                ExtractField(
                    name="product_name",
                    selector="h1, .product-title, [itemprop*='name']",
                    type="text",
                    required=True,
                ),
                ExtractField(
                    name="price",
                    selector=".price, [itemprop*='price'], .product-price",
                    type="text",
                    required=True,
                ),
                ExtractField(
                    name="original_price",
                    selector=".original-price, .was-price",
                    type="text",
                ),
                ExtractField(
                    name="stock_status",
                    selector=".stock, .availability, [itemprop*='availability']",
                    type="text",
                ),
                ExtractField(
                    name="rating",
                    selector=".rating, [itemprop*='rating']",
                    type="text",
                ),
                ExtractField(
                    name="reviews_count",
                    selector=".reviews-count, [itemprop*='reviewCount']",
                    type="number",
                ),
                ExtractField(
                    name="image_url",
                    selector=".product-image img, [itemprop*='image']",
                    type="image",
                    multiple=True,
                ),
            ],
            advanced=AdvancedConfig(
                delay=2.0,  # 艹，电商网站反爬严格，延迟要长
                scroll_to_load=True,  # 可能需要滚动加载评论
                max_scrolls=3,
            ),
        )

    async def extract(self, url: str, crawler) -> dict[str, Any]:
        """
        执行电商监控

        Args:
            url: 商品页面URL
            crawler: Crawl4AI封装实例

        Returns:
            dict: 提取结果
        """
        result = await crawler.crawl(url)

        if not result.get("success"):
            return result

        # TODO: 实现智能价格解析（去除符号、提取数字等）
        # 暂时返回原始结果
        return result


# 自动注册
from ..core.scenario_registry import register_scenario
register_scenario(EcommerceMonitor)
