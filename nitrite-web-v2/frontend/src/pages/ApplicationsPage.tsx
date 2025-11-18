import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { applicationsApi } from '@/services/api/applications'
import { ApplicationCard } from '@/components/applications/ApplicationCard'
import { Button } from '@/components/ui/Button'
import { Filter } from 'lucide-react'

export function ApplicationsPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>('')
  const [search, setSearch] = useState('')

  // Fetch applications
  const { data, isLoading } = useQuery({
    queryKey: ['applications', selectedCategory, search],
    queryFn: () =>
      applicationsApi.getAll({
        category: selectedCategory || undefined,
        search: search || undefined,
      }),
  })

  // Fetch categories
  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: applicationsApi.getCategories,
  })

  // Install mutation
  const installMutation = useMutation({
    mutationFn: applicationsApi.install,
    onSuccess: () => {
      // Show success toast (to implement)
      console.log('Installation started!')
    },
  })

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Applications</h1>
        <p className="text-muted-foreground mt-1">
          {data?.total || 0} applications disponibles
        </p>
      </div>

      {/* Filters */}
      <div className="flex gap-4 items-center">
        <Button
          variant={!selectedCategory ? 'default' : 'outline'}
          onClick={() => setSelectedCategory('')}
        >
          Toutes
        </Button>

        {categories?.slice(0, 8).map((category) => (
          <Button
            key={category}
            variant={selectedCategory === category ? 'default' : 'outline'}
            onClick={() => setSelectedCategory(category)}
          >
            {category}
          </Button>
        ))}

        <Button variant="outline" size="icon">
          <Filter className="w-4 h-4" />
        </Button>
      </div>

      {/* Applications Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              className="h-64 bg-card border border-border rounded-lg animate-pulse"
            />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {data?.applications.map((app) => (
            <ApplicationCard
              key={app.id}
              application={app}
              onInstall={(id) => installMutation.mutate(id)}
              isInstalling={installMutation.isPending}
            />
          ))}
        </div>
      )}

      {/* Empty State */}
      {!isLoading && data?.applications.length === 0 && (
        <div className="text-center py-12">
          <p className="text-muted-foreground">Aucune application trouvée</p>
        </div>
      )}
    </div>
  )
}
