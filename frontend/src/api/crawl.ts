/**
 * 爬取API客户端
 * Crawl API Client
 *
 * 处理所有爬取相关的API请求
 * Handle all crawl-related API requests
 */

import client from './client'
import type {
  CrawlConfig,
  CrawlResult,
  Task,
  TaskFilter,
  ApiResponse,
} from '@/types'

/**
 * 创建爬取任务
 * Create crawl task
 */
export async function createCrawlTask(
  url: string,
  templateId?: number,
  config?: CrawlConfig
): Promise<ApiResponse<{ task_id: number; result?: CrawlResult }>> {
  return client.post('/crawl', {
    url,
    template_id: templateId,
    config,
  })
}

/**
 * 批量爬取
 * Batch crawl
 */
export async function batchCrawl(
  urls: string[],
  templateId?: number,
  config?: CrawlConfig,
  maxConcurrent = 5
): Promise<
  ApiResponse<{
    total: number
    completed: number
    failed: number
    task_ids: number[]
  }>
> {
  return client.post('/crawl/batch', {
    urls,
    template_id: templateId,
    config,
    max_concurrent: maxConcurrent,
  })
}

/**
 * 获取任务列表
 * Get task list
 */
export async function getTasks(
  filter?: TaskFilter
): Promise<ApiResponse<{ items: Task[]; total: number }>> {
  return client.get('/crawl/tasks', { params: filter })
}

/**
 * 获取任务详情
 * Get task details
 */
export async function getTask(taskId: number): Promise<ApiResponse<Task>> {
  return client.get(`/crawl/tasks/${taskId}`)
}

/**
 * 删除任务
 * Delete task
 */
export async function deleteTask(taskId: number): Promise<ApiResponse<void>> {
  return client.delete(`/crawl/tasks/${taskId}`)
}

/**
 * 轮询任务状态（用于实时更新）
 * Poll task status
 */
export async function pollTaskStatus(
  taskId: number,
  onUpdate: (task: Task) => void,
  interval = 2000
): Promise<() => void> {
  const poll = async () => {
    try {
      const response = await getTask(taskId)
      const task = response.data as Task

      onUpdate(task)

      // 如果任务完成或失败，停止轮询
      if (task.status === 'completed' || task.status === 'failed') {
        return true
      }

      return false
    } catch (error) {
      console.error('轮询任务状态失败:', error)
      return true // 出错也停止轮询
    }
  }

  const timerId = setInterval(async () => {
    const shouldStop = await poll()
    if (shouldStop) {
      clearInterval(timerId)
    }
  }, interval)

  // 返回取消函数
  return () => clearInterval(timerId)
}
