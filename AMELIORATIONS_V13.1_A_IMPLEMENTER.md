# Améliorations NiTriTe V13.1 à Implémenter

## 🎯 Liste des améliorations demandées

### 1. ✅ Page Diagnostic - Performances en Temps Réel

**Objectif :** Les barres CPU/RAM/Disque doivent se mettre à jour automatiquement toutes les 2 secondes.

**Modifications dans `src/advanced_pages.py` - Classe `DiagnosticPage` :**

```python
class DiagnosticPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=ModernColors.BG_DARK)
        self.wmi_obj = None
        try:
            self.wmi_obj = wmi.WMI()
        except:
            pass

        # Variables pour stockage des widgets de performance
        self.perf_widgets = {
            'cpu_percent': None,
            'cpu_bar': None,
            'ram_percent': None,
            'ram_bar': None,
            'disk_percent': None,
            'disk_bar': None
        }
        self.update_running = False  # Flag pour arrêter les updates

        self._create_widgets()
        # Démarrer les updates automatiques
        self._start_realtime_updates()

    def _start_realtime_updates(self):
        """Démarrer les mises à jour en temps réel"""
        self.update_running = True
        self._update_performance_realtime()

    def _stop_realtime_updates(self):
        """Arrêter les mises à jour"""
        self.update_running = False

    def _update_performance_realtime(self):
        """Mettre à jour les performances en temps réel"""
        if not self.update_running:
            return

        try:
            # Mettre à jour CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            if self.perf_widgets['cpu_percent']:
                self.perf_widgets['cpu_percent'].config(text=f"{cpu_percent:.1f}%")
            if self.perf_widgets['cpu_bar']:
                self.perf_widgets['cpu_bar'].place(x=0, y=0, relwidth=cpu_percent/100, relheight=1)

            # Mettre à jour RAM
            ram = psutil.virtual_memory()
            if self.perf_widgets['ram_percent']:
                self.perf_widgets['ram_percent'].config(text=f"{ram.percent:.1f}%")
            if self.perf_widgets['ram_bar']:
                self.perf_widgets['ram_bar'].place(x=0, y=0, relwidth=ram.percent/100, relheight=1)

            # Mettre à jour Disque
            disk = psutil.disk_usage('C:\\' if platform.system() == 'Windows' else '/')
            if self.perf_widgets['disk_percent']:
                self.perf_widgets['disk_percent'].config(text=f"{disk.percent:.1f}%")
            if self.perf_widgets['disk_bar']:
                self.perf_widgets['disk_bar'].place(x=0, y=0, relwidth=disk.percent/100, relheight=1)

        except Exception as e:
            pass  # Ignorer les erreurs

        # Relancer dans 2 secondes
        self.after(2000, self._update_performance_realtime)

    def _create_performance_bar(self, parent, label, percent, color):
        """Créer une barre de performance avec widgets storés"""
        container = tk.Frame(parent, bg=ModernColors.BG_CARD)
        container.pack(fill=tk.X, pady=5)

        # Label et pourcentage
        top_row = tk.Frame(container, bg=ModernColors.BG_CARD)
        top_row.pack(fill=tk.X, pady=(0, 5))

        label_widget = tk.Label(
            top_row,
            text=label,
            font=("Segoe UI", 11, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_PRIMARY
        )
        label_widget.pack(side=tk.LEFT)

        percent_widget = tk.Label(
            top_row,
            text=f"{percent:.1f}%",
            font=("Segoe UI", 11, "bold"),
            bg=ModernColors.BG_CARD,
            fg=color
        )
        percent_widget.pack(side=tk.RIGHT)

        # Barre de progression
        bar_bg = tk.Frame(container, bg=ModernColors.BG_LIGHT, height=20)
        bar_bg.pack(fill=tk.X)

        bar_fill = tk.Frame(bar_bg, bg=color, height=20)
        bar_fill.place(x=0, y=0, relwidth=percent/100, relheight=1)

        # Stocker les références pour update en temps réel
        if label.lower() == 'cpu':
            self.perf_widgets['cpu_percent'] = percent_widget
            self.perf_widgets['cpu_bar'] = bar_fill
        elif label.lower() == 'ram':
            self.perf_widgets['ram_percent'] = percent_widget
            self.perf_widgets['ram_bar'] = bar_fill
        elif label.lower() == 'disque':
            self.perf_widgets['disk_percent'] = percent_widget
            self.perf_widgets['disk_bar'] = bar_fill

    def destroy(self):
        """Arrêter les updates avant destruction"""
        self._stop_realtime_updates()
        super().destroy()
```

---

### 2. ✅ Page Diagnostic - Informations Système Complètes

**Objectif :** Afficher les VRAIES informations : CPU exact, RAM, GPU, Disque (type SSD/HDD/NVMe), Version OS

**Remplacer la méthode `_create_system_info()` :**

```python
def _create_system_info(self):
    """Créer les informations système COMPLÈTES"""
    card = tk.Frame(self.scrollable_frame, bg=ModernColors.BG_CARD)
    card.pack(fill=tk.X, pady=(0, 20))

    header = tk.Label(
        card,
        text="💻 Informations Système",
        font=("Segoe UI", 16, "bold"),
        bg=ModernColors.BG_CARD,
        fg=ModernColors.BLUE_INFO,
        anchor='w',
        padx=20,
        pady=15
    )
    header.pack(fill=tk.X)

    info_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
    info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

    # Obtenir les VRAIES informations
    system_info = self._get_detailed_system_info()

    for key, value in system_info.items():
        self._create_info_row(info_frame, key, value)

def _get_detailed_system_info(self):
    """Obtenir les informations système détaillées"""
    info = {}

    # OS Version COMPLÈTE
    try:
        import subprocess
        result = subprocess.run(['wmic', 'os', 'get', 'Caption,Version,BuildNumber'],
                              capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            os_info = ' '.join(lines[1].split())
            info["Version OS"] = os_info
        else:
            info["Version OS"] = f"{platform.system()} {platform.release()} (Build {platform.version()})"
    except:
        info["Version OS"] = f"{platform.system()} {platform.release()}"

    # Processeur (NOM EXACT)
    try:
        if PSUTIL_AVAILABLE:
            import subprocess
            result = subprocess.run(['wmic', 'cpu', 'get', 'Name'],
                                  capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                cpu_name = lines[1].strip()
                cpu_count = psutil.cpu_count(logical=False)
                cpu_threads = psutil.cpu_count(logical=True)
                info["Processeur"] = f"{cpu_name}"
                info["Cœurs / Threads"] = f"{cpu_count} cœurs / {cpu_threads} threads"
            else:
                info["Processeur"] = platform.processor()
        else:
            info["Processeur"] = platform.processor()
    except:
        info["Processeur"] = platform.processor()

    # RAM (Capacité totale + Type)
    try:
        if PSUTIL_AVAILABLE:
            ram = psutil.virtual_memory()
            ram_gb = ram.total / (1024**3)
            info["Mémoire RAM"] = f"{ram_gb:.1f} Go ({ram.percent:.1f}% utilisé)"

            # Type de RAM via WMI
            try:
                import subprocess
                result = subprocess.run(['wmic', 'memorychip', 'get', 'Speed,Capacity'],
                                      capture_output=True, text=True)
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    speed = lines[1].split()[0] if lines[1].split() else "N/A"
                    info["Type RAM"] = f"DDR (Speed: {speed} MHz)"
            except:
                pass
    except:
        info["Mémoire RAM"] = "N/A"

    # Carte Graphique (NOM EXACT)
    try:
        import subprocess
        result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'Name,AdapterRAM'],
                              capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            gpu_info = lines[1].strip()
            info["Carte Graphique"] = gpu_info
        else:
            info["Carte Graphique"] = "N/A"
    except:
        info["Carte Graphique"] = "N/A"

    # Processeur Graphique (si GPU intégré Intel/AMD)
    try:
        cpu_name_lower = info.get("Processeur", "").lower()
        if "intel" in cpu_name_lower:
            # Extraire la génération Intel (ex: i7-11700K -> 11ème gen)
            import re
            match = re.search(r'i[357]-(\d{1,2})\d{2,3}', info.get("Processeur", ""))
            if match:
                gen = match.group(1)
                info["GPU Intégré"] = f"Intel UHD Graphics (Gen {gen})"
        elif "amd" in cpu_name_lower:
            if "ryzen" in cpu_name_lower:
                info["GPU Intégré"] = "AMD Radeon Graphics (APU)"
    except:
        pass

    # Disque (Type SSD/HDD/NVMe)
    try:
        import subprocess
        # Obtenir le type de disque
        result = subprocess.run(['wmic', 'diskdrive', 'get', 'Model,MediaType,InterfaceType,Size'],
                              capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        disks = []
        for i, line in enumerate(lines[1:], 1):
            if line.strip():
                parts = line.split()
                if parts:
                    model = ' '.join(parts[:-3]) if len(parts) > 3 else "Unknown"
                    size_bytes = int(parts[-1]) if parts[-1].isdigit() else 0
                    size_gb = size_bytes / (1024**3)

                    # Détecter le type
                    disk_type = "HDD"
                    if "nvme" in model.lower() or "SSD" in model:
                        disk_type = "NVMe SSD" if "nvme" in model.lower() else "SSD"

                    disks.append(f"{model} ({size_gb:.0f} Go, {disk_type})")

        if disks:
            info["Disque(s)"] = "\n".join(disks)
        else:
            # Fallback avec psutil
            if PSUTIL_AVAILABLE:
                disk = psutil.disk_usage('C:\\' if platform.system() == 'Windows' else '/')
                disk_gb = disk.total / (1024**3)
                info["Disque Principal"] = f"{disk_gb:.0f} Go ({disk.percent:.1f}% utilisé)"
    except:
        if PSUTIL_AVAILABLE:
            disk = psutil.disk_usage('C:\\' if platform.system() == 'Windows' else '/')
            disk_gb = disk.total / (1024**3)
            info["Disque"] = f"{disk_gb:.0f} Go"

    return info
```

---

### 3. ✅ Page Paramètres - Choix Langue et Mode Sombre/Clair

**Ajouter dans `SettingsPage` :**

```python
def _create_language_section(self, parent):
    """Section choix de langue"""
    card = tk.Frame(parent, bg=ModernColors.BG_CARD)
    card.pack(fill=tk.X, pady=(0, 20))

    header = tk.Label(
        card,
        text="🌍 Langue / Language",
        font=("Segoe UI", 16, "bold"),
        bg=ModernColors.BG_CARD,
        fg=ModernColors.BLUE_INFO,
        anchor='w',
        padx=20,
        pady=15
    )
    header.pack(fill=tk.X)

    lang_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
    lang_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

    # Français
    fr_btn = tk.Button(
        lang_frame,
        text="🇫🇷 Français",
        font=("Segoe UI", 12, "bold"),
        bg=ModernColors.ORANGE_PRIMARY,
        fg=ModernColors.TEXT_PRIMARY,
        activebackground=ModernColors.ORANGE_DARK,
        relief=tk.FLAT,
        cursor="hand2",
        padx=20,
        pady=10,
        command=lambda: self._change_language('fr')
    )
    fr_btn.pack(side=tk.LEFT, padx=5)

    # English
    en_btn = tk.Button(
        lang_frame,
        text="🇬🇧 English",
        font=("Segoe UI", 12, "bold"),
        bg=ModernColors.BLUE_INFO,
        fg=ModernColors.TEXT_PRIMARY,
        activebackground=ModernColors.ORANGE_DARK,
        relief=tk.FLAT,
        cursor="hand2",
        padx=20,
        pady=10,
        command=lambda: self._change_language('en')
    )
    en_btn.pack(side=tk.LEFT, padx=5)

def _change_language(self, lang):
    """Changer la langue de l'application"""
    from translations import set_language
    set_language(lang)

    # Sauvegarder dans config
    try:
        config_path = self._get_config_path()
        config = {}
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

        config['language'] = lang

        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)

        messagebox.showinfo(
            "Langue changée",
            "Redémarrez l'application pour appliquer la nouvelle langue.\n\n"
            "Restart the application to apply the new language."
        )
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")

def _create_appearance_section(self, parent):
    """Section apparence (mode sombre/clair)"""
    card = tk.Frame(parent, bg=ModernColors.BG_CARD)
    card.pack(fill=tk.X, pady=(0, 20))

    header = tk.Label(
        card,
        text="🎨 Apparence",
        font=("Segoe UI", 16, "bold"),
        bg=ModernColors.BG_CARD,
        fg=ModernColors.PURPLE_PREMIUM,
        anchor='w',
        padx=20,
        pady=15
    )
    header.pack(fill=tk.X)

    appearance_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
    appearance_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

    # Mode sombre / clair
    tk.Label(
        appearance_frame,
        text="Mode d'affichage :",
        font=("Segoe UI", 11),
        bg=ModernColors.BG_CARD,
        fg=ModernColors.TEXT_PRIMARY
    ).grid(row=0, column=0, sticky='w', pady=5)

    mode_var = tk.StringVar(value="dark")

    dark_radio = tk.Radiobutton(
        appearance_frame,
        text="🌙 Mode Sombre",
        variable=mode_var,
        value="dark",
        font=("Segoe UI", 10),
        bg=ModernColors.BG_CARD,
        fg=ModernColors.TEXT_PRIMARY,
        selectcolor=ModernColors.BG_DARK,
        activebackground=ModernColors.BG_CARD,
        command=lambda: self._apply_mode("dark")
    )
    dark_radio.grid(row=0, column=1, padx=10)

    light_radio = tk.Radiobutton(
        appearance_frame,
        text="☀️ Mode Clair",
        variable=mode_var,
        value="light",
        font=("Segoe UI", 10),
        bg=ModernColors.BG_CARD,
        fg=ModernColors.TEXT_PRIMARY,
        selectcolor=ModernColors.BG_DARK,
        activebackground=ModernColors.BG_CARD,
        command=lambda: self._apply_mode("light")
    )
    light_radio.grid(row=0, column=2, padx=10)

def _apply_mode(self, mode):
    """Appliquer mode sombre ou clair"""
    if mode == "dark":
        ThemeManager.apply_theme("dark_orange", self.root)
    else:
        ThemeManager.apply_theme("light_orange", self.root)

    messagebox.showinfo(
        "Thème appliqué",
        f"Mode {'sombre' if mode == 'dark' else 'clair'} appliqué !"
    )
```

---

### 4. ✅ Master Installation - Ajout bouton winver

**Dans `src/gui_modern_v13.py`, trouver la classe `MasterInstallationPage` et ajouter :**

```python
def _create_quick_actions(self):
    """Créer les actions rapides"""
    card = tk.Frame(self.scrollable_frame, bg=ModernColors.BG_CARD)
    card.pack(fill=tk.X, pady=(0, 20))

    header = tk.Label(
        card,
        text="⚡ Actions Rapides",
        font=("Segoe UI", 16, "bold"),
        bg=ModernColors.BG_CARD,
        fg=ModernColors.ORANGE_PRIMARY,
        anchor='w',
        padx=20,
        pady=15
    )
    header.pack(fill=tk.X)

    buttons_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
    buttons_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

    # Bouton winver
    winver_btn = tk.Button(
        buttons_frame,
        text="🪟 Version Windows (winver)",
        font=("Segoe UI", 11, "bold"),
        bg=ModernColors.BLUE_INFO,
        fg=ModernColors.TEXT_PRIMARY,
        activebackground=ModernColors.ORANGE_DARK,
        relief=tk.FLAT,
        cursor="hand2",
        padx=20,
        pady=12,
        command=lambda: os.system('winver')
    )
    winver_btn.pack(side=tk.LEFT, padx=5)

    # Autres actions rapides...
    # Ajoutez d'autres boutons ici si besoin
```

---

### 5. ✅ Scroll avec Roulette Partout

**C'EST DÉJÀ FAIT!** La fonction `bind_mousewheel()` est utilisée dans toutes les pages avec scroll.

Vérifier dans chaque page qu'on a bien :

```python
bind_mousewheel(canvas, scrollable_frame)
```

---

## 📋 Instructions d'Implémentation

### Étape 1 : Traduire l'application

1. Le fichier `src/translations.py` est créé ✅
2. Dans chaque page, importer : `from translations import _`
3. Remplacer les textes par : `_(key)`

### Étape 2 : Améliorer DiagnosticPage

1. Copier le code de la section 1 ci-dessus
2. Remplacer les méthodes dans `src/advanced_pages.py`
3. Tester que les performances se mettent à jour en temps réel

### Étape 3 : Améliorer SettingsPage

1. Copier les sections langue et apparence
2. Les ajouter dans `_create_widgets()` de SettingsPage
3. Tester le changement de langue

### Étape 4 : Ajouter winver

1. Trouver MasterInstallationPage dans `src/gui_modern_v13.py`
2. Ajouter la méthode `_create_quick_actions()`
3. L'appeler dans `_create_widgets()`

---

## 🧪 Tests

### Test Diagnostic
```python
python nitrite_v13_modern.py
# Aller sur Diagnostic
# Vérifier que CPU/RAM/Disque s'animent (changent toutes les 2s)
# Vérifier que le nom du CPU est correct
# Vérifier que GPU s'affiche
```

### Test Paramètres
```python
# Aller sur Paramètres
# Cliquer sur 🇬🇧 English
# Redémarrer -> Vérifier que textes sont en anglais
# Changer en Mode Clair -> Vérifier que thème change
```

### Test winver
```python
# Aller sur Master Installation
# Cliquer sur "Version Windows"
# Vérifier que fenêtre winver s'ouvre
```

---

## ✅ Checklist Finale

- [ ] Performances en temps réel (DiagnosticPage)
- [ ] Infos système complètes (CPU, RAM, GPU, Disque)
- [ ] Choix langue FR/EN (SettingsPage)
- [ ] Mode sombre/clair (SettingsPage)
- [ ] Bouton winver (MasterInstallationPage)
- [ ] Scroll roulette (déjà fait)
- [ ] Traduction complète des textes
- [ ] Tests sur Windows 10/11

---

**Voulez-vous que j'implémente ces changements directement dans les fichiers ?**
