# 🚀 CHANGELOG NiTrite v.2 - Améliorations OrdiPlus

## 📅 Date : 4 Novembre 2025

### ✨ Nouvelles fonctionnalités

#### 1️⃣ Catégorie "Outils OrdiPlus" réorganisée
La catégorie a été **complètement refaite** avec les outils essentiels pour les techniciens :

- ✅ **AnyDesk Portable** - Bureau à distance (version portable)
- ✅ **RustDesk Portable** - Bureau à distance open source (version portable)
- ✅ **Malwarebytes** - Protection anti-malware
- ✅ **AdwCleaner** - Suppression d'adwares et PUPs
- ✅ **Wise Disk Cleaner** - Nettoyage avancé des disques
- ✅ **Spybot Search & Destroy** - Détection de spywares
- ✅ **Adobe Acrobat Reader DC** - Lecteur PDF officiel
- ✅ **VLC Media Player** - Lecteur multimédia universel
- ✅ **Mozilla Firefox** - Navigateur web

#### 2️⃣ Nouvelle catégorie "Pack Office"
Une nouvelle catégorie dédiée aux éditions Microsoft Office en **français** :

- 📦 Office 2007 Pro Plus (FR)
- 📦 Office 2010 Pro Plus (FR)
- 📦 Office 2013 Pro Plus (FR)
- 📦 Office 2016 Pro Plus (FR)
- 📦 Office 2019 Pro Plus (FR)
- 📦 Office 2021 Pro Plus (FR)
- 📦 Office 2024 LTSC Pro Plus (FR)

*Sources : https://gravesoft.dev/office_c2r_links#french-fr-fr*

#### 3️⃣ Boutons d'activation Windows
Deux nouveaux boutons dans la barre d'outils :

- 🔐 **MAS (Activation)** - Ouvre le site https://massgrave.dev/
- ⚡ **Activer Windows** - Lance la commande `irm https://get.activated.win | iex` en PowerShell admin

#### 4️⃣ Dossier "Outils de nettoyage"
Création automatique d'un dossier sur le **Bureau** après installation contenant :

- 📁 Raccourcis vers : Malwarebytes, AdwCleaner, Wise Disk Cleaner, Spybot
- 📂 Exécutables portables : AnyDesk.exe, RustDesk.exe

### 🎨 Améliorations de l'interface

#### Optimisation de l'espace
- ✅ **5 colonnes** au lieu de 4 pour les programmes (gain de place)
- ✅ Réduction des **paddings** et marges
- ✅ **Polices plus petites** mais lisibles :
  - Titre : 16pt (au lieu de 18pt)
  - Catégories : 11pt (au lieu de 13pt)
  - Programmes : 9pt (au lieu de 10pt)
  - Boutons : 9pt (au lieu de 10pt)
- ✅ Descriptions raccourcies (max 40 caractères)
- ✅ Bouton d'installation renommé "🚀 INSTALLER" (plus court)

#### Organisation des catégories
L'ordre d'affichage a été optimisé :
1. 🛠️ Outils OrdiPlus *(EN PREMIER)*
2. 📦 Pack Office
3. 🌐 Navigateurs
4. 📝 Bureautique
5. 🎨 Multimédia
6. 💻 Développement
7. 🔧 Utilitaires
8. 🛡️ Sécurité
9. 💬 Communication
10. 🎮 Jeux
11. 🌍 Internet

### 🔧 Modifications techniques

#### Fichiers modifiés
- ✅ `data/programs.json` - Ajout des nouvelles catégories et programmes
- ✅ `src/gui_manager_complet.py` - Refonte complète de l'interface
- ✅ `install_requirements.bat` - Script d'installation des dépendances

#### Nouvelles dépendances
Pour la création du dossier "Outils de nettoyage" :
```bash
pip install pywin32
pip install winshell
```

Lancer `install_requirements.bat` pour les installer automatiquement.

### 📝 Notes d'utilisation

#### Pour les techniciens
1. Sélectionnez **"🛠️ OrdiPlus"** pour installer tous les outils essentiels
2. Utilisez **"🔐 MAS"** pour accéder aux scripts d'activation
3. Cliquez sur **"⚡ Activer Windows"** pour lancer l'activation directement
4. Après installation, retrouvez tous les outils de nettoyage sur le **Bureau**

#### Pack Office
- Les éditions Office sont téléchargées depuis les serveurs Microsoft officiels
- Pour l'activation, utilisez le bouton **"⚡ Activer Windows"** ou le site MAS

### 🐛 Correctifs
- ✅ Suppression de AnyDesk et RustDesk de la catégorie "Communication"
- ✅ Ajout en version portable dans "Outils OrdiPlus"
- ✅ Optimisation de l'affichage pour éviter le débordement

### 🎯 Objectifs atteints
- ✅ Catégorie OrdiPlus réorganisée avec les bons outils
- ✅ Pack Office complet en français
- ✅ Boutons d'activation Windows intégrés
- ✅ Dossier automatique sur le Bureau
- ✅ Interface plus compacte et efficace

---

**Version** : NiTrite v.2.5 OrdiPlus Edition  
**Développé pour** : Techniciens de maintenance informatique  
**Statut** : ✅ Prêt pour déploiement
