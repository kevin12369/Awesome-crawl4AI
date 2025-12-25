<!--
  主控面板页面
  Dashboard Page

  艹，这是主界面，展示所有核心功能！
-->
<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <!-- 快速爬取卡片 -->
      <el-col :span="24" :lg="8">
        <el-card class="quick-crawl-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon :size="20" color="#409EFF"><Rocket /></el-icon>
              <span>快速爬取</span>
            </div>
          </template>

          <el-form @submit.prevent="handleQuickCrawl">
            <el-form-item>
              <el-input
                v-model="urlInput"
                placeholder="输入网址，例如：https://example.com"
                size="large"
                clearable
              >
                <template #prepend>
                  <el-icon><Link /></el-icon>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="crawlStore.loading.creating"
                :disabled="!urlInput"
                @click="handleQuickCrawl"
                style="width: 100%"
              >
                <el-icon v-if="!crawlStore.loading.creating"><Play /></el-icon>
                <span>{{ crawlStore.loading.creating ? '爬取中...' : '开始爬取' }}</span>
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 系统统计卡片 -->
      <el-col :span="24" :lg="16">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="stat-card" shadow="hover">
              <el-statistic title="总任务数" :value="crawlStore.stats.total">
                <template #suffix>
                  <el-icon color="#909399"><Document /></el-icon>
                </template>
              </el-statistic>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card" shadow="hover">
              <el-statistic title="运行中" :value="crawlStore.stats.running">
                <template #suffix>
                  <el-icon color="#409EFF"><Loading /></el-icon>
                </template>
              </el-statistic>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card" shadow="hover">
              <el-statistic title="已完成" :value="crawlStore.stats.completed">
                <template #suffix>
                  <el-icon color="#67C23A"><CircleCheck /></el-icon>
                </template>
              </el-statistic>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card" shadow="hover">
              <el-statistic title="失败" :value="crawlStore.stats.failed">
                <template #suffix>
                  <el-icon color="#F56C6C"><CircleClose /></el-icon>
                </template>
              </el-statistic>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>

    <!-- 最近任务 -->
    <el-card class="tasks-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon :size="20" color="#409EFF"><List /></el-icon>
            <span>最近任务</span>
          </div>
          <div class="header-right">
            <el-button text type="primary" @click="loadTasks">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
            <el-button text type="primary" @click="$router.push('/templates')">
              查看全部
            </el-button>
          </div>
        </div>
      </template>

      <div v-if="crawlStore.loading.tasks" class="loading-container">
        <el-skeleton :rows="3" animated />
      </div>

      <div v-else-if="crawlStore.tasks.length === 0" class="empty-container">
        <el-empty description="暂无任务，开始第一次爬取吧！">
          <el-button type="primary" @click="$router.push('/templates')">
            使用场景模板
          </el-button>
        </el-empty>
      </div>

      <div v-else class="tasks-container">
        <CrawlTaskCard
          v-for="task in crawlStore.tasks.slice(0, 5)"
          :key="task.id"
          :task="task"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  Rocket,
  Link,
  Play,
  Document,
  Loading,
  CircleCheck,
  CircleClose,
  List,
  Refresh,
} from '@element-plus/icons-vue'
import CrawlTaskCard from '@/components/CrawlTaskCard.vue'
import { useCrawlStore } from '@/stores/crawl'

// Store
const crawlStore = useCrawlStore()

// URL输入
const urlInput = ref('')

/**
 * 快速爬取
 */
const handleQuickCrawl = async () => {
  if (!urlInput.value) return

  try {
    await crawlStore.createCrawl(urlInput.value)

    // 成功提示
    ElMessage.success('爬取任务已创建！')

    // 清空输入
    urlInput.value = ''

    // 刷新任务列表
    await loadTasks()
  } catch (error) {
    // 错误已经在store中处理了
    console.error('创建爬取任务失败:', error)
  }
}

/**
 * 加载任务列表
 */
const loadTasks = async () => {
  try {
    await crawlStore.loadTasks()
  } catch (error) {
    console.error('加载任务列表失败:', error)
  }
}

onMounted(() => {
  loadTasks()
})
</script>

<style scoped lang="scss">
.dashboard {
  .quick-crawl-card {
    .card-header {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 600;
    }
  }

  .stat-card {
    text-align: center;

    :deep(.el-statistic__head) {
      font-size: 13px;
      color: #909399;
    }

    :deep(.el-statistic__number) {
      font-size: 28px;
      font-weight: 600;
    }
  }

  .tasks-card {
    margin-top: 20px;

    .card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;

      .header-left {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
      }

      .header-right {
        display: flex;
        gap: 8px;
      }
    }

    .loading-container {
      padding: 20px 0;
    }

    .empty-container {
      padding: 40px 0;
    }

    .tasks-container {
      padding: 12px 0;
    }
  }
}
</style>
