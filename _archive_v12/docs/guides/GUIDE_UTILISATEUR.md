# 🚀 Guide d'utilisation - NiTrite v.2

## Bienvenue dans NiTrite v.2 !

NiTrite v.2 est votre assistant personnel pour installer automatiquement tous vos programmes favoris sur Windows 10/11 en quelques clics !

---

## 🎯 Démarrage rapide

### 1. Première utilisation
1. **Double-cliquez** sur `Lancer_NiTrite.bat` 
2. L'application installera automatiquement ses dépendances si nécessaire
3. L'interface graphique s'ouvrira

### 2. Alternative
- Exécutez directement : `python nitrite_installer.py`
- Ou utilisez le fichier de test : `python test_nitrite.py`

---

## 🖥️ Interface utilisateur

### Zone de sélection des programmes
- **Cases à cocher** : Sélectionnez les programmes à installer
- **Catégories** : Les programmes sont organisés par type :
  - 🌐 **Navigateurs** : Firefox, Chrome
  - 💻 **Développement** : VS Code, Git, Python, Node.js, etc.
  - 📄 **Bureautique** : LibreOffice, Adobe Reader
  - 🎵 **Multimédia** : VLC Player
  - 🔧 **Utilitaires** : 7-Zip, WinRAR, CCleaner, etc.
  - 💬 **Communication** : Discord
  - 🎮 **Jeux** : Steam
  - 🔒 **Sécurité** : Malwarebytes

### Boutons de sélection rapide
- **Tout sélectionner** : Sélectionne tous les programmes
- **Tout désélectionner** : Désélectionne tout
- **Configuration bureautique** : Sélection pour usage bureautique
- **Configuration développeur** : Sélection pour développeurs

### Zone de contrôle
- **Installer** : Lance l'installation des programmes sélectionnés
- **Barre de progression** : Affiche l'avancement
- **Rafraîchir** : Recharge la liste des programmes
- **Arrêter** : Stoppe l'installation en cours

---

## 📋 Procédure d'installation

### Étape 1 - Sélection
1. Parcourez la liste des programmes disponibles
2. Cochez ceux que vous souhaitez installer
3. Ou utilisez une configuration prédéfinie

### Étape 2 - Installation
1. Cliquez sur **"Installer les programmes sélectionnés"**
2. Confirmez votre choix
3. L'installation démarre automatiquement

### Étape 3 - Suivi
- Suivez la progression dans la barre
- Consultez les logs en temps réel
- L'installation est **100% silencieuse**

---

## ⚙️ Fonctionnalités avancées

### Gestion intelligente
- ✅ **Détection automatique** : Ne réinstalle pas les programmes déjà présents
- ✅ **Téléchargement optimisé** : Mise en cache des fichiers
- ✅ **Vérification d'intégrité** : Contrôle SHA256 quand disponible
- ✅ **Nettoyage automatique** : Suppression des fichiers temporaires

### Logs et débogage
- **Logs en temps réel** : Dans la zone de journal
- **Logs détaillés** : Bouton "Voir les logs" pour plus d'infos
- **Fichiers de logs** : Sauvegardés dans le dossier `logs/`

### Gestion des erreurs
- **Arrêt d'urgence** : Bouton pour stopper l'installation
- **Reprises automatiques** : Continue même si un programme échoue
- **Messages d'erreur clairs** : Explication des problèmes

---

## 🔧 Dépannage

### Problèmes courants

**"Erreur de dépendances"**
- Exécutez : `python install_dependencies.py`
- Ou relancez l'application, elle gère automatiquement

**"Connexion échouée"**
- Vérifiez votre connexion Internet
- Certains antivirus bloquent les téléchargements

**"Installation échouée"**
- Assurez-vous d'avoir les **droits administrateur**
- Fermez les programmes en cours d'utilisation
- Consultez les logs détaillés

**"Interface figée"**
- Normal pendant les téléchargements
- Utilisez le bouton "Arrêter" si besoin

### Solutions rapides
1. **Redémarrez** l'application
2. **Exécutez en tant qu'administrateur**
3. **Désactivez temporairement** l'antivirus
4. **Vérifiez les logs** dans le dossier `logs/`

---

## 📁 Structure des dossiers

```
NiTrite v.2/
├── 📄 nitrite_installer.py    # Application principale
├── 📄 Lancer_NiTrite.bat     # Lanceur rapide
├── 📁 src/                   # Code source
├── 📁 data/                  # Configuration
├── 📁 downloads/             # Téléchargements (temporaire)
├── 📁 logs/                  # Fichiers de logs
└── 📄 README.md              # Documentation complète
```

---

## 🛡️ Sécurité

### Téléchargements sécurisés
- **Sources officielles uniquement** : Pas de sites tiers
- **HTTPS obligatoire** : Connexions chiffrées
- **Vérification d'intégrité** : Contrôle des fichiers

### Installation propre
- **Installations silencieuses** : Pas de logiciels indésirables
- **Paramètres par défaut** : Configurations recommandées
- **Nettoyage automatique** : Suppression des fichiers temporaires

---

## 💡 Conseils d'utilisation

### Pour un usage optimal
1. **Fermez les autres programmes** avant installation
2. **Connectez-vous en tant qu'administrateur** 
3. **Assurez-vous d'avoir de l'espace libre** (au moins 2 GB)
4. **Gardez une connexion Internet stable**

### Configurations recommandées
- **Bureautique** : Firefox + LibreOffice + VLC + 7-Zip
- **Développement** : VS Code + Git + Python + Node.js + Chrome
- **Sécurité** : Malwarebytes + CCleaner + 7-Zip
- **Multimédia** : VLC + Discord + Steam

---

## 🆘 Support

### En cas de problème
1. **Consultez les logs** : Bouton "Voir les logs"
2. **Testez l'application** : `python test_nitrite.py`
3. **Vérifiez la configuration** : Fichiers dans `data/`
4. **Réinstallez les dépendances** : `python install_dependencies.py`

### Informations système
- **OS supportés** : Windows 10, Windows 11
- **Python** : 3.8+ (auto-installé si nécessaire)
- **Droits** : Administrateur recommandé
- **Internet** : Connexion stable requise

---

## 🎉 Profitez de NiTrite v.2 !

Votre nouvel assistant d'installation est prêt à vous faire gagner des heures ! 

**Installation rapide, sécurisée et sans tracas !** 🚀

---

*Développé avec ❤️ pour simplifier votre vie numérique*