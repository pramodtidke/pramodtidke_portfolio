const V="pt-__BUILD__",ASSETS=V+"-assets",MAX=60;
self.addEventListener("install",()=>self.skipWaiting());
self.addEventListener("activate",e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>!x.startsWith(V)).map(x=>caches.delete(x)))).then(()=>clients.claim())));
function trim(c){return c.keys().then(k=>k.length>MAX?c.delete(k[0]).then(()=>trim(c)):0)}
self.addEventListener("fetch",e=>{
  const r=e.request,u=new URL(r.url);
  if(r.method!=="GET"||u.origin!==location.origin||u.pathname.startsWith("/admin/")||r.headers.has("range"))return;
  const isAsset=u.pathname.startsWith("/assets/")&&!u.pathname.endsWith("data.json");
  if(isAsset){
    // static assets: cache first (files are replaced whenever a new build changes the cache version)
    e.respondWith(caches.open(ASSETS).then(c=>c.match(r).then(hit=>hit||fetch(r).then(res=>{if(res.ok&&res.type==="basic")c.put(r,res.clone()).then(()=>trim(c));return res}))));
    return;
  }
  // pages and data: network first, fall back to cache, then to the home page when offline
  e.respondWith(fetch(r).then(res=>{if(res.ok&&res.type==="basic"){const cp=res.clone();caches.open(V).then(c=>c.put(r,cp).then(()=>trim(c)))}return res}).catch(()=>caches.match(r).then(x=>x||caches.match("/")||new Response("Offline",{status:503,headers:{"Content-Type":"text/plain"}}))));
});
