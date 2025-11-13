# 📘 Guide d'Utilisation - NiTrite v2.0 Portable

**Version Autonome - Aucune Installation Requise**

---

## 🎯 Pour l'Utilisateur Final

### ✅ Ce qu'il faut savoir

Cette version de NiTrite est **100% autonome** :
- ✅ Aucun Python à installer
- ✅ Aucune dépendance requise
- ✅ Fonctionne sur n'importe quel PC Windows 10/11
- ✅ Peut être lancé depuis une clé USB

---

## 🚀 Utilisation (3 étapes simples)

### 1️⃣ Décompresser
```
1. Téléchargez NiTrite_Autonome_v2.0.zip
2. Faites clic-droit > Extraire tout
3. Choisissez un dossier (Bureau, Téléchargements, etc.)
```

### 2️⃣ Lancer
```
Double-clic sur NiTrite_OrdiPlus_v2.exe
```

**ℹ️ Note:** Le premier lancement peut prendre 5-10 secondes (normal).

### 3️⃣ Utiliser
```
1. Cochez les programmes à installer
2. Cliquez sur "🚀 INSTALLER"
3. Attendez la fin de l'installation
```

**C'est tout ! 🎉**

---

## ⚠️ Messages Windows Normaux

### "Windows a protégé votre PC"
**C'est normal !** L'exe n'est pas signé.

**Solution:**
1. Cliquez sur "Informations complémentaires"
2. Cliquez sur "Exécuter quand même"

### Antivirus bloque l'exécutable
**C'est un faux positif** (exécutable non signé).

**Solution:**
1. Ouvrez votre antivirus
2. Ajoutez une exception pour `NiTrite_OrdiPlus_v2.exe`

---

## 🔧 Pour le Développeur / Technicien

### Compilation de l'Exécutable

#### Prérequis (uniquement pour compiler)
```bash
# Python 3.8+ installé
python --version

# PyInstaller
pip install pyinstaller

# Dépendances (optionnel - seront embarquées)
pip install -r requirements.txt
```

#### Étape 1 : Vérification
```bash
# Lancer le script de vérification
VERIFIER_AVANT_BUILD.bat
```

Ce script vérifie :
- ✅ Présence de tous les fichiers sources
- ✅ Python installé
- ✅ PyInstaller installé
- ✅ Structure des dossiers correcte

#### Étape 2 : Compilation
```bash
# Méthode recommandée
BUILD_AUTONOME.bat

# Ou directement
python build_exe.py
```

**Temps de compilation:** ~5 minutes

#### Étape 3 : Résultat
```
NiTrite_Autonome/
├── NiTrite_OrdiPlus_v2.exe  (~27 MB)
├── LANCER_NITRITE.bat
└── README.txt

NiTrite_Autonome_v2.0.zip    (~25 MB) ← À distribuer
```

---

## 🐛 Dépannage

### L'exe ne se lance pas
**Solutions:**
1. Vérifiez que Windows 10/11 est installé
2. Désactivez temporairement l'antivirus
3. Consultez les logs : `logs/nitrite.log`

### Lancement très lent
**Normal au premier lancement** (Python se décompresse).
Les lancements suivants seront plus rapides.

### Programmes ne s'installent pas
**Solutions:**
1. Vérifiez votre connexion Internet
2. Lancez en tant qu'administrateur (clic-droit > Exécuter en tant qu'administrateur)
3. Certains programmes nécessitent WinGet (installé automatiquement)

### Message "Fichier manquant"
**Solutions:**
1. Assurez-vous de ne pas déplacer juste l'exe
2. Gardez tous les fichiers du dossier `NiTrite_Autonome` ensemble
3. Redécompressez le ZIP complet

---

## 📊 Détails Techniques

### Contenu de l'Exécutable
L'exe contient :
- Python 3.x embarqué
- tkinter (interface graphique)
- Toutes les bibliothèques (requests, Pillow, pywin32, etc.)
- Base de données de 240+ programmes
- Code source de NiTrite

### Taille
- **Exécutable:** ~27 MB
- **ZIP:** ~25 MB (compressé)
- **Extraction:** ~30 MB

### Performance
- **Premier lancement:** 5-10 secondes
- **Lancements suivants:** 2-3 secondes
- **Installation d'un programme:** Variable (dépend du téléchargement)

---

## 📁 Structure du Dossier Portable

```
NiTrite_Autonome/
│
├── NiTrite_OrdiPlus_v2.exe    ← Exécutable principal
│   └── [Contient tout Python + code]
│
├── LANCER_NITRITE.bat         ← Lanceur optionnel
├── README.txt                 ← Instructions rapides
│
└── logs/                      ← Créé au premier lancement
    └── nitrite.log            ← Journal d'activité
```

---

## ✨ Avantages de cette Version

| Critère | Version Portable | Version Source |
|---------|------------------|----------------|
| **Installation Python** | ❌ Non requis | ✅ Requis |
| **Dépendances** | ❌ Aucune | ✅ pip install... |
| **Fichiers à distribuer** | 📦 1 exe (27 MB) | 📂 Dossier complet |
| **Compatibilité** | 🟢 100% PC Windows | 🟡 Si Python installé |
| **Simplicité** | 🟢 Double-clic | 🟡 Plusieurs étapes |
| **Portable USB** | ✅ Oui | ❌ Non |

---

## 🔐 Sécurité

### Est-ce sûr ?
✅ **OUI**, c'est sûr !

- Le code source est ouvert
- Aucun virus, malware ou spyware
- Les programmes installés proviennent de sources officielles
- PyInstaller est un outil standard et reconnu

### Pourquoi l'antivirus bloque ?
- L'exe n'est pas signé numériquement (coût élevé)
- C'est un **faux positif** classique pour les exes PyInstaller
- Solution : Ajouter une exception

---

## 📞 Support

### En cas de problème
1. 📖 Lisez ce guide
2. 📝 Consultez `CORRECTIFS_VERSION_PORTABLE.md`
3. 🔍 Vérifiez `logs/nitrite.log`
4. 💬 Créez une issue sur GitHub

### Fichiers de support
- `CORRECTIFS_VERSION_PORTABLE.md` - Détails techniques des corrections
- `README_AUTONOME.md` - Documentation complète
- `logs/nitrite.log` - Journal d'exécution

---

## 🎉 Prêt à l'Emploi !

**Votre version portable de NiTrite est maintenant prête !**

Pour distribuer :
1. Partagez `NiTrite_Autonome_v2.0.zip`
2. L'utilisateur décompresse
3. L'utilisateur double-clique sur l'exe
4. C'est parti ! 🚀

---

**Version:** 2.0 Autonome  
**Dernière mise à jour:** 5 novembre 2025  
**Statut:** ✅ Production