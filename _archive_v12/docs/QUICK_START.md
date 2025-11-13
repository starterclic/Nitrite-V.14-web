# 🚀 Quick Start - NiTrite v2.0

## Démarrage Rapide (3 étapes)

### 1️⃣ Télécharger
```bash
git clone https://github.com/heiphaistos44-crypto/nitrite-v2-portable.git
cd nitrite-v2-portable
```

### 2️⃣ Lancer
**Windows** (double-clic):
```
LANCER_NITRITE.bat
```

**Ou avec Python**:
```bash
python lancer_nitrite.py
```

### 3️⃣ Utiliser
- Cochez les programmes que vous voulez installer
- Cliquez sur "Installer"
- C'est tout ! 🎉

---

## 📋 Ce que fait le lanceur automatiquement

✅ Vérifie Python 3.8+
✅ Installe les dépendances manquantes
✅ Vérifie l'intégrité des fichiers
✅ Lance l'application

**Temps estimé:** 30 secondes à 2 minutes (première fois)

---

## 🎯 Modes de Lancement

| Mode | Quand l'utiliser | Commande |
|------|------------------|----------|
| **Complet** | Première utilisation | `LANCER_NITRITE.bat` |
| **Portable** | Utilisations suivantes | `LANCER_PORTABLE.bat` |
| **Compilation** | Distribution | `python build_exe.py` |

---

## 🔍 Vérifier l'Installation

```bash
python verifier_installation.py
```

Affiche:
- ✅ Version Python
- ✅ Modules installés
- ✅ Structure du projet
- ✅ Fichiers de données
- ✅ Tests unitaires

---

## 🧪 Lancer les Tests

```bash
python run_tests.py
```

**Résultat:** 17 tests unitaires

---

## 📚 Documentation Complète

Pour plus de détails, consultez:
- **[GUIDE_UTILISATION.md](GUIDE_UTILISATION.md)** - Guide complet
- **[README.md](README.md)** - Documentation technique

---

## ⚡ Raccourcis Utiles

### Installation
```bash
# Installation manuelle des dépendances
pip install -r requirements.txt

# Lancement direct
python nitrite_complet.py
```

### Compilation
```bash
# Créer un exécutable standalone
python build_exe.py

# Résultat: NiTrite_Autonome/NiTrite_OrdiPlus_v2.exe
```

### Tests
```bash
# Tests unitaires
python run_tests.py

# Tests spécifiques
python -m unittest tests.test_core_functionality
```

---

## 🐛 Problèmes Courants

### Python non reconnu
**Solution:** Installez Python et cochez "Add Python to PATH"

### Modules manquants
**Solution:** Lancez `LANCER_NITRITE.bat` (installe automatiquement)

### Erreur d'import
**Solution:**
```bash
pip install -r requirements.txt
```

---

## 💡 Astuces

1. **Première fois?** → Utilisez `LANCER_NITRITE.bat`
2. **Déjà configuré?** → Utilisez `LANCER_PORTABLE.bat` (plus rapide)
3. **Besoin d'aide?** → Consultez `GUIDE_UTILISATION.md`
4. **Problème?** → Lancez `verifier_installation.py`

---

## 🎉 C'est prêt !

Votre installation de NiTrite est maintenant complète et prête à l'emploi.

**Pour lancer:**
- Double-cliquez sur `LANCER_NITRITE.bat`
- Ou tapez: `python lancer_nitrite.py`

**Bon usage ! 🚀**
