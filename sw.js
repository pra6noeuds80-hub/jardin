/* Service worker : le site fonctionne hors ligne après la première visite.
   Il ne touche ni aux musiques (mp3/mp4), ni aux requêtes vers d'autres sites (météo, radios). */
const CACHE = 'jardin-lunaire-v1';
const SHELL = ['./', './index.html', './poster.jpg', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(k => Promise.all(k.filter(n => n !== CACHE).map(n => caches.delete(n)))).then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const r = e.request, u = new URL(r.url);
  if (r.method !== 'GET' || u.origin !== location.origin) return;
  if (r.headers.has('range') || /\.(mp4|mp3|m4a|ogg|wav)$/i.test(u.pathname)) return;
  e.respondWith(
    caches.match(r).then(hit => {
      const net = fetch(r).then(res => {
        if (res && res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(r, copy)); }
        return res;
      }).catch(() => hit);
      return hit || net;
    })
  );
});
