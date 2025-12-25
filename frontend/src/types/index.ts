/**
 * TypeScript类型定义
 * TypeScript Type Definitions
 *
 * 艹，集中管理所有类型，别tm到处重复定义！
 */

// ==================== 任务相关类型 ====================

/**
 * 任务状态枚举
 */
export enum TaskStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

/**
 * 任务数据结构
 */
export interface Task {
  id: number
  url: string
  template_id?: number
  status: TaskStatus
  config?: CrawlConfig
  result?: CrawlResult
  error_message?: string
  created_at: string
  completed_at?: string
}

/**
 * 爬取配置
 */
export interface CrawlConfig {
  // 浏览器配置
  browser_config?: {
    headless?: boolean
    user_agent?: string
    viewport?: {
      width: number
      height: number
    }
  }
  // 爬取配置
  crawler_config?: {
    word_count_threshold?: number
    extraction_strategy?: string
    cache_mode?: string
  }
  // 高级配置
  advanced?: {
    deep_crawl?: boolean
    max_pages?: number
    strategy?: 'bfs' | 'dfs'
    proxy?: string
    delay?: number
  }
}

/**
 * 爬取结果
 */
export interface CrawlResult {
  // Markdown输出
  markdown?: string
  fit_markdown?: string
  // 提取的内容
  extracted_content?: string
  // 链接
  links?: {
    internal: string[]
    external: string[]
  }
  // 元数据
  metadata?: {
    title?: string
    description?: string
    keywords?: string[]
  }
  // 媒体
  media?: {
    images: string[]
    videos: string[]
    audio: string[]
  }
  // 截图（Base64）
  screenshot?: string
}

// ==================== 模板相关类型 ====================

/**
 * 模板分类枚举
 */
export enum TemplateCategory {
  NEWS = 'news',
  DOCS = 'docs',
  ECOMMERCE = 'ecommerce',
  ACADEMIC = 'academic',
  TABLE = 'table',
  CUSTOM = 'custom',
}

/**
 * 模板数据结构
 */
export interface Template {
  id: number
  name: string
  description?: string
  category: TemplateCategory
  config_schema: TemplateConfigSchema
  is_builtin: boolean
  created_at: string
  updated_at: string
}

/**
 * 模板配置Schema
 */
export interface TemplateConfigSchema {
  // 提取字段
  fields: ExtractField[]
  // 高级配置
  advanced?: {
    // 深度爬取
    deep_crawl?: boolean
    max_pages?: number
    strategy?: 'bfs' | 'dfs'
    // 代理
    proxy?: string
    // 限流
    delay?: number
    // 滚动加载
    scroll_to_load?: boolean
    max_scrolls?: number
  }
}

/**
 * 提取字段
 */
export interface ExtractField {
  name: string
  selector: string
  type: 'text' | 'number' | 'link' | 'image' | 'attribute'
  attribute?: string  // 当type为attribute时使用
  required?: boolean
  multiple?: boolean  // 是否提取多个值
}

// ==================== 教程相关类型 ====================

/**
 * 教程分类枚举
 */
export enum TutorialCategory {
  BEGINNER = 'beginner',
  INTERMEDIATE = 'intermediate',
  ADVANCED = 'advanced',
}

/**
 * 教程数据结构
 */
export interface Tutorial {
  id: number
  title: string
  content: string
  step_order: number
  category: TutorialCategory
  code_example?: {
    python?: string
    bash?: string
  }
  extra_data?: Record<string, any>
  created_at: string
}

// ==================== API响应类型 ====================

/**
 * 通用API响应
 */
export interface ApiResponse<T = any> {
  success: boolean
  message?: string
  data?: T
  error?: string
}

/**
 * 分页响应
 */
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

// ==================== UI状态类型 ====================

/**
 * 加载状态
 */
export interface LoadingState {
  loading: boolean
  error?: string
}

/**
 * 表单状态
 */
export interface FormState<T = any> {
  data: T
  errors: Record<string, string>
  touched: Record<string, boolean>
}

// ==================== 监控相关类型 ====================

/**
 * 系统统计
 */
export interface SystemStats {
  total_tasks: number
  running_tasks: number
  completed_tasks: number
  failed_tasks: number
  total_templates: number
  custom_templates: number
}

/**
 * 任务过滤器
 */
export interface TaskFilter {
  status?: TaskStatus
  template_id?: number
  date_from?: string
  date_to?: string
  search?: string
}
