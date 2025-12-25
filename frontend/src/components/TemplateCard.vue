<!--
  模板卡片组件
  Template Card Component

  展示单个场景模板的信息
  Display information of a single scenario template
-->
<template>
  <el-card
    class="template-card"
    :class="{ 'builtin': template.is_builtin }"
    shadow="hover"
    @click="handleClick"
  >
    <!-- 卡片头部 -->
    <template #header>
      <div class="card-header">
        <div class="template-name">
          <el-icon :size="20" :color="getCategoryColor(template.category)">
            <component :is="getCategoryIcon(template.category)" />
          </el-icon>
          <span>{{ template.name }}</span>
        </div>
        <el-tag v-if="template.is_builtin" type="info" size="small">
          内置
        </el-tag>
      </div>
    </template>

    <!-- 卡片内容 -->
    <div class="card-content">
      <!-- 描述 -->
      <p v-if="template.description" class="description">
        {{ template.description }}
      </p>

      <!-- 分类和字段数 -->
      <div class="meta-info">
        <el-tag size="small" :type="getCategoryType(template.category)">
          {{ getCategoryText(template.category) }}
        </el-tag>
        <span class="field-count">
          {{ template.config_schema?.fields?.length || 0 }} 个字段
        </span>
      </div>

      <!-- 高级配置 -->
      <div v-if="hasAdvancedConfig" class="advanced-info">
        <el-tag size="small" type="warning">
          高级配置
        </el-tag>
      </div>
    </div>

    <!-- 卡片底部操作 -->
    <template #footer v-if="showActions">
      <div class="card-footer">
        <el-button type="primary" size="small" @click.stop="handleApply">
          应用
        </el-button>
        <el-button
          v-if="!template.is_builtin"
          size="small"
          @click.stop="handleEdit"
        >
          编辑
        </el-button>
      </div>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  Document,
  Collection,
  ShoppingBag,
  Reading,
  Grid,
  MagicStick,
} from '@element-plus/icons-vue'
import type { Template } from '@/types'

// Props
const props = defineProps<{
  template: Template
  showActions?: boolean
}>()

// Router
const router = useRouter()

// 获取分类图标
const getCategoryIcon = (category: string) => {
  const icons: Record<string, any> = {
    news: Document,
    docs: Collection,
    ecommerce: ShoppingBag,
    academic: Reading,
    table: Grid,
    custom: MagicStick,
  }
  return icons[category] || Document
}

// 获取分类颜色
const getCategoryColor = (category: string) => {
  const colors: Record<string, string> = {
    news: '#409EFF',
    docs: '#67C23A',
    ecommerce: '#E6A23C',
    academic: '#909399',
    table: '#F56C6C',
    custom: '#909399',
  }
  return colors[category] || '#909399'
}

// 获取分类类型
const getCategoryType = (category: string) => {
  const types: Record<string, any> = {
    news: 'primary',
    docs: 'success',
    ecommerce: 'warning',
    academic: 'info',
    table: 'danger',
    custom: '',
  }
  return types[category] || ''
}

// 获取分类文本
const getCategoryText = (category: string) => {
  const texts: Record<string, string> = {
    news: '新闻',
    docs: '文档',
    ecommerce: '电商',
    academic: '学术',
    table: '表格',
    custom: '自定义',
  }
  return texts[category] || category
}

// 是否有高级配置
const hasAdvancedConfig = computed(() => {
  const advanced = props.template.config_schema?.advanced
  return advanced && Object.keys(advanced).length > 0
})

// 点击卡片
const handleClick = () => {
  router.push(`/templates/${props.template.id}`)
}

// 应用模板
const handleApply = () => {
  router.push(`/templates/${props.template.id}`)
}

// 编辑模板
const handleEdit = () => {
  router.push(`/templates/${props.template.id}/edit`)
}
</script>

<style scoped lang="scss">
.template-card {
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  &.builtin {
    border: 1px solid #dcdfe6;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .template-name {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 600;
      font-size: 16px;
    }
  }

  .card-content {
    .description {
      font-size: 14px;
      color: #606266;
      margin: 12px 0;
      line-height: 1.6;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .meta-info {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-top: 12px;

      .field-count {
        font-size: 13px;
        color: #909399;
      }
    }

    .advanced-info {
      margin-top: 8px;
    }
  }

  .card-footer {
    display: flex;
    gap: 8px;
    justify-content: flex-end;
  }
}
</style>
