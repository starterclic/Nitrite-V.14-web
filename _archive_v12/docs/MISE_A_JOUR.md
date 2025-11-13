# 🔄 Guide de Mise à Jour - NiTrite v2.0

## 🎯 Objectif

Ce guide vous aide à récupérer les dernières modifications (304 applications au lieu de 241).

---

## ✅ Étape 1: Vérifier votre version actuelle

### Windows (méthode simple):
```
Double-cliquez sur: VERIFIER_NOMBRE_APPS.bat
```

### Ligne de commande:
```bash
python verifier_nombre_apps.py
```

**Résultat attendu:**
- ✅ **304 applications** = Vous avez la dernière version
- ⚠️ **241 applications** = Vous devez mettre à jour

---

## 🔄 Étape 2: Récupérer les dernières modifications

### Méthode 1: Git Pull (recommandé)

Si vous avez cloné le dépôt:

```bash
# Aller dans le répertoire du projet
cd nitrite-v2-portable

# Récupérer les dernières modifications
git pull origin claude/analyze-and-fix-app-011CUxUDqMVYZBmahuMZqLZf
```

### Méthode 2: Téléchargement manuel

1. Allez sur GitHub: https://github.com/heiphaistos44-crypto/nitrite-v2-portable
2. Changez de branche vers: `claude/analyze-and-fix-app-011CUxUDqMVYZBmahuMZqLZf`
3. Cliquez sur "Code" → "Download ZIP"
4. Décompressez et remplacez vos fichiers

### Méthode 3: Clone frais

```bash
# Supprimer l'ancien dossier et recloner
git clone -b claude/analyze-and-fix-app-011CUxUDqMVYZBmahuMZqLZf https://github.com/heiphaistos44-crypto/nitrite-v2-portable.git
cd nitrite-v2-portable
```

---

## ✅ Étape 3: Vérifier après mise à jour

Relancez la vérification:

```
VERIFIER_NOMBRE_APPS.bat
```

Ou:

```bash
python verifier_nombre_apps.py
```

**Vous devriez maintenant voir: ✅ 304 applications**

---

## 🔍 Si vous utilisez un exécutable (.exe)

Si vous avez compilé NiTrite en `.exe`, vous devez **recompiler**:

```bash
# Après avoir récupéré les dernières modifications
python build_exe.py
```

Cela créera un nouveau `.exe` avec les 304 applications.

---

## 📊 Détails des modifications

### Avant (version 241 applications):
- 17 catégories avec 10+ programmes
- Plusieurs popups UAC

### Après (version 304 applications):
- **+63 nouvelles applications**
- **25 catégories** avec 10+ programmes
- **Auto-élévation admin** (1 seul popup UAC)
- **Tests unitaires** (17 tests)
- **Documentation complète**

---

## 🐛 Problèmes Courants

### Problème 1: "git pull" ne fonctionne pas

**Solution:**
```bash
# Réinitialiser votre branche locale
git fetch origin
git reset --hard origin/claude/analyze-and-fix-app-011CUxUDqMVYZBmahuMZqLZf
```

### Problème 2: Toujours 241 applications après git pull

**Cause possible:** Vous regardez un ancien exécutable compilé

**Solution:**
- Vérifiez avec `python verifier_nombre_apps.py`
- Si le fichier JSON a 304 mais l'app affiche 241, recompilez:
  ```bash
  python build_exe.py
  ```

### Problème 3: Modifications locales en conflit

**Solution:**
```bash
# Sauvegarder vos modifications
git stash

# Récupérer les dernières modifications
git pull origin claude/analyze-and-fix-app-011CUxUDqMVYZBmahuMZqLZf

# Réappliquer vos modifications (optionnel)
git stash pop
```

---

## ✅ Checklist Finale

Avant de lancer NiTrite, vérifiez:

- [ ] Le fichier `data/programs.json` contient 304 applications
- [ ] La vérification affiche "✅ 304 applications"
- [ ] Si vous utilisez un `.exe`, il a été recompilé après la mise à jour
- [ ] Tous les fichiers de la branche `claude/analyze-and-fix-app-011CUxUDqMVYZBmahuMZqLZf` sont présents

---

## 🚀 Lancement après mise à jour

Une fois la mise à jour confirmée:

```
LANCER_NITRITE.bat
```

Ou:

```bash
python lancer_nitrite.py
```

---

## 📝 Note Importante

La catégorie **"Outils OrdiPlus"** n'a **PAS** été modifiée et contient toujours exactement 10 programmes (comme demandé).

---

## 💡 Besoin d'aide?

1. Exécutez `verifier_installation.py` pour un diagnostic complet
2. Consultez `GUIDE_UTILISATION.md` pour plus d'informations
3. Vérifiez les logs Git pour voir l'historique des modifications

---

**Dernière mise à jour:** 2025-11-09
**Version cible:** NiTrite v2.0 (304 applications)
**Branche:** `claude/analyze-and-fix-app-011CUxUDqMVYZBmahuMZqLZf`
