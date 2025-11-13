# NiTriTe V.13 Beta - Version Web & Desktop

Gestionnaire d'Applications et Outils Système pour Windows

## 🎉 Nouveautés

### ✨ Version HTML/Web
Une version web complète a été ajoutée ! Vous pouvez maintenant utiliser NiTriTe dans votre navigateur avec **exactement les mêmes fonctionnalités** que l'application desktop.

### 🚀 Écran de Chargement
Les deux versions (web et desktop) incluent maintenant un magnifique écran de chargement avec :
- Logo animé NiTriTe
- Barre de progression
- Messages de chargement détaillés
- Animation fluide

---

## 📦 Contenu

- **715 applications** disponibles
- **25 catégories** d'applications
- **553+ outils système** Windows
- **10 profils** d'installation pré-configurés
- Interface moderne orange/noir
- Thème clair/sombre

---

## 🚀 Lancement

### Version Desktop (Tkinter)

**Windows :**
```bash
LANCER_V13.bat
```

**Ou directement avec Python :**
```bash
python nitrite_v13_modern.py
```

### Version Web (HTML + Flask)

**Windows :**
```bash
LANCER_WEB.bat
```

**Ou manuellement :**
```bash
# 1. Installer les dépendances
pip install flask flask-cors psutil

# 2. Lancer le serveur
python web_backend.py

# 3. Ouvrir dans le navigateur
http://localhost:5000
```

---

## 🌐 Version Web - Caractéristiques

### Structure des fichiers
```
web/
├── index.html          # Page principale
├── css/
│   ├── loading.css     # Styles de l'écran de chargement
│   └── styles.css      # Styles principaux
└── js/
    ├── loading.js      # Gestion de l'écran de chargement
    ├── api.js          # Communication avec le backend
    └── app.js          # Logique principale de l'application
```

### Fonctionnalités Web

#### ✅ Pages Disponibles
- **Applications** - Parcourir et installer 715 applications
- **Outils Système** - Accéder aux 553+ outils Windows
- **Profils** - Charger des profils d'installation pré-configurés
- **Installation Master** - Assistant d'installation en masse
- **Favoris** - Gérer vos applications favorites
- **Diagnostic** - Voir les informations système
- **Optimisations** - Optimiser Windows
- **Paramètres** - Configuration de l'application

#### ✅ Fonctionnalités Implémentées
- ✅ Recherche d'applications en temps réel
- ✅ Filtres par catégorie et source (WinGet, Portable, Download)
- ✅ Sélection multiple d'applications
- ✅ Système de favoris (stocké localement)
- ✅ Thème clair/sombre
- ✅ Interface responsive
- ✅ Animations fluides
- ✅ Statistiques en temps réel

#### 🔧 Backend API (Flask)

**Endpoints disponibles :**
```
GET  /api/health              - État du serveur
GET  /api/applications        - Liste des applications
GET  /api/tools               - Liste des outils système
GET  /api/profiles            - Liste des profils
GET  /api/diagnostics         - Informations système
POST /api/install             - Installer une application
POST /api/install/bulk        - Installation en masse
POST /api/tools/execute       - Exécuter un outil système
```

---

## 🎨 Écran de Chargement

### Version Web (HTML/CSS/JS)

L'écran de chargement web affiche :
1. Logo animé avec cercle rotatif
2. Titre "NiTriTe V.13 Beta"
3. Barre de progression avec effet shimmer
4. Pourcentage en temps réel
5. Messages de statut

**Séquence de chargement :**
```
0%   → Initialisation...
10%  → Chargement du système...
25%  → Chargement des ressources...
40%  → Lecture de 715 applications...
55%  → Organisation de 25 catégories...
70%  → Préparation de 553+ outils...
85%  → Configuration de 10 profils...
95%  → Préparation de l'interface...
100% → Lancement de NiTriTe V.13...
```

### Version Desktop (Tkinter)

Même séquence de chargement avec :
- Fenêtre centrée 500x400
- Logo "N" dans un cercle orange
- Barre de progression Tkinter stylisée
- Animation fluide en thread séparé

---

## 🔧 Configuration Requise

### Version Desktop
- Windows 10/11
- Python 3.8+
- Dépendances : `pip install -r requirements.txt`

### Version Web
- Windows 10/11 (pour le backend)
- Python 3.8+
- Navigateur moderne (Chrome, Firefox, Edge)
- Dépendances : `pip install flask flask-cors psutil`

---

## 📂 Architecture

### Version Desktop
```
nitrite_v13_modern.py       → Lanceur avec splash screen
src/
├── splash_screen.py        → Écran de chargement Tkinter
├── gui_modern_v13.py       → Interface principale
├── advanced_pages.py       → Pages additionnelles
├── profiles_manager.py     → Gestion des profils
├── installer_manager.py    → Gestionnaire d'installation
└── ...
```

### Version Web
```
web_backend.py              → Serveur Flask API
web/
├── index.html              → Interface HTML
├── css/                    → Feuilles de style
│   ├── loading.css         → Styles du loading screen
│   └── styles.css          → Styles principaux
└── js/                     → Scripts JavaScript
    ├── loading.js          → Gestion du loading
    ├── api.js              → Communication API
    └── app.js              → Logique application
```

---

## 🎯 Utilisation

### Version Desktop

1. **Lancer l'application :**
   - Double-clic sur `LANCER_V13.bat`
   - Un écran de chargement apparaît pendant 2-3 secondes
   - L'interface principale se lance automatiquement

2. **Naviguer :**
   - Menu latéral gauche pour changer de page
   - Recherche d'applications
   - Sélection et installation

### Version Web

1. **Démarrer le serveur :**
   - Double-clic sur `LANCER_WEB.bat`
   - Le serveur démarre sur http://localhost:5000
   - Le navigateur s'ouvre automatiquement

2. **Utilisation :**
   - Écran de chargement animé (2-3 secondes)
   - Interface identique à la version desktop
   - Toutes les fonctionnalités disponibles

---

## 🎨 Personnalisation

### Thème

**Web :**
- Bouton de thème dans la barre latérale
- Choix entre thème sombre et clair
- Préférence sauvegardée dans `localStorage`

**Desktop :**
- Bouton de thème dans la barre latérale
- Préférence sauvegardée dans les paramètres

### Couleurs

Les couleurs principales sont définies dans `web/css/styles.css` :
```css
--primary-color: #FF6B35;      /* Orange principal */
--primary-dark: #E85A28;       /* Orange foncé */
--bg-primary: #1a1a1a;         /* Fond principal */
--bg-secondary: #2d2d2d;       /* Fond secondaire */
```

---

## 🐛 Dépannage

### Version Web

**Le serveur ne démarre pas :**
```bash
pip install --upgrade flask flask-cors psutil
```

**Port 5000 déjà utilisé :**
Modifier `web_backend.py` ligne ~330 :
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

**Les applications ne se chargent pas :**
- Vérifier que `data/programs.json` existe
- Vérifier les logs du serveur Flask

### Version Desktop

**L'écran de chargement ne s'affiche pas :**
- Vérifier que `src/splash_screen.py` existe
- Vérifier l'import dans `nitrite_v13_modern.py`

**Erreur au lancement :**
```bash
pip install --upgrade tkinter
```

---

## 📝 Notes de Développement

### Mode Démonstration Web

Si le backend Flask n'est pas démarré, l'interface web fonctionne en **mode démonstration** :
- Les données sont chargées depuis `data/programs.json` directement
- Les installations sont simulées
- Les outils système ne sont pas exécutables
- Toutes les autres fonctionnalités restent disponibles

### Communication Backend

L'interface web communique avec le backend via **fetch API** :
```javascript
const response = await fetch('http://localhost:5000/api/applications');
const apps = await response.json();
```

---

## 🚀 Prochaines Étapes

### Fonctionnalités Prévues
- [ ] WebSocket pour mises à jour en temps réel
- [ ] Gestionnaire de téléchargement avec progression
- [ ] Installation réelle via le backend Flask
- [ ] Système de notifications push
- [ ] Export/Import de profils personnalisés
- [ ] Historique d'installation
- [ ] Scan des applications installées

---

## 📄 Licence

NiTriTe V.13 Beta - Gestionnaire d'Applications pour Techniciens

---

## 👨‍💻 Auteur

Développé avec ❤️ pour faciliter la maintenance informatique

**Version :** 13.0 Beta
**Date :** 2024
**Plateforme :** Windows 10/11

---

## 📞 Support

Pour toute question ou problème :
- Consulter la documentation complète
- Vérifier les logs du serveur (version web)
- Tester en mode démonstration

---

**Profitez de NiTriTe V.13 ! 🎉**
