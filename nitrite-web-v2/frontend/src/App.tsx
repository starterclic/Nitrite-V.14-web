import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Layout } from '@/components/layout/Layout'
import { ApplicationsPage } from '@/pages/ApplicationsPage'

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
})

// Placeholder pages
function ToolsPage() {
  return <div className="text-2xl font-bold">Outils Système (Coming Soon)</div>
}

function ProfilesPage() {
  return <div className="text-2xl font-bold">Profils (Coming Soon)</div>
}

function MasterPage() {
  return <div className="text-2xl font-bold">Master Installation (Coming Soon)</div>
}

function FavoritesPage() {
  return <div className="text-2xl font-bold">Favoris (Coming Soon)</div>
}

function DiagnosticPage() {
  return <div className="text-2xl font-bold">Diagnostic (Coming Soon)</div>
}

function OptimizationPage() {
  return <div className="text-2xl font-bold">Optimisations (Coming Soon)</div>
}

function BackupPage() {
  return <div className="text-2xl font-bold">Sauvegarde (Coming Soon)</div>
}

function UpdatesPage() {
  return <div className="text-2xl font-bold">Mises à jour (Coming Soon)</div>
}

function SettingsPage() {
  return <div className="text-2xl font-bold">Paramètres (Coming Soon)</div>
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<ApplicationsPage />} />
            <Route path="tools" element={<ToolsPage />} />
            <Route path="profiles" element={<ProfilesPage />} />
            <Route path="master" element={<MasterPage />} />
            <Route path="favorites" element={<FavoritesPage />} />
            <Route path="diagnostic" element={<DiagnosticPage />} />
            <Route path="optimization" element={<OptimizationPage />} />
            <Route path="backup" element={<BackupPage />} />
            <Route path="updates" element={<UpdatesPage />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
