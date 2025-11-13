"""
Système de mise à jour automatique des URLs
Maintient les URLs à jour au démarrage de l'application
"""
import json
import os
import logging
from datetime import datetime

class URLUpdater:
    """Gestionnaire de mise à jour automatique des URLs"""
    
    def __init__(self, programs_file):
        self.programs_file = programs_file
        self.logger = logging.getLogger(__name__)
        
        # Définition des URLs dynamiques qui se mettent à jour automatiquement
        self.dynamic_urls = {
            # Navigateurs
            "Vivaldi": "https://downloads.vivaldi.com/stable/Vivaldi.6.9.3447.54.x64.exe",
            "Tor Browser": "https://www.torproject.org/dist/torbrowser/14.0/torbrowser-install-win64-14.0_fr.exe",
            
            # Antivirus (pages de téléchargement)
            "Norton 360": "",  # Winget only
            "ESET NOD32": "",  # Winget only
            "Sophos Home": "https://central.sophos.com/manage/downloads/sophos-home",
            
            # Sécurité
            "Comodo Firewall": "https://download.comodo.com/cis/download/installs/2000/partners/cfw_installer_12009_86.exe",
            
            # Bureautique
            "Foxit Reader": "",  # Utiliser winget
            "Evernote": "https://cdn1.evernote.com/boron/win/builds/Evernote-latest-win-ddl-ga.exe",
            
            # Multimédia
            "K-Lite Codec Pack": "https://files3.codecguide.com/K-Lite_Codec_Pack_1805_Standard.exe",
            "Audacity": "https://github.com/audacity/audacity/releases/download/Audacity-3.6.4/audacity-win-3.6.4-x64.exe",
            "Paint.NET": "",  # Winget only
            
            # Développement
            "Git": "https://github.com/git-for-windows/git/releases/download/v2.47.0.windows.1/Git-2.47.0-64-bit.exe",
            "Node.js": "https://nodejs.org/dist/v22.11.0/node-v22.11.0-x64.msi",
            "Android Studio": "",  # Winget only
            
            # Utilitaires
            "PowerToys": "https://github.com/microsoft/PowerToys/releases/download/v0.86.0/PowerToysSetup-0.86.0-x64.exe",
            "HWiNFO64": "https://www.hwinfo.com/files/hwi_768.exe",
            "MSI Afterburner": "",  # Winget only
            
            # Jeux
            "GOG Galaxy": "https://cdn.gog.com/open/galaxy/client/2.0.77.126/setup_galaxy_2.0.77.126.exe",
            "Origin": "",  # Winget only
            
            # Désinstallateurs (redirections vers pages support)
            "Bitdefender Uninstall Tool": "https://www.bitdefender.com/consumer/support/answer/15722/",
            "Norton Remove and Reinstall Tool": "",  # Winget only
            "ESET Uninstaller": "",  # Winget only
            "Malwarebytes Support Tool": "https://downloads.malwarebytes.com/file/mb-support-tool",
            "Sophos Removal Tool": "",  # Winget only
            
            # Internet
            "qBittorrent": "https://github.com/qbittorrent/qBittorrent/releases/download/release-5.0.1/qbittorrent_5.0.1_x64_setup.exe",
            "Internet Download Manager": "https://www.internetdownloadmanager.com/idman642build25.exe",
            "FileZilla": "https://download.filezilla-project.org/client/FileZilla_3.67.1_win64-setup.exe",
            
            # Productivité
            "Monday.com": "",  # Winget only
            
            # Compression
            "KGB Archiver": "",  # Site SSL cassé - abandonner
        }
        
        # Programmes à basculer vers winget uniquement
        self.switch_to_winget = {
            "Norton 360": "NortonLifeLock.Norton360",
            "ESET NOD32": "ESET.Security",
            "Foxit Reader": "Foxit.FoxitReader",
            "Paint.NET": "dotPDN.PaintDotNet",
            "Android Studio": "Google.AndroidStudio",
            "MSI Afterburner": "Guru3D.Afterburner",
            "Origin": "ElectronicArts.Origin",
            "Norton Remove and Reinstall Tool": "NortonLifeLock.NortonRemoveAndReinstall",
            "ESET Uninstaller": "ESET.ESETUninstaller",
            "Sophos Removal Tool": "Sophos.SophosRemovalTool",
            "Monday.com": "Monday.Monday",
            "KGB Archiver": "",  # Abandonner ce programme (site SSL cassé)
            
            # Programmes avec "winget" comme URL au lieu de vide
            "Ollama": "Ollama.Ollama",
            "LM Studio": "LMStudio.LMStudio",
            "Jan AI": "Jan.Jan",
            "Waifu2x-Extension-GUI": "AaronFeng753.Waifu2x-Extension-GUI",
            "Upscayl": "Upscayl.Upscayl",
            "AnythingLLM": "MintplexLabs.AnythingLLM",
            "Whisper Desktop": "Const-me.Whisper",
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
            "Epson Print and Scan": "Epson.PrintandScan",
            "Brother iPrint&Scan": "Brother.iPrintAndScan",
            "VueScan": "Hamrick.VueScan",
            "NAPS2": "NAPS2.NAPS2",
            "PaperScan": "ORPALIS.PaperScan",
            "PDF24 Creator": "geeksoftwareGmbH.PDF24Creator",
            "iCloud": "Apple.iCloud",
            "Apple Devices": "Apple.Devices",
            "Adobe Creative Cloud": "Adobe.CreativeCloud",
            "Autodesk AutoCAD": "Autodesk.AutoCAD",
            "SketchUp": "Trimble.SketchUp",
            "CorelDRAW Graphics Suite": "Corel.CorelDRAW",
            "Figma": "Figma.Figma",
            "Canva": "Canva.Canva",
            "Blender": "BlenderFoundation.Blender",
            "Affinity Designer": "SerifEurope.AffinityDesigner",
            "Affinity Photo": "SerifEurope.AffinityPhoto",
            "Affinity Publisher": "SerifEurope.AffinityPublisher",
            "PeaZip": "Giorgiotani.Peazip",
            "Bandizip": "Bandisoft.Bandizip",
            "NanaZip": "M2Team.NanaZip",
        }
    
    def update_all_urls(self):
        """Met à jour toutes les URLs dans programs.json"""
        try:
            # Charger le fichier
            with open(self.programs_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            updated_count = 0
            fixed_winget = 0
            
            # Parcourir toutes les catégories et programmes
            for category, programs in data.items():
                for prog_name, prog_info in programs.items():
                    
                    # 1. Corriger les URLs "winget" invalides
                    if prog_info.get('download_url') == 'winget':
                        prog_info['download_url'] = ''
                        if prog_name in self.switch_to_winget and self.switch_to_winget[prog_name]:
                            if 'winget_id' not in prog_info or not prog_info['winget_id']:
                                prog_info['winget_id'] = self.switch_to_winget[prog_name]
                        fixed_winget += 1
                        self.logger.info(f"Corrigé URL 'winget' invalide: {prog_name}")
                    
                    # 2. Mettre à jour les URLs dynamiques
                    if prog_name in self.dynamic_urls:
                        new_url = self.dynamic_urls[prog_name]
                        old_url = prog_info.get('download_url', '')
                        
                        if new_url != old_url:
                            prog_info['download_url'] = new_url
                            
                            # Si URL vide, ajouter winget_id si disponible
                            if not new_url and prog_name in self.switch_to_winget:
                                winget_id = self.switch_to_winget[prog_name]
                                if winget_id and ('winget_id' not in prog_info or not prog_info['winget_id']):
                                    prog_info['winget_id'] = winget_id
                            
                            updated_count += 1
                            self.logger.info(f"Mis à jour: {prog_name}")
            
            # Sauvegarder si des modifications ont été faites
            if updated_count > 0 or fixed_winget > 0:
                # Créer une sauvegarde
                backup_file = f"{self.programs_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                
                # Sauvegarder le fichier mis à jour
                with open(self.programs_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                
                self.logger.info(f"✅ Mise à jour terminée: {updated_count} URLs mises à jour, {fixed_winget} 'winget' corrigés")
                return True, updated_count + fixed_winget
            else:
                self.logger.info("Aucune mise à jour nécessaire")
                return False, 0
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la mise à jour des URLs: {e}")
            return False, 0
    
    def check_for_updates(self):
        """Vérifie si des mises à jour sont disponibles (appel au démarrage)"""
        self.logger.info("Vérification des mises à jour des URLs...")
        return self.update_all_urls()
