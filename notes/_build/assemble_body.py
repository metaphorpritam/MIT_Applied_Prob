# /// script
# requires-python = ">=3.10"
# ///
"""Concatenate section fragments into a note body.

    uv run assemble_body.py <slug>     # e.g. g1 -> notes/src/01_probability_basics.body.html

Reads notes/src/fragments/<slug>_s*.html in filename order, checks the contract
(one h2 per fragment, section-local figure numbering Fig. N.k consecutive,
placeholder/img-file existence, widget id uniqueness across the note), then
writes the combined body to the path given in notes/src/<slug>.target.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
NOTES = Path(__file__).resolve().parent.parent

def main() -> int:
    slug = sys.argv[1]
    frags = sorted((NOTES / "src" / "fragments").glob(f"{slug}_s*.html"),
                   key=lambda p: int(re.search(r"_s(\d+)", p.name).group(1)))
    if not frags:
        raise SystemExit(f"no fragments notes/src/fragments/{slug}_s*.html")
    target = (NOTES / "src" / f"{slug}.target").read_text(encoding="utf-8").strip()

    errs, bodies, widget_ids = [], [], {}
    imgs = {p.stem for p in (NOTES / "img").glob("*.png")}
    for p in frags:
        t = p.read_text(encoding="utf-8")
        n = int(re.search(r"_s(\d+)", p.name).group(1))
        h2s = re.findall(r"<h2\b", t)
        if len(h2s) != 1:
            errs.append(f"{p.name}: {len(h2s)} h2 tags (want 1)")
        fignums = re.findall(r"Fig\.\s*(\d+)\.(\d+)", t)
        secs = {int(a) for a, _ in fignums}
        if secs - {n}:
            errs.append(f"{p.name}: figure numbers reference sections {secs - {n}} (fragment is s{n})")
        ks, seen = [int(b) for a, b in fignums if int(a) == n], []
        for k in ks:
            if k not in seen:
                seen.append(k)
        if seen != list(range(1, len(seen) + 1)):
            errs.append(f"{p.name}: Fig. {n}.k first appearances not consecutive-from-1: {seen}")
        for key in re.findall(r"\{\{IMG:([\w\-]+)\}\}", t):
            if key not in imgs:
                errs.append(f"{p.name}: {{{{IMG:{key}}}}} missing notes/img/{key}.png")
        for wid in re.findall(r"id=\"(w-[\w-]+)\"", t):
            if wid in widget_ids:
                errs.append(f"{p.name}: widget id {wid} already used in {widget_ids[wid]}")
            widget_ids[wid] = p.name
        bodies.append(t.strip())

    if errs:
        print("ASSEMBLY ERRORS:")
        for e in errs:
            print("  -", e)
        return 1
    out = NOTES / "src" / target
    out.write_text("\n\n".join(bodies) + "\n", encoding="utf-8")
    print(f"OK assembled {len(frags)} fragments -> {out} ({out.stat().st_size/1024:.0f} KB, {len(widget_ids)} widgets)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
