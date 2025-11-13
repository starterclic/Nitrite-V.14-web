#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide pour compter les statistiques finales
"""

import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def quick_test():
    """Test rapide des programmes"""
    
    with open('data/programs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total = 0
    winget_count = 0
    url_ok = 0
    warnings = 0
    errors = 0
    
    print("\n🧪 Test rapide des programmes...\n")
    
    for category_name, programs in data.items():
        for prog_name, prog_data in programs.items():
            total += 1
            url = prog_data.get('download_url', '')
            winget_id = prog_data.get('winget_id', '')
            
            if winget_id:
                winget_count += 1
            elif url and url != "winget":
                url_ok += 1
            elif not url or url == "winget":
                if not winget_id:
                    warnings += 1
                    print(f"⚠️  {prog_name:<40} - Pas d'URL ni winget_id")
    
    print(f"\n📊 STATISTIQUES FINALES:")
    print(f"   Total: {total} programmes")
    print(f"   📦 Winget: {winget_count} ({winget_count/total*100:.1f}%)")
    print(f"   ✅ URLs: {url_ok} ({url_ok/total*100:.1f}%)")
    print(f"   ⚠️  Warnings: {warnings} ({warnings/total*100:.1f}%)")
    print(f"\n🏆 Score de qualité: {((winget_count + url_ok)/total*100):.1f}%")

if __name__ == "__main__":
    quick_test()
