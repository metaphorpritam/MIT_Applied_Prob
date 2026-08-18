# Question-bank fragment contract (slug `qb`)

Addendum to `STYLE_CONTRACT.md`. Applies to `notes/src/fragments/qb_s*.html`.
Everything in STYLE_CONTRACT still holds (MathJax-safe LaTeX, `&lt;`/`&gt;`,
`\mathbb{E}`, B&T citation form, figures via `{{IMG:key}}` with section-local
`Fig. N.k` numbering, one `<h2>` per fragment, computes for every number).

## Question numbering — GLOBAL, contiguous, do not overlap

| Fragment | Section | Questions | Source note |
|---|---|---|---|
| `qb_s0` | §0 How to use this bank | — (filter UI + guidance only) | — |
| `qb_s1` | §1 Probability fundamentals | **Q1–Q25** | G1 |
| `qb_s2` | §2 Discrete random variables | **Q26–Q47** | G2 |
| `qb_s3` | §3 Continuous random variables | **Q48–Q72** | G3 |
| `qb_s4` | §4 Iterated expectations & arrival processes | **Q73–Q94** | G4 |
| `qb_s5` | §5 Markov chains | **Q95–Q114** | G5 |
| `qb_s6` | §6 Limit theorems & Bayesian inference | **Q115–Q134** | G6 |
| `qb_s7` | §7 Classical statistical inference | **Q135–Q150** | G7 |
| `qb_s8` | §8 Exam classics: multinomial, random walks, waiting times | **Q151–Q170** | G1 §4, G2 §3–§4, G4 §2, G5 §4 |

Total = 170. Your range is exact — no more, no fewer.

## The question card — copy this shape exactly

```html
<div class="ex qcard" id="q17" data-diff="2" data-topic="bayes">
<p><b>Q17.</b> <span class="qmeta"><span class="stars">&#9733;&#9733;</span>
 &middot; Bayes' rule &middot; <span class="ref">G1 &sect;2.4</span></span></p>
<p>Question statement, self-contained, all symbols defined&hellip;</p>
<details class="sol"><summary>Solution</summary><div class="body">
<p><b>Setup.</b> &hellip;</p>
<p><b>Step 1.</b> &hellip; (every step shown, intermediate values substituted)</p>
<p><b>Answer.</b> $\;p = 0.3426$.</p>
<p class="srcref">Tool: G1 &sect;2.4 (Bayes' rule) &middot; B&amp;T &sect;1.4</p>
</div></details>
</div>
```

Rules:
- `id="qN"` — lowercase q + the global number. Unique across the whole bank.
- `data-diff` — `1` warm-up, `2` standard (exam-level), `3` challenging. Stars in
  `.stars` must match: 1→`&#9733;`, 2→`&#9733;&#9733;`, 3→`&#9733;&#9733;&#9733;`.
- `data-topic` — ONE lowercase slug from your section's topic list (see your brief).
  The §0 filter chips are built from these, so stay inside the list.
- The `.qmeta` line reads: stars · topic in words · the note section that teaches it.
- Every solution ends with a bold **Answer.** line and a `.srcref` "Tool:" line.

## Question quality bar

- **Fresh questions.** Do NOT copy recitation/quiz problems that the seven notes
  already solve verbatim. Test the same skills with new numbers, new stories, new
  angles. (You may reference a note's worked example as the "tool", never restate it
  as the question.)
- **Self-contained**: a reader who has the notes open can answer without hunting.
- **Mix of forms**: numeric answer, derivation/proof, true-or-false-with-reason,
  "which tool applies and why", spot-the-error, and interpretation questions.
- **Difficulty spread per section**: roughly 30% ★, 50% ★★, 20% ★★★.
- **Solutions teach**: full steps with substituted intermediate values, the reason
  for each step, and — where a trap exists — a closing line naming the wrong answer
  a careless reader would give and why it is wrong.
- **Every number recomputed** in `computes/qb_s<N>.py` (print + JSON dump, keyed);
  cite nothing you did not compute. Monte-Carlo cross-check anything subtle.
- Figures are optional and rare here — only when a question genuinely needs a
  diagram to be answerable. If used: `{{IMG:qb_s<N>_<name>}}` + `Fig. <N>.k` caption,
  section-local numbering, and view the PNG before shipping.

## Cross-linking

Each `.qmeta` cites the teaching section (e.g. `G3 &sect;4.2`). Use the real section
maps: G1 §1 models/axioms §2 conditioning/Bayes §3 independence §4 counting §5 synthesis ·
G2 §1 PMFs §2 expectation §3 variance/conditioning/geometric §4 joint PMFs §5 synthesis ·
G3 §1 PDFs/CDFs/named §2 joint/conditional §3 Bayes variants §4 derived/convolution/cov-corr §5 synthesis ·
G4 §1 iterated expectations §2 random sums/Bernoulli §3 Poisson I §4 Poisson II §5 synthesis ·
G5 §1 model/n-step §2 classification §3 steady state §4 absorption §5 synthesis ·
G6 §1 inequalities/WLLN §2 CLT §3 Bayesian/MAP §4 LMS/linear LMS §5 synthesis ·
G7 §1 estimators/CIs §2 ML §3 regression §4 hypothesis testing §5 synthesis.
