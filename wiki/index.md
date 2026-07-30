---
title: MIT 6.041 Applied Probability KB Index
type: concept
status: active
tags: [index]
---

# MIT 6.041 Applied Probability KB — wiki index

The catalog of the wiki, and the FIRST thing read both by a fresh session and
at query time. Convention (from Karpathy's llm-wiki pattern): **every page
gets one line here** — a wikilink plus a one-line summary — grouped
under a category heading. Update it on every ingest; the audit flags pages
missing from this file.

## Sources & plans

- [[MIT 6.041 Course]] — the course, its materials, verified lecture topics, extraction hazards
- [[Notes Plan]] — the 7 topic-group HTML notes: statuses, quality contract, per-note pipeline (THE progress tracker)

## Modules

- [[Build Pipeline]] — every layer (corpus→index→raster→transcripts→computes→notes), rebuild commands, assembler contract, visual verification loop

## Notes (complete)

One concept page per built note — section map, widgets, flagship worked problems,
review stats, and the per-note oddities worth remembering.

- [[Note G1 Probability Fundamentals]] — L01–L04: axioms, conditioning, Bayes, independence, counting; sets the conventions the other six inherit
- [[Note G2 Discrete Random Variables]] — L05–L07: PMFs, expectation, variance, joint PMFs; the bus and St. Petersburg paradoxes
- [[Note G3 Continuous Random Variables]] — L08–L11: densities, CDFs, the four faces of Bayes, derived distributions and convolution (largest note, 38 figures)
- [[Note G4 Iterated Expectations and Arrival Processes]] — L12–L15: iterated expectations, random sums, Bernoulli & Poisson processes; where the recitation offset starts
- [[Note G5 Markov Chains]] — L16–L18: transition probabilities, classification, steady state, absorption; folds rec16–17 in as a G3/G4 checkpoint
- [[Note G6 Limit Theorems and Bayesian Inference]] — L19–L22: Chebyshev, WLLN, CLT, then MAP/LMS/linear LMS; the one note whose review JSON was never saved
- [[Note G7 Classical Statistical Inference]] — L23–L25: estimators, CIs, MLE, regression, the LRT; OCR-damaged sources reconstructed from B&T ch. 9, and the course-in-one-page finale

## Conventions

- Transcripts in `transcripts/LNN.md` / `recNN.md` are the ground-truth layer for
  notes-building; markers: `[UNSOLVED EXAMPLE]`, `[DERIVATION GAP]`, `[SOLUTION GAP]`,
  `[FIGURE: desc | raster/x.png]`, `[UNCERTAIN: ...]`, `[SOURCE TYPO?: ...]`.
- `transcripts/_summary.json` — structured per-source inventory (unsolved examples,
  gaps, figures, anomalies) from the transcription workflow.
- Notes bodies live in `notes/src/`, assembled with `notes/_build/build_note.py`.
- Subagents run Opus 5 / medium effort (user requirement).

## Decisions & open questions

Tracked in `memory/decisions.md` and `memory/questions.md` (append via
`wiki_log.py`; memory files sit outside the graph by design).
