# rec22 — Recitation 22 (November 30, 2010)

Covers: Bayesian inference with continuous parameter and continuous observations; posterior distribution of a uniform-scale parameter; MAP estimation; LMS (conditional expectation) estimation; conditional mean squared error; linear LMS estimation
Sources: MIT6_041F10_rec22.pdf (questions), MIT6_041F10_rec22_sol.pdf (solutions)

Note on the solution PDF: the official "solutions" document contains **no worked derivations at all**. It only points to the corresponding worked examples in the course textbook (Bertsekas & Tsitsiklis, *Introduction to Probability*, 2nd ed.). This is transcribed faithfully below.

---

## Problem 1 — Romeo and Juliet: Bayesian inference of the lateness range $\Theta$ (Examples 8.2, 8.7, 8.12, 8.15 in the textbook)

### Statement

**Examples 8.2, 8.7, 8.12, and 8.15 in the textbook**

Romeo and Juliet start dating, but Juliet will be late on any date by a random amount $X$, uniformly distributed over the interval $[0, \theta]$. The parameter $\theta$ is unknown and is modeled as the value of a random variable $\Theta$, uniformly distributed between zero and one hour.

(a) Assuming that Juliet was late by an amount $x$ on their first date, how should Romeo use this information to update the distribution of $\Theta$?

(b) How should Romeo update the distribution of $\Theta$ if he observes that Juliet is late by $x_1, \ldots, x_n$ on the first $n$ dates? Assume that Juliet is late by a random amount $X_1, \ldots, X_n$ on the first $n$ dates where, given $\theta$, $X_1, \ldots, X_n$ are uniformly distributed between zero and $\theta$ and are conditionally independent.

(c) Find the MAP estimate of $\Theta$ based on the observation $X = x$.

(d) Find the LMS estimate of $\Theta$ based on the observation $X = x$.

(e) Calculate the conditional mean squared error for the MAP and the LMS estimates. Compare your results.

(f) Derive the linear LMS estimator of $\Theta$ based on X.

[SOURCE TYPO?: in part (f) the observation is typeset as an upright "X" rather than the math-italic $X$ used everywhere else in the document; it denotes the same random variable.]

(g) Calculate the conditional mean squared error for the linear LMS estimate. Compare your answer to the results of part (e).

*Footer of the question page:* "Textbook problems are courtesy of Athena Scientific, and are used with permission. Page 1 of 1"

### Official solution

**Recitation 22 Solutions**

The problem is based on the following examples in the textbook.

(a) Example 8.2 page 414.

(b) Example 8.2 page 414.

(c) Example 8.7 page 424.

(d) Example 8.7 page 424.

(e) Example 8.12 page 432-433.

(f) Example 8.15 page 439-440.

(g) Example 8.15 page 439-440.

*Footer of the solution page:* "Page 1 of 1" (the solution page carries no "Textbook problems are courtesy of Athena Scientific" credit line — only the question page does).

[UNSOLVED EXAMPLE: All seven parts (a)–(g) are posed in the question PDF and left without any worked answer in the solution PDF; only textbook cross-references are supplied.]

[SOLUTION GAP: The entire solution is skipped. The official solution document provides only textbook cross-references — no posterior density, no MAP/LMS estimator, no mean-squared-error computation, and no linear LMS derivation is given anywhere in the PDF. All seven parts (a)–(g) are unanswered in the source material.]

---

## Figures

No figures, plots, diagrams, or trees appear in either the question PDF or the solution PDF. Page 1 of each is pure text; page 2 of each is the standard MIT OpenCourseWare citation/terms-of-use notice.
