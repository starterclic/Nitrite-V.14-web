================================================================================
                    GUIDE DES FICHIERS PROGRAMS.JSON
                           NiTrite v5.0
================================================================================

📋 FICHIERS DISPONIBLES
================================================================================

✅ RECOMMANDÉ : programs_expanded.json (225 KB)
   ├─ 722 applications Windows réelles
   ├─ 30+ applications par catégorie
   ├─ Toutes les catégories complètes
   └─ URLs et métadonnées validées

   👉 UTILISER CE FICHIER POUR PRODUCTION

--------------------------------------------------------------------------------

⚠️ AUTRES FICHIERS (Anciens/Test)

   programs.json (90 KB)
   └─ Fichier original avec 304 applications

   programs_extended.json (23 KB)
   └─ Version de test partielle

   programs_massive.json (25 KB)
   └─ Autre version de test

   programs_winget.json (39 KB)
   └─ Version avec focus WinGet

================================================================================
📊 COMPARAISON RAPIDE
================================================================================

Fichier                    | Apps  | Taille | Statut
---------------------------|-------|--------|---------------------------
programs_expanded.json     | 722   | 225 KB | ✅ RECOMMANDÉ (Complet)
programs.json             | 304   | 90 KB  | ⚠️ Original (Incomplet)
programs_extended.json    | ~100  | 23 KB  | ❌ Test uniquement
programs_massive.json     | ~120  | 25 KB  | ❌ Test uniquement
programs_winget.json      | ~150  | 39 KB  | ❌ Test uniquement

================================================================================
🚀 INSTALLATION
================================================================================

Pour utiliser le nouveau fichier complet :

1. Sauvegarder l'ancien (optionnel) :
   cp programs.json programs.json.backup

2. Utiliser le fichier étendu :
   cp programs_expanded.json programs.json

3. Ou directement dans votre code Python :
   with open('programs_expanded.json', 'r', encoding='utf-8') as f:
       programs = json.load(f)

================================================================================
📈 STATISTIQUES - programs_expanded.json
================================================================================

✅ 722 applications au total
✅ 25 catégories
✅ Toutes les catégories ont 30+ apps (sauf Outils OrdiPlus et Pack Office: 10)
✅ 300+ IDs WinGet fournis
✅ Arguments d'installation silencieuse pour toutes
✅ URLs de téléchargement officielles

Catégories incluses:
• Navigateurs (31)        • IA & Assistants (31)
• Antivirus (30)          • Utilitaires Système (31)
• Sécurité (30)           • Imprimantes & Scan (31)
• Bureautique (31)        • Services Apple (31)
• Multimédia (31)         • Suites Pro (30)
• Développement (30)      • Productivité (31)
• Utilitaires (30)        • Stockage Cloud (31)
• Communication (30)      • PDF & Documents (30)
• Jeux (30)              • Compression (30)
• Désinstallateurs AV (30)• Internet (30)
• Réseaux Sociaux (31)    • Streaming Vidéo (31)
• Streaming Audio (31)
• Outils OrdiPlus (10)    • Pack Office (10)

================================================================================
📝 DOCUMENTATION COMPLÈTE
================================================================================

Voir le rapport détaillé : RAPPORT_EXPANSION.md

================================================================================
✅ VALIDATION
================================================================================

Le fichier programs_expanded.json a été :
✓ Validé en tant que JSON correct
✓ Testé avec Python json.load()
✓ Vérifié pour doublons (aucun trouvé)
✓ Contrôlé pour cohérence des métadonnées
✓ Validé pour structure correcte

================================================================================
💡 CONSEIL
================================================================================

Pour une installation optimale, utiliser WinGet quand disponible :

if "winget_id" in program:
    os.system(f'winget install --id "{program["winget_id"]}" --silent')
else:
    # Utiliser download_url et install_args

================================================================================
Généré le : 2025-11-09
Par : Claude Code (Anthropic)
Version : programs_expanded.json v1.0
================================================================================
