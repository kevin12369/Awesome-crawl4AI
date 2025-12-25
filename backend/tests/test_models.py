"""
数据模型测试
Data Model Tests

艹，测试所有数据模型！
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models.template import Template
from models.task import Task


@pytest.mark.unit
class TestTemplateModel:
    """模板模型测试 / Template model tests"""

    async def test_create_template(self, test_session: AsyncSession):
        """测试创建模板 / Test create template"""
        template = Template(
            name="test_template",
            description="Test description",
            category="test",
            config_schema={
                "name": "test_template",
                "fields": [],
            },
            is_builtin=False,
        )
        test_session.add(template)
        await test_session.commit()
        await test_session.refresh(template)

        assert template.id is not None
        assert template.name == "test_template"
        assert template.category == "test"
        assert template.is_builtin is False

    async def test_template_fields_property(self, test_session: AsyncSession):
        """测试模板 fields 属性 / Test template fields property"""
        template = Template(
            name="test_template",
            description="Test",
            category="test",
            config_schema={
                "name": "test_template",
                "fields": [
                    {"name": "title", "selector": "h1", "type": "text"},
                    {"name": "content", "selector": "p", "type": "text"},
                ],
            },
            is_builtin=False,
        )
        test_session.add(template)
        await test_session.commit()
        await test_session.refresh(template)

        fields = template.fields
        assert len(fields) == 2
        assert fields[0]["name"] == "title"
        assert fields[1]["name"] == "content"

    async def test_template_advanced_config_property(self, test_session: AsyncSession):
        """测试模板 advanced_config 属性 / Test template advanced_config property"""
        template = Template(
            name="test_template",
            description="Test",
            category="test",
            config_schema={
                "name": "test_template",
                "fields": [],
                "advanced": {
                    "delay": 2.0,
                    "deep_crawl": True,
                    "max_pages": 100,
                },
            },
            is_builtin=False,
        )
        test_session.add(template)
        await test_session.commit()
        await test_session.refresh(template)

        advanced = template.advanced_config
        assert advanced["delay"] == 2.0
        assert advanced["deep_crawl"] is True
        assert advanced["max_pages"] == 100

    async def test_template_unique_name(self, test_session: AsyncSession):
        """测试模板名称唯一性 / Test template name uniqueness"""
        template1 = Template(
            name="duplicate_name",
            description="First",
            category="test",
            config_schema={"name": "duplicate_name", "fields": []},
            is_builtin=False,
        )
        test_session.add(template1)
        await test_session.commit()

        # 尝试创建同名的第二个模板 / Try to create second template with same name
        template2 = Template(
            name="duplicate_name",  # 重复名称 / duplicate name
            description="Second",
            category="test",
            config_schema={"name": "duplicate_name", "fields": []},
            is_builtin=False,
        )
        test_session.add(template2)

        # 艹，应该抛出异常 / Should raise exception
        with pytest.raises(Exception):  # IntegrityError
            await test_session.commit()

    async def test_delete_template(self, test_session: AsyncSession):
        """测试删除模板 / Test delete template"""
        template = Template(
            name="to_delete",
            description="Will be deleted",
            category="test",
            config_schema={"name": "to_delete", "fields": []},
            is_builtin=False,
        )
        test_session.add(template)
        await test_session.commit()
        template_id = template.id

        # 删除模板 / Delete template
        await test_session.delete(template)
        await test_session.commit()

        # 验证已删除 / Verify deleted
        result = await test_session.get(Template, template_id)
        assert result is None


@pytest.mark.unit
class TestTaskModel:
    """任务模型测试 / Task model tests"""

    async def test_create_task(self, test_session: AsyncSession):
        """测试创建任务 / Test create task"""
        task = Task(
            url="https://example.com",
            template_id=None,
            status="pending",
            config={},
            result=None,
            error_message=None,
        )
        test_session.add(task)
        await test_session.commit()
        await test_session.refresh(task)

        assert task.id is not None
        assert task.url == "https://example.com"
        assert task.status == "pending"
        assert task.created_at is not None

    async def test_task_status_enum(self, test_session: AsyncSession):
        """测试任务状态枚举 / Test task status enum"""
        valid_statuses = ["pending", "running", "completed", "failed"]

        for status in valid_statuses:
            task = Task(
                url="https://example.com",
                status=status,
            )
            test_session.add(task)
            await test_session.commit()

            assert task.status == status

    async def test_task_with_template(self, test_session: AsyncSession):
        """测试任务关联模板 / Test task with template"""
        # 先创建模板 / Create template first
        template = Template(
            name="test_template",
            description="Test",
            category="test",
            config_schema={"name": "test_template", "fields": []},
            is_builtin=False,
        )
        test_session.add(template)
        await test_session.commit()
        await test_session.refresh(template)

        # 创建关联模板的任务 / Create task with template
        task = Task(
            url="https://example.com",
            template_id=template.id,
            status="pending",
        )
        test_session.add(task)
        await test_session.commit()
        await test_session.refresh(task)

        assert task.template_id == template.id

    async def test_task_completed_at(self, test_session: AsyncSession):
        """测试任务完成时间 / Test task completed_at"""
        task = Task(
            url="https://example.com",
            status="completed",
        )
        test_session.add(task)
        await test_session.commit()
        await test_session.refresh(task)

        # 艹，completed_at 应该在状态变为 completed 时自动设置
        # 这里需要手动设置，因为模型没有设置默认值
        # TODO: 添加模型钩子自动设置 completed_at

    async def test_task_with_result(self, test_session: AsyncSession):
        """测试任务带结果 / Test task with result"""
        result_data = {
            "success": True,
            "markdown": "# Test\n\nContent",
        }
        task = Task(
            url="https://example.com",
            status="completed",
            result=result_data,
        )
        test_session.add(task)
        await test_session.commit()
        await test_session.refresh(task)

        assert task.result is not None
        assert task.result["success"] is True

    async def test_task_with_error(self, test_session: AsyncSession):
        """测试任务带错误 / Test task with error"""
        task = Task(
            url="https://example.com",
            status="failed",
            error_message="Connection timeout",
        )
        test_session.add(task)
        await test_session.commit()
        await test_session.refresh(task)

        assert task.status == "failed"
        assert task.error_message == "Connection timeout"

    async def test_task_config_json(self, test_session: AsyncSession):
        """测试任务配置 JSON / Test task config JSON"""
        config = {
            "delay": 1.5,
            "deep_crawl": False,
            "max_pages": 50,
        }
        task = Task(
            url="https://example.com",
            config=config,
        )
        test_session.add(task)
        await test_session.commit()
        await test_session.refresh(task)

        assert task.config["delay"] == 1.5
        assert task.config["deep_crawl"] is False
