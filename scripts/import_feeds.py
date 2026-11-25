"""Pulls Medium, Substack and YouTube feeds into content/imported-*.json. Existing entries are kept."""
import json, os, re, urllib.request, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(open(f"{ROOT}/scripts/feeds.json"))
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (feed-importer)"})
    return ET.fromstring(urllib.request.urlopen(req, timeout=25).read())
def ln(t): return t.rsplit("}", 1)[-1]
def text(el, name):
    k = [c for c in el if ln(c.tag) == name]; return (k[0].text or "").strip() if k else ""
def day(s):
    try: return parsedate_to_datetime(s).date().isoformat()
    except Exception: return (s or "")[:10]
def clean(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h or "")).strip()
def items(root): return [e for e in root.iter() if ln(e.tag) in ("item", "entry")]
def load(n):
    try: return json.load(open(f"{ROOT}/content/{n}.json"))["items"]
    except Exception: return []
def save(n, new, old):
    seen = {i["url"] for i in old}
    out = sorted(old + [i for i in new if i["url"] not in seen], key=lambda i: i.get("date", ""), reverse=True)
    json.dump({"items": out}, open(f"{ROOT}/content/{n}.json", "w"), indent=2, ensure_ascii=False); print(n, len(out))
W = []
for plat, key in (("Medium", "medium"), ("Substack", "substack")):
    if not cfg.get(key): continue
    try:
        for it in items(get(cfg[key])):
            link = text(it, "link") or next((c.get("href", "") for c in it if ln(c.tag) == "link"), "")
            W.append({"title": text(it, "title"), "platform": plat, "category": "Life & Experiences",
                "date": day(text(it, "pubDate") or text(it, "published")), "url": link.split("?")[0],
                "description": clean(text(it, "description") or text(it, "summary"))[:180], "featured": False, "draft": False, "sample": False})
    except Exception as ex: print("skip", plat, ex)
save("imported-writing", W, load("imported-writing"))
V = []
for ch in cfg.get("youtube", []):
    if not ch.get("channel_id"): continue
    try:
        for it in items(get("https://www.youtube.com/feeds/videos.xml?channel_id=" + ch["channel_id"])):
            v = text(it, "videoId")
            V.append({"title": text(it, "title"), "channel": ch["channel"], "url": "https://www.youtube.com/watch?v=" + v, "date": day(text(it, "published")),
                "duration": "", "thumbnail": f"https://i.ytimg.com/vi/{v}/hqdefault.jpg", "sample": False, "draft": False})
    except Exception as ex: print("skip", ch["channel"], ex)
save("imported-videos", V, load("imported-videos"))

# GitHub repositories (rendered into the home page at build time, so visitors never hit the API rate limit)
try:
    hdr = {"User-Agent": "Mozilla/5.0 (feed-importer)", "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"): hdr["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request("https://api.github.com/users/pramodtidke/repos?sort=pushed&per_page=12", headers=hdr)
    repos = [{"name": r["name"], "url": r["html_url"], "description": r.get("description") or "", "language": r.get("language") or "repo", "pushed": (r.get("pushed_at") or "")[:10]}
             for r in json.load(urllib.request.urlopen(req, timeout=25)) if not r.get("fork")][:6]
    if repos:
        json.dump({"items": repos}, open(f"{ROOT}/content/github-repos.json", "w"), indent=2, ensure_ascii=False); print("github-repos", len(repos))
except Exception as ex: print("skip github", ex)
