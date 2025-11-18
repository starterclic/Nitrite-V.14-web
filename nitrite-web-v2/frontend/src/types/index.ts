export interface Application {
  id: number
  name: string
  description: string
  category: string
  winget_id?: string
  download_url?: string
  install_args?: string
  essential: boolean
  admin_required: boolean
  icon_url?: string
  website?: string
  version?: string
  metadata?: Record<string, any>
  created_at: string
  updated_at?: string
}

export interface Tool {
  id: number
  name: string
  description: string
  section: string
  command: string
  requires_admin: number
  icon?: string
  category?: string
  metadata?: Record<string, any>
}

export interface Profile {
  id: number
  name: string
  description: string
  icon: string
  applications: number[]
  tools: number[]
  metadata?: Record<string, any>
}

export interface SystemInfo {
  system: {
    os: string
    os_version: string
    hostname: string
    architecture: string
    processor: string
  }
  cpu: {
    cores: number
    usage_percent: number
    frequency_mhz?: number
  }
  memory: {
    total_gb: number
    available_gb: number
    used_gb: number
    percent: number
  }
  disk: {
    total_gb: number
    used_gb: number
    free_gb: number
    percent: number
  }
  timestamp: string
}

export type Theme = 'dark_orange' | 'dark_blue' | 'dark_purple' | 'light_gray' | 'high_contrast'

export type Language = 'fr' | 'en'
