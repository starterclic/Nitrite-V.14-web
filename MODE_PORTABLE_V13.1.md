# NiTriTe V13.1 - Mode Portable Complet

## 🎯 Tout est Inclus dans l'Exe !

**L'exécutable portable inclut TOUTES les dépendances :**

### ✅ Bibliothèques GUI
- ✅ `tkinter` (interface graphique)
- ✅ `Pillow` (images)
- ✅ `ttk` (widgets modernes)

### ✅ Diagnostics Système (CRITIQUE)
- ✅ `psutil` - CPU, RAM, disque, performances
- ✅ `wmi` - Informations système Windows détaillées
- ✅ `win32com` - Accès WMI avancé

### ✅ Windows API
- ✅ `pywin32` - Privilèges admin, API Windows
- ✅ `win32api`, `win32con`, `win32process`
- ✅ `win32security`, `win32event`, `win32file`

### ✅ Networking
- ✅ `requests` - Téléchargements
- ✅ `urllib3` - HTTP
- ✅ `certifi` - Certificats SSL

### ✅ Tous les Modules de l'App
- ✅ `src.gui_modern_v13` - Interface principale
- ✅ `src.advanced_pages` - **5 pages avancées**
- ✅ `src.tools_data_complete` - 553+ outils
- ✅ `src.winget_manager` - Gestion WinGet
- ✅ Et 11 autres modules...

---

## 📊 Taille de l'Exe Portable

**Avec toutes les dépendances incluses :**
- Exécutable : ~35-50 MB
- Archive ZIP : ~25-35 MB (compressé)

**Contenu :**
- NiTriTe_V13_Modern.exe (tout-en-un)
- data/programs.json (715 apps)
- README.txt

---

## 🔧 Pages Avancées Fonctionnelles en Portable

### 🔄 Page Mises à Jour
**Dépendances incluses :**
- WinGet (utilisé via subprocess)
- PowerShell (natif Windows)

**Fonctionnalités actives :**
- ✅ Détection apps installées
- ✅ Vérification updates
- ✅ Génération scripts PowerShell/Batch

### 💾 Page Backup & Restore
**Dépendances incluses :**
- PowerShell pour points de restauration
- DISM pour drivers (natif Windows)

**Fonctionnalités actives :**
- ✅ Création point de restauration
- ✅ Backup drivers système
- ✅ Sauvegarde liste apps (JSON)

### ⚡ Page Optimisations
**Dépendances incluses :**
- Registre Windows (natif)
- Services Windows (natif)
- Task Manager (natif)

**Fonctionnalités actives :**
- ✅ Désactivation télémétrie
- ✅ Gestion services
- ✅ Optimisation démarrage
- ✅ Nettoyage registre

### 🔍 Page Diagnostic
**Dépendances incluses :**
- ✅ `psutil` (embarqué dans l'exe!)
- ✅ `wmi` (embarqué dans l'exe!)
- ✅ `win32com` (embarqué dans l'exe!)

**Fonctionnalités actives :**
- ✅ Score de santé PC (0-100)
- ✅ Infos système complètes (CPU, RAM, GPU)
- ✅ Barres de performance en temps réel
- ✅ Benchmark CPU/RAM/Disque
- ✅ Rapport système complet

### ⚙️ Page Paramètres
**Dépendances incluses :**
- JSON pour sauvegarde thème

**Fonctionnalités actives :**
- ✅ 4 thèmes (Dark/Light Orange, Dark Blue, Dark Purple)
- ✅ Sauvegarde préférence dans data/theme_config.json
- ✅ Changement à chaud (pas besoin de redémarrer)

---

## 🚀 Build Portable - Process Complet

### 1. Installation Dépendances (Automatique)
```bash
python build_v13.py
```

Le script installe automatiquement :
- PyInstaller
- psutil
- wmi
- pywin32
- Pillow
- requests
- Et toutes les autres...

### 2. Compilation (2-5 minutes)
PyInstaller crée un **exe monolithique** avec :
- Toutes les bibliothèques Python embarquées
- Les modules psutil/wmi compilés
- Les DLL Windows nécessaires
- Les fichiers data/ et assets/

### 3. Package Final
```
NiTriTe V13.1 Portable/
├── NiTriTe_V13_Modern.exe  ← TOUT EST DEDANS
├── README.txt
├── README_V13.md
└── LANCER.bat
```

**Aucune installation requise !**
**Aucune dépendance externe !**
**Tout fonctionne en mode portable !**

---

## ✅ Vérification - Comment Tester

### Test 1 : Pages s'affichent
1. Lancez l'exe portable
2. Cliquez sur chaque page dans la navigation
3. **TOUTES les pages devraient avoir du contenu**

**Si une page est vide :**
- Le build n'a pas inclus `psutil` ou `wmi`
- Vérifiez que `build_v13.py` a bien tous les hiddenimports

### Test 2 : Diagnostic Fonctionne
1. Allez sur page "🔍 Diagnostic"
2. Vous devriez voir :
   - Score de santé PC (pas 0)
   - CPU : nom + % utilisation
   - RAM : Go utilisés + %
   - Barres de performance animées

**Si tout est à 0% :**
- `psutil` n'est pas chargé
- Recompilez avec `python build_v13.py`

### Test 3 : Thèmes Fonctionnent
1. Allez sur page "⚙️ Paramètres"
2. Cliquez sur un thème différent
3. Les couleurs devraient changer immédiatement

**Si rien ne change :**
- Fichier `data/theme_config.json` non accessible
- Vérifiez que data/ est bien dans le même dossier que l'exe

### Test 4 : Optimisations Accessibles
1. Allez sur "⚡ Optimisations"
2. Vous devriez voir 4 sections colorées
3. Cliquez sur "Désactiver Télémétrie"

**Si page vide :**
- Erreur dans `advanced_pages.py`
- Vérifiez les logs console

---

## 🔍 Fallbacks Automatiques

**Si psutil/wmi échouent en mode portable :**

Les pages affichent quand même :
- ✅ Tous les boutons et sections
- ⚠️ Valeurs à 0 pour performances
- ℹ️ Message "Module non disponible"

**Exemple (DiagnosticPage sans psutil) :**
```
💯 Score de Santé PC
Score: 0/100
État: Données non disponibles
⚠️ Module psutil non chargé

💻 Informations Système
OS: Windows (via platform)
CPU: N/A
RAM: N/A

[Boutons benchmark toujours fonctionnels]
```

**C'est normal en mode développement**, mais **PAS en mode portable compilé** car tout est inclus dans l'exe !

---

## 🐛 Problèmes Courants

### "ImportError: No module named psutil"
**Solution :** Recompilez avec tous les hiddenimports :
```bash
python build_v13.py
```

Vérifiez que `build_v13.py` contient :
```python
hiddenimports=[
    ...
    'psutil',
    'psutil._common',
    'psutil._psutil_windows',
    'wmi',
    'win32com',
    ...
]
```

### "Pages vides après compilation"
**Causes possibles :**
1. ❌ `src.advanced_pages` pas dans hiddenimports
2. ❌ Erreur lors import psutil/wmi
3. ❌ Fichier advanced_pages.py corrompu

**Solution :**
```bash
# Nettoyer
rmdir /S /Q build dist

# Recompiler
python build_v13.py
```

### "DLL load failed: Le module spécifié est introuvable"
**Cause :** pywin32 mal inclus

**Solution :**
```bash
pip uninstall pywin32
pip install pywin32==306
python build_v13.py
```

---

## 📦 Checklist Build Portable

Avant de distribuer :

- [ ] `python build_v13.py` réussit sans erreur
- [ ] Exe créé dans `NiTriTe V13.1 Portable/`
- [ ] Archive ZIP créée à la racine
- [ ] Taille exe : 35-50 MB (si plus petit, des libs manquent)
- [ ] Test exe sur PC propre (sans Python installé)
- [ ] Toutes les 8 pages s'affichent correctement
- [ ] Page Diagnostic affiche CPU/RAM/% (pas 0)
- [ ] Page Paramètres change les thèmes
- [ ] Page Optimisations affiche 4 sections
- [ ] WinGet fonctionne (détection apps)

---

## ✅ Conclusion

**NiTriTe V13.1 en mode portable = 100% autonome**

- ✅ Aucune dépendance externe
- ✅ Pas besoin de Python installé
- ✅ Pas besoin de pip install
- ✅ Toutes les bibliothèques embarquées
- ✅ Fonctionne sur Windows 10/11 propre
- ✅ Un seul exe de ~40 MB
- ✅ Toutes les fonctionnalités actives

**Si vous avez compilé avec `build_v13.py` récent (avec tous les hiddenimports), TOUT devrait fonctionner parfaitement !**
