# 🚀 NiTriTe V13.0 - Nouvelles Fonctionnalités

## 📋 Vue d'ensemble

Cette mise à jour majeure ajoute **5 nouvelles pages** et de nombreuses fonctionnalités avancées pour les techniciens de maintenance informatique.

---

## 🎨 1. Page Paramètres & Thèmes

### Fonctionnalités
- **4 thèmes préconçus** :
  - 🌙 Sombre Orange (défaut) - Le thème classique noir & orange
  - ☀️ Clair Orange - Version claire pour environnements lumineux
  - 💙 Sombre Bleu - Thème bleu professionnel
  - 💜 Sombre Violet - Thème violet moderne

### Utilisation
1. Accéder à **⚙️ Paramètres** dans la navigation
2. Cliquer sur **"Appliquer"** sous le thème désiré
3. L'application redémarre automatiquement
4. Le thème est sauvegardé et appliqué au prochain démarrage

### Détails techniques
- Changement dynamique des couleurs
- Sauvegarde dans `data/theme_config.json`
- Aperçu des couleurs avant application

---

## 🔍 2. Page Diagnostic & Benchmark

### Score de Santé PC
- **Calcul automatique** basé sur :
  - Utilisation CPU
  - Saturation RAM
  - Espace disque disponible
- **Score 0-100** avec code couleur :
  - 🟢 80-100 : Excellent
  - 🟡 60-79 : Correct
  - 🔴 0-59 : Attention requise
- **Recommandations personnalisées**

### Informations Système
- OS et version
- Processeur et nombre de cœurs
- RAM totale
- Architecture

### Performance en Temps Réel
- **Barres de progression** pour :
  - Utilisation CPU (%)
  - Utilisation RAM (%)
  - Utilisation Disque (%)
- Rafraîchissement manuel

### Benchmarks (à venir)
- Test CPU
- Test RAM
- Test Disque (lecture/écriture)

### Prérequis
- Module `psutil` (installé automatiquement)
- Module `wmi` pour infos avancées (optionnel)

---

## 💾 3. Page Backup & Restauration

### Point de Restauration Windows
- **Création automatique** avec date et heure
- Nécessite **droits administrateur**
- Utilise PowerShell : `Checkpoint-Computer`
- **Accès direct** à l'interface de restauration

### Sauvegarde des Pilotes
- **Export complet** de tous les pilotes système
- Utilise `DISM /export-driver`
- Sauvegarde dans dossier horodaté
- **Restauration guidée** via Gestionnaire de périphériques

### Liste des Applications
- **Export** : Génère liste complète (winget list)
- Sauvegarde sur le Bureau en `.txt`
- **Import** : Installation batch (à venir)
- Compatible avec winget

### Fonctionnalités
```
✅ Créer Point de Restauration
✅ Voir Points de Restauration existants
✅ Sauvegarder tous les pilotes
✅ Restaurer les pilotes
✅ Exporter liste applications
🚧 Importer & réinstaller apps
```

---

## ⚡ 4. Page Optimisations Windows

### Confidentialité & Télémétrie
Options disponibles :
- ☑️ Désactiver la télémétrie Windows
- ☑️ Désactiver Cortana
- ☑️ Désactiver la localisation
- ☑️ Désactiver l'ID publicitaire

⚠️ **Attention** : Modifications du registre Windows

### Services Windows
- Accès direct à `services.msc`
- Optimisation automatique (à venir)
- Désactivation services non essentiels

### Applications au Démarrage
- Accès rapide aux paramètres
- Ouvre `ms-settings:startupapps`
- Gestion avancée des programmes de démarrage

### Registre Windows
- Accès à `regedit`
- Nettoyage automatique (en développement)
- ⚠️ **Fonction avancée** - Utiliser avec prudence

### Recommandations
Pour l'instant, utiliser des outils dédiés :
- O&O ShutUp10++
- W10Privacy
- WPD (Windows Privacy Dashboard)

---

## 🔄 5. Page Mises à Jour & Scripts

### Détection des Applications
- **Scanner** les apps installées via winget
- Comptage automatique
- Détection des versions installées

### Vérification Mises à Jour
- **winget upgrade** : Liste complète
- Affichage dans fenêtre dédiée
- Détection apps obsolètes

### Mise à Jour Automatique
- **Update global** : `winget upgrade --all`
- Confirmation avant exécution
- Progression en temps réel

### Générateur de Scripts

#### PowerShell (.ps1)
```powershell
# Installation automatique via winget
# Apps prédéfinies ou personnalisées
# Compatible Windows 10/11
```

#### Batch (.bat)
```batch
# Scripts compatibles anciennes versions
# Installation séquentielle
# Logs d'installation
```

### Cas d'usage
1. **Déploiement** : Installer même config sur plusieurs PC
2. **Automatisation** : Scripts planifiés
3. **Documentation** : Traçabilité des installations

---

## 🎯 Fonctionnalités Communes

### Interface Unifiée
- **Scroll intelligent** avec roulette souris
- **Design cohérent** avec le reste de l'app
- **Cartes Material Design**
- **Animations fluides**

### Navigation
- **8 pages** au total :
  1. 📦 Applications (715 apps)
  2. 🛠️ Outils Système (553+ outils)
  3. 🚀 Master Installation
  4. 🔄 Mises à Jour
  5. 💾 Backup & Restore
  6. ⚡ Optimisations
  7. 🔍 Diagnostic
  8. ⚙️ Paramètres

### Gestion d'Erreurs
- **Fallbacks** si modules manquants
- **Messages clairs** pour l'utilisateur
- **Logs détaillés** pour debug

---

## 📦 Installation & Prérequis

### Dépendances Python
```bash
pip install -r requirements.txt
```

### Modules Requis
- `psutil>=5.9.0` - Monitoring système
- `wmi>=1.5.1` - Infos système (Windows)

### Modules Optionnels
Si non installés, fonctionnalités réduites mais app fonctionnelle.

---

## 🔧 Configuration

### Fichiers de Configuration
```
data/
├── theme_config.json      # Thème sélectionné
├── programs.json          # Liste applications
└── ...
```

### Chemins Importants
- **Bureau** : Export rapports, drivers, listes
- **AppData** : Configurations utilisateur (si non portable)

---

## 🚦 Roadmap - Fonctionnalités à Venir

### Court Terme
- ✅ Thèmes personnalisables
- ✅ Diagnostic avancé
- ✅ Backup complet
- 🚧 Rollback/Désinstallation propre
- 🚧 Système de favoris

### Moyen Terme
- Import/Réinstallation depuis liste apps
- Benchmarks complets avec scores
- Nettoyage registre automatique
- Profils d'installation

### Long Terme
- Mode multi-PC (réseau)
- Cloud sync
- Historique complet
- Rapports PDF professionnels
- Mode technicien Pro

---

## 🐛 Bugs Connus & Limitations

### Windows uniquement
Certaines fonctionnalités sont spécifiques à Windows :
- Point de restauration
- Backup drivers (DISM)
- Services Windows
- Registre

### Droits Administrateur
Requis pour :
- Point de restauration
- Backup drivers
- Modifications registre
- Tweaks système

### Modules Python
- `wmi` : Windows uniquement
- `psutil` : Fortement recommandé pour diagnostic

---

## 📖 Documentation Technique

### Architecture Fichiers
```
src/
├── gui_modern_v13.py      # Interface principale
├── advanced_pages.py      # Nouvelles pages (2000+ lignes)
├── tools_data_complete.py # Données outils
└── ...
```

### Classes Principales
- `ThemeManager` - Gestion thèmes
- `SettingsPage` - Page paramètres
- `DiagnosticPage` - Diagnostic & benchmark
- `BackupPage` - Backup & restauration
- `OptimizationsPage` - Optimisations Windows
- `UpdatesPage` - Mises à jour & scripts

---

## 💡 Conseils d'Utilisation

### Pour Techniciens
1. **Créer point de restauration** AVANT toute opération
2. **Exporter liste apps** pour traçabilité
3. **Générer scripts** pour déploiements répétés
4. **Utiliser diagnostic** avant/après maintenance

### Pour Utilisateurs Avancés
1. **Choisir thème** adapté à l'environnement
2. **Monitorer santé PC** régulièrement
3. **Sauvegarder drivers** avant mises à jour
4. **Désactiver télémétrie** pour confidentialité

---

## 🤝 Contribution

Pour rapporter bugs ou suggérer fonctionnalités :
- Issues GitHub
- Pull Requests bienvenues
- Tests approfondis appréciés

---

## 📝 Changelog

### v13.0 - 2025
- ✨ 5 nouvelles pages avancées
- 🎨 Système de thèmes avec 4 présets
- 🔍 Diagnostic complet avec score santé
- 💾 Backup drivers et point restauration
- ⚡ Optimisations Windows avancées
- 🔄 Gestion mises à jour winget
- 📜 Générateur scripts PowerShell/Batch
- 🖱️ Scroll roulette souris (toutes pages)
- 📦 Grille Applications optimisée (4 colonnes)
- 🎯 Navigation étendue à 8 pages

---

## 📞 Support

Pour assistance :
- Documentation intégrée
- Tooltips dans l'interface
- Messages d'erreur détaillés
- Logs système

---

**NiTriTe V13.0** - L'outil complet pour techniciens de maintenance ! 🚀
