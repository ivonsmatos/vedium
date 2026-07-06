// =============================================================================
// Vedium — Push Notifications Client
// Gerencia assinatura Web Push e comunicação com o backend.
// Só faz sentido pra usuários autenticados (Guest não tem onde persistir
// a subscription — ver push_notifications.save_subscription).
// =============================================================================
(function () {
    'use strict';

    let vapidKeyCache = null;

    async function getVapidKey() {
        if (vapidKeyCache !== null) return vapidKeyCache;
        try {
            const r = await frappe.call({ method: 'vedium_core.push_notifications.get_vapid_public_key' });
            vapidKeyCache = (r.message && r.message.vapid_public_key) || '';
        } catch (err) {
            vapidKeyCache = '';
        }
        return vapidKeyCache;
    }

    function urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
        const rawData = atob(base64);
        return new Uint8Array([...rawData].map(c => c.charCodeAt(0)));
    }

    async function subscribePush(registration) {
        const vapidKey = await getVapidKey();
        if (!vapidKey) {
            console.warn('[Vedium Push] VAPID key não configurada');
            return null;
        }

        try {
            const existing = await registration.pushManager.getSubscription();
            if (existing) return existing;

            const subscription = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: urlBase64ToUint8Array(vapidKey),
            });

            // Envia a subscription ao backend
            await frappe.call({
                method: 'vedium_core.push_notifications.save_subscription',
                args: { subscription_json: JSON.stringify(subscription) },
            });

            return subscription;
        } catch (err) {
            // Usuário negou permissão ou erro de rede — não bloquear
            console.warn('[Vedium Push] Subscrição falhou:', err.message);
            return null;
        }
    }

    async function requestPermissionAndSubscribe() {
        if (typeof frappe === 'undefined' || !frappe.session || frappe.session.user === 'Guest') return;
        if (!('Notification' in window) || !('serviceWorker' in navigator)) return;
        if (Notification.permission === 'denied') return;

        let permission = Notification.permission;
        if (permission === 'default') {
            permission = await Notification.requestPermission();
        }
        if (permission !== 'granted') return;

        const registration = await navigator.serviceWorker.ready;
        await subscribePush(registration);
    }

    // Expõe para uso nos componentes da página (ex: botão "Ativar notificações")
    window.VediumPush = {
        requestPermission: requestPermissionAndSubscribe,

        isSupported() {
            return 'Notification' in window && 'serviceWorker' in navigator && 'PushManager' in window;
        },

        async getStatus() {
            if (!this.isSupported()) return 'unsupported';
            return Notification.permission; // 'default' | 'granted' | 'denied'
        },

        async unsubscribe() {
            if (!('serviceWorker' in navigator)) return;
            const reg = await navigator.serviceWorker.ready;
            const sub = await reg.pushManager.getSubscription();
            if (!sub) return;
            await sub.unsubscribe();
            await frappe.call({
                method: 'vedium_core.push_notifications.remove_subscription',
                args: { endpoint: sub.endpoint },
            });
        },
    };

    // Auto-inscrever usuários que já deram permissão (ex: refresh da página)
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            if (Notification.permission === 'granted') requestPermissionAndSubscribe();
        });
    } else {
        if (Notification.permission === 'granted') requestPermissionAndSubscribe();
    }
})();
