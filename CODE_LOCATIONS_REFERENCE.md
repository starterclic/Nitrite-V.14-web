# NiTriTe V.13 - Windows Optimization Features Code Locations

## File Structure Overview
```
/home/user/Nitrite-V.13-Beta-Portable-web-/
├── src/
│   ├── gui_modern_v13.py          [Master Installation Page - Line 1486]
│   ├── advanced_pages.py           [4 Major Pages - All optimization features]
│   ├── tools_data_complete.py      [548+ System Tools Database]
│   ├── config_manager.py
│   ├── modern_colors.py            [Color scheme]
│   └── ...
└── web/
    └── js/
        ├── app.js                  [Web app logic - needs enhancement]
        ├── api.js                  [API communication - needs enhancement]
        └── loading.js
```

---

## DETAILED FEATURE LOCATIONS

### 1. MASTER INSTALLATION PAGE
**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/gui_modern_v13.py`
**Lines:** 1486-1800+
**Class:** `MasterInstallationPage`

```python
# Line 1486: Class definition
class MasterInstallationPage(tk.Frame):
    """Page Master Installation Windows - Installation rapide d'applications essentielles"""

# Line 1495: Application list definition
def _get_master_apps(self):
    return {
        "Adobe Acrobat Reader": {...},
        "VLC Media Player": {...},
        # ... 12 total apps
    }

# Line 1558: UI widget creation
def _create_widgets(self):
    # Creates 6-column grid layout
    # Select/Deselect all buttons
    # Batch installation button
```

**Key Methods:**
- `_get_master_apps()` - Returns 12 application metadata (Line 1495)
- `_create_widgets()` - Builds the UI (Line 1558)
- `_create_app_card_grid()` - Creates individual app cards
- `_select_all()` - Select all applications
- `_deselect_all()` - Deselect all applications
- `_start_installation()` - Begin batch installation

---

### 2. OPTIMIZATIONS PAGE
**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/advanced_pages.py`
**Lines:** 1965-2795
**Class:** `OptimizationsPage`

```python
# Line 1965: Class definition
class OptimizationsPage(tk.Frame):
    """Page Optimisations Windows"""

# Line 2020-2030: Four main sections
def _create_widgets(self):
    self._create_telemetry_section(scrollable_frame)      # Line 2021
    self._create_services_section(scrollable_frame)       # Line 2024
    self._create_startup_section(scrollable_frame)        # Line 2027
    self._create_registry_section(scrollable_frame)       # Line 2030
```

#### SUBSECTION A: TELEMETRY & PRIVACY (Lines 2032-2100)
```python
# Line 2032: Telemetry section creation
def _create_telemetry_section(self, parent):
    # Toggle options:
    # - disable_telemetry
    # - disable_cortana
    # - disable_location
    # - disable_advertising
    # Apply button → _apply_telemetry_tweaks()
```

**Implementation:** Line 2269-2354
```python
def _apply_telemetry_tweaks(self):
    """Appliquer les tweaks de télémétrie Windows"""
    # Creates PowerShell script with registry modifications
    # Script path: tempfile + nitrite_telemetry_tweaks.ps1
    # Registry keys modified:
    # - HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection
    # - HKLM:\SOFTWARE\Microsoft\Windows\Windows Error Reporting
    # - HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager
    # - HKLM:\SOFTWARE\Policies\Microsoft\Windows\System
```

#### SUBSECTION B: SERVICES OPTIMIZATION (Lines 2101-2161)
```python
# Line 2101: Services section creation
def _create_services_section(self, parent):
    # Two buttons:
    # - "🔧 Ouvrir Services" → services.msc
    # - "⚡ Optimisation Auto" → _optimize_services()

# Line 2355: Service optimization with selection dialog
def _optimize_services(self):
    # Creates popup window with 15+ checkboxes:
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

#### SUBSECTION C: STARTUP MANAGEMENT (Lines 2162-2206)
```python
# Line 2162: Startup section
def _create_startup_section(self, parent):
    # Button: "📋 Ouvrir Gestionnaire Démarrage"
    # Command: os.system("start ms-settings:startupapps")
```

#### SUBSECTION D: REGISTRY CLEANUP (Lines 2208-2267)
```python
# Line 2208: Registry section
def _create_registry_section(self, parent):
    # Two buttons:
    # - "🔍 Ouvrir Éditeur Registre" → regedit
    # - "🧹 Nettoyage Auto" → _auto_cleanup()
```

---

### 3. AUTO CLEANUP FUNCTION (Lines 2519-2700+)
**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/advanced_pages.py`

```python
def _auto_cleanup(self):
    """Nettoyage automatique du système"""
    # Cleanup operations:
    # 1. %TEMP% folder cleanup (Line 2579-2609)
    # 2. Recycle bin empty via PowerShell (Line 2611-2627)
    # 3. Windows Update cache cleanup (Line 2629-2654)
    # 4. Old log files cleanup (Line 2656-2700+)
    
    # Features:
    # - Progress window with logging
    # - Size tracking (MB calculation)
    # - Error handling for locked files
    # - Real-time status updates
```

**Cleanup Paths:**
- `%TEMP%` (Environment variable)
- `%TMP%` (Environment variable)
- `C:\Windows\Temp`
- `C:\Windows\SoftwareDistribution\Download` (Windows Update)
- `C:\Windows\Logs`
- `C:\Windows\Temp\*.log`
- `%TEMP%\*.log`

---

### 4. BACKUP & RESTORATION PAGE
**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/advanced_pages.py`
**Lines:** 1391-1800
**Class:** `BackupPage`

```python
# Line 1391: Class definition
class BackupPage(tk.Frame):
    """Page Backup & Restauration"""

# Line 1443: Restore point section (Lines 1443-1502)
def _create_restore_point_section(self, parent):
    # Buttons:
    # - "🛡️ Créer Point de Restauration" → _create_restore_point()
    # - "📋 Voir Points de Restauration" → _list_restore_points()

# Line 1504: Driver backup section (Lines 1504-1563)
def _create_driver_backup_section(self, parent):
    # Button: "💾 Sauvegarder les Pilotes" → _backup_drivers()

# Line 1565: Application list section
def _create_app_list_section(self, parent):
    # Buttons for exporting application lists
```

---

### 5. DIAGNOSTIC & BENCHMARK PAGE
**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/advanced_pages.py`
**Lines:** 558-1390
**Class:** `DiagnosticPage`

```python
# Line 558: Class definition
class DiagnosticPage(tk.Frame):
    """Page Diagnostic & Benchmark"""

# Line 640: Load diagnostics (Line 640-652)
def _load_diagnostics(self):
    self._create_health_score()        # Line 643
    self._create_system_info()         # Line 646
    self._create_performance_section() # Line 649
    self._create_benchmark_section()   # Line 652

# Line 654: Real-time performance updates
def _start_realtime_updates(self):
    self._update_performance_realtime()

# Line 663: Update every 2 seconds
def _update_performance_realtime(self):
    # CPU monitoring (Line 669)
    # RAM monitoring (Line 677)
    # Disk monitoring (Line 685)
    # Updates every 2000ms (Line 696)
```

**Performance Widgets:**
```python
self.perf_widgets = {
    'cpu_percent': Label widget,
    'cpu_bar': Progress bar,
    'ram_percent': Label widget,
    'ram_bar': Progress bar,
    'disk_percent': Label widget,
    'disk_bar': Progress bar
}
```

---

### 6. SYSTEM TOOLS DATABASE
**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/tools_data_complete.py`
**Function:** `get_all_tools()`

```python
def get_all_tools():
    """Retourne tous les outils organisés par section"""
    # 12 Sections with 548+ tools:
    
    "🔨 Réparation Système": [        # System Repair
        ("🔍 DISM Check", "DISM /Online /Cleanup-Image /CheckHealth"),
        # ... 30+ repair commands
    ],
    
    "🔧 Activation & Téléchargements": [  # Activation & Downloads
        ("⚡ PowerToys", "https://github.com/microsoft/PowerToys/releases/latest"),
        # ... 25+ links
    ],
    
    "🧹 Maintenance & Nettoyage": [   # Maintenance & Cleaning
        ("🧹 Disk Cleanup", "cleanmgr"),
        # ... 15+ cleaning tools
    ],
    
    "📊 Diagnostics & Infos": [...],
    "🔑 Activation": [...],
    "🛠️ Utilities": [...],
    "🎮 Gaming": [...],
    "📚 Development": [...],
    "🌐 Network": [...],
    "🔒 Security": [...],
    "💻 System": [...],
    "📱 Mobile": [...]
```

---

## PAGE NAVIGATION IN GUI

**Location:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/gui_modern_v13.py`
**Lines:** 345-350

```python
# Navigation menu definition
("master_install", "🚀", "Master Installation", "Installation rapide Windows"),
("optimizations", "⚡", "Optimisations", "Tweaks Windows"),
("diagnostics", "🔍", "Diagnostic", "Benchmark système"),
("backup", "💾", "Backup", "Sauvegarde & Restauration"),
```

---

## RENDERING IN PAGES DICTIONARY

**Location:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/gui_modern_v13.py`
**Lines:** 2345-2355

```python
# Create page instances
self.pages['master_install'] = MasterInstallationPage(self.content_area)
self.pages['optimizations'] = OptimizationsPage(self.content_area)
self.pages['diagnostics'] = DiagnosticPage(self.content_area)
self.pages['backup'] = BackupPage(self.content_area)
```

---

## COLOR SCHEME DEFINITION

**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/src/modern_colors.py`

```python
class ModernColors:
    BG_DARK = '#1E1E1E'
    BG_CARD = '#2D2D2D'
    BG_LIGHT = '#3D3D3D'
    
    TEXT_PRIMARY = '#FFFFFF'
    TEXT_SECONDARY = '#A0A0A0'
    
    ORANGE_PRIMARY = '#FF9500'
    ORANGE_DARK = '#E68400'
    
    RED_ERROR = '#FF6B6B'
    BLUE_INFO = '#4A9EFF'
    GREEN_SUCCESS = '#51CF66'
    PURPLE_PREMIUM = '#B365F5'
    YELLOW_WARNING = '#FFD166'
```

---

## API COMMUNICATION (WEB VERSION)

**File:** `/home/user/Nitrite-V.13-Beta-Portable-web-/web/js/api.js`

```javascript
// Current API endpoints in use
class NiTriTeAPI {
    async getApplications()     // GET /api/applications
    async getTools()            // GET /api/tools
    async getProfiles()         // GET /api/profiles
    async getDiagnostics()      // GET /api/diagnostics
    async installApplication()  // POST /api/install
    async executeTool()         // POST /api/tools/execute
    async getFavorites()        // localStorage access
    
    // MISSING ENDPOINTS (need to be added):
    // POST /api/optimize/telemetry
    // POST /api/optimize/services
    // POST /api/system/cleanup
    // POST /api/system/restore-point
    // POST /api/system/backup-drivers
}
```

