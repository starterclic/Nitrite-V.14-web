# ADW CLEANER - MODE PORTABLE

**Date:** 5 novembre 2025  
**Version:** NiTrite v2.0

## 📋 MODIFICATION

ADW Cleaner a été converti en **application portable** au lieu d'une installation système, comme AnyDesk et RustDesk.

## 🔄 CHANGEMENTS EFFECTUÉS

### Configuration (`data/programs.json`)

**AVANT:**
```json
"AdwCleaner": {
    "description": "Suppression d'adwares, toolbars et PUPs",
    "download_url": "https://adwcleaner.malwarebytes.com/adwcleaner?channel=release",
    "install_args": "/eula /clean /noreboot",
    "portable": false,
    "admin_required": true,
    "cleanup_folder": "Outils de nettoyage"
}
```

**APRÈS:**
```json
"AdwCleaner Portable": {
    "description": "Suppression d'adwares, toolbars et PUPs (Version portable)",
    "download_url": "https://adwcleaner.malwarebytes.com/adwcleaner?channel=release",
    "install_args": "portable",
    "portable": true,
    "admin_required": false,
    "cleanup_folder": "Outils de nettoyage"
}
```

## 🎯 COMPORTEMENT

### Installation classique (AVANT)
1. ❌ Téléchargement du setup
2. ❌ Exécution avec `/eula /clean /noreboot`
3. ❌ Installation dans `C:\Program Files`
4. ❌ Nécessite droits administrateur

### Mode portable (APRÈS)
1. ✅ Téléchargement de l'exécutable
2. ✅ Copie dans `Bureau\Outils de nettoyage\adwcleaner_x.x.x.exe`
3. ✅ Création d'un raccourci sur le bureau
4. ✅ AUCUNE installation système
5. ✅ Pas besoin de droits admin

## 📂 EMPLACEMENT

L'application sera téléchargée dans le dossier **"Outils de nettoyage"** sur le Bureau, comme:

```
Bureau/
└── Outils de nettoyage/
    ├── AnyDesk.exe (portable)
    ├── RustDesk-1.3.2-x86_64.exe (portable)
    └── adwcleaner_x.x.x.exe (portable) ← NOUVEAU
```

## ✅ AVANTAGES

- **Pas d'installation système** : L'application ne modifie pas Windows
- **Pas besoin d'admin** : Fonctionne sans élévation de privilèges
- **Facilement accessible** : Raccourci direct sur le bureau
- **Portable** : Peut être copié sur une clé USB
- **Cohérence** : Même comportement que AnyDesk et RustDesk

## 🧪 TESTS

Le script `test_adwcleaner_portable.py` vérifie que:
- ✅ `portable = true`
- ✅ `install_args = "portable"`
- ✅ `cleanup_folder = "Outils de nettoyage"`
- ✅ `admin_required = false`
- ✅ URL de téléchargement valide

## 📦 VERSION

Cette modification est incluse dans **NiTrite_Autonome_v2.0.zip** (25 MB)

---

**Note:** ADW Cleaner est naturellement une application portable. Cette configuration respecte mieux sa conception native.
