#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction des 23 avertissements (pages HTML au lieu de fichiers)
- Basculer vers winget pour les programmes disponibles
- Corriger les URLs pour les autres
"""

import json
from datetime import datetime

def corriger_warnings():
    """Corrige les 23 programmes avec des warnings (pages HTML)"""
    
    # Charger les programmes
    with open('data/programs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Sauvegarder l'original
    backup_name = f"data/programs.json.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(backup_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    corrections = 0
    
    print("\n" + "="*80)
    print("          🔧 CORRECTION DES 23 AVERTISSEMENTS (HTML)          ")
    print("="*80 + "\n")
    
    # Liste des programmes à corriger avec leurs solutions
    # Basé sur les résultats du test complet
    corrections_map = {
        # Sécurité - Antivirus Uninstallers
        "AVAST Uninstall Utility": ("Avast.Avast", None),
        "AVG Remover": ("AVG.AntiVirusFree", None),
        
        # Développement
        "Postman": ("Postman.Postman", None),
        "Insomnia": ("Insomnia.Insomnia", None),
        
        # Multimédia
        "Spotify": ("Spotify.Spotify", None),
        "AIMP": ("AIMP.AIMP", None),
        "Foobar2000": ("PeterPawlowski.foobar2000", None),  # Nom avec majuscule
        
        # Utilitaires
        "CPU-Z": ("CPUID.CPU-Z", None),
        "GPU-Z": ("TechPowerUp.GPU-Z", None),
        "HWMonitor": ("CPUID.HWMonitor", None),
        "Ventoy": ("Ventoy.Ventoy", None),
        
        # Internet
        "JDownloader": ("AppWork.JDownloader", None),
        
        # Productivité
        "Asana": ("Asana.Asana", None),
        
        # Stockage Cloud
        "pCloud Drive": ("pCloud.pCloudDrive", None),
        "Sync.com": ("Sync.Sync", None),
        
        # IA & Assistants
        "Stable Diffusion WebUI": ("", "Projet GitHub complexe"),
        
        # Compression
        "FreeArc": ("", "Archiveur obsolète"),
        
        # Jeux
        "Overwolf": ("Overwolf.Overwolf", None),
        
        # Utilitaires Système
        "CrystalDiskInfo": ("CrystalDewWorld.CrystalDiskInfo", None),
        "CrystalDiskMark": ("CrystalDewWorld.CrystalDiskMark", None),
        "MSI Afterburner": ("Guru3D.Afterburner", None),
        "Balena Etcher": ("Balena.Etcher", None),
    }
    
    # Parcourir toutes les catégories
    for category_name, programs in data.items():
        programmes_a_retirer = []
        
        for prog_name in list(programs.keys()):
            prog_data = programs[prog_name]
            
            if prog_name in corrections_map:
                winget_id, note = corrections_map[prog_name]
                
                if winget_id:
                    # Basculer vers winget
                    prog_data['download_url'] = ""
                    prog_data['winget_id'] = winget_id
                    prog_data['admin_required'] = prog_data.get('admin_required', False)
                    print(f"✅ {prog_name:<40} → Winget: {winget_id}")
                    corrections += 1
                else:
                    # Retirer le programme
                    programmes_a_retirer.append(prog_name)
                    note_str = f" ({note})" if note else ""
                    print(f"🗑️  {prog_name:<40} → RETIRÉ{note_str}")
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
    
    programmes_winget = sum(1 for winget_id, _ in corrections_map.values() if winget_id)
    programmes_retires = sum(1 for winget_id, _ in corrections_map.values() if not winget_id)
    
    print("\n📋 RÉSUMÉ:")
    print(f"   • {programmes_winget} programmes basculés vers winget")
    print(f"   • {programmes_retires} programmes retirés (obsolètes)")
    print(f"\n🔄 Reconstruisez le package: python build_portable_complet.py")

if __name__ == "__main__":
    corriger_warnings()
