/**
 * Vitest 配置文件
 * Vitest Configuration
 *
 * 艹，前端测试框架配置！
 */

import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  test: {
    // 测试环境 / Test environment
    environment: 'jsdom',

    // 全局配置 / Global configuration
    globals: true,

    // 覆盖率配置 / Coverage configuration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData',
        '**/test/**',
      ],
      // 覆盖率阈值 / Coverage thresholds
      lines: 60,
      functions: 60,
      branches: 60,
      statements: 60,
    },

    // 设置文件 / Setup files
    setupFiles: ['./src/test/setup.ts'],

    // 包含的测试文件模式 / Include test file patterns
    include: ['**/*.{test,spec}.{js,ts,jsx,tsx}'],

    // 排除的文件 / Exclude files
    exclude: ['node_modules', 'dist', '.idea', '.git', '.cache'],

    // 测试超时 / Test timeout
    testTimeout: 10000,

    // 并行执行 / Parallel execution
    threads: true,

    // 显示堆栈 / Show heap
    heap: 'inherit',

    // 监听模式配置 / Watch mode configuration
    watch: true,

    // 报告器 / Reporter
    reporter: ['verbose', 'json', 'html'],
  },

  // 解析配置 / Resolve configuration
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
