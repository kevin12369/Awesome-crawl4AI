/**
 * Template Store 测试
 * Template Store Tests
 *
 * 艹，测试模板状态管理！
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useTemplateStore } from '../template'

// Mock API client / Mock API 客户端
vi.mock('../api/template', () => ({
  getTemplates: vi.fn(),
  createTemplate: vi.fn(),
  updateTemplate: vi.fn(),
  deleteTemplate: vi.fn(),
  validateTemplate: vi.fn(),
}))

import { getTemplates, createTemplate, updateTemplate, deleteTemplate, validateTemplate } from '../api/template'

describe('Template Store', () => {
  let templateStore: ReturnType<typeof useTemplateStore>

  beforeEach(() => {
    setActivePinia(createPinia())
    templateStore = useTemplateStore()
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('初始状态 / Initial State', () => {
    it('应该有正确的初始状态 / should have correct initial state', () => {
      expect(templateStore.templates).toEqual([])
      expect(templateStore.currentTemplate).toBeNull()
      expect(templateStore.loading).toBe(false)
      expect(templateStore.categoryFilter).toBe('all')
    })

    it('stats 应该返回正确的初始统计 / stats should return correct initial stats', () => {
      const stats = templateStore.stats
      expect(stats.total).toBe(0)
      expect(stats.builtin).toBe(0)
      expect(stats.custom).toBe(0)
    })
  })

  describe('loadTemplates / 加载模板列表', () => {
    it('应该成功加载模板 / should load templates successfully', async () => {
      const mockTemplates = [
        { id: 1, name: 'news_crawler', is_builtin: true, category: 'news' },
        { id: 2, name: 'custom_template', is_builtin: false, category: 'custom' },
      ]

      vi.mocked(getTemplates).mockResolvedValue({
        code: 200,
        message: 'success',
        data: {
          total: 2,
          templates: mockTemplates,
        },
      })

      await templateStore.loadTemplates()

      expect(getTemplates).toHaveBeenCalled()
      expect(templateStore.templates).toEqual(mockTemplates)
    })

    it('应该按分类过滤 / should filter by category', async () => {
      const mockTemplates = [
        { id: 1, name: 'news_crawler', category: 'news', is_builtin: true },
        { id: 2, name: 'docs_archiver', category: 'docs', is_builtin: true },
      ]

      vi.mocked(getTemplates).mockResolvedValue({
        code: 200,
        message: 'success',
        data: {
          total: 2,
          templates: mockTemplates,
        },
      })

      await templateStore.loadTemplates('news')

      expect(getTemplates).toHaveBeenCalledWith({ category: 'news' })
    })
  })

  describe('createTemplate / 创建模板', () => {
    it('应该成功创建模板 / should create template successfully', async () => {
      const newTemplate = {
        name: 'new_template',
        description: 'New template',
        category: 'custom' as const,
        config_schema: {
          name: 'new_template',
          description: 'New template',
          category: 'custom',
          fields: [],
          advanced: {},
        },
      }

      vi.mocked(createTemplate).mockResolvedValue({
        code: 200,
        message: 'success',
        data: { id: 3, ...newTemplate },
      })

      await templateStore.createTemplate(newTemplate)

      expect(createTemplate).toHaveBeenCalledWith(newTemplate)
    })
  })

  describe('updateTemplate / 更新模板', () => {
    it('应该成功更新自定义模板 / should update custom template successfully', async () => {
      const templateId = 1
      const updates = {
        name: 'updated_template',
        description: 'Updated description',
      }

      vi.mocked(updateTemplate).mockResolvedValue({
        code: 200,
        message: 'success',
        data: { id: templateId, ...updates },
      })

      await templateStore.updateTemplate(templateId, updates)

      expect(updateTemplate).toHaveBeenCalledWith(templateId, updates)
    })
  })

  describe('deleteTemplate / 删除模板', () => {
    it('应该成功删除自定义模板 / should delete custom template successfully', async () => {
      const templateId = 1

      vi.mocked(deleteTemplate).mockResolvedValue({
        code: 200,
        message: 'success',
        data: null,
      })

      // 先添加模板 / Add template first
      templateStore.templates = [
        { id: templateId, name: 'to_delete', is_builtin: false, category: 'custom' },
      ]

      await templateStore.deleteTemplate(templateId)

      expect(deleteTemplate).toHaveBeenCalledWith(templateId)
      expect(templateStore.templates.length).toBe(0)
    })

    it('不应该删除内置模板 / should not delete builtin template', async () => {
      const templateId = 1

      vi.mocked(deleteTemplate).mockResolvedValue({
        code: 403,
        message: 'Cannot delete builtin template',
        data: null,
      })

      // 添加内置模板 / Add builtin template
      templateStore.templates = [
        { id: templateId, name: 'builtin', is_builtin: true, category: 'news' },
      ]

      await templateStore.deleteTemplate(templateId)

      // 内置模板不应该被删除 / Builtin template should not be deleted
      expect(templateStore.templates.length).toBe(1)
    })
  })

  describe('validateTemplate / 验证模板', () => {
    it('应该验证有效模板 / should validate valid template', async () => {
      const validSchema = {
        name: 'valid_template',
        fields: [{ name: 'title', selector: 'h1', type: 'text' }],
      }

      vi.mocked(validateTemplate).mockResolvedValue({
        code: 200,
        message: 'success',
        data: {
          valid: true,
          errors: [],
        },
      })

      const result = await templateStore.validateTemplate(validSchema)

      expect(result.valid).toBe(true)
      expect(result.errors).toEqual([])
    })

    it('应该验证无效模板 / should validate invalid template', async () => {
      const invalidSchema = {
        name: '',  // 空名称 / empty name
        fields: [],
      }

      vi.mocked(validateTemplate).mockResolvedValue({
        code: 200,
        message: 'success',
        data: {
          valid: false,
          errors: ['Name cannot be empty'],
        },
      })

      const result = await templateStore.validateTemplate(invalidSchema)

      expect(result.valid).toBe(false)
      expect(result.errors.length).toBeGreaterThan(0)
    })
  })

  describe('computed properties / 计算属性', () => {
    it('builtinTemplates 应该只返回内置模板 / builtinTemplates should return only builtin templates', () => {
      templateStore.templates = [
        { id: 1, name: 'news', is_builtin: true, category: 'news' },
        { id: 2, name: 'custom', is_builtin: false, category: 'custom' },
      ]

      expect(templateStore.builtinTemplates.length).toBe(1)
      expect(templateStore.builtinTemplates[0].name).toBe('news')
    })

    it('customTemplates 应该只返回自定义模板 / customTemplates should return only custom templates', () => {
      templateStore.templates = [
        { id: 1, name: 'news', is_builtin: true, category: 'news' },
        { id: 2, name: 'custom', is_builtin: false, category: 'custom' },
      ]

      expect(templateStore.customTemplates.length).toBe(1)
      expect(templateStore.customTemplates[0].name).toBe('custom')
    })

    it('templatesByCategory 应该按分类分组 / templatesByCategory should group by category', () => {
      templateStore.templates = [
        { id: 1, name: 'news', category: 'news', is_builtin: true },
        { id: 2, name: 'news2', category: 'news', is_builtin: true },
        { id: 3, name: 'docs', category: 'docs', is_builtin: true },
      ]

      const byCategory = templateStore.templatesByCategory
      expect(byCategory['news'].length).toBe(2)
      expect(byCategory['docs'].length).toBe(1)
    })
  })
})
