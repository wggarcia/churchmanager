// Cache básico do app
const CACHE_NAME = "adsjs-cache-v1";
const urlsToCache = [
  "/",
  "/static/css/bootstrap.min.css",
  "/static/css/adsjs.css",
  "/static/js/bootstrap.bundle.min.js",
  "/static/icon-192.png",
  "/static/icon-512.png"
];

// Instala e armazena os arquivos
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

// Intercepta requisições e serve do cache offline
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});

// Atualiza o cache antigo
self.addEventListener("activate", event => {
  const whitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.map(key => {
        if (!whitelist.includes(key)) {
          return caches.delete(key);
        }
      }))
    )
  );
});
