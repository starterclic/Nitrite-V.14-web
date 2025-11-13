# 🚀 NiTriTe V13.0 - Outil de Maintenance Informatique Moderne

![Version](https://img.shields.io/badge/version-13.0-orange)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey)
![License](https://img.shields.io/badge/license-Proprietary-red)

**Application professionnelle pour techniciens de maintenance informatique**

Interface moderne avec 715 applications et 553+ outils système organisés.

---

## ✨ Nouveautés V13

- 🎨 **Interface entièrement redesignée** - Design moderne noir & orange
- 📦 **Navigation à 2 pages** - Applications + Outils Système
- 🎯 **10 profils prédéfinis** - Gaming, Bureau, Développeur, etc.
- ⭐ **Système de favoris** - Personnalisation avancée
- 📊 **Historique intelligent** - Statistiques d'utilisation
- 🔍 **Scanner de système** - Détection automatique des apps

---

## 🚀 Démarrage Rapide

### Installation et Lancement

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'application
python nitrite_v13_modern.py
```

**OU** double-cliquez sur `LANCER_V13.bat`

### Compiler en Version Portable

⚠️ **Le build doit être effectué sur Windows**

```bash
# Sur Windows uniquement
python build_v13.py

# Résultat dans dist/
# ├── NiTriTe_V13_Modern.exe
# └── NiTriTe_V13_Portable_YYYYMMDD.zip
```

📚 **Voir [GUIDE_BUILD_WINDOWS.md](GUIDE_BUILD_WINDOWS.md) pour instructions complètes**

---

## 📦 Fonctionnalités

### Page Applications (715 apps)

- **Cartes modernes** avec design Material
- **Recherche instantanée** par nom ou description
- **Statistiques temps réel** (total, catégories, sélections)
- **Boutons web** 🌐 pour accès direct aux sites
- **Installation en un clic** avec barre de progression
- **Badges visuels** : Portable, WinGet, Catégorie

### Page Outils Système (553+ boutons)

- **10+ sections organisées** par thématique
- **Exécution directe** des commandes système
- **Liens web** vers outils externes
- **Recherche rapide** d'outils

### Profils Prédéfinis

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

## 📁 Structure du Projet

```
Nitrite-V.13-Beta-Portable-/
├── nitrite_v13_modern.py      # 🚀 Point d'entrée
├── build_v13.py               # 🔨 Script de build
├── LANCER_V13.bat             # 🪟 Lanceur Windows
├── requirements.txt           # 📦 Dépendances
│
├── data/
│   └── programs.json          # Base 715 applications
│
├── src/                       # Code source
│   ├── gui_modern_v13.py      # Interface moderne
│   ├── profiles_manager.py    # Gestionnaire profils
│   ├── installer_manager.py   # Gestion installations
│   ├── config_manager.py      # Configuration
│   ├── elevation_helper.py    # Droits admin
│   ├── cleanup_manager.py     # Nettoyage
│   ├── portable_database.py   # DB portable
│   ├── winget_manager.py      # Intégration WinGet
│   └── [autres modules...]
│
├── assets/                    # Ressources visuelles
│   └── icon.ico
│
├── README_V13.md              # 📚 Documentation complète
├── DEMARRAGE_RAPIDE.md        # ⚡ Guide rapide
│
└── _archive_v12/              # 📦 Anciens fichiers V12
```

---

## 🎨 Thème Visuel

**Palette Noir & Orange Premium**

- Noir profond (#0a0a0a)
- Orange principal (#ff6b00)
- Vert succès (#00e676)
- Bleu info (#00b0ff)
- Animations fluides
- Design Material moderne

---

## 💡 Utilisation

### Navigation

1. **Barre latérale** : Basculer entre pages
   - 📦 Applications
   - 🛠️ Outils Système

2. **Recherche** : Taper pour filtrer instantanément

3. **Installation** :
   - Sélectionner les apps (checkbox)
   - Cliquer "🚀 INSTALLER"
   - Suivre la progression

4. **Accès web** : Cliquer 🌐 pour site officiel

### Profils

- Sélectionner un profil prédéfini
- Toutes les apps sont auto-sélectionnées
- Cliquer "INSTALLER"

### Outils Système

- Parcourir les sections
- Cliquer sur un outil pour l'exécuter
- Les commandes s'exécutent automatiquement

---

## 🔧 Configuration Requise

- **OS** : Windows 10/11
- **Python** : 3.8+ (pour version script)
- **RAM** : 4 GB minimum (8 GB recommandé)
- **Résolution** : 1400x900 minimum
- **Internet** : Connexion requise pour téléchargements

---

## 📚 Documentation

- **README_V13.md** - Documentation complète (500+ lignes)
- **DEMARRAGE_RAPIDE.md** - Guide de démarrage rapide
- Code source commenté dans `src/`

---

## 🎯 Cas d'Usage

### Pour Techniciens
```
1. Setup rapide client
2. Profil adapté au besoin
3. Installation automatique
4. Outils de réparation intégrés
```

### Pour Particuliers
```
1. Choisir profil (Gaming, Bureau, etc.)
2. Installer applications
3. Personnaliser avec favoris
4. Utiliser outils système
```

---

## 🔄 Compilation Portable

Le script `build_v13.py` crée automatiquement :

1. **Exécutable standalone** (60-80 MB)
2. **Package complet** avec documentation
3. **Archive ZIP** prête à distribuer

**Aucune installation requise sur le PC client !**

---

## 🆚 Comparaison V12 vs V13

| Fonctionnalité | V12 | V13 |
|---|:---:|:---:|
| Interface | Simple | Moderne ✨ |
| Pages | 1 | 2 |
| Profils | ❌ | ✅ 10 |
| Favoris | ❌ | ✅ |
| Historique | ❌ | ✅ |
| Scanner | ❌ | ✅ |
| Animations | ❌ | ✅ |
| Thème | Basique | Premium |

---

## 🛠️ Développement

### Prérequis

```bash
pip install -r requirements.txt
```

### Lancer en mode dev

```bash
python nitrite_v13_modern.py
```

### Compiler

```bash
python build_v13.py
```

---

## 📊 Statistiques

- **715 applications** disponibles
- **25 catégories** organisées
- **553+ outils système**
- **10 profils** prédéfinis
- **3,000+ lignes** de code V13
- **100% portable** (rien installé sur PC)

---

## 🤝 Support

- **Documentation** : Voir `README_V13.md` et `DEMARRAGE_RAPIDE.md`
- **Code source** : Commenté et documenté
- **Issues** : GitHub Issues

---

## 📝 Changelog

### Version 13.0 (Actuelle)
- ✨ Interface moderne redesignée
- 📦 Navigation à 2 pages
- 🎯 10 profils prédéfinis
- ⭐ Système de favoris
- 📊 Historique intelligent
- 🔍 Scanner de système
- 🎨 Thème noir & orange premium
- 💫 Animations fluides

### Version 12.0
- Interface basique fonctionnelle
- 715 applications
- Outils système de base

---

## 🏆 Points Forts

✅ **Interface moderne** et professionnelle
✅ **715 applications** organisées
✅ **553+ outils système**
✅ **10 profils** pour gain de temps
✅ **Mode portable** sans installation
✅ **Personnalisation** avec favoris
✅ **Statistiques** en temps réel
✅ **Scanner intelligent** du système

---

## 📄 Licence

**NiTriTe V13.0** - Outil professionnel pour maintenance informatique

© 2024 OrdiPlus Tools - Tous droits réservés

---

## 🎉 Prêt à Utiliser !

```bash
# Lancer maintenant
python nitrite_v13_modern.py
```

**Bon succès avec NiTriTe V13 ! 🚀**

---

*Version 13.0 - Modern Edition*
*Développé avec ❤️ pour les techniciens de maintenance*
