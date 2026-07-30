---
title: Note G3 Continuous Random Variables
type: concept
status: active
aliases: [G3]
tags: [notes, g3]
sources:
  - ../notes/03_continuous_rvs.html
  - ../notes/src/fragments/g3_s0.html
  - ../notes/src/fragments/g3_s1.html
  - ../notes/src/fragments/g3_s2.html
  - ../notes/src/fragments/g3_s3.html
  - ../notes/src/fragments/g3_s4.html
  - ../notes/src/fragments/g3_s5.html
  - ../transcripts/_g3_review.json
links:
  relates: [Notes Plan, MIT 6.041 Course, Note G2 Discrete Random Variables, Note G4 Iterated Expectations and Arrival Processes]
---

# Note G3 Continuous Random Variables

`notes/03_continuous_rvs.html` — 6.1 MB (the largest note), 38 figures, 5 widgets,
77 practice items. Covers [[MIT 6.041 Course]] L08–L11 with rec08–11: sums become
integrals. Tracked in [[Notes Plan]]; assembled by [[Build Pipeline]].

## Section map

- **§0 From sums to integrals** — why a continuous random variable has no PMF, the
  discrete/continuous correspondence table, and a reading guide.
- **§1 PDFs, CDFs, and the classic continuous distributions** — densities, expectation
  and variance by integration, the continuous uniform, the CDF as the one object that
  works in all three worlds, the exponential and its memorylessness, maxima and minima
  of independent exponentials, the normal, and a choose-a-method guide.
- **§2 Joint, marginal, and conditional PDFs** — probability as volume, marginalizing,
  the conditional density as a renormalized slice, independence and Buffon's needle,
  conditional expectation with stick-breaking, rec09 P1/P3/P4 in full, and a decision
  guide.
- **§3 The four faces of Bayes' rule** — the inference problem as one rule with four
  faces; L10's derivation gap filled with the thin-strip argument; (C|C) continuous
  unknown and continuous evidence; (D|C) detection; (C|D) learning a probability; plus
  an appendix solving L10's three unsolved derived-distribution examples.
- **§4 Derived distributions and convolution** — the CDF method, the general formula for
  strictly monotonic $g$, $Z = Y/X$ on the unit square, rec11 P3's normal through a
  kinked map, discrete convolution (flip, shift, cross-multiply, add), continuous
  convolution and the sum of two uniforms, the sum of two normals, and
  covariance/correlation.
- **§5 Synthesis and checkpoint** — all of G3 on one page, the continuous distribution
  zoo, which derived-distribution method and when, top gotchas, a G1–G3 mixed
  quiz-style checkpoint, and the bridge to G4.

## Widgets

`w-g3s1-memoryless` (slide the elapsed time, watch nothing happen) · `w-g3s1-normal`
(move $\mu$ and $\sigma$, shade $[a,b]$, read the probability) · `w-g3s2-slice` (fix
$Y = y$, slice the joint density, renormalize) · `w-g3s3-bayesupdater` (learning a
coin's bias, rec11 P2 generalized) · `w-g3s4-convolve` (convolution animator with the
product shaded).

## Flagship worked problems

Buffon's needle, solved · the broken stick (rec09 P4) and uniform-on-a-triangle
(rec09 P3) · an exponential landing in an odd interval (rec09 P1) · the thin-strip
derivation of continuous Bayes · rec11 P3, a normal pushed through a kinked map ·
the sum of two independent normals shown normal · the sum of two uniforms by
convolution.

## Review stats

`transcripts/_g3_review.json` — **56 issues** (the largest count of any note):
2 critical, 21 major, 33 minor, distributed 9/7/6/8/14/12 across §0–§5. One critical
was an off-by-one in the *dice convolution compute script*, not just the prose — the
recompute-everything rule earned its keep. 53 fixes; the consistency pass made 42
edits including 12 cross-note citation repairs.

## Special notes

- The other critical was a mixed-convention sentence in §1.7: a two-sided tail
  $P(|X| \ge 3\sigma) = 0.0027$ described as "one time in 740", which is the one-sided
  figure ($1/0.00135$); the two-sided value is $1/370$.
- The authoring agent caught and corrected a source typo in rec08 P3(e).
- rec10 is used as the checkpoint problem set in §5 rather than as new material.
- Prev: [[Note G2 Discrete Random Variables]] · Next:
  [[Note G4 Iterated Expectations and Arrival Processes]].
