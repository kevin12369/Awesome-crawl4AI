"""
Crawl4AI 封装层
Crawl4AI Wrapper

这个SB模块封装Crawl4AI的AsyncWebCrawler，提供统一的爬取接口
This module wraps Crawl4AI's AsyncWebCrawler for unified crawl interface
"""

import asyncio
from typing import Any, Optional
from pathlib import Path

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy, JsonCssExtractionStrategy


class Crawl4AIWrapper:
    """
    Crawl4AI封装类
    Crawl4AI Wrapper Class

    艹，这个类统一管理所有爬取操作，别tm到处创建爬虫实例！
    """

    def __init__(
        self,
        headless: bool = True,
        browser_type: str = "chromium",
        verbose: bool = True,
    ):
        """
        初始化封装器

        Args:
            headless: 是否无头模式
            browser_type: 浏览器类型（chromium/firefox/webkit）
            verbose: 是否输出详细日志
        """
        self.browser_config = BrowserConfig(
            headless=headless,
            browser_type=browser_type,
            verbose=verbose,
        )
        self.verbose = verbose
        self._crawler: Optional[AsyncWebCrawler] = None

    async def __aenter__(self):
        """异步上下文管理器入口"""
        self._crawler = AsyncWebCrawler(config=self.browser_config)
        await self._crawler.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        if self._crawler:
            await self._crawler.__aexit__(exc_type, exc_val, exc_tb)

    async def crawl(
        self,
        url: str,
        config: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        爬取单个URL
        Crawl a single URL

        Args:
            url: 目标URL
            config: 爬取配置（可选）

        Returns:
            dict: 爬取结果字典
            {
                "success": bool,
                "markdown": str,
                "fit_markdown": str,
                "extracted_content": str,
                "links": dict,
                "media": dict,
                "metadata": dict,
                "screenshot": str,
                "error": str  # 如果失败
            }
        """
        if not self._crawler:
            raise RuntimeError("艹，爬虫未初始化！请使用 async with 语句。")

        try:
            # 构建爬取配置
            run_config = self._build_run_config(config or {})

            # 执行爬取
            if self.verbose:
                print(f"🔍 开始爬取: {url}")

            result = await self._crawler.arun(url=url, config=run_config)

            # 处理结果
            if result.success:
                if self.verbose:
                    print(f"✅ 爬取成功: {url}")

                return {
                    "success": True,
                    "markdown": result.markdown.raw_markdown if result.markdown else "",
                    "fit_markdown": result.markdown.fit_markdown if result.markdown else "",
                    "extracted_content": result.extracted_content,
                    "links": {
                        "internal": result.links.get("internal", []),
                        "external": result.links.get("external", []),
                    } if result.links else {},
                    "media": {
                        "images": result.media.get("images", []),
                        "videos": result.media.get("videos", []),
                        "audio": result.media.get("audio", []),
                    } if result.media else {},
                    "metadata": {
                        "title": result.metadata.get("title"),
                        "description": result.metadata.get("description"),
                        "keywords": result.metadata.get("keywords", []),
                    } if result.metadata else {},
                    "screenshot": result.screenshot,
                }
            else:
                error_msg = result.error_message or "爬取失败，未知错误"
                if self.verbose:
                    print(f"❌ 爬取失败: {url} - {error_msg}")

                return {
                    "success": False,
                    "error": error_msg,
                }

        except Exception as e:
            error_msg = f"爬取异常: {str(e)}"
            if self.verbose:
                print(f"❌ {error_msg}")

            return {
                "success": False,
                "error": error_msg,
            }

    async def crawl_batch(
        self,
        urls: list[str],
        config: Optional[dict[str, Any]] = None,
        max_concurrent: int = 5,
    ) -> list[dict[str, Any]]:
        """
        批量爬取URL
        Batch crawl URLs

        Args:
            urls: URL列表
            config: 爬取配置（可选）
            max_concurrent: 最大并发数

        Returns:
            list: 爬取结果列表
        """
        if not self._crawler:
            raise RuntimeError("艹，爬虫未初始化！请使用 async with 语句。")

        semaphore = asyncio.Semaphore(max_concurrent)

        async def crawl_with_semaphore(url: str) -> dict[str, Any]:
            async with semaphore:
                return await self.crawl(url, config)

        tasks = [crawl_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理异常
        formatted_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                formatted_results.append({
                    "success": False,
                    "error": f"任务异常: {str(result)}",
                })
            else:
                formatted_results.append(result)

        return formatted_results

    async def deep_crawl(
        self,
        url: str,
        strategy: str = "bfs",
        max_pages: int = 10,
        max_depth: int = 3,
        config: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        深度爬取（爬取整个网站）
        Deep crawl (crawl entire website)

        Args:
            url: 起始URL
            strategy: 爬取策略（bfs/dfs）
            max_pages: 最大页面数
            max_depth: 最大深度
            config: 爬取配置（可选）

        Returns:
            dict: 深度爬取结果
        """
        if not self._crawler:
            raise RuntimeError("艹，爬虫未初始化！请使用 async with 语句。")

        # 艹，深度爬取需要使用Crawl4AI的深度爬取功能
        # 这里先实现基础版本，后续可以优化
        visited_urls = set()
        results = []

        async def crawl_recursive(current_url: str, depth: int):
            if depth > max_depth or len(visited_urls) >= max_pages:
                return

            if current_url in visited_urls:
                return

            visited_urls.add(current_url)

            # 爬取当前页面
            result = await self.crawl(current_url, config)
            results.append({
                "url": current_url,
                "depth": depth,
                "result": result,
            })

            if not result.get("success"):
                return

            # 获取链接
            links = result.get("links", {}).get("internal", [])

            # BFS或DFS策略
            if strategy == "bfs":
                # BFS：按层级爬取
                tasks = []
                for link in links[:max_pages]:
                    if link not in visited_urls:
                        tasks.append(crawl_recursive(link, depth + 1))
                await asyncio.gather(*tasks)
            else:
                # DFS：深度优先
                for link in links[:max_pages]:
                    await crawl_recursive(link, depth + 1)

        await crawl_recursive(url, 0)

        return {
            "success": True,
            "total_pages": len(results),
            "results": results,
        }

    def _build_run_config(self, config: dict[str, Any]) -> CrawlerRunConfig:
        """
        构建爬取配置
        Build crawl run configuration

        Args:
            config: 配置字典

        Returns:
            CrawlerRunConfig: Crawl4AI运行配置对象
        """
        # 缓存模式
        cache_mode = CacheMode.ENABLED
        if config.get("cache_mode") == "bypass":
            cache_mode = CacheMode.BYPASS
        elif config.get("cache_mode") == "disable":
            cache_mode = CacheMode.DISABLED

        # 提取策略
        extraction_strategy = None
        if config.get("extraction_strategy"):
            # 艹，这里可以添加各种提取策略
            pass

        # 构建配置
        run_config = CrawlerRunConfig(
            cache_mode=cache_mode,
            word_count_threshold=config.get("word_count_threshold", 1),
            extraction_strategy=extraction_strategy,
        )

        return run_config


# 便捷函数
async def quick_crawl(
    url: str,
    headless: bool = True,
) -> dict[str, Any]:
    """
    快速爬取（便捷函数）
    Quick crawl (convenience function)

    Args:
        url: 目标URL
        headless: 是否无头模式

    Returns:
        dict: 爬取结果
    """
    async with Crawl4AIWrapper(headless=headless) as crawler:
        return await crawler.crawl(url)


# 测试代码
if __name__ == "__main__":
    async def test():
        """测试爬虫"""
        async with Crawl4AIWrapper() as crawler:
            result = await crawler.crawl("https://example.com")
            print(result)

    asyncio.run(test())
