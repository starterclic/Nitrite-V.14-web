/**
 * NiTriTe V.13 - Loading Screen Manager
 * Handles the loading sequence with progress bar
 */

class LoadingManager {
    constructor() {
        this.progressBar = document.getElementById('progressBar');
        this.loadingText = document.getElementById('loadingText');
        this.loadingPercent = document.getElementById('loadingPercent');
        this.statusText = document.getElementById('statusText');
        this.loadingScreen = document.getElementById('loadingScreen');
        this.mainApp = document.getElementById('mainApp');

        this.currentProgress = 0;
        this.targetProgress = 0;
        this.loadingSteps = [
            { progress: 10, text: 'Initialisation...', status: 'Chargement du système...' },
            { progress: 25, text: 'Chargement des ressources...', status: 'Préparation de l\'interface...' },
            { progress: 40, text: 'Chargement de la base de données...', status: 'Lecture de 715 applications...' },
            { progress: 55, text: 'Chargement des catégories...', status: 'Organisation de 25 catégories...' },
            { progress: 70, text: 'Chargement des outils système...', status: 'Préparation de 553+ outils...' },
            { progress: 85, text: 'Chargement des profils...', status: 'Configuration de 10 profils...' },
            { progress: 95, text: 'Finalisation...', status: 'Préparation de l\'interface...' },
            { progress: 100, text: 'Terminé !', status: 'Lancement de NiTriTe V.13...' }
        ];

        this.currentStep = 0;
    }

    /**
     * Start the loading sequence
     */
    async start() {
        console.log('[Loading] Starting loading sequence...');

        // Simulate loading steps
        for (let i = 0; i < this.loadingSteps.length; i++) {
            this.currentStep = i;
            await this.executeStep(this.loadingSteps[i]);
        }

        // Wait a bit before hiding
        await this.delay(500);

        // Hide loading screen and show main app
        this.complete();
    }

    /**
     * Execute a single loading step
     */
    async executeStep(step) {
        this.targetProgress = step.progress;
        this.loadingText.textContent = step.text;
        this.statusText.textContent = step.status;

        // Animate progress bar
        await this.animateProgress(this.targetProgress);

        // Wait between steps (simulate loading time)
        const delay = step.progress === 100 ? 300 : Math.random() * 300 + 200;
        await this.delay(delay);
    }

    /**
     * Animate progress bar to target value
     */
    async animateProgress(target) {
        return new Promise((resolve) => {
            const step = 1;
            const interval = setInterval(() => {
                if (this.currentProgress < target) {
                    this.currentProgress += step;
                    if (this.currentProgress > target) {
                        this.currentProgress = target;
                    }
                    this.updateProgress(this.currentProgress);
                } else {
                    clearInterval(interval);
                    resolve();
                }
            }, 10);
        });
    }

    /**
     * Update progress bar and percentage display
     */
    updateProgress(progress) {
        this.progressBar.style.width = progress + '%';
        this.loadingPercent.textContent = Math.floor(progress) + '%';
    }

    /**
     * Complete loading and show main app
     */
    complete() {
        console.log('[Loading] Loading complete!');

        // Fade out loading screen
        this.loadingScreen.classList.add('fade-out');

        // Wait for fade out animation, then show main app
        setTimeout(() => {
            this.loadingScreen.style.display = 'none';
            this.mainApp.style.display = 'flex';

            // Trigger app initialization
            if (window.NiTriTeApp) {
                window.NiTriTeApp.init();
            }

            console.log('[Loading] Main app displayed');
        }, 500);
    }

    /**
     * Utility delay function
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Update loading progress manually (for real loading tasks)
     */
    setProgress(progress, text = null, status = null) {
        this.targetProgress = progress;
        if (text) this.loadingText.textContent = text;
        if (status) this.statusText.textContent = status;
        this.animateProgress(progress);
    }
}

// Auto-start loading when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('[Loading] DOM ready, initializing loading screen...');

    const loader = new LoadingManager();
    window.loadingManager = loader;

    // Start loading sequence
    loader.start();
});
