"""
模板 API 测试
Template API Tests

艹，测试模板管理的所有接口！
"""

import pytest
from httpx import AsyncClient


@pytest.mark.unit
class TestTemplatesAPI:
    """模板 API 测试类 / Template API test class"""

    async def test_get_templates_empty(self, client: AsyncClient):
        """测试获取模板列表（空）/ Test get templates list (empty)"""
        response = await client.get("/api/templates")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        # 艹，内置模板可能存在，所以不检查 total == 0

    async def test_get_templates_with_data(
        self, client: AsyncClient, test_template
    ):
        """测试获取模板列表（有数据）/ Test get templates list with data"""
        response = await client.get("/api/templates")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["total"] >= 1

    async def test_get_template_by_id(self, client: AsyncClient, test_template):
        """测试获取单个模板 / Test get template by ID"""
        response = await client.get(f"/api/templates/{test_template.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["id"] == test_template.id
        assert data["data"]["name"] == test_template.name

    async def test_get_template_not_found(self, client: AsyncClient):
        """测试获取不存在的模板 / Test get non-existent template"""
        response = await client.get("/api/templates/99999")
        assert response.status_code == 404

    async def test_create_template(self, client: AsyncClient):
        """测试创建模板 / Test create template"""
        response = await client.post(
            "/api/templates",
            json={
                "name": "new_template",
                "description": "A new template",
                "category": "custom",
                "config_schema": {
                    "name": "new_template",
                    "description": "A new template",
                    "category": "custom",
                    "fields": [
                        {
                            "name": "title",
                            "selector": "h1",
                            "type": "text",
                            "required": True,
                            "multiple": False,
                        }
                    ],
                    "advanced": {
                        "delay": 1.0,
                        "deep_crawl": False,
                    },
                },
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["name"] == "new_template"

    async def test_create_template_duplicate_name(self, client: AsyncClient, test_template):
        """测试创建模板（重复名称）/ Test create template with duplicate name"""
        response = await client.post(
            "/api/templates",
            json={
                "name": test_template.name,  # 重复名称 / duplicate name
                "description": "Duplicate name template",
                "category": "custom",
                "config_schema": {
                    "name": test_template.name,
                    "fields": [],
                },
            },
        )
        assert response.status_code == 400  # Bad request

    async def test_create_template_invalid_data(self, client: AsyncClient):
        """测试创建模板（无效数据）/ Test create template with invalid data"""
        response = await client.post(
            "/api/templates",
            json={
                "name": "",  # 空名称 / empty name
                "description": "Invalid template",
                "category": "custom",
            },
        )
        assert response.status_code == 422  # Validation error

    async def test_update_template(self, client: AsyncClient, test_template):
        """测试更新模板 / Test update template"""
        response = await client.put(
            f"/api/templates/{test_template.id}",
            json={
                "name": "updated_template",
                "description": "Updated description",
                "category": "custom",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200

    async def test_update_builtin_template(self, client: AsyncClient, test_session):
        """测试更新内置模板（应该失败）/ Test update builtin template (should fail)"""
        # 创建内置模板 / Create builtin template
        from tests.conftest import create_test_template
        builtin_template = await create_test_template(
            test_session,
            name="builtin_template",
            category="test",
        )
        builtin_template.is_builtin = True
        await test_session.commit()

        response = await client.put(
            f"/api/templates/{builtin_template.id}",
            json={"description": "Try to update builtin"},
        )
        assert response.status_code == 403  # Forbidden

    async def test_delete_template(self, client: AsyncClient, test_session):
        """测试删除模板 / Test delete template"""
        from tests.conftest import create_test_template
        template = await create_test_template(test_session)

        response = await client.delete(f"/api/templates/{template.id}")
        assert response.status_code == 200

        # 验证模板已删除 / Verify template is deleted
        response = await client.get(f"/api/templates/{template.id}")
        assert response.status_code == 404

    async def test_delete_builtin_template(self, client: AsyncClient, test_session):
        """测试删除内置模板（应该失败）/ Test delete builtin template (should fail)"""
        from tests.conftest import create_test_template
        builtin_template = await create_test_template(
            test_session,
            name="builtin_to_delete",
            category="test",
        )
        builtin_template.is_builtin = True
        await test_session.commit()

        response = await client.delete(f"/api/templates/{builtin_template.id}")
        assert response.status_code == 403  # Forbidden

    async def test_validate_template_valid(self, client: AsyncClient):
        """测试验证模板（有效）/ Test validate template (valid)"""
        response = await client.post(
            "/api/templates/validate",
            json={
                "config_schema": {
                    "name": "valid_template",
                    "description": "A valid template",
                    "category": "test",
                    "fields": [
                        {
                            "name": "title",
                            "selector": "h1",
                            "type": "text",
                        }
                    ],
                },
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["valid"] is True

    async def test_validate_template_invalid(self, client: AsyncClient):
        """测试验证模板（无效）/ Test validate template (invalid)"""
        response = await client.post(
            "/api/templates/validate",
            json={
                "config_schema": {
                    "name": "",  # 空名称 / empty name
                    "fields": [],  # 空字段 / empty fields
                },
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["valid"] is False
        assert len(data["data"]["errors"]) > 0

    async def test_filter_templates_by_category(
        self, client: AsyncClient, test_template
    ):
        """测试按分类过滤模板 / Test filter templates by category"""
        response = await client.get(
            f"/api/templates?category={test_template.category}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        # 验证返回的模板都是指定分类
        for template in data["data"]["templates"]:
            assert template["category"] == test_template.category
