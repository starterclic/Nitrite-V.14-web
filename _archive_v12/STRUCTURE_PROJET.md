# 📁 Structure du Projet NiTriTe V12.0

## 🎯 Organisation Générale

```
nitrite-v5.0/
├── 📂 src/                           # Code source principal
│   ├── gui_manager.py                # Interface graphique V12.0
│   ├── installer_manager.py          # Gestion installations
│   ├── config_manager.py             # Configuration
│   ├── elevation_helper.py           # Élévation admin
│   ├── dependency_manager.py         # Dépendances
│   ├── cleanup_manager.py            # Nettoyage
│   └── url_updater.py                # Mise à jour URLs
│
├── 📂 data/                          # Données de l'application
│   ├── programs.json                 # 715 applications (25 catégories)
│   └── config.json                   # Configuration utilisateur
│
├── 📂 scripts/                       # Scripts utilitaires
│   ├── NiTrite_v12_Final.spec        # Config PyInstaller
│   ├── create_icon.py                # Générateur d'icône V12
│   ├── validate_programs.py          # Validation programs.json
│   ├── generate_500plus_apps.py      # Générateur d'applications
│   ├── add_massive_applications.py   # Ajout massif
│   ├── build_executable.py           # Build alternatif
│   ├── check_before_build.py         # Vérifications pré-build
│   ├── list_all_programs.py          # Liste programmes
│   ├── show_project_structure.py     # Affiche structure
│   ├── 📂 lanceurs/                  # Scripts de lancement
│   ├── 📂 tests/                     # Tests unitaires
│   ├── 📂 utilitaires/               # Outils divers
│   ├── 📂 batch/                     # Scripts batch
│   └── 📂 database/                  # Base de données portables
│
├── 📂 assets/                        # Ressources visuelles
│   ├── icon.ico                      # Icône principale V12 (multi-résolutions)
│   └── icon_nitrite_v12.png          # Icône PNG haute qualité
│
├── 📂 docs/                          # Documentation complète
│   ├── README.md                     # Guide principal
│   ├── GUIDE_UTILISATION.md          # Guide utilisateur
│   ├── QUICK_START.md                # Démarrage rapide
│   ├── 📂 guides/                    # Guides détaillés
│   ├── 📂 historique/                # Historique versions
│   ├── 📂 developpeur/               # Doc développeur
│   └── 📂 archives/                  # Archives documentation
│       └── RÉSUMÉ_FINAL.txt          # Résumé sessions
│
├── 📂 archives/                      # Archives anciennes versions
│   ├── 📂 anciennes_versions/        # Versions précédentes
│   ├── 📂 anciens_scripts/           # Scripts obsolètes
│   ├── 📂 documentation/             # Ancienne doc
│   ├── 📂 documentation_dev/         # Ancienne doc dev
│   └── 📂 scripts_dev/               # Scripts dev archivés
│
├── 📂 .github/                       # Configuration GitHub
│   └── DESCRIPTION.md                # Description du dépôt
│
├── 📄 nitrite_complet.py             # Lanceur principal
├── 📄 LANCER.bat                     # Lanceur Windows
├── 📄 build_nitrite_v12_final.py     # Script de build portable V12.0
├── 📄 requirements.txt               # Dépendances Python
├── 📄 README.md                      # README principal du projet
├── 📄 STRUCTURE_PROJET.md            # Ce fichier
└── 📄 .gitignore                     # Exclusions Git

📦 Après build (non versionné) :
├── 📂 NiTriTe V12 Portable/          # Dossier application portable
│   ├── NiTriTe V12.0.exe             # Exécutable autonome
│   ├── Lancer NiTriTe.bat            # Lanceur rapide
│   └── README.txt                    # Instructions
└── 📦 NiTriTe V12 Portable.zip       # Archive pour distribution

```

## 📊 Statistiques du Projet

### Applications et Outils
- **715 applications** réparties en **25 catégories**
- **553 outils système** organisés en **18 sections**

### Catégories d'Applications
1. Outils OrdiPlus (10)
2. Pack Office (10)
3. Navigateurs (31)
4. Antivirus (30)
5. Sécurité (29)
6. Bureautique (31)
7. Multimédia (31)
8. Développement (30)
9. Utilitaires (30)
10. Communication (30)
11. Jeux (30)
12. Désinstallateurs Antivirus (30)
13. Internet (30)
14. Réseaux Sociaux (30)
15. Streaming Vidéo (30)
16. Streaming Audio (30)
17. IA & Assistants (31)
18. Utilitaires Système (31)
19. Imprimantes & Scan (30)
20. Services Apple (30)
21. Suites Professionnelles (30)
22. Productivité (30)
23. Stockage Cloud (31)
24. PDF et Documents (30)
25. Compression (30)

### Sections d'Outils Système
1. Activation & Téléchargements (32 boutons)
2. Réparation Système (31 boutons)
3. Maintenance & Nettoyage (16 boutons)
4. Diagnostics & Infos (56 boutons)
5. Réseau & Internet (22 boutons)
6. Winget - Package Manager (12 boutons)
7. Paramètres Windows (19 boutons)
8. Support Constructeurs (18 boutons)
9. Fournisseurs & Achats (47 boutons)
10. Sécurité & Confidentialité (48 boutons)
11. Benchmark & Tests (35 boutons)
12. Utilitaires Système (39 boutons)
13. Multimédia & Création (48 boutons)
14. Bureautique & Productivité (42 boutons)
15. Développement Web (45 boutons)
16. Dépannage à Distance (14 boutons)
17. Drivers & Pilotes (14 boutons)
18. Documentation & Aide (15 boutons)

## 🔧 Fichiers de Configuration

### `.gitignore`
Exclut les dossiers de build, cache Python, fichiers logs, etc.

### `requirements.txt`
Liste toutes les dépendances Python nécessaires.

### `data/config.json`
Configuration utilisateur (préférences, ordre des sections, etc.)

## 🚀 Points d'Entrée

1. **`nitrite_complet.py`** : Lanceur Python principal
2. **`LANCER.bat`** : Lanceur Windows (double-clic)
3. **`build_nitrite_v12_final.py`** : Script de build pour créer la version portable autonome

## 📝 Documentation

- **README.md** : Documentation principale complète
- **docs/** : Documentation détaillée pour utilisateurs et développeurs
- **STRUCTURE_PROJET.md** : Ce fichier (organisation du projet)
- **.github/DESCRIPTION.md** : Description pour GitHub

## 🎨 Ressources Visuelles

### Icône V12.0
- **Format** : ICO + PNG
- **Design** : Fond noir arrondi, bordure orange, titre "NiTriTe" + "V12" avec opacité
- **Résolutions ICO** : 256, 128, 64, 48, 32, 16 pixels
- **Générateur** : `scripts/create_icon.py`

## 🔄 Workflow de Développement

1. **Développement** : Modifier les fichiers dans `src/`
2. **Test** : Lancer via `nitrite_complet.py` ou `LANCER.bat`
3. **Validation** : Exécuter `scripts/validate_programs.py`
4. **Build** : Utiliser `build_nitrite_v12_final.py` (à la racine)
5. **Distribution** : Le dossier `NiTriTe V12 Portable/` et le ZIP sont créés automatiquement

## 📦 Gestion des Versions

### Version Actuelle : V12.0
- Interface moderne avec titre multicolore
- 715 applications + 553 outils
- Icône personnalisée
- Optimisations visuelles

### Archives
Toutes les anciennes versions et documentations sont archivées dans le dossier `archives/`.

---

**Dernière mise à jour** : 10 novembre 2025
**Version** : NiTriTe V12.0
