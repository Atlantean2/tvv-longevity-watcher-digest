# LONGEVITY WATCH (TVV Longevity Watch)

Public site: https://atlantean2.github.io/tvv-longevity-watcher-digest/

Weekly longevity digest from TechVestVentures (Fridays). Every page is labeled **Not medical advice**.
Every source in an issue is a clickable https link; each issue ends with its Sources list.

## Weekly publish

From this folder (`/workspace/longevity-digests/site/`):

```bash
python3 build.py YYYY-MM-DD "/workspace/longevity-digests/Longevity Digest YYYY-MM-DD v1.0.docx"
git add index.html .nojekyll assets issues issues.json
git -c user.name=Atlantean2 -c user.email=Atlantean2@users.noreply.github.com commit -m "Longevity Digest YYYY-MM-DD"
git push origin main
```

Add `--test` to the build command to label an issue "test issue". `python3 build.py` alone rebuilds index and CSS from `issues/`.
`build.py` reads the shared sidebar from `/workspace/risk-watcher/tvv_nav.py`.

## Masthead art

The masthead banner is the "Duo 3" painting (active older couple on a forest trail in teal exoskeletons), saved as `assets/masthead-duo3.webp` (1152x864, webp) and shown as a wide cropped strip (`.banner img`, object-fit cover, focus on the two people). `build.py` writes it into every rebuild; the page title is `TVV Longevity Watch` and the masthead title is `LONGEVITY WATCH`.

The provisional single-man Sage portrait (`assets/sage.png`, `assets/sage-full.jpg`) is kept in the repo but not shown; the `.sage-slot` CSS is hidden.
