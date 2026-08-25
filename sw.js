// ClassPulse Service Worker — v1.0
// Caches everything for full offline use

const CACHE_NAME = "classpulse-v18";

// Files to cache on install (the shell)
const PRECACHE = [
  "./",
  "./index.html",
  "./manifest.json",
  // React + Babel from CDN (cache on first fetch via network-first below)
];

// CDN URLs to cache when first loaded
const CDN_HOSTS = [
  "unpkg.com",
];

// ─── INSTALL ──────────────────────────────────────────────────────────────────
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(PRECACHE);
    }).then(() => self.skipWaiting())
  );
});

// ─── ACTIVATE ─────────────────────────────────────────────────────────────────
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

// ─── FETCH ────────────────────────────────────────────────────────────────────
self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);

  // CDN resources: cache-first (they never change for a given version)
  if (CDN_HOSTS.some(h => url.hostname.includes(h))) {
    event.respondWith(
      caches.match(event.request).then(cached => {
        if (cached) return cached;
        return fetch(event.request).then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          }
          return response;
        }).catch(() => cached); // offline fallback to whatever we have
      })
    );
    return;
  }

  // App shell: network-first, fall back to cache
  event.respondWith(
    fetch(event.request)
      .then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      })
      .catch(() => caches.match(event.request).then(cached => {
        if (cached) return cached;
        // Ultimate fallback: serve index.html for navigation requests
        if (event.request.mode === "navigate") {
          return caches.match("./index.html");
        }
      }))
  );
});
