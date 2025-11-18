.PHONY: help install dev build up down logs test clean migrate seed

help: ## Afficher l'aide
	@echo "Commandes disponibles:"
	@echo "  make install    - Installer les dépendances"
	@echo "  make dev        - Lancer en mode développement"
	@echo "  make build      - Builder les images Docker"
	@echo "  make up         - Démarrer tous les services"
	@echo "  make down       - Arrêter tous les services"
	@echo "  make logs       - Voir les logs"
	@echo "  make test       - Lancer les tests"
	@echo "  make clean      - Nettoyer les containers et volumes"
	@echo "  make migrate    - Lancer les migrations DB"
	@echo "  make seed       - Seeder la base de données"

install: ## Installer les dépendances
	@echo "Installation des dépendances backend..."
	cd backend && pip install -r requirements.txt
	@echo "Installation des dépendances frontend..."
	cd frontend && npm install
	@echo "✅ Dépendances installées"

dev: ## Lancer en mode développement
	@echo "Démarrage des services..."
	docker-compose up

build: ## Builder les images Docker
	@echo "Build des images Docker..."
	docker-compose build
	@echo "✅ Images buildées"

up: ## Démarrer tous les services
	@echo "Démarrage des services en arrière-plan..."
	docker-compose up -d
	@echo "✅ Services démarrés"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/api/docs"

down: ## Arrêter tous les services
	@echo "Arrêt des services..."
	docker-compose down
	@echo "✅ Services arrêtés"

logs: ## Voir les logs
	docker-compose logs -f

test: ## Lancer les tests
	@echo "Tests backend..."
	cd backend && pytest
	@echo "Tests frontend..."
	cd frontend && npm test
	@echo "✅ Tests terminés"

clean: ## Nettoyer les containers et volumes
	@echo "Nettoyage..."
	docker-compose down -v
	rm -rf backend/__pycache__ backend/.pytest_cache
	rm -rf frontend/node_modules frontend/dist
	@echo "✅ Nettoyage terminé"

migrate: ## Lancer les migrations DB
	@echo "Migration de la base de données..."
	docker-compose exec backend alembic upgrade head
	@echo "✅ Migrations terminées"

seed: ## Seeder la base de données
	@echo "Seed de la base de données..."
	docker-compose exec backend python scripts/seed_data.py
	@echo "✅ Seed terminé"

status: ## Voir le statut des services
	docker-compose ps

restart: ## Redémarrer tous les services
	docker-compose restart

shell-backend: ## Ouvrir un shell dans le container backend
	docker-compose exec backend /bin/bash

shell-frontend: ## Ouvrir un shell dans le container frontend
	docker-compose exec frontend /bin/sh

db-shell: ## Ouvrir un shell PostgreSQL
	docker-compose exec postgres psql -U nitrite -d nitrite
