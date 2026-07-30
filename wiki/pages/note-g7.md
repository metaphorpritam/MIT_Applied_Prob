---
title: Note G7 Classical Statistical Inference
type: concept
status: active
aliases: [G7]
tags: [notes, g7]
sources:
  - ../notes/07_classical_inference.html
  - ../notes/src/fragments/g7_s0.html
  - ../notes/src/fragments/g7_s1.html
  - ../notes/src/fragments/g7_s2.html
  - ../notes/src/fragments/g7_s3.html
  - ../notes/src/fragments/g7_s4.html
  - ../notes/src/fragments/g7_s5.html
  - ../transcripts/_g7_review.json
links:
  relates: [Notes Plan, MIT 6.041 Course, Note G6 Limit Theorems and Bayesian Inference, Note G1 Probability Fundamentals]
---

# Note G7 Classical Statistical Inference

`notes/07_classical_inference.html` — 5.3 MB, 30 figures, 5 widgets, 46 practice items.
Covers [[MIT 6.041 Course]] L23–L25 with rec23–24, and closes the course: §5.4 puts all
seven notes on one page. Tracked in [[Notes Plan]]; assembled by [[Build Pipeline]].

## Section map

- **§0 Orientation: the classical turn** — one parameter and many models, the estimator
  (random) versus the estimate (a number), why every classical question is a probability
  question about the data, when to be Bayesian and when classical, and the roadmap.
- **§1 Estimators, bias, consistency, and confidence intervals** — bias and consistency,
  $\mathrm{MSE} = \mathrm{bias}^2 + \mathrm{variance}$, the sample mean as an estimator,
  constructing a confidence interval, what a CI means and emphatically does not mean,
  three ways out when $\sigma$ is unknown, and rec23 P3 (polling with three variance
  estimates).
- **§2 Maximum likelihood estimation** — the likelihood function and what it is not, the
  smooth case via the log-likelihood, normal mean and variance together (rec23 P2), the
  uniform $[0,\theta]$ model where calculus fails (rec23 P1), rec24 P1 (the blackbody
  photon counter) end to end, rec24 P2 showing least squares *is* maximum likelihood,
  and why ML is worth trusting.
- **§3 Linear regression** — what is fixed and what is random, the least-squares
  criterion and the normal equations, residuals and $R^2$, the linear-LMS reading of the
  formulas, ML under normal noise, reporting a regression on a real dataset, more and
  better variables and priors, and what a fitted line does not claim.
- **§4 Binary hypothesis testing and the likelihood ratio test** — two hypotheses / a
  rejection region / two errors, the LRT and where it comes from, tests on a normal mean
  (L25 slide 3) and on a normal variance (L25 slide 4), the error tradeoff and what
  changes when $L(X)$ is discrete, Neyman–Pearson optimality with the ROC picture,
  composite hypotheses and significance testing (L25 slide 5), goodness of fit solving
  the lecture's two open problems (L25 slides 6–7), and a which-test guide.
- **§5 Synthesis, and the course in one figure** — the classical-inference cheatsheet,
  the Bayesian/classical master comparison, five costly gotchas, the whole course on one
  page, and where to go next.

## Widgets

`w-g7s1-mse` (bias–variance tradeoff for the shrunk estimator $cM_n$) ·
`w-g7s1-cicover` (coverage simulator, 100 replications) · `w-g7s2-mle` (likelihood
explorer: three models, one recipe) · `w-g7s3-lsq` (what the noise level does to the
fit) · `w-g7s4-lrt` (threshold explorer, $N(0,1)$ versus $N(d,1)$).

## Flagship worked problems

rec23 P3, polling with three different variance estimates compared side by side ·
rec23 P2, normal mean and variance estimated jointly · rec23 P1, the uniform
$[0,\theta]$ MLE where differentiation fails and the maximum sits at the boundary ·
rec24 P1, the blackbody photon counter end to end · rec24 P2, least squares derived as
maximum likelihood under normal noise · the L25 normal-mean and normal-variance tests ·
the two open goodness-of-fit problems from L25 slides 6–7, solved.

## Review stats

`transcripts/_g7_review.json` — **49 issues**: 4 critical, 12 major, 33 minor,
distributed 4/9/10/9/10/7 across §0–§5; 50 fixes. Two criticals are worth remembering:

- `w-g7s2-mle` shipped an LCG whose product `sd * 1103515245` reaches $\sim$2.4e18, past
  $2^{53}$, so the low bits were destroyed by double rounding *before* the `& 0x7fffffff`
  mask — every parity number the widget advertised was unreachable in a browser. The
  reviewer proved it by emulating IEEE-754 doubles plus `ToInt32` against the exact
  big-integer Python LCG in `computes/g7_s2.py`.
- §4.7's rejection region $\{s \le 469\} \cup \{s \ge 531\}$ busted the stated $\alpha$
  budget and contradicted itself within the same example.

The consistency pass was the largest of the course: 84 edits, including splitting a
shared counter in §3, unifying ML/MAP notation, and 3 cross-note fixes.

## Special notes — OCR-mangled sources

The L23–L25 handouts sit at the bad end of the font-encoding damage described in
[[MIT 6.041 Course]], and rec24's transcript carries five `[UNCERTAIN]` /
`[SOURCE TYPO?]` markers — the most of any G7 source. Where a printed constant or
formula could not be trusted, it was **reconstructed against Bertsekas–Tsitsiklis
Chapter 9** (the chapter preamble and §9.1 onward), which this note therefore cites
far more heavily than its siblings; the review brief carried a dedicated hint to
re-verify every reconstructed quantity against the book. That discipline paid off in
both directions — the authoring pass caught a rounding slip in B&T's own Example 9.8(c).

Course totals at close: roughly 330 review issues found and fixed, 226 figures,
36 widgets across the seven notes.

Prev: [[Note G6 Limit Theorems and Bayesian Inference]] · Back to the start:
[[Note G1 Probability Fundamentals]].
