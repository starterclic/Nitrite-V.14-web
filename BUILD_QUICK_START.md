# 🚀 Guide Rapide de Build - NiTriTe V13.0

## ⚡ Build en 3 étapes (Windows uniquement)

### 1️⃣ Installer les dépendances
```cmd
pip install -r requirements.txt
```

### 2️⃣ Lancer le build
```cmd
python build_v13.py
```

### 3️⃣ Récupérer le package
Le fichier portable est dans `dist/NiTriTe_V13_Portable_YYYYMMDD.zip`

---

## 🔧 Prérequis

- **Windows 10/11** (obligatoire)
- **Python 3.8+** avec pip
- **5-10 minutes** pour le premier build

---

## ❌ Résolution des problèmes

### Le build échoue avec "Module not found"
```cmd
pip install --upgrade -r requirements.txt
```

### PyInstaller n'est pas trouvé
```cmd
pip install pyinstaller
```

### L'exécutable n'est pas créé
1. Supprimez les dossiers `build/` et `dist/`
2. Supprimez le fichier `*.spec`
3. Relancez `python build_v13.py`

### Erreur "tkinter not found" sur Windows
tkinter est normalement inclus avec Python Windows. Réinstallez Python avec l'option "tcl/tk" cochée.

---

## 📦 Structure du package final

```
NiTriTe_V13_Portable_20251110/
├── NiTriTe_V13_Modern.exe  (35-50 MB)
├── README.txt
├── README_V13.md
└── LANCER.bat
```

---

## 💡 Options avancées

### Build avec console de debug
Modifiez `build_v13.py` ligne 176 : `console=True`

### Réduire la taille de l'exe
1. Installez UPX : https://upx.github.io/
2. Le script l'utilisera automatiquement

### Build sans compression
Modifiez le .spec : `upx=False`

---

## 📞 Support

- Documentation complète : `GUIDE_BUILD_WINDOWS.md`
- Structure projet : `STRUCTURE.md`
- README principal : `README_V13.md`

---

**Version** : 13.0
**Build Script** : `build_v13.py`
**Type** : Portable (One-File)
