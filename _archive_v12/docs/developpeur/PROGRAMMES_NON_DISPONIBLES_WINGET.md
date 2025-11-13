# 📋 Programmes non disponibles dans Winget

Ce document liste les programmes qui ont été demandés mais qui ne sont **pas disponibles** dans le dépôt officiel Winget.

---

## ❌ Programmes recherchés sans succès

### 📄 Lecture PDF
- **Sumatra PDF** - Alternative légère à Adobe Reader
  - *Raison:* Non trouvé dans Winget
  - *Alternative:* Adobe Reader disponible dans NiTrite

### 💬 Communication
- **Beeper** - Client de messagerie tout-en-un
  - *Raison:* Erreur de connexion Winget
  - *Alternative:* Discord, Slack, Teams disponibles

### 🔧 Utilitaires Système
- **Double Driver** - Sauvegarde de pilotes
  - *Raison:* Erreur de connexion Winget
  - *Alternative:* Utiliser Windows Update

- **WinMerge** - Outil de comparaison de fichiers
  - *Raison:* Erreur de connexion Winget
  - *Suggestion:* Installation manuelle depuis winmerge.org

- **WinSCP** - Client SFTP/FTP
  - *Raison:* Erreur de connexion Winget
  - *Alternative:* FileZilla disponible dans NiTrite

- **PCI-Z** - Informations sur les slots PCI
  - *Raison:* Non trouvé dans Winget
  - *Alternative:* CPU-Z disponible

- **RamExpert** - Analyse détaillée de la RAM
  - *Raison:* Non trouvé dans Winget
  - *Alternative:* CPU-Z disponible

- **SSD-Z** - Informations sur les SSD
  - *Raison:* Non trouvé dans Winget
  - *Alternative:* CrystalDiskInfo disponible

- **SSD Life** - Analyse de santé SSD
  - *Raison:* Non trouvé dans Winget
  - *Alternative:* CrystalDiskInfo disponible

- **Speccy** - Informations système détaillées
  - *Raison:* Non trouvé dans Winget
  - *Alternative:* CPU-Z, GPU-Z disponibles

- **PortableApps.com** - Plateforme d'applications portables
  - *Raison:* Non trouvé dans Winget
  - *Note:* Installation manuelle recommandée

### 💾 Gestion de disques
- **EaseUS Partition Master** - Gestionnaire de partitions
  - *Raison:* Non trouvé dans Winget
  - *Alternative:* Utiliser Gestion des disques Windows

- **Macrorit NTFS to FAT** - Conversion de système de fichiers
  - *Raison:* Non trouvé dans Winget
  - *Alternative:* Formatage Windows standard

- **Win to HDD** - Installation Windows sur disque externe
  - *Raison:* Non trouvé dans Winget

### 🎮 Gaming & Launchers
- **Playnite** - Gestionnaire de bibliothèque de jeux
  - *Raison:* Erreur de connexion Winget
  - *Alternative:* GOG Galaxy disponible

- **LaunchBox** - Frontend pour émulateurs et jeux
  - *Raison:* Non trouvé dans Winget
  - *Suggestion:* Installation manuelle

- **FiveM** - Client GTA V modifié pour multijoueur
  - *Raison:* Non trouvé dans Winget
  - *Note:* Installation depuis fivem.net

- **GameLoop** - Émulateur Android pour gaming
  - *Raison:* Erreur de connexion Winget
  - *Alternative:* BlueStacks disponible dans NiTrite

- **OpenIV** - Éditeur de mods GTA
  - *Raison:* Erreur de connexion Winget
  - *Note:* Installation manuelle recommandée

### ☁️ Cloud Gaming
- **Steam Link** - Streaming de jeux Steam
  - *Raison:* Non trouvé dans Winget
  - *Alternative:* GeForce NOW, Moonlight disponibles

- **Google Stadia** - Service cloud gaming Google
  - *Raison:* Non trouvé dans Winget
  - *Note:* Service arrêté par Google

- **Shadow** - PC gaming dans le cloud
  - *Raison:* Non trouvé dans Winget
  - *Alternative:* GeForce NOW disponible

### 🛠️ Modding & Tools
- **Special K** - Framework de modding de jeux
  - *Raison:* Non trouvé dans Winget

- **Porting Kit** - Outil pour exécuter jeux Windows sur Mac
  - *Raison:* Non trouvé dans Winget
  - *Note:* Spécifique à macOS

### 📱 APK & Android
- **Aptoide** - Store alternatif Android
  - *Raison:* Non trouvé dans Winget
  - *Note:* Application mobile uniquement

- **APK Pure** - Téléchargeur APK
  - *Raison:* Non trouvé dans Winget
  - *Note:* Service web principalement

- **APK Mirror** - Repository APK
  - *Raison:* Non trouvé dans Winget
  - *Note:* Service web uniquement

- **Panda Helper** - Store alternatif iOS/Android
  - *Raison:* Non trouvé dans Winget
  - *Note:* Application mobile uniquement

---

## 💡 Solutions alternatives

### Pour installer ces programmes manuellement :

1. **Chocolatey** - Alternative à Winget
   ```powershell
   choco install winmerge winscp playnite
   ```

2. **Scoop** - Gestionnaire de packages
   ```powershell
   scoop install winscp winmerge
   ```

3. **Sites officiels** - Téléchargement direct
   - WinMerge: https://winmerge.org
   - WinSCP: https://winscp.net
   - Playnite: https://playnite.link
   - FiveM: https://fivem.net
   - LaunchBox: https://www.launchbox-app.com

---

## 🔄 Problèmes de connexion Winget

Certaines recherches ont échoué avec l'erreur:
```
Failed when opening source(s); try the 'source reset' command
```

### Solution :
```powershell
winget source reset --force
winget source update
```

---

## ✅ Programmes similaires disponibles dans NiTrite

| Programme demandé | Alternative dans NiTrite |
|-------------------|--------------------------|
| Sumatra PDF | Adobe Acrobat Reader |
| WinSCP | FileZilla |
| Playnite | GOG Galaxy, Steam |
| GameLoop | BlueStacks, Google Play Games |
| PCI-Z | CPU-Z |
| RamExpert | CPU-Z |
| SSD-Z | CrystalDiskInfo |
| Speccy | CPU-Z, GPU-Z, HWiNFO |

---

*Dernière mise à jour: v2.4*
