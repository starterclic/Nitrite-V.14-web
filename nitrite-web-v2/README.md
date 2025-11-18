# 🚀 NiTriTe V2 - Application Web Ultra-Moderne

Application web professionnelle de maintenance Windows, construite avec React, FastAPI et Docker.

## ✨ Fonctionnalités

- 📦 **715+ Applications** - Installation facile via WinGet
- 🔧 **547+ Outils Système** - Maintenance et diagnostic
- 👤 **10 Profils Prédéfinis** - Configurations métier
- ⚡ **Master Installation** - Installation en masse
- ⭐ **Favoris** - Gestion personnalisée
- 📊 **Diagnostic Système** - Analyse complète
- 🎨 **Thèmes Personnalisables** - Interface premium
- 🌐 **Multi-langue** - Français/Anglais
- 🐳 **Docker** - Déploiement simplifié

## 🏗️ Architecture

### Frontend
- **React 18** + TypeScript
- **Vite** - Build ultra-rapide
- **Tailwind CSS** - Styling moderne
- **TanStack Query** - State management serveur
- **Zustand** - State management client
- **shadcn/ui** - Composants UI premium

### Backend
- **FastAPI** - Framework moderne Python
- **PostgreSQL** - Base de données relationnelle
- **Redis** - Cache et sessions
- **Celery** - Tâches asynchrones
- **SQLAlchemy** - ORM
- **Pydantic** - Validation

### DevOps
- **Docker Compose** - Orchestration
- **Nginx** - Reverse proxy
- **GitHub Actions** - CI/CD (à venir)

## 📋 Prérequis

- Docker 20.10+
- Docker Compose 2.0+
- (Optionnel) Node.js 18+ et Python 3.11+ pour développement local

## 🚀 Démarrage Rapide

### Option 1: Docker (Recommandé)

```bash
# Cloner le projet
cd nitrite-web-v2

# Lancer tous les services
make up

# Ou sans Makefile
docker-compose up -d
```

L'application sera accessible sur:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

### Option 2: Développement Local

#### Backend

```bash
cd backend

# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# Copier .env
cp .env.example .env

# Lancer PostgreSQL et Redis via Docker
docker-compose up -d postgres redis

# Migrer les données
python scripts/migrate_data.py

# Lancer le serveur
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Installer dépendances
npm install

# Copier .env
cp .env.example .env

# Lancer le serveur de dev
npm run dev
```

## 📝 Commandes Makefile

```bash
make help          # Afficher l'aide
make install       # Installer les dépendances
make dev           # Lancer en mode développement
make build         # Builder les images Docker
make up            # Démarrer tous les services
make down          # Arrêter tous les services
make logs          # Voir les logs
make test          # Lancer les tests
make clean         # Nettoyer
make migrate       # Lancer les migrations DB
make status        # Voir le statut des services
```

## 🗄️ Migration des Données

Pour migrer les données de l'ancienne version:

```bash
# Via Docker
docker-compose exec backend python scripts/migrate_data.py

# Ou localement
cd backend
python scripts/migrate_data.py
```

Le script migre automatiquement:
- Applications (programs.json)
- Outils système (tools.json)
- Profils prédéfinis

## 🔧 Configuration

### Variables d'Environnement Backend

```bash
# backend/.env
APP_NAME=NiTriTe API
APP_VERSION=2.0.0
DEBUG=True
SECRET_KEY=your-secret-key

DATABASE_URL=postgresql+asyncpg://nitrite:password@postgres:5432/nitrite
REDIS_URL=redis://redis:6379/0

ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Variables d'Environnement Frontend

```bash
# frontend/.env
VITE_API_URL=http://localhost:8000
```

## 📚 API Documentation

La documentation interactive de l'API est disponible sur:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Endpoints Principaux

```
GET    /api/v1/applications          # Liste des applications
GET    /api/v1/applications/{id}     # Détails application
POST   /api/v1/applications/{id}/install   # Installer

GET    /api/v1/tools                 # Liste des outils
POST   /api/v1/tools/{id}/execute    # Exécuter un outil

GET    /api/v1/profiles              # Liste des profils
POST   /api/v1/profiles/{id}/install # Installer un profil

GET    /api/v1/system/info           # Infos système
GET    /api/v1/system/health         # Health check
POST   /api/v1/system/diagnostic     # Lancer diagnostic
```

## 🎨 Interface Utilisateur

L'interface comprend:

1. **Sidebar** - Navigation principale avec 10 pages
2. **Header** - Recherche et infos système temps réel
3. **Applications** - Catalogue de 715+ apps avec filtres
4. **Outils Système** - 547 outils organisés en 12 sections
5. **Profils** - 10 profils métier prédéfinis
6. **Master Installation** - Installation en masse
7. **Diagnostic** - Analyse système complète
8. **Optimisations** - Tweaks Windows
9. **Sauvegarde** - Points de restauration
10. **Paramètres** - Thèmes, langue, préférences

## 🐳 Architecture Docker

```
nitrite-web-v2/
├── frontend (React + Nginx)      → Port 3000
├── backend (FastAPI)             → Port 8000
├── postgres (Database)           → Port 5432
├── redis (Cache)                 → Port 6379
├── celery (Workers)              → Background
└── nginx (Reverse Proxy)         → Port 80/443
```

## 🔒 Sécurité

- **CORS** configuré pour origines autorisées
- **Rate limiting** sur API (10 req/s)
- **Headers de sécurité** (X-Frame-Options, CSP, etc.)
- **Validation** automatique (Pydantic)
- **Sanitization** des inputs
- **HTTPS** ready (production)

## 📊 Monitoring

- **Prometheus** metrics exposées sur `/metrics`
- **Health checks** sur `/health`
- **Logs structurés** (JSON format)

## 🧪 Tests

```bash
# Tests backend
cd backend
pytest

# Tests frontend
cd frontend
npm test

# Ou via Makefile
make test
```

## 🚢 Déploiement Production

### Docker Compose Production

```bash
# Utiliser docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml up -d

# Avec SSL/TLS
# 1. Ajouter certificats dans docker/nginx/ssl/
# 2. Décommenter config HTTPS dans nginx.conf
# 3. Redémarrer nginx
```

### Variables d'Environnement Production

```bash
DEBUG=False
SECRET_KEY=<strong-random-key>
DATABASE_URL=<production-db-url>
ALLOWED_ORIGINS=https://yourdomain.com
```

## 📈 Performance

- **Backend**: 1000+ req/s (async FastAPI)
- **Frontend**: Build optimisé (Vite)
- **Database**: Connection pooling
- **Cache**: Redis pour sessions/cache
- **CDN Ready**: Assets optimisés

## 🆚 Comparaison avec V1

| Fonctionnalité | V1 (Ancien) | V2 (Nouveau) |
|----------------|-------------|--------------|
| Frontend | HTML/CSS/JS vanilla | React + TypeScript |
| Backend | Flask basique | FastAPI async |
| Database | JSON + SQLite | PostgreSQL |
| Cache | LocalStorage | Redis |
| Déploiement | .exe portable | Docker |
| Tests | Aucun | Pytest + Vitest |
| API Docs | Aucune | OpenAPI/Swagger |
| Performance | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence propriétaire.

## 👥 Auteurs

- **NiTriTe Team** - Maintenance Windows Pro

## 🙏 Remerciements

- React Team
- FastAPI Team
- shadcn/ui
- Tailwind CSS
- Docker

## 📞 Support

Pour toute question ou problème:
- Ouvrir une issue sur GitHub
- Documentation: `/docs`
- API Docs: http://localhost:8000/api/docs

---

**Made with ❤️ by NiTriTe Team**
