"""TVV Longevity Watcher Digest site builder (GitHub Pages: Atlantean2/tvv-longevity-watcher-digest).

Usage (run from this folder):
  python3 build.py                                   # rebuild index.html + style.css from issues/*.html + issues.json
  python3 build.py YYYY-MM-DD "path/to/issue.docx" [--test]   # render that docx to issues/YYYY-MM-DD.html, then rebuild index

Every source stays a clickable https link; the docx Sources list is kept. Footer: Not medical advice.
Nothing is invented: text comes from the docx via mammoth; only layout classes are added.
"""
import os, re, sys, json, html, datetime, shutil
import mammoth
sys.path.insert(0, "/workspace/risk-watcher")
from tvv_nav import nav, NAV_CSS, favicon_links, ensure_favicons
os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = "TVV Longevity Watch"        # page <title>
H1 = "LONGEVITY WATCH"           # masthead title (all caps)
URL = "https://atlantean2.github.io/tvv-longevity-watcher-digest/"
NOTICE = "Not medical advice."
META = "issues.json"
E = lambda s: html.escape(str(s), quote=True)

def lab(d, test):
    x = datetime.date.fromisoformat(d)
    return f"{x:%b} {x.day}, {x.year}" + (" · test issue" if test else "")

def render(d, src, test):
    imgs = []
    def _img(i):
        # extract embedded image(s), compress to webp (max 900px wide) into issues/img/, with alt text
        from PIL import Image
        import io
        with i.open() as f: data = f.read()
        im = Image.open(io.BytesIO(data)).convert("RGB")
        if im.width > 900: im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
        os.makedirs("issues/img", exist_ok=True)
        fn = f"{d}-fig{len(imgs) + 1}.webp"
        im.save(f"issues/img/{fn}", "WEBP", quality=74, method=6)
        imgs.append(fn)
        alt = i.alt_text or "Illustration: an active older couple walking a sunlit forest trail, both wearing teal exoskeleton leg supports and glasses"
        return {"src": f"img/{fn}", "alt": alt, "width": str(im.width), "height": str(im.height), "loading": "lazy"}
    b = mammoth.convert_to_html(open(src, "rb"), convert_image=mammoth.images.img_element(_img)).value
    # embedded image paragraph -> centered figure
    b = re.sub(r"<p>(?:<strong>)?\s*(<img [^>]*/>)\s*(?:</strong>)?</p>", r'<figure class="end">\1</figure>', b)
    # Section Contents (docx 'Digest Sections:' list, entries typed '1.<tab>TITLE') -> linked list
    def _toc(m):
        items = re.findall(r"<p><strong>(\d{1,2})\.\s*([^<]*?)\s*</strong></p>", m.group(2))
        li = "".join(f'<p class="toc-item"><a href="#sec-{n}" class="toc-link">{n}. {t}</a></p>' for n, t in items)
        return f'<p class="toc-title">{m.group(1)}</p><div class="toc">{li}</div>'
    b = re.sub(r"<p><strong>(Digest Sections:|Section Contents:?)</strong></p>((?:<p><strong>\d{1,2}\.\t[^<]*</strong></p>)+)", _toc, b)
    # public page: drop local directory of the internal spreadsheet; drop internal routing note
    b = b.replace("/workspace/longevity-supplements/", "")
    b = re.sub(r"\s*Stays out of Victoria, TVV and Psychometric Assessments\.", "", b)
    # title line
    b = re.sub(r"<p><strong>(LONGEVITY DIGEST[^<]*)</strong></p>", r'<h1 class="issue-title">\1</h1>', b, count=1)
    # numbered section headings -> h2
    b = re.sub(r"<p><strong>(\d{1,2})\. ([A-Z][^<]{2,120})</strong></p>", r'<h2 class="desk" id="sec-\1">\1. \2</h2>', b)
    # not-medical-advice paragraph -> boxed notice
    b = re.sub(r"<p>(<strong>NOT MEDICAL ADVICE\.[^>]*</strong>.*?)</p>", r'<p class="notice">\1</p>', b, count=1, flags=re.S)
    # bullets
    b = re.sub(r"<p>\s*●\s*(.*?)</p>", r"<li>\1</li>", b, flags=re.S)
    b = re.sub(r"((?:<li>.*?</li>)+)", r'<ul class="items">\1</ul>', b, flags=re.S)
    b = b.replace("<table>", '<div class="tw"><table class="lw">').replace("</table>", "</table></div>")
    b = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', b)
    page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{T} — {d}</title>{favicon_links("../assets/")}<link rel="stylesheet" href="../assets/style.css">'
            f'<script>if(!/[?&]raw/.test(location.search))location.replace("../index.html#{d}")</script></head>'
            f'<body><main id="issue">{b}</main></body></html>')
    open(f"issues/{d}.html", "w").write(page)
    meta = json.load(open(META)) if os.path.exists(META) else {}
    meta[d] = {"test": bool(test), "docx": os.path.basename(src)}
    json.dump(meta, open(META, "w"), indent=1, sort_keys=True)
    print("rendered", d, len(b), "chars")

CSS = """body{margin:0;font:16px/1.55 Arial,Helvetica,sans-serif;color:#111;background:#fafafa}
#top{position:sticky;top:0;z-index:9;background:#fff;box-shadow:0 2px 6px #0002}
header{border-bottom:3px solid #1aa88b;display:flex;align-items:center;gap:14px;padding:8px 16px}
header img.logo{height:56px}header h1{font-size:1.25rem;margin:0}header .sub{font-size:.8rem;color:#444;margin-top:2px}
header .grow{flex:1 1 auto;min-width:0}
/* Masthead banner: Duo 3 painting (assets/masthead-duo3.webp, 1152x864), wide strip, cover, focus on the two people. */
.banner{max-width:1040px;margin:0 auto;background:#0b0f08}
.banner img{display:block;width:100%;aspect-ratio:2.4/1;max-height:400px;object-fit:cover;object-position:50% 3%}
/* Longevity Watcher Sage portrait slot: hidden for now (assets/sage.png kept, not shown). */
.sage-slot{display:none}
#tabs{display:flex;gap:6px;overflow-x:auto;white-space:nowrap;padding:6px 12px;background:#f3f3f3;border-bottom:1px solid #ddd;align-items:center}
#tabs .al{font:700 12px Arial,sans-serif;letter-spacing:1px;text-transform:uppercase;color:#555;padding-right:4px}
#tabs button{flex:0 0 auto;font:600 14px Arial,sans-serif;padding:6px 12px;border:1px solid #bbb;border-radius:16px;background:#fff;color:#222;cursor:pointer}
#tabs button[aria-selected=true]{background:#1aa88b;border-color:#1aa88b;color:#fff}
main{max-width:1040px;margin:0 auto;padding:16px;background:#fff}
a{color:#0645ad;text-decoration:underline}
h1.issue-title{font-size:1.35rem;margin:6px 0 10px}
h2{border-top:2px solid #1aa88b;padding-top:8px;margin-top:24px;font-size:1.2rem;font-weight:700;scroll-margin-top:130px}
ul.items{margin-left:24px;padding-left:1.1em}ul.items li{margin:7px 0}
.notice{border:3px solid #8B0000;background:#faf3f3;padding:10px 14px;margin:14px 0}
.tw{overflow-x:auto;margin:10px 0}table.lw{border-collapse:collapse;width:100%;font-size:.9rem}
table.lw th,table.lw td{border:1px solid #ccc;padding:5px 8px;text-align:left;vertical-align:top}table.lw th{background:#e9f7f3;white-space:nowrap}
table.lw td p,table.lw th p{margin:0}
table.lw{min-width:720px;font-size:.95rem}
.toc-title{font-weight:700;margin:14px 0 4px}div.toc{margin:0 0 10px;columns:2;column-gap:28px}p.toc-item{margin:3px 0;break-inside:avoid}div.toc a{font-weight:600}
figure.end{margin:18px auto;text-align:center}figure.end img{width:100%;height:auto;max-width:560px;display:block;margin:0 auto;border-radius:4px}
@media(max-width:700px){div.toc{columns:1}}
p{overflow-wrap:anywhere}
footer{max-width:1040px;margin:0 auto;padding:14px 16px 40px;font-size:.85rem;color:#333;border-top:1px solid #ddd}
@media(max-width:600px){header img.logo{height:40px}header h1{font-size:1rem}.banner img{aspect-ratio:1.6/1;max-height:260px;object-position:50% 12%}}
"""

def main():
    ensure_favicons("assets")
    if not os.path.isfile("assets/logo.png"):
        shutil.copy("/workspace/risk-watcher/site/assets/logo.png", "assets/logo.png")
    meta = json.load(open(META)) if os.path.exists(META) else {}
    issues = sorted([f[:-5] for f in os.listdir("issues") if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.html", f)], reverse=True)
    if not issues: raise SystemExit("no issues rendered yet")
    labels = {d: lab(d, meta.get(d, {}).get("test", False)) for d in issues}
    open("assets/style.css", "w").write(CSS + NAV_CSS)
    open(".nojekyll", "w").write("")
    tabs = "".join(f'<button role="tab" data-d="{d}" aria-selected="false">{E(labels[d])}</button>' for d in issues)
    # static copy of the latest issue so the page reads without JavaScript; JS swaps in the chosen issue
    latest = open(f"issues/{issues[0]}.html").read()
    latest_body = re.search(r'<main id="issue">(.*)</main>', latest, re.S).group(1).replace('src="img/', 'src="issues/img/')
    archive = "".join(f'<li><a href="issues/{d}.html?raw">{E(labels[d])}</a></li>' for d in issues)
    JS = """const tabs=[...document.querySelectorAll('#tabs button')],m=document.getElementById('content'),ds=tabs.map(t=>t.dataset.d);
async function show(d){if(!ds.includes(d))d=ds[0];tabs.forEach(t=>t.setAttribute('aria-selected',t.dataset.d==d));
m.innerHTML='<p>Loading…</p>';try{const r=await fetch('issues/'+d+'.html',{cache:'no-cache'});const doc=new DOMParser().parseFromString(await r.text(),'text/html');
const c=doc.querySelector('#issue');c.querySelectorAll('img').forEach(i=>{const u=i.getAttribute('src');if(!/^(https?:|\\/)/.test(u))i.setAttribute('src','issues/'+u)});m.innerHTML=c.innerHTML;document.title=TT+' — '+tabs.find(t=>t.dataset.d==d).textContent;window.scrollTo(0,0)}
catch(e){m.innerHTML='<p>Could not load '+d+'.</p>'}}
const TT=document.title;tabs.forEach(t=>t.onclick=()=>{location.hash=t.dataset.d});
function go(){const h=location.hash.slice(1);if(/^sec-\\d+$/.test(h)){const e=document.getElementById(h);if(e){e.scrollIntoView();return true}}return false}
addEventListener('hashchange',()=>{if(!go())show(location.hash.slice(1))});show(location.hash.slice(1)).then(()=>{go()});"""
    desc = "Weekly longevity digest from TechVestVentures: science and regulation, behavioral and physical tools, social and economic longevity, with every source linked. Not medical advice."
    open("index.html", "w").write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{T}</title><meta name="description" content="{E(desc)}"><meta property="og:title" content="{T}"><meta property="og:image" content="{URL}assets/masthead-duo3.webp"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{URL}">{favicon_links("assets/")}<link rel="stylesheet" href="assets/style.css"></head><body>{nav("lwdigest")}<div class="banner"><img src="assets/masthead-duo3.webp" width="1152" height="864" alt="An active older couple walking a sunlit forest trail, both wearing teal exoskeleton leg supports and glasses (illustration)"></div><div id="top"><header><img class="logo" src="assets/logo.png" alt="TVV logo"><div class="grow"><h1>{H1}</h1><div class="sub">Weekly, Fridays · Not medical advice</div></div></header><nav id="tabs" role="tablist" aria-label="Issue archive"><span class="al">Archive</span>{tabs}</nav></div><main id="content">{latest_body}</main><noscript><footer><strong>Archive</strong><ul>{archive}</ul></footer></noscript><footer><strong>{NOTICE}</strong> Research intelligence for editorial and advisory use only; discuss any drug, supplement, device or test with a clinician. Published by TechVestVentures. Every source is linked at the end of each issue.</footer><script>{JS}</script></body></html>''')
    print("index.html:", len(issues), "issue(s)")

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(a) == 2: render(a[0], a[1], "--test" in sys.argv)
    elif a: raise SystemExit(__doc__)
    main()
