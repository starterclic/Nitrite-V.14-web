# 🚀 Guide d'Utilisation - NiTrite v2.0

## Table des matières
- [Installation](#installation)
- [Lancement de l'application](#lancement)
- [Utilisation](#utilisation)
- [Dépannage](#dépannage)
- [Scripts disponibles](#scripts-disponibles)

---

## 📋 Prérequis

- **Windows 10** ou **Windows 11**
- **Python 3.8+** (recommandé: Python 3.11)
- **4 GB RAM** minimum
- **Connexion Internet** pour télécharger les programmes

---

## 🔧 Installation

### Option 1: Installation complète (recommandée)

1. **Cloner ou télécharger le projet**
   ```bash
   git clone https://github.com/heiphaistos44-crypto/nitrite-v2-portable.git
   cd nitrite-v2-portable
   ```

2. **Lancer avec le script automatique**
   ```bash
   # Windows
   LANCER_NITRITE.bat

   # Ou avec Python directement
   python lancer_nitrite.py
   ```

   Le script va automatiquement:
   - Vérifier la version de Python
   - Installer les dépendances manquantes
   - Lancer l'application

### Option 2: Installation manuelle des dépendances

```bash
pip install -r requirements.txt
python nitrite_complet.py
```

### Option 3: Version portable (sans vérification)

```bash
# Windows
LANCER_PORTABLE.bat

# Ou avec Python
python lancer_portable.py
```

---

## 🚀 Lancement

### Méthode 1: Double-clic (Windows)
- Double-cliquez sur `LANCER_NITRITE.bat`

### Méthode 2: Ligne de commande
```bash
python lancer_nitrite.py
```

### Méthode 3: Mode portable
```bash
python lancer_portable.py
```

### Méthode 4: Version compilée (.exe)
Si vous avez compilé l'application:
```bash
cd NiTrite_Autonome
LANCER_NITRITE.bat
```

---

## 📱 Utilisation de l'Interface

### 1. Fenêtre Principale

L'interface affiche les programmes organisés par catégories:
- 🔧 Outils OrdiPlus
- 📦 Pack Office
- 🌐 Navigateurs
- 📖 Lecteurs
- 🛠️ Utilitaires
- 🎨 Multimédia
- 💻 Développement
- 💬 Communication

### 2. Sélection des Programmes

- **Cochez** les cases des programmes que vous souhaitez installer
- Vous pouvez sélectionner plusieurs programmes
- Les catégories peuvent être réduites/développées

### 3. Installation

1. Cliquez sur le bouton **"Installer les programmes sélectionnés"**
2. L'application va:
   - Télécharger les programmes
   - Les installer automatiquement
   - Gérer les privilèges administrateur
   - Afficher la progression en temps réel

### 4. Barre de Progression

- Affiche le programme en cours d'installation
- Pourcentage de progression
- Statut (téléchargement, installation, terminé)

---

## 🔍 Fonctionnalités Avancées

### Installation via WinGet

Si un téléchargement direct échoue, NiTrite utilise automatiquement **WinGet** (gestionnaire de paquets Windows) comme méthode alternative.

### Applications Portables

Certains programmes sont marqués comme "portables":
- Ils seront copiés dans un dossier sur votre Bureau
- Aucune installation système requise
- Peuvent être déplacés sur une clé USB

### Base de Données Locale

NiTrite maintient une base de données SQLite des programmes installés:
- Localisation: `portable_apps.db`
- Contient: chemins, versions, hashes SHA256
- Permet la vérification d'intégrité

---

## ⚙️ Scripts Disponibles

### Scripts de Lancement

| Script | Description | Usage |
|--------|-------------|-------|
| `LANCER_NITRITE.bat` | Lance avec vérification des dépendances (Windows) | Double-clic |
| `LANCER_PORTABLE.bat` | Lance en mode portable (Windows) | Double-clic |
| `lancer_nitrite.py` | Lance avec vérification des dépendances (Python) | `python lancer_nitrite.py` |
| `lancer_portable.py` | Lance en mode portable (Python) | `python lancer_portable.py` |

### Scripts de Build

| Script | Description | Usage |
|--------|-------------|-------|
| `build_exe.py` | Compile l'application en .exe | `python build_exe.py` |
| `scripts/batch/BUILD_AUTONOME.bat` | Build via batch (Windows) | Double-clic |

### Scripts de Tests

| Script | Description | Usage |
|--------|-------------|-------|
| `run_tests.py` | Lance tous les tests unitaires | `python run_tests.py` |
| `tests/test_core_functionality.py` | Tests des fonctionnalités de base | `python -m unittest` |

### Scripts Utilitaires

| Script | Description | Usage |
|--------|-------------|-------|
| `scripts/batch/NETTOYER_PROJET.bat` | Nettoie le projet | Double-clic |
| `scripts/batch/VOIR_STRUCTURE.bat` | Affiche la structure | Double-clic |

---

## 🐛 Dépannage

### Problème: Python n'est pas reconnu

**Solution:**
1. Téléchargez Python depuis https://www.python.org/downloads/
2. Lors de l'installation, **cochez "Add Python to PATH"**
3. Redémarrez votre terminal

### Problème: Erreur d'import de module

**Solution:**
```bash
pip install -r requirements.txt
```

### Problème: Privilèges administrateur requis

**Solution:**
- Faites un clic droit sur le script
- Sélectionnez "Exécuter en tant qu'administrateur"

### Problème: WinGet n'est pas installé

**Solution:**
WinGet est installé automatiquement. Si le problème persiste:
1. Ouvrez le Microsoft Store
2. Recherchez "App Installer"
3. Installez/Mettez à jour

### Problème: Échec de téléchargement

**Solutions:**
- Vérifiez votre connexion Internet
- Désactivez temporairement votre antivirus
- Essayez avec un autre navigateur/réseau

### Problème: Interface ne s'affiche pas

**Solution:**
```bash
pip install --upgrade Pillow tkinter
```

---

## 📊 Logs et Débogage

### Localisation des Logs

Les logs sont enregistrés dans:
```
logs/nitrite.log
```

### Niveaux de Log

- **INFO**: Opérations normales
- **WARNING**: Avertissements (non bloquants)
- **ERROR**: Erreurs (opération échouée)
- **CRITICAL**: Erreurs critiques (application arrêtée)

### Activer le Mode Débogage

Modifiez `data/config.json`:
```json
{
    "log_level": "DEBUG"
}
```

---

## 🔐 Sécurité

### Vérification d'Intégrité

NiTrite vérifie automatiquement:
- Les hash SHA256 des fichiers téléchargés
- Les signatures numériques (si disponibles)
- L'origine des téléchargements

### Privilèges Administrateur

Certains programmes nécessitent des privilèges admin:
- L'élévation est demandée automatiquement
- Vous pouvez accepter ou refuser
- Les installations sans privilèges sont tentées en premier

---

## 📞 Support

### Rapporter un Bug

1. Ouvrez une issue sur GitHub
2. Incluez:
   - Version de Windows
   - Version de Python
   - Le fichier `logs/nitrite.log`
   - Description détaillée du problème

### Demander une Fonctionnalité

Ouvrez une issue avec le tag `enhancement`

---

## 📄 Licence

© 2025 NiTrite OrdiPlus - Installation simplifiée Windows

---

## 🎯 Conseils d'Utilisation

1. **Première utilisation**: Utilisez `LANCER_NITRITE.bat` pour installer les dépendances
2. **Utilisations suivantes**: Utilisez `LANCER_PORTABLE.bat` pour un lancement plus rapide
3. **Sauvegardez** votre sélection de programmes favoris
4. **Vérifiez** régulièrement les mises à jour de l'application
5. **Testez** les installations dans un environnement de test avant production

---

## 🚀 Compilation en Exécutable

Pour créer une version standalone (.exe):

```bash
python build_exe.py
```

Le fichier sera généré dans: `NiTrite_Autonome/NiTrite_OrdiPlus_v2.exe`

**Avantages:**
- ✅ Aucune dépendance Python requise
- ✅ ~27 MB (tout inclus)
- ✅ Fonctionne sur n'importe quel PC Windows
- ✅ Parfait pour distribution

---

**Bon usage de NiTrite ! 🎉**
