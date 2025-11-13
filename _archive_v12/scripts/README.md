# 🔧 Scripts NiTrite v2.0

## 📁 Organisation des scripts

### 🛠️ Scripts principaux (racine)
- `build_executable.py` - Création de l'exécutable final
- `check_before_build.py` - Vérifications avant build
- `list_all_programs.py` - Liste tous les programmes disponibles
- `corriger_erreur_powershell.py` - Corrections PowerShell

### 🏗️ [batch/](batch/)
Scripts batch (.bat) pour automatisation
- Scripts de nettoyage
- Scripts de build
- Scripts de vérification

### 🧪 [tests/](tests/)
Scripts de test et validation
- Tests d'intégration
- Validation des corrections
- Diagnostics

### 🗄️ [database/](database/)
Scripts de gestion de base de données
- Création de la base portable
- Scan des applications
- Import/Export

### ⚙️ [utilitaires/](utilitaires/)
Scripts utilitaires et outils
- Installation des dépendances
- Lanceurs sécurisés
- Nettoyage de conflits

## 🚀 Scripts importants

### Build et déploiement
```bash
# Vérifier avant le build
python check_before_build.py

# Créer l'exécutable
python build_executable.py
```

### Développement
```bash
# Lister tous les programmes
python list_all_programs.py

# Installer les dépendances
python utilitaires/install_dependencies.py
```

---
*Scripts organisés le 9 novembre 2025*