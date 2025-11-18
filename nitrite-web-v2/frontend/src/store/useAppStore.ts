import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { Theme, Language } from '@/types'

interface AppState {
  theme: Theme
  language: Language
  favorites: number[]
  sidebarCollapsed: boolean
  setTheme: (theme: Theme) => void
  setLanguage: (language: Language) => void
  toggleFavorite: (appId: number) => void
  setSidebarCollapsed: (collapsed: boolean) => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      theme: 'dark_orange',
      language: 'fr',
      favorites: [],
      sidebarCollapsed: false,
      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
      toggleFavorite: (appId) =>
        set((state) => ({
          favorites: state.favorites.includes(appId)
            ? state.favorites.filter((id) => id !== appId)
            : [...state.favorites, appId],
        })),
      setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
    }),
    {
      name: 'nitrite-storage',
    }
  )
)
