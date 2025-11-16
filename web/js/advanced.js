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

                <!-- Performance Optimization Section -->
                <div class="optimization-section">
                    <div class="section-header">
                        <h3>⚡ Optimisations de Performance</h3>
                        <p class="section-description">Tweaks avancés pour améliorer les performances</p>
                    </div>
                    <div class="section-content">
                        <div class="optimization-card">
                            <div class="card-icon">🚀</div>
                            <div class="card-content">
                                <h4>Optimisations Avancées</h4>
                                <p>Désactive les fonctionnalités gourmandes en ressources</p>
                                <ul class="feature-list">
                                    <li>✓ Désactiver effets visuels</li>
                                    <li>✓ Désactiver hibernation</li>
                                    <li>✓ Optimiser système de fichiers</li>
                                    <li>✓ Désactiver indexation (SSD)</li>
                                    <li>✓ Désactiver Prefetch/Superfetch</li>
                                </ul>
                            </div>
                            <button class="btn btn-primary" onclick="window.NiTriTeApp.applyPerformanceTweaks()">
                                Optimiser
                            </button>
                        </div>
                    </div>
                </div>

                <!-- System Repair Section -->
                <div class="optimization-section">
                    <div class="section-header">
                        <h3>🔧 Réparation Système</h3>
                        <p class="section-description">Outils de diagnostic et réparation Windows</p>
                    </div>
                    <div class="section-content">
                        <div class="tools-grid">
                            <button class="tool-button" onclick="window.NiTriTeApp.runDISMScan('CheckHealth')">
                                <span class="tool-icon">🔍</span>
                                <span class="tool-name">DISM Check</span>
                            </button>
                            <button class="tool-button" onclick="window.NiTriTeApp.runDISMScan('ScanHealth')">
                                <span class="tool-icon">🔎</span>
                                <span class="tool-name">DISM Scan</span>
                            </button>
                            <button class="tool-button" onclick="window.NiTriTeApp.runDISMScan('RestoreHealth')">
                                <span class="tool-icon">🔧</span>
                                <span class="tool-name">DISM Repair</span>
                            </button>
                            <button class="tool-button" onclick="window.NiTriTeApp.runSFCScan()">
                                <span class="tool-icon">🛡️</span>
                                <span class="tool-name">SFC Scan</span>
                            </button>
                            <button class="tool-button" onclick="window.NiTriTeApp.resetNetwork()">
                                <span class="tool-icon">🌐</span>
                                <span class="tool-name">Reset Réseau</span>
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
                            <button class="tool-button" onclick="window.NiTriTeAPI.executeTool('device_manager')">
                                <span class="tool-icon">🔌</span>
                                <span class="tool-name">Périphériques</span>
                            </button>
                            <button class="tool-button" onclick="window.NiTriTeAPI.executeTool('system_info')">
                                <span class="tool-icon">💻</span>
                                <span class="tool-name">Infos Système</span>
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

                <div class="master-actions" style="display: flex; flex-direction: column; gap: 15px;">
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
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
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <button class="btn btn-success btn-large" onclick="window.NiTriTeApp.exportInstallScript()" style="background: #00c853; flex: 1;">
                            🚀 Télécharger Script PowerShell (.ps1)
                        </button>
                        <button class="btn btn-success btn-large" onclick="window.NiTriTeApp.generateOneLiner()" style="background: #2196f3; flex: 1;">
                            📋 Copier Commande One-Liner
                        </button>
                    </div>
                </div>

                <div id="masterInstallProgress" style="display: none;">
                    <div class="progress-container">
                        <div class="progress-bar" id="masterProgressBar"></div>
                    </div>
                    <p id="masterProgressText" class="progress-text"></p>
                </div>

                <!-- Actions Rapides Section -->
                <div class="master-quick-actions" style="margin-top: 40px;">
                    <h3 style="color: var(--accent-color); margin-bottom: 20px;">⚡ Actions Rapides</h3>
                    <div class="quick-actions-grid">
                        <button class="action-button" onclick="window.open('https://massgrave.dev/', '_blank')">
                            <span class="action-icon">🔑</span>
                            <span class="action-title">MassGrave Scripts</span>
                            <span class="action-desc">Activation Windows & Office</span>
                        </button>
                        <button class="action-button" onclick="window.NiTriTeApp.runActivationScript()">
                            <span class="action-icon">⚡</span>
                            <span class="action-title">Activation Auto</span>
                            <span class="action-desc">Script automatique</span>
                        </button>
                        <button class="action-button" onclick="window.NiTriTeApp.createPortableFolder()">
                            <span class="action-icon">📁</span>
                            <span class="action-title">Outils Portables</span>
                            <span class="action-desc">Créer dossier Bureau</span>
                        </button>
                        <button class="action-button" onclick="window.open('https://gravesoft.dev/office_c2r_links#french-fr-fr', '_blank')">
                            <span class="action-icon">📋</span>
                            <span class="action-title">Office FR</span>
                            <span class="action-desc">Télécharger Office français</span>
                        </button>
                        <button class="action-button" onclick="window.NiTriTeAPI.executeTool('msconfig')">
                            <span class="action-icon">⚙️</span>
                            <span class="action-title">MSConfig</span>
                            <span class="action-desc">Configuration système</span>
                        </button>
                        <button class="action-button" onclick="window.NiTriTeAPI.executeTool('windows_update')">
                            <span class="action-icon">🔄</span>
                            <span class="action-title">Windows Update</span>
                            <span class="action-desc">Mises à jour Windows</span>
                        </button>
                        <button class="action-button" onclick="window.NiTriTeAPI.executeTool('disk_c')">
                            <span class="action-icon">💾</span>
                            <span class="action-title">Disque C:</span>
                            <span class="action-desc">Ouvrir le disque C:</span>
                        </button>
                        <button class="action-button" onclick="window.NiTriTeAPI.executeTool('startup_apps')">
                            <span class="action-icon">🚀</span>
                            <span class="action-title">Apps Démarrage</span>
                            <span class="action-desc">Applications de démarrage</span>
                        </button>
                        <button class="action-button" onclick="window.NiTriTeApp.openAdminTerminal()">
                            <span class="action-icon">⚡</span>
                            <span class="action-title">Terminal Admin</span>
                            <span class="action-desc">PowerShell administrateur</span>
                        </button>
                        <button class="action-button" onclick="window.NiTriTeApp.generateSystemReport()">
                            <span class="action-icon">📋</span>
                            <span class="action-title">Rapport Système</span>
                            <span class="action-desc">Générer rapport détaillé</span>
                        </button>
                        <button class="action-button" onclick="window.NiTriTeAPI.executeTool('winver')">
                            <span class="action-icon">🪟</span>
                            <span class="action-title">Version Windows</span>
                            <span class="action-desc">Afficher infos Windows</span>
                        </button>
                        <button class="action-button" onclick="window.NiTriTeAPI.executeTool('msinfo32')">
                            <span class="action-icon">ℹ️</span>
                            <span class="action-title">Infos Système</span>
                            <span class="action-desc">Informations système</span>
                        </button>
                    </div>

                    <!-- WinGet Manager Section -->
                    <h4 style="color: var(--accent-color); margin-top: 30px; margin-bottom: 15px;">📦 WinGet Manager</h4>
                    <div class="winget-actions">
                        <button class="action-button wide" onclick="window.NiTriTeApp.wingetUpgradeAll()">
                            <span class="action-icon">⬆️</span>
                            <span class="action-title">Tout Mettre à Jour</span>
                            <span class="action-desc">winget upgrade --all</span>
                        </button>
                        <button class="action-button wide" onclick="window.NiTriTeApp.wingetListUpgrades()">
                            <span class="action-icon">📋</span>
                            <span class="action-title">Lister Mises à Jour</span>
                            <span class="action-desc">winget upgrade</span>
                        </button>
                    </div>
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

// ==================== BACKUP & RESTORE PAGE ====================
if (typeof NiTriTeApp !== 'undefined') {
    /**
     * Render Backup & Restore Page
     */
    NiTriTeApp.prototype.renderBackupPage = function() {
        const backupPage = document.getElementById('backupPage');
        if (!backupPage) {
            console.warn('[App] backupPage element not found - skipping render');
            return;
        }

        backupPage.innerHTML = `
            <div class="page-header">
                <h1>💾 Sauvegarde & Restauration</h1>
                <p class="page-description">Protégez votre système et vos données</p>
            </div>

            <div class="backup-sections">
                <!-- Restore Point Section -->
                <div class="backup-section">
                    <div class="section-header">
                        <h3>📌 Points de Restauration</h3>
                        <p class="section-description">Créez un point de sauvegarde système</p>
                    </div>
                    <div class="section-content">
                        <div class="backup-card">
                            <div class="card-icon">🔄</div>
                            <div class="card-content">
                                <h4>Créer un Point de Restauration</h4>
                                <p>Permet de revenir en arrière en cas de problème après des modifications système</p>
                                <input type="text" id="restorePointDesc" placeholder="Description (optionnel)" class="input-text">
                            </div>
                            <button class="btn btn-primary" onclick="window.NiTriTeApp.createRestorePoint()">
                                Créer
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Driver Backup Section -->
                <div class="backup-section">
                    <div class="section-header">
                        <h3>🔌 Sauvegarde des Drivers</h3>
                        <p class="section-description">Exportez tous les drivers installés</p>
                    </div>
                    <div class="section-content">
                        <div class="backup-card">
                            <div class="card-icon">💿</div>
                            <div class="card-content">
                                <h4>Exporter les Drivers</h4>
                                <p>Sauvegarde tous les drivers système pour réinstallation rapide</p>
                                <input type="text" id="driverBackupPath" value="C:\\DriversBackup" class="input-text">
                                <div id="driverBackupResults" style="display: none; margin-top: 10px;">
                                    <div class="result-box">
                                        <strong>✅ Sauvegarde terminée:</strong> <span id="driverCount">0</span> drivers exportés
                                    </div>
                                </div>
                            </div>
                            <button class="btn btn-primary" onclick="window.NiTriTeApp.backupDrivers()">
                                Exporter
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Apps List Export Section -->
                <div class="backup-section">
                    <div class="section-header">
                        <h3>📋 Liste des Applications</h3>
                        <p class="section-description">Exportez la liste des applications installées</p>
                    </div>
                    <div class="section-content">
                        <div class="backup-card">
                            <div class="card-icon">📝</div>
                            <div class="card-content">
                                <h4>Exporter la Liste</h4>
                                <p>Génère une liste de toutes les applications installées (utile pour réinstallation)</p>
                                <div id="appsListResults" style="display: none; margin-top: 10px;">
                                    <div class="result-box">
                                        <strong>✅ Export terminé:</strong> <span id="appsCount">0</span> applications
                                        <button class="btn btn-small" onclick="window.NiTriTeApp.downloadAppsList()" style="margin-top: 10px;">
                                            💾 Télécharger la liste
                                        </button>
                                    </div>
                                </div>
                            </div>
                            <button class="btn btn-primary" onclick="window.NiTriTeApp.exportAppsList()">
                                Exporter
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    };

    /**
     * Create system restore point
     */
    NiTriTeApp.prototype.createRestorePoint = async function() {
        const description = document.getElementById('restorePointDesc')?.value || 'NiTriTe Manual Restore Point';

        if (!confirm(`💾 Créer un point de restauration système?\n\nDescription: ${description}\n\n⚠️ Requiert les droits administrateur`)) {
            return;
        }

        try {
            const response = await fetch('/api/backup/restore-point', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({description})
            });

            const result = await response.json();

            if (result.status === 'success') {
                alert('✅ ' + result.message);
                document.getElementById('restorePointDesc').value = '';
            } else {
                alert('❌ ' + (result.message || result.error || 'Erreur inconnue'));
            }
        } catch (error) {
            console.error('Error creating restore point:', error);
            alert('❌ Erreur lors de la création du point de restauration');
        }
    };

    /**
     * Backup drivers
     */
    NiTriTeApp.prototype.backupDrivers = async function() {
        const path = document.getElementById('driverBackupPath')?.value || 'C:\\DriversBackup';

        if (!confirm(`🔌 Sauvegarder tous les drivers?\n\nDestination: ${path}\n\n⚠️ Requiert les droits administrateur\n⏱️ Peut prendre plusieurs minutes`)) {
            return;
        }

        try {
            const response = await fetch('/api/backup/drivers', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({path})
            });

            const result = await response.json();

            if (result.status === 'success') {
                document.getElementById('driverBackupResults').style.display = 'block';
                document.getElementById('driverCount').textContent = result.count;
                alert(`✅ ${result.message}\n\nEmplacement: ${result.path}`);
            } else {
                alert('❌ ' + (result.message || result.error || 'Erreur inconnue'));
            }
        } catch (error) {
            console.error('Error backing up drivers:', error);
            alert('❌ Erreur lors de la sauvegarde des drivers');
        }
    };

    /**
     * Export apps list
     */
    NiTriTeApp.prototype.exportAppsList = async function() {
        try {
            const response = await fetch('/api/backup/apps-list');
            const result = await response.json();

            if (result.status === 'success') {
                this.cachedAppsList = result.applications;
                document.getElementById('appsListResults').style.display = 'block';
                document.getElementById('appsCount').textContent = result.count;
                alert(`✅ Liste exportée avec succès!\n\n${result.count} applications trouvées`);
            } else {
                alert('❌ ' + (result.error || 'Erreur inconnue'));
            }
        } catch (error) {
            console.error('Error exporting apps list:', error);
            alert('❌ Erreur lors de l\'export de la liste');
        }
    };

    /**
     * Download apps list as JSON
     */
    NiTriTeApp.prototype.downloadAppsList = function() {
        if (!this.cachedAppsList) {
            alert('⚠️ Veuillez d\'abord exporter la liste');
            return;
        }

        const dataStr = JSON.stringify(this.cachedAppsList, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `applications_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        URL.revokeObjectURL(url);
    };

    // ==================== ADVANCED OPTIMIZATION ====================

    /**
     * Add performance tweaks to optimization page
     */
    NiTriTeApp.prototype.applyPerformanceTweaks = async function() {
        if (!confirm('⚡ Optimisations de Performance\n\n' +
                     'Cette opération va:\n' +
                     '• Désactiver les effets visuels inutiles\n' +
                     '• Désactiver l\'hibernation\n' +
                     '• Optimiser le système de fichiers\n' +
                     '• Désactiver l\'indexation Windows Search\n' +
                     '• Désactiver Prefetch/Superfetch (SSD)\n\n' +
                     '⚠️ Requiert droits admin\n' +
                     '⚠️ Redémarrage recommandé\n\n' +
                     'Continuer?')) {
            return;
        }

        try {
            const response = await fetch('/api/optimization/performance', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });

            const result = await response.json();

            if (result.status === 'success') {
                alert('✅ ' + result.message);
            } else {
                alert('⚠️ ' + (result.message || 'Certaines optimisations ont échoué'));
            }
        } catch (error) {
            console.error('Error applying performance tweaks:', error);
            alert('❌ Erreur lors de l\'application des optimisations');
        }
    };

    // ==================== SYSTEM REPAIR TOOLS ====================

    /**
     * Run DISM scan
     */
    NiTriTeApp.prototype.runDISMScan = async function(operation = 'ScanHealth') {
        const operations = {
            'ScanHealth': 'Analyse de santé',
            'CheckHealth': 'Vérification rapide',
            'RestoreHealth': 'Réparation complète'
        };

        if (!confirm(`🔧 DISM - ${operations[operation]}\n\n` +
                     `⚠️ Requiert droits administrateur\n` +
                     `⏱️ Peut prendre 10-30 minutes\n\n` +
                     `Continuer?`)) {
            return;
        }

        try {
            const response = await fetch('/api/system/dism-scan', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({operation})
            });

            const result = await response.json();

            if (result.status === 'success') {
                alert('✅ DISM scan terminé avec succès\n\nVoir la console pour les détails');
                console.log('DISM Output:', result.output);
            } else {
                alert('⚠️ ' + result.message + '\n\nVoir la console pour les détails');
                console.log('DISM Output:', result.output);
            }
        } catch (error) {
            console.error('Error running DISM:', error);
            alert('❌ Erreur lors de l\'exécution de DISM');
        }
    };

    /**
     * Run SFC scan
     */
    NiTriTeApp.prototype.runSFCScan = async function() {
        if (!confirm('🔍 System File Checker (SFC)\n\n' +
                     '⚠️ Requiert droits administrateur\n' +
                     '⏱️ Peut prendre 15-30 minutes\n\n' +
                     'Continuer?')) {
            return;
        }

        try {
            const response = await fetch('/api/system/sfc-scan', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });

            const result = await response.json();

            if (result.status === 'success') {
                alert('✅ SFC scan terminé avec succès\n\nVoir la console pour les détails');
                console.log('SFC Output:', result.output);
            } else {
                alert('⚠️ ' + result.message + '\n\nVoir la console pour les détails');
                console.log('SFC Output:', result.output);
            }
        } catch (error) {
            console.error('Error running SFC:', error);
            alert('❌ Erreur lors de l\'exécution de SFC');
        }
    };

    /**
     * Reset network
     */
    NiTriTeApp.prototype.resetNetwork = async function() {
        if (!confirm('🌐 Réinitialisation Réseau Complète\n\n' +
                     'Cette opération va:\n' +
                     '• Libérer et renouveler l\'IP\n' +
                     '• Vider le cache DNS\n' +
                     '• Réinitialiser Winsock\n' +
                     '• Réinitialiser TCP/IP\n\n' +
                     '⚠️ Requiert droits admin\n' +
                     '⚠️ Redémarrage OBLIGATOIRE\n\n' +
                     'Continuer?')) {
            return;
        }

        try {
            const response = await fetch('/api/system/network-reset', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });

            const result = await response.json();

            if (result.status === 'success') {
                alert('✅ ' + result.message);
            } else {
                alert('❌ ' + (result.message || 'Erreur lors de la réinitialisation'));
            }
        } catch (error) {
            console.error('Error resetting network:', error);
            alert('❌ Erreur lors de la réinitialisation réseau');
        }
    };

    /**
     * Check Windows Updates
     */
    NiTriTeApp.prototype.checkUpdates = async function() {
        const updatesContent = document.getElementById('updatesContent');
        if (!updatesContent) return;

        updatesContent.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>Recherche des mises à jour...</p>
            </div>
        `;

        try {
            const response = await fetch('/api/updates/check');
            const result = await response.json();

            if (result.status === 'success') {
                if (result.count === 0) {
                    updatesContent.innerHTML = `
                        <div class="result-box" style="background: rgba(76, 175, 80, 0.1); border-color: #4CAF50;">
                            <h3>✅ Système à jour</h3>
                            <p>Aucune mise à jour disponible</p>
                        </div>
                    `;
                } else {
                    let updatesHTML = `
                        <div class="result-box">
                            <h3>📥 ${result.count} mise(s) à jour disponible(s)</h3>
                        </div>
                        <div class="updates-list">
                    `;

                    result.updates.forEach(update => {
                        updatesHTML += `
                            <div class="update-item">
                                <h4>${update.Title}</h4>
                                <p>${update.Description}</p>
                                <span class="update-size">${update.Size} MB</span>
                            </div>
                        `;
                    });

                    updatesHTML += `
                        </div>
                        <button class="btn btn-primary" onclick="window.location.href='ms-settings:windowsupdate'">
                            Ouvrir Windows Update
                        </button>
                    `;

                    updatesContent.innerHTML = updatesHTML;
                }
            } else {
                updatesContent.innerHTML = `
                    <div class="result-box" style="background: rgba(244, 67, 54, 0.1); border-color: #F44336;">
                        <h3>❌ Erreur</h3>
                        <p>Impossible de vérifier les mises à jour</p>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error checking updates:', error);
            updatesContent.innerHTML = `
                <div class="result-box" style="background: rgba(244, 67, 54, 0.1); border-color: #F44336;">
                    <h3>❌ Erreur</h3>
                    <p>Erreur lors de la vérification des mises à jour</p>
                </div>
            `;
        }
    };

    /**
     * Run benchmark
     */
    NiTriTeApp.prototype.runBenchmark = async function() {
        const benchmarkResults = document.getElementById('benchmarkResults');
        if (!benchmarkResults) return;

        benchmarkResults.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>Benchmark en cours...</p>
            </div>
        `;

        try {
            const response = await fetch('/api/benchmark/run', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });

            const result = await response.json();

            if (result.status === 'success') {
                benchmarkResults.innerHTML = `
                    <div class="benchmark-results">
                        <div class="overall-score">
                            <div class="score-circle-large">
                                <span class="score-value">${result.overall_score}</span>
                                <span class="score-label">/ 100</span>
                            </div>
                            <p class="score-status">${this.getScoreStatus(result.overall_score)}</p>
                        </div>
                        <div class="score-breakdown">
                            <div class="score-item">
                                <span class="score-name">💻 CPU</span>
                                <span class="score-value">${result.cpu_score}</span>
                            </div>
                            <div class="score-item">
                                <span class="score-name">🧠 Mémoire</span>
                                <span class="score-value">${result.memory_score}</span>
                            </div>
                            <div class="score-item">
                                <span class="score-name">💿 Disque</span>
                                <span class="score-value">${result.disk_score}</span>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                benchmarkResults.innerHTML = `
                    <div class="result-box" style="background: rgba(244, 67, 54, 0.1); border-color: #F44336;">
                        <h3>❌ Erreur</h3>
                        <p>Impossible d'exécuter le benchmark</p>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error running benchmark:', error);
            benchmarkResults.innerHTML = `
                <div class="result-box" style="background: rgba(244, 67, 54, 0.1); border-color: #F44336;">
                    <h3>❌ Erreur</h3>
                    <p>Erreur lors du benchmark</p>
                </div>
            `;
        }
    };

    /**
     * Get score status text
     */
    NiTriTeApp.prototype.getScoreStatus = function(score) {
        if (score >= 90) return 'Excellent';
        if (score >= 75) return 'Très Bon';
        if (score >= 60) return 'Bon';
        if (score >= 45) return 'Moyen';
        return 'Faible';
    };

    // ==================== MASTER PAGE ACTIONS ====================

    /**
     * Run Windows activation script
     */
    NiTriTeApp.prototype.runActivationScript = async function() {
        if (!confirm('⚠️ Cette action va exécuter le script d\'activation Windows/Office.\n\n' +
                     'Le script va être téléchargé depuis massgrave.dev et exécuté.\n\n' +
                     'Continuer?')) {
            return;
        }

        try {
            const response = await fetch('/api/system/activate-windows', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });

            const result = await response.json();

            if (result.status === 'success') {
                alert('✅ Script d\'activation lancé!\n\nSuivez les instructions dans la fenêtre PowerShell.');
            } else {
                alert('❌ ' + (result.message || 'Erreur inconnue'));
            }
        } catch (error) {
            console.error('Error running activation:', error);
            alert('❌ Erreur lors du lancement du script d\'activation');
        }
    };

    /**
     * Create portable tools folder on desktop
     */
    NiTriTeApp.prototype.createPortableFolder = async function() {
        if (!confirm('📁 Créer un dossier "Outils de Nettoyage" sur le Bureau?\n\n' +
                     'Ce dossier contiendra des raccourcis vers les outils portables.\n\n' +
                     'Continuer?')) {
            return;
        }

        try {
            const response = await fetch('/api/system/create-portable-folder', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });

            const result = await response.json();

            if (result.status === 'success') {
                alert('✅ ' + result.message);
            } else {
                alert('❌ ' + (result.message || 'Erreur inconnue'));
            }
        } catch (error) {
            console.error('Error creating folder:', error);
            alert('❌ Erreur lors de la création du dossier');
        }
    };

    /**
     * Open admin terminal (PowerShell)
     */
    NiTriTeApp.prototype.openAdminTerminal = async function() {
        if (!confirm('⚡ Ouvrir PowerShell en tant qu\'administrateur?\n\n' +
                     '⚠️ Requiert les droits administrateur\n\n' +
                     'Continuer?')) {
            return;
        }

        try {
            const response = await fetch('/api/system/open-admin-terminal', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });

            const result = await response.json();

            if (result.status === 'success') {
                alert('✅ PowerShell administrateur lancé!');
            } else {
                alert('❌ ' + (result.message || 'Erreur inconnue'));
            }
        } catch (error) {
            console.error('Error opening terminal:', error);
            alert('❌ Erreur lors de l\'ouverture du terminal');
        }
    };

    /**
     * Generate system report
     */
    NiTriTeApp.prototype.generateSystemReport = async function() {
        if (!confirm('📋 Générer un rapport système détaillé?\n\n' +
                     '⏱️ Cette opération peut prendre quelques minutes\n\n' +
                     'Continuer?')) {
            return;
        }

        try {
            const response = await fetch('/api/system/generate-report', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });

            const result = await response.json();

            if (result.status === 'success') {
                alert('✅ Rapport généré!\n\nEmplacement: ' + result.path);
            } else {
                alert('❌ ' + (result.message || 'Erreur inconnue'));
            }
        } catch (error) {
            console.error('Error generating report:', error);
            alert('❌ Erreur lors de la génération du rapport');
        }
    };

    /**
     * WinGet upgrade all
     */
    NiTriTeApp.prototype.wingetUpgradeAll = async function() {
        if (!confirm('📦 Mettre à jour toutes les applications via WinGet?\n\n' +
                     'Commande: winget upgrade --all\n\n' +
                     '⏱️ Cette opération peut prendre du temps\n\n' +
                     'Continuer?')) {
            return;
        }

        try {
            const response = await fetch('/api/winget/upgrade-all', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });

            const result = await response.json();

            if (result.status === 'success') {
                alert('✅ Mises à jour WinGet lancées!\n\nConsultez la fenêtre de terminal.');
            } else {
                alert('❌ ' + (result.message || 'Erreur inconnue'));
            }
        } catch (error) {
            console.error('Error running winget upgrade:', error);
            alert('❌ Erreur lors de la mise à jour WinGet');
        }
    };

    /**
     * WinGet list upgrades
     */
    NiTriTeApp.prototype.wingetListUpgrades = async function() {
        try {
            const response = await fetch('/api/winget/list-upgrades', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });

            const result = await response.json();

            if (result.status === 'success') {
                alert('✅ Liste des mises à jour WinGet affichée!\n\nConsultez la fenêtre de terminal.');
            } else {
                alert('❌ ' + (result.message || 'Erreur inconnue'));
            }
        } catch (error) {
            console.error('Error listing winget upgrades:', error);
            alert('❌ Erreur lors de la récupération de la liste');
        }
    };

    /**
     * Export installation script for selected master apps
     */
    NiTriTeApp.prototype.exportInstallScript = async function() {
        // Get selected apps from master page
        const checkboxes = document.querySelectorAll('#masterContent input[type="checkbox"]:checked');

        if (checkboxes.length === 0) {
            alert('⚠️ Veuillez sélectionner au moins une application');
            return;
        }

        const selectedAppIds = Array.from(checkboxes).map(cb => cb.value);

        // Fetch full app data
        try {
            const masterApps = await window.NiTriTeAPI.getMasterApps();
            const selectedApps = masterApps.filter(app => selectedAppIds.includes(app.id));

            // Generate PowerShell script
            const scriptContent = this.generatePowerShellInstallScript(selectedApps);

            // Create downloadable file
            const blob = new Blob([scriptContent], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `NiTriTe_AutoInstall_${new Date().toISOString().split('T')[0]}.ps1`;
            a.click();
            URL.revokeObjectURL(url);

            // Show instructions
            const instructions = `✅ Script d'installation généré avec succès!

📥 Fichier téléchargé: NiTriTe_AutoInstall_${new Date().toISOString().split('T')[0]}.ps1
📋 ${selectedApps.length} application(s) sélectionnée(s)

🚀 UTILISATION:
1. Copiez le fichier .ps1 sur le PC cible
2. Clic droit → "Exécuter avec PowerShell"
   OU
   PowerShell en Admin: .\\NiTriTe_AutoInstall_*.ps1

⚡ Le script va:
• Vérifier WinGet
• Installer toutes les apps en mode silencieux
• Créer un log d'installation
• Afficher un résumé final

⚠️ IMPORTANT:
• Exécuter en tant qu'administrateur
• Connexion internet requise`;

            alert(instructions);

        } catch (error) {
            console.error('Error generating install script:', error);
            alert('❌ Erreur lors de la génération du script');
        }
    };

    /**
     * Generate PowerShell installation script
     */
    NiTriTeApp.prototype.generatePowerShellInstallScript = function(apps) {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const appsList = apps.map(app => `    "${app.name}"`).join(',\n');

        const script = `# ========================================
# NiTriTe V.13 - Script d'Installation Automatique
# Généré le: ${new Date().toLocaleString('fr-FR')}
# Nombre d'applications: ${apps.length}
# ========================================

# Élévation des privilèges si nécessaire
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "⚠️ Ce script nécessite les droits administrateur!"
    Write-Host "Relancement en tant qu'administrateur..." -ForegroundColor Yellow
    Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File \`"$PSCommandPath\`"" -Verb RunAs
    exit
}

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  NiTriTe V.13 - Installation Auto     ║" -ForegroundColor Cyan
Write-Host "║  ${apps.length} applications sélectionnées          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configuration
$logFile = "$env:TEMP\\NiTriTe_Install_Log_${timestamp}.txt"
$successCount = 0
$failedCount = 0
$failedApps = @()

# Fonction de logging
function Write-Log {
    param($Message, $Color = "White")
    Write-Host $Message -ForegroundColor $Color
    Add-Content -Path $logFile -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $Message"
}

# Vérification de WinGet
Write-Log "🔍 Vérification de WinGet..." "Yellow"
try {
    $wingetVersion = winget --version
    Write-Log "✅ WinGet installé: $wingetVersion" "Green"
} catch {
    Write-Log "❌ WinGet n'est pas installé!" "Red"
    Write-Log "📥 Installation de WinGet..." "Yellow"

    # Installation automatique de WinGet
    $progressPreference = 'silentlyContinue'
    Invoke-WebRequest -Uri https://aka.ms/getwinget -OutFile "$env:TEMP\\Microsoft.DesktopAppInstaller.msixbundle"
    Add-AppxPackage "$env:TEMP\\Microsoft.DesktopAppInstaller.msixbundle"
    Write-Log "✅ WinGet installé avec succès!" "Green"
}

Write-Host ""
Write-Log "════════════════════════════════════════" "Cyan"
Write-Log "🚀 DÉBUT DE L'INSTALLATION" "Cyan"
Write-Log "════════════════════════════════════════" "Cyan"
Write-Host ""

# Liste des applications à installer
$applications = @(
${apps.map(app => {
    // Générer la commande WinGet appropriée
    let wingetId = app.wingetId || app.name;
    return `    @{
        Name = "${app.name}"
        WinGetId = "${wingetId}"
        Category = "${app.category || 'Général'}"
    }`;
}).join(',\n')}
)

# Compteur
$current = 0
$total = $applications.Count

# Installation de chaque application
foreach ($app in $applications) {
    $current++
    $percentage = [math]::Round(($current / $total) * 100)

    Write-Host ""
    Write-Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Gray"
    Write-Log "[$current/$total] ($percentage%) 📦 $($app.Name)" "Cyan"
    Write-Log "Catégorie: $($app.Category)" "Gray"

    try {
        # Installation silencieuse via WinGet
        Write-Log "   ⏳ Installation en cours..." "Yellow"

        $process = Start-Process -FilePath "winget" \`
            -ArgumentList "install", "--id", $app.WinGetId, "--silent", "--accept-package-agreements", "--accept-source-agreements" \`
            -NoNewWindow -Wait -PassThru

        if ($process.ExitCode -eq 0) {
            Write-Log "   ✅ Installation réussie!" "Green"
            $successCount++
        } else {
            Write-Log "   ⚠️ Installation terminée avec code: $($process.ExitCode)" "Yellow"
            $successCount++
        }
    } catch {
        Write-Log "   ❌ Erreur: $($_.Exception.Message)" "Red"
        $failedCount++
        $failedApps += $app.Name
    }
}

# Résumé final
Write-Host ""
Write-Host ""
Write-Log "════════════════════════════════════════" "Cyan"
Write-Log "📊 RÉSUMÉ DE L'INSTALLATION" "Cyan"
Write-Log "════════════════════════════════════════" "Cyan"
Write-Host ""
Write-Log "✅ Réussies:  $successCount / $total" "Green"
Write-Log "❌ Échouées:  $failedCount / $total" $(if ($failedCount -eq 0) { "Green" } else { "Red" })
Write-Host ""

if ($failedCount -gt 0) {
    Write-Log "Applications échouées:" "Red"
    foreach ($app in $failedApps) {
        Write-Log "  • $app" "Red"
    }
    Write-Host ""
}

Write-Log "📝 Log complet: $logFile" "Yellow"
Write-Host ""
Write-Log "════════════════════════════════════════" "Cyan"
Write-Log "✨ INSTALLATION TERMINÉE!" "Cyan"
Write-Log "════════════════════════════════════════" "Cyan"
Write-Host ""

# Ouvrir le log
$openLog = Read-Host "Voulez-vous ouvrir le fichier log? (O/N)"
if ($openLog -eq "O" -or $openLog -eq "o") {
    Start-Process notepad.exe $logFile
}

Write-Host "Appuyez sur une touche pour fermer..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
`;

        return script;
    };

    /**
     * Generate one-liner PowerShell command
     */
    NiTriTeApp.prototype.generateOneLiner = async function() {
        // Get selected apps from master page
        const checkboxes = document.querySelectorAll('#masterContent input[type="checkbox"]:checked');

        if (checkboxes.length === 0) {
            alert('⚠️ Veuillez sélectionner au moins une application');
            return;
        }

        const selectedAppIds = Array.from(checkboxes).map(cb => cb.value);

        // Fetch full app data
        try {
            const masterApps = await window.NiTriTeAPI.getMasterApps();
            const selectedApps = masterApps.filter(app => selectedAppIds.includes(app.id));

            // Generate WinGet commands
            const wingetCommands = selectedApps.map(app => {
                const wingetId = app.wingetId || app.name;
                return `winget install --id "${wingetId}" --silent --accept-package-agreements --accept-source-agreements`;
            });

            // Create one-liner with all commands
            const oneLiner = wingetCommands.join(' ; ');

            // Full PowerShell command with admin elevation
            const fullCommand = `powershell -Command "Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -Command \\"${oneLiner}\\"'"`;

            // Copy to clipboard
            try {
                await navigator.clipboard.writeText(oneLiner);

                // Show modal with command
                this.showOneLinerModal(oneLiner, fullCommand, selectedApps.length);

            } catch (clipboardError) {
                // Fallback: show in text area for manual copy
                this.showOneLinerModal(oneLiner, fullCommand, selectedApps.length, true);
            }

        } catch (error) {
            console.error('Error generating one-liner:', error);
            alert('❌ Erreur lors de la génération de la commande');
        }
    };

    /**
     * Show one-liner modal
     */
    NiTriTeApp.prototype.showOneLinerModal = function(oneLiner, fullCommand, appCount, manualCopy = false) {
        const modalHTML = `
            <div class="one-liner-modal" style="
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                padding: 20px;
            ">
                <div style="
                    background: var(--bg-secondary, #1e1e2e);
                    border-radius: 16px;
                    padding: 30px;
                    max-width: 900px;
                    width: 100%;
                    max-height: 90vh;
                    overflow-y: auto;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2 style="margin: 0; color: var(--text-primary, #ffffff);">
                            📋 Commande d'Installation One-Liner
                        </h2>
                        <button onclick="this.closest('.one-liner-modal').remove()" style="
                            background: transparent;
                            border: none;
                            color: var(--text-primary, #ffffff);
                            font-size: 24px;
                            cursor: pointer;
                            padding: 5px 10px;
                        ">×</button>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <p style="color: var(--text-secondary, #a8a8b3); margin: 0;">
                            ${manualCopy ? '⚠️ Sélectionnez et copiez manuellement la commande ci-dessous' : '✅ Commande copiée dans le presse-papier!'}
                        </p>
                        <p style="color: var(--accent-color, #FF6B35); margin: 10px 0 0 0; font-weight: bold;">
                            ${appCount} application(s) sélectionnée(s)
                        </p>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <h3 style="color: var(--text-primary, #ffffff); font-size: 1rem; margin-bottom: 10px;">
                            🚀 Commande Simple (PowerShell Admin):
                        </h3>
                        <textarea readonly style="
                            width: 100%;
                            min-height: 120px;
                            padding: 15px;
                            background: var(--bg-tertiary, #282838);
                            color: var(--text-primary, #ffffff);
                            border: 1px solid rgba(255, 255, 255, 0.2);
                            border-radius: 8px;
                            font-family: 'Consolas', 'Monaco', monospace;
                            font-size: 13px;
                            resize: vertical;
                        " onclick="this.select()">${oneLiner}</textarea>
                        <button onclick="navigator.clipboard.writeText(\`${oneLiner.replace(/`/g, '\\`')}\`).then(() => alert('✅ Copié!'))" style="
                            background: #00c853;
                            color: white;
                            border: none;
                            padding: 10px 20px;
                            border-radius: 8px;
                            margin-top: 10px;
                            cursor: pointer;
                            font-weight: bold;
                        ">
                            📋 Copier la commande
                        </button>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <h3 style="color: var(--text-primary, #ffffff); font-size: 1rem; margin-bottom: 10px;">
                            ⚡ Commande avec Auto-Élévation (CMD/PowerShell):
                        </h3>
                        <textarea readonly style="
                            width: 100%;
                            min-height: 80px;
                            padding: 15px;
                            background: var(--bg-tertiary, #282838);
                            color: var(--text-primary, #ffffff);
                            border: 1px solid rgba(255, 255, 255, 0.2);
                            border-radius: 8px;
                            font-family: 'Consolas', 'Monaco', monospace;
                            font-size: 13px;
                            resize: vertical;
                        " onclick="this.select()">${fullCommand}</textarea>
                        <button onclick="navigator.clipboard.writeText(\`${fullCommand.replace(/`/g, '\\`')}\`).then(() => alert('✅ Copié!'))" style="
                            background: #2196f3;
                            color: white;
                            border: none;
                            padding: 10px 20px;
                            border-radius: 8px;
                            margin-top: 10px;
                            cursor: pointer;
                            font-weight: bold;
                        ">
                            📋 Copier avec auto-élévation
                        </button>
                    </div>

                    <div style="
                        background: rgba(255, 107, 53, 0.1);
                        border-left: 4px solid var(--accent-color, #FF6B35);
                        padding: 15px;
                        border-radius: 8px;
                        margin-top: 20px;
                    ">
                        <h4 style="margin: 0 0 10px 0; color: var(--accent-color, #FF6B35);">
                            📖 Instructions d'utilisation:
                        </h4>
                        <ol style="margin: 0; padding-left: 20px; color: var(--text-secondary, #a8a8b3); line-height: 1.8;">
                            <li><strong>Option 1 (Simple):</strong> Ouvrez PowerShell en tant qu'administrateur → Collez la commande simple</li>
                            <li><strong>Option 2 (Auto-élévation):</strong> Ouvrez CMD ou PowerShell normal → Collez la commande avec auto-élévation</li>
                            <li>Les applications seront installées automatiquement en mode silencieux</li>
                            <li>Connexion internet requise</li>
                        </ol>
                    </div>

                    <div style="margin-top: 20px; text-align: right;">
                        <button onclick="this.closest('.one-liner-modal').remove()" style="
                            background: var(--bg-tertiary, #282838);
                            color: var(--text-primary, #ffffff);
                            border: 1px solid rgba(255, 255, 255, 0.2);
                            padding: 10px 25px;
                            border-radius: 8px;
                            cursor: pointer;
                            font-weight: bold;
                        ">
                            Fermer
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Add modal to page
        const modalElement = document.createElement('div');
        modalElement.innerHTML = modalHTML;
        document.body.appendChild(modalElement.firstElementChild);
    };
}
