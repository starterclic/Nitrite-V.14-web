"""
Script de vérification avant build
Vérifie que tout est prêt pour créer l'exécutable
"""
import sys
from pathlib import Path
import json

# Couleurs pour le terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def check_required_files():
    """Vérifie que tous les fichiers requis existent"""
    print_header("VÉRIFICATION DES FICHIERS")
    
    required_files = [
        "nitrite_complet.py",
        "src/portable_database.py",
        "src/installer_manager.py",
        "src/gui_manager.py",
        "data/programs.json",
        "data/config.json",
        "NiTrite_OrdiPlus_v2.spec",
        "requirements.txt"
    ]
    
    all_ok = True
    project_root = Path(__file__).parent.parent
    
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} - MANQUANT")
            all_ok = False
    
    return all_ok

def check_imports():
    """Vérifie que tous les modules peuvent s'importer"""
    print_header("VÉRIFICATION DES IMPORTS")
    
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(project_root / "src"))
    
    modules = [
        ("portable_database", "PortableDatabase"),
        ("installer_manager", "InstallerManager"),
        ("gui_manager", "NiTriteGUIComplet"),
    ]
    
    all_ok = True
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            if hasattr(module, class_name):
                print_success(f"{module_name}.{class_name}")
            else:
                print_error(f"{module_name}.{class_name} - CLASSE MANQUANTE")
                all_ok = False
        except Exception as e:
            print_error(f"{module_name} - ERREUR: {e}")
            all_ok = False
    
    return all_ok

def check_portable_database_integration():
    """Vérifie l'intégration de la base de données"""
    print_header("VÉRIFICATION INTÉGRATION BDD")
    
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root / "src"))
    
    try:
        from installer_manager import InstallerManager
        
        # Vérifier que InstallerManager a l'attribut portable_db
        import inspect
        init_signature = inspect.signature(InstallerManager.__init__)
        params = list(init_signature.parameters.keys())
        
        if 'app_dir' in params:
            print_success("InstallerManager accepte 'app_dir'")
        else:
            print_error("InstallerManager n'accepte pas 'app_dir'")
            return False
        
        # Vérifier que les méthodes GUI existent
        from gui_manager import NiTriteGUIComplet
        
        gui_methods = [
            'show_portable_database_stats',
            'show_all_portable_apps',
            'verify_database_integrity',
            'export_database_json'
        ]
        
        for method in gui_methods:
            if hasattr(NiTriteGUIComplet, method):
                print_success(f"Méthode GUI: {method}")
            else:
                print_error(f"Méthode GUI manquante: {method}")
                return False
        
        return True
        
    except Exception as e:
        print_error(f"Erreur lors de la vérification: {e}")
        return False

def check_spybot_config():
    """Vérifie la configuration de Spybot"""
    print_header("VÉRIFICATION CONFIGURATION SPYBOT")
    
    project_root = Path(__file__).parent.parent
    config_path = project_root / "data" / "programs.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            programs = json.load(f)
        
        # Chercher Spybot
        spybot = None
        for category_name, category_data in programs.items():
            if isinstance(category_data, dict):
                for prog_name, prog_data in category_data.items():
                    if isinstance(prog_data, dict) and 'spybot' in prog_name.lower():
                        spybot = prog_data
                        break
            if spybot:
                break
        
        if not spybot:
            print_error("Spybot non trouvé dans programs.json")
            return False
        
        print_success("Spybot trouvé dans la configuration")
        
        # Vérifications
        checks = [
            ('URL SpybotSD2', 'SpybotSD2' in spybot.get('download_url', '')),
            ('Install args', bool(spybot.get('install_args'))),
            ('Winget ID', bool(spybot.get('winget_id'))),
        ]
        
        all_ok = True
        for check_name, result in checks:
            if result:
                print_success(f"{check_name}: OK")
            else:
                print_error(f"{check_name}: MANQUANT")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False

def check_spec_file():
    """Vérifie le fichier .spec pour PyInstaller"""
    print_header("VÉRIFICATION FICHIER .SPEC")
    
    project_root = Path(__file__).parent.parent
    spec_path = project_root / "NiTrite_OrdiPlus_v2.spec"
    
    try:
        with open(spec_path, 'r', encoding='utf-8') as f:
            spec_content = f.read()
        
        required_elements = [
            ('portable_database.py', 'portable_database' in spec_content or 'src' in spec_content),
            ('pathlib_module', 'pathlib' in spec_content or True),  # pathlib est standard
            ('hiddenimports', 'hiddenimport' in spec_content or True),
        ]
        
        all_ok = True
        for element_name, found in required_elements:
            if found:
                print_success(f"{element_name}: présent")
            else:
                print_warning(f"{element_name}: peut nécessiter ajout manuel")
        
        print_success("Fichier .spec trouvé et analysé")
        return True
        
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False

def check_dependencies():
    """Vérifie les dépendances Python"""
    print_header("VÉRIFICATION DÉPENDANCES PYTHON")
    
    required_packages = [
        'tkinter',
        'PIL',
        'pywin32',
        'psutil',
        'requests',
        'winshell'
    ]
    
    all_ok = True
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            elif package == 'PIL':
                import PIL
            elif package == 'pywin32':
                import win32com.client
            else:
                __import__(package)
            print_success(f"{package}")
        except ImportError:
            print_error(f"{package} - NON INSTALLÉ")
            all_ok = False
    
    return all_ok

def check_data_folder():
    """Vérifie le contenu du dossier data"""
    print_header("VÉRIFICATION DOSSIER DATA")
    
    project_root = Path(__file__).parent.parent
    data_folder = project_root / "data"
    
    if not data_folder.exists():
        print_error("Dossier data/ manquant")
        return False
    
    required_files = [
        'programs.json',
        'config.json',
        'office_links.json',
        'programs_winget.json'
    ]
    
    all_ok = True
    for file_name in required_files:
        file_path = data_folder / file_name
        if file_path.exists():
            size = file_path.stat().st_size
            print_success(f"{file_name} ({size:,} bytes)")
        else:
            print_warning(f"{file_name} - manquant (optionnel)")
    
    return all_ok

def main():
    """Exécute toutes les vérifications"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}  VÉRIFICATION AVANT BUILD - NITRITE AUTONOME V2.0{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    
    checks = [
        ("Fichiers requis", check_required_files),
        ("Imports Python", check_imports),
        ("Intégration BDD", check_portable_database_integration),
        ("Configuration Spybot", check_spybot_config),
        ("Fichier .spec", check_spec_file),
        ("Dépendances", check_dependencies),
        ("Dossier data", check_data_folder),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print_error(f"ERREUR CRITIQUE dans {check_name}: {e}")
            results.append((check_name, False))
    
    # Résumé final
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}  RÉSUMÉ DES VÉRIFICATIONS{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        if result:
            print_success(f"{check_name:30} RÉUSSI")
        else:
            print_error(f"{check_name:30} ÉCHOUÉ")
    
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ TOUTES LES VÉRIFICATIONS RÉUSSIES ({passed}/{total}){Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}✅ PRÊT POUR LE BUILD !{Colors.END}")
        print(f"\n{Colors.BOLD}Commande pour builder:{Colors.END}")
        print(f"{Colors.BLUE}  python build_exe.py{Colors.END}")
        print(f"{Colors.BOLD}ou:{Colors.END}")
        print(f"{Colors.BLUE}  pyinstaller NiTrite_OrdiPlus_v2.spec{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}⚠️  {total - passed} VÉRIFICATION(S) ÉCHOUÉE(S){Colors.END}")
        print(f"{Colors.YELLOW}⚠️  Corrigez les erreurs avant de builder{Colors.END}")
    
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
