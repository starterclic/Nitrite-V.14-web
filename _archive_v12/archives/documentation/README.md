# 🚀 NiTrite v2.7 - L'installateur Windows ultime

![Version](https://img.shields.io/badge/version-2.7-blue.svg)
![Programmes](https://img.shields.io/badge/programmes-230-green.svg)
![Catégories](https://img.shields.io/badge/catégories-38-orange.svg)
![Python](https://img.shields.io/badge/python-3.14+-brightgreen.svg)
![Winget](https://img.shields.io/badge/winget-1.11.510-blue.svg)

> L'installateur de programmes Windows le plus complet, propulsé par Winget

---

## 📋 Table des matières

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Structure du projet](#-structure-du-projet)
- [Utilisation](#-utilisation)
- [Statistiques](#-statistiques)
- [Documentation](#-documentation)
- [Licence](#-licence)

---

## 🎯 Présentation

**NiTrite** est un installateur de programmes Windows moderne et intuitif qui utilise **Winget** (le gestionnaire de paquets officiel de Microsoft) pour installer vos applications favorites en un clic.

### Pourquoi NiTrite ?

- ✅ **230 programmes** disponibles
- ✅ **38 catégories** organisées
- ✅ Interface graphique **mode sombre** élégante
- ✅ Installation **silencieuse** et automatique
- ✅ Mises à jour **automatiques** via Winget
- ✅ **Privilèges administrateur** automatiques
- ✅ Sources **officielles et vérifiées**
- ✅ **100% gratuit** et open source

---

## ✨ Fonctionnalités

### 🎨 Interface moderne
- Mode sombre élégant et confortable
- Navigation intuitive par catégories
- Recherche instantanée de programmes
- Sélection multiple
- Barre de progression en temps réel

### 🔧 Installation intelligente
- Auto-élévation des privilèges administrateur
- Installation silencieuse (sans popups)
- Gestion automatique des dépendances
- Logging détaillé des opérations
- Retry automatique en cas d'échec

### 📦 Bibliothèque massive
- **38 catégories** thématiques
- **230 programmes** vérifiés
- Drivers, runtimes, SDK
- Outils de développement
- Multimédia et gaming
- CAO et design 3D
- Bureautique et productivité

---

## 🚀 Installation

### Prérequis

- Windows 10/11
- Python 3.14 ou supérieur
- Winget installé (inclus par défaut sur Windows 11)

### Installation rapide

```powershell
# 1. Cloner ou télécharger le projet
cd "C:\Users\[VotreNom]\Documents"
git clone [URL_DU_REPO] "Projet NiTrite v.2"

# 2. Accéder au dossier
cd "Projet NiTrite v.2"

# 3. Installer les dépendances
python scripts\install_dependencies.py

# 4. Lancer NiTrite
python nitrite_winget.py
```

### Installation Winget (si nécessaire)

```powershell
# Winget est préinstallé sur Windows 11
# Pour Windows 10, installer depuis le Microsoft Store:
# "App Installer" ou visiter: https://aka.ms/getwinget
```

---

## 📁 Structure du projet

```
Projet NiTrite v.2/
├── 📂 src/                      # Code source principal
│   ├── winget_manager.py        # Gestionnaire Winget
│   ├── gui_manager_winget.py    # Interface graphique
│   ├── config_manager.py        # Configuration
│   └── __pycache__/
│
├── 📂 data/                     # Données et configuration
│   ├── programs_winget.json     # Base de données exportée
│   └── config.json              # Configuration utilisateur
│
├── 📂 docs/                     # Documentation
│   ├── README.md                # Ce fichier
│   ├── GUIDE_UTILISATEUR.md     # Guide utilisateur détaillé
│   ├── MISE_A_JOUR_V2.7_MEGA_UPDATE.md
│   ├── GUIDE_INSTALLATION_OUTILS_ORDIPLUS.md
│   └── [autres documentations]
│
├── 📂 tests/                    # Tests unitaires
│   ├── test_nitrite.py
│   ├── test_redimensionnement.py
│   └── [autres tests]
│
├── 📂 scripts/                  # Scripts utilitaires
│   ├── install_dependencies.py
│   ├── build_executable.py
│   └── [autres scripts]
│
├── 📂 logs/                     # Fichiers de logs
├── 📂 assets/                   # Ressources (icônes, images)
├── 📂 downloads/                # Téléchargements temporaires
├── 📂 dependencies/             # Dépendances externes
│
├── nitrite_winget.py            # ⭐ LANCEUR PRINCIPAL
├── Lancer_NiTrite.bat          # Lanceur Windows
└── requirements.txt             # Dépendances Python
```

---

## 🎮 Utilisation

### Lancement rapide

**Option 1 : Double-clic sur le fichier BAT**
```
Lancer_NiTrite.bat
```

**Option 2 : Ligne de commande**
```powershell
python nitrite_winget.py
```

**Option 3 : Avec auto-élévation admin**
```powershell
python nitrite_winget.py --admin
```

### Guide d'utilisation

1. **Sélectionner une catégorie**
   - Cliquez sur une catégorie dans le menu de gauche
   - Exemple: "Outils OrdiPlus", "Driver Générique", etc.

2. **Choisir vos programmes**
   - Cochez les programmes que vous souhaitez installer
   - Utilisez la barre de recherche pour filtrer

3. **Installer**
   - Cliquez sur "Installer la sélection"
   - Acceptez les privilèges administrateur si demandé
   - Attendez la fin de l'installation

4. **Profiter !**
   - Tous vos programmes sont installés et à jour
   - Lancez-les depuis le menu Démarrer

---

## 📊 Statistiques

### Évolution du projet

| Version | Programmes | Catégories | Ajouts | Date |
|---------|-----------|-----------|---------|------|
| v2.2 | 148 | 27 | Base initiale | Oct 2025 |
| v2.3 | 171 | 30 | +23 programmes | Oct 2025 |
| v2.4 | 180 | 30 | +9 programmes | Oct 2025 |
| v2.5 | 192 | 31 | +12 programmes | Nov 2025 |
| v2.6 | 207 | 32 | +15 programmes | Nov 2025 |
| **v2.7** | **230** | **38** | **+23 programmes** | **Nov 2025** |

**Croissance totale : +82 programmes (+55.4%), +11 catégories (+40.7%)**

### Répartition par catégorie

**🔧 Système & Utilitaires (10 catégories)**
- Navigateurs (6 programmes)
- Utilitaires (13 programmes)
- Sécurité (10 programmes)
- Driver Générique (17 programmes) ⭐
- Outils OrdiPlus (12 programmes) ⭐
- Et plus...

**💻 Développement (9 catégories)**
- Développement (13 programmes)
- Serveurs & Dev Web (6 programmes) ⭐ NEW
- CAO & Design 3D (4 programmes) ⭐ NEW
- Et plus...

**🎬 Multimédia (10 catégories)**
- Multimédia Avancé (5 programmes) ⭐ NEW
- Gaming Console (4 programmes)
- Streaming Vidéo (6 programmes)
- Et plus...

**💬 Communication (6 catégories)**
- Communication (8 programmes)
- Communication Sociale (3 programmes) ⭐ NEW
- Réseaux Sociaux (6 programmes)
- Et plus...

---

## 📚 Documentation

### Documentation utilisateur
- **[GUIDE_UTILISATEUR.md](docs/GUIDE_UTILISATEUR.md)** - Guide complet d'utilisation
- **[GUIDE_INSTALLATION_OUTILS_ORDIPLUS.md](docs/GUIDE_INSTALLATION_OUTILS_ORDIPLUS.md)** - Installation pack OrdiPlus

### Documentation technique
- **[MISE_A_JOUR_V2.7_MEGA_UPDATE.md](docs/MISE_A_JOUR_V2.7_MEGA_UPDATE.md)** - Notes de version 2.7
- **[MISE_A_JOUR_V2.6_DRIVERS.md](docs/MISE_A_JOUR_V2.6_DRIVERS.md)** - Notes de version 2.6
- **[RECAPITULATIF_COMPLET_V2.2_A_V2.4.md](docs/RECAPITULATIF_COMPLET_V2.2_A_V2.4.md)** - Historique complet

---

## 🔑 Fonctionnalités avancées

### Auto-élévation des privilèges

NiTrite peut automatiquement demander les privilèges administrateur :

```python
from src.winget_manager import WingetManager

# Avec auto-élévation
wm = WingetManager(auto_elevate=True)

# Sans auto-élévation (par défaut)
wm = WingetManager(auto_elevate=False)
```

### Export de la base de données

```python
from src.winget_manager import WingetManager

wm = WingetManager()
wm.export_to_json('data/programs_winget.json')
```

### Installation programmatique

```python
from src.winget_manager import WingetManager

wm = WingetManager()

# Installer un programme
success = wm.install_program(
    "Mozilla Firefox",
    wm.programs_db["Navigateurs"]["Mozilla Firefox"]
)

# Installer plusieurs programmes
programs = ["Google Chrome", "VLC Media Player", "7-Zip"]
wm.batch_install(programs)
```

---

## 🛠️ Développement

### Contribuer

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Tests

```powershell
# Lancer tous les tests
python -m pytest tests/

# Test spécifique
python tests/test_nitrite.py
```

### Build exécutable

```powershell
python scripts/build_executable.py
```

---

## 🌟 Catégories disponibles

<details>
<summary>Cliquez pour voir toutes les 38 catégories</summary>

1. Navigateurs
2. Communication
3. Multimédia
4. Développement
5. Utilitaires
6. Sécurité
7. Productivité
8. Cloud & Stockage
9. Gaming
10. Accès à distance
11. Logiciels Matériel
12. Streaming & Médias
13. Runtimes & Bibliothèques
14. Pilotes & Drivers
15. Émulateurs
16. Réseaux Sociaux
17. Streaming Vidéo
18. Streaming Audio
19. IA & Assistants
20. Utilitaires Système Avancés
21. Imprimantes & Scan
22. Services Apple
23. Logiciels Constructeur
24. Suites Professionnelles
25. Outils Système Bootables
26. Virtualisation
27. Téléchargement & Médias
28. Gaming Console
29. Benchmarks & Tests
30. IA Locale
31. Outils OrdiPlus ⭐
32. Driver Générique ⭐
33. Serveurs & Dev Web ⭐ NEW
34. Multimédia Avancé ⭐ NEW
35. CAO & Design 3D ⭐ NEW
36. Communication Sociale ⭐ NEW
37. Bureautique Alternative ⭐ NEW
38. Utilitaires Système Experts ⭐ NEW

</details>

---

## ❓ FAQ

**Q: Ai-je besoin d'un compte Microsoft ?**  
R: Non, Winget fonctionne sans compte Microsoft.

**Q: Les installations sont-elles sûres ?**  
R: Oui, toutes les applications proviennent des dépôts officiels Winget vérifiés par Microsoft.

**Q: Puis-je désinstaller les programmes installés ?**  
R: Oui, via "Ajouter ou supprimer des programmes" Windows ou via `winget uninstall`.

**Q: NiTrite fonctionne-t-il hors ligne ?**  
R: Non, une connexion Internet est nécessaire pour télécharger les programmes.

**Q: Comment mettre à jour les programmes ?**  
R: Utilisez `winget upgrade --all` ou réinstallez via NiTrite.

---

## 🔄 Mises à jour

Pour mettre à jour NiTrite :

```powershell
git pull origin main
python scripts/install_dependencies.py
```

---

## 📞 Support

- **Issues GitHub** : [Créer une issue](#)
- **Documentation** : Dossier `docs/`
- **Email** : [support@nitrite.com](#)

---

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 🙏 Remerciements

- **Microsoft** pour Winget
- **Communauté Python** pour les bibliothèques utilisées
- **Tous les contributeurs** du projet

---

## 🎊 Changelog

### v2.7 - MEGA UPDATE (3 novembre 2025)
- ✨ +23 nouveaux programmes
- 🆕 +6 nouvelles catégories
- ⚡ Auto-élévation des privilèges administrateur
- 📁 Réorganisation complète du projet
- 🎬 Multimédia Avancé (Jellyfin, Kodi, MPV)
- 💻 Serveurs & Dev Web (XAMPP, Arduino, Godot)
- 📐 CAO & Design 3D (LibreCAD, FreeCAD, SketchUp)

### v2.6 - Driver Générique (3 novembre 2025)
- ✨ +15 drivers et runtimes
- 🆕 Catégorie Driver Générique
- 📦 Visual C++, .NET, DirectX, Java, Windows SDK

### v2.5 - Outils OrdiPlus (3 novembre 2025)
- ✨ +12 programmes essentiels
- 🆕 Catégorie Outils OrdiPlus
- 🔧 Pack complet pour maintenance PC

---

<div align="center">

**Fait avec ❤️ pour la communauté Windows**

[⬆ Retour en haut](#-nitrite-v27---linstallateur-windows-ultime)

</div>
