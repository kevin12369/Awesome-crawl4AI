/**
 * 通用HTTP客户端
 * Common HTTP Client
 *
 * 艹，所有API请求都通过这个客户端发送！
 */

import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'

// API基础URL
const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

/**
 * 创建axios实例
 */
const client: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 60000, // 60秒超时
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * 请求拦截器
 */
client.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 艹，可以在这里添加认证token等
    // const token = localStorage.getItem('token')
    // if (token && config.headers) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 */
client.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error: AxiosError) => {
    // 统一错误处理
    const message = error.response?.data?.error || error.message || '请求失败'

    // 艹，根据状态码显示不同的错误信息
    if (error.response?.status === 404) {
      ElMessage.error('资源不存在')
    } else if (error.response?.status === 403) {
      ElMessage.error('没有权限')
    } else if (error.response?.status === 500) {
      ElMessage.error('服务器错误，请稍后重试')
    } else {
      ElMessage.error(message)
    }

    return Promise.reject(error)
  }
)

export default client
