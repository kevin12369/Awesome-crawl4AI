/**
 * Crawl Store 测试
 * Crawl Store Tests
 *
 * 艹，测试爬取状态管理！
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCrawlStore } from '../crawl'

// Mock API client / Mock API 客户端
vi.mock('../api/crawl', () => ({
  createCrawlTask: vi.fn(),
  batchCrawl: vi.fn(),
  getTasks: vi.fn(),
  getTask: vi.fn(),
  deleteTask: vi.fn(),
}))

import { createCrawlTask, batchCrawl, getTasks, getTask, deleteTask } from '../api/crawl'

describe('Crawl Store', () => {
  let crawlStore: ReturnType<typeof useCrawlStore>

  beforeEach(() => {
    // 创建新的 pinia 实例 / Create new pinia instance
    setActivePinia(createPinia())
    crawlStore = useCrawlStore()

    // 清除所有 mock / Clear all mocks
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('初始状态 / Initial State', () => {
    it('应该有正确的初始状态 / should have correct initial state', () => {
      expect(crawlStore.tasks).toEqual([])
      expect(crawlStore.currentTask).toBeNull()
      expect(crawlStore.loading).toBe(false)
      expect(crawlStore.error).toBeNull()
    })

    it('stats 应该返回正确的初始统计 / stats should return correct initial stats', () => {
      const stats = crawlStore.stats
      expect(stats.total).toBe(0)
      expect(stats.running).toBe(0)
      expect(stats.completed).toBe(0)
      expect(stats.failed).toBe(0)
    })
  })

  describe('loadTasks / 加载任务列表', () => {
    it('应该成功加载任务 / should load tasks successfully', async () => {
      const mockTasks = [
        { id: 1, url: 'https://example.com', status: 'completed' },
        { id: 2, url: 'https://example2.com', status: 'pending' },
      ]

      vi.mocked(getTasks).mockResolvedValue({
        code: 200,
        message: 'success',
        data: {
          total: 2,
          tasks: mockTasks,
        },
      })

      await crawlStore.loadTasks()

      expect(getTasks).toHaveBeenCalled()
      expect(crawlStore.tasks).toEqual(mockTasks)
      expect(crawlStore.loading).toBe(false)
    })

    it('应该处理加载失败 / should handle load failure', async () => {
      vi.mocked(getTasks).mockRejectedValue(new Error('Network error'))

      await crawlStore.loadTasks()

      expect(crawlStore.error).toBeTruthy()
      expect(crawlStore.loading).toBe(false)
    })
  })

  describe('createCrawl / 创建爬取任务', () => {
    it('应该成功创建任务 / should create task successfully', async () => {
      const mockTask = {
        id: 1,
        url: 'https://example.com',
        status: 'pending',
      }

      vi.mocked(createCrawlTask).mockResolvedValue({
        code: 200,
        message: 'success',
        data: mockTask,
      })

      await crawlStore.createCrawl('https://example.com')

      expect(createCrawlTask).toHaveBeenCalledWith('https://example.com')
      expect(crawlStore.tasks.length).toBeGreaterThan(0)
    })
  })

  describe('deleteTask / 删除任务', () => {
    it('应该成功删除任务 / should delete task successfully', async () => {
      // 先添加一个任务 / Add a task first
      crawlStore.tasks = [
        { id: 1, url: 'https://example.com', status: 'completed' },
      ]

      vi.mocked(deleteTask).mockResolvedValue({
        code: 200,
        message: 'success',
        data: null,
      })

      await crawlStore.deleteTask(1)

      expect(deleteTask).toHaveBeenCalledWith(1)
      expect(crawlStore.tasks.length).toBe(0)
    })
  })

  describe('updateFilter / 更新过滤器', () => {
    it('应该更新过滤状态 / should update filter state', () => {
      crawlStore.updateFilter('completed')

      expect(crawlStore.filter).toBe('completed')
    })
  })

  describe('computed stats / 计算属性统计', () => {
    it('应该正确计算各状态任务数 / should calculate task counts correctly', () => {
      crawlStore.tasks = [
        { id: 1, status: 'completed' },
        { id: 2, status: 'completed' },
        { id: 3, status: 'running' },
        { id: 4, status: 'failed' },
        { id: 5, status: 'pending' },
      ]

      expect(crawlStore.stats.total).toBe(5)
      expect(crawlStore.stats.completed).toBe(2)
      expect(crawlStore.stats.running).toBe(1)
      expect(crawlStore.stats.failed).toBe(1)
      expect(crawlStore.stats.pending).toBe(1) // pending + running
    })
  })
})
