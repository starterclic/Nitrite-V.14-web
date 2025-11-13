# 📦 Guide d'installation - Outils OrdiPlus

## 🎯 Vue d'ensemble

Cette catégorie regroupe **11 programmes essentiels** pour la maintenance et l'utilisation quotidienne d'un ordinateur, tels que recommandés par OrdiPlus.

---

## 🚀 Installation rapide via NiTrite

### Méthode 1 : Interface graphique (Recommandée)
```powershell
python nitrite_winget.py
```
1. Sélectionner la catégorie **"Outils OrdiPlus"**
2. Cocher les programmes souhaités
3. Cliquer sur **"Installer la sélection"**

### Méthode 2 : Installation manuelle via Winget

Voici les commandes pour installer chaque programme individuellement :

---

## 📋 Liste complète des programmes

### 🔐 **1. AnyDesk** - Accès à distance
```powershell
winget install --id AnyDesk.AnyDesk --silent
```
- **Catégorie:** Accès à distance
- **Fonction:** Contrôle à distance de PC
- **Version:** Mise à jour automatique via Winget

---

### 🔐 **2. RustDesk** - Alternative TeamViewer open source
```powershell
winget install --id RustDesk.RustDesk --silent
```
- **Catégorie:** Accès à distance
- **Fonction:** Contrôle à distance open source
- **Avantage:** Gratuit et sans limitation

---

### 🛡️ **3. Spybot Search & Destroy** - Anti-malware
```powershell
winget install --id SaferNetworking.SpybotSearchAndDestroy --silent
```
- **Catégorie:** Sécurité
- **Fonction:** Détection et suppression de malwares et spywares
- **Protection:** Complète contre les menaces

---

### 🛡️ **4. Malwarebytes** - Protection anti-malware
```powershell
winget install --id Malwarebytes.Malwarebytes --silent
```
- **Catégorie:** Sécurité
- **Fonction:** Protection en temps réel contre les malwares
- **Scan:** Analyse complète du système

---

### 🧹 **5. AdwCleaner** - Suppression d'adwares
```powershell
winget install --id Malwarebytes.AdwCleaner --silent
```
- **Catégorie:** Sécurité
- **Fonction:** Suppression de programmes indésirables et adwares
- **Rapidité:** Scan ultra-rapide

---

### 🧹 **6. Wise Disk Cleaner** - Nettoyage de disque
```powershell
winget install --id WiseCleaner.WiseDiskCleaner --silent
```
- **Catégorie:** Optimisation
- **Fonction:** Nettoyage et optimisation de disque
- **Gain:** Libération d'espace disque importante

---

### 📄 **7. Adobe Acrobat Reader** - Lecteur PDF
```powershell
winget install --id Adobe.Acrobat.Reader.64-bit --silent
```
- **Catégorie:** Lecteurs
- **Fonction:** Lecture de fichiers PDF
- **Standard:** Lecteur PDF de référence

---

### 🎬 **8. VLC Media Player** - Lecteur multimédia
```powershell
winget install --id VideoLAN.VLC --silent
```
- **Catégorie:** Multimédia
- **Fonction:** Lecture de tous les formats audio/vidéo
- **Universel:** Lit pratiquement tous les formats

---

### 📊 **9. Microsoft Office 2007** - Suite bureautique
```powershell
winget install --id Microsoft.Office --silent
```
- **Catégorie:** Bureautique
- **Fonction:** Word, Excel, PowerPoint, etc.
- **Note:** Version 2007 (classique)

---

### 📊 **10. Microsoft Office 2016** - Suite bureautique
```powershell
winget install --id Microsoft.Office --silent
```
- **Catégorie:** Bureautique
- **Fonction:** Suite Office moderne
- **Note:** Version 2016 (recommandée)

---

### 📊 **11. Microsoft Office 2024** - Suite bureautique (la plus récente)
```powershell
winget install --id Microsoft.Office --silent
```
- **Catégorie:** Bureautique
- **Fonction:** Dernière version d'Office
- **Note:** Version 2024 (toutes dernières fonctionnalités)

---

## 🔧 Installation complète - Pack OrdiPlus

### Installer TOUS les outils OrdiPlus en une seule commande :

```powershell
# Installation complète du pack OrdiPlus
winget install --id AnyDesk.AnyDesk --silent
winget install --id RustDesk.RustDesk --silent
winget install --id SaferNetworking.SpybotSearchAndDestroy --silent
winget install --id Malwarebytes.Malwarebytes --silent
winget install --id Malwarebytes.AdwCleaner --silent
winget install --id WiseCleaner.WiseDiskCleaner --silent
winget install --id Adobe.Acrobat.Reader.64-bit --silent
winget install --id VideoLAN.VLC --silent
winget install --id Microsoft.Office --silent
```

---

## 📦 Installation par thématique

### Pack Sécurité (4 programmes)
```powershell
winget install --id SaferNetworking.SpybotSearchAndDestroy --silent
winget install --id Malwarebytes.Malwarebytes --silent
winget install --id Malwarebytes.AdwCleaner --silent
winget install --id WiseCleaner.WiseDiskCleaner --silent
```

### Pack Accès à distance (2 programmes)
```powershell
winget install --id AnyDesk.AnyDesk --silent
winget install --id RustDesk.RustDesk --silent
```

### Pack Lecteurs (2 programmes)
```powershell
winget install --id Adobe.Acrobat.Reader.64-bit --silent
winget install --id VideoLAN.VLC --silent
```

### Pack Bureautique (1 programme - choisir une version)
```powershell
# Choisir UNE SEULE version d'Office
winget install --id Microsoft.Office --silent
```

---

## ⚠️ Notes importantes

### Microsoft Office
- **Attention:** Les trois versions (2007, 2016, 2024) utilisent le même ID Winget
- **Recommandation:** N'installez qu'une seule version d'Office
- **Choix:** Winget installera la version disponible dans votre contexte

### Ordre d'installation recommandé
1. **D'abord la sécurité:** Malwarebytes, AdwCleaner, Spybot
2. **Ensuite le nettoyage:** Wise Disk Cleaner
3. **Puis les lecteurs:** Adobe Reader, VLC
4. **Enfin la bureautique:** Office
5. **Si nécessaire:** Outils d'accès à distance (AnyDesk, RustDesk)

### Droits administrateur
Certains programmes peuvent nécessiter des droits administrateur pour l'installation. Exécutez PowerShell en tant qu'administrateur si nécessaire.

---

## 🔄 Mises à jour

### Mettre à jour tous les programmes OrdiPlus
```powershell
winget upgrade --id AnyDesk.AnyDesk
winget upgrade --id RustDesk.RustDesk
winget upgrade --id SaferNetworking.SpybotSearchAndDestroy
winget upgrade --id Malwarebytes.Malwarebytes
winget upgrade --id Malwarebytes.AdwCleaner
winget upgrade --id WiseCleaner.WiseDiskCleaner
winget upgrade --id Adobe.Acrobat.Reader.64-bit
winget upgrade --id VideoLAN.VLC
winget upgrade --id Microsoft.Office
```

### Mettre à jour TOUT en une commande
```powershell
winget upgrade --all
```

---

## 🗑️ Désinstallation

### Désinstaller un programme
```powershell
# Exemple avec AnyDesk
winget uninstall --id AnyDesk.AnyDesk
```

### Désinstaller tout le pack OrdiPlus
```powershell
winget uninstall --id AnyDesk.AnyDesk
winget uninstall --id RustDesk.RustDesk
winget uninstall --id SaferNetworking.SpybotSearchAndDestroy
winget uninstall --id Malwarebytes.Malwarebytes
winget uninstall --id Malwarebytes.AdwCleaner
winget uninstall --id WiseCleaner.WiseDiskCleaner
winget uninstall --id Adobe.Acrobat.Reader.64-bit
winget uninstall --id VideoLAN.VLC
winget uninstall --id Microsoft.Office
```

---

## 📊 Vérification des installations

### Lister les programmes OrdiPlus installés
```powershell
winget list --id AnyDesk.AnyDesk
winget list --id RustDesk.RustDesk
winget list --id SaferNetworking.SpybotSearchAndDestroy
winget list --id Malwarebytes.Malwarebytes
winget list --id Malwarebytes.AdwCleaner
winget list --id WiseCleaner.WiseDiskCleaner
winget list --id Adobe.Acrobat.Reader.64-bit
winget list --id VideoLAN.VLC
winget list --id Microsoft.Office
```

---

## 🎯 Cas d'usage typiques

### 🖥️ **Configuration PC neuf**
Installez le pack complet pour avoir tous les outils essentiels :
```powershell
python nitrite_winget.py
# Sélectionner "Outils OrdiPlus" > Tout cocher > Installer
```

### 🔧 **Maintenance PC existant**
Installez uniquement les outils de sécurité et nettoyage :
```powershell
# Pack Sécurité + Nettoyage
winget install --id Malwarebytes.Malwarebytes --silent
winget install --id Malwarebytes.AdwCleaner --silent
winget install --id WiseCleaner.WiseDiskCleaner --silent
```

### 🏢 **Configuration bureau à distance**
Installez les outils d'accès à distance :
```powershell
winget install --id AnyDesk.AnyDesk --silent
winget install --id RustDesk.RustDesk --silent
```

### 📄 **Poste utilisateur basique**
Installez les lecteurs essentiels + Office :
```powershell
winget install --id Adobe.Acrobat.Reader.64-bit --silent
winget install --id VideoLAN.VLC --silent
winget install --id Microsoft.Office --silent
```

---

## 💡 Astuces

### Installation silencieuse complète
Ajoutez `--silent` à chaque commande pour éviter toute interaction utilisateur.

### Accepter automatiquement les licences
Ajoutez `--accept-package-agreements --accept-source-agreements` :
```powershell
winget install --id VideoLAN.VLC --silent --accept-package-agreements --accept-source-agreements
```

### Vérifier avant installation
Utilisez `winget show` pour voir les détails :
```powershell
winget show --id AnyDesk.AnyDesk
```

---

## 📞 Support

Pour toute question sur les programmes OrdiPlus, référez-vous à :
- **Documentation NiTrite:** MISE_A_JOUR_V2.5_ORDIPLUS.md
- **Support Winget:** `winget --help`
- **Site officiel des éditeurs** pour chaque programme

---

*Guide d'installation - Outils OrdiPlus pour NiTrite v2.5*
*11 programmes essentiels pour votre PC Windows*
