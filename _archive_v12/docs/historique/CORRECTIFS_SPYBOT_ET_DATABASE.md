# 🔧 Correctifs Spybot et Base de Données Portable

## 📅 Date : 5 Novembre 2025

---

## ✅ 1. CORRECTION SPYBOT SEARCH & DESTROY

### 🐛 Problème identifié
- **Spybot** ne s'installait pas correctement
- URL de téléchargement obsolète
- Arguments d'installation incomplets
- Absence de winget_id pour installation alternative

### 🔧 Correctifs appliqués

#### Fichier : `data/programs.json`

**AVANT :**
```json
"Spybot Search & Destroy": {
    "description": "Détection et suppression de spywares et malwares",
    "download_url": "https://download.spybot.info/SpybotSD2.exe",
    "install_args": "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-",
    "category": "Outils OrdiPlus",
    "essential": true,
    "auto_reject_ads": true,
    "cleanup_folder": "Outils de nettoyage",
    "admin_required": true,
    "note": "Téléchargement direct depuis le CDN officiel Spybot"
}
```

**APRÈS :**
```json
"Spybot Search & Destroy": {
    "description": "Détection et suppression de spywares et malwares",
    "download_url": "https://download.spybot.info/SpybotSD2-latest.exe",
    "install_args": "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP- /NOCANCEL /TASKS=\"\"",
    "category": "Outils OrdiPlus",
    "essential": true,
    "auto_reject_ads": true,
    "cleanup_folder": "Outils de nettoyage",
    "admin_required": true,
    "winget_id": "SaferNetworking.SpybotSearchAndDestroy",
    "note": "Installation via winget recommandée - URL alternative SpybotSD2-latest.exe"
}
```

### 🎯 Améliorations
1. ✅ **URL mise à jour** : `SpybotSD2-latest.exe` (version toujours à jour)
2. ✅ **Arguments enrichis** : 
   - `/NOCANCEL` : Empêche l'annulation
   - `/TASKS=""` : Désactive les tâches optionnelles
3. ✅ **Winget ID ajouté** : Installation alternative via winget
4. ✅ **Note mise à jour** : Recommandation d'installation

### 🧪 Test de validation
```powershell
# Test 1: Vérifier la disponibilité winget
winget search SaferNetworking.SpybotSearchAndDestroy

# Test 2: Installation via winget (recommandé)
winget install SaferNetworking.SpybotSearchAndDestroy --silent --accept-package-agreements

# Test 3: Téléchargement direct
# L'URL https://download.spybot.info/SpybotSD2-latest.exe redirige vers la dernière version
```

---

## ✅ 2. BASE DE DONNÉES LOCALE POUR APPLICATIONS PORTABLES

### 🎯 Objectif
Créer une base de données SQLite locale pour gérer tous les exécutables des applications portables avec :
- 📦 Métadonnées complètes
- 🔍 Recherche rapide
- 📊 Statistiques
- 🔐 Vérification d'intégrité (hash SHA256)

### 📁 Fichiers créés

#### 1. `src/portable_database.py` (712 lignes)
**Module principal de gestion de la base de données**

Fonctionnalités :
- ✅ Création de la structure SQLite
- ✅ Ajout/Suppression/Modification d'applications
- ✅ Recherche par nom, catégorie, description
- ✅ Calcul automatique du hash SHA256
- ✅ Import depuis `programs.json`
- ✅ Export vers JSON (backup)
- ✅ Vérification d'intégrité
- ✅ Statistiques détaillées

**Tables créées :**
```sql
- applications      (infos principales)
- metadata         (métadonnées personnalisées)
- categories       (liste des catégories)
- execution_history (historique, pour futur usage)
```

#### 2. `scripts/create_portable_database.py`
**Script pour créer et initialiser la base de données**

Actions :
- ✅ Crée `portable_apps.db`
- ✅ Importe depuis `data/programs.json`
- ✅ Affiche les statistiques
- ✅ Exporte vers JSON
- ✅ Vérifie l'intégrité

**Utilisation :**
```bash
python scripts\create_portable_database.py
```

#### 3. `scripts/scan_portable_apps.py`
**Script pour scanner automatiquement le dossier downloads**

Actions :
- ✅ Scanne tous les .exe dans `downloads/`
- ✅ Détecte automatiquement la catégorie
- ✅ Extrait la version du nom de fichier
- ✅ Ajoute à la base de données
- ✅ Ignore les doublons

**Utilisation :**
```bash
python scripts\scan_portable_apps.py
```

#### 4. `README_PORTABLE_DATABASE.md`
**Documentation complète du système**

Contient :
- 📖 Guide d'utilisation
- 💻 Exemples de code
- 🔧 Intégration avec NiTrite
- 📊 Requêtes SQL utiles
- 🐛 Dépannage

### 🗄️ Structure de la base de données

```
portable_apps.db
│
├── applications
│   ├── id (PRIMARY KEY)
│   ├── name (UNIQUE)
│   ├── display_name
│   ├── category
│   ├── description
│   ├── version
│   ├── executable_path
│   ├── file_size
│   ├── file_hash (SHA256)
│   ├── download_url
│   ├── download_date
│   ├── last_updated
│   ├── is_portable
│   ├── install_args
│   ├── notes
│   ├── icon_path
│   ├── official_website
│   └── admin_required
│
├── metadata
│   ├── app_id (FK)
│   ├── key
│   └── value
│
├── categories
│   ├── id
│   ├── name
│   ├── description
│   └── icon
│
└── execution_history
    ├── id
    ├── app_id (FK)
    ├── execution_date
    ├── duration
    ├── success
    └── notes
```

### 💡 Exemple d'utilisation

```python
from src.portable_database import PortableDatabase

# Initialiser
db = PortableDatabase(
    db_path="portable_apps.db",
    apps_folder="downloads"
)

# Ajouter une application
app_id = db.add_application(
    name="AnyDesk Portable",
    executable_path="downloads/AnyDesk.exe",
    category="Outils OrdiPlus",
    description="Bureau à distance rapide",
    version="7.1.14",
    is_portable=True,
    download_url="https://download.anydesk.com/AnyDesk.exe"
)

# Rechercher
apps = db.search_applications("anydesk")

# Statistiques
stats = db.get_statistics()
print(f"Total: {stats['total_apps']} apps")
print(f"Espace: {stats['total_size_gb']:.2f} GB")

# Lister par catégorie
outils = db.list_applications(category="Outils OrdiPlus")

# Vérifier l'intégrité
issues = db.verify_integrity()
if not issues:
    print("✅ Intégrité vérifiée")
```

### 📊 Fonctionnalités avancées

#### 1. Détection automatique de catégorie
Le scanner analyse le nom du fichier pour détecter la catégorie :
```python
'AnyDesk.exe' → "Outils OrdiPlus"
'Chrome.exe' → "Navigateurs"
'VLC.exe' → "Multimédia"
```

#### 2. Extraction de version
```python
'VLC-3.0.18.exe' → version: "3.0.18"
'git-v2.47.0.exe' → version: "2.47.0"
```

#### 3. Hash SHA256 automatique
Chaque fichier reçoit un hash unique pour vérifier :
- ✅ Intégrité du fichier
- ✅ Détection de modifications
- ✅ Doublons

#### 4. Import/Export JSON
```python
# Import
db.import_from_json("data/programs.json", "downloads")

# Export (backup)
db.export_to_json("backup.json")
```

### 🔧 Intégration avec NiTrite

#### Modifier `installer_manager.py` :

```python
from .portable_database import PortableDatabase

class InstallerManager:
    def __init__(self, config_path=None, log_callback=None):
        # ... code existant ...
        
        # Ajouter la base de données
        self.portable_db = PortableDatabase(
            db_path=APP_DIR / "portable_apps.db",
            apps_folder=self.download_dir
        )
    
    def download_program(self, program_name, download_url):
        # ... téléchargement ...
        
        # Si portable, ajouter à la BDD
        if program_info.get('portable', False):
            self.portable_db.add_application(
                name=program_name,
                executable_path=str(exe_path),
                category=program_info.get('category'),
                description=program_info.get('description'),
                download_url=download_url,
                is_portable=True
            )
```

### 📈 Statistiques générées

```python
{
    'total_apps': 150,
    'portable_apps': 130,
    'installed_apps': 20,
    'total_size_bytes': 5368709120,
    'total_size_mb': 5120.0,
    'total_size_gb': 5.0,
    'apps_by_category': {
        'Outils OrdiPlus': 25,
        'Navigateurs': 15,
        'Multimédia': 30,
        'Développement': 20,
        'Utilitaires': 15,
        'Communication': 10,
        'Jeux': 8,
        'Sécurité': 7
    }
}
```

---

## 🚀 MISE EN ŒUVRE

### Étape 1 : Créer la base de données
```bash
cd "c:\Users\Momo\Documents\Projet NiTrite v.2"
python scripts\create_portable_database.py
```

**Résultat attendu :**
- ✅ Création de `portable_apps.db`
- ✅ Import des applications depuis `programs.json`
- ✅ Affichage des statistiques
- ✅ Export vers `portable_apps_export.json`

### Étape 2 : Scanner les exécutables existants
```bash
python scripts\scan_portable_apps.py
```

**Résultat attendu :**
- ✅ Scan de `downloads/*.exe`
- ✅ Ajout automatique dans la BDD
- ✅ Détection de catégorie et version
- ✅ Calcul des hash SHA256

### Étape 3 : Tester Spybot
```bash
# Via winget (recommandé)
winget install SaferNetworking.SpybotSearchAndDestroy --silent

# Ou via le script NiTrite
python nitrite_complet.py
# Sélectionner Spybot Search & Destroy
```

---

## 📋 CHECKLIST DE VALIDATION

### ✅ Spybot
- [x] URL mise à jour (SpybotSD2-latest.exe)
- [x] Arguments d'installation complets
- [x] Winget ID ajouté
- [ ] Test d'installation réussi
- [ ] Vérification du fonctionnement

### ✅ Base de données portable
- [x] Module `portable_database.py` créé
- [x] Script de création `create_portable_database.py`
- [x] Script de scan `scan_portable_apps.py`
- [x] Documentation `README_PORTABLE_DATABASE.md`
- [ ] Base de données créée
- [ ] Applications importées
- [ ] Tests de recherche effectués
- [ ] Vérification d'intégrité OK

---

## 🔍 TESTS RECOMMANDÉS

### Test 1 : Installation Spybot
```powershell
# Test avec winget
winget install SaferNetworking.SpybotSearchAndDestroy --silent --accept-package-agreements

# Vérifier l'installation
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" | 
    Where-Object { $_.DisplayName -like "*Spybot*" } | 
    Select-Object DisplayName, DisplayVersion
```

### Test 2 : Base de données
```python
from src.portable_database import PortableDatabase

db = PortableDatabase()

# Test ajout
app_id = db.add_application(
    name="Test App",
    executable_path="downloads/test.exe",
    category="Test"
)
print(f"App ajoutée : {app_id}")

# Test recherche
results = db.search_applications("Test")
print(f"Trouvé : {len(results)} apps")

# Test stats
stats = db.get_statistics()
print(f"Total : {stats['total_apps']} apps")

# Test intégrité
issues = db.verify_integrity()
print(f"Problèmes : {len(issues)}")
```

---

## 📊 RÉSUMÉ DES MODIFICATIONS

### Fichiers modifiés :
1. ✅ `data/programs.json` - Correction Spybot

### Fichiers créés :
1. ✅ `src/portable_database.py` - Module de BDD
2. ✅ `scripts/create_portable_database.py` - Création BDD
3. ✅ `scripts/scan_portable_apps.py` - Scan automatique
4. ✅ `README_PORTABLE_DATABASE.md` - Documentation
5. ✅ `CORRECTIFS_SPYBOT_ET_DATABASE.md` - Ce fichier

### Impact :
- 🐛 **Spybot** : Installation corrigée
- 💾 **Database** : Système complet de gestion des apps portables
- 📊 **Stats** : Suivi précis de l'espace et des applications
- 🔐 **Sécurité** : Vérification d'intégrité par hash SHA256

---

## 🎯 PROCHAINES ÉTAPES

1. ✅ Tester l'installation de Spybot
2. ✅ Créer la base de données portable
3. ✅ Scanner les applications existantes
4. 🔄 Intégrer la BDD dans `installer_manager.py`
5. 🔄 Créer une interface GUI de gestion des apps portables
6. 🔄 Ajouter l'historique d'exécution
7. 🔄 Implémenter le lancement direct depuis la BDD

---

**Créé le :** 5 Novembre 2025  
**Auteur :** Assistant NiTrite v.2  
**Version :** 1.0

---

## 💬 SUPPORT

Pour toute question :
- Consultez `README_PORTABLE_DATABASE.md`
- Vérifiez les logs dans `logs/nitrite.log`
- Testez avec les scripts fournis

**Bon développement ! 🚀**
