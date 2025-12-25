/**
 * 模板API客户端
 * Template API Client
 *
 * 处理场景模板的CRUD操作
 * Handle CRUD operations for scenario templates
 */

import client from './client'
import type {
  Template,
  TemplateConfigSchema,
  ApiResponse,
} from '@/types'

/**
 * 获取模板列表
 * Get template list
 */
export async function getTemplates(
  category?: string,
  isBuiltin?: boolean
): Promise<ApiResponse<{ items: Template[]; total: number }>> {
  return client.get('/templates', {
    params: { category, is_builtin: isBuiltin },
  })
}

/**
 * 获取单个模板
 * Get single template
 */
export async function getTemplate(
  templateId: number
): Promise<ApiResponse<Template>> {
  return client.get(`/templates/${templateId}`)
}

/**
 * 创建模板
 * Create template
 */
export async function createTemplate(
  name: string,
  description: string,
  category: string,
  configSchema: TemplateConfigSchema
): Promise<ApiResponse<Template>> {
  return client.post('/templates', {
    name,
    description,
    category,
    config_schema: configSchema,
  })
}

/**
 * 更新模板
 * Update template
 */
export async function updateTemplate(
  templateId: number,
  updates: Partial<{
    name: string
    description: string
    category: string
    config_schema: TemplateConfigSchema
  }>
): Promise<ApiResponse<Template>> {
  return client.put(`/templates/${templateId}`, updates)
}

/**
 * 删除模板
 * Delete template
 */
export async function deleteTemplate(
  templateId: number
): Promise<ApiResponse<void>> {
  return client.delete(`/templates/${templateId}`)
}

/**
 * 验证模板配置
 * Validate template configuration
 */
export async function validateTemplate(
  configSchema: TemplateConfigSchema
): Promise<ApiResponse<{ valid: boolean; message: string; errors?: string[] }>> {
  return client.post('/templates/validate', {
    config_schema: configSchema,
  })
}

/**
 * 获取内置模板列表
 * Get built-in templates
 */
export async function getBuiltinTemplates(): Promise<Template[]> {
  const response = await getTemplates(undefined, true)
  return response.data?.items || []
}

/**
 * 获取自定义模板列表
 * Get custom templates
 */
export async function getCustomTemplates(): Promise<Template[]> {
  const response = await getTemplates(undefined, false)
  return response.data?.items || []
}
