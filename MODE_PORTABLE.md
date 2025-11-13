# 📦 Mode Portable - NiTriTe V13.0

## 🎯 Objectif : RIEN sur le PC Client

L'application NiTriTe V13 est **100% portable** :
- ✅ Un seul fichier `.exe` (35-50 MB)
- ✅ Toutes les dépendances embarquées
- ✅ Pas d'installation requise
- ✅ Pas de traces laissées sur le système

---

## 📦 Comment fonctionne le mode portable ?

### 1. **Build avec PyInstaller "onefile"**

Le script `build_v13.py` crée un exécutable **onefile** :

```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,    # ← Toutes les DLL embarquées
    a.zipfiles,    # ← Bibliothèques Python embarquées
    a.datas,       # ← Fichiers data/ et assets/ embarqués
    [],
    name='NiTriTe_V13_Modern',
    ...
)
```

**Résultat** : Un seul fichier `.exe` autonome

---

### 2. **Dépendances embarquées**

Toutes ces bibliothèques sont **à l'intérieur de l'exe** :

| Dépendance | Taille | Usage |
|------------|--------|-------|
| **Python 3.x** | ~15 MB | Runtime Python complet |
| **tkinter** | ~5 MB | Interface graphique |
| **PIL/Pillow** | ~3 MB | Gestion des images |
| **requests** | ~2 MB | Téléchargements HTTP |
| **pywin32** | ~5 MB | API Windows |
| **Modules src/** | ~1 MB | Code de l'application |
| **data/** | ~1 MB | Base de 715 apps |
| **assets/** | <1 MB | Icônes et logo |

**Total** : ~35-50 MB dans un seul `.exe`

---

### 3. **Extraction temporaire**

⚠️ **Important** : PyInstaller utilise un dossier temporaire lors de l'exécution

**Au lancement de l'exe** :
1. L'exe extrait les fichiers dans `%TEMP%\_MEIxxxxxx\`
2. L'application s'exécute depuis ce dossier temporaire
3. À la fermeture, le dossier temporaire est **automatiquement supprimé**

**Avantages** :
- ✅ Rapide (extraction en ~1-2 secondes)
- ✅ Nettoyage automatique
- ✅ Pas de traces permanentes

**Localisation du temp** :
```
Windows : C:\Users\[User]\AppData\Local\Temp\_MEIxxxxxx\
```

---

### 4. **Aucune installation système**

L'exe **n'installe RIEN** sur le PC :

❌ Pas d'installation dans `Program Files`
❌ Pas d'entrée dans le Registre Windows
❌ Pas de fichiers dans `AppData` (sauf temp temporaire)
❌ Pas de service Windows
❌ Pas de modification système

✅ Juste l'exe qui s'exécute

---

## 🚀 Utilisation Portable

### Pour le client final :

1. **Décompresser le ZIP**
   ```
   NiTriTe_V13_Portable_20251110.zip
   ```

2. **Lancer l'exe**
   ```
   Double-clic sur NiTriTe_V13_Modern.exe
   ```

3. **C'est tout !**
   - Pas d'installation
   - Pas de setup
   - L'application démarre directement

### Pour déplacer l'application :

- ✅ Copier l'exe sur une clé USB : **OK**
- ✅ Envoyer l'exe par email : **OK**
- ✅ Partager sur réseau : **OK**
- ✅ Exécuter depuis un dossier réseau : **OK**

---

## 🔒 Sécurité & Privilèges

### Privilèges administrateur

Certaines fonctionnalités nécessitent les droits admin :
- Installation d'applications via WinGet
- Commandes système (DISM, SFC, etc.)
- Modifications de configuration réseau

**Solution** : Windows affichera l'UAC prompt automatiquement

### Antivirus

⚠️ Les antivirus peuvent bloquer l'exe car :
- Fichier non signé
- Comportement de "packer" (PyInstaller)
- Exécution de commandes système

**Solutions** :
1. Signer l'exe avec un certificat de code
2. Ajouter à la liste blanche de l'antivirus
3. Expliquer au client que c'est normal

---

## 📊 Comparaison des modes

| Critère | Mode Portable (actuel) | Mode Installé | Mode Script Python |
|---------|------------------------|---------------|-------------------|
| **Fichier unique** | ✅ 1 exe | ❌ Setup + fichiers | ❌ Multiples .py |
| **Installation** | ✅ Aucune | ❌ Requise | ❌ Python requis |
| **Taille** | 35-50 MB | ~100 MB | ~10 MB |
| **Démarrage** | ~2-3 sec | ~1 sec | ~3-5 sec |
| **Traces système** | ✅ Minimal (temp) | ❌ Registre, AppData | ✅ Aucune |
| **Facilité d'usage** | ✅✅✅ Excellent | ⭐⭐ Moyen | ⭐ Difficile |
| **Distribution** | ✅ Simple (ZIP) | ⭐ Setup.exe | ❌ Complexe |

**Verdict** : Le mode portable est **idéal pour les techniciens** 👍

---

## 🎨 Optimisations avancées

### Réduire la taille de l'exe

**Option 1 : UPX (déjà activé)**
```python
upx=True  # Compression ~30-40%
```
Taille : 50 MB → ~35 MB

**Option 2 : Exclure modules inutiles**
```python
excludes=['pytest', 'unittest', 'email', 'xml']
```
Gain : ~5-10 MB

**Option 3 : Strip symbols**
```python
strip=True  # Linux/Mac uniquement
```

### Mode vraiment offline

Pour garantir que l'exe fonctionne **sans Internet** :

1. Embarquer tous les fichiers nécessaires
2. Vérifier que `requests` n'est utilisé que pour les téléchargements optionnels
3. Mode dégradé si pas de connexion

---

## 💾 Stockage des données

### Où l'application stocke-t-elle ses données ?

**Actuellement** :
- ✅ Tout est dans l'exe (data/, assets/, src/)
- ✅ Pas de fichiers externes requis
- ✅ Pas de base de données SQLite externe

**Si besoin de persistance** (profils, favoris, historique) :
- Option 1 : Fichier JSON à côté de l'exe
- Option 2 : Base SQLite à côté de l'exe
- Option 3 : Fichier dans `%APPDATA%` (NON portable)

**Recommandation** : Garder les données dans un fichier à côté de l'exe pour rester portable

---

## 🔧 Dépannage Mode Portable

### L'exe ne démarre pas

**1. Vérifier les prérequis Windows**
```
- Windows 10/11 (x64)
- .NET Framework 4.8+ (normalement préinstallé)
- Visual C++ Redistributable (embarqué dans l'exe)
```

**2. Vérifier l'antivirus**
```
- Désactiver temporairement
- Ajouter exception pour l'exe
```

**3. Lancer en mode debug**
Modifier le .spec : `console=True` puis rebuilder

### L'exe est trop lent

**Causes possibles** :
1. Premier lancement (extraction dans temp) : Normal
2. Antivirus qui scanne l'exe : Ajouter exception
3. Disque lent : Copier sur SSD

**Solutions** :
- Ajouter l'exe à l'exception antivirus
- Utiliser un SSD
- Réduire la taille avec UPX

### Le dossier %TEMP% se remplit

**Normal** : PyInstaller crée un dossier `_MEIxxxxxx` à chaque lancement

**Nettoyage automatique** :
- Windows nettoie automatiquement après 7 jours
- Ou manuellement : `cleanmgr` → Fichiers temporaires

---

## 📞 FAQ

### Est-ce vraiment portable ?
**Oui**, mais avec extraction temporaire dans %TEMP%. C'est le standard pour les exe Python.

### Puis-je vendre cette application ?
**Oui**, l'exe peut être distribué commercialement. Pensez à :
- Signer le code avec un certificat
- Créer une licence
- Ajouter un système d'activation (optionnel)

### Puis-je exécuter depuis une clé USB ?
**Oui**, complètement. L'exe fonctionne depuis n'importe quel support.

### Quid de la sécurité ?
- L'exe n'est pas signé par défaut → Alerte Windows Defender
- Solution : Acheter un certificat de signature de code (~200-300€/an)

---

## 🎯 Checklist Build Portable

Avant de distribuer l'exe, vérifier :

- [ ] L'exe démarre sans erreur
- [ ] Toutes les pages (Apps + Outils) s'affichent
- [ ] Les 548 outils sont présents
- [ ] Les 715 applications sont listées
- [ ] La recherche fonctionne
- [ ] Les redirections web fonctionnent
- [ ] Les commandes système s'exécutent
- [ ] Pas d'erreur dans les logs
- [ ] Taille de l'exe < 100 MB
- [ ] Icône visible dans l'exe

---

**Version** : 13.0
**Mode** : Portable (onefile)
**PyInstaller** : 6.0+
**Taille cible** : 35-50 MB
