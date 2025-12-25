/**
 * 爬取状态管理
 * Crawl State Management
 *
 * 艹，所有爬取相关的状态都在这！
 */

import { defineStore } from 'pinia'
import { ref, reactive, computed } from 'vue'
import type { Task, TaskFilter, CrawlConfig } from '@/types'
import * as crawlApi from '@/api/crawl'

export const useCrawlStore = defineStore('crawl', () => {
  // ==================== 状态 ====================

  // 任务列表
  const tasks = ref<Task[]>([])

  // 当前任务（正在查看的任务）
  const currentTask = ref<Task | null>(null)

  // 加载状态
  const loading = reactive({
    tasks: false,
    current: false,
    creating: false,
  })

  // 过滤器
  const filter = ref<TaskFilter>({})

  // 错误信息
  const error = ref<string | null>(null)

  // ==================== 计算属性 ====================

  // 总任务数
  const totalCount = computed(() => tasks.value.length)

  // 运行中的任务
  const runningTasks = computed(() =>
    tasks.value.filter(t => t.status === 'running')
  )

  // 已完成的任务
  const completedTasks = computed(() =>
    tasks.value.filter(t => t.status === 'completed')
  )

  // 失败的任务
  const failedTasks = computed(() =>
    tasks.value.filter(t => t.status === 'failed')
  )

  // 统计信息
  const stats = computed(() => ({
    total: totalCount.value,
    running: runningTasks.value.length,
    completed: completedTasks.value.length,
    failed: failedTasks.value.length,
  }))

  // ==================== 操作 ====================

  /**
   * 加载任务列表
   */
  async function loadTasks() {
    loading.tasks = true
    error.value = null

    try {
      const response = await crawlApi.getTasks(filter.value)
      tasks.value = response.data?.items || []
    } catch (err: any) {
      error.value = err.message || '加载任务列表失败'
      console.error('加载任务列表失败:', err)
    } finally {
      loading.tasks = false
    }
  }

  /**
   * 加载单个任务
   */
  async function loadTask(taskId: number) {
    loading.current = true
    error.value = null

    try {
      const response = await crawlApi.getTask(taskId)
      currentTask.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message || '加载任务失败'
      console.error('加载任务失败:', err)
      throw err
    } finally {
      loading.current = false
    }
  }

  /**
   * 创建爬取任务
   */
  async function createCrawl(
    url: string,
    templateId?: number,
    config?: CrawlConfig
  ) {
    loading.creating = true
    error.value = null

    try {
      const response = await crawlApi.createCrawlTask(url, templateId, config)

      // 艹，创建成功后刷新列表
      await loadTasks()

      return response.data
    } catch (err: any) {
      error.value = err.message || '创建任务失败'
      console.error('创建任务失败:', err)
      throw err
    } finally {
      loading.creating = false
    }
  }

  /**
   * 批量爬取
   */
  async function batchCrawl(
    urls: string[],
    templateId?: number,
    config?: CrawlConfig,
    maxConcurrent = 5
  ) {
    loading.creating = true
    error.value = null

    try {
      const response = await crawlApi.batchCrawl(
        urls,
        templateId,
        config,
        maxConcurrent
      )

      // 刷新列表
      await loadTasks()

      return response.data
    } catch (err: any) {
      error.value = err.message || '批量爬取失败'
      console.error('批量爬取失败:', err)
      throw err
    } finally {
      loading.creating = false
    }
  }

  /**
   * 删除任务
   */
  async function deleteTask(taskId: number) {
    error.value = null

    try {
      await crawlApi.deleteTask(taskId)

      // 从列表中移除
      const index = tasks.value.findIndex(t => t.id === taskId)
      if (index !== -1) {
        tasks.value.splice(index, 1)
      }

      // 如果删除的是当前任务
      if (currentTask.value?.id === taskId) {
        currentTask.value = null
      }
    } catch (err: any) {
      error.value = err.message || '删除任务失败'
      console.error('删除任务失败:', err)
      throw err
    }
  }

  /**
   * 更新过滤器
   */
  function updateFilter(newFilter: Partial<TaskFilter>) {
    filter.value = { ...filter.value, ...newFilter }
  }

  /**
   * 重置过滤器
   */
  function resetFilter() {
    filter.value = {}
  }

  /**
   * 清空错误
   */
  function clearError() {
    error.value = null
  }

  // ==================== 返回 ====================

  return {
    // 状态
    tasks,
    currentTask,
    loading,
    filter,
    error,

    // 计算属性
    totalCount,
    runningTasks,
    completedTasks,
    failedTasks,
    stats,

    // 操作
    loadTasks,
    loadTask,
    createCrawl,
    batchCrawl,
    deleteTask,
    updateFilter,
    resetFilter,
    clearError,
  }
})
