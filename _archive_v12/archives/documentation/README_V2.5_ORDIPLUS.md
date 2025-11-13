# 🚀 NiTrite v.2.5 - Édition OrdiPlus

## 📋 Description

**NiTrite v.2.5** est un installateur automatique de programmes conçu spécialement pour les **techniciens de maintenance informatique**. L'application permet d'installer rapidement et silencieusement plus de **90 programmes** depuis leurs sources officielles.

### ✨ Nouveautés de la version 2.5 OrdiPlus

- 🛠️ **Catégorie OrdiPlus** dédiée aux outils essentiels pour techniciens
- 📦 **Pack Office complet** (2019, 2021, 2024 LTSC) en français
- 🔐 **Activation Windows/Office** intégrée (via MAS)
- 📁 **Dossier "Outils de nettoyage"** créé automatiquement sur le Bureau
- 🎨 **Interface optimisée** - 5 colonnes, polices réduites, meilleure organisation
- ⚡ **Boutons rapides** pour activation et accès MAS

---

## 📦 Contenu

### 🛠️ Outils OrdiPlus (9 programmes)

**Outils de bureau à distance :**
- AnyDesk Portable (exécutable)
- RustDesk Portable (exécutable)

**Outils de nettoyage et sécurité :**
- Malwarebytes
- AdwCleaner
- Wise Disk Cleaner
- Spybot Search & Destroy

**Logiciels essentiels :**
- Adobe Acrobat Reader DC
- VLC Media Player
- Mozilla Firefox

### 📦 Pack Office (3 éditions)

- Office 2019 Professional Plus (FR)
- Office 2021 Professional Plus (FR)
- Office 2024 LTSC Professional Plus (FR)

*Sources officielles Microsoft C2R*

### 🌐 Autres catégories (80+ programmes)

- **Navigateurs** : Chrome, Firefox, Edge, Brave, Opera, Vivaldi
- **Développement** : VS Code, Git, Node.js, Python, IntelliJ, Android Studio
- **Jeux** : Steam, Epic Games, GOG Galaxy, Discord
- **Sécurité** : Malwarebytes, Bitdefender, Avast, CCleaner
- **Utilitaires** : 7-Zip, WinRAR, Everything, PowerToys
- **Communication** : TeamViewer, Skype, Zoom, Teams, Slack
- **Multimédia** : VLC, OBS Studio, GIMP, Audacity
- **Bureautique** : LibreOffice, Adobe Reader, SumatraPDF
- **Internet** : FileZilla, qBittorrent, JDownloader

---

## 🚀 Installation

### 1️⃣ Prérequis

- Windows 10/11 (64-bit recommandé)
- Python 3.8 ou supérieur
- Connexion Internet

### 2️⃣ Installation des dépendances

Double-cliquez sur :
```
install_requirements.bat
```

Ou manuellement :
```powershell
pip install pywin32 winshell tkinter requests
```

### 3️⃣ Lancement

Double-cliquez sur :
```
Lancer_NiTrite.bat
```

Ou utilisez :
```
Lancer_NiTrite_Complet.bat  # Version complète (tous les programmes)
Lancer_NiTrite_DARK.bat     # Mode sombre
```

---

## 📖 Guide d'utilisation

### 🛠️ Installation rapide des Outils OrdiPlus

1. Lancez NiTrite
2. Cliquez sur **"🛠️ OrdiPlus (9)"** dans la barre d'outils
3. Cliquez sur **"🚀 INSTALLER"**
4. Attendez la fin de l'installation
5. Retrouvez le dossier **"Outils de nettoyage"** sur votre Bureau

### 📦 Installer un Pack Office

1. Développez la catégorie **"📦 PACK OFFICE"**
2. Cochez la version souhaitée (2019, 2021 ou 2024)
3. Cliquez sur **"🚀 INSTALLER"**
4. Pour l'activation, utilisez le bouton **"⚡ Activer Windows"**

### ⚡ Activer Windows/Office

**Méthode 1 : Via le site**
- Cliquez sur **"🔐 MAS (Activation)"**
- Le site https://massgrave.dev/ s'ouvrira
- Suivez les instructions

**Méthode 2 : Direct**
- Cliquez sur **"⚡ Activer Windows"**
- Acceptez les privilèges administrateur
- Le script d'activation se lance automatiquement

### 🎯 Sélection rapide

- **✅ TOUT** - Sélectionne tous les programmes
- **❌ RIEN** - Désélectionne tout
- **Boutons par catégorie** - Sélectionne tous les programmes d'une catégorie

---

## 📁 Structure du projet

```
Projet NiTrite v.2/
├── Lancer_NiTrite.bat              # Lanceur principal
├── install_requirements.bat         # Installation dépendances
├── nitrite_complet.py              # Script principal
├── data/
│   ├── programs.json               # Base de données programmes
│   └── office_links.json           # Liens Office officiels
├── src/
│   ├── gui_manager_complet.py      # Interface graphique
│   ├── installer_manager.py        # Gestionnaire installation
│   └── config_manager.py           # Configuration
├── logs/                           # Logs d'installation
├── downloads/                      # Fichiers téléchargés
└── docs/                           # Documentation
```

---

## 🔧 Fonctionnalités techniques

### Installation silencieuse
- ✅ Tous les programmes s'installent **sans interaction**
- ✅ Paramètres `/silent` `/S` `/quiet` adaptés à chaque programme
- ✅ Rejet automatique des publicités et logiciels tiers

### Téléchargement intelligent
- ✅ Sources **officielles uniquement**
- ✅ Vérification de l'intégrité
- ✅ Barre de progression en temps réel
- ✅ Gestion des erreurs et retry automatique

### Interface optimisée
- ✅ **5 colonnes** pour affichage compact
- ✅ Catégories **pliables/dépliables**
- ✅ Recherche et filtrage rapides
- ✅ Plein écran automatique

### Logs détaillés
- ✅ Tous les événements sont enregistrés dans `logs/nitrite.log`
- ✅ Horodatage de chaque action
- ✅ Messages d'erreur détaillés

---

## 🐛 Résolution des problèmes

### Le dossier "Outils de nettoyage" n'est pas créé
```powershell
# Réinstaller les dépendances
pip install --force-reinstall pywin32 winshell
```

### Erreur lors du téléchargement
- Vérifiez votre connexion Internet
- Désactivez temporairement votre antivirus/firewall
- Consultez les logs : `logs/nitrite.log`

### Le bouton "Activer Windows" ne fonctionne pas
- Assurez-vous d'avoir les droits administrateur
- Vérifiez que PowerShell n'est pas bloqué
- Utilisez la méthode manuelle via le site MAS

### Programme non installé
- Vérifiez les logs pour les messages d'erreur
- Certains programmes nécessitent des dépendances (.NET, Visual C++)
- Essayez de relancer l'installation du programme individuel

---

## 📝 Changelog

### Version 2.5 OrdiPlus (4 Nov 2025)
- ✅ Nouvelle catégorie "Outils OrdiPlus" avec 9 outils essentiels
- ✅ Catégorie "Pack Office" avec 3 éditions en français
- ✅ Boutons d'activation Windows/Office intégrés
- ✅ Création automatique du dossier "Outils de nettoyage"
- ✅ Interface optimisée (5 colonnes, polices réduites)
- ✅ Réorganisation des catégories (OrdiPlus en premier)

### Version 2.4 (Précédente)
- Interface complète avec 80+ programmes
- Mode sombre disponible
- Système de catégories amélioré

---

## 👨‍💻 Développement

### Technologies utilisées
- **Python 3.x** - Langage principal
- **Tkinter** - Interface graphique
- **Requests** - Téléchargements HTTP
- **Threading** - Installations asynchrones
- **JSON** - Base de données programmes

### Architecture
- **MVC** - Séparation GUI / Logic / Data
- **Threading** - Installation non-bloquante
- **Logging** - Traçabilité complète
- **Error handling** - Gestion robuste des erreurs

---

## 📄 Licence

Ce projet est destiné à un usage personnel et professionnel par les techniciens de maintenance informatique.

**Attention** : 
- Les programmes installés sont soumis à leurs propres licences
- L'activation de Windows/Office doit respecter les termes de Microsoft
- Le script d'activation MAS est un outil tiers indépendant

---

## 🙏 Remerciements

- **Microsoft** pour les liens Office C2R
- **Gravesoft** pour la documentation Office
- **MAS Team** pour les scripts d'activation
- **Communauté Open Source** pour tous les outils gratuits

---

## 📞 Support

Pour toute question ou problème :
1. Consultez les fichiers de documentation dans `docs/`
2. Vérifiez les logs dans `logs/nitrite.log`
3. Lisez le `CHANGELOG_ORDIPLUS.md` pour les dernières modifications

---

**🎯 NiTrite v.2.5 OrdiPlus Edition - Fait pour les techniciens, par des techniciens**
