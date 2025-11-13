# NiTriTe V.13 - Key Implementation Snippets

## 1. MASTER INSTALLATION APPS LIST

**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/gui_modern_v13.py` (Lines 1495-1556)

```python
def _get_master_apps(self):
    """Obtenir la liste des applications Master Installation"""
    return {
        "Adobe Acrobat Reader": {
            "url": "https://get.adobe.com/reader/",
            "portable": False,
            "description": "Lecteur PDF officiel d'Adobe"
        },
        "VLC Media Player": {
            "url": "https://www.videolan.org/vlc/",
            "portable": False,
            "description": "Lecteur multimédia universel"
        },
        "Pack Office 2007": {
            "url": "https://gravesoft.dev/office_c2r_links#2007",
            "portable": False,
            "description": "Suite bureautique Microsoft Office 2007"
        },
        "Pack Office 2024": {
            "url": "https://gravesoft.dev/office_c2r_links#2024",
            "portable": False,
            "description": "Suite bureautique Microsoft Office 2024"
        },
        "Spybot Search & Destroy": {
            "url": "https://www.safer-networking.org/download/",
            "portable": False,
            "description": "Anti-malware et protection système"
        },
        "AdwCleaner": {
            "url": "https://www.malwarebytes.com/adwcleaner",
            "portable": True,
            "exe_name": "adwcleaner.exe",
            "description": "Suppression des adwares (Portable)"
        },
        "AnyDesk": {
            "url": "https://anydesk.com/en/downloads/thank-you?dv=win_exe",
            "portable": True,
            "exe_name": "AnyDesk.exe",
            "description": "Contrôle à distance (Portable)"
        },
        "RustDesk": {
            "url": "https://github.com/rustdesk/rustdesk/releases/latest",
            "portable": True,
            "exe_name": "rustdesk.exe",
            "description": "Contrôle à distance open-source (Portable)"
        },
        "Wise Disk Cleaner": {
            "url": "https://www.wisecleaner.com/wise-disk-cleaner.html",
            "portable": False,
            "description": "Nettoyage et optimisation du disque"
        },
        "Malwarebytes": {
            "url": "https://www.malwarebytes.com/",
            "portable": False,
            "description": "Protection anti-malware avancée"
        },
        "Firefox": {
            "url": "https://www.mozilla.org/firefox/download/",
            "portable": False,
            "description": "Navigateur web Mozilla Firefox"
        },
    }
```

---

## 2. TELEMETRY TWEAKS POWERSHELL SCRIPT

**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/advanced_pages.py` (Lines 2298-2314)

```powershell
# Désactiver télémétrie
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" -Name "AllowTelemetry" -Type DWord -Value 0

# Désactiver rapport d'erreurs Windows
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\Windows Error Reporting" -Name "Disabled" -Type DWord -Value 1

# Désactiver suggestions dans Démarrer
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" -Name "SystemPaneSuggestionsEnabled" -Type DWord -Value 0

# Désactiver historique d'activité
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\System" -Name "PublishUserActivities" -Type DWord -Value 0
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\System" -Name "UploadUserActivities" -Type DWord -Value 0

Write-Host "Tweaks télémétrie appliqués avec succès!"
```

**Execution Method:**
```python
# Line 2324-2330
result = subprocess.run(
    ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
    capture_output=True,
    text=True,
    timeout=30,
    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
)
```

---

## 3. WINDOWS SERVICES TO DISABLE

**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/advanced_pages.py` (Lines 2420-2436)

```python
services_to_optimize = [
    ("DiagTrack", "Télémétrie et diagnostics Windows"),
    ("dmwappushservice", "Routage push WAP (télémétrie)"),
    ("WSearch", "Windows Search (si non utilisé)"),
    ("SysMain", "Superfetch (sur SSD)"),
    ("WMPNetworkSvc", "Partage réseau Windows Media Player"),
    ("XblAuthManager", "Authentification Xbox Live"),
    ("XblGameSave", "Sauvegarde jeux Xbox"),
    ("XboxNetApiSvc", "Service réseau Xbox"),
    ("XboxGipSvc", "Service Xbox Accessory Management"),
    ("Fax", "Service de télécopie"),
    ("RetailDemo", "Service de démonstration magasin"),
    ("MapsBroker", "Gestionnaire cartes téléchargées"),
    ("lfsvc", "Service de géolocalisation"),
    ("TabletInputService", "Service d'entrée tablette"),
    ("TrkWks", "Client de suivi de liens distribués"),
]
```

**Service Disabling Script:**
```python
# Line 2480-2483
ps_commands = '\n'.join([
    f'Set-Service -Name "{svc}" -StartupType Disabled -ErrorAction SilentlyContinue'
    for svc in selected
])
```

---

## 4. SYSTEM CLEANUP OPERATIONS

**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/advanced_pages.py` (Lines 2573-2700+)

### Cleanup Operation 1: Temp Folder
```python
# Clean %TEMP% paths
temp_paths = [
    os.path.expandvars('%TEMP%'),
    os.path.expandvars('%TMP%'),
    os.path.expandvars('C:\\Windows\\Temp')
]

for temp_path in temp_paths:
    if os.path.exists(temp_path):
        for item in os.listdir(temp_path):
            item_path = os.path.join(temp_path, item)
            try:
                if os.path.isfile(item_path):
                    size = os.path.getsize(item_path)
                    os.unlink(item_path)
                    total_freed += size
                elif os.path.isdir(item_path):
                    size = sum(os.path.getsize(os.path.join(dirpath, filename))
                               for dirpath, dirnames, filenames in os.walk(item_path)
                               for filename in filenames)
                    shutil.rmtree(item_path)
                    total_freed += size
            except:
                pass  # Ignorer les fichiers verrouillés
```

### Cleanup Operation 2: Empty Recycle Bin
```python
# PowerShell command to empty recycle bin
subprocess.run(
    ["powershell", "-Command", "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"],
    capture_output=True,
    timeout=30,
    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
)
```

### Cleanup Operation 3: Windows Update Cache
```python
update_cache = os.path.expandvars('C:\\Windows\\SoftwareDistribution\\Download')
if os.path.exists(update_cache):
    for item in os.listdir(update_cache):
        item_path = os.path.join(update_cache, item)
        try:
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                os.unlink(item_path)
                total_freed += size
            elif os.path.isdir(item_path):
                size = sum(os.path.getsize(os.path.join(dirpath, filename))
                           for dirpath, dirnames, filenames in os.walk(item_path)
                           for filename in filenames)
                shutil.rmtree(item_path)
                total_freed += size
        except:
            pass
```

---

## 5. DIAGNOSTIC REAL-TIME MONITORING

**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/advanced_pages.py` (Lines 663-696)

```python
def _update_performance_realtime(self):
    """Mettre à jour les performances en temps réel (toutes les 2 secondes)"""
    if not self.update_running:
        return

    try:
        # Mettre à jour CPU
        cpu_percent = psutil.cpu_percent(interval=0.1) if PSUTIL_AVAILABLE else 0
        if self.perf_widgets['cpu_percent']:
            self.perf_widgets['cpu_percent'].config(text=f"{cpu_percent:.1f}%")
        if self.perf_widgets['cpu_bar']:
            self.perf_widgets['cpu_bar'].place(x=0, y=0, relwidth=cpu_percent/100, relheight=1)

        # Mettre à jour RAM
        if PSUTIL_AVAILABLE:
            ram = psutil.virtual_memory()
            if self.perf_widgets['ram_percent']:
                self.perf_widgets['ram_percent'].config(text=f"{ram.percent:.1f}%")
            if self.perf_widgets['ram_bar']:
                self.perf_widgets['ram_bar'].place(x=0, y=0, relwidth=ram.percent/100, relheight=1)

        # Mettre à jour Disque
        if PSUTIL_AVAILABLE:
            disk = psutil.disk_usage('C:\\' if platform.system() == 'Windows' else '/')
            if self.perf_widgets['disk_percent']:
                self.perf_widgets['disk_percent'].config(text=f"{disk.percent:.1f}%")
            if self.perf_widgets['disk_bar']:
                self.perf_widgets['disk_bar'].place(x=0, y=0, relwidth=disk.percent/100, relheight=1)

    except Exception as e:
        pass  # Ignorer les erreurs silencieusement

    # Relancer dans 2 secondes
    self.after(2000, self._update_performance_realtime)
```

---

## 6. SYSTEM TOOLS DATABASE STRUCTURE

**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/tools_data_complete.py` (Lines 11-100)

```python
def get_all_tools():
    """Retourne tous les outils organisés par section"""
    return {
        # SYSTEM REPAIR SECTION
        "🔨 Réparation Système": [
            ("🔍 DISM Check", "DISM /Online /Cleanup-Image /CheckHealth"),
            ("🔎 DISM Scan", "DISM /Online /Cleanup-Image /ScanHealth"),
            ("🔧 DISM Restore", "DISM /Online /Cleanup-Image /RestoreHealth"),
            ("🛠️ SFC Scan", "sfc /scannow"),
            ("💽 CHKDSK C:", "chkdsk C: /f /r"),
            ("💾 CHKDSK D:", "chkdsk D: /f /r"),
            # ... 30+ more repair tools
        ],

        # ACTIVATION & DOWNLOADS
        "🔧 Activation & Téléchargements": [
            ("⚡ PowerToys", "https://github.com/microsoft/PowerToys/releases/latest"),
            ("📦 Office FR", "https://gravesoft.dev/office_c2r_links#french-fr-france"),
            ("📋 Office EN", "https://gravesoft.dev/office_c2r_links"),
            ("🔑 MS Activation Scripts", "https://massgrave.dev/"),
            # ... 25+ more tools
        ],

        # MAINTENANCE & CLEANING
        "🧹 Maintenance & Nettoyage": [
            ("🧹 Disk Cleanup", "cleanmgr"),
            ("📦 Cleanup Full", "cleanmgr /sageset:1 & cleanmgr /sagerun:1"),
            ("🗂️ Clean WinSxS", "DISM /Online /Cleanup-Image /StartComponentCleanup"),
            ("🔧 WinSxS Analyze", "DISM /Online /Cleanup-Image /AnalyzeComponentStore"),
            # ... 15+ more cleaning tools
        ],

        # DIAGNOSTICS & INFOS
        "📊 Diagnostics & Infos": [
            ("💻 System Info", "msinfo32"),
            ("🎮 DirectX Diag", "dxdiag"),
            ("📊 Event Viewer", "eventvwr.msc"),
            ("🔧 Device Manager", "devmgmt.msc"),
            # ... more diagnostic tools
        ],
    }
```

---

## 7. THEME COLOR PALETTE

**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/modern_colors.py`

```python
# Dark Theme Colors
class ModernColors:
    # Backgrounds
    BG_DARK = '#1E1E1E'          # Main dark background
    BG_CARD = '#2D2D2D'          # Card/section background
    BG_LIGHT = '#3D3D3D'         # Lighter sections

    # Text Colors
    TEXT_PRIMARY = '#FFFFFF'     # Main text
    TEXT_SECONDARY = '#A0A0A0'   # Secondary/muted text

    # Action Colors
    ORANGE_PRIMARY = '#FF9500'   # Primary action button
    ORANGE_DARK = '#E68400'      # Hover state

    # Status Colors
    RED_ERROR = '#FF6B6B'        # Errors
    BLUE_INFO = '#4A9EFF'        # Information
    GREEN_SUCCESS = '#51CF66'    # Success
    PURPLE_PREMIUM = '#B365F5'   # Premium/special
    YELLOW_WARNING = '#FFD166'   # Warnings

    # Borders
    BORDER_COLOR = '#404040'
    BORDER_LIGHT = '#505050'
```

---

## 8. MAIN GUI NAVIGATION STRUCTURE

**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/gui_modern_v13.py` (Lines 345-350)

```python
# Navigation menu items definition
self.nav_items = [
    # Format: (page_id, icon, title, description)
    ("master_install", "🚀", "Master Installation", "Installation rapide Windows"),
    ("optimizations", "⚡", "Optimisations", "Tweaks Windows"),
    ("diagnostics", "🔍", "Diagnostic", "Benchmark système"),
    ("backup", "💾", "Backup", "Sauvegarde & Restauration"),
]

# Page instantiation
# Lines 2345-2350
self.pages['master_install'] = MasterInstallationPage(self.content_area)
self.pages['optimizations'] = OptimizationsPage(self.content_area)
self.pages['diagnostics'] = DiagnosticPage(self.content_area)
self.pages['backup'] = BackupPage(self.content_area)
```

---

## 9. WEB API STRUCTURE (Current + Missing)

**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/web/js/api.js`

```javascript
// Currently Implemented Endpoints
class NiTriTeAPI {
    // Data retrieval
    async getApplications() {
        return await this.request('/applications');
    }

    async getTools() {
        return await this.request('/tools');
    }

    async getProfiles() {
        return await this.request('/profiles');
    }

    async getDiagnostics() {
        return await this.request('/diagnostics');
    }

    // Installation commands
    async installApplication(appId, method = 'auto') {
        return await this.request('/install', 'POST', {
            app_id: appId,
            method: method
        });
    }

    async installMultiple(appIds) {
        return await this.request('/install/bulk', 'POST', {
            app_ids: appIds
        });
    }

    // Tool execution
    async executeTool(toolId, params = {}) {
        return await this.request('/tools/execute', 'POST', {
            tool_id: toolId,
            params: params
        });
    }

    // Favorites management (localStorage)
    async getFavorites() {
        const favorites = localStorage.getItem('nitrite_favorites');
        return favorites ? JSON.parse(favorites) : [];
    }

    async addFavorite(appId) {
        const favorites = await this.getFavorites();
        if (!favorites.includes(appId)) {
            favorites.push(appId);
            localStorage.setItem('nitrite_favorites', JSON.stringify(favorites));
        }
    }
}

// MISSING ENDPOINTS FOR WEB VERSION:
// POST /api/optimize/telemetry          - Apply telemetry tweaks
// POST /api/optimize/services           - Disable services
// POST /api/system/cleanup              - Auto cleanup
// POST /api/system/restore-point        - Create restore point
// POST /api/system/backup-drivers       - Backup drivers
// GET /api/system/restore-points        - List restore points
// GET /api/performance/realtime         - Real-time stats (WebSocket?)
```

---

## Summary Table of All Features

| Feature | Type | Location | Implementation | Status |
|---------|------|----------|---|---|
| Master Installation | Page | gui_modern_v13.py:1486 | Desktop GUI | Complete |
| Optimizations | Page | advanced_pages.py:1965 | Desktop GUI | Complete |
| Diagnostics | Page | advanced_pages.py:558 | Desktop GUI + Web Partial |
| Backup & Restore | Page | advanced_pages.py:1391 | Desktop GUI | Complete |
| System Tools | Database | tools_data_complete.py | 548+ Tools | Complete |
| Telemetry Tweaks | Function | advanced_pages.py:2269 | PowerShell | Complete |
| Service Optimization | Function | advanced_pages.py:2355 | PowerShell | Complete |
| System Cleanup | Function | advanced_pages.py:2519 | Python + PowerShell | Complete |
| Real-time Monitoring | Function | advanced_pages.py:663 | psutil | Complete |
| Web UI | Interface | web/js/*.js | Partial | Needs Enhancement |

