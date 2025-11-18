# 🚀 Guide de Démarrage Rapide - NiTriTe V2

## Installation en 5 minutes

### 1️⃣ Prérequis

Installez Docker Desktop:
- **Windows**: https://docs.docker.com/desktop/install/windows-install/
- **Mac**: https://docs.docker.com/desktop/install/mac-install/
- **Linux**: https://docs.docker.com/desktop/install/linux-install/

### 2️⃣ Cloner et Démarrer

```bash
# Cloner le repository
git clone <your-repo-url>
cd nitrite-web-v2

# Démarrer tous les services
docker-compose up -d
```

### 3️⃣ Migrer les Données

```bash
# Migrer les données depuis l'ancienne version
docker-compose exec backend python scripts/migrate_data.py
```

### 4️⃣ Accéder à l'Application

Ouvrez votre navigateur:

- **Application Web**: http://localhost:3000
- **API Documentation**: http://localhost:8000/api/docs
- **Backend API**: http://localhost:8000

### 5️⃣ Premiers Pas

1. **Page Applications** - Parcourez les 715+ applications disponibles
2. **Installer une app** - Cliquez sur "Installer" sur une carte d'application
3. **Outils Système** - Accédez aux 547 outils de maintenance
4. **Profils** - Utilisez un profil prédéfini pour installer plusieurs apps
5. **Favoris** - Marquez vos applications favorites avec l'étoile

## 🛠️ Commandes Utiles

```bash
# Voir les logs en temps réel
docker-compose logs -f

# Arrêter tous les services
docker-compose down

# Redémarrer un service spécifique
docker-compose restart backend

# Ouvrir un shell dans le container backend
docker-compose exec backend /bin/bash

# Accéder à PostgreSQL
docker-compose exec postgres psql -U nitrite -d nitrite

# Voir le statut des services
docker-compose ps
```

## 🐛 Dépannage

### Le frontend ne démarre pas

```bash
# Vérifier les logs
docker-compose logs frontend

# Rebuilder le frontend
docker-compose build frontend
docker-compose up -d frontend
```

### Le backend ne se connecte pas à la DB

```bash
# Vérifier que PostgreSQL est démarré
docker-compose ps postgres

# Vérifier les logs de PostgreSQL
docker-compose logs postgres

# Redémarrer PostgreSQL
docker-compose restart postgres
```

### Les données ne sont pas migrées

```bash
# Vérifier que la DB est créée
docker-compose exec postgres psql -U nitrite -l

# Relancer la migration
docker-compose exec backend python scripts/migrate_data.py
```

### Port déjà utilisé

```bash
# Si le port 3000 est déjà utilisé, modifier docker-compose.yml
# Changer "3000:80" en "3001:80" par exemple

# Si le port 8000 est déjà utilisé
# Changer "8000:8000" en "8001:8000"
```

## 📊 Vérification de Santé

```bash
# Vérifier que tous les services sont healthy
docker-compose ps

# Tester l'API backend
curl http://localhost:8000/health

# Tester le frontend
curl http://localhost:3000/health
```

## 🔄 Mise à Jour

```bash
# Récupérer les dernières modifications
git pull

# Rebuilder et redémarrer
docker-compose down
docker-compose build
docker-compose up -d

# Relancer les migrations si nécessaire
docker-compose exec backend python scripts/migrate_data.py
```

## 🎨 Personnalisation

### Changer le port du frontend

Éditez `docker-compose.yml`:

```yaml
frontend:
  ports:
    - "3001:80"  # Changez 3000 en 3001
```

### Changer le thème

Dans l'application, allez dans **Paramètres** → **Thème** et choisissez parmi:
- Dark Orange (défaut)
- Dark Blue
- Dark Purple
- Light Gray
- High Contrast

### Changer la langue

Dans l'application, allez dans **Paramètres** → **Langue** et choisissez:
- Français
- English

## 💡 Astuces

1. **Recherche Rapide**: Utilisez la barre de recherche en haut pour trouver rapidement une application

2. **Favoris**: Cliquez sur l'étoile pour ajouter une app aux favoris

3. **Installation en Masse**: Utilisez la page "Master Installation" pour installer plusieurs apps en une fois

4. **Profils**: Les profils sont des configurations prédéfinies (Gaming, Bureau, Développeur, etc.)

5. **Diagnostic**: La page Diagnostic vous donne des infos système en temps réel

## 🚀 Pour Aller Plus Loin

- Consultez le [README.md](README.md) pour la documentation complète
- Explorez l'[API Documentation](http://localhost:8000/api/docs)
- Personnalisez les profils dans l'interface
- Configurez vos applications favorites

## 📞 Besoin d'Aide ?

- Ouvrez une issue sur GitHub
- Consultez la documentation: http://localhost:8000/api/docs
- Vérifiez les logs: `docker-compose logs -f`

---

**Bon démarrage avec NiTriTe V2 ! 🎉**
