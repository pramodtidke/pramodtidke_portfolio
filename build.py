#!/usr/bin/env python3
"""Static site generator: content/*.json + content/blog/*.md -> _site/ (real pages, blog, RSS, sitemap)."""
import datetime, glob, html, json, os, re, shutil, sys, urllib.parse as up
from email.utils import format_datetime
import markdown, yaml

BASE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(BASE, "_site")
SITE = os.environ.get("SITE_URL", "https://pramodtidke.in").rstrip("/")
TODAY = datetime.date.today().isoformat()
EMAIL = "pramodtidkework@gmail.com"
ENT = lambda s: "".join(f"&#{ord(c)};" for c in s)
EMAIL_H = ENT(EMAIL)
esc = lambda s: html.escape(str(s if s is not None else ""), quote=True)

def J(n, d):
    try: return json.load(open(f"{BASE}/content/{n}.json", encoding="utf8"))
    except Exception: return d
def items(n): return [i for i in J(n, {}).get("items", []) if not i.get("draft")]
def slugify(s): return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")[:70] or "item"
def fd(d):
    try: return datetime.date.fromisoformat(str(d)[:10]).strftime("%-d %b %Y")
    except Exception: return esc(d)
def dday(i): return str(i.get("date", ""))[:10]

# ---------- content
site = J("site", {}); about = J("about", {}); now = J("now", {}); PF = items("profiles")
CATS = ["Technology & AI", "Business & Entrepreneurship", "Finance & Economics", "Marketing & Creativity", "Personal Development", "Life & Experiences"]

def posts():
    out = []
    for f in sorted(glob.glob(f"{BASE}/content/blog/*.md")):
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", open(f, encoding="utf8").read(), re.S)
        if not m: continue
        meta = yaml.safe_load(m.group(1)) or {}; body = m.group(2)
        d = str(meta.get("date", TODAY))[:10]
        if meta.get("draft") or d > TODAY: continue
        out.append(dict(title=meta.get("title", "Untitled"), date=d, description=meta.get("description", ""),
            category=meta.get("category", "Life & Experiences"), tags=meta.get("tags") or [], cover=meta.get("cover") or "",
            platform="On this site", url="", sample=bool(meta.get("sample")), blog=True, featured=bool(meta.get("featured")),
            body=markdown.markdown(body, extensions=["fenced_code", "tables", "sane_lists"]),
            minutes=max(1, round(len(re.findall(r"\w+", body)) / 200)),
            slug=meta.get("slug") or slugify(meta.get("title", os.path.basename(f)))))
    return out

def writing():
    W = posts(); seen = set()
    for i in items("writing") + items("imported-writing"):
        if dday(i) > TODAY: continue
        k = i.get("url") if up.urlparse(i.get("url", "")).path.strip("/") else i.get("title")
        if k in seen: continue
        seen.add(k); j = dict(i); j.update(blog=False, date=dday(i), slug=slugify(i.get("title", "")), tags=i.get("tags") or []); W.append(j)
    W.sort(key=lambda i: i["date"], reverse=True); used = set()
    for i in W:
        s, n = i["slug"], 2
        while s in used: s = f'{i["slug"]}-{n}'; n += 1
        used.add(s); i["slug"] = s; i["p"] = f"writing/{s}/"
    return W

W = writing(); VD = sorted([dict(i, date=dday(i)) for i in items("videos") + items("imported-videos") if dday(i) <= TODAY], key=lambda i: i["date"], reverse=True)
seenv = set(); vk = lambda v: v["url"] if up.urlparse(v["url"]).path.strip("/") not in ("", ) and "watch" in v["url"] else v["title"]
VD = [v for v in VD if not (vk(v) in seenv or seenv.add(vk(v)))]
PJ = items("projects"); used = set()
for i in PJ:
    s, n = i.get("slug") or slugify(i["name"]), 2; b = s
    while s in used: s = f"{b}-{n}"; n += 1
    used.add(s); i["slug"] = s; i["p"] = f"projects/{s}/"
EX = sorted([i for i in items("explore")], key=lambda i: str(i.get("date", "")), reverse=True)
TS = items("testimonials")

# ---------- layout
PAGES = []
NAV = [("Home", ""), ("About", "about/"), ("Writing", "writing/"), ("Videos", "videos/"), ("Projects", "projects/"), ("Now", "now/"), ("Explore", "explore/"), ("Games", "games/"), ("Connect", "connect/")]
CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline' https://plausible.io; style-src 'self' 'unsafe-inline'; font-src 'self'; "
       "img-src 'self' data: https:; frame-src https://www.youtube-nocookie.com; connect-src 'self' https://plausible.io; "
       "form-action 'self' https://formsubmit.co; base-uri 'self'; object-src 'none'")
NAVG = [("About", [("About", "about/"), ("Now", "now/")]), ("Content", [("Writing", "writing/"), ("Videos", "videos/")]),
        ("Projects", "projects/"), ("Explore", [("Explore", "explore/"), ("Games", "games/")]), ("Connect", "connect/")]
def navlinks(root, path):
    on = lambda p: path.startswith(p)
    def a(l, p, extra=""):
        cur = on(p); cls = (extra + (" on" if cur else "")).strip()
        return f'<a href="{root}{p}"' + (f' class="{cls}"' if cls else "") + (' aria-current="page"' if cur else "") + f'>{l}</a>'
    out = ""
    for l, v in NAVG:
        if isinstance(v, str): out += a(l, v, "cn" if v == "connect/" else "")
        else:
            act = any(on(p) for _, p in v)
            out += (f'<div class="dg"><button type="button" class="dd{" on" if act else ""}" aria-expanded="false" aria-haspopup="true">{l}<i aria-hidden="true"></i></button>'
                    f'<div class="dm">{"".join(a(x, p) for x, p in v)}</div></div>')
    return out
FAV = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23E8431F'/%3E%3Ctext x='32' y='43' font-size='30' text-anchor='middle' fill='white' font-family='sans-serif' font-weight='800'%3EPT%3C/text%3E%3C/svg%3E"
PERSON = {"@type": "Person", "@id": SITE + "/#person", "name": "Pramod Tidke", "url": SITE + "/", "jobTitle": "DevOps Engineer",
    "image": SITE + "/assets/og-image.png", "alumniOf": {"@type": "CollegeOrUniversity", "name": "G. H. Raisoni Institute of Engineering & Technology"},
    "knowsAbout": ["DevOps", "Cloud", "Artificial intelligence", "Digital marketing", "CI/CD"], "sameAs": [p["url"] for p in PF if p["url"].startswith("http")]}

def page(path, title, desc, body, sample=False, noindex=False, img=None, typ="website", ld=None, prio="0.7", date=None, canon=None):
    depth = path.count("/"); root = "../" * depth; url = f"{SITE}/{path}"; ni = noindex or sample; canon = canon or url
    og = img if img and img.startswith("http") else (f"{SITE}/{img.lstrip('/')}" if img else SITE + "/assets/og-image.png")
    if not ni and canon == url: PAGES.append((path, prio, date or TODAY))
    nav = (f'<nav id="nav" aria-label="Main"><a class="brand" href="{root}" aria-label="Home">PT</a><div class="nl">{navlinks(root, path)}</div>'
           f'<div class="tools"><button id="sb" type="button" aria-label="Search the site"><span class="si" aria-hidden="true">⌕</span><span class="sl">Search</span><kbd>⌘K</kbd></button>'
           f'<div class="dg setg"><button type="button" class="dd" aria-label="Settings" aria-expanded="false" aria-haspopup="true"><span aria-hidden="true">⚙</span></button>'
           f'<div class="dm"><button id="th" type="button" aria-label="Switch light and dark mode">◐ Theme</button><button id="calm" type="button" aria-label="Calm mode: turn motion off" aria-pressed="false">Calm mode</button></div></div>'
           f'<button id="mb" type="button" aria-label="Menu" aria-expanded="false">Menu</button></div></nav>')
    def grp(g): return "".join(f'<a href="{esc(p["url"])}">{esc(p["name"])}</a>' for p in PF if p.get("group") == g)
    foot = (f'<footer><div class="ww"><div class="ftop"><h2>Let’s build, write<br>or explore something.</h2><a class="mail" href="{ENT("mailto:")}{EMAIL_H}"><small>Say hello</small>{EMAIL_H}</a></div>'
            f'<div class="fcols"><div><h4>Pages</h4>{"".join(f"<a href={chr(34)}{root}{p}{chr(34)}>{l}</a>" for l, p in NAV)}</div><div><h4>Platforms</h4>{grp("Platforms")}</div><div><h4>More</h4>{grp("More")}<a href="{root}feed.xml">RSS feed</a></div>'
            f'<div class="fsub"><h4>Newsletter</h4><p>New essays, straight to your inbox.</p><a class="b1" href="https://substack.com/@pramodtidke">Subscribe on Substack</a></div></div>'
            f'<div class="wm" aria-hidden="true">Pramod Tidke</div><div class="fb"><span>© 2026 Pramod Tidke · pramodtidke.in</span><span>Psst: ↑ ↑ ↓ ↓ ← → ← → B A</span><button id="up" onclick="scrollTo({{top:0,behavior:\'smooth\'}})">Back to top ↑</button></div></div></footer>')
    chat = ('<button id="cbt" aria-label="Ask the assistant">✦ Ask</button><section id="cp" aria-label="Assistant"><header><span>Ask about Pramod</span><button id="cx" aria-label="Close">×</button></header><div id="cm" aria-live="polite"></div><div id="cs"></div><div id="cf"><input id="ci" placeholder="Ask about work, writing, projects…" aria-label="Your question" autocomplete="off"><button id="cg">Send</button></div></section>'
            '<div id="pal" role="dialog" aria-modal="true" aria-label="Search"><div class="pb"><input id="pq" placeholder="Search articles, videos, projects, anything…" aria-label="Search" autocomplete="off"><ul id="pl"></ul><div class="ph" id="ph"></div></div></div><div id="toast" role="status"></div>')
    an = f'<script defer data-domain="{esc(site["analytics_domain"])}" src="https://plausible.io/js/script.js"></script>' if site.get("analytics_domain") else ""
    graph = [{"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Pramod Tidke", "inLanguage": "en"}]
    if path == "": graph.append(PERSON)
    for x in ([ld] if isinstance(ld, dict) else (ld or [])): graph.append(x)
    head = (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="{CSP}"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>{esc(title)}</title>'
        f'<meta name="description" content="{esc(desc)}"><link rel="canonical" href="{esc(canon)}"><meta name="robots" content="{"noindex,follow" if ni else "index,follow,max-image-preview:large"}"><meta name="author" content="Pramod Tidke"><meta name="theme-color" content="#15120E">'
        f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="{typ}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="Pramod Tidke"><meta property="og:locale" content="en_IN"><meta property="og:image" content="{esc(og)}">'
        f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{esc(og)}">'
        f'<link rel="alternate" type="application/rss+xml" title="Pramod Tidke" href="{root}feed.xml"><link rel="icon" href="{FAV}">'
        f'<link rel="preload" href="{root}assets/fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="{root}assets/fonts/dm-sans.woff2" as="font" type="font/woff2" crossorigin>'
        f'<link rel="manifest" href="{root}manifest.webmanifest"><link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">'
        f'<link rel="stylesheet" href="{root}assets/style.css">'
        '<script>try{var t=localStorage.getItem("t");if(t)document.documentElement.setAttribute("data-theme",t);if(localStorage.getItem("seen2"))document.documentElement.classList.add("go","noi");if(localStorage.getItem("calm")==="1")document.documentElement.classList.add("calm")}catch(e){}</script>'
        f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")}</script>{an}</head>')
    intro = '<div id="intro" role="presentation"><div class="ip t"></div><div class="ip b"></div><div class="ic"><span id="icn">0</span><b>Pramod Tidke</b><small>Engineer · Marketer · Explorer</small><div class="ibar" id="ibar"><i></i></div></div></div>' if path == "" else ""
    doc = (head + f'<body><a class="skip-link" href="#main">Skip to content</a>{intro}<div id="cr"><span></span></div><div id="cd"></div><div id="bar"></div>{nav}<main id="main">{body}</main>{foot}{chat}'
           f'<script>window.SITE={{"root":"{root}"}}</script><script src="{root}assets/site.js" defer></script></body></html>')
    d = os.path.join(OUT, path); os.makedirs(d, exist_ok=True); open(os.path.join(d, "index.html"), "w", encoding="utf8").write(doc)

# ---------- fragments
def crumbs(*pairs):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": n + 1, "name": nm, "item": SITE + "/" + pp} for n, (nm, pp) in enumerate(pairs)]}
def badges(i):
    b = ""
    if i.get("sample"): b += ' <span class="sm">Sample</span>'
    if i.get("blog"): b += ' <span class="sm" style="background:var(--ac);color:#fff">On this site</span>'
    if i.get("featured"): b += ' <span class="sm" style="background:var(--tx);color:var(--bg)">Featured</span>'
    return b
def wrow(i, root):
    c = i.get("category", "")
    return (f'<a class="er" href="{root}{i["p"]}" data-cat="{esc(c)}"><div><small>{fd(i["date"])}</small><br><span class="pf">{esc(i.get("platform", ""))} · {esc(c.split(" &")[0])}</span></div>'
            f'<div><h3>{esc(i["title"])}{badges(i)}</h3><p>{esc(i.get("description", ""))}</p></div><span class="ar">→</span></a>')
def vcard(i):
    h = (len(str(i["title"])) * 37) % 360
    th = f'<img src="{esc(i["thumbnail"])}" alt="" loading="lazy">' if i.get("thumbnail") else ""
    dur = f'<small>{esc(i["duration"])}</small>' if i.get("duration") else ""
    return (f'<a class="vc" href="{esc(i["url"])}" target="_blank" rel="noopener"><div class="th" style="--h:{h}">{th}{dur}</div><h3>{esc(i["title"])}{badges(i)}</h3><p>{esc(i.get("channel", ""))} · {fd(i["date"])}</p></a>')
SC = {"Completed": "#19A974", "In progress": "#E8431F", "Experiment": "#F5B335", "On hold": "#9A9486"}
def chips(a): return '<div class="chips">' + "".join(f"<span>{esc(t)}</span>" for t in a) + "</div>"
def filters(vals, target):
    return f'<div class="chips" data-filter="{target}"><button class="fc on" data-v="All">All</button>' + "".join(f'<button class="fc" data-v="{esc(v)}">{esc(v)}</button>' for v in vals) + "</div>"
def share(url, title):
    q = up.quote
    return (f'<div class="share"><button type="button" data-copy="{esc(url)}">Copy link</button><a href="https://twitter.com/intent/tweet?text={q(title)}&url={q(url)}" target="_blank" rel="noopener">Share on X</a>'
            f'<a href="https://www.linkedin.com/sharing/share-offsite/?url={q(url)}" target="_blank" rel="noopener">LinkedIn</a><a href="https://wa.me/?text={q(title + " " + url)}" target="_blank" rel="noopener">WhatsApp</a></div>')
CTA = '<div class="cta"><b>Enjoyed this?</b><p>Get new essays by email.</p><a class="b1" href="https://substack.com/@pramodtidke">Subscribe on Substack</a></div>'
def lead(h, t): return f'<div class="wrap"><h1 class="pg">{h}</h1><p class="lead">{t}</p>'

# ---------- pages
def home():
    r = ""; st = esc(site.get("status") or "Building in public"); words = site.get("hero_words") or ["Engineer", "Marketer", "Explorer", "Writer", "Builder"]
    hs = (site.get("headshot") or "").lstrip("/"); img = f'<img id="hs" src="{esc(hs)}" alt="Pramod Tidke" width="520" height="520">' if hs else ""
    hero = (f'<header class="hero"><div class="ww"><div class="hg"><div class="hl"><p class="chip rise2"><i></i><span id="hstat">{st}</span></p>'
        '<h1 class="nm" aria-label="Pramod Tidke"><span class="w">Pramod</span><span class="w">Tidke</span></h1>'
        f'<p class="role rise2">I’m an <span id="rot" data-w="{esc(json.dumps(words))}">{esc(words[0])}</span></p><p class="sub rise2">Building with technology. Exploring with curiosity.</p>'
        '<div class="bt rise2"><a class="b1" href="writing/">Read my writing</a><a class="b2" href="projects/">See projects</a><a class="b2" href="games/">Play a game</a></div></div>'
        '</div>'
        '<div class="p5"><span>Think &amp; Write</span><span>Build &amp; Create</span><span>Learn &amp; Explore</span><span>Experience &amp; Share</span><span>Connect &amp; Publish</span></div></div></header>')
    tick = '<div class="tick" aria-hidden="true"><div>' + "Engineer ✦ Marketer ✦ Explorer ✦ DevOps ✦ Cloud ✦ AI ✦ Writing ✦ Building ✦ " * 4 + "</div></div>"
    stmt = f'<section class="st"><div class="ww"><p id="hst">{esc((about.get("statement_main", "This is my home on the internet.") + " " + about.get("statement_muted", "")).strip())}</p></div></section>'
    start = ('<section class="ww"><h2 class="sh" style="margin-top:0">Start here</h2><div class="start"><a href="about/"><b>Hiring?</b><small>See my background and experience →</small></a>'
             '<a href="projects/"><b>Need something built?</b><small>Look at the projects, then get in touch →</small></a><a href="writing/"><b>Here to read?</b><small>Essays and notes, sorted by subject →</small></a></div></section>')
    intro = esc(about.get("intro") or "Computer science graduate, former trader and DevOps engineer, now building independently across technology, marketing and my own brand.")
    B = [("c7", "about/", "About", intro, ["DevOps", "Cloud", "AI", "Marketing"]), ("c5 k1", "writing/", "Writing", "Essays and reflections from every platform, sorted by subject.", ["Technology & AI", "Business", "Finance", "Marketing", "Personal Development", "Life"]),
         ("c4", "videos/", "Videos", "Two YouTube channels: @thepramodtidke and SevenLearn.", []), ("c4 k2", "projects/", "Projects", "Apps, experiments and businesses, with the lessons from each.", ["In progress", "Experiment", "Completed"]),
         ("c4 k3", "now/", "Now", "What I’m working on, learning and reading at the moment.", []), ("c6", "explore/", "Explore", "Learning notes, books and selected experiences.", ["Notes", "Books", "Experiences"]),
         ("c6 k2", "games/", "Games", "A small arcade of mind games: memory, logic, speed and a daily riddle.", ["Memory", "Logic", "Reflex"]), ("c12 k1", "connect/", "Connect", "Every public profile in one place, plus email.", [])]
    bento = '<section class="ww"><div class="bento">' + "".join(f'<a class="bc {c}" href="{h}"><div><h3>{t}</h3><p>{d}</p></div><div class="ft">{chips(ch) if ch else "<span></span>"}<span class="ar">↗</span></div></a>' for c, h, t, d, ch in B) + "</div></section>"
    feed = sorted([dict(i, kind="w") for i in W] + [dict(i, kind="v") for i in VD], key=lambda i: i["date"], reverse=True)[:4]
    def frow(i):
        if i["kind"] == "w": return wrow(i, "")
        return f'<a class="er" href="{esc(i["url"])}" target="_blank" rel="noopener"><div><small>{fd(i["date"])}</small><br><span class="pf">YouTube · {esc(i.get("channel", ""))}</span></div><div><h3>{esc(i["title"])}{badges(i)}</h3></div><span class="ar">↗</span></a>'
    feedh = '<section class="ww feed"><div class="fh"><h2 class="sh">Latest from everywhere</h2><a class="b2" href="writing/">All writing</a></div>' + ("".join(frow(i) for i in feed) or '<p class="note">Nothing here yet.</p>') + "</section>"
    yt = ""
    for v in VD:
        m = re.search(r"watch\?v=([\w-]{11})", v["url"])
        if m: yt = f'<section class="ww feed"><h2 class="sh">Latest video</h2><button class="yt" data-id="{m.group(1)}" aria-label="Play: {esc(v["title"])}"><img src="https://i.ytimg.com/vi/{m.group(1)}/hqdefault.jpg" alt="" loading="lazy"><span>▶</span></button></section>'; break
    repos = items("github-repos")[:4]
    gh = ('<section class="ww feed"><div class="fh"><h2 class="sh">Latest on GitHub</h2><a class="b2" href="https://github.com/pramodtidke">All repositories</a></div><div>'
          + "".join(f'<a class="er" href="{esc(x["url"])}" target="_blank" rel="noopener"><div><small>{fd(x.get("pushed", ""))}</small><br><span class="pf">GitHub · {esc(x.get("language", "repo"))}</span></div><div><h3>{esc(x["name"])}</h3><p>{esc(x.get("description", ""))}</p></div><span class="ar">↗</span></a>' for x in repos)
          + '</div></section>') if repos else ""
    ts = ('<section class="ww feed"><h2 class="sh">Kind words</h2><div class="grid">' + "".join(f'<div class="quote"><p>“{esc(t.get("quote", ""))}”</p><small>{esc(t.get("name", ""))}, {esc(t.get("role", ""))}</small></div>' for t in TS) + "</div></section>") if TS else ""
    page("", "Pramod Tidke · DevOps Engineer, Marketer, Explorer", "Pramod Tidke is a DevOps, cloud and AI engineer and marketer. Read his writing, see his projects and videos, and play a few mind games.", hero + tick + stmt + bento + feedh + yt + gh + ts, prio="1.0")

def about_page():
    bio = esc(about.get("bio") or "Biography and motivation, in my own words, will go here. Until then, here is the short version.")
    page("about/", "About · Pramod Tidke", "Computer science graduate, former trader and DevOps engineer at Capgemini, now building independently across DevOps, cloud, AI and marketing.", '<div class="wrap">' + open(f"{BASE}/templates/about.html", encoding="utf8").read().replace("{{BIO}}", bio) + "</div>", prio="0.8")

def writing_pages():
    body = lead("Writing", "Everything I publish, sorted by subject. Posts marked “On this site” are written here; the rest link to the original.")
    if any(i.get("sample") for i in W): body += '<p class="note"><span class="sm">Sample</span> Demo entries show how this page will look. Replace them from the dashboard.</p>'
    body += filters(CATS, "#wl") + '<div id="wl">' + ("".join(wrow(i, "../") for i in W) or '<p class="note">Nothing here yet.</p>') + '</div><div style="height:90px"></div></div>'
    page("writing/", "Writing · Pramod Tidke", "Essays, notes and posts by Pramod Tidke on technology, business, finance, marketing and life.", body, prio="0.8")
    for i in W:
        url = f'{SITE}/{i["p"]}'; tags = chips(i["tags"]) if i["tags"] else ""
        rel = [j for j in W if j is not i and (j["category"] == i["category"] or set(j["tags"]) & set(i["tags"]))][:3]
        relh = ('<h2 class="sh" style="font-size:1.6rem">Keep reading</h2>' + "".join(wrow(j, "../../") for j in rel)) if rel else ""
        cover = f'<img class="cover" src="../../{esc(i["cover"].lstrip("/"))}" alt="" loading="lazy">' if i.get("cover") and not i["cover"].startswith("http") else (f'<img class="cover" src="{esc(i["cover"])}" alt="" loading="lazy">' if i.get("cover") else "")
        crumb = '<p class="crumb"><a href="../">← All writing</a></p>'
        if i["blog"]:
            meta = f'<p class="meta"><span>{fd(i["date"])}</span><span>{i["minutes"]} min read</span><span>{esc(i["category"])}</span></p>'
            main = f'<article class="post">{crumb}<h1>{esc(i["title"])}{badges(i)}</h1>{meta}{tags}{cover}<div class="prose">{i["body"]}</div>{share(url, i["title"])}{CTA}{relh}<div style="height:90px"></div></article>'
            ld = {"@type": "BlogPosting", "headline": i["title"], "datePublished": i["date"], "description": i["description"], "author": {"@id": SITE + "/#person"}, "dateModified": i["date"], "image": (i["cover"] if i.get("cover","").startswith("http") else SITE + "/" + (i.get("cover") or "assets/og-image.png").lstrip("/")), "publisher": {"@id": SITE + "/#person"}, "mainEntityOfPage": url, "keywords": ", ".join(i["tags"])}
            page(i["p"], f'{i["title"]} · Pramod Tidke', i["description"] or i["title"], main, sample=i["sample"], img=i.get("cover") or None, typ="article", ld=[ld, crumbs(("Home", ""), ("Writing", "writing/"), (i["title"], i["p"]))], date=i["date"])
        else:
            plat = esc(i.get("platform", "the original site")); meta = f'<p class="meta"><span>{fd(i["date"])}</span><span>{plat}</span><span>{esc(i.get("category", ""))}</span></p>'
            main = (f'<article class="post">{crumb}<h1>{esc(i["title"])}{badges(i)}</h1>{meta}<div class="prose"><p>{esc(i.get("description", ""))}</p></div>'
                    f'<p><a class="b1" href="{esc(i.get("url", "#"))}" target="_blank" rel="noopener">Read the full article on {plat} ↗</a></p>{share(url, i["title"])}{relh}<div style="height:90px"></div></article>')
            orig = i.get("url", ""); d0 = i.get("description") or i["title"]
            page(i["p"], f'{i["title"]} · Pramod Tidke', d0 if len(d0) >= 110 else f'{d0} Originally published on {i.get("platform", "another site")}; summary and link by Pramod Tidke.', main, sample=bool(i.get("sample")), typ="article", date=i["date"], prio="0.5", canon=orig if orig.startswith("http") and up.urlparse(orig).path.strip("/") else None, ld=crumbs(("Home", ""), ("Writing", "writing/"), (i["title"], i["p"])))

def videos_page():
    body = lead("Videos", "Two YouTube channels, one place.") + ('<div class="bento" style="padding:30px 0 10px"><a class="bc k1" href="https://www.youtube.com/@thepramodtidke"><div><h3>@thepramodtidke</h3><p>My main channel.</p></div><div class="ft"><span></span><span class="ar">↗</span></div></a>'
        '<a class="bc k2" href="https://www.youtube.com/@sevenlearnn"><div><h3>SevenLearn</h3><p>The learning channel.</p></div><div class="ft"><span></span><span class="ar">↗</span></div></a></div>')
    if any(i.get("sample") for i in VD): body += '<p class="note"><span class="sm">Sample</span> Demo entries show how this page will look. Replace them from the dashboard.</p>'
    body += '<div class="vgd">' + ("".join(vcard(i) for i in VD) or '<p class="note">Nothing here yet.</p>') + '</div><div style="height:90px"></div></div>'
    page("videos/", "Videos · Pramod Tidke", "Videos from Pramod Tidke’s two YouTube channels, @thepramodtidke and SevenLearn: DevOps, technology and learning content, all in one place.", body, prio="0.6")

def projects_pages():
    body = lead("Projects", "A build log of apps, experiments and businesses, with status, lessons, and links. Unfinished experiments get published too.")
    if any(i.get("sample") for i in PJ): body += '<p class="note"><span class="sm">Sample</span> Demo entries show how this page will look. Replace them from the dashboard.</p>'
    cards = ""
    for i in PJ:
        links = f'<a href="../{i["p"]}">Case study →</a>' + (f'<a href="{esc(i["github"])}">GitHub ↗</a>' if i.get("github") else "") + (f'<a href="{esc(i["live"])}">Live ↗</a>' if i.get("live") else "")
        cards += (f'<div class="pc" data-cat="{esc(i["status"])}"><span class="bd" style="--c:{SC.get(i["status"], "#9A9486")}">{esc(i["status"])}</span><h3>{esc(i["name"])}{badges(i)}</h3><p>{esc(i.get("problem", ""))}</p>{chips(i.get("tech") or [])}'
                  + (f'<small>Lesson: {esc(i["lesson"])}</small>' if i.get("lesson") else "") + links + "</div>")
    body += filters(["Completed", "In progress", "Experiment", "On hold"], "#pj") + f'<div class="pcs" id="pj">{cards or "<p class=note>Nothing here yet.</p>"}</div><div style="height:90px"></div></div>'
    page("projects/", "Projects · Pramod Tidke", "Apps, experiments and businesses built by Pramod Tidke, with the problem, the tech and the lessons from each.", body, prio="0.8")
    for i in PJ:
        sec = lambda h, t: f'<h2 class="sh" style="font-size:1.6rem">{h}</h2><div class="prose"><p>{esc(t)}</p></div>' if t else ""
        shot = f'<img class="cover" src="../../{esc(i["screenshot"].lstrip("/"))}" alt="Screenshot of {esc(i["name"])}" loading="lazy">' if i.get("screenshot") else ""
        links = "".join(f'<a class="b2" href="{esc(i[k])}" target="_blank" rel="noopener">{t} ↗</a>' for k, t in (("github", "View on GitHub"), ("live", "Open live")) if i.get(k))
        main = (f'<article class="post"><p class="crumb"><a href="../">← All projects</a></p><h1>{esc(i["name"])}{badges(i)}</h1><p class="meta"><span class="bd" style="--c:{SC.get(i["status"], "#9A9486")}">{esc(i["status"])}</span>' + (f'<span>{esc(i["role"])}</span>' if i.get("role") else "") + f'</p>{shot}'
                + sec("The problem", i.get("problem")) + sec("What I did", i.get("what_i_did")) + (f'<h2 class="sh" style="font-size:1.6rem">Tech</h2>{chips(i["tech"])}' if i.get("tech") else "") + sec("What I learned", i.get("lesson")) + f'<div class="bt" style="margin-top:30px">{links}</div>{share(SITE + "/" + i["p"], i["name"])}<div style="height:90px"></div></article>')
        pd = i.get("problem") or i["name"]
        page(i["p"], f'{i["name"]} · Project · Pramod Tidke', pd if len(pd) >= 110 else f'{pd} A {i["status"].lower()} project by Pramod Tidke, with the tech used and what was learned.', main, sample=bool(i.get("sample")), prio="0.6", ld=crumbs(("Home", ""), ("Projects", "projects/"), (i["name"], i["p"])))

def small_pages():
    nb = '<div class="nowbox">' + "".join(f'<div class="card"><b>{t}</b><ul>' + "".join(f"<li>{esc(x)}</li>" for x in now.get(k, [])) + "</ul></div>" for t, k in (("Working on", "working_on"), ("Learning", "learning"), ("Reading", "reading"), ("Goals", "goals"), ("Next", "next"))) + "</div>"
    page("now/", "Now · Pramod Tidke", "What Pramod Tidke is working on, learning and reading right now: a living snapshot in the spirit of the now-page idea, updated from time to time.", lead("Now", "What I’m doing at the moment.") + nb + '<p class="lead" style="margin-bottom:90px"><small>Inspired by the “now page” idea: a snapshot, not a history.</small></p></div>', prio="0.5")
    exr = "".join(f'<div class="er" data-cat="{esc(i.get("type", ""))}"><div><small>{fd(i.get("date", ""))}</small><br><span class="pf">{esc(i.get("type", ""))}</span></div><div><h3>{esc(i["title"])}{badges(i)}</h3><p>{esc(i.get("text", ""))}</p></div><span></span></div>' for i in EX)
    note = '<p class="note"><span class="sm">Sample</span> Demo entries show how this page will look. Replace them from the dashboard.</p>' if any(i.get("sample") for i in EX) else ""
    page("explore/", "Explore · Pramod Tidke", "Learning notes, books and selected experiences from Pramod Tidke, collected in one place and filterable by type so you can find what interests you.", lead("Explore", "Learning notes, books and selected experiences.") + note + filters(["Learning notes", "Books", "Experiences"], "#ex") + f'<div id="ex">{exr or "<p class=note>Nothing here yet.</p>"}</div><div style="height:90px"></div></div>', prio="0.5")
    page("games/", "Games · Pramod Tidke", "A small arcade of mind games: memory match, tic-tac-toe, reaction test, mental math, pattern memory, number sequences and a daily riddle.",
         lead("Games", "A tiny arcade of mind games. Best scores are saved on this device only.") + '<div class="gl" id="gl"></div><div class="gp" id="gp" hidden></div><div style="height:90px"></div></div>', prio="0.5")
    links = "".join(f'<a href="{esc(p["url"])}"><b>{esc(p["name"])}</b><small>{esc(p.get("note", ""))}</small></a>' for p in PF)
    form = (f'<form class="contact" action="https://formsubmit.co/{EMAIL_H}" method="POST"><label class="hp">Leave empty<input name="_honey" tabindex="-1" autocomplete="off"></label><input type="hidden" name="_subject" value="New message from pramodtidke.in"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_next" value="{SITE}/connect/?sent=1">'
            '<input name="name" placeholder="Your name" aria-label="Your name" required><input name="email" type="email" placeholder="Your email" aria-label="Your email" required><textarea name="message" placeholder="Your message" aria-label="Your message" required></textarea><button class="b1" type="submit">Send message</button></form>')
    page("connect/", "Connect · Pramod Tidke", "Email Pramod Tidke, send a message through the contact form, or find him on GitHub, LinkedIn, YouTube, Instagram, X, Medium and Substack.",
         lead("Connect", "The best way to reach me is email. Every public profile is below, with what I share there.") + f'<a class="mail" style="margin-top:34px" href="{ENT("mailto:")}{EMAIL_H}"><small>Email</small>{EMAIL_H}</a><h2 class="sh">Or send a message</h2>{form}<h2 class="sh">Profiles</h2><div class="plinks">{links}</div></div>', prio="0.6")

# ---------- build
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT); shutil.copytree(f"{BASE}/assets", f"{OUT}/assets")
for f in ("CNAME", "robots.txt", "404.html", "manifest.webmanifest"):
    if os.path.exists(f"{BASE}/{f}"): shutil.copy(f"{BASE}/{f}", OUT)
open(f"{OUT}/sw.js", "w", encoding="utf8").write(open(f"{BASE}/sw.js", encoding="utf8").read().replace("__BUILD__", datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S")))
shutil.copytree(f"{BASE}/admin", f"{OUT}/admin")
home(); about_page(); writing_pages(); videos_page(); projects_pages(); small_pages()
data = {"WR": [{k: i.get(k, "") for k in ("title", "platform", "category", "date", "description", "url", "sample", "p")} for i in W],
        "VD": VD, "PJ": [{k: i.get(k, "") for k in ("name", "status", "problem", "tech", "lesson", "github", "live", "sample", "p")} for i in PJ],
        "EX": EX, "PF": PF, "N": now, "A": about, "R": items("games")}
json.dump(data, open(f"{OUT}/assets/data.json", "w", encoding="utf8"), ensure_ascii=False)
sm = "".join(f"<url><loc>{SITE}/{p}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>" for p, pr, d in PAGES)
open(f"{OUT}/sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
ri = "".join(f'<item><title>{esc(i["title"])}</title><link>{SITE}/{i["p"]}</link><guid>{SITE}/{i["p"]}</guid><pubDate>{format_datetime(datetime.datetime.fromisoformat(i["date"]).replace(tzinfo=datetime.timezone.utc))}</pubDate><description>{esc(i["description"])}</description></item>' for i in W if not i["sample"])
open(f"{OUT}/feed.xml", "w", encoding="utf8").write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>Pramod Tidke</title><link>{SITE}/</link><atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/><language>en</language><description>Writing by Pramod Tidke</description><lastBuildDate>{format_datetime(datetime.datetime.now(datetime.timezone.utc))}</lastBuildDate>{ri}</channel></rss>')
# link check
bad = []
for f in glob.glob(f"{OUT}/**/*.html", recursive=True):
    if f.endswith("/404.html"): continue
    for m in re.finditer(r'(?:href|src)="([^"]*)"', open(f, encoding="utf8").read()):
        u = re.split(r"[#?]", html.unescape(m.group(1)), 1)[0]
        if not u: continue
        if re.match(r"^(https?:|mailto:|data:|javascript:|//)", u): continue
        t = os.path.normpath(os.path.join(os.path.dirname(f), u))
        if not (os.path.isfile(t) or os.path.isfile(os.path.join(t, "index.html"))): bad.append((os.path.relpath(f, OUT), u))
print(f"built {len(PAGES)} indexable pages; {len(W)} writing entries, {len(PJ)} projects; broken links: {len(bad)}")
for b in bad[:20]: print("  BROKEN", b)
sys.exit(1 if bad else 0)
