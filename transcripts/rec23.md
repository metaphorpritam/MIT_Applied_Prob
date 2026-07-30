# rec23 — Recitation 23 (December 2, 2010)

Covers: Classical statistical inference — maximum likelihood (ML) estimation (uniform $[0,\theta]$ model; normal mean and variance), confidence intervals via the central limit theorem, variance estimation/bounding (sample variance $\hat S_n^2$, plug-in Bernoulli variance $\hat\Theta_n(1-\hat\Theta_n)$, conservative upper bound), polling application.

Sources: `MIT6_041F10_rec23.pdf` (questions), `MIT6_041F10_rec23_sol.pdf` (solutions)

> Header block on both PDFs: Massachusetts Institute of Technology — Department of Electrical Engineering & Computer Science — 6.041/6.431: Probabilistic Systems Analysis (Fall 2010).
>
> Footnote on the question sheet: "Textbook problems are courtesy of Athena Scientific, and are used with permission."

> **Note on the solution PDF.** The solution sheet's title line is "**Recitation 23 Solutions**" (no date line, unlike the question sheet which carries "Recitation 23 / December 2, 2010"), and it has *no* Athena Scientific footnote — only the "Page 1 of 1" footer. The official solutions document for Recitation 23 contains *no worked solutions at all*. Its entire body is a list of three pointers back to the course textbook (Bertsekas & Tsitsiklis, *Introduction to Probability*). It is reproduced verbatim below, per problem. Page 2 of each PDF is the standard MIT OpenCourseWare boilerplate page (`http://ocw.mit.edu`, "6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010", "For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.").

---

## Problem 1 — ML estimation of $\theta$ for a uniform $[0,\theta]$ lateness (Romeo and Juliet)

### Statement

**Example 9.1, page 463 in textbook**

Romeo and Juliet start dating, but Juliet will be late on any date by a random amount $X$, uniformly distributed over the interval $[0,\theta]$. The parameter $\theta$ is unknown. Assuming that Juliet was late by an amount $x$ on their first date, find the ML estimate of $\theta$ based on the observation $X = x$.

### Official solution

Reproduced in full, verbatim, from the solution PDF:

> 1. Example 9.1 in the textbook (page 463)

[SOLUTION GAP: The entire solution is omitted. The official document only cites textbook Example 9.1 (page 463). No likelihood function $f_X(x;\theta) = 1/\theta$ for $0 \le x \le \theta$, no argument that the likelihood is decreasing in $\theta$ over the feasible region $\theta \ge x$, and no conclusion $\hat\theta_{ML} = x$ is written out in the recitation solution sheet.]

---

## Problem 2 — ML estimation of the mean and variance of a normal distribution

### Statement

**Example 9.4, page 464 in textbook**

Estimate the mean $\mu$ and variance $v$ of a normal distribution using $n$ independent observations $X_1, \ldots, X_n$.

### Official solution

Reproduced in full, verbatim, from the solution PDF:

> 2. Example 9.4 in the textbook (page 464)

[SOLUTION GAP: The entire solution is omitted. The official document only cites textbook Example 9.4 (page 464). No joint likelihood $f_X(x;\mu,v) = \prod_{i=1}^n \frac{1}{\sqrt{2\pi v}} \exp\{-(x_i-\mu)^2/(2v)\}$, no log-likelihood, no differentiation with respect to $\mu$ and $v$, and no resulting estimators $\hat\mu = \frac1n\sum_i x_i$, $\hat v = \frac1n\sum_i (x_i-\hat\mu)^2$ are written out in the recitation solution sheet.]

---

## Problem 3 — 95% confidence interval for a voter proportion (three variance estimates)

### Statement

**Example 9.8, page 474 of textbook**

We would like to estimate the fraction of voters supporting a particular candidate for office. We collect $n$ independent sample voter responses $X_1, \ldots, X_n$, where $X_i$ is viewed as a Bernoulli random variable, with $X_i = 1$ if the $i$th voter supports the candidate. We conducted a poll of 1200 people in North Carolina, and found that 684 were supporting the candidate. We would like to construct a 95% confidence interval for $\theta$, the proportion of people who support the candidate. As we saw in lecture, using the central limit theorem, an (approximate) 95% confidence interval can be defined as

$$\hat\Theta^- = \hat\Theta_n - 1.96\sqrt{\frac{v}{n}}, \qquad \hat\Theta^+ = \hat\Theta_n + 1.96\sqrt{\frac{v}{n}}$$

where $v = \operatorname{Var}(X_i)$, and $\hat\Theta_n = (X_1 + \ldots + X_n)/n$. Unfortunately, we don't know the value for $v$. Construct confidence intervals for $\theta$ using the following three ways of estimating or bounding the value for $v$ (in each case simply assume that $v$ is equal to the given estimate; note that this is a further approximation in cases (a) and (b)).

(a)

$$\hat S_n^2 = \frac{1}{n-1}\sum_{i=1}^{n}(X_i - \hat\Theta_n)^2$$

(b)

$$\hat\Theta_n(1 - \hat\Theta_n)$$

(c) The most conservative upper bound for the variance.

### Official solution

Reproduced in full, verbatim, from the solution PDF:

> 3. Example 9.8 in the textbook (page 474)

[SOLUTION GAP: The entire solution is omitted. The official document only cites textbook Example 9.8 (page 474). The recitation solution sheet contains no computation of $\hat\theta_n = 684/1200 = 0.57$, no evaluation of the three variance choices (sample variance $\hat s_n^2$, the plug-in value $\hat\theta_n(1-\hat\theta_n)$, and the conservative bound $v \le 1/4$), and no resulting numerical confidence intervals.]

---

## Figures

No figures, plots, diagrams, or trees appear in either the question PDF (`raster/rec23_p01.png`, `raster/rec23_p02.png`) or the solution PDF (`raster/rec23_sol_p01.png`, `raster/rec23_sol_p02.png`). Both documents are pure text/mathematics, with page 2 of each being the OCW boilerplate page.

## Notes on the text extraction

- The raw text extraction mangled the displayed confidence-interval formula into a single run: `Θˆ − = Θˆ n − 1.96 v v , Θˆ + = Θˆ n + 1.96 n n`. The page image confirms the correct form is the pair $\hat\Theta^- = \hat\Theta_n - 1.96\sqrt{v/n}$ and $\hat\Theta^+ = \hat\Theta_n + 1.96\sqrt{v/n}$ (the $\pm$ superscript matches the sign in front of the $1.96$), as transcribed above.
- The raw extraction rendered $\hat S_n^2$ as `Sˆn 2` and the summation as `1 � (Xi − Θˆ n)2 = n − 1 i=1`; the image confirms $\hat S_n^2 = \frac{1}{n-1}\sum_{i=1}^n (X_i-\hat\Theta_n)^2$.
- Ligature artifacts in the extraction (`ﬁrst`, `oﬃce`, `conﬁdence`, `deﬁned`) are normal `fi`/`ffi` ligatures, transcribed as plain text above.
- The footer "Page 1 of 1" was extracted as the broken fragment `f 1 ... Page 1 o`.
