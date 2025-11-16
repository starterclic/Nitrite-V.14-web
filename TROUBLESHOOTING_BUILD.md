# 🔧 Guide de Dépannage - Build Version Web Portable

## 🧪 ÉTAPE 1: Test Rapide (RECOMMANDÉ D'ABORD)

Avant de compiler, testez que tout fonctionne:

```bash
# Double-cliquez sur:
TEST_WEB_PORTABLE.bat
```

**Ce test permet de:**
- ✅ Vérifier que Python fonctionne
- ✅ Vérifier que les dépendances sont installées
- ✅ Tester le script sans compilation
- ✅ Identifier les problèmes rapidement

**Si le test fonctionne:** Passez à la compilation
**Si le test échoue:** Consultez les erreurs ci-dessous

---

## ❌ Problèmes Courants et Solutions

### 1. "Python n'est pas installé"

**Problème:** Python n'est pas dans le PATH

**Solutions:**
```bash
# Option A: Installer Python
https://www.python.org/downloads/

# Option B: Ajouter au PATH
# Cherchez "Variables d'environnement" dans Windows
# Ajoutez le chemin Python (ex: C:\Python39)
```

### 2. "Module not found: flask"

**Problème:** Dépendances manquantes

**Solution:**
```bash
pip install -r requirements.txt
```

### 3. "PyInstaller command not found"

**Problème:** PyInstaller pas installé

**Solution:**
```bash
pip install pyinstaller
```

### 4. "Erreur lors de la compilation"

**Problème:** PyInstaller échoue

**Solutions:**
```bash
# Option A: Réinstaller PyInstaller
pip uninstall pyinstaller
pip install pyinstaller

# Option B: Version spécifique
pip install pyinstaller==5.13.0

# Option C: Nettoyer et réessayer
rmdir /s /q build
rmdir /s /q dist
BUILD_WEB.bat
```

### 5. "Module 'src.xxx' not found"

**Problème:** Modules src/ non trouvés

**Solution:**
- Vérifiez que le dossier `src/` existe
- Vérifiez que tous les `.py` sont présents dans `src/`
- Relancez `BUILD_WEB.bat`

### 6. "web_backend.py not found"

**Problème:** Fichier backend manquant

**Solution:**
- Vérifiez que `web_backend.py` est à la racine du projet
- Ne déplacez pas ce fichier

### 7. "Dossier web\ non trouvé"

**Problème:** Interface web manquante

**Solution:**
- Vérifiez que le dossier `web/` existe
- Vérifiez qu'il contient: `index.html`, `css/`, `js/`, `data/`

### 8. L'exe se ferme immédiatement

**Problème:** Erreur au démarrage de l'exe

**Solutions:**
```bash
# Lancez l'exe depuis une console pour voir l'erreur
cmd
cd dist
NiTriTe_Web_V13.exe

# Ou testez sans compiler:
TEST_WEB_PORTABLE.bat
```

### 9. Le navigateur ne s'ouvre pas

**Problème:** Webbrowser échoue

**Solution:**
- Attendez 3-5 secondes
- Ouvrez manuellement: `http://127.0.0.1:5000`
- Le serveur fonctionne même si le navigateur ne s'ouvre pas

### 10. "Port 5000 déjà utilisé"

**Problème:** Un autre processus utilise le port

**Solutions:**
```bash
# Trouver le processus
netstat -ano | findstr :5000

# Tuer le processus (remplacez PID par le numéro)
taskkill /PID <numero> /F

# Ou changez le port dans web_backend.py (ligne ~1037)
# app.run(host='0.0.0.0', port=5001, ...)
```

---

## 🔍 Debugging Avancé

### Logs détaillés

Le script `nitrite_web_portable.py` affiche des logs détaillés:
- Répertoire de base
- Fichiers trouvés
- Modules importés
- Erreurs avec traceback

### Test manuel

```bash
# 1. Activer environnement (si utilisé)
# venv\Scripts\activate

# 2. Tester l'import
python
>>> import web_backend
>>> # Si pas d'erreur, c'est bon !

# 3. Tester le lanceur
python nitrite_web_portable.py
```

### Vérifier la structure

```
Votre projet doit avoir:
├── nitrite_web_portable.py     ✓
├── NiTriTe_Web_Portable.spec   ✓
├── BUILD_WEB.bat               ✓
├── TEST_WEB_PORTABLE.bat       ✓
├── web_backend.py              ✓
├── requirements.txt            ✓
├── web/
│   ├── index.html              ✓
│   ├── css/                    ✓
│   ├── js/                     ✓
│   └── data/                   ✓
├── src/
│   ├── *.py (tous les modules) ✓
├── data/
│   └── programs.json           ✓
└── assets/
    └── icon.ico                ✓
```

---

## 🆘 Problèmes Persistants

Si rien ne fonctionne:

### 1. Environnement propre

```bash
# Créer un environnement virtuel propre
python -m venv venv_build
venv_build\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
BUILD_WEB.bat
```

### 2. Version Python

Assurez-vous d'utiliser Python 3.8 à 3.11:
```bash
python --version
# Si < 3.8 ou > 3.11, installez Python 3.10
```

### 3. Permissions

Lancez en tant qu'administrateur:
- Clic droit sur `BUILD_WEB.bat`
- "Exécuter en tant qu'administrateur"

### 4. Antivirus

Certains antivirus bloquent PyInstaller:
- Ajoutez une exception pour le dossier du projet
- Ou désactivez temporairement l'antivirus

---

## ✅ Checklist Complète

Avant de compiler, vérifiez:

- [ ] Python 3.8-3.11 installé
- [ ] `pip install -r requirements.txt` réussi
- [ ] `pip install pyinstaller` réussi
- [ ] `TEST_WEB_PORTABLE.bat` fonctionne
- [ ] Tous les fichiers présents (voir structure ci-dessus)
- [ ] Pas d'erreurs dans les imports
- [ ] Antivirus autorise PyInstaller

Si tout est ✅ → Lancez `BUILD_WEB.bat` ! 🚀

---

## 📞 Support

Si vous rencontrez toujours des problèmes:

1. Vérifiez les logs détaillés dans la console
2. Testez avec `TEST_WEB_PORTABLE.bat`
3. Vérifiez que tous les fichiers sont présents
4. Essayez dans un environnement virtuel propre

**Le build devrait fonctionner avec les corrections apportées !**

---

*Dernière mise à jour: Corrections build web portable*
