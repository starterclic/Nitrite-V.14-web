"""
Test des téléchargements des programmes Outils OrdiPlus
"""
import requests
import json

programs = {
    "Malwarebytes": "https://data-cdn.mbamupdates.com/web/mb4-setup-consumer/MBSetup.exe",
    "AdwCleaner": "https://adwcleaner.malwarebytes.com/adwcleaner?channel=release",
    "Wise Disk Cleaner": "https://downloads.wisecleaner.com/soft/WDCFree.exe",
    "Spybot": "https://download.spybot.info/SpybotSD-2.9.82.0-setup.exe",
    "Adobe Reader": "https://get.adobe.com/reader/download/?installer=Reader_DC_2024_fr_FR.exe&os=Windows%2010&browser_type=KHTML&browser_dist=Chrome&d=McAfee_Security_Scan_Plus_PC1_CPDWN_CDS_BS_&dualoffer=false",
}

print("=" * 80)
print("TEST DES URLs DES PROGRAMMES OUTILS ORDIPLUS")
print("=" * 80)
print()

for name, url in programs.items():
    print(f"📋 {name}")
    print(f"   URL: {url[:80]}...")
    
    try:
        # HEAD request pour vérifier sans télécharger
        response = requests.head(url, allow_redirects=True, timeout=10)
        
        # Si HEAD ne fonctionne pas, essayer GET
        if response.status_code == 405:
            response = requests.get(url, stream=True, timeout=10)
            response.close()
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', 'Unknown')
            content_length = response.headers.get('content-length', '0')
            size_mb = int(content_length) / (1024 * 1024) if content_length != '0' else 0
            
            print(f"   ✅ OK - Type: {content_type}")
            if size_mb > 0:
                print(f"   📦 Taille: {size_mb:.1f} MB")
            
            # Vérifier si c'est bien un exécutable
            if 'application/octet-stream' in content_type or 'application/x-msdownload' in content_type:
                print(f"   ✅ Type correct: Exécutable")
            elif 'text/html' in content_type:
                print(f"   ⚠️  ATTENTION: Page HTML au lieu d'un exécutable!")
                print(f"   URL finale: {response.url}")
            
        elif response.status_code == 302 or response.status_code == 301:
            print(f"   🔄 Redirection vers: {response.headers.get('Location', 'unknown')}")
        else:
            print(f"   ❌ Échec: Code {response.status_code}")
        
    except requests.exceptions.Timeout:
        print(f"   ⏱️  Timeout après 10 secondes")
    except Exception as e:
        print(f"   ❌ Erreur: {type(e).__name__}: {str(e)[:50]}")
    
    print()

print("=" * 80)
print("SUGGESTIONS DE CORRECTIONS")
print("=" * 80)

corrections = {
    "AdwCleaner": {
        "probleme": "URL de redirection, pas un lien direct",
        "solution": "Utiliser l'URL directe ou winget",
        "winget_id": "Malwarebytes.AdwCleaner"
    },
    "Adobe Reader": {
        "probleme": "URL complexe avec paramètres",
        "solution": "Utiliser winget",
        "winget_id": "Adobe.Acrobat.Reader.64-bit"
    }
}

for prog, info in corrections.items():
    print(f"\n{prog}:")
    print(f"  ❌ Problème: {info['probleme']}")
    print(f"  ✅ Solution: {info['solution']}")
    if 'winget_id' in info:
        print(f"  📦 Winget ID: {info['winget_id']}")
