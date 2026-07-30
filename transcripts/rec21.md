# rec21 — Recitation 21 (November 23, 2010)

Covers: Markov inequality, Chebyshev inequality, Central Limit Theorem (normal approximation to sums of i.i.d. random variables), CLT with de-Moivre/continuity-style correction for integer-valued sums, sums of Poisson random variables via the Poisson process, Stirling's approximation for $n!$

Sources: `MIT6_041F10_rec21.pdf` (questions), `MIT6_041F10_rec21_sol.pdf` (solutions)

Header block on both PDFs:
> MASSACHUSETTS INSTITUTE OF TECHNOLOGY
> Department of Electrical Engineering & Computer Science
> 6.041/6.431: Probabilistic Systems Analysis
> (Fall 2010)

Title line of the question sheet: "Recitation 21 / November 23, 2010". Title line of the solution sheet: "Recitation 21 Solutions / November 23, 2010".

Footer of the question sheet: "Textbook problems are courtesy of Athena Scientific, and are used with permission. Page 1 of 1". The solution sheet carries the same MIT header block on both content pages, with centered page numbers "1" and "2" at the foot.

---

## Problem 1 — Bounding $P(X_1+\cdots+X_{10}\ge 7)$ for uniforms: Markov vs. Chebyshev vs. CLT

### Statement

Let $X_1, \ldots, X_{10}$ be independent random variables, uniformly distributed over the unit interval $[0,1]$.

(a) Estimate $\mathbf{P}(X_1 + \cdots + X_{10} \ge 7)$ using the Markov inequality.

(b) Repeat part (a) using the Chebyshev inequality.

(c) Repeat part (a) using the central limit theorem.

### Official solution

**(a)** To use the Markov inequality, let $X = \sum_{i=1}^{10} X_i$. Then,

$$\mathbf{E}[X] = 10\,\mathbf{E}[X_i] = 5,$$

and the Markov inequality yields

$$\mathbf{P}(X \ge 7) \le \frac{5}{7} = 0.7142.$$

**(b)** Using the Chebyshev inequality, we find that

$$2\mathbf{P}(X - 5 \ge 2) = \mathbf{P}(|X - 5| \ge 2)$$
$$\le \frac{\operatorname{var}(X)}{4} = \frac{10/12}{4}$$
$$\mathbf{P}(X - 5 \ge 2) \le \frac{5}{48} = 0.1042.$$

[SOLUTION GAP: the first equality uses, without comment, the symmetry of the distribution of $X$ about its mean $5$ (so that the two tails $\{X-5\ge 2\}$ and $\{X-5\le -2\}$ have equal probability). Also unstated: $\operatorname{var}(X)=10\cdot\frac{1}{12}=\frac{10}{12}$ from $\operatorname{var}(X_i)=1/12$ for a uniform on $[0,1]$; and the final arithmetic $\frac{1}{2}\cdot\frac{10/12}{4}=\frac{10}{96}=\frac{5}{48}$.]

**(c)** Finally, using the Central Limit Theorem, we find that

$$\mathbf{P}\!\left(\sum_{i=1}^{10} X_i \ge 7\right) = 1 - \mathbf{P}\!\left(\sum_{i=1}^{10} X_i \le 7\right)$$
$$= 1 - \mathbf{P}\!\left(\frac{\sum_{i=1}^{10} X_i - 5}{\sqrt{10/12}} \le \frac{7-5}{\sqrt{10/12}}\right)$$
$$\approx 1 - \Phi(2.19)$$
$$\approx 0.0143.$$

[SOLUTION GAP: the numerical evaluation $\dfrac{2}{\sqrt{10/12}} = \dfrac{2}{0.9129} \approx 2.19$ is not shown, nor is the table lookup $\Phi(2.19) \approx 0.9857$.]

---

## Problem 2 — Textbook Problem 10 (page 290): factory gadget production

### Statement

**Problem 10 in the textbook (page 290)**

A factory produces $X_n$ gadgets on day $n$, where the $X_n$ are independent and identically distributed random variables, with mean 5 and variance 9.

(a) Find an approximation to the probability that the total number of gadgets produced in 100 days is less than 440.

(b) Find (approximately) the largest value of $n$ such that

$$\mathbf{P}\left(X_1 + \cdots + X_n \ge 200 + 5n\right) \le 0.05.$$

(c) Let $N$ be the first day on which the total number of gadgets produced exceeds 1000. Calculate an approximation to the probability that $N \ge 220$.

### Official solution

> 2. Check online solutions.

[UNSOLVED EXAMPLE: Problem 2 (a), (b) and (c) are posed on the question sheet but the solution sheet gives no worked solution at all — only the one-line pointer "Check online solutions." Nothing further about this problem appears anywhere in either PDF.]

[SOLUTION GAP: the entire solution to Problem 2 is omitted from the recitation solution sheet — it merely refers the reader to the online (textbook) solutions. Parts (a), (b) and (c) are all unsolved in this document.]

---

## Problem 3 — Sums of unit-mean Poissons and the CLT derivation of Stirling's formula

### Statement

Let $X_1, X_2, \ldots$, be independent Poisson random variables with mean and variance equal to 1. For any $n > 0$, let $S_n = \sum_{i=1}^{n} X_i$.

(a) Show that $S_n$ is Poisson with mean and variance equal to $n$. Hint: Relate $X_1, X_2, \ldots, X_n$ to a Poisson process with rate 1.

(b) Show how the central limit theorem suggests the approximation

$$n! \approx \sqrt{2\pi n}\left(\frac{n}{e}\right)^n$$

for large values of the positive integer $n$.

### Official solution

**(a)** If we interpret $X_i$ as the number of arrivals in an interval of length 1 in a Poisson process of rate 1, then, $S_n = X_1 + \cdots + X_n$ can be seen as the number of arrivals in an interval of length $n$ in the Poisson process of rate 1. Therefore, $S_n$ is a Poisson random variable with mean and variance equal to $n$.

**(b)** We use the random variables $X_1, \ldots, X_n$ and the random variable $S_n = X_1 + \cdots + X_n$. Denoting by $Z$ the standard normal, and applying the central limit theorem, we have for large $n$

$$
\begin{aligned}
\mathbf{P}(S_n = n) &= \mathbf{P}(n - 1/2 < S_n < n + 1/2)\\
&= \mathbf{P}\!\left(\frac{-1}{2\sqrt{n}} < \frac{S_n - n}{\sqrt{n}} \le \frac{1}{2\sqrt{n}}\right)\\
&\approx \mathbf{P}\!\left(\frac{-1}{2\sqrt{n}} < Z \le \frac{1}{2\sqrt{n}}\right)\\
&= \frac{1}{\sqrt{2\pi}}\int_{-1/2\sqrt{n}}^{1/2\sqrt{n}} e^{-z^2/2}\,dz\\
&\approx \frac{1}{\sqrt{2\pi}}\,\frac{1}{\sqrt{n}}\, e^{-z^2/2}\bigg|_{z=0}\\
&= \frac{1}{\sqrt{2\pi n}}
\end{aligned}
$$

where the first equation follows from the fact that $S_n$ takes integer values, the first approximation is suggested by the central limit theorem, and the second approximation uses the fundamental theorem of calculus (the value of a definite integral over a small interval is equal to the length of the interval times the integrand evaluated at some point within the interval). Since $S_n$ is Poisson with mean $n$, we have

$$\mathbf{P}(S_n = n) = e^{-n}\frac{n^n}{n!},$$

and by combining the preceding relations, we see that $n! \approx n^n e^{-n}\sqrt{2\pi n} = \sqrt{2\pi n}\left(\frac{n}{e}\right)^n$.

One may show that

$$\lim_{n\to\infty} \frac{n!}{n^n e^{-n}\sqrt{2\pi n}} = 1,$$

so the relative error of the approximation tends to 0 as $n \to \infty$. A more precise estimate is that

$$n! = n^n e^{-n}\sqrt{2\pi n}\cdot e^{\lambda_n},$$

where

$$\frac{1}{12n+1} < \lambda_n < \frac{1}{12n}.$$

However, one cannot derive these relations from the central limit theorem.

Note that the form of the approximation was first discovered by de Moivre in the form $n! \approx n^{n+1/2} e^{-n}\cdot(\text{constant})$, and gave a complicated expression for the constant. De Moivre's friend Stirling subsequently showed that the constant has the simple form $\sqrt{2\pi}$.

[SOLUTION GAP: the "second approximation" step replaces the integral over $\left(-\frac{1}{2\sqrt n}, \frac{1}{2\sqrt n}\right]$ (an interval of length $\frac{1}{\sqrt n}$) by (length) × (integrand at $z=0$) = $\frac{1}{\sqrt n}\cdot 1$; the evaluation $e^{-z^2/2}\big|_{z=0}=1$ and hence $\frac{1}{\sqrt{2\pi}}\cdot\frac{1}{\sqrt n} = \frac{1}{\sqrt{2\pi n}}$ is not spelled out. The claim $\lim_{n\to\infty} n!/(n^n e^{-n}\sqrt{2\pi n}) = 1$ and the bounds on $\lambda_n$ are stated without proof ("One may show that").]

---

## Figures

No figures, diagrams, plots, or trees appear in either the question sheet or the solution sheet for rec21. Both documents are pure text/formula pages. (raster/rec21_p02.png and raster/rec21_sol_p03.png are the standard MIT OpenCourseWare back-matter page: "MIT OpenCourseWare — http://ocw.mit.edu — 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability — Fall 2010 — For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.")
