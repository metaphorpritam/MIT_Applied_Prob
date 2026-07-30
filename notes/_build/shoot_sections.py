# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf"]
# ///
"""Per-section screenshot sweep for a big note (full-note print-to-PDF times out
on MathJax-heavy pages).

    uv run shoot_sections.py <slug> <shots_dir>     e.g. g1 scratchpad/shots_g1

For each notes/src/fragments/<slug>_s<N>.html:
  1. temp-build a single-section note via build_note.py machinery
  2. Edge print-to-PDF -> rasterize -> <shots_dir>/s<N>_p<K>.png
  3. one live viewport shot (widgets/controls/sidebar) -> <shots_dir>/s<N>_live.png
Temp files are removed afterwards.
"""
from __future__ import annotations
import json, os, re, shutil, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
NOTES = Path(__file__).resolve().parent.parent

EDGE_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
EDGE = next(p for p in EDGE_CANDIDATES if os.path.exists(p))

def run(args, timeout=300):
    subprocess.run(args, capture_output=True, timeout=timeout)

def main() -> int:
    slug, shots = sys.argv[1], Path(sys.argv[2])
    redo = "--redo" in sys.argv
    shots.mkdir(parents=True, exist_ok=True)
    frags = sorted((NOTES / "src" / "fragments").glob(f"{slug}_s*.html"),
                   key=lambda p: int(re.search(r"_s(\d+)", p.name).group(1)))
    if not frags:
        raise SystemExit(f"no fragments for {slug}")
    import fitz
    total_pages, failed = 0, []
    for frag in frags:
        n = int(re.search(r"_s(\d+)", frag.name).group(1))
        if not redo and list(shots.glob(f"s{n}_p*.png")):
            print(f"s{n}: already shot, skipping")
            continue
        for old in shots.glob(f"s{n}_*.png"): old.unlink()
        tmp = f"_tmp_{slug}_s{n}"
        try:
            (NOTES / "src" / f"{tmp}.body.html").write_text(frag.read_text(encoding="utf-8"), encoding="utf-8")
            (NOTES / "src" / f"{tmp}.meta.json").write_text(json.dumps({
                "title": f"[review] {slug} s{n}", "subtitle": "per-section review build",
                "prev": None, "next": None, "sources": "review temp"}), encoding="utf-8")
            r = subprocess.run([sys.executable, str(NOTES / "_build" / "build_note.py"), tmp],
                               capture_output=True, text=True, encoding="utf-8")
            if r.returncode != 0:
                print(f"s{n}: BUILD FAILED\n{r.stdout}\n{r.stderr}")
                failed.append(n)
                continue
            url = "file:///" + str(NOTES / f"{tmp}.html").replace("\\", "/")
            pdf = shots / f"_s{n}.pdf"
            run([EDGE, "--headless", "--disable-gpu", f"--print-to-pdf={pdf}",
                 "--no-pdf-header-footer", "--virtual-time-budget=45000", url], timeout=900)
            if pdf.exists():
                doc = fitz.open(pdf)
                for i in range(len(doc)):
                    doc[i].get_pixmap(dpi=110).save(shots / f"s{n}_p{i+1:02d}.png")
                total_pages += len(doc)
                doc.close(); pdf.unlink()
                print(f"s{n}: {len(list(shots.glob(f's{n}_p*.png')))} pages")
            else:
                print(f"s{n}: print-to-pdf produced nothing")
                failed.append(n)
            run([EDGE, "--headless", "--disable-gpu", "--window-size=1400,2200",
                 f"--screenshot={shots / f's{n}_live.png'}", "--virtual-time-budget=25000", url], timeout=600)
        except subprocess.TimeoutExpired:
            print(f"s{n}: TIMEOUT, continuing with next section")
            failed.append(n)
        finally:
            for p in [NOTES / f"{tmp}.html", NOTES / "src" / f"{tmp}.body.html",
                      NOTES / "src" / f"{tmp}.meta.json"]:
                if p.exists(): p.unlink()
    print(f"DONE {total_pages} new print pages -> {shots}; failed sections: {failed or 'none'}")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
