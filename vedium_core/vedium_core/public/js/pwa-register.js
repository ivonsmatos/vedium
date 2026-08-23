// =============================================================================
// Vedium - Registro PWA seguro
// -----------------------------------------------------------------------------
// O PWA antigo cacheava navegacao/API e podia deixar paginas brancas apos deploy.
// Este registro fica restrito ao site publico e usa um SW network-safe: sem cache
// para login, API, LMS, app, checkout ou navegacao HTML.
// =============================================================================

(function () {
    'use strict';

    var PUBLIC_HOSTS = ['vediums.com', 'www.vediums.com'];
    // sw.js gerencia sua própria versão de cache (CACHE_NAME) e já limpa
    // versões antigas no evento `activate`. Aqui só removemos caches de fora
    // desse esquema (ex.: PWA antigo, pré-versionamento) — nunca um valor de
    // versão fixo, pra não brigar com o sw.js quando a versão for atualizada.
    var CACHE_PREFIX = 'vedium-static-';

    function isPublicHost() {
        return PUBLIC_HOSTS.indexOf(window.location.hostname) !== -1;
    }

    function cleanupCaches() {
        if (!window.caches || !caches.keys) return;
        caches.keys()
            .then(function (keys) {
                keys.forEach(function (key) {
                    if (key.indexOf(CACHE_PREFIX) !== 0) caches.delete(key);
                });
            })
            .catch(function () { /* noop */ });
    }

    function unregisterAll() {
        if (!('serviceWorker' in navigator) || !navigator.serviceWorker.getRegistrations) return;
        navigator.serviceWorker.getRegistrations()
            .then(function (registrations) {
                registrations.forEach(function (reg) {
                    reg.unregister();
                });
            })
            .catch(function () { /* noop */ });
    }

    function registerServiceWorker() {
        navigator.serviceWorker.register('/sw.js', {
            scope: '/',
            updateViaCache: 'none'
        })
            .then(function (registration) {
                registration.update();
            })
            .catch(function () { /* noop */ });
    }

    try {
        cleanupCaches();

        if (!isPublicHost()) {
            unregisterAll();
            return;
        }

        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function () {
                if ('requestIdleCallback' in window) {
                    window.requestIdleCallback(registerServiceWorker, { timeout: 2000 });
                } else {
                    window.setTimeout(registerServiceWorker, 0);
                }
            });
        }
    } catch (e) {
        /* noop */
    }
})();
