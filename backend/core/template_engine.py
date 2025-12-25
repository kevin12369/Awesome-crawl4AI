"""
模板引擎
Template Engine

这个SB模块负责场景模板的加载、验证和应用
This module handles scenario template loading, validation, and application
"""

import json
from typing import Any, Optional
from pathlib import Path
from abc import ABC, abstractmethod

from pydantic import BaseModel, Field, validator

from .crawler import Crawl4AIWrapper


# ==================== 提取字段定义 ====================

class ExtractField(BaseModel):
    """
    提取字段模型
    Extraction Field Model

    定义如何从网页中提取特定字段的数据
    Defines how to extract specific field data from web pages
    """

    name: str = Field(..., description="字段名称")
    selector: str = Field(..., description="CSS选择器")
    type: str = Field(default="text", description="提取类型: text/number/link/image/attribute")
    attribute: Optional[str] = Field(None, description="当type为attribute时指定属性名")
    required: bool = Field(default=False, description="是否必需")
    multiple: bool = Field(default=False, description="是否提取多个值")

    @validator('type')
    def validate_type(cls, v):
        """验证提取类型"""
        valid_types = {'text', 'number', 'link', 'image', 'attribute'}
        if v not in valid_types:
            raise ValueError(f'艹，无效的提取类型: {v}，必须是: {valid_types}')
        return v

    @validator('attribute')
    def validate_attribute(cls, v, values):
        """当type为attribute时，attribute字段必填"""
        if values.get('type') == 'attribute' and not v:
            raise ValueError('艹，type为attribute时必须指定attribute字段')
        return v


# ==================== 高级配置定义 ====================

class AdvancedConfig(BaseModel):
    """
    高级配置模型
    Advanced Configuration Model

    深度爬取、代理、限流等高级选项
    Advanced options: deep crawl, proxy, rate limiting, etc.
    """

    deep_crawl: bool = Field(default=False, description="是否深度爬取")
    max_pages: int = Field(default=10, description="最大页面数")
    strategy: str = Field(default="bfs", description="爬取策略: bfs/dfs")
    proxy: Optional[str] = Field(None, description="代理地址")
    delay: float = Field(default=0.0, description="请求延迟（秒）")
    scroll_to_load: bool = Field(default=False, description="是否滚动加载")
    max_scrolls: int = Field(default=10, description="最大滚动次数")

    @validator('strategy')
    def validate_strategy(cls, v):
        """验证爬取策略"""
        if v not in {'bfs', 'dfs'}:
            raise ValueError('艹，策略必须是 bfs 或 dfs')
        return v

    @validator('delay')
    def validate_delay(cls, v):
        """验证延迟"""
        if v < 0:
            raise ValueError('艹，延迟不能为负数')
        return v


# ==================== 模板配置Schema ====================

class TemplateConfigSchema(BaseModel):
    """
    模板配置Schema
    Template Configuration Schema

    完整的场景模板配置
    Complete scenario template configuration
    """

    name: str = Field(..., description="模板名称")
    description: Optional[str] = Field(None, description="模板描述")
    fields: list[ExtractField] = Field(default_factory=list, description="提取字段列表")
    advanced: Optional[AdvancedConfig] = Field(None, description="高级配置")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "news_crawler",
                "description": "新闻文章爬取",
                "fields": [
                    {
                        "name": "title",
                        "selector": "h1.title",
                        "type": "text",
                        "required": True,
                    },
                    {
                        "name": "content",
                        "selector": "article.content",
                        "type": "text",
                        "required": True,
                    },
                ],
                "advanced": {
                    "deep_crawl": False,
                    "delay": 1.0,
                },
            }
        }


# ==================== 模板引擎 ====================

class TemplateEngine:
    """
    模板引擎
    Template Engine

    艹，这个引擎负责加载、验证和应用场景模板！
    """

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        初始化模板引擎

        Args:
            templates_dir: 自定义模板目录路径
        """
        self.templates_dir = templates_dir or Path(__file__).parent.parent.parent / "data" / "templates"
        self.templates_dir.mkdir(parents=True, exist_ok=True)

    def validate_template_config(self, config: dict[str, Any]) -> tuple[bool, str, Optional[TemplateConfigSchema]]:
        """
        验证模板配置
        Validate template configuration

        Args:
            config: 配置字典

        Returns:
            tuple: (是否有效, 错误信息, 验证后的Schema对象)
        """
        try:
            schema = TemplateConfigSchema(**config)
            return True, "", schema
        except Exception as e:
            error_msg = f"配置验证失败: {str(e)}"
            return False, error_msg, None

    async def apply_template(
        self,
        url: str,
        template_config: TemplateConfigSchema,
        crawler: Crawl4AIWrapper,
    ) -> dict[str, Any]:
        """
        应用模板进行爬取
        Apply template for crawling

        Args:
            url: 目标URL
            template_config: 模板配置Schema
            crawler: Crawl4AI封装实例

        Returns:
            dict: 爬取结果（包含提取的字段数据）
        """
        # 艹，先爬取基础内容
        crawl_config = {}

        # 应用高级配置
        if template_config.advanced:
            if template_config.advanced.delay > 0:
                crawl_config["delay"] = template_config.advanced.delay

        # 执行基础爬取
        result = await crawler.crawl(url, crawl_config)

        if not result.get("success"):
            return result

        # 艹，现在根据模板字段提取数据
        extracted_data = {}
        # TODO: 实现字段提取逻辑（需要使用CSS选择器或LLM提取）

        # 临时返回原始结果
        result["extracted_data"] = extracted_data
        return result

    def load_template_from_file(self, file_path: Path) -> Optional[TemplateConfigSchema]:
        """
        从文件加载模板
        Load template from file

        Args:
            file_path: 模板文件路径

        Returns:
            TemplateConfigSchema: 模板配置对象，失败返回None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            valid, _, schema = self.validate_template_config(config_data)
            if valid:
                return schema
            else:
                return None

        except Exception as e:
            print(f"艹，加载模板失败 {file_path}: {str(e)}")
            return None

    def save_template_to_file(self, template_config: TemplateConfigSchema, filename: str) -> bool:
        """
        保存模板到文件
        Save template to file

        Args:
            template_config: 模板配置对象
            filename: 文件名

        Returns:
            bool: 是否成功
        """
        try:
            file_path = self.templates_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(template_config.dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"艹，保存模板失败: {str(e)}")
            return False

    def list_custom_templates(self) -> list[str]:
        """
        列出自定义模板文件
        List custom template files

        Returns:
            list: 模板文件名列表
        """
        try:
            template_files = list(self.templates_dir.glob("*.json"))
            return [f.name for f in template_files]
        except Exception:
            return []


# ==================== 基础场景类 ====================

class BaseScenario(ABC):
    """
    基础场景类（抽象基类）
    Base Scenario Class (Abstract Base Class)

    所有场景模板都必须继承这个类并实现extract方法
    All scenario templates must inherit this class and implement extract method
    """

    def __init__(self):
        self._config_schema: Optional[TemplateConfigSchema] = None

    @abstractmethod
    def get_schema(self) -> TemplateConfigSchema:
        """
        获取场景配置Schema（子类必须实现）
        Get scenario configuration schema (must be implemented by subclasses)

        Returns:
            TemplateConfigSchema: 场景配置对象
        """
        pass

    @abstractmethod
    async def extract(self, url: str, crawler: Crawl4AIWrapper) -> dict[str, Any]:
        """
        执行数据提取（子类必须实现）
        Execute data extraction (must be implemented by subclasses)

        Args:
            url: 目标URL
            crawler: Crawl4AI封装实例

        Returns:
            dict: 提取结果
        """
        pass

    def validate(self) -> tuple[bool, str]:
        """
        验证场景配置
        Validate scenario configuration

        Returns:
            tuple: (是否有效, 错误信息)
        """
        try:
            schema = self.get_schema()
            # 基础验证
            if not schema.name:
                return False, "场景名称不能为空"
            if not schema.fields:
                return False, "至少需要一个提取字段"
            return True, ""
        except Exception as e:
            return False, f"验证失败: {str(e)}"

    @property
    def config_schema(self) -> TemplateConfigSchema:
        """获取配置Schema（懒加载）"""
        if self._config_schema is None:
            self._config_schema = self.get_schema()
        return self._config_schema
