# /// script
# requires-python = ">=3.10"
# ///
"""Assemble a final self-contained note HTML from a body fragment.

    uv run build_note.py <slug>          e.g.  uv run build_note.py 01_probability_basics

Reads:
  notes/src/<slug>.body.html   — the authored content (sections only, no <html> shell)
  notes/src/<slug>.meta.json   — {title, subtitle, prev:[file,label]|null, next:[...]|null, sources}
  notes/_shared/{notes.css, plot.js, widgets.js, toc.js}
  notes/img/*.png              — for {{IMG:key}} placeholders (key = filename stem)
Writes:
  notes/<slug>.html            — single-file, self-contained (MathJax CDN is the only external dep)

Validates: no unresolved {{IMG:}}, figure numbers consecutive, balanced <div>/<section>,
MathJax present, every referenced widget container exists exactly once.
"""
from __future__ import annotations
import base64, json, re, sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
NOTES = Path(__file__).resolve().parent.parent

MATHJAX = """
<script>
window.MathJax = {
  tex: { inlineMath: [['$','$'], ['\\\\(','\\\\)']],
         displayMath: [['$$','$$'], ['\\\\[','\\\\]']],
         processEscapes: true, tags: 'none' },
  svg: { fontCache: 'global' },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" id="mathjax"></script>
"""

def b64(p: Path) -> str:
    return base64.b64encode(p.read_bytes()).decode()

def main() -> int:
    slug = sys.argv[1]
    site_mode = "--site" in sys.argv   # external images + output to ../docs/ (GitHub Pages)
    body = (NOTES / "src" / f"{slug}.body.html").read_text(encoding="utf-8")
    meta = json.loads((NOTES / "src" / f"{slug}.meta.json").read_text(encoding="utf-8"))
    css = (NOTES / "_shared" / "notes.css").read_text(encoding="utf-8")
    js = "\n".join((NOTES / "_shared" / n).read_text(encoding="utf-8")
                   for n in ["plot.js", "widgets.js", "toc.js"])

    # ---- image substitution (embedded base64 by default; external files in --site mode)
    imgs = {p.stem: p for p in (NOTES / "img").glob("*.png")}
    used = set()
    def sub(m):
        key = m.group(1)
        if key not in imgs:
            raise SystemExit(f"ERROR: {{{{IMG:{key}}}}} has no notes/img/{key}.png")
        used.add(key)
        return b64(imgs[key])
    if site_mode:
        # rewrite the whole data-URI attribute value to a relative path
        body = re.sub(r"data:image/png;base64,\{\{IMG:([A-Za-z0-9_\-]+)\}\}",
                      lambda m: (used.add(m.group(1)), f"img/{m.group(1)}.png")[1], body)
        missing = [k for k in used if k not in imgs]
        if missing:
            raise SystemExit(f"ERROR: missing notes/img PNGs: {missing}")
    else:
        body = re.sub(r"\{\{IMG:([A-Za-z0-9_\-]+)\}\}", sub, body)
    leftover = re.findall(r"\{\{IMG:[^}]*\}\}", body)
    if leftover:
        raise SystemExit(f"ERROR: unresolved placeholders: {leftover}")

    # ---- validations
    errs = []
    # section-local figure numbering: Fig. N.k consecutive-from-1 within each section N
    per_sec: dict[int, list[int]] = {}
    for a, b in re.findall(r"Fig\.\s*(\d+)\.(\d+)", body):
        per_sec.setdefault(int(a), [])
        if int(b) not in per_sec[int(a)]:
            per_sec[int(a)].append(int(b))
    for sec, ks in sorted(per_sec.items()):
        if ks != list(range(1, len(ks) + 1)):
            errs.append(f"Fig. {sec}.k first appearances not consecutive-from-1: {ks}")
    for tag in ["div", "section", "details", "table", "p"]:
        op = len(re.findall(rf"<{tag}\b", body)); cl = len(re.findall(rf"</{tag}>", body))
        if op != cl:
            errs.append(f"<{tag}> open/close mismatch: {op} vs {cl}")
    for wid in re.findall(r"el:\s*['\"]#([\w-]+)['\"]", body):
        c = len(re.findall(rf"id=\"{wid}\"", body))
        if c != 1:
            errs.append(f"widget container #{wid} appears {c} times (want 1)")
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs:
            print("  -", e)
        return 1

    nav = ""
    if meta.get("prev"):
        nav += f'<a href="{meta["prev"][0]}">&larr; {meta["prev"][1]}</a>\n'
    if meta.get("next"):
        nav += f'<a href="{meta["next"][0]}">{meta["next"][1]} &rarr;</a>\n'
    nav += '<a href="index.html">Course index</a>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta['title']}</title>
{MATHJAX}
<style>
{css}
</style>
<script>
{js}
</script>
</head>
<body>
<button id="sbtoggle" aria-label="toggle contents">&#9776;</button>
<nav id="sidebar">
<h1>{meta['title']}</h1>
<div class="crumb"><a href="index.html">&#8962; Course hub</a> &middot; MIT 6.041/6.431 F10</div>
<input id="tocfilter" type="text" placeholder="filter topics&hellip;">
<ul id="toc"></ul>
<div class="navlinks">
{nav}
</div>
</nav>
<main id="main">
<h1 class="title">{meta['title']}</h1>
<div class="subtitle">{meta['subtitle']}</div>
{body}
<hr>
<div class="small" style="text-align:center;">Compiled from {meta['sources']} on {date.today().isoformat()}. Every numerical value recomputed independently in Python; see computes/.</div>
</main>
</body>
</html>
"""
    if site_mode:
        outdir = NOTES.parent / "docs"
        (outdir / "img").mkdir(parents=True, exist_ok=True)
        import shutil
        for key in used:
            shutil.copy2(imgs[key], outdir / "img" / f"{key}.png")
        out = outdir / f"{slug}.html"
    else:
        out = NOTES / f"{slug}.html"
    out.write_text(html, encoding="utf-8")
    nfigs = sum(len(v) for v in per_sec.values())
    print(f"OK wrote {out}  ({out.stat().st_size/1024:.0f} KB, {len(used)} embedded images, "
          f"{nfigs} figures, widgets: {len(re.findall(r'Widget.create', body))})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
