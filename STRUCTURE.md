# 📂 Structure du Projet NiTriTe V13

## Vue d'ensemble

```
Nitrite-V.13-Beta-Portable-/
│
├── 🚀 FICHIERS ESSENTIELS (Racine)
│   ├── nitrite_v13_modern.py      # Point d'entrée principal
│   ├── build_v13.py               # Script de build portable
│   ├── LANCER_V13.bat             # Lanceur Windows
│   ├── requirements.txt           # Dépendances Python
│   │
│   ├── README.md                  # Documentation principale
│   ├── README_V13.md              # Documentation détaillée
│   ├── DEMARRAGE_RAPIDE.md        # Guide rapide
│   └── STRUCTURE.md               # Ce fichier
│
├── 📦 DATA
│   ├── data/
│   │   └── programs.json          # Base 715 applications
│   │
│   └── assets/
│       └── icon.ico               # Icône application
│
├── 💻 CODE SOURCE
│   └── src/
│       ├── gui_modern_v13.py      # Interface moderne V13 ⭐
│       ├── profiles_manager.py    # Gestionnaire profils ⭐
│       │
│       ├── installer_manager.py   # Gestion installations
│       ├── config_manager.py      # Configuration
│       ├── elevation_helper.py    # Droits admin
│       ├── cleanup_manager.py     # Nettoyage
│       ├── portable_database.py   # Base données portable
│       ├── winget_manager.py      # Intégration WinGet
│       ├── winget_installer.py    # Installation WinGet
│       ├── dependency_manager.py  # Gestion dépendances
│       └── url_updater.py         # Validation URLs
│
├── 📦 ARCHIVE V12 (Historique)
│   └── _archive_v12/
│       ├── nitrite_complet.py     # Ancien point d'entrée
│       ├── build_nitrite_v12_final.py
│       ├── LANCER.bat
│       ├── README.md
│       ├── STRUCTURE_PROJET.md
│       │
│       ├── scripts/               # Anciens scripts utilitaires
│       ├── docs/                  # Ancienne documentation
│       ├── archives/              # Historique builds
│       │
│       ├── src/                   # Anciennes interfaces GUI
│       │   ├── gui_manager.py
│       │   ├── gui_manager_dark.py
│       │   ├── gui_manager_maxvisibility.py
│       │   ├── gui_manager_winget.py
│       │   └── gui_portable_db.py
│       │
│       └── README_ARCHIVE.md      # Info archive
│
└── ⚙️ CONFIGURATION
    ├── .gitignore                 # Fichiers ignorés Git
    └── .github/                   # Configuration GitHub
```

---

## 🎯 Fichiers Essentiels pour Utilisation

### Lancement de l'Application

**Option 1 : Script Python**
```bash
python nitrite_v13_modern.py
```

**Option 2 : Lanceur Windows**
```bash
LANCER_V13.bat
```

### Compilation Portable

```bash
python build_v13.py
```

Génère :
- `dist/NiTriTe_V13_Modern.exe` (exécutable)
- `dist/NiTriTe_V13_Portable_YYYYMMDD.zip` (package complet)

---

## 📝 Documentation

| Fichier | Contenu |
|---------|---------|
| `README.md` | Vue d'ensemble, démarrage rapide |
| `README_V13.md` | Documentation complète (500+ lignes) |
| `DEMARRAGE_RAPIDE.md` | Guide pas à pas détaillé |
| `STRUCTURE.md` | Structure du projet (ce fichier) |

---

## 💻 Code Source Clé

### Nouveautés V13 ⭐

1. **gui_modern_v13.py** (1400+ lignes)
   - Interface moderne à 2 pages
   - Navigation latérale élégante
   - Cartes Material Design
   - Animations fluides
   - Fenêtre de progression

2. **profiles_manager.py** (600+ lignes)
   - 10 profils prédéfinis
   - Gestionnaire de profils personnalisés
   - Système de favoris
   - Historique intelligent
   - Scanner de système

### Modules Réutilisés V12

3. **installer_manager.py**
   - Téléchargement d'applications
   - Installation silencieuse
   - Gestion WinGet

4. **config_manager.py**
   - Configuration application
   - Paramètres utilisateur

5. **elevation_helper.py**
   - Élévation privilèges admin
   - UAC Windows

6. **cleanup_manager.py**
   - Nettoyage après installation
   - Gestion temporaires

7. **portable_database.py**
   - Base de données SQLite
   - Apps portables

8. **winget_manager.py**
   - Intégration WinGet
   - Recherche packages

9. **dependency_manager.py**
   - Vérification dépendances
   - Auto-installation modules

10. **url_updater.py**
    - Validation URLs
    - Mise à jour liens

---

## 🗂️ Archive V12

Le dossier `_archive_v12/` contient :

### Conservé pour Référence
- ✅ Anciens points d'entrée
- ✅ Anciennes interfaces GUI
- ✅ Scripts utilitaires
- ✅ Documentation V12
- ✅ Historique des builds

### Non Utilisé par V13
- ❌ Interfaces GUI anciennes
- ❌ Scripts de test
- ❌ Documentation obsolète

**Note** : Ces fichiers sont archivés mais non supprimés pour historique et référence.

---

## 🔄 Workflow de Développement

### 1. Développement
```bash
# Modifier le code dans src/
nano src/gui_modern_v13.py

# Tester
python nitrite_v13_modern.py
```

### 2. Build Portable
```bash
# Compiler
python build_v13.py

# Tester l'exécutable
dist/NiTriTe_V13_Modern.exe
```

### 3. Distribution
```bash
# Partager l'archive
dist/NiTriTe_V13_Portable_YYYYMMDD.zip
```

---

## 🎨 Organisation Visuelle

```
┌─────────────────────────────────────┐
│  RACINE (Essentiels uniquement)    │
│  ├── Lanceurs                       │
│  ├── Documentation                  │
│  └── Build script                   │
├─────────────────────────────────────┤
│  DATA (Base de données)             │
│  ├── programs.json (715 apps)      │
│  └── assets (ressources)           │
├─────────────────────────────────────┤
│  SRC (Code source actif V13)        │
│  ├── GUI moderne ⭐                 │
│  ├── Profils ⭐                     │
│  └── Modules réutilisés            │
├─────────────────────────────────────┤
│  ARCHIVE (Historique V12)           │
│  └── Tout l'ancien code             │
└─────────────────────────────────────┘
```

---

## ✅ Avantages de cette Structure

1. ✨ **Racine propre** - Seulement fichiers essentiels
2. 📦 **Code organisé** - src/ contient uniquement code actif
3. 🗂️ **Archive propre** - Historique conservé mais séparé
4. 🚀 **Build simple** - Un seul script à la racine
5. 📚 **Documentation claire** - Plusieurs niveaux de détail

---

## 🎯 Pour Débuter

1. **Lire** : `README.md`
2. **Guide rapide** : `DEMARRAGE_RAPIDE.md`
3. **Tester** : `python nitrite_v13_modern.py`
4. **Compiler** : `python build_v13.py`
5. **Approfondir** : `README_V13.md`

---

*Structure V13.0 - Organisée et Optimisée*
*Dernière mise à jour : 2024-11-10*
