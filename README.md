# TVV Longevity Watcher Digest

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

## Sage portrait

The masthead has a hidden `.sage-slot`. To show the Longevity Watcher Sage: put the image at `assets/sage.png`, add `<img src="assets/sage.png" alt="Longevity Watcher Sage">` inside `#lw-sage` and add class `on`.
