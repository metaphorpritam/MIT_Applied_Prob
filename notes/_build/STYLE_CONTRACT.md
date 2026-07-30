# Section-fragment style contract (all note groups)

Every section author writes ONE fragment file `notes/src/fragments/<slug>_s<N>.html`
(e.g. `g1_s2.html`). Fragments are concatenated in filename order by
`assemble_body.py` — they must be self-contained and follow this contract EXACTLY.

## Structure

```html
<h2 id="<slug>-s<N>">§<N> &nbsp; <Section Title></h2>
<p class="srcref">Sources: L02 slides 1–8 (raster p1–p2) · rec02 problems 1–3 · Bertsekas–Tsitsiklis §1.3–1.4</p>
<p>…motivating intro prose…</p>
<h3><N>.1 <Sub-topic></h3>
…
```

- `h2` once per fragment, `h3` sub-sections numbered `<N>.1, <N>.2, …` (these feed the sidebar TOC).
- HTML entities for literal `<`, `>`, `&` in prose AND inside math: write `&lt;`.

## Math

- Inline `$...$`, display `$$...$$`. MathJax v3, `\mathbf{P}` for probability, `\mathbb{E}` for
  expectation, `\operatorname{var}`, `p_X(x)`, `f_{X|Y}(x|y)` — follow the course notation.
- EVERY derivation: no skipped steps. Substitutions shown with intermediate numeric values.
  After each nontrivial step, one clause of justification (axiom/rule used, in words).
- Every variable introduced gets one sentence saying what it is.

## Boxes (use deliberately)

- `<div class="defn"><b>Definition.</b> …</div>` — definitions
- `<div class="thm"><b>Theorem.</b>/<b>Property.</b> …</div>` — results
- `<div class="ex"><b>Example N.k (source).</b> …</div>` — worked examples (incl. solved slide examples + recitation problems)
- `<div class="warn"><b>Gotcha.</b> …</div>` — pitfalls, common errors
- `<div class="note"><b>Intuition.</b>/<b>Interpretation.</b> …</div>` — meaning of results
- `<div class="recipe"><b>Recipe.</b> …</div>` — step-by-step procedures / decision guides
- `<div class="summary">` — end-of-section cheatsheet (one per fragment, at the end)

## Worked problems & practice

- Every `[UNSOLVED EXAMPLE]` from the transcripts for your sources: solve COMPLETELY in an
  `.ex` box (statement first, then step-by-step solution).
- Recitation problems: statement in `.ex` box, full expanded solution (official solution +
  every `[SOLUTION GAP]` filled) inside `<details class="sol"><summary>Solution</summary><div class="body">…</div></details>`.
- End each `h3` topic with 1–3 practice questions in `.ex` boxes with `<details class="sol">` answers.

## Figures

- Placeholder: `<img class="fig" src="data:image/png;base64,{{IMG:<slug>_s<N>_<name>}}" alt="…" style="max-width:<W>px">`
  followed by `<div class="figcap">Fig. <N>.<k> — caption (cite source: L02 slide 5).</div>`
- Figure numbering is SECTION-LOCAL: `Fig. <N>.1, <N>.2, …` in order of appearance.
- The PNG must exist at `notes/img/<slug>_s<N>_<name>.png` (author generates it with
  matplotlib, style from `notes/_build/mpl_style.py`, and MUST view the PNG to check it).
- Regenerate charts cleanly when data is known; embed a raster crop only for content that
  cannot be redrawn (photos, scans).
- Flowcharts/diagrams (trees, decision guides, Venn, Markov chains): draw with matplotlib
  patches/annotations (clean boxes+arrows, NO overlapping text) — check the PNG.

## Interactive widgets

- Container+script pair, ids unique across the whole note: `w-<slug>s<N>-<name>`:
  ```html
  <div id="w-g1s2-bayes"></div>
  <script>
  Widget.create({ el: '#w-g1s2-bayes', title: '…', note: '…', height: 300,
    controls: [ {type:'range', id:'p', label:'prior P(A)', min:0.001, max:0.5, step:0.001, value:0.05} ],
    draw(s, canvas, out) { const P = new Plot(canvas, {…}); P.frame(); … } });
  </script>
  ```
- `Plot` API: frame(), line(xs,ys,{label,color,width,dash}), func(f,{label}), stem(xs,ys,{label})
  for PMFs, bars(), step(xs,ys) for CDFs, area(), points(), vline(x)/hline(y), text(s,x,y),
  legend(). Colors auto-cycle the palette; pass color:0..7 to pin.
- Every widget: `out.textContent = …` readout of the key computed values.

## Numbers

- NEVER hand-compute a numeric value. Write `computes/<slug>_s<N>.py` (uv-run, UTF-8 stdout,
  PEP-723 header, stdlib+numpy/scipy ok), print + json.dump results to `computes/<slug>_s<N>.json`,
  run it, and copy the printed values into the HTML. Cross-check against the source; if a
  source value disagrees, investigate — flag unresolved conflicts as `[SOURCE CONFLICT: …]`.

## Citations

- Every claim/derivation cites its source inline in the nearest `srcref`/figcap/ex-box header:
  lecture slide (e.g. "L02 slide 5"), recitation problem ("rec02 P1"), or book section ("§1.3").

## Tone

Textbook prose, second person sparingly. Interpret results ("what this means"), don't just
derive them. British/American spelling: American. No filler.
