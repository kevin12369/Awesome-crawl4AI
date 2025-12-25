<!--
  交互式教程页面
  Tutorial Page

  艹，从入门到高级的完整教程！
-->
<template>
  <div class="tutorial-page">
    <el-page-header title="交互式教程" />

    <el-card class="tutorials-card" shadow="never">
      <el-empty description="教程内容开发中..." />
      <p style="text-align: center; color: #909399; margin-top: 20px;">
        即将推出：
      </p>
      <ul style="max-width: 600px; margin: 0 auto; color: #606266;">
        <li>第1课：入门 - 快速开始第一次爬取</li>
        <li>第2课：进阶 - 使用场景模板</li>
        <li>第3课：高级 - 创建自定义模板</li>
        <li>第4课：专家 - 反爬虫对抗策略</li>
      </ul>
    </el-card>
  </div>
</template>

<script setup lang="ts">
// TODO: 实现完整教程系统
</script>

<style scoped lang="scss">
.tutorial-page {
  .tutorials-card {
    margin-top: 20px;

    ul {
      list-style: none;
      padding: 0;

      li {
        padding: 12px 16px;
        border-bottom: 1px solid #f0f0f0;

        &:last-child {
          border-bottom: none;
        }
      }
    }
  }
}
</style>
