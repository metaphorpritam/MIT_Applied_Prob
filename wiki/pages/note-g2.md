---
title: Note G2 Discrete Random Variables
type: concept
status: active
aliases: [G2]
tags: [notes, g2]
sources:
  - ../notes/02_discrete_rvs.html
  - ../notes/src/fragments/g2_s0.html
  - ../notes/src/fragments/g2_s1.html
  - ../notes/src/fragments/g2_s2.html
  - ../notes/src/fragments/g2_s3.html
  - ../notes/src/fragments/g2_s4.html
  - ../notes/src/fragments/g2_s5.html
  - ../transcripts/_g2_review.json
links:
  relates: [Notes Plan, MIT 6.041 Course, Note G1 Probability Fundamentals, Note G3 Continuous Random Variables]
---

# Note G2 Discrete Random Variables

`notes/02_discrete_rvs.html` — 3.4 MB, 25 figures, 4 widgets, 77 practice items.
Covers [[MIT 6.041 Course]] L05–L07 with rec05–07: the step from events to numbers.
Tracked in [[Notes Plan]]; assembled by [[Build Pipeline]].

## Section map

- **§0 From outcomes to numbers** — what a random variable is and why attaching numbers
  changes everything, the roadmap, and where the note sits in the course.
- **§1 Random variables and PMFs** — the PMF, the two starter PMFs (Bernoulli and
  discrete uniform), the binomial, the geometric, and how to choose among the named
  PMFs.
- **§2 Expectation** — the definition and the center-of-gravity reading, the expected
  value rule for $\mathbb{E}[g(X)]$, linearity (filling the three blanks on L05
  slide 7), the marksman, the bus paradox as size-biased sampling, and St. Petersburg
  as a genuinely infinite expectation.
- **§3 Variance, conditioning, and the geometric distribution** — why
  $\mathbb{E}[X - \mathbb{E}[X]] = 0$, variance and standard deviation, the
  expected-value rule biting on random speed, conditional PMFs and conditional
  expectation, geometric memorylessness, the total expectation theorem, geometric
  mean and variance, and state recursions for waiting for two in a row.
- **§4 Joint PMFs and multiple random variables** — joint PMFs, marginals, the
  conditional/chain rule, conditioning on a general event with the L07 grid worked out,
  independence, $\mathbb{E}[g(X,Y)]$ and linearity, variance of a sum, binomial mean
  and variance via indicators, three recitation joint-PMF problems in full, and the hat
  problem as indicators without independence.
- **§5 Synthesis: the discrete toolbox** — how the pieces fit, the PMF zoo, the
  expectation/variance identity sheet, G2's top gotchas, and what breaks when values go
  continuous.

## Widgets

`w-g2s1-pmf` (binomial/geometric/discrete-uniform explorer) · `w-g2s2-petersburg`
(St. Petersburg with a bankroll cap — what the game is actually worth) ·
`w-g2s3-memoryless` (k wasted tosses change nothing) · `w-g2s4-jointpmf` (the L07
slide-3 grid, conditioned).

## Flagship worked problems

The marksman (rec05 P2) · the bus paradox / size-biased vs uniform sampling
(rec05 P3) · St. Petersburg (rec05 P4) · waiting for two heads in a row via state
recursion · the L07 slide-3 joint grid conditioned on a general event · binomial mean
and variance by indicator decomposition · the hat problem.

## Review stats

`transcripts/_g2_review.json` — **49 issues**: 2 critical, 25 major, 22 minor,
distributed 10/3/10/8/11/7 across §0–§5. 46 fixes, 10 deferred; consistency pass then
did 34 renumbers, 49 citation fixes and one real cross-reference repair into
[[Note G1 Probability Fundamentals]].

## Special notes

- The §0 roadmap figure was authored before §3–§5 scopes were final and printed the
  wrong section split — caught as a critical and corrected. Roadmap figures were
  authored last in every later note as a result.
- A reviewer *falsified* an author claim about scipy/numpy geometric conventions by
  running both libraries; both count trials, so the note's convention stands.
- Leftover cosmetic item: the `Problem 4.A/B/C` label style in `g2_s4.html`.
- Prev: [[Note G1 Probability Fundamentals]] · Next:
  [[Note G3 Continuous Random Variables]].
