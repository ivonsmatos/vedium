// =============================================================================
// Vedium - PWA Registration
// =============================================================================

(function () {
    'use strict';

    const SW_PATH = '/sw.js';
    const SW_SCOPE = '/';

    // Check if service workers are supported
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', async () => {
            try {
                const registration = await navigator.serviceWorker.register(SW_PATH, {
                    scope: SW_SCOPE
                });

                console.log('[PWA] Service Worker registered:', registration.scope);

                // Check for updates
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    console.log('[PWA] New Service Worker installing...');

                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            // New update available
                            showUpdateNotification();
                        }
                    });
                });

            } catch (error) {
                console.error('[PWA] Service Worker registration failed:', error);
            }
        });

        // Handle controller change (new SW activated)
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            console.log('[PWA] Controller changed, reloading...');
            window.location.reload();
        });
    }

    // Show update notification
    function showUpdateNotification() {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('Vedium Atualizado', {
                body: 'Uma nova versão está disponível. Recarregue para atualizar.',
                icon: '/assets/vedium_core/images/icon-192x192.png'
            });
        }

        // Show in-app notification
        if (window.frappe && window.frappe.show_alert) {
            frappe.show_alert({
                message: 'Nova versão disponível! <a href="javascript:location.reload()">Atualizar</a>',
                indicator: 'green'
            }, 10);
        }
    }

    // Request notification permission on first interaction
    document.addEventListener('click', requestNotificationPermission, { once: true });

    function requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission().then(permission => {
                console.log('[PWA] Notification permission:', permission);
            });
        }
    }

    // Install prompt handling
    let deferredPrompt = null;

    window.addEventListener('beforeinstallprompt', (e) => {
        console.log('[PWA] Install prompt available');
        e.preventDefault();
        deferredPrompt = e;

        // Show custom install button
        showInstallButton();
    });

    function showInstallButton() {
        // Check if already installed
        if (window.matchMedia('(display-mode: standalone)').matches) {
            return;
        }

        // Create install button
        const installBtn = document.createElement('button');
        installBtn.id = 'vedium-install-btn';
        installBtn.className = 'vedium-install-btn';
        installBtn.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="7 10 12 15 17 10"/>
        <line x1="12" y1="15" x2="12" y2="3"/>
      </svg>
      <span>Instalar App</span>
    `;

        installBtn.style.cssText = `
      position: fixed;
      bottom: 80px;
      right: 20px;
      z-index: 9999;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 20px;
      background: linear-gradient(135deg, #166534, #14532d);
      color: white;
      border: none;
      border-radius: 12px;
      font-family: inherit;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 4px 20px rgba(22, 101, 52, 0.4);
      transition: all 0.3s ease;
    `;

        installBtn.addEventListener('click', async () => {
            if (!deferredPrompt) return;

            deferredPrompt.prompt();
            const { outcome } = await deferredPrompt.userChoice;

            console.log('[PWA] Install outcome:', outcome);
            deferredPrompt = null;
            installBtn.remove();
        });

        document.body.appendChild(installBtn);

        // Auto-hide after 10 seconds
        setTimeout(() => {
            if (installBtn.parentNode) {
                installBtn.style.opacity = '0';
                setTimeout(() => installBtn.remove(), 300);
            }
        }, 10000);
    }

    // Track if app is installed
    window.addEventListener('appinstalled', () => {
        console.log('[PWA] App installed successfully');
        deferredPrompt = null;

        // Track installation
        if (window.frappe && window.frappe.call) {
            frappe.call({
                method: 'vedium_core.api.track_pwa_install',
                async: true
            });
        }
    });

    console.log('[PWA] Vedium PWA registration script loaded');
})();
