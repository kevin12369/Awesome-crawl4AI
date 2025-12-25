/*
 * Vite配置文件
 * Vite Configuration
 *
 * 艹，这个配置让开发服务器能跑起来，还配了后端代理
 */

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],

  // 开发服务器配置
  server: {
    port: 5173,
    host: true,
    // 代理后端API请求（艹，解决跨域问题）
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      // WebSocket代理（实时任务状态）
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      },
    },
  },

  // 路径别名（艹，import不用写一长串../../了）
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },

  // 构建配置
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        // 分包策略（艹，优化加载速度）
        manualChunks: {
          'element-plus': ['element-plus'],
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
        },
      },
    },
  },

  // CSS配置
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/styles/variables.scss" as *;`,
      },
    },
  },
})
