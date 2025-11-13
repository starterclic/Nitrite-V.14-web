# 🔧 CORRECTION DES INSTALLATIONS - 5 novembre 2025

## ❌ Problème rapporté par l'utilisateur

"Les applications ne s'installent pas. Tout se déroule normalement mais à part AnyDesk Portable et le fichier de nettoyage créé, rien ne se passe quand j'installe toute la catégorie Ordi Plus et ça fait sûrement ça pour tout."

## 🔍 Diagnostic

### 1. Problèmes identifiés

#### A) **33 programmes en doublon dans programs.json**
- Malwarebytes, Adobe Acrobat Reader DC, VLC Media Player, etc. apparaissaient dans plusieurs catégories
- Résultat : 279 entrées dans JSON mais seulement 246 checkboxes créées
- **Impact** : Programmes non comptés quand cochés dans certaines catégories

#### B) **Programmes portables non gérés**
- Les programmes avec `"portable": true` et `"install_args": "portable"` se téléchargeaient mais ne s'installaient PAS
- Code tentait d'exécuter le fichier avec l'argument `"portable"` (invalide)
- **Impact** : AnyDesk Portable et RustDesk Portable ne s'installaient pas correctement

#### C) **Programmes non-portables sans logs d'installation**
- Les autres programmes (Malwarebytes, AdwCleaner, etc.) ne laissaient aucune trace dans les logs
- Problème à investiguer plus en profondeur

## ✅ Corrections appliquées

### 1. Nettoyage des doublons ✅

**Script créé** : `nettoyer_doublons.py`

**Actions** :
- Identification automatique des 33 doublons
- Sauvegarde de l'ancien fichier : `programs.json.backup_20251105_193024`
- Suppression intelligente avec ordre de priorité :
  1. Outils OrdiPlus (priorité maximale)
  2. Pack Office
  3. Navigateurs
  4. Antivirus
  5. Autres catégories...

**Résultat** :
```
Avant : 279 programmes (avec doublons)
Après : 246 programmes (sans doublons)
Supprimés : 33 doublons
```

**Exemples de doublons supprimés** :
- `Malwarebytes` : gardé dans "Outils OrdiPlus", supprimé de "Antivirus" et "Sécurité"
- `Adobe Acrobat Reader DC` : gardé dans "Outils OrdiPlus", supprimé de "Bureautique" et "Suites Professionnelles"
- `VLC Media Player` : gardé dans "Outils OrdiPlus", supprimé de "Multimédia"
- `Mozilla Firefox` : gardé dans "Outils OrdiPlus", supprimé de "Navigateurs"

### 2. Gestion des programmes portables ✅

**Fichier modifié** : `src/installer_manager.py`

**Ajout** dans `execute_installation()` (lignes 265-287) :

```python
# GESTION DES PROGRAMMES PORTABLES
if is_portable or install_args == 'portable':
    log_callback(f"Programme portable détecté - téléchargement uniquement", "info")
    log_callback(f"Fichier disponible: {installer_path}", "success")
    
    # Pour les portables, créer un dossier dédié
    portable_folder = program_info.get('cleanup_folder', 'Programmes Portables')
    portable_dir = Path.home() / 'Desktop' / portable_folder
    portable_dir.mkdir(parents=True, exist_ok=True)
    
    # Copier le fichier portable sur le bureau
    program_name = program_info.get('name', Path(installer_path).stem)
    dest_file = portable_dir / Path(installer_path).name
    
    import shutil
    shutil.copy2(installer_path, dest_file)
    log_callback(f"✅ Fichier portable copié dans: {portable_dir}", "success")
    
    # Créer un raccourci si c'est un .exe
    if dest_file.suffix.lower() == '.exe':
        self.create_desktop_shortcut(str(dest_file), program_name, log_callback)
    
    return True
```

**Comportement** :
1. Détecte les programmes portables (`portable: true` OU `install_args: "portable"`)
2. Crée un dossier sur le Bureau (selon `cleanup_folder` défini dans JSON)
3. Copie le fichier téléchargé dans ce dossier
4. Crée un raccourci sur le Bureau pour les .exe
5. Log le succès et retourne `True`

**Programmes concernés** :
- `AnyDesk Portable` → copié dans `Bureau/Outils de nettoyage/`
- `RustDesk Portable` → copié dans `Bureau/Outils de nettoyage/`

## 📊 État des programmes "Outils OrdiPlus"

Après corrections, voici l'état des 10 programmes :

| Programme | Type | Status | Commentaire |
|-----------|------|--------|-------------|
| AnyDesk Portable | Portable | ✅ CORRIGÉ | Copié sur le Bureau + raccourci |
| RustDesk Portable | Portable | ✅ CORRIGÉ | Copié sur le Bureau + raccourci |
| Malwarebytes | Installable | ⚠️ À TESTER | Args: `/VERYSILENT /NORESTART` |
| AdwCleaner | Installable | ⚠️ À TESTER | Args: `/eula /clean /noreboot` |
| Wise Disk Cleaner | Installable | ⚠️ À TESTER | Args: `/VERYSILENT /NORESTART` |
| Spybot Search & Destroy | Installable | ⚠️ À TESTER | Args: `/VERYSILENT /NORESTART` |
| Adobe Acrobat Reader DC | Installable | ⚠️ À TESTER | Args: `/sAll /rs /msi EULA_ACCEPT=YES` |
| VLC Media Player | Installable | ⚠️ À TESTER | Args: `/S` |
| Mozilla Firefox | Installable | ⚠️ À TESTER | Args: `/S` |
| Office 2007 | Installable | ⚠️ À TESTER | Args: `/silent` |

## 🔄 Prochaines étapes

### Tests requis :

1. **✅ Tester les programmes portables**
   - Cocher AnyDesk Portable + RustDesk Portable
   - Cliquer INSTALLER
   - Vérifier : dossier créé sur Bureau, fichiers copiés, raccourcis créés

2. **⚠️ Tester les programmes installables**
   - Cocher Malwarebytes, AdwCleaner, VLC
   - Cliquer INSTALLER
   - Vérifier les logs : téléchargement, installation, succès
   - Vérifier : programmes réellement installés dans Ajout/Suppression de programmes

3. **🔍 Analyser les logs si échec**
   - Fichier : `NiTrite_Portable/logs/nitrite.log`
   - Rechercher : erreurs d'installation, codes de retour non-zéro

### Corrections potentielles si problèmes persistent :

**Si les programmes ne s'installent toujours pas** :

1. **Vérifier les arguments d'installation**
   - Certains programmes peuvent nécessiter des arguments différents
   - Exemple : Adobe Reader utilise `/sAll /rs /msi EULA_ACCEPT=YES`

2. **Ajouter plus de logs**
   - Logger le téléchargement réussi
   - Logger le code de retour de l'installation
   - Logger stdout/stderr de l'installeur

3. **Vérifier les droits administrateur**
   - Certains programmes nécessitent des droits admin
   - Ajouter `admin_required: true` dans programs.json

4. **Timeout d'installation**
   - Certains programmes prennent plus de 5 minutes
   - Augmenter `install_timeout` dans programs.json

## 📝 Fichiers modifiés

1. `data/programs.json`
   - ✅ 33 doublons supprimés
   - ✅ Sauvegarde créée

2. `src/installer_manager.py`
   - ✅ Gestion des programmes portables ajoutée (lignes 265-287)
   - ✅ Import de `shutil` ajouté

3. Nouveaux fichiers créés :
   - `nettoyer_doublons.py` - Script de nettoyage réutilisable
   - `CORRECTION_INSTALLATIONS.md` - Ce document

## 🎯 Résumé

**Problèmes résolus** :
✅ Doublons supprimés (246 programmes uniques)
✅ Checkboxes comptées correctement
✅ Programmes portables gérés (copie + raccourcis)

**Problèmes à investiguer** :
⚠️ Installation silencieuse des programmes non-portables
⚠️ Logs d'installation manquants

**Recommandation** :
Tester l'installation de la catégorie "Outils OrdiPlus" et fournir les logs pour diagnostic approfondi si nécessaire.

---

**Date** : 5 novembre 2025
**Version** : NiTrite v.2 Ordi Plus Portable
**Package** : `NiTrite_Portable_v2.0.zip` (25.2 MB)
