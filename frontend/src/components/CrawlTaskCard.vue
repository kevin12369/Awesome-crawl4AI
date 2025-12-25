<!--
  爬取任务卡片组件
  Crawl Task Card Component

  展示单个爬取任务的信息和状态
  Display information and status of a single crawl task
-->
<template>
  <el-card class="task-card" :class="`status-${task.status}`" shadow="hover">
    <!-- 卡片头部 -->
    <template #header>
      <div class="card-header">
        <div class="task-info">
          <el-tag :type="getStatusType(task.status)" size="small">
            {{ getStatusText(task.status) }}
          </el-tag>
          <span class="task-url">{{ truncateUrl(task.url) }}</span>
        </div>
        <div class="task-actions">
          <el-button
            v-if="task.status === 'completed'"
            type="primary"
            size="small"
            text
            @click="viewResult"
          >
            <el-icon><View /></el-icon>
          </el-button>
          <el-button
            type="danger"
            size="small"
            text
            @click="handleDelete"
          >
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>
    </template>

    <!-- 卡片内容 -->
    <div class="card-content">
      <!-- 模板信息 -->
      <div v-if="task.template_id" class="task-meta">
        <el-icon><Collection /></el-icon>
        <span>模板 ID: {{ task.template_id }}</span>
      </div>

      <!-- 创建时间 -->
      <div class="task-meta">
        <el-icon><Clock /></el-icon>
        <span>{{ formatTime(task.created_at) }}</span>
      </div>

      <!-- 错误信息 -->
      <el-alert
        v-if="task.status === 'failed' && task.error_message"
        type="error"
        :closable="false"
        show-icon
        class="error-alert"
      >
        {{ task.error_message }}
      </el-alert>

      <!-- 执行时间 -->
      <div v-if="task.completed_at" class="task-meta">
        <el-icon><Timer /></el-icon>
        <span>耗时: {{ getDuration(task.created_at, task.completed_at) }}</span>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { View, Delete, Collection, Clock, Timer } from '@element-plus/icons-vue'
import type { Task } from '@/types'
import { useCrawlStore } from '@/stores/crawl'

// Props
const props = defineProps<{
  task: Task
}>()

// Router
const router = useRouter()

// Store
const crawlStore = useCrawlStore()

// 获取状态类型
const getStatusType = (status: string) => {
  const types: Record<string, any> = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger',
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '待执行',
    running: '执行中',
    completed: '已完成',
    failed: '失败',
  }
  return texts[status] || status
}

// 截断URL
const truncateUrl = (url: string) => {
  if (url.length > 50) {
    return url.substring(0, 50) + '...'
  }
  return url
}

// 格式化时间
const formatTime = (timeStr: string) => {
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return date.toLocaleDateString()
}

// 计算耗时
const getDuration = (start: string, end: string) => {
  const startDate = new Date(start)
  const endDate = new Date(end)
  const diff = endDate.getTime() - startDate.getTime()

  if (diff < 1000) return `${diff}ms`
  if (diff < 60000) return `${Math.floor(diff / 1000)}s`
  return `${Math.floor(diff / 60000)}m ${Math.floor((diff % 60000) / 1000)}s`
}

// 查看结果
const viewResult = () => {
  router.push(`/results/${props.task.id}`)
}

// 删除任务
const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这个任务吗？', '确认删除', {
      type: 'warning',
    })

    await crawlStore.deleteTask(props.task.id)
  } catch (error) {
    // 用户取消或删除失败
    if (error !== 'cancel') {
      console.error('删除任务失败:', error)
    }
  }
}
</script>

<style scoped lang="scss">
.task-card {
  margin-bottom: 16px;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-2px);
  }

  &.status-running {
    border-left: 4px solid #E6A23C;
  }

  &.status-completed {
    border-left: 4px solid #67C23A;
  }

  &.status-failed {
    border-left: 4px solid #F56C6C;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .task-info {
      display: flex;
      align-items: center;
      gap: 8px;
      flex: 1;

      .task-url {
        font-size: 14px;
        color: #606266;
      }
    }

    .task-actions {
      display: flex;
      gap: 4px;
    }
  }

  .card-content {
    .task-meta {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      color: #909399;
      margin-bottom: 8px;

      &:last-child {
        margin-bottom: 0;
      }
    }

    .error-alert {
      margin: 12px 0;
    }
  }
}
</style>
