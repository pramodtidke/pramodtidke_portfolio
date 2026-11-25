# Browser smoke tests (needs: pip install playwright && playwright install chromium).
# Usage: python build.py && (cd _site && python -m http.server 8766 &) && python tests/browser_test.py
import asyncio, re, json, sys
from playwright.async_api import async_playwright
BASE="http://localhost:8766"
PAGES=["","about/","writing/","videos/","projects/","projects/this-personal-website/","now/","explore/","games/","connect/","writing/sample-post-how-to-write-on-this-site/","404.html"]
res=[]
def ck(name,ok,detail=""):
    res.append((name,ok,detail)); print(("PASS " if ok else "FAIL ")+name+(" — "+str(detail) if detail and not ok else (" ("+str(detail)+")" if detail else "")))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for dev,vp,touch in (("desktop",{"width":1366,"height":800},False),("mobile",{"width":375,"height":700},True)):
            ctx=await b.new_context(viewport=vp,has_touch=touch,is_mobile=touch); 
            for pg in PAGES:
                page=await ctx.new_page(); errs=[]
                page.on("pageerror",lambda e:errs.append("JS:"+str(e)[:100]))
                page.on("console",lambda m:errs.append(m.text[:140]) if m.type in("error","warning") and "Content Security" in m.text else (errs.append("ERR:"+m.text[:100]) if m.type=="error" and "Failed to load resource" not in m.text else None))
                await page.goto(f"{BASE}/{pg}",wait_until="load"); await page.wait_for_timeout(1800)
                m=await page.evaluate("""()=>({ox:document.documentElement.scrollWidth>document.documentElement.clientWidth+1,
                  navh:(document.querySelector('nav#nav')||{getBoundingClientRect:()=>({height:0,right:0,left:0})}).getBoundingClientRect().height,
                  navr:(document.querySelector('nav#nav')||{getBoundingClientRect:()=>({right:0})}).getBoundingClientRect().right,vw:innerWidth})""")
                ck(f"{dev} {pg or '/'}: no overflow/JS/CSP errors", (not m['ox']) and not errs, errs[:2] or ("overflow" if m['ox'] else ""))
                if pg!="404.html":
                    ck(f"{dev} {pg or '/'}: nav compact & inside viewport", (m['navh']<=75 if dev=="desktop" else m['navh']<=64) and m['navr']<=m['vw']+0.5, f"h={m['navh']:.0f} right={m['navr']:.0f}/{m['vw']}")
                await page.close()
            await ctx.close()
        # ---- desktop interaction tests
        ctx=await b.new_context(viewport={"width":1366,"height":800}); pg=await ctx.new_page()
        await pg.goto(BASE+"/about/",wait_until="load"); await pg.wait_for_timeout(1500)
        tops=await pg.evaluate("()=>[...document.querySelectorAll('nav .nl>a, nav .nl>.dg>.dd')].map(e=>e.textContent.trim())")
        ck("desktop: 5 top-level nav items",len(tops)==5,tops)
        ck("desktop: About group highlighted on /about/",await pg.evaluate("()=>document.querySelector('nav .dd.on')?.textContent.includes('About')"))
        await pg.hover("nav .nl>.dg:nth-child(2)>.dd"); await pg.wait_for_timeout(300)
        ck("desktop: hover opens Write & Watch menu",await pg.evaluate("()=>getComputedStyle(document.querySelectorAll('.nl .dm')[1]).display==='flex'"))
        await pg.mouse.move(600,500); await pg.wait_for_timeout(300)
        ck("desktop: menu closes when mouse leaves",await pg.evaluate("()=>getComputedStyle(document.querySelectorAll('.nl .dm')[1]).display==='none'"))
        await pg.click("nav .nl>.dg:nth-child(4)>.dd"); await pg.wait_for_timeout(200)
        ck("desktop: click opens Explore menu + aria-expanded",await pg.evaluate("()=>document.querySelectorAll('.nl .dd')[2].getAttribute('aria-expanded')==='true'"))
        await pg.keyboard.press("Escape"); await pg.wait_for_timeout(200)
        ck("desktop: Esc closes menu",await pg.evaluate("()=>!document.querySelector('.dg.open')"))
        await pg.click("nav .nl>.dg:nth-child(4)>.dd"); await pg.click("body",position={"x":600,"y":500}); await pg.wait_for_timeout(200)
        ck("desktop: outside click closes menu",await pg.evaluate("()=>!document.querySelector('.dg.open')"))
        await pg.hover("nav .nl>.dg:nth-child(4)>.dd"); await pg.click("nav .nl>.dg:nth-child(4) .dm a:has-text('Games')"); await pg.wait_for_url("**/games/"); 
        ck("desktop: sub-menu link navigates (Games)",pg.url.endswith("/games/"))
        await pg.wait_for_timeout(1200)
        ck("desktop: Explore group highlighted on /games/",await pg.evaluate("()=>document.querySelector('nav .dd.on')?.textContent.includes('Explore')"))
        # settings: theme + calm
        t0=await pg.evaluate("()=>getComputedStyle(document.documentElement).colorScheme")
        await pg.click(".setg>.dd"); await pg.click("#th"); await pg.wait_for_timeout(200)
        t1=await pg.evaluate("()=>getComputedStyle(document.documentElement).colorScheme")
        ck("desktop: settings menu theme toggle works",t0!=t1,f"{t0}->{t1}")
        await pg.click("#calm"); await pg.wait_for_timeout(200)
        ck("desktop: calm toggle works",await pg.evaluate("()=>document.documentElement.classList.contains('calm')&&document.querySelector('#calm').getAttribute('aria-pressed')==='true'"))
        # search + chat
        await pg.keyboard.press("Escape"); await pg.keyboard.press("Control+k"); await pg.wait_for_timeout(300)
        await pg.fill("#pq","projects"); await pg.wait_for_timeout(300)
        n=await pg.evaluate("()=>document.querySelectorAll('#pl li').length")
        ck("desktop: ⌘K search returns results",n>0,n)
        await pg.keyboard.press("Escape")
        await pg.click("#cbt"); await pg.fill("#ci","who is pramod"); await pg.click("#cg"); await pg.wait_for_timeout(1500)
        ck("desktop: chat assistant answers",await pg.evaluate("()=>document.querySelector('#cm').innerText.length>40"))
        # games smoke
        await pg.goto(BASE+"/games/",wait_until="load"); await pg.wait_for_timeout(1500)
        ng=await pg.evaluate("()=>document.querySelectorAll('#gl > *').length")
        ck("desktop: games list renders",ng>=5,ng)
        # email obfuscation
        h=open('/home/claude/site/_site/connect/index.html').read()
        ck("email not in plain text in HTML",'pramodtidkework@gmail.com' not in h and '@gmail' not in h)
        mt=await pg.evaluate("()=>1"); await pg.goto(BASE+"/connect/",wait_until="load")
        ck("mailto link decodes correctly in browser",await pg.evaluate("()=>document.querySelector('a.mail').href==='mailto:pramodtidkework@gmail.com'"))
        ck("contact form action decodes correctly",await pg.evaluate("()=>document.querySelector('form.contact').action==='https://formsubmit.co/pramodtidkework@gmail.com'"))
        # service worker
        await pg.wait_for_timeout(1500)
        sw=await pg.evaluate("""async()=>{try{const r=await navigator.serviceWorker.register('/sw.js');await navigator.serviceWorker.ready;await new Promise(x=>setTimeout(x,800));await fetch('/about/');await new Promise(x=>setTimeout(x,500));const k=await caches.keys();return {ok:true,keys:k}}catch(e){return {ok:false,e:String(e)}}}""")
        ck("service worker installs, activates and caches (versioned cache)",sw.get('ok') and any(x.startswith('pt-2') for x in sw.get('keys',[])),sw)
        await ctx.close()
        # ---- mobile interaction
        ctx=await b.new_context(viewport={"width":375,"height":600},has_touch=True,is_mobile=True); pg=await ctx.new_page()
        await pg.goto(BASE+"/projects/",wait_until="load"); await pg.wait_for_timeout(1500)
        await pg.tap("#mb"); await pg.wait_for_timeout(300)
        info=await pg.evaluate("""()=>{const n=document.querySelector('nav').getBoundingClientRect();const l=document.querySelector('.nl');return {open:document.querySelector('nav').classList.contains('open'),bottom:n.bottom,vh:innerHeight,links:l.querySelectorAll('a').length,heads:[...l.querySelectorAll('.dd')].map(e=>e.textContent.trim()),sh:l.scrollHeight,ch:l.clientHeight,cur:l.querySelector('a.on')?.textContent}}""")
        ck("mobile: menu opens with 3 group headings + 8 links",info['open'] and info['links']==8 and len(info['heads'])==3,info)
        ck("mobile: menu fits inside screen",info['bottom']<=info['vh'],f"{info['bottom']:.0f}/{info['vh']}")
        ck("mobile: current page highlighted",info['cur']=="Projects",info['cur'])
        await pg.screenshot(path="/tmp/t/m_menu.png")
        await pg.tap("body",position={"x":190,"y":580}); await pg.wait_for_timeout(300)
        ck("mobile: tap outside closes menu",not await pg.evaluate("()=>document.querySelector('nav').classList.contains('open')"))
        await pg.tap("#mb"); await pg.keyboard.press("Escape"); await pg.wait_for_timeout(200)
        ck("mobile: Esc closes menu",not await pg.evaluate("()=>document.querySelector('nav').classList.contains('open')"))
        await pg.tap("#mb"); await pg.tap(".nl a:has-text('Videos')"); await pg.wait_for_url("**/videos/")
        await pg.wait_for_timeout(500)
        ck("mobile: link navigates and menu closed",pg.url.endswith("/videos/") and not await pg.evaluate("()=>document.querySelector('nav').classList.contains('open')"))
        await pg.tap(".setg>.dd"); await pg.wait_for_timeout(200)
        r=await pg.evaluate("()=>{const m=document.querySelector('.setg .dm').getBoundingClientRect();return {l:m.left,r:m.right,w:innerWidth,disp:getComputedStyle(document.querySelector('.setg .dm')).display}}")
        ck("mobile: settings popover visible & inside screen",r['disp']=='flex' and r['l']>=0 and r['r']<=r['w'],r)
        await pg.screenshot(path="/tmp/t/m_settings.png")
        # tap target audit
        await pg.goto(BASE+"/",wait_until="load"); await pg.wait_for_timeout(2500)
        small=await pg.evaluate("""()=>[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!=='hidden'&&(r.height<40)&&!e.closest('.nl')&&e.id!=='cbt'}).map(e=>(e.className||e.tagName)+':'+Math.round(e.getBoundingClientRect().height)).slice(0,12)""")
        ck("mobile home: tap targets >=40px (visible controls)",len(small)==0,small)
        await ctx.close()
        await b.close()
    bad=[r for r in res if not r[1]]; print(f"\n{len(res)-len(bad)}/{len(res)} passed"); 
    sys.exit(1 if bad else 0)
asyncio.run(main())
