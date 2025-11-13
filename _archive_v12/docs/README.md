# 📚 Documentation NiTrite v2.0# NiTrite v.2 - Installateur de programmes automatique



## 📁 Organisation de la documentation## Description



### 📖 [guides/](guides/)NiTrite v.2 est un installateur de programmes automatique similaire à Ninite, développé spécialement pour Windows 10 et 11. Il permet d'installer plusieurs programmes de manière silencieuse avec une interface graphique complète et intuitive.

Documentation utilisateur finale

- Guides d'utilisation## Fonctionnalités

- Modes d'emploi portables

- Installation et configuration- ✅ Interface graphique moderne avec tkinter

- ✅ Installation silencieuse de multiples programmes

### 👨‍💻 [developpeur/](developpeur/)- ✅ Gestion automatique des dépendances

Documentation technique et développement- ✅ Nettoyage automatique des fichiers temporaires

- Intégration base de données- ✅ Support Windows 10/11

- Guides techniques- ✅ Journalisation complète des activités

- APIs et modules- ✅ Configurations prédéfinies (bureautique, développement)

- ✅ Base de données extensible de programmes

### 📜 [historique/](historique/)- ✅ Vérification d'intégrité des téléchargements

Correctifs et solutions passées- ✅ Détection des programmes déjà installés

- Corrections de bugs

- Solutions techniques## Programmes supportés

- Historique des modifications

### Navigateurs

### 🗄️ [archives/](archives/)- Mozilla Firefox

Anciennes versions et fichiers de référence- Google Chrome

- Versions précédentes

- Fichiers obsolètes conservés pour référence### Développement

- Logs de sessions- Visual Studio Code

- Git for Windows

## 🚀 Démarrage rapide- Python 3.11

- Node.js

1. **Utilisateurs** → Consultez [guides/](guides/)- Notepad++

2. **Développeurs** → Consultez [developpeur/](developpeur/)- PuTTY

3. **Historique** → Consultez [historique/](historique/)- FileZilla

- Wireshark

## 📋 Fichiers principaux

### Bureautique

- [`guides/GUIDE_UTILISATION_PORTABLE.md`](guides/GUIDE_UTILISATION_PORTABLE.md) - Guide principal- LibreOffice

- [`developpeur/INTEGRATION_REUSSIE.md`](developpeur/INTEGRATION_REUSSIE.md) - Documentation technique- Adobe Acrobat Reader DC

- [`README.md`](../README.md) - README principal du projet

### Multimédia

---- VLC Media Player

*Documentation organisée le 9 novembre 2025*
### Utilitaires
- 7-Zip
- WinRAR
- TeamViewer
- CCleaner

### Communication
- Discord

### Jeux
- Steam

### Sécurité
- Malwarebytes

## Prérequis

- Windows 10 ou Windows 11
- Python 3.8+ (optionnel, inclus dans l'exécutable)
- Connexion Internet
- Droits administrateur pour l'installation des programmes

## Installation et utilisation

### Méthode 1: Exécution directe (Recommandée)
1. Téléchargez le dossier complet du projet
2. Double-cliquez sur `nitrite_installer.py`
3. L'application installera automatiquement ses dépendances si nécessaire

### Méthode 2: Avec Python installé
```bash
cd "c:\Users\Momo\Documents\Projet NiTrite v.2"
python nitrite_installer.py
```

## Guide d'utilisation

### Interface principale
1. **Sélection des programmes**: Cochez les programmes que vous souhaitez installer
2. **Configurations prédéfinies**: Utilisez les boutons pour sélectionner rapidement:
   - Configuration bureautique (Firefox, Chrome, LibreOffice, VLC, etc.)
   - Configuration développeur (VS Code, Git, Python, Node.js, etc.)
3. **Installation**: Cliquez sur "Installer les programmes sélectionnés"
4. **Suivi**: Surveillez la progression dans la barre et les logs

### Fonctionnalités avancées
- **Rafraîchir**: Met à jour la liste des programmes disponibles
- **Logs détaillés**: Accédez aux logs complets pour le débogage
- **Arrêt d'urgence**: Stoppez l'installation en cours si nécessaire

## Structure du projet

```
Projet NiTrite v.2/
├── nitrite_installer.py          # Fichier principal
├── src/                          # Code source
│   ├── gui_manager.py           # Interface graphique
│   ├── installer_manager.py     # Gestionnaire d'installations
│   ├── dependency_manager.py    # Gestionnaire de dépendances
│   └── config_manager.py        # Gestionnaire de configuration
├── data/                        # Données de configuration
│   ├── config.json             # Configuration de l'application
│   └── programs.json           # Base de données des programmes
├── downloads/                   # Fichiers téléchargés (temporaire)
├── logs/                       # Fichiers de logs
├── assets/                     # Ressources (icônes, etc.)
└── dependencies/               # Dépendances locales (temporaire)
```

## Configuration

### Fichier config.json
```json
{
    "app_version": "2.0.0",
    "language": "fr",
    "auto_cleanup": true,
    "max_concurrent_downloads": 3,
    "download_timeout": 300,
    "install_timeout": 600,
    "verify_signatures": true,
    "create_restore_point": false,
    "log_level": "INFO"
}
```

### Ajouter un nouveau programme
Éditez `data/programs.json` et ajoutez une nouvelle entrée:
```json
"mon_programme": {
    "name": "Mon Programme",
    "description": "Description du programme",
    "category": "Ma Catégorie",
    "download_url": "https://exemple.com/setup.exe",
    "install_args": ["/silent"],
    "install_type": "exe",
    "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\MonProgramme",
    "cleanup_after_install": true
}
```

## Dépannage

### Problèmes courants

**Erreur de dépendances**
- L'application installe automatiquement ses dépendances
- En cas d'échec, vérifiez votre connexion Internet

**Échec d'installation d'un programme**
- Vérifiez les logs détaillés
- Assurez-vous d'avoir les droits administrateur
- Vérifiez que l'URL de téléchargement est valide

**Interface qui ne répond pas**
- Les installations se font en arrière-plan
- Utilisez le bouton "Arrêter" si nécessaire

### Logs
Les logs sont sauvegardés dans le dossier `logs/` avec horodatage.
Consultez-les pour diagnostiquer les problèmes.

## Sécurité

- ✅ Vérification d'intégrité des téléchargements (SHA256 quand disponible)
- ✅ Téléchargement uniquement depuis les sites officiels
- ✅ Installation silencieuse sans modifications système non désirées
- ✅ Nettoyage automatique des fichiers temporaires

## Limitations

- Nécessite une connexion Internet pour télécharger les programmes
- Certains programmes peuvent nécessiter une activation manuelle
- Les antivirus peuvent bloquer certains téléchargements (faux positifs)

## Support

Pour des problèmes ou suggestions:
1. Consultez les logs dans `logs/`
2. Vérifiez le fichier `programs.json` pour les URLs mises à jour
3. Assurez-vous d'avoir les dernières versions des programmes

## Changelog

### Version 2.0.0
- Interface graphique complète avec tkinter
- Gestion automatique des dépendances
- Installation silencieuse multiple
- Base de données extensible de programmes
- Journalisation complète
- Support Windows 10/11
- Nettoyage automatique

## Licence

Ce projet est développé pour un usage personnel et professionnel.
Les programmes installés sont soumis à leurs propres licences respectives.

## Développement

Le projet est structuré de manière modulaire pour faciliter:
- L'ajout de nouveaux programmes
- La modification de l'interface
- L'extension des fonctionnalités
- La maintenance du code

Chaque module a une responsabilité spécifique et peut être modifié indépendamment.