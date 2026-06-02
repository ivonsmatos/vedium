// =============================================================================
// Vedium - Limpeza de Service Worker (PWA desativado)
// -----------------------------------------------------------------------------
// O service worker do PWA estava interceptando e cacheando respostas de API
// (inclusive 404 capturados durante deploys), o que quebrava o LMS (telas em
// branco, erros "Failed to convert value to 'Response'"). Como o site não
// depende de PWA/offline, este script DESREGISTRA qualquer service worker
// existente e limpa todos os caches do navegador. Roda em todas as paginas do
// site (web_include_js), entao limpa o SW de quem ja visitou.
// =============================================================================

(function () {
    'use strict';

    try {
        if ('serviceWorker' in navigator && navigator.serviceWorker.getRegistrations) {
            navigator.serviceWorker.getRegistrations()
                .then(function (registrations) {
                    registrations.forEach(function (reg) {
                        reg.unregister();
                    });
                })
                .catch(function () { /* noop */ });
        }

        if (window.caches && caches.keys) {
            caches.keys()
                .then(function (keys) {
                    keys.forEach(function (key) {
                        caches.delete(key);
                    });
                })
                .catch(function () { /* noop */ });
        }
    } catch (e) {
        /* noop */
    }
})();
