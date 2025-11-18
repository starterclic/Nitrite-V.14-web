import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import {
  Package,
  Wrench,
  User,
  Zap,
  Star,
  Activity,
  Sparkles,
  HardDrive,
  Download,
  Settings,
} from 'lucide-react'

const menuItems = [
  { icon: Package, label: 'Applications', path: '/', count: 715 },
  { icon: Wrench, label: 'Outils Système', path: '/tools', count: 547 },
  { icon: User, label: 'Profils', path: '/profiles', count: 10 },
  { icon: Zap, label: 'Master Installation', path: '/master' },
  { icon: Star, label: 'Favoris', path: '/favorites' },
  { icon: Activity, label: 'Diagnostic', path: '/diagnostic' },
  { icon: Sparkles, label: 'Optimisations', path: '/optimization' },
  { icon: HardDrive, label: 'Sauvegarde', path: '/backup' },
  { icon: Download, label: 'Mises à jour', path: '/updates' },
  { icon: Settings, label: 'Paramètres', path: '/settings' },
]

export function Sidebar() {
  const location = useLocation()

  return (
    <aside className="w-64 bg-card border-r border-border flex flex-col h-screen">
      {/* Logo */}
      <div className="p-6 border-b border-border">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary to-orange-600 rounded-lg flex items-center justify-center">
            <Package className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-foreground">NiTriTe</h1>
            <p className="text-xs text-muted-foreground">V2.0 Pro</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-4 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path

          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                'flex items-center gap-3 px-4 py-3 rounded-lg transition-all group',
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
              )}
            >
              <Icon className="w-5 h-5" />
              <span className="flex-1 font-medium">{item.label}</span>
              {item.count && (
                <span
                  className={cn(
                    'text-xs px-2 py-0.5 rounded-full',
                    isActive
                      ? 'bg-primary-foreground/20 text-primary-foreground'
                      : 'bg-muted text-muted-foreground group-hover:bg-accent-foreground/10'
                  )}
                >
                  {item.count}
                </span>
              )}
            </Link>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-border">
        <div className="text-xs text-muted-foreground text-center">
          <p>© 2024 NiTriTe</p>
          <p className="mt-1">Maintenance Windows Pro</p>
        </div>
      </div>
    </aside>
  )
}
