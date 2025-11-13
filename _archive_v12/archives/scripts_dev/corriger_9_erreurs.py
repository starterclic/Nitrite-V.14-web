#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction des 9 programmes en erreur
- Basculer vers winget pour les programmes disponibles
- Retirer les programmes obsolètes
"""

import json
from datetime import datetime

def corriger_programmes_erreurs():
    """Corrige les 9 programmes identifiés avec des erreurs"""
    
    # Charger les programmes
    with open('data/programs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Sauvegarder l'original
    backup_name = f"data/programs.json.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(backup_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    corrections = 0
    programmes_retires = []
    
    print("\n" + "="*80)
    print("          🔧 CORRECTION DES 9 PROGRAMMES EN ERREUR          ")
    print("="*80 + "\n")
    
    # Parcourir toutes les catégories
    for category_name, programs in data.items():
        programmes_a_retirer = []
        
        for prog_name in list(programs.keys()):
            prog_data = programs[prog_name]
            
            # 1. COMODO FIREWALL - Basculer vers winget
            if prog_name == "Comodo Firewall":
                prog_data['download_url'] = ""
                prog_data['winget_id'] = "COMODO.ComodoFirewall"
                prog_data['admin_required'] = True
                print(f"✅ {prog_name:<30} → Winget: {prog_data['winget_id']}")
                corrections += 1
            
            # 2. EVERNOTE - Basculer vers winget
            elif prog_name == "Evernote":
                prog_data['download_url'] = ""
                prog_data['winget_id'] = "evernote.evernote"
                prog_data['admin_required'] = False
                print(f"✅ {prog_name:<30} → Winget: {prog_data['winget_id']}")
                corrections += 1
            
            # 3. AUDACITY - Basculer vers winget
            elif prog_name == "Audacity":
                prog_data['download_url'] = ""
                prog_data['winget_id'] = "Audacity.Audacity"
                prog_data['admin_required'] = False
                print(f"✅ {prog_name:<30} → Winget: {prog_data['winget_id']}")
                corrections += 1
            
            # 4. HWINFO64 - Basculer vers winget
            elif prog_name == "HWiNFO64":
                prog_data['download_url'] = ""
                prog_data['winget_id'] = "REALiX.HWiNFO"
                prog_data['admin_required'] = False
                print(f"✅ {prog_name:<30} → Winget: {prog_data['winget_id']}")
                corrections += 1
            
            # 5. BITDEFENDER UNINSTALL TOOL - Basculer vers winget
            elif prog_name == "Bitdefender Uninstall Tool":
                prog_data['download_url'] = ""
                prog_data['winget_id'] = "Bitdefender.Bitdefender"
                prog_data['admin_required'] = True
                print(f"✅ {prog_name:<30} → Winget: {prog_data['winget_id']}")
                corrections += 1
            
            # 6. MALWAREBYTES SUPPORT TOOL - Basculer vers Malwarebytes principal
            elif prog_name == "Malwarebytes Support Tool":
                prog_data['download_url'] = ""
                prog_data['winget_id'] = "Malwarebytes.Malwarebytes"
                prog_data['admin_required'] = True
                print(f"✅ {prog_name:<30} → Winget: {prog_data['winget_id']}")
                corrections += 1
            
            # 7. INTERNET DOWNLOAD MANAGER - Basculer vers winget
            elif prog_name == "Internet Download Manager":
                prog_data['download_url'] = ""
                prog_data['winget_id'] = "Tonec.InternetDownloadManager"
                prog_data['admin_required'] = False
                print(f"✅ {prog_name:<30} → Winget: {prog_data['winget_id']}")
                corrections += 1
            
            # 8. CANON IJ SCAN UTILITY - Retirer (page web, pas de programme)
            elif prog_name == "Canon IJ Scan Utility":
                programmes_a_retirer.append(prog_name)
                programmes_retires.append(prog_name)
                print(f"🗑️  {prog_name:<30} → RETIRÉ (page web)")
                corrections += 1
            
            # 9. KGB ARCHIVER - Retirer (obsolète, SSL invalide)
            elif prog_name == "KGB Archiver":
                programmes_a_retirer.append(prog_name)
                programmes_retires.append(prog_name)
                print(f"🗑️  {prog_name:<30} → RETIRÉ (obsolète)")
                corrections += 1
        
        # Retirer les programmes marqués pour suppression
        for prog_name in programmes_a_retirer:
            del programs[prog_name]
    
    # Sauvegarder les modifications
    with open('data/programs.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Sauvegarde: {backup_name}")
    
    print("\n" + "="*80)
    print(f"          ✅ {corrections} CORRECTIONS APPLIQUÉES          ")
    print("="*80)
    
    print("\n📋 RÉSUMÉ:")
    print(f"   • 7 programmes basculés vers winget")
    print(f"   • {len(programmes_retires)} programmes retirés: {', '.join(programmes_retires)}")
    print(f"\n🔄 Reconstruisez le package: python build_portable_complet.py")

if __name__ == "__main__":
    corriger_programmes_erreurs()
