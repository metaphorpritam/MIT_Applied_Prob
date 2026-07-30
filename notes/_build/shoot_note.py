# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf"]
# ///
"""Capture review screenshots of a built note.

    uv run shoot_note.py <noteFile.html> <shots_dir>

1. Edge headless print-to-PDF (full document; print CSS hides sidebar/controls),
   then rasterize every PDF page -> <shots_dir>/pNN.png  (full coverage).
2. Edge headless viewport screenshots at the top and at each h2 anchor
   -> <shots_dir>/live_<anchor>.png  (sidebar, widget controls, live layout).
"""
from __future__ import annotations
import os, re, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
NOTES = Path(__file__).resolve().parent.parent

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
EDGE = next(p for p in EDGE_CANDIDATES if os.path.exists(p))

def run(args):
    subprocess.run(args, capture_output=True, timeout=480)

def main() -> int:
    note = NOTES / sys.argv[1]
    shots = Path(sys.argv[2]); shots.mkdir(parents=True, exist_ok=True)
    for old in shots.glob("*.png"): old.unlink()
    url = "file:///" + str(note).replace("\\", "/")

    # full-document PDF -> page PNGs
    pdf = shots / "_doc.pdf"
    run([EDGE, "--headless", "--disable-gpu", f"--print-to-pdf={pdf}",
         "--no-pdf-header-footer", "--virtual-time-budget=20000", url])
    import fitz
    doc = fitz.open(pdf)
    for i in range(len(doc)):
        doc[i].get_pixmap(dpi=110).save(shots / f"p{i+1:02d}.png")
    n = len(doc); doc.close()

    # live viewport shots: top + each h2 anchor
    html = note.read_text(encoding="utf-8")
    anchors = ["", *re.findall(r'<h2 id="([\w\-]+)"', html)]
    for a in anchors:
        out = shots / f"live_{a or 'top'}.png"
        run([EDGE, "--headless", "--disable-gpu", "--window-size=1400,1900",
             f"--screenshot={out}", "--virtual-time-budget=15000", url + (f"#{a}" if a else "")])
    print(f"OK {n} print pages + {len(anchors)} live shots -> {shots}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
