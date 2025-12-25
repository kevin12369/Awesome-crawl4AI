<!--
  场景模板页面
  Scenario Templates Page

  艹，这里展示所有内置和自定义的爬取场景模板！
-->
<template>
  <div class="templates-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>
        <el-icon><Collection /></el-icon>
        场景模板
      </h2>
      <el-button type="primary" @click="handleCreateTemplate">
        <el-icon><Plus /></el-icon>
        创建模板
      </el-button>
    </div>

    <!-- 分类过滤 -->
    <el-card class="filter-card" shadow="never">
      <div class="filter-options">
        <span class="filter-label">分类：</span>
        <el-radio-group v-model="selectedCategory" @change="handleCategoryChange">
          <el-radio-button value="all">全部</el-radio-button>
          <el-radio-button value="news">新闻</el-radio-button>
          <el-radio-button value="docs">文档</el-radio-button>
          <el-radio-button value="ecommerce">电商</el-radio-button>
          <el-radio-button value="academic">学术</el-radio-button>
          <el-radio-button value="table">表格</el-radio-button>
          <el-radio-button value="custom">自定义</el-radio-button>
        </el-radio-group>

        <div class="template-stats">
          <el-tag>内置: {{ templateStore.stats.builtin }}</el-tag>
          <el-tag type="success">自定义: {{ templateStore.stats.custom }}</el-tag>
        </div>
      </div>
    </el-card>

    <!-- 模板列表 -->
    <div v-if="templateStore.loading.templates" class="loading-container">
      <el-row :gutter="20">
        <el-col :span="8" v-for="i in 6" :key="i">
          <el-skeleton animated>
            <template #template>
              <el-skeleton-item variant="image" style="width: 100%; height: 150px" />
              <div style="padding: 14px">
                <el-skeleton-item variant="h3" style="width: 50%" />
                <el-skeleton-item variant="text" />
                <el-skeleton-item variant="text" style="width: 70%" />
              </div>
            </template>
          </el-skeleton>
        </el-col>
      </el-row>
    </div>

    <div v-else-if="filteredTemplates.length === 0" class="empty-container">
      <el-empty description="暂无模板">
        <el-button type="primary" @click="handleCreateTemplate">
          创建第一个模板
        </el-button>
      </el-empty>
    </div>

    <div v-else class="templates-grid">
      <el-row :gutter="20">
        <el-col
          v-for="template in filteredTemplates"
          :key="template.id"
          :span="24"
          :sm="12"
          :lg="8"
        >
          <TemplateCard :template="template" :show-actions="true" />
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Collection, Plus } from '@element-plus/icons-vue'
import TemplateCard from '@/components/TemplateCard.vue'
import { useTemplateStore } from '@/stores/template'
import type { TemplateCategory } from '@/types'

// Router
const router = useRouter()

// Store
const templateStore = useTemplateStore()

// 选中的分类
const selectedCategory = ref<TemplateCategory | 'all'>('all')

// 过滤后的模板
const filteredTemplates = computed(() => {
  if (selectedCategory.value === 'all') {
    return templateStore.templates
  }
  return templateStore.templates.filter(t => t.category === selectedCategory.value)
})

/**
 * 加载模板
 */
const loadTemplates = async () => {
  try {
    await templateStore.loadTemplates()
  } catch (error) {
    console.error('加载模板失败:', error)
  }
}

/**
 * 分类改变
 */
const handleCategoryChange = () => {
  templateStore.updateCategoryFilter(selectedCategory.value)
}

/**
 * 创建模板
 */
const handleCreateTemplate = () => {
  router.push('/templates/create')
}

onMounted(() => {
  loadTemplates()
})
</script>

<style scoped lang="scss">
.templates-page {
  .page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;

    h2 {
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 0;
      font-size: 24px;
      color: #303133;
    }
  }

  .filter-card {
    margin-bottom: 20px;

    :deep(.el-card__body) {
      padding: 16px 20px;
    }

    .filter-options {
      display: flex;
      align-items: center;
      gap: 16px;

      .filter-label {
        font-size: 14px;
        color: #606266;
        font-weight: 500;
      }

      .template-stats {
        margin-left: auto;
        display: flex;
        gap: 8px;
      }
    }
  }

  .loading-container,
  .empty-container {
    padding: 60px 20px;
  }

  .templates-grid {
    .el-col {
      margin-bottom: 20px;
    }
  }
}
</style>
