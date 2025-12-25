<!--
  模板详情页面
  Template Detail Page
-->
<template>
  <div class="template-detail-page">
    <el-page-header @back="$router.back()" title="返回">
      <template #content>
        {{ template?.name || '模板详情' }}
      </template>
    </el-page-header>

    <el-card v-if="templateStore.loading.current" shadow="never">
      <el-skeleton :rows="5" animated />
    </el-card>

    <el-card v-else-if="template" shadow="never">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="模板名称">
          {{ template.name }}
        </el-descriptions-item>
        <el-descriptions-item label="分类">
          <el-tag :type="getCategoryType(template.category)">
            {{ getCategoryText(template.category) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
          {{ template.description }}
        </el-descriptions-item>
      </el-descriptions>

      <el-divider>提取字段</el-divider>

      <el-table :data="template.config_schema?.fields || []" border>
        <el-table-column prop="name" label="字段名" />
        <el-table-column prop="selector" label="CSS选择器" />
        <el-table-column prop="type" label="类型" width="100" />
        <el-table-column label="选项" width="150">
          <template #default="{ row }">
            <el-tag v-if="row.required" type="danger" size="small">必需</el-tag>
            <el-tag v-if="row.multiple" type="info" size="small">多个</el-tag>
          </template>
        </el-table-column>
      </el-table>

      <div style="margin-top: 24px; text-align: center;">
        <el-space>
          <el-button type="primary" @click="handleUseTemplate">
            使用此模板
          </el-button>
          <el-button v-if="!template.is_builtin" @click="handleEdit">
            编辑
          </el-button>
        </el-space>
      </div>
    </el-card>

    <el-card v-else shadow="never">
      <el-empty description="模板不存在" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTemplateStore } from '@/stores/template'

const route = useRoute()
const router = useRouter()
const templateStore = useTemplateStore()

const template = computed(() => templateStore.currentTemplate)

const getCategoryType = (category: string) => {
  const types: Record<string, any> = {
    news: 'primary',
    docs: 'success',
    ecommerce: 'warning',
    academic: 'info',
    table: 'danger',
  }
  return types[category] || ''
}

const getCategoryText = (category: string) => {
  const texts: Record<string, string> = {
    news: '新闻',
    docs: '文档',
    ecommerce: '电商',
    academic: '学术',
    table: '表格',
  }
  return texts[category] || category
}

const handleUseTemplate = () => {
  router.push('/')
}

const handleEdit = () => {
  router.push(`/templates/${route.params.id}/edit`)
}

onMounted(() => {
  templateStore.loadTemplate(Number(route.params.id))
})
</script>

<style scoped lang="scss">
.template-detail-page {
  :deep(.el-page-header) {
    margin-bottom: 20px;
  }
}
</style>
