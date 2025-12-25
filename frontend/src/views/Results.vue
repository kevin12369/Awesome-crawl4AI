<!--
  结果展示页面
  Results Page

  艹，展示爬取结果，支持Markdown预览和数据导出！
-->
<template>
  <div class="results-page">
    <el-page-header @back="$router.back()" title="返回">
      <template #content>
        爬取结果 #{{ taskId }}
      </template>
    </el-page-header>

    <el-card v-if="crawlStore.loading.current" class="loading-card" shadow="never">
      <el-skeleton :rows="5" animated />
    </el-card>

    <el-card v-else-if="task" class="result-card" shadow="never">
      <!-- 任务信息 -->
      <el-descriptions :column="2" border>
        <el-descriptions-item label="目标URL">
          {{ task.url }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(task.status)">
            {{ getStatusText(task.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ formatTime(task.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="完成时间" v-if="task.completed_at">
          {{ formatTime(task.completed_at) }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- 错误信息 -->
      <el-alert
        v-if="task.status === 'failed' && task.error_message"
        type="error"
        :title="task.error_message"
        :closable="false"
        style="margin: 20px 0"
      />

      <!-- 结果内容 -->
      <template v-if="task.status === 'completed' && task.result">
        <el-tabs v-model="activeTab" style="margin-top: 20px">
          <!-- Markdown预览 -->
          <el-tab-pane label="Markdown" name="markdown">
            <div class="markdown-preview" v-html="renderedMarkdown"></div>
          </el-tab-pane>

          <!-- JSON数据 -->
          <el-tab-pane label="JSON" name="json">
            <pre class="json-preview">{{ JSON.stringify(task.result, null, 2) }}</pre>
          </el-tab-pane>

          <!-- 元数据 -->
          <el-tab-pane label="元数据" name="metadata">
            <el-descriptions :column="1" border v-if="task.result.metadata">
              <el-descriptions-item label="标题">
                {{ task.result.metadata.title }}
              </el-descriptions-item>
              <el-descriptions-item label="描述">
                {{ task.result.metadata.description }}
              </el-descriptions-item>
            </el-descriptions>
          </el-tab-pane>
        </el-tabs>

        <!-- 导出按钮 -->
        <div class="export-actions">
          <el-button @click="exportMarkdown">
            <el-icon><Download /></el-icon>
            导出 Markdown
          </el-button>
          <el-button @click="exportJson">
            <el-icon><Download /></el-icon>
            导出 JSON
          </el-button>
        </div>
      </template>
    </el-card>

    <el-card v-else class="empty-card" shadow="never">
      <el-empty description="任务不存在" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import { Download } from '@element-plus/icons-vue'
import type { Task } from '@/types'
import { useCrawlStore } from '@/stores/crawl'

// Route
const route = useRoute()
const taskId = computed(() => Number(route.params.taskId))

// Store
const crawlStore = useCrawlStore()

// 当前任务
const task = ref<Task | null>(null)

// 活动标签页
const activeTab = ref('markdown')

// 渲染的Markdown
const renderedMarkdown = computed(() => {
  if (!task.value?.result?.markdown) return ''
  return marked(task.value.result.markdown)
})

// 获取状态类型
const getStatusType = (status: string) => {
  const types: Record<string, any> = {
    completed: 'success',
    failed: 'danger',
    running: 'warning',
    pending: 'info',
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    completed: '已完成',
    failed: '失败',
    running: '运行中',
    pending: '待执行',
  }
  return texts[status] || status
}

// 格式化时间
const formatTime = (timeStr: string) => {
  return new Date(timeStr).toLocaleString()
}

// 导出Markdown
const exportMarkdown = () => {
  if (!task.value?.result?.markdown) return

  const blob = new Blob([task.value.result.markdown], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `result-${taskId.value}.md`
  a.click()
  URL.revokeObjectURL(url)

  ElMessage.success('Markdown导出成功！')
}

// 导出JSON
const exportJson = () => {
  if (!task.value?.result) return

  const blob = new Blob([JSON.stringify(task.value.result, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `result-${taskId.value}.json`
  a.click()
  URL.revokeObjectURL(url)

  ElMessage.success('JSON导出成功！')
}

// 加载任务
const loadTask = async () => {
  try {
    task.value = await crawlStore.loadTask(taskId.value)
  } catch (error) {
    console.error('加载任务失败:', error)
  }
}

onMounted(() => {
  loadTask()
})
</script>

<style scoped lang="scss">
.results-page {
  .loading-card,
  .empty-card,
  .result-card {
    margin-top: 20px;
  }

  .markdown-preview {
    padding: 20px;
    background-color: #fafafa;
    border-radius: 4px;
    line-height: 1.8;

    :deep(h1),
    :deep(h2),
    :deep(h3) {
      margin-top: 24px;
      margin-bottom: 16px;
    }

    :deep(p) {
      margin-bottom: 12px;
    }

    :deep(code) {
      background-color: #f5f5f5;
      padding: 2px 6px;
      border-radius: 3px;
    }

    :deep(pre) {
      background-color: #2d2d2d;
      color: #ccc;
      padding: 16px;
      border-radius: 4px;
      overflow-x: auto;
    }
  }

  .json-preview {
    padding: 20px;
    background-color: #f5f7fa;
    border-radius: 4px;
    font-size: 13px;
    line-height: 1.6;
    overflow-x: auto;
  }

  .export-actions {
    margin-top: 20px;
    display: flex;
    gap: 12px;
    justify-content: flex-end;
  }
}
</style>
