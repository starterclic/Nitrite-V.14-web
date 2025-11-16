/**
 * NiTriTe V.13 - Main Application
 * Manages the entire application logic and UI
 */

class NiTriTeApp {
    constructor() {
        this.applications = {};
        this.tools = {};
        this.profiles = [];
        this.favorites = [];
        this.selectedApps = new Set();
        this.currentPage = 'applications';
        this.currentTheme = 'dark';
        this.categories = new Set();
    }

    /**
     * Initialize the application
     */
    async init() {
        console.log('[App] Initializing NiTriTe V.13...');

        // Initialize API
        await window.NiTriTeAPI.init();

        // Load theme
        this.loadTheme();

        // Load data
        await this.loadData();

        // Setup UI
        this.setupNavigation();
        this.setupSearch();
        this.setupActionButtons();
        this.setupThemeToggle();

        // Render initial page
        this.renderApplicationsPage();

        console.log('[App] Initialization complete!');
    }

    /**
     * Load all data
     */
    async loadData() {
        console.log('[App] Loading data...');

        // Load applications
        const appsData = await window.NiTriTeAPI.getApplications();
        this.parseApplications(appsData);

        // Load tools from JSON file
        try {
            const toolsResponse = await fetch('data/tools.json');
            this.tools = await toolsResponse.json();
            console.log(`[App] Loaded ${this.tools.length} tool sections with ${this.tools.reduce((sum, s) => sum + s.tools.length, 0)} tools`);
        } catch (error) {
            console.error('[App] Failed to load tools:', error);
            this.tools = [];
        }

        // Load profiles
        this.profiles = await window.NiTriTeAPI.getProfiles();

        // Load favorites
        this.favorites = await window.NiTriTeAPI.getFavorites();

        console.log(`[App] Loaded ${this.getTotalAppsCount()} applications, ${this.categories.size} categories`);
    }

    /**
     * Parse applications from JSON data
     */
    parseApplications(data) {
        this.applications = data;

        // Extract all categories
        Object.keys(data).forEach(category => {
            this.categories.add(category);
        });

        // Populate category filter
        this.populateCategoryFilter();
    }

    /**
     * Get total number of applications
     */
    getTotalAppsCount() {
        let count = 0;
        Object.values(this.applications).forEach(category => {
            count += Object.keys(category).length;
        });
        return count;
    }

    /**
     * Get all apps as flat array
     */
    getAllAppsArray() {
        const apps = [];
        Object.entries(this.applications).forEach(([category, categoryApps]) => {
            Object.entries(categoryApps).forEach(([name, app]) => {
                apps.push({
                    id: this.generateAppId(name, category),
                    name,
                    category,
                    ...app
                });
            });
        });
        return apps;
    }

    /**
     * Generate unique app ID
     */
    generateAppId(name, category) {
        return `${category}_${name}`.replace(/[^a-zA-Z0-9]/g, '_').toLowerCase();
    }

    /**
     * Setup navigation
     */
    setupNavigation() {
        const navItems = document.querySelectorAll('.nav-item');

        navItems.forEach(item => {
            item.addEventListener('click', () => {
                const page = item.getAttribute('data-page');
                this.navigateToPage(page);
            });
        });
    }

    /**
     * Navigate to a specific page
     */
    navigateToPage(pageName) {
        // Update nav items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('data-page') === pageName) {
                item.classList.add('active');
            }
        });

        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });

        // Show target page
        const targetPage = document.getElementById(`${pageName}Page`);
        if (targetPage) {
            targetPage.classList.add('active');
            this.currentPage = pageName;

            // Render page content
            this.renderCurrentPage();
        }
    }

    /**
     * Render current page content
     */
    renderCurrentPage() {
        switch (this.currentPage) {
            case 'applications':
                this.renderApplicationsPage();
                break;
            case 'tools':
                this.renderToolsPage();
                break;
            case 'profiles':
                this.renderProfilesPage();
                break;
            case 'master':
                this.renderMasterPage();
                break;
            case 'favorites':
                this.renderFavoritesPage();
                break;
            case 'diagnostic':
                this.renderDiagnosticPage();
                break;
            case 'optimization':
                this.renderOptimizationPage();
                break;
            case 'backup':
                this.renderBackupPage();
                break;
            case 'updates':
                // Updates page is already rendered in HTML with inline buttons
                console.log('[App] Updates page loaded');
                break;
            case 'settings':
                this.renderSettingsPage();
                break;
            default:
                console.log(`[App] Page ${this.currentPage} not implemented yet`);
        }
    }

    /**
     * Render applications page
     */
    renderApplicationsPage() {
        const grid = document.getElementById('applicationsGrid');
        if (!grid) return;

        grid.innerHTML = '';

        const apps = this.getAllAppsArray();
        const searchTerm = document.getElementById('searchInput')?.value.toLowerCase() || '';
        const categoryFilter = document.getElementById('categoryFilter')?.value || 'all';
        const sourceFilter = document.getElementById('sourceFilter')?.value || 'all';

        // Filter apps
        const filteredApps = apps.filter(app => {
            // Search filter
            if (searchTerm && !app.name.toLowerCase().includes(searchTerm) &&
                !app.description.toLowerCase().includes(searchTerm)) {
                return false;
            }

            // Category filter
            if (categoryFilter !== 'all' && app.category !== categoryFilter) {
                return false;
            }

            // Source filter
            if (sourceFilter !== 'all') {
                if (sourceFilter === 'winget' && !app.winget_id) return false;
                if (sourceFilter === 'portable' && !app.portable_url) return false;
                if (sourceFilter === 'download' && !app.download_url) return false;
            }

            return true;
        });

        // Render filtered apps
        filteredApps.forEach(app => {
            const card = this.createAppCard(app);
            grid.appendChild(card);
        });

        // Update stats
        this.updateStats();
    }

    /**
     * Create app card element
     */
    createAppCard(app) {
        const card = document.createElement('div');
        card.className = 'app-card';
        card.setAttribute('data-app-id', app.id);

        if (this.selectedApps.has(app.id)) {
            card.classList.add('selected');
        }

        // Determine source badges
        const badges = [];
        if (app.portable_url) badges.push('<span class="badge badge-portable">Portable</span>');
        if (app.winget_id) badges.push('<span class="badge badge-winget">WinGet</span>');
        if (app.download_url && !app.portable_url) badges.push('<span class="badge badge-download">Download</span>');

        // Check if favorite
        const isFavorite = this.favorites.includes(app.id);
        const favoriteIcon = isFavorite ? '⭐' : '☆';

        card.innerHTML = `
            <div class="app-card-header">
                <div class="app-icon">📦</div>
                <div class="app-info">
                    <div class="app-name">${app.name}</div>
                    <div class="app-category">${app.category}</div>
                </div>
            </div>
            <div class="app-badges">
                ${badges.join('')}
            </div>
            <div class="app-description">${app.description}</div>
            <div class="app-actions">
                <button class="app-btn" onclick="window.NiTriTeApp.installApp('${app.id}')">
                    📥 Installer
                </button>
                <button class="app-btn-icon" onclick="window.NiTriTeApp.toggleFavorite('${app.id}')" title="Favoris">
                    ${favoriteIcon}
                </button>
                ${app.website ? `<button class="app-btn-icon" onclick="window.open('${app.website}', '_blank')" title="Site web">🌐</button>` : ''}
            </div>
        `;

        // Toggle selection on click
        card.addEventListener('click', (e) => {
            if (!e.target.closest('button')) {
                this.toggleAppSelection(app.id);
            }
        });

        return card;
    }

    /**
     * Toggle app selection
     */
    toggleAppSelection(appId) {
        if (this.selectedApps.has(appId)) {
            this.selectedApps.delete(appId);
        } else {
            this.selectedApps.add(appId);
        }

        // Update card visual
        const card = document.querySelector(`[data-app-id="${appId}"]`);
        if (card) {
            card.classList.toggle('selected');
        }

        this.updateStats();
    }

    /**
     * Toggle favorite
     */
    async toggleFavorite(appId) {
        if (this.favorites.includes(appId)) {
            await window.NiTriTeAPI.removeFavorite(appId);
            this.favorites = this.favorites.filter(id => id !== appId);
        } else {
            await window.NiTriTeAPI.addFavorite(appId);
            this.favorites.push(appId);
        }

        // Update badge
        document.getElementById('favoritesBadge').textContent = this.favorites.length;

        // Re-render if on applications or favorites page
        if (this.currentPage === 'applications' || this.currentPage === 'favorites') {
            this.renderCurrentPage();
        }
    }

    /**
     * Install app
     */
    async installApp(appId) {
        console.log(`[App] Installing ${appId}...`);

        // Show modal
        const modal = document.getElementById('installModal');
        modal.classList.add('active');

        try {
            const result = await window.NiTriTeAPI.installApplication(appId);
            console.log('[App] Installation result:', result);
            alert(`Installation lancée pour ${appId}`);
        } catch (error) {
            console.error('[App] Installation failed:', error);
            alert(`Erreur lors de l'installation: ${error.message}`);
        } finally {
            modal.classList.remove('active');
        }
    }

    /**
     * Render tools page
     */
    renderToolsPage() {
        const container = document.getElementById('toolsContainer');
        if (!container) return;

        if (!this.tools || this.tools.length === 0) {
            container.innerHTML = '<p style="color: var(--text-secondary); padding: 20px; text-align: center;">Chargement des outils...</p>';
            return;
        }

        container.innerHTML = `
            <div class="tools-header">
                <h2>🛠️ Outils Système</h2>
                <p class="tools-subtitle">${this.tools.reduce((sum, s) => sum + s.tools.length, 0)} outils répartis en ${this.tools.length} catégories</p>
            </div>
        `;

        this.tools.forEach(section => {
            const sectionEl = this.createToolSection(section);
            container.appendChild(sectionEl);
        });
    }

    /**
     * Create tool section
     */
    createToolSection(section) {
        const div = document.createElement('div');
        div.className = 'tool-section';

        const toolsHTML = section.tools.map((tool, index) => {
            const isUrl = tool.command.startsWith('http://') || tool.command.startsWith('https://');
            const isCommand = !isUrl;

            return `
                <button class="tool-btn ${isUrl ? 'tool-btn-url' : 'tool-btn-command'}"
                        onclick="window.NiTriTeApp.executeTool(${JSON.stringify(tool).replace(/"/g, '&quot;')})">
                    <span class="tool-btn-text">${tool.name}</span>
                    ${isUrl ? '<span class="tool-btn-indicator">🌐</span>' : '<span class="tool-btn-indicator">⚡</span>'}
                </button>
            `;
        }).join('');

        div.innerHTML = `
            <div class="tool-section-header">
                <h3 class="tool-section-title">${section.title}</h3>
                <span class="tool-section-count">${section.tools.length} outils</span>
            </div>
            <div class="tool-grid">
                ${toolsHTML}
            </div>
        `;

        return div;
    }

    /**
     * Execute tool
     */
    async executeTool(tool) {
        console.log(`[App] Executing tool:`, tool);

        const isUrl = tool.command.startsWith('http://') || tool.command.startsWith('https://');

        if (isUrl) {
            // Open URL in new tab
            window.open(tool.command, '_blank');
        } else {
            // Execute command via API
            try {
                const result = await window.NiTriTeAPI.executeCommand(tool.command);
                console.log('[App] Command execution result:', result);

                if (result.status === 'success') {
                    alert(`✅ ${tool.name}\n\nCommande exécutée avec succès`);
                } else {
                    alert(`⚠️ ${tool.name}\n\n${result.message || 'Commande exécutée'}`);
                }
            } catch (error) {
                console.error('[App] Command execution failed:', error);
                alert(`❌ Erreur lors de l'exécution de ${tool.name}\n\n${error.message}`);
            }
        }
    }

    /**
     * Render profiles page
     */
    renderProfilesPage() {
        const grid = document.getElementById('profilesGrid');
        if (!grid) return;

        grid.innerHTML = '';

        this.profiles.forEach(profile => {
            const card = this.createProfileCard(profile);
            grid.appendChild(card);
        });
    }

    /**
     * Create profile card
     */
    createProfileCard(profile) {
        const card = document.createElement('div');
        card.className = 'profile-card';

        card.innerHTML = `
            <div class="profile-icon">${profile.icon}</div>
            <div class="profile-name">${profile.name}</div>
            <div class="profile-description">${profile.description}</div>
            <div class="profile-apps-count">${profile.apps_count} applications</div>
        `;

        card.addEventListener('click', () => {
            this.loadProfile(profile.id);
        });

        return card;
    }

    /**
     * Load profile
     */
    loadProfile(profileId) {
        console.log(`[App] Loading profile ${profileId}...`);
        alert(`Chargement du profil ${profileId}...`);
    }

    /**
     * Render favorites page
     */
    renderFavoritesPage() {
        const grid = document.getElementById('favoritesGrid');
        if (!grid) return;

        grid.innerHTML = '';

        const allApps = this.getAllAppsArray();
        const favoriteApps = allApps.filter(app => this.favorites.includes(app.id));

        if (favoriteApps.length === 0) {
            grid.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 40px;">Aucune application favorite</p>';
            return;
        }

        favoriteApps.forEach(app => {
            const card = this.createAppCard(app);
            grid.appendChild(card);
        });
    }

    /**
     * Render diagnostic page
     */
    async renderDiagnosticPage() {
        const content = document.getElementById('diagnosticContent');
        if (!content) return;

        const diagnostics = await window.NiTriTeAPI.getDiagnostics();

        content.innerHTML = `
            <div style="background: var(--bg-secondary); padding: 20px; border-radius: 12px;">
                <h3 style="margin-bottom: 15px;">Informations Système</h3>
                <p><strong>OS:</strong> ${diagnostics.system.os}</p>
                <p><strong>CPU:</strong> ${diagnostics.system.cpu}</p>
                <p><strong>RAM:</strong> ${diagnostics.system.ram}</p>
                <p><strong>Disque:</strong> ${diagnostics.system.disk}</p>
                <p style="margin-top: 20px; color: var(--text-secondary);">${diagnostics.status}</p>
            </div>
        `;
    }

    /**
     * Render settings page
     */
    renderSettingsPage() {
        const content = document.getElementById('settingsContent');
        if (!content) return;

        content.innerHTML = `
            <div class="settings-sections">
                <!-- Language Section -->
                <div class="settings-section">
                    <h3>🌐 Langue / Language</h3>
                    <p class="section-description">Choisissez la langue de l'interface</p>
                    <div class="language-buttons">
                        <button class="btn btn-secondary lang-btn active" onclick="window.NiTriTeApp.setLanguage('fr')">
                            🇫🇷 Français
                        </button>
                        <button class="btn btn-secondary lang-btn" onclick="window.NiTriTeApp.setLanguage('en')">
                            🇬🇧 English
                        </button>
                    </div>
                    <p style="margin-top: 10px; font-size: 0.9em; color: var(--text-secondary);">
                        ℹ️ L'application sera rechargée pour appliquer les changements
                    </p>
                </div>

                <!-- Theme Section -->
                <div class="settings-section">
                    <h3>🎨 Thèmes</h3>
                    <p class="section-description">Personnalisez l'apparence de l'application</p>
                    <div class="themes-grid">
                        <div class="theme-card" onclick="window.NiTriTeApp.setTheme('dark')">
                            <div class="theme-preview dark-theme-preview">
                                <div class="preview-bar"></div>
                                <div class="preview-content"></div>
                            </div>
                            <h4>Sombre</h4>
                            <p>Thème par défaut</p>
                        </div>
                        <div class="theme-card" onclick="window.NiTriTeApp.setTheme('light')">
                            <div class="theme-preview light-theme-preview">
                                <div class="preview-bar"></div>
                                <div class="preview-content"></div>
                            </div>
                            <h4>Clair</h4>
                            <p>Pour plus de luminosité</p>
                        </div>
                        <div class="theme-card" onclick="window.NiTriTeApp.setTheme('dark-blue')">
                            <div class="theme-preview dark-blue-theme-preview">
                                <div class="preview-bar"></div>
                                <div class="preview-content"></div>
                            </div>
                            <h4>Sombre Bleu</h4>
                            <p>Accent bleu</p>
                        </div>
                        <div class="theme-card" onclick="window.NiTriTeApp.setTheme('light-blue')">
                            <div class="theme-preview light-blue-theme-preview">
                                <div class="preview-bar"></div>
                                <div class="preview-content"></div>
                            </div>
                            <h4>Clair Bleu</h4>
                            <p>Tons bleus clairs</p>
                        </div>
                        <div class="theme-card" onclick="window.NiTriTeApp.setTheme('dark-purple')">
                            <div class="theme-preview dark-purple-theme-preview">
                                <div class="preview-bar"></div>
                                <div class="preview-content"></div>
                            </div>
                            <h4>Sombre Violet</h4>
                            <p>Accent violet</p>
                        </div>
                        <div class="theme-card" onclick="window.NiTriTeApp.setTheme('dark-orange')">
                            <div class="theme-preview dark-orange-theme-preview">
                                <div class="preview-bar"></div>
                                <div class="preview-content"></div>
                            </div>
                            <h4>Sombre Orange</h4>
                            <p>Thème original</p>
                        </div>
                    </div>
                </div>

                <!-- App Settings Section -->
                <div class="settings-section">
                    <h3>⚙️ Paramètres de l'Application</h3>
                    <p class="section-description">Gérez les données et les préférences</p>
                    <div class="settings-actions">
                        <button class="btn btn-secondary" onclick="window.NiTriTeApp.clearCache()">
                            🗑️ Effacer le cache
                        </button>
                        <button class="btn btn-secondary" onclick="window.NiTriTeApp.exportSettings()">
                            💾 Exporter les paramètres
                        </button>
                        <button class="btn btn-secondary" onclick="window.NiTriTeApp.importSettings()">
                            📥 Importer les paramètres
                        </button>
                    </div>
                </div>

                <!-- About Section -->
                <div class="settings-section">
                    <h3>ℹ️ À propos</h3>
                    <p class="section-description">Informations sur l'application</p>
                    <div class="about-info">
                        <p><strong>NiTriTe V.13 Beta</strong></p>
                        <p>Gestionnaire d'Applications et Outils Système</p>
                        <p style="margin-top: 10px; color: var(--text-secondary);">
                            Version Web - Portée depuis la version Bureau
                        </p>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Setup search functionality
     */
    setupSearch() {
        const searchInput = document.getElementById('searchInput');
        const categoryFilter = document.getElementById('categoryFilter');
        const sourceFilter = document.getElementById('sourceFilter');

        if (searchInput) {
            searchInput.addEventListener('input', () => {
                if (this.currentPage === 'applications') {
                    this.renderApplicationsPage();
                }
            });
        }

        if (categoryFilter) {
            categoryFilter.addEventListener('change', () => {
                if (this.currentPage === 'applications') {
                    this.renderApplicationsPage();
                }
            });
        }

        if (sourceFilter) {
            sourceFilter.addEventListener('change', () => {
                if (this.currentPage === 'applications') {
                    this.renderApplicationsPage();
                }
            });
        }
    }

    /**
     * Populate category filter
     */
    populateCategoryFilter() {
        const select = document.getElementById('categoryFilter');
        if (!select) return;

        // Keep "all" option
        select.innerHTML = '<option value="all">Toutes les catégories</option>';

        // Add category options
        Array.from(this.categories).sort().forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            select.appendChild(option);
        });
    }

    /**
     * Setup action buttons
     */
    setupActionButtons() {
        const installSelected = document.getElementById('installSelected');
        const selectAll = document.getElementById('selectAll');
        const deselectAll = document.getElementById('deselectAll');
        const exportSelection = document.getElementById('exportSelection');
        const importSelection = document.getElementById('importSelection');

        if (installSelected) {
            installSelected.addEventListener('click', () => {
                this.installSelectedApps();
            });
        }

        if (selectAll) {
            selectAll.addEventListener('click', () => {
                this.selectAllApps();
            });
        }

        if (deselectAll) {
            deselectAll.addEventListener('click', () => {
                this.deselectAllApps();
            });
        }

        if (exportSelection) {
            exportSelection.addEventListener('click', () => {
                this.exportSelection();
            });
        }

        if (importSelection) {
            importSelection.addEventListener('click', () => {
                this.importAndInstallSelection();
            });
        }
    }

    /**
     * Install selected apps
     */
    async installSelectedApps() {
        if (this.selectedApps.size === 0) {
            alert('Aucune application sélectionnée');
            return;
        }

        console.log(`[App] Installing ${this.selectedApps.size} apps...`);
        const appIds = Array.from(this.selectedApps);

        try {
            const result = await window.NiTriTeAPI.installMultiple(appIds);
            console.log('[App] Bulk installation result:', result);
            alert(`Installation lancée pour ${appIds.length} applications`);
        } catch (error) {
            console.error('[App] Bulk installation failed:', error);
            alert(`Erreur lors de l'installation: ${error.message}`);
        }
    }

    /**
     * Select all apps
     */
    selectAllApps() {
        const allApps = this.getAllAppsArray();
        allApps.forEach(app => {
            this.selectedApps.add(app.id);
        });
        this.renderApplicationsPage();
    }

    /**
     * Deselect all apps
     */
    deselectAllApps() {
        this.selectedApps.clear();
        this.renderApplicationsPage();
    }

    /**
     * Export selection
     */
    exportSelection() {
        const selection = Array.from(this.selectedApps);
        const json = JSON.stringify(selection, null, 2);

        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'nitrite_selection.json';
        a.click();
        URL.revokeObjectURL(url);
    }

    /**
     * Import and install selection
     */
    importAndInstallSelection() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';

        input.onchange = async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = async (event) => {
                try {
                    const appIds = JSON.parse(event.target.result);

                    if (!Array.isArray(appIds) || appIds.length === 0) {
                        alert('❌ Fichier invalide ou vide');
                        return;
                    }

                    if (!confirm(`📂 Importer et installer ${appIds.length} application(s)?\n\nContinuer?`)) {
                        return;
                    }

                    // Add apps to selection
                    appIds.forEach(id => this.selectedApps.add(id));
                    this.renderApplicationsPage();

                    // Install imported apps
                    try {
                        const result = await window.NiTriTeAPI.installMultiple(appIds);
                        console.log('[App] Import installation result:', result);
                        alert(`✅ Installation lancée pour ${appIds.length} applications`);
                    } catch (error) {
                        console.error('[App] Import installation failed:', error);
                        alert(`❌ Erreur lors de l'installation: ${error.message}`);
                    }
                } catch (error) {
                    console.error('Error importing selection:', error);
                    alert('❌ Erreur lors de l\'import\n\nFichier invalide.');
                }
            };
            reader.readAsText(file);
        };

        input.click();
    }

    /**
     * Setup theme toggle
     */
    setupThemeToggle() {
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }
    }

    /**
     * Load theme
     */
    loadTheme() {
        this.currentTheme = window.NiTriTeAPI.getTheme();
        this.applyTheme();
    }

    /**
     * Set theme
     */
    setTheme(theme) {
        this.currentTheme = theme;
        window.NiTriTeAPI.setTheme(theme);
        this.applyTheme();
    }

    /**
     * Toggle theme
     */
    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    /**
     * Apply theme
     */
    applyTheme() {
        if (this.currentTheme === 'light') {
            document.body.classList.add('light-theme');
            document.getElementById('themeIcon').textContent = '☀️';
        } else {
            document.body.classList.remove('light-theme');
            document.getElementById('themeIcon').textContent = '🌙';
        }
    }

    /**
     * Update stats
     */
    updateStats() {
        const totalApps = this.getTotalAppsCount();
        const totalCategories = this.categories.size;
        const selectedApps = this.selectedApps.size;

        document.getElementById('totalApps').textContent = totalApps;
        document.getElementById('totalCategories').textContent = totalCategories;
        document.getElementById('selectedApps').textContent = selectedApps;
        document.getElementById('appsBadge').textContent = totalApps;
        document.getElementById('favoritesBadge').textContent = this.favorites.length;

        // Enable/disable install button
        const installBtn = document.getElementById('installSelected');
        if (installBtn) {
            installBtn.disabled = selectedApps === 0;
        }
    }

    /**
     * Clear cache
     */
    clearCache() {
        localStorage.clear();
        alert('Cache effacé ! Rechargez la page.');
        location.reload();
    }

    /**
     * Set language
     */
    setLanguage(lang) {
        if (!confirm(`Changer la langue en ${lang === 'fr' ? 'Français' : 'English'}?\n\nL'application sera rechargée.`)) {
            return;
        }
        localStorage.setItem('nitrite_language', lang);
        alert(`Langue changée en ${lang === 'fr' ? 'Français' : 'English'}!\n\nNote: La traduction complète sera implémentée prochainement.`);
        location.reload();
    }

    /**
     * Export settings
     */
    exportSettings() {
        const settings = {
            theme: this.currentTheme,
            language: localStorage.getItem('nitrite_language') || 'fr',
            favorites: this.favorites,
            selectedApps: Array.from(this.selectedApps),
            exportDate: new Date().toISOString()
        };

        const json = JSON.stringify(settings, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `nitrite_settings_${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);

        alert('✅ Paramètres exportés avec succès!');
    }

    /**
     * Import settings
     */
    importSettings() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';

        input.onchange = (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = (event) => {
                try {
                    const settings = JSON.parse(event.target.result);

                    // Apply settings
                    if (settings.theme) {
                        this.setTheme(settings.theme);
                    }
                    if (settings.language) {
                        localStorage.setItem('nitrite_language', settings.language);
                    }
                    if (settings.favorites) {
                        this.favorites = settings.favorites;
                        window.NiTriTeAPI.saveFavorites(this.favorites);
                    }

                    alert('✅ Paramètres importés avec succès!\n\nL\'application va se recharger.');
                    location.reload();
                } catch (error) {
                    console.error('Error importing settings:', error);
                    alert('❌ Erreur lors de l\'import des paramètres\n\nFichier invalide.');
                }
            };
            reader.readAsText(file);
        };

        input.click();
    }
}

// Create global app instance
window.NiTriTeApp = new NiTriTeApp();

// Close modal handlers
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-close') || e.target.classList.contains('modal')) {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.remove('active');
        });
    }
});
