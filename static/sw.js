const CACHE_NAME = 'classifieds-cache-v1';
const urlsToCache = [
  '/', // Cache the homepage
  '/static/manifest.json',
  // Add paths to your main CSS and JS files if they are static
  // e.g., '/static/css/custom.css', '/static/js/custom.js'
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js',
  // Add paths to your icons
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  '/offline.html' // A simple offline fallback page
];

// Install event: Cache the core assets
self.addEventListener('install', event => {
  console.log('Service Worker: Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: Caching core assets');
        return cache.addAll(urlsToCache);
      })
      .catch(error => {
        console.error('Service Worker: Failed to cache core assets:', error);
      })
      .then(() => self.skipWaiting()) // Activate the new service worker immediately
  );
});

// Activate event: Clean up old caches
self.addEventListener('activate', event => {
  console.log('Service Worker: Activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: Clearing old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim()) // Take control of uncontrolled clients
  );
});

// Fetch event: Serve cached assets or fetch from network
self.addEventListener('fetch', event => {
  // Only handle GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        // Cache hit - return response
        if (cachedResponse) {
          return cachedResponse;
        }

        // Not in cache - fetch from network
        return fetch(event.request).then(
          networkResponse => {
            // Check if we received a valid response
            if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
              // Don't cache invalid responses (like opaque responses from CDNs without CORS)
              // unless it's a CDN asset we explicitly trust and want to cache
              if (event.request.url.startsWith('https://cdn.jsdelivr.net')) {
                 // Clone the response to cache it
                 let responseToCache = networkResponse.clone();
                 caches.open(CACHE_NAME)
                   .then(cache => {
                     cache.put(event.request, responseToCache);
                   });
              }
              return networkResponse;
            }

            // Clone the response. A response is a stream and
            // can only be consumed once. We need one for the browser
            // and one for the cache.
            let responseToCache = networkResponse.clone();

            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return networkResponse;
          }
        ).catch(() => {
          // Network request failed, try to return offline page
          if (event.request.mode === 'navigate') { // Only for page navigations
            return caches.match('/offline.html');
          }
        });
      })
  );
});