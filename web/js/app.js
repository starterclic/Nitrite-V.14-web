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

        // Load tools
        this.tools = await window.NiTriTeAPI.getTools();

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

        container.innerHTML = '';

        const toolsData = this.tools.sections || this.tools;

        if (Array.isArray(toolsData)) {
            toolsData.forEach(section => {
                const sectionEl = this.createToolSection(section);
                container.appendChild(sectionEl);
            });
        }
    }

    /**
     * Create tool section
     */
    createToolSection(section) {
        const div = document.createElement('div');
        div.className = 'tool-section';

        const toolsHTML = section.tools.map(tool => `
            <button class="tool-btn" onclick="window.NiTriTeApp.executeTool('${tool.id}')">
                <span class="tool-btn-icon">${tool.icon || '🔧'}</span>
                <span>${tool.name}</span>
            </button>
        `).join('');

        div.innerHTML = `
            <div class="tool-section-header">
                <span class="tool-section-icon">${section.icon}</span>
                <h3 class="tool-section-title">${section.title}</h3>
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
    async executeTool(toolId) {
        console.log(`[App] Executing tool ${toolId}...`);

        try {
            const result = await window.NiTriTeAPI.executeTool(toolId);
            console.log('[App] Tool execution result:', result);
            alert(`Outil ${toolId} exécuté`);
        } catch (error) {
            console.error('[App] Tool execution failed:', error);
            alert(`Erreur lors de l'exécution: ${error.message}`);
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
            <div style="background: var(--bg-secondary); padding: 20px; border-radius: 12px;">
                <h3 style="margin-bottom: 15px;">Paramètres de l'Application</h3>
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px;">Thème:</label>
                    <select id="themeSelect" style="padding: 10px; border-radius: 8px; background: var(--bg-tertiary); color: var(--text-primary); border: 1px solid var(--border-color);">
                        <option value="dark" ${this.currentTheme === 'dark' ? 'selected' : ''}>Sombre</option>
                        <option value="light" ${this.currentTheme === 'light' ? 'selected' : ''}>Clair</option>
                    </select>
                </div>
                <div>
                    <button class="btn btn-primary" onclick="window.NiTriTeApp.clearCache()">🗑️ Effacer le cache</button>
                </div>
            </div>
        `;

        document.getElementById('themeSelect')?.addEventListener('change', (e) => {
            this.setTheme(e.target.value);
        });
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
