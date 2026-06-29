const CACHE_NAME = 'vedium-static-v3';
const CACHEABLE_PATHS = [
    '/assets/vedium_core/vedium_assets/images/logos/Icone-color.png',
    '/assets/vedium_core/vedium_assets/images/favicons/android-chrome-192x192.png',
    '/assets/vedium_core/vedium_assets/images/favicons/android-chrome-512x512.png'
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

self.addEventListener('install', (event) => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(CACHEABLE_PATHS)).catch(() => undefined)
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys()
            .then((keys) => Promise.all(keys.map((key) => key === CACHE_NAME ? undefined : caches.delete(key))))
            .then(() => self.clients.claim())
    );
});

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
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone)).catch(() => undefined);
                }
                return response;
            })
            .catch(() => caches.match(event.request))
    );
});
