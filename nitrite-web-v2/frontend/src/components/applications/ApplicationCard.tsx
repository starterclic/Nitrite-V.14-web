import { Star, Download, ExternalLink } from 'lucide-react'
import { Card, CardContent, CardFooter } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { useAppStore } from '@/store/useAppStore'
import type { Application } from '@/types'

interface ApplicationCardProps {
  application: Application
  onInstall: (id: number) => void
  isInstalling?: boolean
}

export function ApplicationCard({ application, onInstall, isInstalling }: ApplicationCardProps) {
  const { favorites, toggleFavorite } = useAppStore()
  const isFavorite = favorites.includes(application.id)

  return (
    <Card className="group hover:shadow-lg transition-all duration-300 hover:border-primary/50">
      <CardContent className="pt-6">
        <div className="flex items-start justify-between mb-4">
          <h3 className="font-semibold text-lg text-foreground group-hover:text-primary transition-colors">
            {application.name}
          </h3>
          <button
            onClick={() => toggleFavorite(application.id)}
            className="text-muted-foreground hover:text-primary transition-colors"
          >
            <Star
              className={`w-5 h-5 ${isFavorite ? 'fill-primary text-primary' : ''}`}
            />
          </button>
        </div>

        <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
          {application.description}
        </p>

        <div className="flex gap-2 mb-4 flex-wrap">
          <Badge variant="secondary">{application.category}</Badge>
          {application.essential && (
            <Badge variant="default">Essentiel</Badge>
          )}
          {application.admin_required && (
            <Badge variant="outline">Admin</Badge>
          )}
        </div>

        {application.version && (
          <p className="text-xs text-muted-foreground">
            Version: {application.version}
          </p>
        )}
      </CardContent>

      <CardFooter className="gap-2">
        <Button
          className="flex-1"
          onClick={() => onInstall(application.id)}
          disabled={isInstalling}
        >
          <Download className="mr-2 h-4 w-4" />
          {isInstalling ? 'Installation...' : 'Installer'}
        </Button>

        {application.website && (
          <Button variant="outline" size="icon" asChild>
            <a href={application.website} target="_blank" rel="noopener noreferrer">
              <ExternalLink className="h-4 w-4" />
            </a>
          </Button>
        )}
      </CardFooter>
    </Card>
  )
}
