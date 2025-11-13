# 🔨 Guide de Build - Windows

## ⚠️ Important

Le build de **NiTriTe V13** doit être effectué **sur Windows** car c'est une application Windows utilisant :
- **tkinter** (interface graphique Windows)
- **win32** API (privilèges administrateur)
- **Chemins Windows** (C:\, etc.)

---

## 📋 Prérequis Windows

### 1. Python 3.8+

Télécharger depuis : https://www.python.org/downloads/

**Important** : Cocher "Add Python to PATH" lors de l'installation

### 2. Vérifier l'installation

```cmd
python --version
```

Devrait afficher : `Python 3.x.x`

---

## 🚀 Méthode 1 : Script Automatique (Recommandé)

### Étape 1 : Préparer l'environnement

```cmd
# Se placer dans le dossier du projet
cd Nitrite-V.13-Beta-Portable-

# Installer les dépendances
pip install -r requirements.txt
```

### Étape 2 : Lancer le build

```cmd
python build_v13.py
```

Le script va automatiquement :
1. ✅ Vérifier les dépendances
2. ✅ Nettoyer les anciens builds
3. ✅ Créer le fichier .spec
4. ✅ Compiler l'exécutable
5. ✅ Créer le package portable
6. ✅ Créer l'archive ZIP

### Étape 3 : Récupérer le résultat

Le build se trouve dans :
```
dist/
├── NiTriTe_V13_Modern.exe         # Exécutable standalone
└── NiTriTe_V13_Portable_YYYYMMDD/  # Package complet
    ├── NiTriTe_V13_Modern.exe
    ├── README.txt
    └── README_V13.md
```

Archive ZIP :
```
dist/NiTriTe_V13_Portable_YYYYMMDD.zip
```

---

## 🛠️ Méthode 2 : Build Manuel

Si le script automatique ne fonctionne pas, utilisez cette méthode.

### Étape 1 : Installer PyInstaller

```cmd
pip install pyinstaller
```

### Étape 2 : Créer le fichier .spec

Créer `NiTriTe_V13.spec` :

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['nitrite_v13_modern.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data', 'data'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'PIL',
        'PIL._tkinter_finder',
        'requests',
        'urllib3',
        'certifi',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NiTriTe_V13_Modern',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)
```

### Étape 3 : Compiler

```cmd
pyinstaller --clean NiTriTe_V13.spec
```

### Étape 4 : Tester l'exécutable

```cmd
dist\NiTriTe_V13_Modern.exe
```

---

## 📦 Méthode 3 : Build avec Options

### Options PyInstaller Utiles

```cmd
# Build avec console (debug)
pyinstaller --clean --console NiTriTe_V13.spec

# Build sans UPX (plus rapide, plus gros)
pyinstaller --clean --noupx NiTriTe_V13.spec

# Build un seul fichier (plus lent au démarrage)
pyinstaller --clean --onefile nitrite_v13_modern.py

# Build avec icône personnalisée
pyinstaller --clean --icon=assets/icon.ico nitrite_v13_modern.py
```

---

## 🔍 Dépannage

### Problème : "PyInstaller n'est pas reconnu"

```cmd
# Réinstaller avec pip
pip install --upgrade pyinstaller

# Ou utiliser python -m
python -m PyInstaller --clean NiTriTe_V13.spec
```

### Problème : "Module 'tkinter' not found"

Tkinter est inclus avec Python Windows par défaut. Si absent :

1. Réinstaller Python en cochant "tcl/tk and IDLE"
2. Ou installer depuis : https://www.python.org/downloads/

### Problème : "Module 'PIL' not found"

```cmd
pip install Pillow
```

### Problème : "Module 'requests' not found"

```cmd
pip install requests
```

### Problème : Build très lent

Le premier build prend 2-5 minutes (normal).
Les builds suivants sont plus rapides grâce au cache.

Pour nettoyer le cache :
```cmd
rmdir /s /q build dist __pycache__
del NiTriTe_V13.spec
```

### Problème : Antivirus bloque l'exécutable

Certains antivirus bloquent les .exe créés par PyInstaller (faux positif).

**Solutions** :
1. Ajouter une exception dans l'antivirus
2. Désactiver temporairement l'antivirus
3. Soumettre l'exe à VirusTotal pour analyse

### Problème : Erreur "Access Denied"

Exécuter l'invite de commandes en **Administrateur** :

1. Chercher "cmd" dans le menu Démarrer
2. Clic droit → "Exécuter en tant qu'administrateur"
3. Relancer le build

---

## 📊 Taille du Build

### Exécutable
- **Taille non compressée** : ~60-80 MB
- **Taille compressée (ZIP)** : ~25-35 MB

### Pourquoi si gros ?

L'exécutable inclut :
- Python runtime
- Tkinter + tcl/tk
- PIL (Pillow)
- requests, urllib3, certifi
- Tous les modules de l'application

### Réduire la taille

```cmd
# Utiliser UPX (compression)
pyinstaller --clean --upx-dir=/path/to/upx NiTriTe_V13.spec

# Télécharger UPX : https://upx.github.io/
```

---

## ✅ Vérification du Build

### Tests à effectuer

1. **Lancement** : Double-clic sur .exe
2. **Interface** : Vérifier affichage correct
3. **Recherche** : Taper dans barre de recherche
4. **Navigation** : Basculer entre pages
5. **Sélection** : Cocher quelques apps
6. **Web** : Cliquer sur boutons 🌐
7. **Outils** : Tester quelques outils système

### Si ça fonctionne

✅ Le build est réussi !

Vous pouvez distribuer :
- `dist/NiTriTe_V13_Modern.exe`
- Ou `dist/NiTriTe_V13_Portable_YYYYMMDD.zip`

---

## 📋 Checklist Complète

Avant de distribuer, vérifier :

- [ ] Build compile sans erreur
- [ ] Exécutable lance correctement
- [ ] Interface s'affiche en 1400x900
- [ ] Navigation entre pages fonctionne
- [ ] Recherche filtre correctement
- [ ] Boutons web ouvrent les sites
- [ ] Sélection d'apps fonctionne
- [ ] Pas d'erreur dans les logs
- [ ] Taille raisonnable (<100 MB)
- [ ] Antivirus ne bloque pas
- [ ] Testé sur PC propre
- [ ] Documentation incluse

---

## 🎯 Build pour Distribution

### Créer un Package Complet

```
NiTriTe_V13_Portable_YYYYMMDD/
├── NiTriTe_V13_Modern.exe      # Exécutable principal
├── README.txt                  # Instructions rapides
├── README_V13.md               # Documentation complète
└── LANCER_V13.bat              # Lanceur (optionnel)
```

### Créer le ZIP

```cmd
# Avec 7-Zip (recommandé)
7z a -tzip NiTriTe_V13_Portable.zip NiTriTe_V13_Portable_YYYYMMDD\*

# Ou avec PowerShell
Compress-Archive -Path dist\NiTriTe_V13_Portable_YYYYMMDD -DestinationPath NiTriTe_V13_Portable.zip
```

---

## 📝 Notes Importantes

### Mode Portable

L'application est **100% portable** :
- ✅ Aucune installation sur le PC
- ✅ Aucun fichier laissé sur le disque
- ✅ Tous les téléchargements dans Temp
- ✅ Configuration dans dossier utilisateur

### Privilèges Admin

L'application demande automatiquement les droits admin si nécessaire :
- UAC prompt au premier lancement
- Nécessaire pour installer les applications

### Compatibilité

- ✅ Windows 10 (64-bit)
- ✅ Windows 11 (64-bit)
- ❌ Windows 7/8 (non testé)
- ❌ Linux/Mac (non supporté)

---

## 🚀 Résumé Ultra-Rapide

```cmd
# 1. Installer dépendances
pip install -r requirements.txt

# 2. Builder
python build_v13.py

# 3. Tester
dist\NiTriTe_V13_Modern.exe

# 4. Distribuer
# → dist/NiTriTe_V13_Portable_YYYYMMDD.zip
```

---

## 📞 Support

Si problèmes persistants :
1. Vérifier version Python (3.8+)
2. Vérifier dépendances installées
3. Nettoyer cache (`rmdir build dist`)
4. Réessayer le build
5. Consulter logs dans console

---

**Bon build ! 🔨**

*Guide pour NiTriTe V13.0*
*Dernière mise à jour : 2024-11-10*
