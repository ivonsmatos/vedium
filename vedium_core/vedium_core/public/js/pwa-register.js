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
    var SAFE_CACHE = 'vedium-static-v3';

    function isPublicHost() {
        return PUBLIC_HOSTS.indexOf(window.location.hostname) !== -1;
    }

    function cleanupCaches() {
        if (!window.caches || !caches.keys) return;
        caches.keys()
            .then(function (keys) {
                keys.forEach(function (key) {
                    if (key !== SAFE_CACHE) caches.delete(key);
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

    try {
        cleanupCaches();

        if (!isPublicHost()) {
            unregisterAll();
            return;
        }

        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function () {
                fetch('/sw.js', { method: 'HEAD', cache: 'no-store' })
                    .then(function (response) {
                        if (!response.ok) return null;
                        return navigator.serviceWorker.register('/sw.js', { scope: '/' });
                    })
                    .then(function (registration) {
                        if (registration) registration.update();
                    })
                    .catch(function () { /* noop */ });
            });
        }
    } catch (e) {
        /* noop */
    }
})();
