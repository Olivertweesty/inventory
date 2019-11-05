const cacheName = 'v1';

//call Install Event
self.addEventListener('install', (e) => {
	console.log('Service Worker: Installed');
});

//call Activate Event
self.addEventListener('activate', (e) => {
	console.log('Service Worker: Activated');
	
	
});

//Call Fetch Event
self.addEventListener('fetch', e => {
	console.log('Service Worker: Fetching');
	e.respondWith(
		fetch(e.request)
			.then(res => {
				const resClone = res.clone();
				caches
					.open(cacheName)
					.then(cache => {
						cache.put(e.request, resClone);
					});
					return res;
				}).catch(err => caches.match(e.request).then(res => res))
	);
});