---
title: Build Pipeline
type: module
status: active
aliases: [pipeline, infrastructure, tooling]
tags: [infra]
sources:
  - ../transcripts/_manifest.json
code:
  - ../notes/_build/build_note.py
  - ../notes/_shared/plot.js
  - ../notes/_shared/widgets.js
  - ../notes/_shared/toc.js
links:
  relates: [MIT 6.041 Course, Notes Plan]
---

# Build Pipeline

All infrastructure for turning the raw course PDFs into interactive HTML notes.

## Layers (all inside `d:\Python-UV\MIT_Applied_Prob`)

| Layer | Path | How built | Rebuild command |
|---|---|---|---|
| Raw sources (immutable) | `lecture_notes/`, `recitations/` | — | — |
| Corpus (text + figure cards) | `corpus/` | pageindex-plus ingest | `uv run _tools/pageindex-plus/scripts/ingest_notes.py <src> corpus` |
| PageIndex (retrieval) | `index/` | 944 pages, 880 nodes | `uv run _tools/pageindex-plus/scripts/build_pageindex.py corpus index --name "MIT 6.041 ..."` |
| Page rasters (vision ground truth) | `raster/` | 215 PNGs @150 DPI, `L01_p01.png` / `rec01_p1.png` / `rec01_sol_p1.png` | scratchpad `rasterize_all.py` (idempotent) |
| Transcripts (faithful md) | `transcripts/` | 49 vision agents (session 1) | re-run transcribe workflow |
| Compute scripts | `computes/` | one per numerical example cluster | `uv run computes/<name>.py` |
| Notes bodies | `notes/src/<slug>.body.html` + `.meta.json` | authored per group | — |
| Final notes | `notes/<slug>.html` | assembler | `uv run notes/_build/build_note.py <slug>` |

## Assembler contract (`build_note.py`)

- Inlines `_shared/{notes.css,plot.js,widgets.js,toc.js}` into `<head>` (scripts MUST
  be in head — body widget scripts call `Widget.create` during parse).
- `{{IMG:key}}` → base64 of `notes/img/key.png`; build fails on unresolved keys.
- Validates: consecutive figure numbers, balanced tags, widget container uniqueness.
- Sidebar TOC is auto-built at runtime by `toc.js` from `#main h2/h3` (scrollspy + filter + collapse).
- Only external dependency: MathJax CDN.

## Visual verification loop

Headless Edge screenshot:
`msedge --headless --disable-gpu --window-size=1400,1100 --screenshot=<out.png> --virtual-time-budget=8000 file:///D:/...html`
then Read the PNG. Used for template smoke test (widget bug caught this way); required for every figure and final note page.

## Book policy (user decision, session 1)

The Bertsekas–Tsitsiklis book stays **reference-only**: indexed in the PageIndex for
section lookup when lectures/recitations cite it ("Readings: Section 4.2"), never
transcribed wholesale. Its figure extraction hit the 40-figure ingest cap — remaining
book figures are rasterized on demand from the PDF page.
