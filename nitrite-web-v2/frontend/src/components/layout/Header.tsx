import { Search, Bell, User } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { useQuery } from '@tanstack/react-query'
import { systemApi } from '@/services/api/system'
import { formatPercent } from '@/lib/utils'

export function Header() {
  const { data: systemInfo } = useQuery({
    queryKey: ['system-info'],
    queryFn: systemApi.getInfo,
    refetchInterval: 5000, // Refresh every 5s
  })

  return (
    <header className="h-16 border-b border-border bg-card flex items-center justify-between px-6">
      {/* Search */}
      <div className="flex-1 max-w-md">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Rechercher une application..."
            className="w-full h-10 pl-10 pr-4 rounded-lg bg-background border border-input text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
      </div>

      {/* System Stats */}
      {systemInfo && (
        <div className="flex items-center gap-6 mx-6">
          <div className="text-sm">
            <span className="text-muted-foreground">CPU: </span>
            <span className="font-medium text-foreground">
              {formatPercent(systemInfo.cpu.usage_percent)}
            </span>
          </div>
          <div className="text-sm">
            <span className="text-muted-foreground">RAM: </span>
            <span className="font-medium text-foreground">
              {formatPercent(systemInfo.memory.percent)}
            </span>
          </div>
          <div className="text-sm">
            <span className="text-muted-foreground">Disque: </span>
            <span className="font-medium text-foreground">
              {formatPercent(systemInfo.disk.percent)}
            </span>
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="icon">
          <Bell className="w-5 h-5" />
        </Button>
        <Button variant="ghost" size="icon">
          <User className="w-5 h-5" />
        </Button>
      </div>
    </header>
  )
}
