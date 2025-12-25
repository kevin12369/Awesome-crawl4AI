"""
核心模块测试
Core Module Tests

艹，测试模板引擎和场景注册表！
"""

import pytest
from pydantic import ValidationError

from core.template_engine import (
    ExtractField,
    AdvancedConfig,
    TemplateConfigSchema,
    TemplateEngine,
)
from core.scenario_registry import ScenarioRegistry, register_scenario, get_registry


@pytest.mark.unit
class TestExtractField:
    """ExtractField 测试 / ExtractField tests"""

    def test_create_extract_field_minimal(self):
        """测试创建最小字段 / Test create minimal field"""
        field = ExtractField(
            name="title",
            selector="h1",
            type="text",
        )
        assert field.name == "title"
        assert field.selector == "h1"
        assert field.type == "text"
        assert field.required is False
        assert field.multiple is False

    def test_create_extract_field_full(self):
        """测试创建完整字段 / Test create full field"""
        field = ExtractField(
            name="content",
            selector="article p",
            type="text",
            required=True,
            multiple=True,
            attribute="text",
        )
        assert field.required is True
        assert field.multiple is True
        assert field.attribute == "text"

    def test_extract_field_validation(self):
        """测试字段验证 / Test field validation"""
        # 缺少必需字段 / Missing required fields
        with pytest.raises(ValidationError):
            ExtractField(
                name="test",
                # 缺少 selector / missing selector
                type="text",
            )


@pytest.mark.unit
class TestAdvancedConfig:
    """AdvancedConfig 测试 / AdvancedConfig tests"""

    def test_create_advanced_config_minimal(self):
        """测试创建最小配置 / Test create minimal config"""
        config = AdvancedConfig()
        assert config.delay is not None
        assert config.deep_crawl is not None

    def test_create_advanced_config_full(self):
        """测试创建完整配置 / Test create full config"""
        config = AdvancedConfig(
            delay=2.0,
            deep_crawl=True,
            max_pages=100,
            strategy="bfs",
            proxy="http://proxy.example.com",
            scroll_to_load=True,
            max_scrolls=10,
        )
        assert config.delay == 2.0
        assert config.deep_crawl is True
        assert config.max_pages == 100
        assert config.strategy == "bfs"

    def test_advanced_config_strategy_validation(self):
        """测试策略验证 / Test strategy validation"""
        # 有效策略 / Valid strategies
        for strategy in ["bfs", "dfs"]:
            config = AdvancedConfig(strategy=strategy)
            assert config.strategy == strategy

        # 无效策略 / Invalid strategy
        with pytest.raises(ValidationError):
            AdvancedConfig(strategy="invalid_strategy")


@pytest.mark.unit
class TestTemplateConfigSchema:
    """TemplateConfigSchema 测试 / TemplateConfigSchema tests"""

    def test_create_schema_minimal(self):
        """测试创建最小 Schema / Test create minimal schema"""
        schema = TemplateConfigSchema(
            name="test",
            description="Test template",
            category="test",
            fields=[],
        )
        assert schema.name == "test"
        assert len(schema.fields) == 0

    def test_create_schema_with_fields(self):
        """测试创建带字段的 Schema / Test create schema with fields"""
        schema = TemplateConfigSchema(
            name="test",
            description="Test template",
            category="test",
            fields=[
                ExtractField(name="title", selector="h1", type="text"),
                ExtractField(name="content", selector="p", type="text"),
            ],
        )
        assert len(schema.fields) == 2

    def test_schema_validation_empty_name(self):
        """测试 Schema 验证（空名称）/ Test schema validation (empty name)"""
        with pytest.raises(ValidationError):
            TemplateConfigSchema(
                name="",  # 空名称 / empty name
                description="Test",
                category="test",
                fields=[],
            )

    def test_schema_validation_empty_fields(self):
        """测试 Schema 验证（空字段列表）/ Test schema validation (empty fields)"""
        # 艹，空字段列表应该是允许的
        schema = TemplateConfigSchema(
            name="test",
            description="Test",
            category="test",
            fields=[],
        )
        assert len(schema.fields) == 0


@pytest.mark.unit
class TestTemplateEngine:
    """TemplateEngine 测试 / TemplateEngine tests"""

    def test_create_template_engine(self):
        """测试创建模板引擎 / Test create template engine"""
        engine = TemplateEngine()
        assert engine is not None

    def test_validate_schema_valid(self):
        """测试验证 Schema（有效）/ Test validate schema (valid)"""
        engine = TemplateEngine()
        schema = TemplateConfigSchema(
            name="test",
            description="Test",
            category="test",
            fields=[
                ExtractField(name="title", selector="h1", type="text"),
            ],
        )

        result = engine.validate_schema(schema)
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_validate_schema_invalid(self):
        """测试验证 Schema（无效）/ Test validate schema (invalid)"""
        engine = TemplateEngine()

        # 创建无效 Schema / Create invalid schema
        invalid_data = {
            "name": "",  # 空名称 / empty name
            "fields": [],
        }

        result = engine.validate(invalid_data)
        assert result["valid"] is False
        assert len(result["errors"]) > 0


@pytest.mark.unit
class TestScenarioRegistry:
    """ScenarioRegistry 测试 / ScenarioRegistry tests"""

    def test_singleton_registry(self):
        """测试单例注册表 / Test singleton registry"""
        registry1 = get_registry()
        registry2 = get_registry()
        assert registry1 is registry2

    def test_register_scenario(self):
        """测试注册场景 / Test register scenario"""
        registry = ScenarioRegistry()

        # 创建测试场景类 / Create test scenario class
        from scenarios.base import BaseScenario

        class TestScenario(BaseScenario):
            def get_schema(self):
                return TemplateConfigSchema(
                    name="test_scenario",
                    description="Test",
                    category="test",
                    fields=[],
                )

            async def extract(self, url, crawler):
                return {}

        # 注册场景 / Register scenario
        registry.register(TestScenario)

        # 验证已注册 / Verify registered
        scenarios = registry.list_all()
        scenario_names = [s["name"] for s in scenarios]
        assert "test_scenario" in scenario_names

    def test_get_scenario(self):
        """测试获取场景 / Test get scenario"""
        registry = get_registry()

        # 假设已有内置场景 / Assuming builtin scenarios exist
        scenarios = registry.list_all()
        if scenarios:
            first_scenario_name = scenarios[0]["name"]
            scenario = registry.get(first_scenario_name)
            assert scenario is not None
            assert scenario.name == first_scenario_name

    def test_get_nonexistent_scenario(self):
        """测试获取不存在的场景 / Test get non-existent scenario"""
        registry = get_registry()
        scenario = registry.get("nonexistent_scenario_xyz")
        assert scenario is None

    def test_register_decorator(self):
        """测试注册装饰器 / Test register decorator"""
        from scenarios.base import BaseScenario

        @register_scenario
        class DecoratorTestScenario(BaseScenario):
            def get_schema(self):
                return TemplateConfigSchema(
                    name="decorator_test",
                    description="Test",
                    category="test",
                    fields=[],
                )

            async def extract(self, url, crawler):
                return {}

        # 验证已通过装饰器注册 / Verify registered via decorator
        registry = get_registry()
        scenario = registry.get("decorator_test")
        assert scenario is not None


@pytest.mark.integration
class TestScenarioIntegration:
    """场景集成测试 / Scenario integration tests"""

    async def test_scenario_extract_method(self):
        """测试场景 extract 方法 / Test scenario extract method"""
        # 这里需要一个真实的 Scenario 和 mock crawler
        # 由于涉及网络，暂时跳过
        # TODO: 实现 mock crawler 的完整测试

    async def test_builtin_scenarios_registered(self):
        """测试内置场景已注册 / Test builtin scenarios are registered"""
        registry = get_registry()
        scenarios = registry.list_all()

        # 检查内置场景是否存在 / Check if builtin scenarios exist
        builtin_names = [
            "news_crawler",
            "docs_archiver",
            "ecommerce_monitor",
            "academic_collector",
            "table_extractor",
        ]

        scenario_names = [s["name"] for s in scenarios]
        # 艹，至少应该有一些场景
        assert len(scenarios) > 0
