const CACHE_NAME = 'vedium-static-v5';
const CACHEABLE_PATHS = [
    '/assets/vedium_core/vedium_assets/images/logos/Icone-color.png',
    '/assets/vedium_core/vedium_assets/images/favicons/android-chrome-192x192.png?v=icon-v2',
    '/assets/vedium_core/vedium_assets/images/favicons/android-chrome-512x512.png?v=icon-v2'
];
const BYPASS_PREFIXES = [
    '/api/',
    '/app',
    '/lms',
    '/login',
    '/checkout',
    '/socket.io/',
    '/payments',
    '/webhook'
];

// ─────────────────────────────────────────────
// Install — pré-cache de assets críticos
// ─────────────────────────────────────────────
self.addEventListener('install', (event) => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(CACHEABLE_PATHS))
            .catch(() => undefined)
    );
});

// ─────────────────────────────────────────────
// Activate — limpa caches antigos
// ─────────────────────────────────────────────
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys()
            .then((keys) => Promise.all(
                keys.map((key) => key === CACHE_NAME ? undefined : caches.delete(key))
            ))
            .then(() => self.clients.claim())
    );
});

// ─────────────────────────────────────────────
// Fetch — Network-first com cache de assets
// ─────────────────────────────────────────────
function shouldBypass(requestUrl, request) {
    if (request.method !== 'GET') return true;
    if (requestUrl.origin !== self.location.origin) return true;
    if (request.mode === 'navigate') return true;
    return BYPASS_PREFIXES.some((prefix) => requestUrl.pathname.startsWith(prefix));
}

self.addEventListener('fetch', (event) => {
    const requestUrl = new URL(event.request.url);
    if (shouldBypass(requestUrl, event.request)) return;

    event.respondWith(
        fetch(event.request)
            .then((response) => {
                if (response && response.ok && requestUrl.pathname.startsWith('/assets/')) {
                    const clone = response.clone();
                    caches.open(CACHE_NAME)
                        .then((cache) => cache.put(event.request, clone))
                        .catch(() => undefined);
                }
                return response;
            })
            .catch(() => caches.match(event.request))
    );
});

// ─────────────────────────────────────────────
// Push Notifications
// ─────────────────────────────────────────────
self.addEventListener('push', (event) => {
    if (!event.data) return;

    let payload;
    try {
        payload = event.data.json();
    } catch {
        payload = { title: 'Vedium', body: event.data.text() };
    }

    const title   = payload.title  || 'Vedium';
    const options = {
        body:    payload.body    || 'Você tem uma novidade!',
        icon:    payload.icon    || '/assets/vedium_core/vedium_assets/images/favicons/android-chrome-192x192.png?v=icon-v2',
        badge:   payload.badge   || '/assets/vedium_core/vedium_assets/images/logos/Icone-color.png',
        image:   payload.image   || undefined,
        data:    { url: payload.url || '/' },
        tag:     payload.tag     || 'vedium-notification',
        renotify: !!payload.renotify,
        vibrate: [200, 100, 200],
        actions: payload.actions || [],
    };

    event.waitUntil(self.registration.showNotification(title, options));
});

// ─────────────────────────────────────────────
// Notification click — abre a URL correta
// ─────────────────────────────────────────────
self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    const targetUrl = (event.notification.data && event.notification.data.url) || '/';

    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then((windowClients) => {
                // Foca uma aba já aberta se possível
                for (const client of windowClients) {
                    if (client.url.includes(self.location.origin) && 'focus' in client) {
                        client.navigate(targetUrl);
                        return client.focus();
                    }
                }
                // Abre nova aba
                if (clients.openWindow) return clients.openWindow(targetUrl);
            })
    );
});
