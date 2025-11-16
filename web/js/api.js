/**
 * NiTriTe V.13 - API Communication Module
 * Handles all backend communications
 */

class NiTriTeAPI {
    constructor() {
        this.baseURL = 'http://localhost:5000/api';
        this.socket = null;
        this.isConnected = false;
    }

    /**
     * Initialize API connection
     */
    async init() {
        try {
            const response = await this.request('/health');
            this.isConnected = response.status === 'ok';
            console.log('[API] Connection established');
            return true;
        } catch (error) {
            console.warn('[API] Backend not available, running in demo mode');
            this.isConnected = false;
            return false;
        }
    }

    /**
     * Make HTTP request to backend
     */
    async request(endpoint, method = 'GET', data = null) {
        const url = `${this.baseURL}${endpoint}`;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('[API] Request failed:', error);
            throw error;
        }
    }

    /**
     * Get all applications from database
     */
    async getApplications() {
        try {
            return await this.request('/applications');
        } catch (error) {
            // Fallback: load from local JSON file
            console.log('[API] Loading applications from local file...');
            const response = await fetch('../data/programs.json');
            return await response.json();
        }
    }

    /**
     * Get system tools data
     */
    async getTools() {
        try {
            return await this.request('/tools');
        } catch (error) {
            console.error('[API] Failed to load tools:', error);
            return this.getDefaultTools();
        }
    }

    /**
     * Get profiles data
     */
    async getProfiles() {
        try {
            return await this.request('/profiles');
        } catch (error) {
            console.error('[API] Failed to load profiles:', error);
            return this.getDefaultProfiles();
        }
    }

    /**
     * Install an application
     */
    async installApplication(appId, method = 'auto') {
        return await this.request('/install', 'POST', {
            app_id: appId,
            method: method
        });
    }

    /**
     * Install multiple applications
     */
    async installMultiple(appIds) {
        return await this.request('/install/bulk', 'POST', {
            app_ids: appIds
        });
    }

    /**
     * Execute a system tool command
     */
    async executeTool(toolId, params = {}) {
        return await this.request('/tools/execute', 'POST', {
            tool_id: toolId,
            params: params
        });
    }

    /**
     * Execute a command directly with UAC bypass
     */
    async executeCommand(command) {
        return await this.request('/execute-command', 'POST', {
            command: command
        });
    }

    /**
     * Get system diagnostics
     */
    async getDiagnostics() {
        try {
            return await this.request('/diagnostics');
        } catch (error) {
            console.error('[API] Failed to get diagnostics:', error);
            return this.getDefaultDiagnostics();
        }
    }

    /**
     * Get user favorites
     */
    async getFavorites() {
        try {
            const favorites = localStorage.getItem('nitrite_favorites');
            return favorites ? JSON.parse(favorites) : [];
        } catch (error) {
            console.error('[API] Failed to load favorites:', error);
            return [];
        }
    }

    /**
     * Add to favorites
     */
    async addFavorite(appId) {
        try {
            const favorites = await this.getFavorites();
            if (!favorites.includes(appId)) {
                favorites.push(appId);
                localStorage.setItem('nitrite_favorites', JSON.stringify(favorites));
            }
            return true;
        } catch (error) {
            console.error('[API] Failed to add favorite:', error);
            return false;
        }
    }

    /**
     * Remove from favorites
     */
    async removeFavorite(appId) {
        try {
            let favorites = await this.getFavorites();
            favorites = favorites.filter(id => id !== appId);
            localStorage.setItem('nitrite_favorites', JSON.stringify(favorites));
            return true;
        } catch (error) {
            console.error('[API] Failed to remove favorite:', error);
            return false;
        }
    }

    /**
     * Get theme preference
     */
    getTheme() {
        return localStorage.getItem('nitrite_theme') || 'dark';
    }

    /**
     * Set theme preference
     */
    setTheme(theme) {
        localStorage.setItem('nitrite_theme', theme);
    }

    /**
     * Default tools data (fallback)
     */
    getDefaultTools() {
        return {
            sections: [
                {
                    id: 'activation',
                    icon: '🔧',
                    title: 'Activation & Téléchargements',
                    tools: [
                        { id: 'kms', name: 'Activation Windows/Office (KMS)', icon: '🔑' },
                        { id: 'rufus', name: 'Rufus (USB Bootable)', icon: '💿' },
                        { id: 'ventoy', name: 'Ventoy', icon: '📀' },
                    ]
                },
                {
                    id: 'repair',
                    icon: '🔨',
                    title: 'Réparation Système',
                    tools: [
                        { id: 'dism', name: 'DISM /RestoreHealth', icon: '🛠️' },
                        { id: 'sfc', name: 'SFC /scannow', icon: '🔍' },
                        { id: 'chkdsk', name: 'CHKDSK', icon: '💾' },
                    ]
                },
                {
                    id: 'maintenance',
                    icon: '🧹',
                    title: 'Maintenance & Nettoyage',
                    tools: [
                        { id: 'cleaner', name: 'Nettoyage Disque', icon: '🗑️' },
                        { id: 'temp', name: 'Nettoyer Fichiers Temporaires', icon: '📁' },
                        { id: 'defrag', name: 'Défragmentation', icon: '📊' },
                    ]
                },
            ]
        };
    }

    /**
     * Default profiles data (fallback)
     */
    getDefaultProfiles() {
        return [
            {
                id: 'gaming',
                name: 'Gaming Station',
                icon: '🎮',
                description: 'Tout pour les joueurs : launchers, Discord, OBS, utilitaires gaming',
                apps_count: 25
            },
            {
                id: 'office',
                name: 'Bureau Professionnel',
                icon: '💼',
                description: 'Suite bureautique complète, outils de productivité et communication',
                apps_count: 30
            },
            {
                id: 'dev',
                name: 'Développeur',
                icon: '💻',
                description: 'IDE, Git, Docker, outils de développement et langages de programmation',
                apps_count: 40
            },
            {
                id: 'media',
                name: 'Création Multimédia',
                icon: '🎨',
                description: 'Outils photo, vidéo, audio, design graphique et création de contenu',
                apps_count: 35
            },
            {
                id: 'student',
                name: 'Étudiant',
                icon: '🏫',
                description: 'Applications éducatives, outils de recherche et productivité étudiante',
                apps_count: 20
            },
            {
                id: 'tech',
                name: 'Maintenance Technique',
                icon: '🔧',
                description: 'Utilitaires système, outils de diagnostic et réparation',
                apps_count: 45
            },
            {
                id: 'home',
                name: 'Maison/Famille',
                icon: '🏠',
                description: 'Applications familiales, multimédia et usage quotidien',
                apps_count: 22
            },
            {
                id: 'express',
                name: 'Installation Express',
                icon: '⚡',
                description: 'Essentiels uniquement : navigateur, PDF, archiveur, antivirus',
                apps_count: 12
            },
            {
                id: 'cinema',
                name: 'Home Cinema',
                icon: '🎬',
                description: 'Lecture multimédia, streaming, gestion de bibliothèque média',
                apps_count: 15
            },
            {
                id: 'remote',
                name: 'Télétravail',
                icon: '🌐',
                description: 'Visioconférence, collaboration, VPN et outils de travail à distance',
                apps_count: 18
            }
        ];
    }

    /**
     * Default diagnostics data (fallback)
     */
    getDefaultDiagnostics() {
        return {
            system: {
                os: 'Windows 10/11',
                cpu: 'Informations non disponibles',
                ram: 'Informations non disponibles',
                disk: 'Informations non disponibles'
            },
            status: 'Backend non connecté - Mode démonstration'
        };
    }
}

// Create global API instance
window.NiTriTeAPI = new NiTriTeAPI();
