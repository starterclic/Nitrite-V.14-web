#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Identifier les programmes avec warnings (HTML au lieu de fichiers)
"""

import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def test_url_is_html(url, timeout=10):
    """Teste si une URL renvoie du HTML"""
    if not url or url == "winget":
        return False, "WINGET"
    
    try:
        session = requests.Session()
        retry = Retry(total=2, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        response = session.head(url, timeout=timeout, allow_redirects=True)
        content_type = response.headers.get('Content-Type', '').lower()
        
        if 'text/html' in content_type:
            return True, "HTML"
        return False, "OK"
    except:
        return False, "ERROR"

def identifier_warnings():
    """Identifie tous les programmes avec des warnings"""
    
    with open('data/programs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    warnings = []
    
    print("\n🔍 Recherche des programmes avec HTML au lieu de fichiers...\n")
    
    for category_name, programs in data.items():
        for prog_name, prog_data in programs.items():
            url = prog_data.get('download_url', '')
            
            if url and url != "winget":
                is_html, status = test_url_is_html(url)
                if is_html:
                    warnings.append({
                        'name': prog_name,
                        'category': category_name,
                        'url': url
                    })
                    print(f"⚠️  {prog_name:<40} [{category_name}]")
    
    print(f"\n📊 Total: {len(warnings)} programmes avec warnings\n")
    
    # Sauvegarder la liste
    with open('warnings_list.json', 'w', encoding='utf-8') as f:
        json.dump(warnings, f, ensure_ascii=False, indent=2)
    
    print("💾 Liste sauvegardée: warnings_list.json")
    return warnings

if __name__ == "__main__":
    identifier_warnings()
