// =============================================================================
// Vedium - Service Worker KILL-SWITCH (PWA desativado)
// -----------------------------------------------------------------------------
// O SW antigo (offline-first) cacheava respostas de API — inclusive 404
// capturados durante deploys — e quebrava o LMS (telas brancas).
// Este arquivo continua sendo servido em /sw.js para que navegadores com o
// SW antigo registrado baixem ESTA versão no próximo update e se
// auto-destruam: desregistra, limpa caches e recarrega as abas controladas.
// Complementa o pwa-register.js (que desregistra do lado da página).
// NÃO reativar PWA sem estratégia network-first para /api/*.
// =============================================================================

self.addEventListener('install', () => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        (async () => {
            // Limpa todos os caches deixados pelo SW antigo
            const keys = await caches.keys();
            await Promise.all(keys.map((key) => caches.delete(key)));

            // Desregistra este próprio service worker
            await self.registration.unregister();

            // Recarrega abas que ainda estavam sob controle do SW antigo
            const clientsList = await self.clients.matchAll({ type: 'window' });
            clientsList.forEach((client) => client.navigate(client.url));
        })()
    );
});

// Sem handler de fetch: o navegador volta a ir direto à rede.
