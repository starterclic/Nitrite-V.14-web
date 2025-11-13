"""
CORRECTION AUTOMATIQUE COMPLÈTE DE TOUS LES PROGRAMMES
Corrige toutes les URLs cassées et configure winget
"""
import json
from datetime import datetime

def main():
    print("=" * 100)
    print("🔧 CORRECTION AUTOMATIQUE COMPLÈTE - TOUS LES PROGRAMMES")
    print("=" * 100)
    print()
    
    programs_file = 'data/programs.json'
    
    with open(programs_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    corrections_count = 0
    
    # Base de corrections massives
    corrections_globales = {
        # Basculer vers winget si URL problématique
        "basculer_winget": {
            # Navigateurs
            "Brave": "Brave.Brave",
            "Chromium": "eloston.ungoogled-chromium",
            "Tor Browser": "TorProject.TorBrowser",
            "Vivaldi": "VivaldiTechnologies.Vivaldi",
            
            # Bureautique
            "Foxit Reader": "Foxit.FoxitReader",
            "PDF-XChange Editor": "TrackerSoftware.PDF-XChangeEditor",
            "LibreOffice": "TheDocumentFoundation.LibreOffice",
            
            # Multimédia
            "K-Lite Codec Pack": "CodecGuide.K-LiteCodecPack.Standard",
            "MPC-HC": "clsid2.mpc-hc",
            "Paint.NET": "dotPDN.PaintDotNet",
            "AIMP": "AIMP.AIMP",
            
            # Développement
            "Visual Studio Code": "Microsoft.VisualStudioCode",
            "Git": "Git.Git",
            "Node.js": "OpenJS.NodeJS",
            "Python": "Python.Python.3.12",
            "Android Studio": "Google.AndroidStudio",
            
            # Utilitaires
            "7-Zip": "7zip.7zip",
            "WinRAR": "RARLab.WinRAR",
            "Notepad++": "Notepad++.Notepad++",
            "PowerToys": "Microsoft.PowerToys",
            "Everything": "voidtools.Everything",
            "Revo Uninstaller": "RevoUninstaller.RevoUninstaller",
            
            # Communication
            "Discord": "Discord.Discord",
            "Skype": "Microsoft.Skype",
            "Zoom": "Zoom.Zoom",
            "TeamViewer": "TeamViewer.TeamViewer",
            "Slack": "SlackTechnologies.Slack",
            
            # Jeux
            "Steam": "Valve.Steam",
            "Epic Games Launcher": "EpicGames.EpicGamesLauncher",
            "GOG Galaxy": "GOG.Galaxy",
            "Origin": "ElectronicArts.Origin",
            "Battle.net": "Blizzard.BattleNet",
            
            # Internet
            "qBittorrent": "qBittorrent.qBittorrent",
            "FileZilla": "FileZilla.FileZilla",
            "PuTTY": "PuTTY.PuTTY",
            
            # Antivirus
            "Avast Free Antivirus": "XPDC2RH70K22MN",
            "AVG Antivirus": "AVG.AntiVirusFree",
            "Avira Free Security": "Avira.Avira",
            "Kaspersky": "Kaspersky.KasperskySecurityCloud",
            "McAfee": "McAfee.TotalProtection",
            
            # Compression
            "WinZip": "WinZip.WinZip",
            "PeaZip": "Giorgiotani.Peazip",
            "Bandizip": "Bandisoft.Bandizip",
            "NanaZip": "M2Team.NanaZip",
        }
    }
    
    # Parcourir toutes les catégories
    for category, programs in data.items():
        for prog_name, prog_info in programs.items():
            
            url = prog_info.get('download_url', '')
            
            # Correction 1: Basculer vers winget si dans la liste
            if prog_name in corrections_globales["basculer_winget"]:
                winget_id = corrections_globales["basculer_winget"][prog_name]
                
                # Ne basculer que si pas déjà winget ou si URL cassée
                if not prog_info.get('winget_id') or 'http' not in url:
                    prog_info['download_url'] = ''
                    prog_info['winget_id'] = winget_id
                    prog_info['note'] = 'Installation via winget'
                    print(f"✅ {prog_name:50} → Winget: {winget_id}")
                    corrections_count += 1
            
            # Correction 2: URLs "winget" invalides
            if url == 'winget':
                prog_info['download_url'] = ''
                print(f"✅ {prog_name:50} → URL 'winget' corrigée")
                corrections_count += 1
            
            # Correction 3: Ajouter admin_required par défaut si téléchargement direct
            if url and 'http' in url and 'admin_required' not in prog_info:
                # Exceptions: programmes portables
                if not prog_info.get('portable') and not prog_info.get('install_args') == 'portable':
                    prog_info['admin_required'] = True
                    corrections_count += 1
    
    # Sauvegarde
    backup_file = f"{programs_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n💾 Sauvegarde: {backup_file}")
    
    # Sauvegarder
    with open(programs_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print()
    print("=" * 100)
    print(f"✅ {corrections_count} CORRECTIONS APPLIQUÉES")
    print("=" * 100)
    print()
    print("📋 TYPES DE CORRECTIONS:")
    print("   • Programmes basculés vers winget")
    print("   • URLs 'winget' invalides corrigées")
    print("   • Flags admin_required ajoutés")
    print()
    print("🔄 Reconstruisez le package: python build_portable_complet.py")
    print()

if __name__ == "__main__":
    main()
