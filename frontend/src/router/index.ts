/**
 * Vue Router配置
 * Vue Router Configuration
 *
 * 艹，路由配置，页面跳转全靠它！
 */

import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      title: '主控面板',
      icon: 'HomeFilled',
    },
  },
  {
    path: '/templates',
    name: 'Templates',
    component: () => import('@/views/ScenarioTemplates.vue'),
    meta: {
      title: '场景模板',
      icon: 'Collection',
    },
  },
  {
    path: '/templates/:id',
    name: 'TemplateDetail',
    component: () => import('@/views/TemplateDetail.vue'),
    meta: {
      title: '模板详情',
    },
  },
  {
    path: '/templates/create',
    name: 'TemplateCreate',
    component: () => import('@/views/TemplateEditor.vue'),
    meta: {
      title: '创建模板',
    },
  },
  {
    path: '/templates/:id/edit',
    name: 'TemplateEdit',
    component: () => import('@/views/TemplateEditor.vue'),
    meta: {
      title: '编辑模板',
    },
  },
  {
    path: '/tutorial',
    name: 'Tutorial',
    component: () => import('@/views/Tutorial.vue'),
    meta: {
      title: '交互教程',
      icon: 'Reading',
    },
  },
  {
    path: '/results/:taskId',
    name: 'ResultDetail',
    component: () => import('@/views/Results.vue'),
    meta: {
      title: '爬取结果',
    },
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: {
      title: '系统设置',
      icon: 'Setting',
    },
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      title: '页面未找到',
    },
  },
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// 全局前置守卫（设置页面标题）
router.beforeEach((to, _from, next) => {
  // 设置页面标题
  const title = to.meta.title as string | undefined
  if (title) {
    document.title = `${title} - Awesome-crawl4AI`
  }
  next()
})

export default router
