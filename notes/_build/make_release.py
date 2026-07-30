# /// script
# requires-python = ">=3.10"
# ///
"""Build both distribution formats of the 6.041 notes.

    uv run make_release.py

1. OFFLINE ZIP  -> dist/mit6041_interactive_notes_offline.zip
   Self-contained single-file notes (images base64-embedded). Each HTML opens
   standalone in any browser, including mobile — no folders required.
2. WEBSITE      -> docs/   (GitHub Pages root)
   External images (docs/img/), light pages, .nojekyll, hub included.
"""
from __future__ import annotations
import shutil, subprocess, sys, zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
NOTES = Path(__file__).resolve().parent.parent
ROOT = NOTES.parent
SLUGS = ["01_probability_basics", "02_discrete_rvs", "03_continuous_rvs",
         "04_expectation_processes", "05_markov_chains", "06_limits_bayesian",
         "07_classical_inference"]

def build(slug: str, site: bool) -> None:
    args = [sys.executable, str(NOTES / "_build" / "build_note.py"), slug]
    if site:
        args.append("--site")
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit(f"BUILD FAILED {slug} (site={site}):\n{r.stdout}\n{r.stderr}")
    print(r.stdout.strip().splitlines()[-1])

def main() -> int:
    # ---- 1. offline (embedded) build + zip
    for s in SLUGS:
        build(s, site=False)
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    zpath = dist / "mit6041_interactive_notes_offline.zip"
    readme = (
        "MIT 6.041 Probabilistic Systems Analysis - Interactive Study Notes (offline)\n"
        "============================================================================\n\n"
        "Each HTML file is fully self-contained (all figures embedded).\n"
        "Open index.html - or any note directly - in any browser, desktop or mobile.\n"
        "Internet is only needed once per session for math rendering (MathJax CDN).\n\n"
        "Compiled from MIT OpenCourseWare 6.041/6.431 Fall 2010 (John Tsitsiklis) and\n"
        "Bertsekas & Tsitsiklis, 'Introduction to Probability', 2nd ed.\n"
        "License: CC BY-NC-SA 4.0 (per MIT OCW terms). Not an official MIT product.\n"
    )
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        z.writestr("mit6041_notes/README.txt", readme)
        z.write(NOTES / "index.html", "mit6041_notes/index.html")
        for s in SLUGS:
            z.write(NOTES / f"{s}.html", f"mit6041_notes/{s}.html")
    print(f"OK zip -> {zpath} ({zpath.stat().st_size/1e6:.1f} MB)")

    # ---- 2. website (external-image) build -> docs/
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    for s in SLUGS:
        build(s, site=True)
    shutil.copy2(NOTES / "index.html", docs / "index.html")
    shutil.copy2(zpath, docs / zpath.name)   # so the site's download link works
    (docs / ".nojekyll").write_text("", encoding="utf-8")
    n_img = len(list((docs / "img").glob("*.png")))
    total = sum(f.stat().st_size for f in docs.rglob("*") if f.is_file()) / 1e6
    print(f"OK site -> {docs}  ({len(SLUGS)} notes + hub, {n_img} images, {total:.1f} MB total)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
