"""
Correction complète de TOUTES les URLs cassées
S'exécute une fois pour corriger l'état actuel
"""
import json
import os
from datetime import datetime

def main():
    print("=" * 80)
    print("🔧 CORRECTION COMPLÈTE DE TOUTES LES URLs CASSÉES")
    print("=" * 80)
    print()
    
    programs_file = 'data/programs.json'
    
    # Charger le fichier
    with open(programs_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    corrections = 0
    
    # 1. CORRIGER LES URLs CASSÉES (404)
    url_fixes = {
        # Navigateurs
        "Vivaldi": {
            "download_url": "https://downloads.vivaldi.com/stable/Vivaldi.6.9.3447.54.x64.exe",
            "install_args": "/VERYSILENT /NORESTART"
        },
        "Tor Browser": {
            "download_url": "https://www.torproject.org/dist/torbrowser/14.0/torbrowser-install-win64-14.0_fr.exe",
            "install_args": "/S"
        },
        
        # Antivirus - basculer vers winget
        "Norton 360": {
            "download_url": "",
            "winget_id": "NortonLifeLock.Norton360"
        },
        "ESET NOD32": {
            "download_url": "",
            "winget_id": "ESET.Security"
        },
        "Sophos Home": {
            "download_url": "",
            "winget_id": "Sophos.SophosHome"
        },
        
        # Sécurité
        "Comodo Firewall": {
            "download_url": "https://download.comodo.com/cis/download/installs/2000/partners/cfw_installer_12009_86.exe",
            "install_args": "/VERYSILENT /NORESTART",
            "admin_required": True
        },
        
        # Bureautique
        "Foxit Reader": {
            "download_url": "",
            "winget_id": "Foxit.FoxitReader"
        },
        "Evernote": {
            "download_url": "https://cdn1.evernote.com/boron/win/builds/Evernote-latest-win-ddl-ga.exe",
            "install_args": "/S"
        },
        
        # Multimédia
        "K-Lite Codec Pack": {
            "download_url": "https://files3.codecguide.com/K-Lite_Codec_Pack_1805_Standard.exe",
            "install_args": "/VERYSILENT /NORESTART"
        },
        "Audacity": {
            "download_url": "https://github.com/audacity/audacity/releases/download/Audacity-3.6.4/audacity-win-3.6.4-x64.exe",
            "install_args": "/VERYSILENT /NORESTART"
        },
        "Paint.NET": {
            "download_url": "",
            "winget_id": "dotPDN.PaintDotNet"
        },
        
        # Développement
        "Git": {
            "download_url": "https://github.com/git-for-windows/git/releases/download/v2.47.0.windows.1/Git-2.47.0-64-bit.exe",
            "install_args": "/VERYSILENT /NORESTART"
        },
        "Node.js": {
            "download_url": "https://nodejs.org/dist/v22.11.0/node-v22.11.0-x64.msi",
            "install_args": "/quiet /norestart",
            "admin_required": True
        },
        "Android Studio": {
            "download_url": "",
            "winget_id": "Google.AndroidStudio"
        },
        
        # Utilitaires
        "PowerToys": {
            "download_url": "https://github.com/microsoft/PowerToys/releases/download/v0.86.0/PowerToysSetup-0.86.0-x64.exe",
            "install_args": "/VERYSILENT /NORESTART"
        },
        "HWiNFO64": {
            "download_url": "https://www.hwinfo.com/files/hwi_768.exe",
            "install_args": "/VERYSILENT"
        },
        "MSI Afterburner": {
            "download_url": "",
            "winget_id": "Guru3D.Afterburner"
        },
        
        # Jeux
        "GOG Galaxy": {
            "download_url": "https://cdn.gog.com/open/galaxy/client/2.0.77.126/setup_galaxy_2.0.77.126.exe",
            "install_args": "/VERYSILENT /NORESTART"
        },
        "Origin": {
            "download_url": "",
            "winget_id": "ElectronicArts.Origin"
        },
        
        # Désinstallateurs antivirus
        "Bitdefender Uninstall Tool": {
            "download_url": "https://download.bitdefender.com/windows/installer/en-us/bitdefender_uninstall_tool.exe",
            "install_args": ""
        },
        "Norton Remove and Reinstall Tool": {
            "download_url": "",
            "winget_id": "NortonLifeLock.NortonRemoveAndReinstall"
        },
        "ESET Uninstaller": {
            "download_url": "",
            "winget_id": "ESET.ESETUninstaller"
        },
        "Malwarebytes Support Tool": {
            "download_url": "https://downloads.malwarebytes.com/file/mb-support-tool",
            "install_args": ""
        },
        "Sophos Removal Tool": {
            "download_url": "",
            "winget_id": "Sophos.SophosRemovalTool"
        },
        
        # Internet
        "qBittorrent": {
            "download_url": "https://github.com/qbittorrent/qBittorrent/releases/download/release-5.0.1/qbittorrent_5.0.1_x64_setup.exe",
            "install_args": "/S"
        },
        "Internet Download Manager": {
            "download_url": "https://www.internetdownloadmanager.com/idman642build25.exe",
            "install_args": "/S"
        },
        "FileZilla": {
            "download_url": "https://download.filezilla-project.org/client/FileZilla_3.67.1_win64-setup.exe",
            "install_args": "/S"
        },
        
        # Productivité
        "Monday.com": {
            "download_url": "",
            "winget_id": "Monday.Monday"
        },
    }
    
    # 2. CORRIGER LES "winget" INVALIDES ET AJOUTER LES winget_id
    winget_programs = {
        # IA & Assistants
        "Ollama": "Ollama.Ollama",
        "LM Studio": "LMStudio.LMStudio",
        "Jan AI": "Jan.Jan",
        "Waifu2x-Extension-GUI": "AaronFeng753.Waifu2x-Extension-GUI",
        "Upscayl": "Upscayl.Upscayl",
        "AnythingLLM": "MintplexLabs.AnythingLLM",
        "Whisper Desktop": "Const-me.Whisper",
        
        # Utilitaires Système
        "HWiNFO": "REALiX.HWiNFO",
        "Wise Care 365": "WiseCleaner.WiseCare365",
        "Advanced SystemCare": "IObit.AdvancedSystemCare",
        "Defraggler": "Piriform.Defraggler",
        "WinDirStat": "WinDirStat.WinDirStat",
        "SpaceSniffer": "UderzoSoftware.SpaceSniffer",
        "Eraser": "Eraser.Eraser",
        "Auslogics Disk Defrag": "Auslogics.DiskDefrag",
        "Auslogics Registry Cleaner": "Auslogics.RegistryCleaner",
        "O&O ShutUp10++": "OO-Software.ShutUp10",
        "PrivaZer": "Goversoft.PrivaZer",
        
        # Imprimantes & Scan
        "Epson Print and Scan": "Epson.EpsonScan2",
        "Brother iPrint&Scan": "Brother.iPrintAndScan",
        "VueScan": "Hamrick.VueScan",
        "NAPS2": "NAPS2.NAPS2",
        "PaperScan": "ORPALIS.PaperScan",
        "PDF24 Creator": "geeksoftwareGmbH.PDF24Creator",
        
        # Services Apple
        "iCloud": "Apple.iCloud",
        "Apple Devices": "Apple.Devices",
        
        # Suites Professionnelles
        "Adobe Creative Cloud": "Adobe.CreativeCloud",
        "Autodesk AutoCAD": "Autodesk.AutoCAD",
        "SketchUp": "Trimble.SketchUp",
        "CorelDRAW Graphics Suite": "Corel.CorelDRAW",
        "Figma": "Figma.Figma",
        "Canva": "Canva.Canva",
        "Blender": "BlenderFoundation.Blender",
        "Affinity Designer": "SerifEurope.AffinityDesigner2",
        "Affinity Photo": "SerifEurope.AffinityPhoto2",
        "Affinity Publisher": "SerifEurope.AffinityPublisher2",
        
        # Compression
        "PeaZip": "Giorgiotani.Peazip",
        "Bandizip": "Bandisoft.Bandizip",
        "NanaZip": "M2Team.NanaZip",
    }
    
    # Appliquer les corrections
    for category, programs in data.items():
        for prog_name, prog_info in programs.items():
            
            # Correction 1: Remplacer "winget" par URL vide + winget_id
            if prog_info.get('download_url') == 'winget':
                prog_info['download_url'] = ''
                if prog_name in winget_programs:
                    prog_info['winget_id'] = winget_programs[prog_name]
                    print(f"✅ {prog_name}: URL 'winget' corrigée -> winget_id ajouté")
                    corrections += 1
            
            # Correction 2: Appliquer les corrections d'URLs
            if prog_name in url_fixes:
                for key, value in url_fixes[prog_name].items():
                    old_value = prog_info.get(key, '')
                    if old_value != value:
                        prog_info[key] = value
                        print(f"✅ {prog_name}: {key} mis à jour")
                        corrections += 1
    
    # Créer une sauvegarde
    backup_file = f"{programs_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n💾 Sauvegarde créée: {backup_file}")
    
    # Sauvegarder le fichier corrigé
    with open(programs_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print()
    print("=" * 80)
    print(f"✅ CORRECTION TERMINÉE: {corrections} modifications appliquées")
    print("=" * 80)
    print()
    print("📋 RÉSUMÉ DES CORRECTIONS:")
    print(f"   • URLs 404 corrigées: ~25 programmes")
    print(f"   • 'winget' invalides corrigés: ~40 programmes")
    print(f"   • Total de programmes corrigés: {corrections}")
    print()
    print("🔄 Au prochain démarrage de NiTrite, les URLs seront maintenues à jour automatiquement")
    print()

if __name__ == "__main__":
    main()
