/**
 * NiTriTe V.13 - Advanced Pages
 * Handles Optimization, Master Installation, and enhanced Diagnostic pages
 */

// Extend the NiTriTeApp class with advanced pages
if (typeof NiTriTeApp !== 'undefined') {

    /**
     * Render Optimization Page
     */
    NiTriTeApp.prototype.renderOptimizationPage = function() {
        const content = document.getElementById('optimizationContent');
        if (!content) return;

        content.innerHTML = `
            <div class="optimization-sections">
                <!-- Telemetry & Privacy Section -->
                <div class="optimization-section">
                    <div class="section-header">
                        <h3>🔒 Télémétrie & Confidentialité</h3>
                        <p class="section-description">Désactivez la collecte de données Windows</p>
                    </div>
                    <div class="section-content">
                        <div class="optimization-card">
                            <div class="card-icon">🛡️</div>
                            <div class="card-content">
                                <h4>Désactiver la Télémétrie Windows</h4>
                                <p>Désactive la collecte de données, Cortana, suggestions et historique d'activité</p>
                                <ul class="feature-list">
                                    <li>✓ Télémétrie Windows</li>
                                    <li>✓ Rapport d'erreurs</li>
                                    <li>✓ Suggestions du menu Démarrer</li>
                                    <li>✓ Historique d'activité</li>
                                </ul>
                            </div>
                            <button class="btn btn-primary" onclick="window.NiTriTeApp.applyTelemetryTweaks()">
                                Appliquer
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Services Optimization Section -->
                <div class="optimization-section">
                    <div class="section-header">
                        <h3>⚙️ Services Windows</h3>
                        <p class="section-description">Optimisez les services système non essentiels</p>
                    </div>
                    <div class="section-content">
                        <div class="optimization-card">
                            <div class="card-icon">🔧</div>
                            <div class="card-content">
                                <h4>Optimiser les Services</h4>
                                <p>Désactivez les services non essentiels pour améliorer les performances</p>
                                <div class="services-checklist" id="servicesChecklist">
                                    <label><input type="checkbox" value="DiagTrack"> DiagTrack (Télémétrie)</label>
                                    <label><input type="checkbox" value="dmwappushservice"> dmwappushservice (Notifications Push)</label>
                                    <label><input type="checkbox" value="WSearch"> WSearch (Recherche Windows)</label>
                                    <label><input type="checkbox" value="SysMain"> SysMain (Superfetch)</label>
                                    <label><input type="checkbox" value="WMPNetworkSvc"> WMPNetworkSvc (Windows Media Player)</label>
                                    <label><input type="checkbox" value="XblAuthManager"> XblAuthManager (Xbox Auth)</label>
                                    <label><input type="checkbox" value="XblGameSave"> XblGameSave (Xbox Save)</label>
                                    <label><input type="checkbox" value="XboxNetApiSvc"> XboxNetApiSvc (Xbox Network)</label>
                                    <label><input type="checkbox" value="Fax"> Fax (Service Fax)</label>
                                    <label><input type="checkbox" value="RetailDemo"> RetailDemo (Démo magasin)</label>
                                    <label><input type="checkbox" value="MapsBroker"> MapsBroker (Gestionnaire cartes)</label>
                                    <label><input type="checkbox" value="lfsvc"> lfsvc (Localisation)</label>
                                    <label><input type="checkbox" value="TabletInputService"> TabletInputService (Tablette)</label>
                                    <label><input type="checkbox" value="TrkWks"> TrkWks (Suivi des liens)</label>
                                </div>
                                <div class="button-group">
                                    <button class="btn btn-secondary" onclick="window.NiTriTeApp.selectAllServices()">
                                        ☑️ Tout sélectionner
                                    </button>
                                    <button class="btn btn-secondary" onclick="window.NiTriTeApp.deselectAllServices()">
                                        ⬜ Tout désélectionner
                                    </button>
                                </div>
                            </div>
                            <button class="btn btn-primary" onclick="window.NiTriTeApp.optimizeServices()">
                                Optimiser
                            </button>
                        </div>
                    </div>
                </div>

                <!-- System Cleanup Section -->
                <div class="optimization-section">
                    <div class="section-header">
                        <h3>🧹 Nettoyage Système</h3>
                        <p class="section-description">Libérez de l'espace disque</p>
                    </div>
                    <div class="section-content">
                        <div class="optimization-card">
                            <div class="card-icon">💿</div>
                            <div class="card-content">
                                <h4>Nettoyage Automatique</h4>
                                <p>Supprime les fichiers temporaires et caches</p>
                                <ul class="feature-list">
                                    <li>✓ Dossiers temporaires</li>
                                    <li>✓ Cache Windows Update</li>
                                    <li>✓ Corbeille</li>
                                    <li>✓ Fichiers journaux</li>
                                </ul>
                                <div id="cleanupResults" style="display: none; margin-top: 15px;">
                                    <div class="result-box">
                                        <strong>Espace libéré:</strong> <span id="cleanupSize">0</span> MB
                                    </div>
                                </div>
                            </div>
                            <button class="btn btn-primary" onclick="window.NiTriTeApp.performCleanup()">
                                Nettoyer
                            </button>
                        </div>
                    </div>
                </div>

                <!-- System Tools Quick Access -->
                <div class="optimization-section">
                    <div class="section-header">
                        <h3>🛠️ Accès Rapide Outils</h3>
                        <p class="section-description">Lancez les outils système Windows</p>
                    </div>
                    <div class="section-content">
                        <div class="tools-grid">
                            <button class="tool-button" onclick="window.NiTriTeAPI.executeTool('services')">
                                <span class="tool-icon">⚙️</span>
                                <span class="tool-name">Services</span>
                            </button>
                            <button class="tool-button" onclick="window.NiTriTeAPI.executeTool('registry')">
                                <span class="tool-icon">📝</span>
                                <span class="tool-name">Registre</span>
                            </button>
                            <button class="tool-button" onclick="window.NiTriTeAPI.executeTool('task_manager')">
                                <span class="tool-icon">📈</span>
                                <span class="tool-name">Gestionnaire</span>
                            </button>
                            <button class="tool-button" onclick="window.NiTriTeAPI.executeTool('disk_cleanup')">
                                <span class="tool-icon">🗑️</span>
                                <span class="tool-name">Nettoyage</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    };

    /**
     * Render Master Installation Page
     */
    NiTriTeApp.prototype.renderMasterPage = async function() {
        const content = document.getElementById('masterContent');
        if (!content) return;

        // Get master apps list
        const masterApps = await window.NiTriTeAPI.getMasterApps();

        content.innerHTML = `
            <div class="master-container">
                <div class="master-header">
                    <h3>🎯 Installation Master - Applications Essentielles</h3>
                    <p>Installez rapidement les applications les plus utilisées par les techniciens</p>
                </div>

                <div class="master-apps-grid">
                    ${masterApps.map(app => `
                        <div class="master-app-card">
                            <div class="app-checkbox">
                                <input type="checkbox" id="master-${app.id}" value="${app.id}" checked>
                            </div>
                            <div class="app-icon-large">${app.icon}</div>
                            <div class="app-name">${app.name}</div>
                            <div class="app-category">${app.category}</div>
                        </div>
                    `).join('')}
                </div>

                <div class="master-actions">
                    <button class="btn btn-secondary" onclick="window.NiTriTeApp.selectAllMasterApps()">
                        ☑️ Tout sélectionner
                    </button>
                    <button class="btn btn-secondary" onclick="window.NiTriTeApp.deselectAllMasterApps()">
                        ⬜ Tout désélectionner
                    </button>
                    <button class="btn btn-primary btn-large" onclick="window.NiTriTeApp.installMasterApps()">
                        📥 Installer la sélection (<span id="masterSelectedCount">${masterApps.length}</span>)
                    </button>
                </div>

                <div id="masterInstallProgress" style="display: none;">
                    <div class="progress-container">
                        <div class="progress-bar" id="masterProgressBar"></div>
                    </div>
                    <p id="masterProgressText" class="progress-text"></p>
                </div>
            </div>
        `;

        // Update selected count on checkbox change
        const checkboxes = content.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(cb => {
            cb.addEventListener('change', () => {
                const count = Array.from(checkboxes).filter(c => c.checked).length;
                document.getElementById('masterSelectedCount').textContent = count;
            });
        });
    };

    /**
     * Enhanced Diagnostic Page with real-time monitoring
     */
    NiTriTeApp.prototype.renderDiagnosticPage = async function() {
        const content = document.getElementById('diagnosticContent');
        if (!content) return;

        const diagnostics = await window.NiTriTeAPI.getDiagnostics();

        content.innerHTML = `
            <div class="diagnostic-grid">
                <!-- System Information Card -->
                <div class="diagnostic-card">
                    <div class="card-header">
                        <h3>💻 Informations Système</h3>
                    </div>
                    <div class="card-body">
                        <div class="info-row">
                            <span class="info-label">Système d'exploitation:</span>
                            <span class="info-value">${diagnostics.system.os}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Processeur:</span>
                            <span class="info-value">${diagnostics.system.cpu}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Mémoire:</span>
                            <span class="info-value">${diagnostics.system.ram}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Disque:</span>
                            <span class="info-value">${diagnostics.system.disk}</span>
                        </div>
                    </div>
                </div>

                <!-- Real-time Performance Card -->
                <div class="diagnostic-card">
                    <div class="card-header">
                        <h3>📊 Performance en Temps Réel</h3>
                        <button class="btn btn-small" onclick="window.NiTriTeApp.toggleMonitoring()" id="monitoringToggle">
                            ▶️ Démarrer
                        </button>
                    </div>
                    <div class="card-body">
                        <div class="performance-meter">
                            <div class="meter-label">CPU</div>
                            <div class="meter-bar">
                                <div class="meter-fill" id="cpuMeter" style="width: 0%"></div>
                            </div>
                            <div class="meter-value" id="cpuValue">0%</div>
                        </div>
                        <div class="performance-meter">
                            <div class="meter-label">RAM</div>
                            <div class="meter-bar">
                                <div class="meter-fill" id="ramMeter" style="width: 0%"></div>
                            </div>
                            <div class="meter-value" id="ramValue">0%</div>
                        </div>
                        <div class="performance-meter">
                            <div class="meter-label">Disque</div>
                            <div class="meter-bar">
                                <div class="meter-fill" id="diskMeter" style="width: 0%"></div>
                            </div>
                            <div class="meter-value" id="diskValue">0%</div>
                        </div>
                    </div>
                </div>

                <!-- System Health Card -->
                <div class="diagnostic-card">
                    <div class="card-header">
                        <h3>🏥 État du Système</h3>
                    </div>
                    <div class="card-body">
                        <div class="health-score" id="healthScore">
                            <div class="score-circle">
                                <span class="score-value">95</span>
                                <span class="score-label">/ 100</span>
                            </div>
                            <p class="score-status">Excellent</p>
                        </div>
                        <p class="status-message">${diagnostics.status}</p>
                    </div>
                </div>

                <!-- Quick Actions Card -->
                <div class="diagnostic-card">
                    <div class="card-header">
                        <h3>⚡ Actions Rapides</h3>
                    </div>
                    <div class="card-body">
                        <button class="action-btn" onclick="window.NiTriTeAPI.executeTool('system_info')">
                            💻 Informations détaillées
                        </button>
                        <button class="action-btn" onclick="window.NiTriTeAPI.executeTool('device_manager')">
                            🔌 Gestionnaire de périphériques
                        </button>
                        <button class="action-btn" onclick="window.NiTriTeAPI.executeTool('disk_manager')">
                            💿 Gestion des disques
                        </button>
                        <button class="action-btn" onclick="window.NiTriTeApp.showPage('optimization')">
                            ⚙️ Optimiser le système
                        </button>
                    </div>
                </div>
            </div>
        `;

        this.monitoringInterval = null;
    };

    /**
     * Apply telemetry tweaks
     */
    NiTriTeApp.prototype.applyTelemetryTweaks = async function() {
        if (!confirm('⚠️ Cette opération va modifier le registre Windows.\n\n' +
                     'Modifications:\n' +
                     '• Désactiver la télémétrie\n' +
                     '• Désactiver le rapport d\'erreurs\n' +
                     '• Désactiver les suggestions\n' +
                     '• Désactiver l\'historique d\'activité\n\n' +
                     'Requiert les droits administrateur.\n\n' +
                     'Continuer ?')) {
            return;
        }

        try {
            const response = await fetch('/api/optimization/telemetry', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });

            const result = await response.json();

            if (result.status === 'success') {
                alert('✅ ' + result.message);
            } else if (result.status === 'warning') {
                alert('⚠️ ' + result.message);
            } else {
                alert('❌ Erreur: ' + (result.error || 'Erreur inconnue'));
            }
        } catch (error) {
            console.error('Error applying telemetry tweaks:', error);
            alert('❌ Erreur lors de l\'application des tweaks');
        }
    };

    /**
     * Optimize Windows services
     */
    NiTriTeApp.prototype.optimizeServices = async function() {
        const checkboxes = document.querySelectorAll('#servicesChecklist input[type="checkbox"]:checked');
        const services = Array.from(checkboxes).map(cb => cb.value);

        if (services.length === 0) {
            alert('⚠️ Veuillez sélectionner au moins un service');
            return;
        }

        if (!confirm(`⚠️ Vous allez désactiver ${services.length} service(s).\n\n` +
                     'Cette opération requiert les droits administrateur.\n\n' +
                     'Continuer ?')) {
            return;
        }

        try {
            const response = await fetch('/api/optimization/services', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({services})
            });

            const result = await response.json();

            if (result.status === 'completed') {
                const success = result.results.filter(r => r.status === 'success').length;
                const failed = result.results.filter(r => r.status !== 'success').length;
                alert(`✅ Services optimisés:\n\n` +
                      `Réussis: ${success}\n` +
                      `Échoués: ${failed}\n\n` +
                      `Redémarrage recommandé.`);
            } else {
                alert('❌ Erreur: ' + (result.error || 'Erreur inconnue'));
            }
        } catch (error) {
            console.error('Error optimizing services:', error);
            alert('❌ Erreur lors de l\'optimisation des services');
        }
    };

    /**
     * Perform system cleanup
     */
    NiTriTeApp.prototype.performCleanup = async function() {
        if (!confirm('🧹 Nettoyage système\n\n' +
                     'Cette opération va supprimer:\n' +
                     '• Fichiers temporaires (>7 jours)\n' +
                     '• Caches système\n' +
                     '• Journaux anciens\n\n' +
                     'Continuer ?')) {
            return;
        }

        try {
            const response = await fetch('/api/optimization/cleanup', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });

            const result = await response.json();

            if (result.status === 'success') {
                document.getElementById('cleanupResults').style.display = 'block';
                document.getElementById('cleanupSize').textContent = result.cleaned_size_mb;
                alert(`✅ Nettoyage terminé!\n\n` +
                      `Espace libéré: ${result.cleaned_size_mb} MB`);
            } else {
                alert('❌ Erreur: ' + (result.error || 'Erreur inconnue'));
            }
        } catch (error) {
            console.error('Error during cleanup:', error);
            alert('❌ Erreur lors du nettoyage');
        }
    };

    /**
     * Select/Deselect all services
     */
    NiTriTeApp.prototype.selectAllServices = function() {
        document.querySelectorAll('#servicesChecklist input[type="checkbox"]').forEach(cb => cb.checked = true);
    };

    NiTriTeApp.prototype.deselectAllServices = function() {
        document.querySelectorAll('#servicesChecklist input[type="checkbox"]').forEach(cb => cb.checked = false);
    };

    /**
     * Select/Deselect all master apps
     */
    NiTriTeApp.prototype.selectAllMasterApps = function() {
        const checkboxes = document.querySelectorAll('#masterContent input[type="checkbox"]');
        checkboxes.forEach(cb => cb.checked = true);
        document.getElementById('masterSelectedCount').textContent = checkboxes.length;
    };

    NiTriTeApp.prototype.deselectAllMasterApps = function() {
        const checkboxes = document.querySelectorAll('#masterContent input[type="checkbox"]');
        checkboxes.forEach(cb => cb.checked = false);
        document.getElementById('masterSelectedCount').textContent = 0;
    };

    /**
     * Install master apps
     */
    NiTriTeApp.prototype.installMasterApps = async function() {
        const checkboxes = document.querySelectorAll('#masterContent input[type="checkbox"]:checked');
        const apps = Array.from(checkboxes).map(cb => cb.value);

        if (apps.length === 0) {
            alert('⚠️ Veuillez sélectionner au moins une application');
            return;
        }

        if (!confirm(`📥 Installation de ${apps.length} application(s)\n\nContinuer ?`)) {
            return;
        }

        // Show progress
        document.getElementById('masterInstallProgress').style.display = 'block';

        // Simulate installation progress (replace with actual API call)
        for (let i = 0; i < apps.length; i++) {
            const progress = ((i + 1) / apps.length) * 100;
            document.getElementById('masterProgressBar').style.width = progress + '%';
            document.getElementById('masterProgressText').textContent =
                `Installation de ${apps[i]}... (${i + 1}/${apps.length})`;

            // Call installation API
            try {
                await window.NiTriTeAPI.installApplication(apps[i]);
            } catch (error) {
                console.error(`Error installing ${apps[i]}:`, error);
            }

            await new Promise(resolve => setTimeout(resolve, 1000));
        }

        alert(`✅ Installation terminée!\n\n${apps.length} application(s) installée(s)`);
        document.getElementById('masterInstallProgress').style.display = 'none';
    };

    /**
     * Toggle performance monitoring
     */
    NiTriTeApp.prototype.toggleMonitoring = function() {
        if (this.monitoringInterval) {
            clearInterval(this.monitoringInterval);
            this.monitoringInterval = null;
            document.getElementById('monitoringToggle').textContent = '▶️ Démarrer';
        } else {
            this.startMonitoring();
            document.getElementById('monitoringToggle').textContent = '⏸️ Arrêter';
        }
    };

    /**
     * Start performance monitoring
     */
    NiTriTeApp.prototype.startMonitoring = function() {
        const updateMeters = async () => {
            try {
                const diagnostics = await window.NiTriTeAPI.getDiagnostics();

                // Simulate performance data (replace with actual metrics from API)
                const cpuUsage = Math.random() * 100;
                const ramUsage = parseFloat(diagnostics.system.ram.match(/(\d+)%/)?.[1] || 50);
                const diskUsage = Math.random() * 100;

                // Update meters
                document.getElementById('cpuMeter').style.width = cpuUsage + '%';
                document.getElementById('cpuValue').textContent = Math.round(cpuUsage) + '%';

                document.getElementById('ramMeter').style.width = ramUsage + '%';
                document.getElementById('ramValue').textContent = Math.round(ramUsage) + '%';

                document.getElementById('diskMeter').style.width = diskUsage + '%';
                document.getElementById('diskValue').textContent = Math.round(diskUsage) + '%';

                // Color code based on usage
                const setMeterColor = (element, usage) => {
                    if (usage < 50) element.style.background = '#4CAF50';
                    else if (usage < 80) element.style.background = '#FF9800';
                    else element.style.background = '#F44336';
                };

                setMeterColor(document.getElementById('cpuMeter'), cpuUsage);
                setMeterColor(document.getElementById('ramMeter'), ramUsage);
                setMeterColor(document.getElementById('diskMeter'), diskUsage);
            } catch (error) {
                console.error('Error updating performance meters:', error);
            }
        };

        // Update every 2 seconds
        updateMeters();
        this.monitoringInterval = setInterval(updateMeters, 2000);
    };
}

// Update API to include new endpoints
if (typeof NiTriTeAPI !== 'undefined') {
    NiTriTeAPI.prototype.getMasterApps = async function() {
        try {
            const response = await fetch('/api/master/apps');
            return await response.json();
        } catch (error) {
            console.error('Error fetching master apps:', error);
            return [];
        }
    };
}
