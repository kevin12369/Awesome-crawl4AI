/**
 * 教程API客户端
 * Tutorial API Client
 *
 * 处理交互式教程的API请求
 * Handle interactive tutorial API requests
 */

import client from './client'
import type { Tutorial, TutorialCategory, ApiResponse } from '@/types'

/**
 * 获取教程列表
 * Get tutorial list
 */
export async function getTutorials(
  category?: TutorialCategory
): Promise<ApiResponse<{ items: Tutorial[]; total: number }>> {
  return client.get('/tutorials', {
    params: { category },
  })
}

/**
 * 获取单个教程
 * Get single tutorial
 */
export async function getTutorial(tutorialId: number): Promise<ApiResponse<Tutorial>> {
  return client.get(`/tutorials/${tutorialId}`)
}

/**
 * 获取入门教程
 * Get beginner tutorials
 */
export async function getBeginnerTutorials(): Promise<Tutorial[]> {
  const response = await getTutorials('beginner')
  return response.data?.items || []
}

/**
 * 获取进阶教程
 * Get intermediate tutorials
 */
export async function getIntermediateTutorials(): Promise<Tutorial[]> {
  const response = await getTutorials('intermediate')
  return response.data?.items || []
}

/**
 * 获取高级教程
 * Get advanced tutorials
 */
export async function getAdvancedTutorials(): Promise<Tutorial[]> {
  const response = await getTutorials('advanced')
  return response.data?.items || []
}
