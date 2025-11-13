"""
Analyseur d'URLs pour identifier les problèmes de téléchargement
"""

import json
import requests
from pathlib import Path
import logging
import sys
from urllib.parse import urlparse

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def check_url_status(url, timeout=10):
    """Vérifie le statut d'une URL"""
    if not url or url.strip() == "":
        return False, "URL vide"
    
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code == 200:
            return True, f"OK ({response.status_code})"
        elif response.status_code in [301, 302, 307, 308]:
            return True, f"Redirection ({response.status_code}) -> {response.headers.get('Location', 'N/A')}"
        else:
            return False, f"Erreur HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except requests.exceptions.ConnectionError:
        return False, "Erreur de connexion"
    except requests.exceptions.RequestException as e:
        return False, f"Erreur requête: {str(e)}"
    except Exception as e:
        return False, f"Erreur inconnue: {str(e)}"

def analyze_programs_json():
    """Analyse le fichier programs.json pour identifier les URLs problématiques"""
    programs_file = Path(__file__).parent / 'data' / 'programs.json'
    
    if not programs_file.exists():
        logger.error(f"Fichier non trouvé: {programs_file}")
        return
    
    with open(programs_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_programs = 0
    broken_urls = []
    empty_urls = []
    working_urls = []
    
    logger.info("🔍 Analyse des URLs en cours...")
    
    for category, programs in data.items():
        if not isinstance(programs, dict):
            continue
            
        logger.info(f"\n📂 Catégorie: {category}")
        
        for program_name, program_info in programs.items():
            total_programs += 1
            download_url = program_info.get('download_url', '')
            
            if not download_url or download_url.strip() == "":
                empty_urls.append({
                    'program': program_name,
                    'category': category,
                    'has_winget': 'winget_id' in program_info
                })
                logger.warning(f"  ❌ {program_name}: URL vide")
                continue
            
            # Vérifier l'URL
            is_working, status = check_url_status(download_url)
            
            if is_working:
                working_urls.append({
                    'program': program_name,
                    'category': category,
                    'url': download_url,
                    'status': status
                })
                logger.info(f"  ✅ {program_name}: {status}")
            else:
                broken_urls.append({
                    'program': program_name,
                    'category': category,
                    'url': download_url,
                    'error': status,
                    'has_winget': 'winget_id' in program_info
                })
                logger.error(f"  ❌ {program_name}: {status}")
    
    # Générer le rapport
    logger.info("\n" + "="*80)
    logger.info("📊 RAPPORT D'ANALYSE")
    logger.info("="*80)
    logger.info(f"Total programmes analysés: {total_programs}")
    logger.info(f"URLs fonctionnelles: {len(working_urls)} ({len(working_urls)/total_programs*100:.1f}%)")
    logger.info(f"URLs cassées: {len(broken_urls)} ({len(broken_urls)/total_programs*100:.1f}%)")
    logger.info(f"URLs vides: {len(empty_urls)} ({len(empty_urls)/total_programs*100:.1f}%)")
    
    # Détail des URLs cassées
    if broken_urls:
        logger.info("\n🔴 URLs CASSÉES:")
        for item in broken_urls:
            winget_info = " (winget disponible)" if item['has_winget'] else ""
            logger.info(f"  - {item['program']} ({item['category']}): {item['error']}{winget_info}")
    
    # Détail des URLs vides
    if empty_urls:
        logger.info("\n⚪ URLs VIDES:")
        for item in empty_urls:
            winget_info = " (winget disponible)" if item['has_winget'] else ""
            logger.info(f"  - {item['program']} ({item['category']}){winget_info}")
    
    # Sauvegarder le rapport
    report = {
        'total_programs': total_programs,
        'working_urls': len(working_urls),
        'broken_urls': broken_urls,
        'empty_urls': empty_urls,
        'working_urls_list': working_urls
    }
    
    report_file = Path(__file__).parent / 'logs' / 'url_analysis_report.json'
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n📝 Rapport sauvegardé: {report_file}")
    
    return report

if __name__ == "__main__":
    try:
        report = analyze_programs_json()
        
        # Suggestion d'améliorations
        broken_count = len(report['broken_urls'])
        empty_count = len(report['empty_urls'])
        
        if broken_count > 0 or empty_count > 0:
            logger.info("\n💡 RECOMMANDATIONS:")
            if broken_count > 0:
                logger.info(f"1. Mettre à jour {broken_count} URLs cassées")
            if empty_count > 0:
                logger.info(f"2. Ajouter des URLs pour {empty_count} programmes sans URL")
            logger.info("3. Utiliser winget comme alternative pour les programmes supportés")
            logger.info("4. Implémenter un système de fallback automatique")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()