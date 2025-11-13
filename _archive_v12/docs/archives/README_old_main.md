# 🚀 NiTrite OrdiPlus v2.0

**Installation automatique de 240+ programmes Windows en un clic !**

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org)
[![Licence](https://img.shields.io/badge/licence-MIT-orange.svg)](LICENSE)

---

## 📋 Table des matières

- [À propos](#-à-propos)
- [Démarrage rapide](#-démarrage-rapide)
- [Version portable](#-version-portable)
- [Fonctionnalités](#-fonctionnalités)
- [Structure du projet](#-structure-du-projet)
- [Documentation](#-documentation)

---

## 🎯 À propos

**NiTrite OrdiPlus** est un installateur automatique de programmes Windows avec interface graphique. Il permet d'installer rapidement tous vos logiciels préférés sans chercher et télécharger manuellement chaque programme.

### ✨ Points forts :
- ✅ **240+ programmes** disponibles
- ✅ Interface graphique **intuitive**
- ✅ Installation **automatique** avec WinGet en fallback
- ✅ **Version portable** prête à distribuer
- ✅ Gestion des **privilèges administrateur**
- ✅ **Multi-threading** pour installations rapides

---

## 🚀 Démarrage rapide

### 📦 Installation standard

```bash
# 1. Cloner le projet
git clone https://github.com/votre-repo/nitrite-ordiplus.git
cd nitrite-ordiplus

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python nitrite_complet.py
```

### 🎮 Utilisation

1. **Sélectionnez** les programmes à installer (cochez les cases)
2. **Cliquez** sur le bouton "Installer la sélection"
3. **Attendez** que NiTrite télécharge et installe tout automatiquement
4. **Profitez** de vos programmes ! 🎉

---

## 📦 Version Autonome (100% Portable)

### 🛠️ Créer la version autonome

```bash
# Exécuter le script de build
python build_exe.py

# OU via batch
BUILD_EXE_RAPIDE.bat

# Résultat : NiTrite_Autonome_v2.0.zip créé en ~5 minutes
```

### 📤 Distribuer

Le fichier **`NiTrite_Autonome_v2.0.zip`** est prêt à partager :
- ✅ ~25 MB (Python + tkinter + dépendances inclus)
- ✅ **AUCUNE installation requise** sur PC cible
- ✅ Fonctionne sur **100% des PC Windows**
- ✅ README détaillé inclus
- ❌ **PAS BESOIN de Python** sur PC cible

### 🚀 Utilisation (Pour l'utilisateur final)

```bash
# 1. Décompresser le ZIP
# 2. Double-clic sur NiTrite_OrdiPlus_v2.exe
# 3. C'est tout ! ✅ (Aucune dépendance requise)
```

---

## 🌟 Fonctionnalités

### 📊 Catégories de programmes

| Catégorie | Exemples | Nombre |
|-----------|----------|--------|
| 🌐 **Navigateurs** | Chrome, Firefox, Brave, Opera | 10+ |
| 💬 **Messagerie** | Discord, WhatsApp, Telegram, Signal | 15+ |
| 🎬 **Multimédia** | VLC, OBS Studio, Audacity, GIMP | 30+ |
| 🎮 **Gaming** | Steam, Epic Games, GeForce Now | 20+ |
| 💼 **Productivité** | Office, LibreOffice, Notion, PDF | 50+ |
| 🛠️ **Développement** | VS Code, Git, Python, Docker | 40+ |
| 🔧 **Utilitaires** | 7-Zip, WinRAR, CCleaner | 40+ |
| 🔒 **Sécurité** | Malwarebytes, KeePass, Bitwarden | 20+ |
| ⚙️ **Système** | PowerToys, Process Explorer, CPU-Z | 20+ |

### 🔧 Fonctionnalités techniques

- **Installation intelligente** :
  - Téléchargement direct depuis URLs officielles
  - Fallback automatique vers WinGet si URL manquante
  - Détection et installation des dépendances
  
- **Gestion des privilèges** :
  - Élévation automatique des privilèges admin
  - 3 méthodes de fallback (PowerShell → runas → normal)
  
- **Interface utilisateur** :
  - Interface graphique tkinter moderne
  - Barre de progression pour chaque installation
  - Logs détaillés en temps réel
  
- **Performance** :
  - Multi-threading pour installations parallèles
  - Cache des téléchargements
  - Optimisation de la mémoire

---

## 📁 Structure du projet

```
NiTrite v.2/
│
├── 🚀 FICHIERS PRINCIPAUX
│   ├── nitrite_complet.py              # Application principale
│   ├── build_exe.py                    # Build version autonome
│   ├── BUILD_EXE_RAPIDE.bat           # Build via batch
│   ├── requirements.txt                # Dépendances Python
│   └── NiTrite_OrdiPlus_v2.spec       # Configuration PyInstaller
│
├── 📦 DISTRIBUTION
│   ├── NiTrite_Autonome/            # Version autonome (dossier)
│   └── NiTrite_Autonome_v2.0.zip   # Version autonome (ZIP - 25 MB)
│
├── 📁 CODE SOURCE
│   ├── src/
│   │   ├── installer_manager.py        # Gestion des installations
│   │   ├── winget_installer.py         # Intégration WinGet
│   │   ├── config_manager.py           # Configuration
│   │   ├── url_updater.py              # Mise à jour URLs
│   │   └── ...
│   │
│   ├── data/
│   │   ├── programs.json               # Base de données (240+ programmes)
│   │   ├── config.json                 # Configuration
│   │   └── ...
│   │
│   └── tests/
│       └── anciens_tests/              # Scripts de test archivés
│
├── 📚 DOCUMENTATION
│   ├── README.md                       # Ce fichier
│   ├── docs/                           # Documentation utilisateur
│   ├── SOLUTION_ERREUR_1.md           # Guide dépannage
│   ├── DEMARRAGE_RAPIDE_PORTABLE.md   # Guide portable
│   └── GUIDE_VERSION_PORTABLE.md      # Guide technique
│
└── 🗄️ ARCHIVES
    ├── scripts_dev/                    # Scripts de développement
    ├── builds_anciens/                 # Anciens builds
    ├── documentation_dev/              # Documentation technique
    └── ...
```

---

## 📖 Documentation

### 📘 Guides utilisateur

- **[Guide de démarrage rapide](docs/DEMARRAGE_RAPIDE.txt)** - Premiers pas avec NiTrite
- **[Guide utilisateur complet](docs/GUIDE_UTILISATEUR.md)** - Toutes les fonctionnalités
- **[README Autonome](README_AUTONOME.md)** - Documentation version autonome

### 🔧 Documentation technique

- **[Solution erreur 1](SOLUTION_ERREUR_1.md)** - Résolution du problème tkinter
- **[Guide versions portables](GUIDE_VERSIONS_PORTABLES.md)** - Comparaison des approches
- **[Archives documentation](archives/documentation_dev/)** - Historique des corrections

### 🛠️ Pour les développeurs

- **[Tests](tests/anciens_tests/)** - Scripts de test archivés
- **[Scripts dev](archives/scripts_dev/)** - Outils de développement
- **[Builds anciens](archives/builds_anciens/)** - Historique des builds

---

## 💻 Configuration requise

### Version autonome (.exe) :
- ✅ Windows 10/11 (64-bit recommandé)
- ✅ 4 GB RAM minimum
- ✅ Connexion Internet
- ❌ **AUCUN Python requis**
- ❌ **AUCUNE dépendance à installer**

### Version standard (pour développement) :
- ✅ Windows 10/11 (64-bit recommandé)
- ✅ Python 3.8 ou supérieur
- ✅ 4 GB RAM minimum
- ✅ Connexion Internet

### Optionnel :
- ⚙️ WinGet (Windows Package Manager) - Améliore le taux de réussite à 85-90%

---

## 🔧 Dépannage

### Problème : "Python n'est pas reconnu..."
**Solution :** Installez Python depuis python.org et cochez "Add Python to PATH"

### Problème : "ModuleNotFoundError"
**Solution :** Exécutez `pip install -r requirements.txt`

### Problème : "Échec d'installation d'un programme"
**Solution :** 
- Vérifiez votre connexion Internet
- Installez WinGet pour le fallback automatique
- Consultez les logs dans le dossier `logs/`

### Plus d'aide :
Consultez **[SOLUTION_ERREUR_1.md](SOLUTION_ERREUR_1.md)** pour les problèmes courants

---

## 📊 Statistiques du projet

- **Programmes disponibles** : 240+
- **Taux de réussite** : 85-90% (avec WinGet)
- **Taille version autonome** : ~25 MB (Python inclus)
- **Taille exécutable** : ~27 MB
- **Temps de build** : ~5 minutes
- **Catégories** : 9 catégories principales

---

## 🎊 Changelog

### Version 2.0 (5 novembre 2025)
- ✅ **Version autonome** avec Python embarqué (PyInstaller)
- ✅ AUCUNE dépendance requise sur PC cible
- ✅ Un seul .exe de 27 MB
- ✅ Ajout de 240+ programmes
- ✅ Intégration WinGet en fallback
- ✅ Interface graphique améliorée
- ✅ Documentation complète
- ✅ Nettoyage et organisation du projet

### Version 1.0
- 🎉 Version initiale

---

## 📝 Licence

MIT License - Voir le fichier LICENSE pour plus de détails

---

## 🙏 Remerciements

Merci à tous les utilisateurs et contributeurs qui ont rendu ce projet possible !

---

## 📞 Contact & Support

Pour toute question ou suggestion :
- 📧 Créez une issue sur GitHub
- 💬 Consultez la documentation dans `docs/`
- 🐛 Rapportez les bugs via GitHub Issues

---

**🚀 Profitez de NiTrite OrdiPlus ! Installation simplifiée pour tous vos programmes Windows !**

*Dernière mise à jour : 5 novembre 2025*
