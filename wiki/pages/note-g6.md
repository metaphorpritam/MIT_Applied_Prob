---
title: Note G6 Limit Theorems and Bayesian Inference
type: concept
status: active
aliases: [G6]
tags: [notes, g6]
sources:
  - ../notes/06_limits_bayesian.html
  - ../notes/src/fragments/g6_s0.html
  - ../notes/src/fragments/g6_s1.html
  - ../notes/src/fragments/g6_s2.html
  - ../notes/src/fragments/g6_s3.html
  - ../notes/src/fragments/g6_s4.html
  - ../notes/src/fragments/g6_s5.html
links:
  relates: [Notes Plan, MIT 6.041 Course, Note G5 Markov Chains, Note G7 Classical Statistical Inference]
---

# Note G6 Limit Theorems and Bayesian Inference

`notes/06_limits_bayesian.html` — 4.3 MB, 32 figures, 4 widgets, 49 practice items.
Covers [[MIT 6.041 Course]] L19–L22 with rec20–22. Two arcs in one note: what happens
to the sample mean, then the turn from modeling to inference. Tracked in
[[Notes Plan]]; assembled by [[Build Pipeline]].

## Section map

- **§0 Orientation: from a model to a conclusion** — Arc A (what happens to the sample
  mean) and Arc B (the inference turn), plus the map and roadmap.
- **§1 Markov, Chebyshev, and the weak law of large numbers** — the Markov inequality,
  the Chebyshev inequality, the sample mean $M_n$ and the weak law, the pollster's
  problem turning the weak law into a sample size, convergence in probability, and
  rec20 worked in full.
- **§2 The Central Limit Theorem** — the statement and why standardization is forced on
  us, what the theorem does *not* say, the normal-approximation recipe,
  De Moivre–Laplace and the $1/2$ correction for integer-valued sums, Chebyshev versus
  the CLT on one question with three answers, and two consequences (Stirling's formula,
  and where the CLT must not go).
- **§3 Bayesian inference: priors, posteriors, and the MAP rule** — the Bayesian setup,
  the three canonical posterior calculations, and MAP versus conditional expectation as
  point estimates.
- **§4 Least mean squares and linear LMS estimation** — the problem and the no-data
  baseline, the LMS theorem that $\mathbb{E}[\Theta\mid X]$ is optimal, the lecture's
  uniform example end to end, properties of the estimation error, linear LMS, several
  observations and choosing what to feed the estimator, and rec22 (Romeo and Juliet) in
  all seven parts.
- **§5 Synthesis** — the inequality-and-limit table, the Bayesian-estimation table, the
  five gotchas that cost the most, and the bridge to G7: drop the prior.

## Widgets

`w-g6s1-chebyshev` (the $1/k^2$ bound against the truth) · `w-g6s2-clt` (CLT animator —
the *exact* distribution of $Z_n$ by $n$-fold convolution, not simulated) ·
`w-g6s3-postexp` (posterior explorer: normal prior $\times$ normal noise) ·
`w-g6s4-lmsvslin` (LMS versus linear LMS on a curved relationship).

## Flagship worked problems

The pollster's sample size, from Chebyshev and then from the CLT · the same tail
question answered three ways (exact, Chebyshev, CLT) · De Moivre–Laplace with the
half-integer correction · the lecture's uniform LMS example end to end · rec20 in full ·
rec22 "Romeo and Juliet", all seven parts, the note's longest single worked problem.

## Review stats

**G6 is the one note with no `transcripts/_g6_review.json` on disk** — the review ran
and was applied, but the artifact was not saved. From `memory/log.md` (2026-07-30
09:52–10:09 UTC): the review completed at 10/10 lenses, fixing critical numeric errors
in the CLT section plus roughly twenty more issues; the consistency pass then made
8 edits, 2 of them real cross-note repairs; builds green and the hub card flipped.
Treat G6's counts as log-attested rather than JSON-attested, and exclude it when
totalling issue severities from the review JSONs.

## Special notes

- Edge headless broke system-wide during G6's re-shoot (print-to-PDF silently emitting
  nothing, even on the hub), which blocked verification for hours; Chrome was added to
  the screenshot candidates in [[Build Pipeline]] permanently as the fallback.
- Two orphan `</p>` closers in `g6_s1.html` were fixed at assembly time — the
  assembler's balanced-tag validation caught them.
- Prev: [[Note G5 Markov Chains]] · Next:
  [[Note G7 Classical Statistical Inference]].
