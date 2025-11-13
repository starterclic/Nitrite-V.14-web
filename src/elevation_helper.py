"""
Module d'élévation automatique des privilèges
Permet l'installation sans confirmation UAC manuelle
VERSION AMÉLIORÉE avec auto-élévation au démarrage
"""

import ctypes
import sys
import subprocess
import os
import tempfile
from pathlib import Path

def is_admin():
    """Vérifie si le script a les privilèges administrateur"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def elevate_if_needed():
    """
    Relance le script avec privilèges administrateur si nécessaire
    Utilise ShellExecuteW pour élévation
    """
    if not is_admin():
        # Relancer avec élévation
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                ' '.join(sys.argv),
                None,
                1  # SW_SHOW
            )
            return True  # Script relancé avec élévation
        except Exception:
            return False  # Élévation refusée
    return False  # Déjà admin

def auto_elevate_at_startup():
    """
    Élève automatiquement les privilèges au démarrage de l'application
    À appeler au tout début du script principal

    Returns:
        bool: True si l'élévation a été effectuée (et le programme doit se terminer),
              False si déjà admin ou si élévation refusée
    """
    if not is_admin():
        print("⚠️  NiTrite nécessite des privilèges administrateur")
        print("🔄 Relancement avec élévation automatique...")

        try:
            # Relancer avec privilèges admin
            ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                ' '.join([f'"{arg}"' if ' ' in arg else arg for arg in sys.argv]),
                None,
                1  # SW_SHOW
            )
            # Le programme actuel doit se terminer
            sys.exit(0)
        except Exception as e:
            print(f"❌ Impossible d'obtenir les privilèges administrateur: {e}")
            print("ℹ️  Certaines installations peuvent échouer sans privilèges admin")
            return False

    print("✅ Privilèges administrateur actifs")
    return False

def run_as_admin_silent(command, timeout=300):
    """
    Exécute une commande avec privilèges admin de manière silencieuse

    Args:
        command: Liste ou chaîne de commande à exécuter
        timeout: Timeout en secondes

    Returns:
        tuple: (success: bool, returncode: int, stdout: str, stderr: str)
    """

    if isinstance(command, str):
        command = [command]

    try:
        # Méthode 1: Si déjà admin, exécuter directement
        if is_admin():
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            return (result.returncode == 0, result.returncode, result.stdout, result.stderr)

        # Méthode 2: Utiliser PowerShell avec -Verb RunAs
        ps_command = ['powershell.exe', '-NoProfile', '-Command']

        if len(command) > 1:
            exe = command[0]
            args = ' '.join([f'"{arg}"' if ' ' in str(arg) else str(arg) for arg in command[1:]])
            ps_script = f'Start-Process -FilePath "{exe}" -ArgumentList \'{args}\' -Verb RunAs -Wait -PassThru | Select-Object -ExpandProperty ExitCode'
        else:
            exe = command[0]
            ps_script = f'Start-Process -FilePath "{exe}" -Verb RunAs -Wait -PassThru | Select-Object -ExpandProperty ExitCode'

        ps_command.append(ps_script)

        result = subprocess.run(
            ps_command,
            capture_output=True,
            text=True,
            timeout=timeout,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )

        try:
            exit_code = int(result.stdout.strip()) if result.stdout.strip() else result.returncode
        except (ValueError, AttributeError):
            exit_code = result.returncode

        return (exit_code == 0, exit_code, result.stdout, result.stderr)

    except subprocess.TimeoutExpired:
        return (False, -1, "", "Timeout expired")
    except Exception as e:
        return (False, -1, "", str(e))

def run_as_admin_batch(commands, timeout=300):
    """
    Exécute plusieurs commandes avec privilèges admin via un script batch
    Évite les multiples popups UAC

    Args:
        commands: Liste de commandes à exécuter
        timeout: Timeout en secondes

    Returns:
        tuple: (success: bool, returncode: int, stdout: str, stderr: str)
    """
    if not commands:
        return (False, -1, "", "No commands provided")

    try:
        # Créer un fichier batch temporaire
        batch_content = "@echo off\n"
        batch_content += "chcp 65001 >nul 2>&1\n"  # UTF-8

        for cmd in commands:
            if isinstance(cmd, list):
                batch_content += ' '.join([f'"{c}"' if ' ' in str(c) else str(c) for c in cmd]) + "\n"
            else:
                batch_content += cmd + "\n"

        batch_content += "exit /b %ERRORLEVEL%\n"

        # Écrire le batch dans un fichier temporaire
        temp_dir = tempfile.gettempdir()
        batch_file = Path(temp_dir) / f"nitrite_install_{os.getpid()}.bat"

        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(batch_content)

        # Exécuter le batch avec élévation
        if is_admin():
            # Déjà admin, exécuter directement
            result = subprocess.run(
                ['cmd.exe', '/c', str(batch_file)],
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            success = result.returncode == 0
        else:
            # Pas admin, utiliser PowerShell pour élever
            ps_command = [
                'powershell.exe',
                '-NoProfile',
                '-Command',
                f'Start-Process -FilePath "cmd.exe" -ArgumentList "/c {batch_file}" -Verb RunAs -Wait -WindowStyle Hidden'
            ]

            result = subprocess.run(
                ps_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            success = result.returncode == 0

        # Nettoyer le fichier batch
        try:
            batch_file.unlink()
        except Exception:
            pass

        return (success, result.returncode, result.stdout, result.stderr)

    except subprocess.TimeoutExpired:
        return (False, -1, "", "Timeout expired")
    except Exception as e:
        return (False, -1, "", str(e))

def create_elevated_process(exe_path, args=None, working_dir=None):
    """
    Crée un processus élevé en utilisant l'API Windows

    Args:
        exe_path: Chemin vers l'exécutable
        args: Arguments (liste ou chaîne)
        working_dir: Répertoire de travail

    Returns:
        bool: True si succès
    """
    if args is None:
        args = ""
    elif isinstance(args, list):
        args = ' '.join([f'"{arg}"' if ' ' in str(arg) else str(arg) for arg in args])

    try:
        # Utiliser ShellExecuteW pour lancer avec élévation
        result = ctypes.windll.shell32.ShellExecuteW(
            None,                    # hwnd
            "runas",                 # lpOperation (runas = exécuter en tant qu'admin)
            exe_path,                # lpFile
            args,                    # lpParameters
            working_dir,             # lpDirectory
            0                        # nShowCmd (0 = caché)
        )
        # ShellExecuteW retourne > 32 si succès
        return result > 32
    except Exception as e:
        print(f"Erreur lors de l'élévation: {e}")
        return False

def disable_uac_temporarily():
    """
    ATTENTION: Cette fonction est à utiliser avec précaution
    Elle ne désactive pas réellement l'UAC mais configure l'application
    pour minimiser les prompts UAC

    Returns:
        bool: True si configuration réussie
    """
    if not is_admin():
        return False

    try:
        # Cette fonction ne fait que retourner True pour indiquer
        # que l'application tourne déjà avec des privilèges admin
        # Il n'est PAS recommandé de désactiver l'UAC système
        return True
    except Exception:
        return False
