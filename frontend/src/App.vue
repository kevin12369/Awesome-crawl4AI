<!--
  根组件
  Root Component

  艹，应用的根，所有组件都在这里渲染
-->
<template>
  <div id="app" class="app-container">
    <!-- 顶部导航栏 -->
    <el-header class="app-header">
      <div class="header-content">
        <div class="logo">
          <el-icon :size="28" color="#409EFF">
            <Spider />
          </el-icon>
          <span class="title">Awesome-crawl4AI</span>
        </div>

        <nav class="nav-menu">
          <router-link to="/" class="nav-item">
            <el-icon><HomeFilled /></el-icon>
            <span>主控面板</span>
          </router-link>
          <router-link to="/templates" class="nav-item">
            <el-icon><Collection /></el-icon>
            <span>场景模板</span>
          </router-link>
          <router-link to="/tutorial" class="nav-item">
            <el-icon><Reading /></el-icon>
            <span>交互教程</span>
          </router-link>
        </nav>

        <div class="header-actions">
          <el-button text @click="showSettings">
            <el-icon><Setting /></el-icon>
          </el-button>
        </div>
      </div>
    </el-header>

    <!-- 主内容区 -->
    <el-main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>

    <!-- 底部状态栏 -->
    <el-footer class="app-footer">
      <div class="footer-content">
        <span class="version">v0.1.0</span>
        <span class="divider">|</span>
        <span class="status">
          <el-icon class="status-icon" color="#67C23A">
            <CircleCheck />
          </el-icon>
          系统运行正常
        </span>
      </div>
    </el-footer>
  </div>
</template>

<script setup lang="ts">
import { Spider, HomeFilled, Collection, Reading, Setting, CircleCheck } from '@element-plus/icons-vue'

/**
 * 显示设置对话框
 * Show settings dialog
 */
const showSettings = () => {
  // 艹，暂时用个简单提示，后续实现设置对话框
  console.log('打开设置')
}
</script>

<style scoped lang="scss">
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.app-header {
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0;
  height: 60px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  z-index: 100;

  .header-content {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    max-width: 1400px;
    margin: 0 auto;
    width: 100%;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 20px;
    font-weight: 600;
    color: #303133;

    .title {
      background: linear-gradient(135deg, #409EFF 0%, #67C23A 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  }

  .nav-menu {
    display: flex;
    gap: 8px;

    .nav-item {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      border-radius: 6px;
      color: #606266;
      text-decoration: none;
      transition: all 0.3s;

      &:hover {
        background-color: #f5f7fa;
        color: #409EFF;
      }

      &.router-link-active {
        background-color: #ecf5ff;
        color: #409EFF;
      }
    }
  }

  .header-actions {
    display: flex;
    gap: 8px;
  }
}

.app-main {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

.app-footer {
  background-color: #fff;
  border-top: 1px solid #e4e7ed;
  padding: 0;
  height: 40px;

  .footer-content {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    font-size: 13px;
    color: #909399;

    .divider {
      color: #dcdfe6;
    }

    .status {
      display: flex;
      align-items: center;
      gap: 4px;

      .status-icon {
        font-size: 16px;
      }
    }
  }
}

// 路由过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
