# 📊 Données de configuration NiTrite v2.0

## 📋 Fichiers principaux

### 🔧 Configuration de base
- `config.json` - Configuration générale de l'application
- `programs.json` - Base de données des programmes (fichier principal)

### 📦 Bases de données spécialisées
- `programs_winget.json` - Programmes disponibles via Winget
- `programs_extended.json` - Programmes étendus
- `programs_massive.json` - Collection massive de programmes
- `office_links.json` - Liens Office et outils Microsoft

### 💾 Sauvegardes
- `programs.json.backup` - Backup principal
- `programs.json.backup_urls_fix` - Backup avec corrections URLs
- [`backups/`](backups/) - Sauvegardes datées automatiques

## 📁 Structure des fichiers

### config.json
Configuration générale de l'application
```json
{
  "app_version": "2.0.0",
  "language": "fr",
  "auto_cleanup": true,
  "max_concurrent_downloads": 3
}
```

### programs.json
Base de données principale des programmes
```json
{
  "Catégorie": {
    "Programme": {
      "description": "Description",
      "download_url": "https://...",
      "install_args": "/silent",
      "category": "Catégorie",
      "portable": true
    }
  }
}
```

## 🔄 Gestion des sauvegardes

- **Backup automatique** : Créé avant chaque modification
- **Retention** : Seule la sauvegarde la plus récente est conservée
- **Format** : `programs.json.backup_YYYYMMDD_HHMMSS`

## ⚠️ Notes importantes

- Ne pas modifier directement `programs.json` en production
- Toujours créer un backup avant modification
- Valider la syntaxe JSON après modification
- Les URLs doivent pointer vers les sites officiels

---
*Configuration organisée le 9 novembre 2025*