<!--
  模板编辑器页面
  Template Editor Page

  艹，可视化编辑模板的核心页面！用户不需要写代码就能创建模板！
-->
<template>
  <div class="template-editor-page">
    <el-page-header @back="$router.back()" title="返回">
      <template #content>
        <div class="header-content">
          {{ isEdit ? '编辑模板' : '创建模板' }}
        </div>
      </template>
    </el-page-header>

    <el-card class="editor-card" shadow="never">
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="120px"
        @submit.prevent="handleSubmit"
      >
        <!-- 基本信息 -->
        <el-divider content-position="left">基本信息</el-divider>

        <el-form-item label="模板名称" prop="name">
          <el-input
            v-model="formData.name"
            placeholder="例如：news_crawler"
            clearable
          />
        </el-form-item>

        <el-form-item label="模板描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="2"
            placeholder="简单描述这个模板的用途..."
          />
        </el-form-item>

        <el-form-item label="分类" prop="category">
          <el-select v-model="formData.category" placeholder="选择分类">
            <el-option label="新闻爬取" value="news" />
            <el-option label="文档归档" value="docs" />
            <el-option label="电商监控" value="ecommerce" />
            <el-option label="学术收集" value="academic" />
            <el-option label="表格提取" value="table" />
            <el-option label="自定义" value="custom" />
          </el-select>
        </el-form-item>

        <!-- 提取字段 -->
        <el-divider content-position="left">
          提取字段
          <el-button
            type="primary"
            size="small"
            text
            @click="addField"
          >
            <el-icon><Plus /></el-icon>
            添加字段
          </el-button>
        </el-divider>

        <div v-if="formData.fields.length === 0" class="empty-fields">
          <el-empty description="暂无提取字段，点击上方按钮添加" />
        </div>

        <div v-else class="fields-list">
          <el-card
            v-for="(field, index) in formData.fields"
            :key="index"
            class="field-card"
            shadow="never"
          >
            <template #header>
              <div class="field-header">
                <span>字段 #{{ index + 1 }}</span>
                <el-button
                  type="danger"
                  size="small"
                  text
                  @click="removeField(index)"
                >
                  <el-icon><Delete /></el-icon>
                  删除
                </el-button>
              </div>
            </template>

            <el-row :gutter="16">
              <el-col :span="8">
                <el-form-item label="字段名" size="small">
                  <el-input
                    v-model="field.name"
                    placeholder="例如：title"
                  />
                </el-form-item>
              </el-col>

              <el-col :span="8">
                <el-form-item label="CSS选择器" size="small">
                  <el-input
                    v-model="field.selector"
                    placeholder="例如：h1.title"
                  />
                </el-form-item>
              </el-col>

              <el-col :span="8">
                <el-form-item label="提取类型" size="small">
                  <el-select v-model="field.type" style="width: 100%">
                    <el-option label="文本" value="text" />
                    <el-option label="数字" value="number" />
                    <el-option label="链接" value="link" />
                    <el-option label="图片" value="image" />
                    <el-option label="属性" value="attribute" />
                  </el-select>
                </el-form-item>
              </el-col>

              <el-col :span="8" v-if="field.type === 'attribute'">
                <el-form-item label="属性名" size="small">
                  <el-input
                    v-model="field.attribute"
                    placeholder="例如：href"
                  />
                </el-form-item>
              </el-col>

              <el-col :span="8">
                <el-form-item label="选项" size="small">
                  <el-checkbox v-model="field.required">必需</el-checkbox>
                  <el-checkbox v-model="field.multiple">多个</el-checkbox>
                </el-form-item>
              </el-col>
            </el-row>
          </el-card>
        </div>

        <!-- 高级配置 -->
        <el-divider content-position="left">
          <el-checkbox v-model="showAdvanced">高级配置</el-checkbox>
        </el-divider>

        <div v-if="showAdvanced" class="advanced-config">
          <el-row :gutter="16">
            <el-col :span="6">
              <el-form-item label="深度爬取" size="small">
                <el-switch v-model="formData.advanced.deep_crawl" />
              </el-form-item>
            </el-col>

            <el-col :span="6">
              <el-form-item label="最大页面数" size="small">
                <el-input-number
                  v-model="formData.advanced.max_pages"
                  :min="1"
                  :max="100"
                />
              </el-form-item>
            </el-col>

            <el-col :span="6">
              <el-form-item label="请求延迟" size="small">
                <el-input-number
                  v-model="formData.advanced.delay"
                  :min="0"
                  :max="60"
                  :step="0.5"
                />
                <span style="margin-left: 8px; font-size: 13px; color: #909399">秒</span>
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- 操作按钮 -->
        <el-form-item style="margin-top: 32px">
          <el-space>
            <el-button
              type="primary"
            :loading="templateStore.loading.saving"
            @click="handleSubmit"
          >
            <el-icon><Check /></el-icon>
            {{ templateStore.loading.saving ? '保存中...' : '保存模板' }}
          </el-button>

            <el-button @click="handleValidate">
              <el-icon><CircleCheck /></el-icon>
              验证配置
            </el-button>

            <el-button @click="$router.back()">
              取消
            </el-button>
          </el-space>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Plus,
  Delete,
  Check,
  CircleCheck,
} from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import type { ExtractField, TemplateConfigSchema } from '@/types'
import { useTemplateStore } from '@/stores/template'

// Router
const route = useRoute()
const router = useRouter()

// Store
const templateStore = useTemplateStore()

// 表单引用
const formRef = ref<FormInstance>()

// 是否编辑模式
const isEdit = computed(() => !!route.params.id && route.params.id !== 'create')

// 是否显示高级配置
const showAdvanced = ref(false)

// 表单数据
const formData = reactive<{
  name: string
  description: string
  category: string
  fields: ExtractField[]
  advanced: {
    deep_crawl: boolean
    max_pages: number
    delay: number
  }
}>({
  name: '',
  description: '',
  category: 'custom',
  fields: [],
  advanced: {
    deep_crawl: false,
    max_pages: 10,
    delay: 0,
  },
})

// 表单验证规则
const formRules: FormRules = {
  name: [
    { required: true, message: '请输入模板名称', trigger: 'blur' },
    {
      pattern: /^[a-z0-9_]+$/,
      message: '只能包含小写字母、数字和下划线',
      trigger: 'blur',
    },
  ],
  description: [
    { required: true, message: '请输入模板描述', trigger: 'blur' },
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'change' },
  ],
}

/**
 * 添加字段
 */
const addField = () => {
  formData.fields.push({
    name: '',
    selector: '',
    type: 'text',
    required: false,
    multiple: false,
  })
}

/**
 * 删除字段
 */
const removeField = (index: number) => {
  formData.fields.splice(index, 1)
}

/**
 * 验证配置
 */
const handleValidate = async () => {
  const config: TemplateConfigSchema = {
    name: formData.name,
    description: formData.description,
    fields: formData.fields,
    advanced: formData.advanced,
  }

  const result = await templateStore.validateTemplate(config)

  if (result.valid) {
    ElMessage.success('配置验证通过！')
  } else {
    ElMessage.error(`验证失败: ${result.message}`)
  }
}

/**
 * 提交表单
 */
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    const config: TemplateConfigSchema = {
      name: formData.name,
      description: formData.description,
      fields: formData.fields,
      advanced: formData.advanced,
    }

    if (isEdit.value) {
      await templateStore.updateTemplate(
        Number(route.params.id),
        {
          name: formData.name,
          description: formData.description,
          category: formData.category,
          config_schema: config,
        }
      )
      ElMessage.success('模板更新成功！')
    } else {
      await templateStore.createTemplate(
        formData.name,
        formData.description,
        formData.category,
        config
      )
      ElMessage.success('模板创建成功！')
    }

    router.push('/templates')
  } catch (error) {
    console.error('提交失败:', error)
  }
}

/**
 * 加载模板（编辑模式）
 */
const loadTemplate = async () => {
  if (!isEdit.value) return

  try {
    const template = await templateStore.loadTemplate(Number(route.params.id))

    if (template) {
      formData.name = template.name
      formData.description = template.description || ''
      formData.category = template.category
      formData.fields = template.config_schema?.fields || []
      formData.advanced = template.config_schema?.advanced || formData.advanced
    }
  } catch (error) {
    console.error('加载模板失败:', error)
    ElMessage.error('加载模板失败')
    router.back()
  }
}

onMounted(() => {
  loadTemplate()
})
</script>

<style scoped lang="scss">
.template-editor-page {
  .header-content {
    font-size: 18px;
    font-weight: 600;
  }

  .editor-card {
    margin-top: 20px;

    .empty-fields {
      padding: 40px 0;
    }

    .fields-list {
      .field-card {
        margin-bottom: 16px;

        .field-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-weight: 600;
        }
      }
    }

    .advanced-config {
      background-color: #f5f7fa;
      padding: 16px;
      border-radius: 4px;
    }
  }
}
</style>
