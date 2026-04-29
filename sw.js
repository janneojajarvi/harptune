const CACHE_NAME = 'harptune-v16';
const ASSETS = [
  './',
  './index.html',
  './style.css',
  './script.js',
  './manifest.json',
  './kuva.ico',
  './kuva.png',
  './harpkuva.png',
  './harptunefinderkuva.png',
  './pitkisplayer.png',
  
  // Peruskirjastot ja testit
  './FinnishTunes.js',
  './FinnishTunes2.js',
  './sekalaista01.js',
  './richardrobinsonbook.js',
  './suomitest1.js',
  './suomitest2.js',
  './suomitest3.js',
  
  // Kansainväliset setit
  './EdinburghKlezmer.js',
  './allklez.js',
  './balk1.js',
  './chinese1.js',
  './france.js',
  './intl.js',
  './norway1.js',
  './swedish2.js',
  
  // Esävelmät-sarja
  './esavelmat_hs1.js',
  './esavelmat_kansantanssit.js',
  './esavelmat_kansantanssit2.js',
  './esavelmat_kjs.js',
  './esavelmat_kt1.js',
  './esavelmat_ls1.js',
  './esavelmat_ls2.js',
  './esavelmat_ls3.js',
  './esavelmat_ls4.js',
  './esavelmat_rs1.js',
  './esavelmat_rs2.js',
  './esavelmat_setti1.js',
  
  // Folkwiki ja muut kokoelmat
  './folkwikiSet1.js',
  './folkwikiSet2.js',
  './folkwikiSet3.js',
  './fsfolkdiktning01.js',
  './fsfolkdiktning02.js',
  './extrasetti5.js',
  
  // SessionSet-sarja (01-18)
  './sessionSet01.js',
  './sessionSet02.js',
  './sessionSet03.js',
  './sessionSet04.js',
  './sessionSet05.js',
  './sessionSet06.js',
  './sessionSet07.js',
  './sessionSet08.js',
  './sessionSet09.js',
  './sessionSet10.js',
  './sessionSet11.js',
  './sessionSet12.js',
  './sessionSet13.js',
  './sessionSet14.js',
  './sessionSet15.js',
  './sessionSet16.js',
  './sessionSet17.js',
  './sessionSet18.js'
];

// Asennusvaihe: Tallennetaan perustiedostot välimuistiin
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

// Aktivoituminen
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
