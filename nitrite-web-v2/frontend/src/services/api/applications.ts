import apiClient from './client'
import type { Application } from '@/types'

export const applicationsApi = {
  getAll: async (params?: {
    category?: string
    search?: string
    page?: number
    page_size?: number
  }) => {
    const response = await apiClient.get<{
      applications: Application[]
      total: number
      page: number
      page_size: number
    }>('/api/v1/applications/', { params })
    return response.data
  },

  getById: async (id: number) => {
    const response = await apiClient.get<Application>(`/api/v1/applications/${id}`)
    return response.data
  },

  getCategories: async () => {
    const response = await apiClient.get<{ categories: string[] }>(
      '/api/v1/applications/categories'
    )
    return response.data.categories
  },

  install: async (id: number) => {
    const response = await apiClient.post(`/api/v1/applications/${id}/install`)
    return response.data
  },
}
