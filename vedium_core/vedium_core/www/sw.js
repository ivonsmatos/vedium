// =============================================================================
// Vedium - Service Worker (Offline First Strategy)
// =============================================================================

const CACHE_NAME = 'vedium-cache-v1';
const OFFLINE_URL = '/offline.html';

// Assets to cache immediately on install
const STATIC_ASSETS = [
    '/',
    '/app',
    '/offline.html',
    '/assets/vedium_core/css/vedium.css',
    '/assets/vedium_core/js/vedium.bundle.js',
    '/assets/vedium_core/images/icon-192x192.png',
    '/assets/vedium_core/images/icon-512x512.png',
    '/assets/frappe/css/frappe-web.css',
    '/assets/frappe/js/frappe-web.min.js',
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
    console.log('[SW] Installing Service Worker...');

    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[SW] Caching static assets...');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => {
                console.log('[SW] Static assets cached successfully');
                return self.skipWaiting();
            })
            .catch((error) => {
                console.error('[SW] Failed to cache static assets:', error);
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating Service Worker...');

    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames
                        .filter((name) => name !== CACHE_NAME)
                        .map((name) => {
                            console.log('[SW] Deleting old cache:', name);
                            return caches.delete(name);
                        })
                );
            })
            .then(() => {
                console.log('[SW] Service Worker activated');
                return self.clients.claim();
            })
    );
});

// Fetch event - Stale While Revalidate for assets, Network First for API
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Skip API calls and frappe methods (always network first)
    if (url.pathname.startsWith('/api/') ||
        url.pathname.startsWith('/method/') ||
        url.pathname.includes('.json')) {
        event.respondWith(networkFirst(request));
        return;
    }

    // For static assets, use stale-while-revalidate
    if (isStaticAsset(url.pathname)) {
        event.respondWith(staleWhileRevalidate(request));
        return;
    }

    // For pages, use network first with offline fallback
    event.respondWith(networkFirstWithOfflineFallback(request));
});

// Check if request is for static asset
function isStaticAsset(pathname) {
    const extensions = ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf'];
    return extensions.some(ext => pathname.endsWith(ext));
}

// Network First strategy
async function networkFirst(request) {
    try {
        const networkResponse = await fetch(request);
        return networkResponse;
    } catch (error) {
        const cachedResponse = await caches.match(request);
        return cachedResponse || new Response('Offline', { status: 503 });
    }
}

// Stale While Revalidate strategy
async function staleWhileRevalidate(request) {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);

    const fetchPromise = fetch(request)
        .then((networkResponse) => {
            if (networkResponse.ok) {
                cache.put(request, networkResponse.clone());
            }
            return networkResponse;
        })
        .catch(() => null);

    return cachedResponse || fetchPromise;
}

// Network First with Offline Fallback
async function networkFirstWithOfflineFallback(request) {
    try {
        const networkResponse = await fetch(request);

        // Cache successful page responses
        if (networkResponse.ok && request.mode === 'navigate') {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        // Try to get from cache first
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }

        // For navigation requests, show offline page
        if (request.mode === 'navigate') {
            const offlineResponse = await caches.match(OFFLINE_URL);
            if (offlineResponse) {
                return offlineResponse;
            }
        }

        return new Response('Offline - Vedium não está disponível', {
            status: 503,
            statusText: 'Service Unavailable',
            headers: new Headers({ 'Content-Type': 'text/plain' })
        });
    }
}

// Background Sync for offline actions
self.addEventListener('sync', (event) => {
    console.log('[SW] Background sync triggered:', event.tag);

    if (event.tag === 'vedium-sync') {
        event.waitUntil(syncOfflineData());
    }
});

async function syncOfflineData() {
    // TODO: Implement sync logic for offline data
    console.log('[SW] Syncing offline data...');
}

// Push Notifications
self.addEventListener('push', (event) => {
    if (!event.data) return;

    const data = event.data.json();

    const options = {
        body: data.body || 'Nova notificação do Vedium',
        icon: '/assets/vedium_core/images/icon-192x192.png',
        badge: '/assets/vedium_core/images/badge-72x72.png',
        vibrate: [100, 50, 100],
        data: {
            url: data.url || '/app'
        },
        actions: [
            { action: 'open', title: 'Abrir' },
            { action: 'dismiss', title: 'Dispensar' }
        ]
    };

    event.waitUntil(
        self.registration.showNotification(data.title || 'Vedium', options)
    );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    if (event.action === 'dismiss') return;

    const urlToOpen = event.notification.data?.url || '/app';

    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then((windowClients) => {
                // Focus existing window if available
                for (const client of windowClients) {
                    if (client.url.includes(urlToOpen) && 'focus' in client) {
                        return client.focus();
                    }
                }
                // Open new window
                if (clients.openWindow) {
                    return clients.openWindow(urlToOpen);
                }
            })
    );
});

console.log('[SW] Vedium Service Worker loaded');
