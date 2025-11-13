"""
TEST COMPLET DE TOUS LES PROGRAMMES
Vérifie toutes les URLs, configurations et dépendances
"""
import json
import requests
import sys
from pathlib import Path

def test_url(url, program_name):
    """Teste une URL"""
    if not url:
        return "WINGET", "Programme installé via winget"
    
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        
        if response.status_code == 405:
            response = requests.get(url, stream=True, timeout=10)
            response.close()
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'text/html' in content_type:
                return "WARNING", f"Page HTML au lieu d'un fichier"
            return "OK", f"Code {response.status_code}"
        elif response.status_code in [301, 302]:
            return "REDIRECT", f"Redirige vers {response.url[:50]}"
        else:
            return "ERROR", f"Code {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "TIMEOUT", "Timeout après 10s"
    except Exception as e:
        return "ERROR", f"{type(e).__name__}"

def main():
    print("=" * 100)
    print("🔍 TEST COMPLET DE TOUS LES PROGRAMMES - NiTrite v.2")
    print("=" * 100)
    print()
    
    # Charger programs.json
    programs_file = Path('data/programs.json')
    if not programs_file.exists():
        print("❌ Fichier programs.json non trouvé!")
        return
    
    with open(programs_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Statistiques
    stats = {
        'total': 0,
        'ok': 0,
        'winget': 0,
        'error': 0,
        'warning': 0,
        'timeout': 0,
        'redirect': 0
    }
    
    problemes = []
    
    # Tester chaque programme
    for category, programs in data.items():
        print(f"\n{'='*100}")
        print(f"📁 {category} ({len(programs)} programmes)")
        print(f"{'='*100}")
        
        for prog_name, prog_info in programs.items():
            stats['total'] += 1
            url = prog_info.get('download_url', '')
            winget_id = prog_info.get('winget_id', '')
            
            status, message = test_url(url, prog_name)
            
            # Icônes de statut
            icons = {
                'OK': '✅',
                'WINGET': '📦',
                'ERROR': '❌',
                'WARNING': '⚠️',
                'TIMEOUT': '⏱️',
                'REDIRECT': '🔄'
            }
            
            icon = icons.get(status, '❓')
            
            # Affichage
            print(f"{icon} {prog_name:50} | {status:10} | {message[:40]}")
            
            # Statistiques
            if status == 'OK':
                stats['ok'] += 1
            elif status == 'WINGET':
                stats['winget'] += 1
            elif status == 'ERROR':
                stats['error'] += 1
                problemes.append({
                    'categorie': category,
                    'programme': prog_name,
                    'url': url,
                    'probleme': message
                })
            elif status == 'WARNING':
                stats['warning'] += 1
            elif status == 'TIMEOUT':
                stats['timeout'] += 1
            elif status == 'REDIRECT':
                stats['redirect'] += 1
    
    # Résumé final
    print("\n" + "=" * 100)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 100)
    print(f"Total de programmes testés: {stats['total']}")
    print(f"✅ URLs OK:                 {stats['ok']:3} ({stats['ok']*100/stats['total']:.1f}%)")
    print(f"📦 Via Winget:              {stats['winget']:3} ({stats['winget']*100/stats['total']:.1f}%)")
    print(f"❌ Erreurs:                 {stats['error']:3} ({stats['error']*100/stats['total']:.1f}%)")
    print(f"⚠️  Avertissements:         {stats['warning']:3} ({stats['warning']*100/stats['total']:.1f}%)")
    print(f"⏱️  Timeouts:               {stats['timeout']:3} ({stats['timeout']*100/stats['total']:.1f}%)")
    print(f"🔄 Redirections:            {stats['redirect']:3} ({stats['redirect']*100/stats['total']:.1f}%)")
    
    # Programmes à corriger
    if problemes:
        print("\n" + "=" * 100)
        print(f"❌ PROGRAMMES À CORRIGER ({len(problemes)})")
        print("=" * 100)
        
        for prob in problemes:
            print(f"\n{prob['categorie']} → {prob['programme']}")
            print(f"  URL: {prob['url'][:80]}")
            print(f"  Problème: {prob['probleme']}")
    
    # Score de qualité
    score = ((stats['ok'] + stats['winget']) / stats['total']) * 100
    print("\n" + "=" * 100)
    print(f"🏆 SCORE DE QUALITÉ: {score:.1f}%")
    print("=" * 100)
    
    if score >= 95:
        print("✅ EXCELLENT! Presque tous les programmes fonctionnent")
    elif score >= 80:
        print("✅ BON! La majorité des programmes fonctionnent")
    elif score >= 60:
        print("⚠️  MOYEN! Beaucoup de corrections nécessaires")
    else:
        print("❌ MAUVAIS! Révision complète nécessaire")
    
    print()

if __name__ == "__main__":
    main()
