/**
 * Vitest 测试设置文件
 * Vitest Test Setup
 *
 * 艹，所有测试的公共配置都在这里！
 */

import { vi } from 'vitest'
import { config } from '@vue/test-utils'

// 艹，全局测试配置 / Global test configuration
config.global.mocks = {
  $t: (key: string) => key, // Mock i18n / Mock 国际化
}

// Mock window.matchMedia / Mock 媒体查询
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

// Mock IntersectionObserver / Mock 交叉观察器
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return []
  }
  unobserve() {}
} as any

// Mock ResizeObserver / Mock 调整大小观察器
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
} as any

// Mock localStorage / Mock 本地存储
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
}
global.localStorage = localStorageMock as any

// Mock sessionStorage / Mock 会话存储
const sessionStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
}
global.sessionStorage = sessionStorageMock as any

// ==================== 测试工具函数 / Test Utility Functions ====================

/**
 * 等待下一个 tick / Wait for next tick
 */
export async function tick(): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, 0)
  })
}

/**
 * 等待所有异步更新 / Wait for all async updates
 */
export async function flushPromises(): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, 100)
  })
}

/**
 * Mock 响应 / Mock response
 */
export function mockResponse<T>(data: T, delay = 100): Promise<Response> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        ok: true,
        json: async () => data,
        status: 200,
        statusText: 'OK',
        headers: new Headers(),
      } as Response)
    }, delay)
  })
}

/**
 * Mock 错误响应 / Mock error response
 */
export function mockErrorResponse(
  message: string,
  status = 400
): Promise<Response> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        ok: false,
        json: async () => ({ error: message }),
        status,
        statusText: 'Error',
        headers: new Headers(),
      } as Response)
    }, 100)
  })
}

/**
 * 创建测试用模板数据 / Create test template data
 */
export function createTestTemplate(overrides = {}) {
  return {
    id: 1,
    name: 'test_template',
    description: 'Test template',
    category: 'test' as const,
    config_schema: {
      name: 'test_template',
      description: 'Test template',
      category: 'test',
      fields: [],
      advanced: {},
    },
    is_builtin: false,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    ...overrides,
  }
}

/**
 * 创建测试用任务数据 / Create test task data
 */
export function createTestTask(overrides = {}) {
  return {
    id: 1,
    url: 'https://example.com',
    template_id: 'test_template',
    status: 'completed' as const,
    config: {},
    result: {
      success: true,
      markdown: '# Test\n\nContent',
    },
    error_message: null,
    created_at: new Date().toISOString(),
    completed_at: new Date().toISOString(),
    ...overrides,
  }
}

/**
 * Mock API 响应 / Mock API response
 */
export function mockApiResponse<T>(data: T, code = 200) {
  return {
    code,
    message: 'success',
    data,
  }
}
