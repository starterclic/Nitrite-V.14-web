import apiClient from './client'
import type { SystemInfo } from '@/types'

export const systemApi = {
  getInfo: async () => {
    const response = await apiClient.get<SystemInfo>('/api/v1/system/info')
    return response.data
  },

  getHealth: async () => {
    const response = await apiClient.get('/api/v1/system/health')
    return response.data
  },

  runDiagnostic: async () => {
    const response = await apiClient.post('/api/v1/system/diagnostic')
    return response.data
  },
}
