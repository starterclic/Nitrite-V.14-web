# 🚀 Guide de Démarrage Rapide - NiTriTe V13

## 📋 Sommaire
1. [Installation](#installation)
2. [Premier Lancement](#premier-lancement)
3. [Navigation](#navigation)
4. [Fonctionnalités Clés](#fonctionnalités-clés)
5. [Raccourcis](#raccourcis)
6. [Dépannage](#dépannage)

---

## 📥 Installation

### Version Script (Développement)

1. **Cloner ou télécharger le projet**
   ```bash
   git clone <repository-url>
   cd Nitrite-V.13-Beta-Portable-
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python nitrite_v13_modern.py
   ```

   **OU** double-cliquer sur `LANCER_V13.bat`

### Version Portable (Production)

1. **Compiler l'exécutable**
   ```bash
   python build_v13.py
   ```

2. **Récupérer le package**
   - Dossier : `dist/NiTriTe_V13_Portable_YYYYMMDD/`
   - Archive : `dist/NiTriTe_V13_Portable_YYYYMMDD.zip`

3. **Distribuer**
   - Extraire l'archive sur n'importe quel PC Windows
   - Double-cliquer sur `NiTriTe_V13_Modern.exe`
   - Aucune installation requise !

---

## 🎯 Premier Lancement

### 1. Démarrage

Au premier lancement, l'application :
- ✅ Charge la base de 715 applications
- ✅ Organise 553+ outils système
- ✅ Initialise les profils prédéfinis
- ✅ Crée le dossier de configuration (~/.nitrite/)

### 2. Interface Principale

Vous verrez :
- **Barre latérale gauche** : Navigation entre pages
- **Zone centrale** : Contenu de la page active
- **Barre de recherche** : Filtrage instantané
- **Statistiques** : En haut de chaque page

---

## 🧭 Navigation

### Barre Latérale

```
┌─────────────────┐
│    ⚡ NiTriTe   │  ← Logo et titre
│      V13.0      │
├─────────────────┤
│ 📦 Applications │  ← Page 1
│ 715 apps        │
├─────────────────┤
│ 🛠️ Outils      │  ← Page 2
│ 553+ boutons    │
└─────────────────┘
```

### Raccourcis Clavier

- **Tab** : Naviguer entre éléments
- **Espace** : Activer bouton/checkbox
- **Entrée** : Confirmer action
- **Échap** : Fermer fenêtre modale

---

## ⚡ Fonctionnalités Clés

### Page Applications

#### 1. Recherche Rapide
```
🔍 [Rechercher une application...]
   ↓
   Tapez "chrome" → Filtre instantané
```

#### 2. Sélection d'Applications
```
☐ Google Chrome [🌐]
   Navigateur web rapide et sécurisé
   📁 Navigateurs | 💼 Portable | ⚡ WinGet

☑ Mozilla Firefox [🌐]  ← Sélectionné
   Navigateur open-source
   📁 Navigateurs | ⚡ WinGet
```

#### 3. Installation
1. Sélectionner les apps (checkbox)
2. Cliquer sur "🚀 INSTALLER"
3. Confirmer
4. Suivre la progression en temps réel

#### 4. Accès Web Direct
- Cliquer sur 🌐 à côté de chaque app
- Ouvre le site officiel dans le navigateur
- Téléchargement manuel si souhaité

### Page Outils

#### 1. Sections Organisées
```
🔧 Activation & Téléchargements (5)
🔨 Réparation Système (5)
🧹 Maintenance & Nettoyage (4)
📊 Diagnostics & Infos (6)
...
```

#### 2. Exécution d'Outils
- **Commandes système** : Clic → Exécution directe
  - Exemple : "SFC Scan" → `sfc /scannow`

- **Liens web** : Clic → Ouvre dans navigateur
  - Exemple : "CCleaner" → https://www.ccleaner.com/

#### 3. Catégories Disponibles
1. 🔧 Activation & Téléchargements
2. 🔨 Réparation Système
3. 🧹 Maintenance & Nettoyage
4. 📊 Diagnostics & Infos
5. 🌐 Réseau & Internet
6. 🎨 Personnalisation Windows
7. 🔒 Sécurité & Confidentialité
8. 💼 Utilitaires Système
9. 🎮 Performance & Gaming
10. 🌍 Navigateurs & Web
11. 🛠️ Fabricants Support

---

## 🎯 Cas d'Usage Rapides

### Scénario 1 : Setup PC Gaming
```
1. Ouvrir "Page Applications"
2. Rechercher "gaming" ou utiliser Profil 🎮 Gaming Station
3. Sélectionner : Steam, Discord, OBS, etc.
4. Cliquer "INSTALLER"
5. Attendre la fin (automatique)
```

### Scénario 2 : Réparation Système
```
1. Ouvrir "Page Outils"
2. Section "🔨 Réparation Système"
3. Cliquer "DISM RestoreHealth"
4. Puis "SFC Scan"
5. Redémarrer si nécessaire
```

### Scénario 3 : Maintenance Client
```
1. Scanner le système (détection apps installées)
2. Comparer avec profil "💼 Bureau Professionnel"
3. Installer applications manquantes
4. Exécuter nettoyage (Page Outils)
5. Vérifier mises à jour
```

---

## 🎨 Personnalisation

### Profils d'Installation

#### Utilisation des Profils Prédéfinis
1. Page Applications → Bouton "Profils"
2. Sélectionner un profil :
   - 🎮 Gaming Station
   - 💼 Bureau Professionnel
   - 💻 Développeur
   - ...
3. Toutes les apps du profil sont sélectionnées
4. Cliquer "INSTALLER"

#### Créer un Profil Personnalisé
```python
# Via l'interface (à venir) ou manuellement
from src.profiles_manager import ProfilesManager

pm = ProfilesManager()
pm.create_profile(
    name="Mon Profil",
    description="Applications pour mes clients",
    applications=["Chrome", "Office", "7-Zip"],
    icon="💼",
    color="#ff6b00"
)
```

### Favoris

#### Ajouter aux Favoris
- ⭐ Cliquer sur l'étoile à côté d'une app
- Accès rapide dans section "Favoris"

#### Gérer les Favoris
- Affichage prioritaire en haut de liste
- Filtrage rapide "Mes Favoris"

---

## 📊 Statistiques & Historique

### Voir l'Historique
```python
from src.profiles_manager import ProfilesManager

pm = ProfilesManager()
history = pm.get_history(limit=20)

for entry in history:
    print(f"{entry['timestamp']}: {entry['app']} - {'✓' if entry['success'] else '✗'}")
```

### Apps les Plus Installées
```python
most_installed = pm.get_most_installed(limit=10)
for app, count in most_installed:
    print(f"{app}: {count} installations")
```

---

## 🔧 Dépannage

### L'application ne démarre pas

**Symptôme** : Double-clic sur .exe → Rien ne se passe

**Solutions** :
1. Vérifier Python installé : `python --version`
2. Vérifier dépendances : `pip install -r requirements.txt`
3. Lancer depuis terminal pour voir erreurs :
   ```bash
   python nitrite_v13_modern.py
   ```
4. Vérifier antivirus (peut bloquer)

### Erreur "Module not found"

**Symptôme** : `ModuleNotFoundError: No module named 'xxx'`

**Solution** :
```bash
pip install -r requirements.txt
# OU
pip install tkinter pillow requests
```

### Interface figée

**Symptôme** : Application ne répond plus

**Solutions** :
1. Attendre la fin de l'opération en cours
2. Vérifier connexion Internet
3. Forcer fermeture : Ctrl+Alt+Suppr → Gestionnaire des tâches
4. Relancer l'application

### Installation échoue

**Symptôme** : Erreur pendant installation d'apps

**Solutions** :
1. Vérifier connexion Internet
2. Exécuter en tant qu'administrateur
3. Désactiver antivirus temporairement
4. Essayer installation manuelle (bouton 🌐)
5. Vérifier logs : `~/.nitrite/logs/`

### Fichiers manquants

**Symptôme** : `File not found: data/programs.json`

**Solutions** :
1. Vérifier structure du projet :
   ```
   Nitrite-V.13-Beta-Portable-/
   ├── nitrite_v13_modern.py
   ├── src/
   ├── data/
   │   └── programs.json  ← Doit exister
   └── assets/
   ```
2. Re-télécharger le projet complet
3. Vérifier extraction complète de l'archive

---

## 💡 Conseils Pro

### Pour Techniciens

1. **Créer des profils personnalisés** pour vos clients récurrents
2. **Utiliser les favoris** pour vos outils préférés
3. **Consulter l'historique** pour tracking client
4. **Exporter les profils** pour partage entre techniciens

### Optimisation

1. **Pré-télécharger les apps** fréquentes (cache)
2. **Utiliser WinGet** quand disponible (plus rapide)
3. **Installer par lots** de 5-10 apps max
4. **Nettoyer régulièrement** le cache de téléchargement

### Bonnes Pratiques

1. **Toujours vérifier** les apps sélectionnées avant installation
2. **Créer un point de restauration** avant changements majeurs
3. **Tester sur VM** avant déploiement client
4. **Documenter** les profils personnalisés

---

## 📚 Ressources

### Documentation Complète
- `README_V13.md` - Documentation complète
- `docs/` - Documentation technique

### Support
- Issues GitHub : [Lien]
- Email : support@example.com
- Site web : https://example.com

### Mises à Jour
- Vérifier régulièrement les nouvelles versions
- Mettre à jour `programs.json` pour nouvelles apps
- Suivre le changelog dans README_V13.md

---

## 🎉 Prêt à Commencer !

Vous êtes maintenant prêt à utiliser **NiTriTe V13** !

### Checklist de Démarrage
- [ ] Application installée/compilée
- [ ] Dépendances vérifiées
- [ ] Premier lancement réussi
- [ ] Navigation comprise
- [ ] Test d'installation d'une app
- [ ] Exploration des outils système

### Prochaines Étapes
1. Explorer les 715 applications disponibles
2. Tester les profils prédéfinis
3. Créer vos premiers favoris
4. Personnaliser selon vos besoins
5. Partager avec votre équipe !

---

**Bonne maintenance ! 🚀**

*NiTriTe V13.0 - Modern Edition*
*© 2024 OrdiPlus Tools*
