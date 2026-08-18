# Skill learnings — MIT 6.041 interactive-notes project

Distilled from building seven adversarially-reviewed interactive HTML study notes
from 25 lecture PDFs, 24 recitations + solutions, and a 539-page textbook —
using pageindex-plus + llm-wiki + multi-agent workflows. Written to be merged
into skill instructions. Every item below was learned by hitting the problem.

---

## 1. Source extraction — where text extraction silently lies

- **Slide-handout PDFs (2-up/6-up layouts) garble under text extraction twice
  over**: columns interleave AND broken font encoding corrupts digits/punctuation
  ("Sections olqkolr" was "Sections 1.1–1.2"). Neither failure raises an error.
  **Rule: for slide PDFs, rasterize every page (150 DPI) and vision-transcribe;
  use extracted text only as a word-hint, never trust its digits or math.**
- The sparse-text heuristic for rasterizing vector-figure pages **fails on dense
  slide pages** — plenty of text, so no raster, yet every diagram is vector and
  invisible to image extraction. Slide decks need whole-page rasters regardless.
- **Vision transcription needs a second adversarial pass.** First-pass agents
  *fabricate plausible details*: ours invented axis labels and tick values on an
  unlabeled stem plot, and described a 4-3-2-branching tree as "binary". A
  verify pass (fresh agents re-reading every raster against the transcript,
  instructed to assume errors exist) fixed 30 of 49 transcripts. Markers that
  make transcripts usable downstream: `[UNSOLVED EXAMPLE]`, `[DERIVATION GAP]`,
  `[SOLUTION GAP]`, `[FIGURE: redraw-grade description | raster/x.png]`,
  `[SOURCE TYPO?: ...]`, `[UNCERTAIN: ...]`.
- **Figure descriptions must be redraw-grade** (chart type, axes, labels, layout,
  what's NOT labeled) — "a tree diagram" is useless to the notes author later.
- **Sources contain real errors** — reversed inequalities in an official
  solution, sign errors, even a rounding slip in the textbook itself. Transcribe
  as-printed + flag; let the notes ADJUDICATE explicitly (show the correction and
  say why). Never silently "fix" toward or away from the source.
- **Filenames and numbering lie**: recitation N covered lecture N−1 in the
  second half of the course. Verify pairing by each document's topic line
  ("Covers: ..."), never by number. Some solution sheets contain no solutions at
  all ("See the textbook") — plan for reconstruction from the reference text.
- Figure-extraction caps (`--max-figures-per-doc`) hit silently on big books;
  log what was dropped and rasterize book pages on demand instead.

## 2. Windows/tooling landmines

- **Every Python script**: `sys.stdout.reconfigure(encoding="utf-8",
  errors="replace")` first line — cp1252 consoles crash on the first ligature.
- **Windows glob is case-insensitive**: `*_L*` matched `_libgen`. Filter with
  regex, not glob, when case matters.
- `python -c "...'🌙'..."` creates **lone surrogates**, not an emoji,
  and `open(...,'w').write()` then dies **mid-write, truncating the file to 0
  bytes**. Two rules: use `\U0001F319`-style escapes; treat any script that
  crashed during a write as having destroyed the target (our site hub was 0
  bytes for hours — caught only by an audit agent, not by the crash itself).
- PowerShell heredocs mangle backslashes — write helper code to `.py` files and
  `uv run` them (PEP-723 inline deps make this frictionless).
- mypy/IDE noise on `sys.stdout.reconfigure` and `import fitz` are stub false
  positives; don't "fix" working scripts to satisfy them.

## 3. Rendering & screenshot verification (the visual QA loop)

- **Headless print-to-PDF is the only full-coverage capture** of a long page
  (screenshot mode captures one viewport). But MathJax-heavy pages (~2000
  formulas, 3–6 MB) **time out even at 480 s**. Fix: build a temp single-section
  note per fragment and shoot those (13–20 print pages each) — also gives
  reviewers clean per-section evidence. Rasterize the PDF pages with PyMuPDF.
- Make the shooter **fault-tolerant and incremental**: per-section try/except
  (one timeout must not kill the run), skip sections that already have shots,
  `--redo` to force, always clean temp files in `finally`.
- **Browsers die**: Edge headless broke system-wide mid-project (print-to-pdf
  produced nothing, even for a trivial page). Keep a candidates list
  (Chrome first, then Edge) and *test with a tiny page* before blaming your own
  pipeline. Headless Chrome defaults to `prefers-color-scheme: dark` — verify
  themes via explicit `<html data-theme="...">` stamped copies, not the default.
- Headless `--window-size=390` clamps to ~497 CSS px on Windows; verify true
  mobile widths inside an iframe or via DOM-probe.
- **View every generated PNG.** Matplotlib failure modes that only eyes catch:
  labels on arrows, legends covering peaks, clipped boxes at axes edges,
  `FancyBboxPatch` pinching on non-equal aspect, radial seams in annuli,
  arrowheads hidden behind node circles. Authors should re-render until clean
  and report `viewed: true` per figure. Matplotlib mathtext: no `\tfrac`,
  `\dfrac`, `\operatorname`; `\sqrt n` crashes — write `\sqrt{n}`.

## 4. Multi-agent orchestration

- **Durable artifacts + compact structured returns.** Agents write their real
  output to disk (transcripts, fragments, computes, PNGs) and return small JSON
  (counts, file lists, concerns). The orchestrator never holds content.
- **The `concerns` field is gold.** Authors self-reported scope overlaps,
  guessed peer boundaries, and source anomalies — these became the `hint` input
  of the review workflow ("known suspects: verify first"). Several review
  criticals came straight from author concerns.
- **Parallel authors WILL guess each other's scope.** Give every author an
  authoritative peer-scope list ("s3 = variance+conditioning+geometric — do NOT
  guess") and forbid roadmap sections from inferring the split. Our s0 roadmap
  agents mislabeled sibling sections twice before this was mandated.
- **Convention drift across parallel authors** is guaranteed unless the prompt
  mandates: notation (`\mathbb{E}` vs slide `\mathbf{E}`), practice labels
  (`Practice N.k`), citation forms, figure-reference forms. Bake conventions +
  prior-note section maps into the COMMON prompt block; add a cross-fragment
  consistency agent as the final pass regardless (it still found 84 edits in
  one note).
- **Session token limits kill fleets mid-flight** (every few hours). Design for
  it: workflows resumable via `resumeFromRunId` (finished agents replay from
  cache free); agents that write-then-report lose only the report, not the work
  (an 84 KB fragment survived its author's death); log a handoff queue with
  exact run IDs after every phase so any fresh session can resume.
- **Review = independent lenses, then per-section fixers.** Two math lenses
  (split sections), one render lens (reads all shots), one pedagogy lens
  (checks every source problem is solved SOMEWHERE, boxes/practice present).
  Findings → per-section fixer agents that verify before fixing and may skip
  with reasons. Fixers only own their fragment — cross-fragment issues need the
  separate consistency pass.
- Reviews found ~330 real issues, including: compute off-by-one (`dice[6]` vs
  `dice[5]`), stale hand-typed numbers contradicting the compute JSON, a
  rejection region violating its own α, a JS LCG whose `sd*1103515245` exceeded
  2^53 and silently lost low bits (fix: `Math.imul(...) >>> 0`), and a false
  claim about scipy/numpy conventions **falsified by actually running both**.
  Instruct reviewers to *execute* claims, not reason about them.
- **Never hand-type a derived number.** Every numeric in prose comes from a
  compute script that prints + JSON-dumps keyed values; prose cites the key;
  reviewers grep keys and re-run scripts. "Provenance defect" (right number, no
  key) is a findable, fixable class of error.
- Workflow `args` may arrive as a JSON **string**: destructure via
  `const A = typeof args === 'string' ? JSON.parse(args) : args`.
- Don't nest `&` background jobs inside an already-backgrounded compound
  command — the outer completes while the inner detaches unmonitored.

## 5. Build-system patterns for fragment-assembled HTML

- **Fragments per section** (`slug_sN.html`), assembled by a script that
  validates: exactly one `h2` per fragment, per-tag open/close balance
  (`<p>`, `<div>`, `<details>`, ...), `{{IMG:key}}` ↔ PNG existence, widget
  container id uniqueness, **section-local figure numbering** (`Fig. N.k`
  first-appearances consecutive from 1).
- That validator forces a citation convention: `Fig. N.k` only for this
  section's figures in order; **forward references and cross-section references
  spell out `Figure N.k`; book figures are cited `its Figure x.y`** — otherwise
  the validator false-positives on citations (it did, three times).
- Common fragment bug: prose between display-math blocks with orphaned `</p>`
  or unclosed `<p>` — tag-balance checks catch it; a char-position bisect
  script locates it fast.
- **Inline shared JS in `<head>`, not end-of-body**: widget `<script>` blocks in
  the body execute during parse and need the framework already defined. (Our
  first smoke test rendered an empty widget for exactly this reason.)
- MathJax **SVG renderer** (not CHTML): renders identically in print/PDF capture
  and doesn't depend on font loading.
- **Two build targets from one source**: default = base64-embedded single-file
  HTML (offline/mobile/zip: opens anywhere, no folders); `--site` = external
  `img/` references (~70–90 % smaller pages, cacheable) into `docs/` for GitHub
  Pages. One release script produces both + the zip, and copies the zip into
  `docs/` so the site's download link resolves.
- Public-repo hygiene: exclude non-redistributable PDFs (textbook), proprietary
  skill bundles, and heavy derived artifacts via `.gitignore`; ship an OCW
  attribution + CC BY-NC-SA notice on the page footer and README.

## 6. Knowledge/memory layer (what made multi-session survival work)

- pageindex corpus+index over ALL sources up front; later **re-ingest the
  generated notes and transcripts into the same index** so the KB can retrieve
  and cite its own outputs.
- llm-wiki: log EVERY session (including 2-line ones), decisions when made, a
  handoff queue with workflow run-IDs before every context death. Recovery
  ritual (index → log tail → audit counts) genuinely restores state; the audit
  also catches real damage (it found our 0-byte hub file).
- `sources:` in wiki frontmatter must list FILES — directories crash the
  hash-based audit.
- Structured inventories as JSON files (`_summary.json`, `_verification.json`,
  per-note `_gN_review.json`) — these are what later phases and totals are
  computed from; losing one (our G6) makes cross-note aggregation branch.

---

## 7. RECIPE — HTML notes with scrollable TOC sidebar + dark mode

The complete pattern, extracted from the working implementation.

### 7.1 Page skeleton

```html
<body>
  <button id="sbtoggle" aria-label="toggle contents">&#9776;</button>  <!-- mobile -->
  <nav id="sidebar">
    <h1>{note title}</h1>                          <!-- sticky mini-header -->
    <div class="crumb"><a href="index.html">&#8962; Hub</a> · course</div>
    <!-- theme toggle inserted HERE by JS — top, always visible -->
    <input id="tocfilter" type="text" placeholder="filter topics…">
    <ul id="toc"></ul>                             <!-- built at runtime -->
    <div class="navlinks">{prev/next/index/feedback links}</div>
  </nav>
  <main id="main">
    <h1 class="title">…</h1>
    {content: h2/h3 sections}
  </main>
</body>
```

### 7.2 Sidebar CSS (the load-bearing rules)

```css
:root { --sidebar-w: 300px; /* …all colors as variables… */ }
#sidebar {
  position: fixed; inset: 0 auto 0 0; width: var(--sidebar-w);
  overflow-y: auto; overflow-x: hidden;            /* THE scroll container */
  scrollbar-width: thin; overscroll-behavior: contain;
}
#sidebar h1 { position: sticky; top: 0; z-index: 3; background: var(--sidebar-bg); }
#main { margin-left: var(--sidebar-w); max-width: 980px; }
h2, h3 { scroll-margin-top: 12px; }                /* anchor offset */
@media (max-width: 900px) {                        /* drawer mode */
  #sidebar { transform: translateX(-100%); transition: transform .22s; }
  #sidebar.open { transform: none; }
  #main { margin-left: 0; }
  #sbtoggle { display: block; position: fixed; top: 10px; left: 10px; }
}
@media print { #sidebar, #sbtoggle { display: none; } #main { margin: 0; } }
```

### 7.3 TOC builder + scrollspy (runtime JS, DOMContentLoaded)

1. Query `#main h2, #main h3`; slugify ids for any heading lacking one.
2. Build nested `<li class="lvl2|lvl3">` with anchors; h2 rows get a collapse
   caret toggling `li.collapsed` (CSS hides the nested `ul`).
3. **Scrollspy**: on scroll (rAF-throttled), active = last heading whose
   `getBoundingClientRect().top <= 90`; toggle `.active` on its link and
   `scrollIntoView({block:'center'})` it **within the sidebar** so the active
   item stays visible in a long TOC.
4. Filter box: hide non-matching `li`; when a lvl3 matches, force its parent
   lvl2 visible.
5. Mobile: `#sbtoggle` click toggles `#sidebar.classList('open')`.

### 7.4 Dark mode — the architecture that wins both ways

**Everything is a CSS variable.** No hardcoded colors in component rules — box
tints, table borders, widget chrome, scrollbar thumb, all of it. Then dark mode
is ONE block of variable overrides declared in **two scopes**:

```css
:root[data-theme="dark"] { --ink:#e8e6e1; --paper:#1e1e1c; /* …every var… */ }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { /* identical var block */ }
}
```

Why two scopes: the media query follows the OS; the `data-theme` attribute
(set by the toggle) must override the OS **in both directions** — the
`:not([data-theme="light"])` guard is what lets an explicit light choice beat
OS-dark. Keep the attribute scope *after* the media block in source order.

**Toggle JS** (inline, or in shared JS):

```js
// apply saved theme ASAP — before DOMContentLoaded — to avoid a flash
try { const s = localStorage.getItem('themeKey');
      if (s) document.documentElement.dataset.theme = s; } catch(e){}

const cur = () => document.documentElement.dataset.theme ||
  (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
btn.onclick = () => {
  const next = cur() === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  try { localStorage.setItem('themeKey', next); } catch(e){}
  relabel();   // "🌙 dark mode" ⇄ "☀ light mode"
};
```

Hard-earned specifics:
- **Put the toggle at the sidebar TOP** (right after the breadcrumb). Appended
  below a 40-entry TOC it exists but nobody ever finds it (real user report).
- **Figures and widget canvases stay white "plates"** in dark mode
  (`.fig{background:#fff}` and the canvas wrapper likewise): matplotlib PNGs
  and canvas charts are baked light; a white card on dark paper is the standard
  textbook-dark treatment and keeps every diagram legible. Restyle only chrome:
  page, sidebar, text, boxes, tables, `details`, code, widget frames.
- Dark values aren't inverted light values: use a **validated dark palette**
  (dark surface ≈ #1a1a19/#1e1e1c, ink #e8e6e1 not #fff, categorical series
  re-stepped for the dark surface, accents lightened for contrast, e.g. a navy
  accent must become a light blue to survive on dark).
- localStorage carries the choice **across pages** of the site automatically.
- If a build script *generates* the dark CSS, mind §2's surrogate/truncation
  trap — and verify the output file is non-empty afterwards.

### 7.5 Verification checklist for each built note

- Screenshot light + dark (stamped `data-theme` copies) + mobile width.
- MathJax rendered (no raw `$…$` in shots); no `{{IMG:…}}` leftovers;
  figure numbering consecutive per section; widget canvases non-blank;
  TOC present with active highlight; toggle visible without scrolling.
- Full-page capture via per-section print-to-PDF if the page is math-heavy.
