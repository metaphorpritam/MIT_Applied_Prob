---
title: Notes Plan
type: decision
status: active
aliases: [topic groups, group plan, html notes plan]
tags: [plan, tracking]
links:
  relates: [MIT 6.041 Course, Build Pipeline]
---

# Notes Plan

Seven topic-grouped interactive HTML notes (3–4 lectures each, aligned recitations),
ordered so each note flows into the next. **This page is the progress tracker —
update the Status column after every work session.**

| # | File slug | Lectures | Recitations | Theme | Status |
|---|---|---|---|---|---|
| G1 | 01_probability_basics | L01–L04 | rec01–04 | Models, axioms, conditioning, Bayes, independence, counting | **DONE** (reviewed, fixed, polished) |
| G2 | 02_discrete_rvs | L05–L07 | rec05–07 | PMF, expectation, variance, joint/conditional PMFs | **DONE** (reviewed, fixed, polished) |
| G3 | 03_continuous_rvs | L08–L11 | rec08–11 | PDFs, CDFs, continuous Bayes, derived distributions, cov/corr | **DONE** (reviewed, fixed, polished) |
| G4 | 04_expectation_processes | L12–L15 | rec13–15 (+rec12=G3 material, worked in s1) | Iterated expectations, random sums, Bernoulli & Poisson processes | **DONE** (reviewed, fixed, polished) |
| G5 | 05_markov_chains | L16–L18 | rec18–19 (+rec16–17 checkpoint) | Markov chains: transition probs, classification, steady state, absorption | **DONE** (reviewed, fixed, polished) |
| G6 | 06_limits_bayesian | L19–L22 | rec20–22 | Chebyshev, WLLN, CLT; Bayesian inference, LMS, linear LMS | **DONE** (reviewed, fixed, polished) |
| G7 | 07_classical_inference | L23–L25 | rec23–24 | Classical estimation, CIs, MLE, hypothesis testing | **DONE** (reviewed, fixed, polished) |

## Per-note quality contract (user requirements)

1. Step-by-step derivations — no skipped steps, every variable explained, substitutions shown with intermediate values.
2. Every `[UNSOLVED EXAMPLE]` in the transcripts SOLVED completely; every `[DERIVATION GAP]` filled.
3. Every numerical value recomputed in Python (`computes/<slug>_*.py` → JSON); never hand-typed.
4. Interpretation + gotchas + 2–3 practice questions (with collapsible solutions) per topic.
5. Figures: regenerate charts in matplotlib where data known; embed raster crops otherwise; flowcharts for decision points (which distribution? which tool? transformation method?). All figures vision-verified.
6. Interactive widgets (sliders/steppers) for key parameter dependencies.
7. Left sidebar TOC (auto-built), prev/next nav, index.html hub entry.
8. Adversarial review pass before a note is marked done.

## Pipeline per note (settled in session 1)

transcripts → section outline → compute scripts → figures (+vision check) →
body HTML → build_note.py → screenshot review → adversarial review workflow → fix → done.
