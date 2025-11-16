# 🚀 NiTriTe V13 - Outil de Maintenance Informatique Moderne

![Version](https://img.shields.io/badge/version-13.0-orange)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey)

**Application professionnelle pour techniciens de maintenance informatique**

Interface moderne avec 715 applications et 547 outils système.

---

## ✨ Fonctionnalités

- 🎨 **Interface moderne** - Design noir & orange premium
- 📦 **715 applications** organisées en 25 catégories
- 🛠️ **547 outils système** répartis en 12 sections
- 🎯 **10 profils prédéfinis** - Gaming, Bureau, Développeur, etc.
- ⭐ **Système de favoris** - Personnalisation avancée
- 🌐 **Version web** - Interface HTML/CSS/JavaScript
- 💻 **Version bureau** - Application Tkinter
- 📦 **Mode portable** - Aucune installation requise

---

## 🚀 Démarrage Rapide

### 1️⃣ Installation des Dépendances

```bash
# Installer toutes les dépendances Python
pip install -r requirements.txt

# OU utiliser le script batch (Windows)
INSTALL_DEPS_PORTABLE.bat
```

### 2️⃣ Lancer l'Application

#### 🌐 Version Web (Recommandée)

```bash
# Lancer le serveur web Flask
python web_backend.py

# Puis ouvrir dans le navigateur
http://localhost:5000
```

**OU** double-cliquez sur `LANCER_WEB.bat`

**Fonctionnalités web :**
- Interface responsive HTML/CSS/JavaScript
- 715 applications installables
- 547 outils système avec bypass UAC
- Master Installation avec actions rapides
- Export de scripts PowerShell
- Génération de commandes One-Liner
- Thèmes multiples (6 disponibles)
- Paramètres import/export

---

#### 💻 Version Bureau (Tkinter)

```bash
# Lancer l'application de bureau
python nitrite_v13_modern.py
```

**OU** double-cliquez sur `LANCER_V13.bat`

**Fonctionnalités bureau :**
- Interface Tkinter moderne
- Installation locale d'applications
- Gestion des profils
- Historique intelligent
- Scanner de système

---

#### 📦 Versions Portables (.exe)

**Version Web Portable (Recommandée)**
```bash
# Compiler la version web en .exe
BUILD_WEB.bat

# Résultat : dist/NiTriTe_Web_V13.exe
# Lance serveur Flask + ouvre navigateur automatiquement
```

**Version Bureau Portable**
```bash
# Compiler la version bureau en .exe
BUILD.bat

# Résultat : dist/NiTriTe_V13_Modern.exe
# Interface Tkinter standalone
```

**Avantages portable :**
- ✅ Aucune installation Python requise
- ✅ Exécutable standalone (.exe)
- ✅ Transportable sur clé USB
- ✅ Prêt à l'emploi sur n'importe quel PC Windows
- ✅ Version web : Navigateur s'ouvre automatiquement

---

## 📁 Structure du Projet

```
Nitrite-V.13-Beta-Portable-web-/
│
├── 🌐 VERSION WEB
│   ├── web_backend.py              # Backend Flask API
│   └── web/                        # Interface web
│       ├── index.html              # Page principale
│       ├── css/                    # Styles
│       │   ├── styles.css          # Styles principaux
│       │   └── advanced.css        # Styles pages avancées
│       ├── js/                     # JavaScript
│       │   ├── app.js              # Application principale
│       │   ├── api.js              # Communication API
│       │   └── advanced.js         # Pages avancées
│       └── data/
│           └── tools.json          # 547 outils système
│
├── 💻 VERSION BUREAU
│   ├── nitrite_v13_modern.py       # Point d'entrée bureau
│   └── src/                        # Code source
│       ├── gui_modern_v13.py       # Interface Tkinter
│       ├── advanced_pages.py       # Pages avancées
│       ├── profiles_manager.py     # Gestionnaire profils
│       ├── installer_manager.py    # Gestion installations
│       ├── winget_manager.py       # Intégration WinGet
│       ├── elevation_helper.py     # Bypass UAC
│       ├── config_manager.py       # Configuration
│       ├── portable_database.py    # DB portable
│       ├── tools_data_complete.py  # 547 outils
│       └── [autres modules...]
│
├── 📦 DONNÉES
│   ├── data/
│   │   └── programs.json           # Base 715 applications
│   └── assets/
│       └── icon.ico                # Icône application
│
├── 🔧 SCRIPTS
│   ├── LANCER_WEB.bat              # Lanceur version web
│   ├── LANCER_V13.bat              # Lanceur version bureau
│   ├── BUILD.bat                   # Build version portable
│   └── INSTALL_DEPS_PORTABLE.bat   # Installation dépendances
│
├── 📄 FICHIERS CONFIG
│   ├── requirements.txt            # Dépendances Python
│   ├── NiTriTe_V13.spec            # Config PyInstaller
│   └── .gitignore
│
└── README.md                       # Ce fichier
```

---

## 🌐 Version Web - Détails

### Pages Disponibles

1. **📱 Applications** (715 apps)
   - Recherche en temps réel
   - Filtrage par catégorie
   - Installation WinGet
   - Liens vers sites officiels

2. **🛠️ Outils Système** (547 outils en 12 sections)
   - 🔨 Réparation Système (30 outils)
   - 🔧 Activation & Téléchargements (30 outils)
   - 🧹 Maintenance & Nettoyage (16 outils)
   - 📊 Diagnostics & Infos (57 outils)
   - 🌐 Réseau & Internet (23 outils)
   - ⚡ WinGet Package Manager (12 outils)
   - ⚙️ Paramètres Windows (20 outils)
   - 🏭 Support Fabricants (18 outils)
   - 🛒 Fournisseurs & Achats (96 outils)
   - 📊 Benchmark & Tests (227 outils)
   - 🔧 Drivers (11 outils)
   - 📚 Documentation (7 outils)

3. **📦 Master Installation**
   - Sélection d'apps essentielles
   - Actions rapides (12 boutons)
   - Export script PowerShell
   - Génération commande One-Liner
   - WinGet Manager

4. **🔍 Diagnostic**
   - Informations système
   - État du matériel
   - Vérifications automatiques

5. **⚡ Optimisation**
   - Tweaks performance
   - Désactivation télémétrie
   - Nettoyage système
   - Optimisation services

6. **💾 Sauvegarde**
   - Point de restauration
   - Backup drivers
   - Export liste apps

7. **⚙️ Paramètres**
   - Choix de langue (FR/EN)
   - 6 thèmes disponibles
   - Export/Import settings

### Bypass UAC

Toutes les commandes système s'exécutent **sans prompts UAC** grâce à :
- Endpoint `/api/execute-command` avec élévation automatique
- Utilisation de `elevation_helper.py`
- Exécution silencieuse des commandes PowerShell et CMD

---

## 💻 Version Bureau - Détails

### Avantages

- Interface native Windows (Tkinter)
- Pas besoin de navigateur
- Intégration système complète
- Base de données SQLite locale
- Historique persistant

### Pages Principales

1. **Applications** - Installation d'apps via WinGet
2. **Outils Système** - 547 outils organisés
3. **Profils** - 10 profils prédéfinis
4. **Favoris** - Apps favorites
5. **Historique** - Statistiques d'utilisation

---

## 📦 Profils Prédéfinis

Les 10 profils disponibles dans les deux versions :

1. 🎮 **Gaming Station** - Setup PC gaming complet
2. 💼 **Bureau Professionnel** - Suite bureautique
3. 💻 **Développeur** - Environnement dev complet
4. 🎨 **Création Multimédia** - Outils photo/vidéo/audio
5. 🏫 **Étudiant** - Pack essentiel étudiants
6. 🔧 **Maintenance Technique** - Outils techniciens
7. 🏠 **Maison/Famille** - Usage domestique
8. ⚡ **Installation Express** - Pack minimal rapide
9. 🎬 **Home Cinema** - PC multimédia
10. 🌐 **Télétravail** - Outils travail à distance

---

## 🎨 Thème Visuel

**Palette Noir & Orange Premium**

- Noir profond (#0a0a0a, #1e1e2e)
- Orange principal (#ff6b00)
- Vert succès (#00e676, #00c853)
- Bleu info (#00b0ff, #2196f3)
- Animations fluides
- Design Material moderne

---

## 🔧 Configuration Requise

- **OS** : Windows 10/11
- **Python** : 3.8+ (pour versions script)
- **RAM** : 4 GB minimum (8 GB recommandé)
- **Résolution** : 1280x720 minimum (1920x1080 recommandé)
- **Internet** : Connexion requise pour installations
- **WinGet** : Installé automatiquement si manquant

---

## 🛠️ Développement

### Structure du Code

#### Backend Flask (`web_backend.py`)
- Routes API pour applications, outils, profils
- Endpoint d'exécution avec UAC bypass
- Gestion des installations
- Diagnostics système
- Optimisations Windows

#### Frontend Web (`web/`)
- **HTML** : Interface responsive
- **CSS** : Styles modernes avec animations
- **JavaScript** : Communication API, gestion UI

#### Code Tkinter (`src/`)
- Interface graphique native
- Gestionnaires de fonctionnalités
- Modules réutilisables

---

## 📊 Statistiques

- **715 applications** disponibles
- **25 catégories** organisées
- **547 outils système** en 12 sections
- **10 profils** prédéfinis
- **2 versions** (Web + Bureau)
- **1 version portable** (compilée)
- **100% offline capable** (après installations)

---

## 🎯 Cas d'Usage

### Pour Techniciens
1. Setup rapide client
2. Profil adapté au besoin
3. Installation automatique
4. Outils de réparation intégrés
5. Export de scripts pour réutilisation

### Pour Particuliers
1. Choisir version (Web ou Bureau)
2. Sélectionner profil
3. Installer applications
4. Utiliser outils système
5. Personnaliser avec favoris

---

## 🆕 Nouveautés V13

✨ **Interface moderne redesignée**
🌐 **Version web HTML/CSS/JavaScript**
📦 **Master Installation avec export PowerShell**
🔧 **547 outils système (vs 553 avant)**
⚡ **Bypass UAC pour toutes commandes**
🎨 **6 thèmes visuels**
🌍 **Support multilingue (FR/EN)**
📊 **Actions rapides (12 boutons)**

---

## 🤝 Support

- **Documentation** : Ce README.md
- **Code source** : Commenté et documenté
- **Issues** : Utiliser GitHub Issues

---

## 📝 Licence

**NiTriTe V13** - Outil professionnel pour maintenance informatique

© 2024 - Tous droits réservés

---

## 🎉 Prêt à Utiliser !

### Version Web (Recommandée)
```bash
python web_backend.py
# Ouvrir http://localhost:5000
```

### Version Bureau
```bash
python nitrite_v13_modern.py
```

### Version Web Portable (.exe)
```bash
BUILD_WEB.bat
# Double-cliquer sur dist/NiTriTe_Web_V13.exe
# Le navigateur s'ouvre automatiquement !
```

### Version Bureau Portable (.exe)
```bash
BUILD.bat
# Double-cliquer sur dist/NiTriTe_V13_Modern.exe
```

**Bon succès avec NiTriTe V13 ! 🚀**

---

*Version 13.0 - Modern Edition*
*Développé avec ❤️ pour les techniciens de maintenance*
