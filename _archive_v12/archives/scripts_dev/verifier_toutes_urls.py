"""
Vérification de TOUTES les URLs de téléchargement dans programs.json
"""
import json
import requests
from urllib.parse import urlparse
import time

def verifier_url(url, nom_programme, timeout=10):
    """Vérifie si une URL est accessible"""
    if not url:
        return "❌ VIDE", "Pas d'URL de téléchargement"
    
    try:
        # HEAD request d'abord (plus rapide)
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        
        # Si HEAD ne fonctionne pas, essayer GET
        if response.status_code == 405:
            response = requests.get(url, stream=True, timeout=timeout)
            response.close()
        
        if response.status_code == 200:
            content_length = response.headers.get('content-length', 'Inconnu')
            if content_length != 'Inconnu':
                size_mb = int(content_length) / (1024 * 1024)
                return "✅ OK", f"{response.status_code} - {size_mb:.1f} MB"
            return "✅ OK", f"{response.status_code}"
        elif response.status_code == 404:
            return "❌ 404", "Page non trouvée"
        elif response.status_code == 403:
            return "⚠️ 403", "Accès interdit (peut fonctionner dans le navigateur)"
        elif response.status_code == 302 or response.status_code == 301:
            return "✅ OK", f"Redirection {response.status_code} vers {response.headers.get('Location', 'inconnu')}"
        else:
            return f"⚠️ {response.status_code}", f"Code HTTP {response.status_code}"
    
    except requests.exceptions.SSLError:
        return "⚠️ SSL", "Erreur SSL (peut fonctionner avec navigateur)"
    except requests.exceptions.Timeout:
        return "⚠️ TIMEOUT", f"Timeout après {timeout}s"
    except requests.exceptions.ConnectionError as e:
        return "❌ ERREUR", f"Erreur de connexion: {str(e)[:50]}"
    except Exception as e:
        return "❌ ERREUR", f"{type(e).__name__}: {str(e)[:50]}"

def main():
    print("=" * 80)
    print("🔍 VÉRIFICATION DE TOUTES LES URLs DE TÉLÉCHARGEMENT")
    print("=" * 80)
    print()
    
    # Charger programs.json
    with open('data/programs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Aplatir la structure (dictionnaire de catégories -> liste de programmes)
    programmes = []
    for categorie, progs in data.items():
        for nom, details in progs.items():
            prog_info = details.copy()
            prog_info['name'] = nom
            prog_info['category'] = categorie
            programmes.append(prog_info)
    
    print(f"📊 Total de programmes: {len(programmes)}\n")
    
    # Statistiques
    stats = {
        'total': 0,
        'ok': 0,
        'erreur': 0,
        'avertissement': 0,
        'vide': 0,
        'winget_only': 0
    }
    
    # Programmes avec erreurs
    erreurs = []
    avertissements = []
    
    # Vérifier chaque programme
    for i, prog in enumerate(programmes, 1):
        nom = prog.get('name', 'SANS NOM')
        categorie = prog.get('category', 'SANS CATÉGORIE')
        url = prog.get('download_url', '')
        winget_id = prog.get('winget_id', '')
        
        stats['total'] += 1
        
        # Si pas d'URL mais winget_id
        if not url and winget_id:
            stats['winget_only'] += 1
            print(f"{i:3}. [WINGET ONLY] {nom} ({categorie})")
            print(f"     winget_id: {winget_id}")
            print()
            continue
        
        # Vérifier l'URL
        print(f"{i:3}. Vérification: {nom}")
        print(f"     Catégorie: {categorie}")
        print(f"     URL: {url[:80]}{'...' if len(url) > 80 else ''}")
        
        statut, details = verifier_url(url, nom)
        
        print(f"     {statut} - {details}")
        print()
        
        # Mettre à jour les statistiques
        if statut.startswith("✅"):
            stats['ok'] += 1
        elif statut.startswith("❌"):
            if "VIDE" in statut:
                stats['vide'] += 1
            else:
                stats['erreur'] += 1
                erreurs.append({
                    'nom': nom,
                    'categorie': categorie,
                    'url': url,
                    'statut': statut,
                    'details': details
                })
        elif statut.startswith("⚠️"):
            stats['avertissement'] += 1
            avertissements.append({
                'nom': nom,
                'categorie': categorie,
                'url': url,
                'statut': statut,
                'details': details
            })
        
        # Pause pour éviter de surcharger les serveurs
        if i % 10 == 0:
            time.sleep(1)
    
    # Afficher le résumé
    print("=" * 80)
    print("📊 RÉSUMÉ DES VÉRIFICATIONS")
    print("=" * 80)
    print(f"Total de programmes: {stats['total']}")
    if stats['total'] > 0:
        print(f"✅ URLs OK: {stats['ok']} ({stats['ok']*100/stats['total']:.1f}%)")
        print(f"❌ URLs en erreur: {stats['erreur']} ({stats['erreur']*100/stats['total']:.1f}%)")
        print(f"⚠️  URLs avec avertissement: {stats['avertissement']} ({stats['avertissement']*100/stats['total']:.1f}%)")
        print(f"📦 Winget uniquement: {stats['winget_only']} ({stats['winget_only']*100/stats['total']:.1f}%)")
        print(f"⭕ URLs vides: {stats['vide']} ({stats['vide']*100/stats['total']:.1f}%)")
    print()
    
    # Détail des erreurs
    if erreurs:
        print("=" * 80)
        print(f"❌ PROGRAMMES AVEC ERREURS ({len(erreurs)})")
        print("=" * 80)
        for err in erreurs:
            print(f"\n{err['nom']} ({err['categorie']})")
            print(f"  URL: {err['url'][:100]}{'...' if len(err['url']) > 100 else ''}")
            print(f"  {err['statut']} - {err['details']}")
    
    # Détail des avertissements
    if avertissements:
        print("\n" + "=" * 80)
        print(f"⚠️  PROGRAMMES AVEC AVERTISSEMENTS ({len(avertissements)})")
        print("=" * 80)
        for warn in avertissements:
            print(f"\n{warn['nom']} ({warn['categorie']})")
            print(f"  URL: {warn['url'][:100]}{'...' if len(warn['url']) > 100 else ''}")
            print(f"  {warn['statut']} - {warn['details']}")
    
    print("\n" + "=" * 80)
    print("✅ Vérification terminée!")
    print("=" * 80)

if __name__ == "__main__":
    main()
