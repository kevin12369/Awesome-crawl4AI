/**
 * 模板状态管理
 * Template State Management
 *
 * 艹，所有模板相关的状态都在这！
 */

import { defineStore } from 'pinia'
import { ref, reactive, computed } from 'vue'
import type { Template, TemplateConfigSchema, TemplateCategory } from '@/types'
import * as templateApi from '@/api/template'

export const useTemplateStore = defineStore('template', () => {
  // ==================== 状态 ====================

  // 模板列表
  const templates = ref<Template[]>([])

  // 当前模板（正在编辑/查看的模板）
  const currentTemplate = ref<Template | null>(null)

  // 加载状态
  const loading = reactive({
    templates: false,
    current: false,
    validating: false,
    saving: false,
  })

  // 分类过滤器
  const categoryFilter = ref<TemplateCategory | 'all'>('all')

  // 错误信息
  const error = ref<string | null>(null)

  // ==================== 计算属性 ====================

  // 内置模板
  const builtinTemplates = computed(() =>
    templates.value.filter(t => t.is_builtin)
  )

  // 自定义模板
  const customTemplates = computed(() =>
    templates.value.filter(t => !t.is_builtin)
  )

  // 按分类过滤的模板
  const filteredTemplates = computed(() => {
    if (categoryFilter.value === 'all') {
      return templates.value
    }
    return templates.value.filter(t => t.category === categoryFilter.value)
  })

  // 按分类分组的模板
  const templatesByCategory = computed(() => {
    const groups: Record<string, Template[]> = {}

    templates.value.forEach(template => {
      const category = template.category
      if (!groups[category]) {
        groups[category] = []
      }
      groups[category].push(template)
    })

    return groups
  })

  // 统计信息
  const stats = computed(() => ({
    total: templates.value.length,
    builtin: builtinTemplates.value.length,
    custom: customTemplates.value.length,
  }))

  // ==================== 操作 ====================

  /**
   * 加载所有模板
   */
  async function loadTemplates() {
    loading.templates = true
    error.value = null

    try {
      const response = await templateApi.getTemplates()
      templates.value = response.data?.items || []
    } catch (err: any) {
      error.value = err.message || '加载模板列表失败'
      console.error('加载模板列表失败:', err)
    } finally {
      loading.templates = false
    }
  }

  /**
   * 加载单个模板
   */
  async function loadTemplate(templateId: number) {
    loading.current = true
    error.value = null

    try {
      const response = await templateApi.getTemplate(templateId)
      currentTemplate.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message || '加载模板失败'
      console.error('加载模板失败:', err)
      throw err
    } finally {
      loading.current = false
    }
  }

  /**
   * 创建模板
   */
  async function createTemplate(
    name: string,
    description: string,
    category: string,
    configSchema: TemplateConfigSchema
  ) {
    loading.saving = true
    error.value = null

    try {
      const response = await templateApi.createTemplate(
        name,
        description,
        category,
        configSchema
      )

      // 添加到列表
      if (response.data) {
        templates.value.push(response.data)
      }

      return response.data
    } catch (err: any) {
      error.value = err.message || '创建模板失败'
      console.error('创建模板失败:', err)
      throw err
    } finally {
      loading.saving = false
    }
  }

  /**
   * 更新模板
   */
  async function updateTemplate(
    templateId: number,
    updates: Partial<{
      name: string
      description: string
      category: string
      config_schema: TemplateConfigSchema
    }>
  ) {
    loading.saving = true
    error.value = null

    try {
      const response = await templateApi.updateTemplate(templateId, updates)

      // 更新列表中的模板
      const index = templates.value.findIndex(t => t.id === templateId)
      if (index !== -1 && response.data) {
        templates.value[index] = response.data
      }

      // 如果是当前模板，也更新
      if (currentTemplate.value?.id === templateId && response.data) {
        currentTemplate.value = response.data
      }

      return response.data
    } catch (err: any) {
      error.value = err.message || '更新模板失败'
      console.error('更新模板失败:', err)
      throw err
    } finally {
      loading.saving = false
    }
  }

  /**
   * 删除模板
   */
  async function deleteTemplate(templateId: number) {
    error.value = null

    try {
      await templateApi.deleteTemplate(templateId)

      // 从列表中移除
      const index = templates.value.findIndex(t => t.id === templateId)
      if (index !== -1) {
        templates.value.splice(index, 1)
      }

      // 如果删除的是当前模板
      if (currentTemplate.value?.id === templateId) {
        currentTemplate.value = null
      }
    } catch (err: any) {
      error.value = err.message || '删除模板失败'
      console.error('删除模板失败:', err)
      throw err
    }
  }

  /**
   * 验证模板配置
   */
  async function validateTemplate(
    configSchema: TemplateConfigSchema
  ): Promise<{ valid: boolean; message: string; errors?: string[] }> {
    loading.validating = true
    error.value = null

    try {
      const response = await templateApi.validateTemplate(configSchema)
      return response.data || { valid: false, message: '验证失败' }
    } catch (err: any) {
      const result = {
        valid: false,
        message: err.message || '验证失败',
        errors: [err.message || '未知错误'],
      }
      error.value = result.message
      return result
    } finally {
      loading.validating = false
    }
  }

  /**
   * 更新分类过滤器
   */
  function updateCategoryFilter(category: TemplateCategory | 'all') {
    categoryFilter.value = category
  }

  /**
   * 清空错误
   */
  function clearError() {
    error.value = null
  }

  /**
   * 清空当前模板
   */
  function clearCurrentTemplate() {
    currentTemplate.value = null
  }

  // ==================== 返回 ====================

  return {
    // 状态
    templates,
    currentTemplate,
    loading,
    categoryFilter,
    error,

    // 计算属性
    builtinTemplates,
    customTemplates,
    filteredTemplates,
    templatesByCategory,
    stats,

    // 操作
    loadTemplates,
    loadTemplate,
    createTemplate,
    updateTemplate,
    deleteTemplate,
    validateTemplate,
    updateCategoryFilter,
    clearError,
    clearCurrentTemplate,
  }
})
