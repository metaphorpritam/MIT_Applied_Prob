# rec09 — Recitation 9 (October 7, 2010)

Covers: continuous random variables; exponential random variable (CDF, interval probabilities, geometric-series summation); memorylessness of the exponential; jointly continuous random variables — joint PDF uniform on a triangle, marginal PDF, conditional PDF, conditional expectation and the total expectation theorem, symmetry arguments; the "broken stick" triangle problem (uniform joint PDF on the unit square, geometric probability).

Sources: MIT6_041F10_rec09.pdf (questions), MIT6_041F10_rec09_sol.pdf (solutions)

Document header (both PDFs):
Massachusetts Institute of Technology
Department of Electrical Engineering & Computer Science
6.041/6.431: Probabilistic Systems Analysis
(Fall 2010)

Title block: question sheet — "Recitation 9 / October 7, 2010"; solution sheet — "Recitation 9 Solutions / October 7, 2010".

Footer of the question sheet: "Textbook problems are courtesy of Athena Scientific, and are used with permission. Page 1 of 1". The solution sheet's footer carries only "Page 1 of 1" (no Athena Scientific credit line).

---

## Problem 1 — Exponential r.v. falling in an interval $[n, n+1]$ with $n$ odd

### Statement

Let $X$ be an exponential random variable with parameter $\lambda > 0$. Calculate the probability that $X$ belongs to one of the intervals $[n, n+1]$ with $n$ odd.

### Official solution

We first compute the probability that $X$ is in interval $[n, n+1]$ for an arbitrary nonnegative $n$. Then, we will add the probabilities for all odd positive integer values of $n$.

We could integrate the PDF of $X$ over the given interval but we will use the CDF here. Using the CDF for the exponential random variable,

$$
\begin{aligned}
\mathbf{P}(n \le X \le n+1) &= F_X(n+1) - F_X(n) \\
&= \left(1 - e^{-\lambda(n+1)}\right) - \left(1 - e^{-\lambda n}\right) \\
&= e^{-\lambda n}\left(1 - e^{-\lambda}\right).
\end{aligned}
$$

Since the intervals are disjoint, we can sum this probability for all odd integers $n$ to find the probability of interest:

$$
\begin{aligned}
\mathbf{P}(\{X \in [n, n+1] \text{ for some odd } n\})
&= \sum_{n \text{ odd}} e^{-\lambda n}\left(1 - e^{-\lambda}\right) \\
&= \left(1 - e^{-\lambda}\right)\sum_{k=0}^{\infty} e^{-\lambda(2k+1)} \\
&= \left(1 - e^{-\lambda}\right) e^{-\lambda} \sum_{k=0}^{\infty}\left(e^{-2\lambda}\right)^{k} \\
&= \left(1 - e^{-\lambda}\right) e^{-\lambda}\, \frac{1}{1 - e^{-2\lambda}} \\
&= \left(1 - e^{-\lambda}\right) e^{-\lambda}\, \frac{1}{(1 - e^{-\lambda})(1 + e^{-\lambda})} \\
&= \frac{e^{-\lambda}}{1 + e^{-\lambda}}.
\end{aligned}
$$

[SOLUTION GAP: the reparametrization of the odd integers as $n = 2k+1$, $k = 0, 1, 2, \dots$ is done silently; the geometric-series formula $\sum_{k=0}^{\infty} r^k = 1/(1-r)$ with $r = e^{-2\lambda} < 1$ is applied without stating the convergence condition; and the factorization $1 - e^{-2\lambda} = (1 - e^{-\lambda})(1 + e^{-\lambda})$ is used without comment.]

---

## Problem 2 — Exponential Random Variable is Memoryless

### Statement

(Example 3.13 of the text book, page 165) **Exponential Random Variable is Memoryless.**
The time $T$ until a new light bulb burns out is an exponential random variable with parameter $\lambda$. Ariadne turns the light on, leaves the room, and when she returns, $t$ time units later, finds that the bulb is still on, which corresponds to the event $A = \{T > t\}$. Let $X$ be the additional time until the bulb burns out. What is the conditional CDF of $X$, given the event $A$?

### Official solution

See Example 3.13 in the textbook on page 165.

[SOLUTION GAP: the entire solution is an external reference — the recitation solution sheet gives no derivation. The textbook result (not reproduced in the source) is that the conditional CDF of $X$ given $A$ equals the unconditional exponential CDF, i.e. $\mathbf{P}(X \le x \mid T > t) = 1 - e^{-\lambda x}$ for $x \ge 0$.]

---

## Problem 3 — Joint PDF uniform on a triangle (Text Problem 3.23)

### Statement

Problem 3.23, page 191 in the text.

Let the random variables $X$ and $Y$ have a joint PDF which is uniform over the triangle with vertices $(0,0)$, $(0,1)$, and $(1,0)$.

(a) Find the joint PDF of $X$ and $Y$.

(b) Find the marginal PDF of $Y$.

(c) Find the conditional PDF of $X$ given $Y$.

(d) Find $\mathbf{E}[X \mid Y = y]$, and use the total expectation theorem to find $\mathbf{E}[X]$ in terms of $\mathbf{E}[Y]$.

(e) Use the symmetry of the problem to find the value of $\mathbf{E}[X]$.

### Official solution

Problem 3.23, page 191 in text. See online solutions.

[SOLUTION GAP: the whole solution is deferred to the textbook's online solutions; no work of any kind is given in the recitation solution sheet.]

---

## Problem 4 — Broken stick forming a triangle

### Statement

We have a stick of unit length, and we break it into three pieces. We choose randomly and independently two points on the stick using a uniform PDF, and we break the stick at these points. What is the probability that the three pieces we are left with can form a triangle?

### Official solution

Problem 3.22, part (i), page 191 in text (see online solution).

[SOLUTION GAP: the whole solution is deferred to the textbook's online solution; no derivation, no region-of-the-unit-square argument, and no numerical answer are given in the recitation solution sheet.]

---

## Figures

No figures, plots, diagrams, or trees appear in either PDF. Page 1 of each document is pure text/equations; page 2 of each is the standard MIT OpenCourseWare back matter:

> MIT OpenCourseWare
> http://ocw.mit.edu
> 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability
> Fall 2010
> For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

(Raster pages: raster/rec09_p01.png, raster/rec09_p02.png, raster/rec09_sol_p01.png, raster/rec09_sol_p02.png.)

---

## Transcription notes

- The raw text extraction of the solution PDF contained stray "�" glyphs at the top of page 1 (artifacts of large LaTeX delimiters `\left(` / `\right)` and `\sum`); these were resolved against raster/rec09_sol_p01.png and are rendered above as proper parentheses and summation signs.
- The extraction also dropped the parentheses in the line `= 1 − e^{-λ(n+1)} − 1 − e^{-λn}`; the raster confirms it is $\left(1 - e^{-\lambda(n+1)}\right) - \left(1 - e^{-\lambda n}\right)$.
- Question 3 and question 4 in the problem sheet correspond, per the solution sheet, to textbook Problem 3.23 and Problem 3.22 part (i) respectively (both page 191). The question sheet labels only question 3 with its textbook number; question 4's textbook origin is revealed only in the solution sheet.
- The solution to Problem 1 says "for an arbitrary nonnegative $n$" and then "all odd positive integer values of $n$"; the summation index used is $n = 2k+1$, $k \ge 0$, i.e. $n = 1, 3, 5, \dots$ [SOURCE TYPO?: "nonnegative" is loose — for the CDF-difference formula to apply, $n \ge 0$ is what is needed, which is consistent; but the phrase "nonnegative" vs. the later restriction to odd *positive* integers is a slight mismatch in wording, not in mathematics.]
