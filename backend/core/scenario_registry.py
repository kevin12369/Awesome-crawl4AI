"""
场景注册中心
Scenario Registry

这个SB模块负责管理和注册所有场景模板
This module manages and registers all scenario templates
"""

from typing import Dict, Type, Optional, List
from pathlib import Path

from .template_engine import BaseScenario, TemplateConfigSchema


class ScenarioRegistry:
    """
    场景注册中心
    Scenario Registry

    艹，这是所有场景的中央仓库，统一管理！
    """

    def __init__(self):
        """初始化注册中心"""
        self._scenarios: Dict[str, Type[BaseScenario]] = {}
        self._instances: Dict[str, BaseScenario] = {}

    def register(self, scenario_class: Type[BaseScenario]) -> None:
        """
        注册场景类
        Register scenario class

        Args:
            scenario_class: 场景类（不是实例！）

        Raises:
            ValueError: 如果场景名称已存在
        """
        # 创建临时实例获取配置
        temp_instance = scenario_class()
        schema = temp_instance.get_schema()

        name = schema.name

        if name in self._scenarios:
            raise ValueError(f'艹，场景 "{name}" 已经注册了！换个名字吧！')

        # 验证场景
        valid, error_msg = temp_instance.validate()
        if not valid:
            raise ValueError(f'艹，场景 "{name}" 验证失败: {error_msg}')

        # 注册
        self._scenarios[name] = scenario_class
        print(f'✅ 场景已注册: {name}')

    def get_scenario(self, name: str) -> Optional[BaseScenario]:
        """
        获取场景实例
        Get scenario instance

        Args:
            name: 场景名称

        Returns:
            BaseScenario: 场景实例，不存在返回None
        """
        if name not in self._scenarios:
            return None

        # 懒加载实例
        if name not in self._instances:
            scenario_class = self._scenarios[name]
            self._instances[name] = scenario_class()

        return self._instances[name]

    def get_all_scenarios(self) -> List[TemplateConfigSchema]:
        """
        获取所有场景的配置Schema
        Get all scenario configuration schemas

        Returns:
            list: 场景配置列表
        """
        schemas = []
        for name, scenario_class in self._scenarios.items():
            if name not in self._instances:
                self._instances[name] = scenario_class()
            schema = self._instances[name].get_schema()
            schemas.append(schema)

        return schemas

    def get_scenario_names(self) -> List[str]:
        """
        获取所有场景名称
        Get all scenario names

        Returns:
            list: 场景名称列表
        """
        return list(self._scenarios.keys())

    def has_scenario(self, name: str) -> bool:
        """
        检查场景是否存在
        Check if scenario exists

        Args:
            name: 场景名称

        Returns:
            bool: 是否存在
        """
        return name in self._scenarios

    def unregister(self, name: str) -> bool:
        """
        注销场景（谨慎使用！）
        Unregister scenario (use with caution!)

        Args:
            name: 场景名称

        Returns:
            bool: 是否成功
        """
        if name in self._scenarios:
            del self._scenarios[name]
            if name in self._instances:
                del self._instances[name]
            print(f'🗑️  场景已注销: {name}')
            return True
        return False

    def get_scenarios_by_category(self, category: str) -> List[TemplateConfigSchema]:
        """
        按分类获取场景
        Get scenarios by category

        Args:
            category: 分类名称（custom表示用户自定义）

        Returns:
            list: 该分类下的场景列表
        """
        all_scenarios = self.get_all_scenarios()

        # 艹，目前没有category字段，暂时通过名称前缀判断
        # 后续可以给TemplateConfigSchema添加category字段
        if category == "custom":
            return [s for s in all_scenarios if s.name.startswith("custom_")]
        elif category == "builtin":
            return [s for s in all_scenarios if not s.name.startswith("custom_")]
        else:
            # 精确匹配
            return [s for s in all_scenarios if s.name.startswith(f"{category}_")]

    def clear(self) -> None:
        """
        清空所有注册的场景（谨慎使用！）
        Clear all registered scenarios (use with caution!)
        """
        self._scenarios.clear()
        self._instances.clear()
        print('🗑️  所有场景已清空')

    def count(self) -> int:
        """
        获取已注册场景数量
        Get count of registered scenarios

        Returns:
            int: 场景数量
        """
        return len(self._scenarios)


# ==================== 全局注册中心实例 ====================

# 艹，全局唯一注册中心，别tm到处创建新实例！
_global_registry: Optional[ScenarioRegistry] = None


def get_registry() -> ScenarioRegistry:
    """
    获取全局注册中心实例（单例模式）
    Get global registry instance (singleton)

    Returns:
        ScenarioRegistry: 全局注册中心
    """
    global _global_registry
    if _global_registry is None:
        _global_registry = ScenarioRegistry()
    return _global_registry


def register_scenario(scenario_class: Type[BaseScenario]) -> None:
    """
    注册场景的便捷函数（装饰器）
    Convenience function to register scenario (decorator)

    使用方式:
        @register_scenario
        class MyNewsCrawler(BaseScenario):
            ...

    Args:
        scenario_class: 场景类
    """
    registry = get_registry()
    registry.register(scenario_class)
    return scenario_class


# ==================== 场景发现和自动注册 ====================

def auto_register_scenarios(scenarios_dir: Optional[Path] = None) -> None:
    """
    自动发现并注册场景模块
    Auto-discover and register scenario modules

    Args:
        scenarios_dir: 场景模块目录路径
    """
    if scenarios_dir is None:
        scenarios_dir = Path(__file__).parent.parent / "scenarios"

    if not scenarios_dir.exists():
        return

    # 艹，动态导入场景模块
    import importlib
    import sys

    # 添加到Python路径
    if str(scenarios_dir.parent) not in sys.path:
        sys.path.insert(0, str(scenarios_dir.parent))

    # 遍历Python文件
    for py_file in scenarios_dir.glob("*.py"):
        if py_file.name.startswith("_"):
            continue

        # 动态导入
        module_name = f"scenarios.{py_file.stem}"
        try:
            importlib.import_module(module_name)
        except Exception as e:
            print(f'艹，导入场景模块失败 {module_name}: {str(e)}')


# ==================== 测试代码 ====================

if __name__ == "__main__":
    from .template_engine import BaseScenario, TemplateConfigSchema, ExtractField

    # 测试场景
    class TestNewsCrawler(BaseScenario):
        """测试新闻爬虫"""

        def get_schema(self) -> TemplateConfigSchema:
            return TemplateConfigSchema(
                name="test_news",
                description="测试新闻爬虫",
                fields=[
                    ExtractField(name="title", selector="h1", type="text", required=True),
                    ExtractField(name="content", selector="article", type="text", required=True),
                ],
            )

        async def extract(self, url: str, crawler) -> dict:
            return {"test": "data"}

    # 测试注册
    registry = get_registry()

    # 装饰器方式注册
    @register_scenario
    class TestNewsCrawler2(BaseScenario):
        def get_schema(self) -> TemplateConfigSchema:
            return TemplateConfigSchema(
                name="test_news2",
                description="测试新闻爬虫2",
                fields=[],
            )

        async def extract(self, url: str, crawler) -> dict:
            return {}

    # 查询
    print(f"已注册场景: {registry.get_scenario_names()}")
    print(f"场景数量: {registry.count()}")
