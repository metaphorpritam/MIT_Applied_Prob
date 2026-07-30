# rec11 — Recitation 11 (October 14, 2010)

Covers: Bayes' rule for a discrete random variable conditioned on a continuous one; Bayes' rule for a continuous random variable conditioned on a discrete one; inference with Laplacian (two-sided exponential) noise; beta-distribution posterior for a Bernoulli success probability; derived distributions — CDF method for a function of a normal random variable.

Sources: MIT6_041F10_rec11.pdf, MIT6_041F10_rec11_sol.pdf

Massachusetts Institute of Technology
Department of Electrical Engineering & Computer Science
6.041/6.431: Probabilistic Systems Analysis (Fall 2010)

---

## Problem 1 — Discrete signal in Laplacian noise: $P(X=1 \mid Z=z)$

### Statement

Let $X$ be a discrete random variable that takes the values $1$ with probability $p$ and $-1$ with probability $1-p$. Let $Y$ be a continuous random variable independent of $X$ with the Laplacian (two-sided exponential) distribution

$$f_Y(y) \;=\; \tfrac{1}{2}\lambda e^{-\lambda |y|},$$

and let $Z = X + Y$. Find $\mathbf{P}(X = 1 \mid Z = z)$. Check that the expression obtained makes sense for $p \to 0^+$, $p \to 1^-$, $\lambda \to 0^+$, and $\lambda \to \infty$.

### Official solution

We need to apply the version of Bayes rule for a discrete random variable conditioned on a continuous random variable:

$$p_{X|Z}(x \mid z) \;=\; \frac{p_X(x) f_{Z|X}(z \mid x)}{f_Z(z)} \;=\; \frac{p_X(x) f_{Z|X}(z \mid x)}{\sum_{k=0}^{1} p_X(k) f_{Z|X}(z \mid k)}.$$

[SOURCE TYPO?: the summation index runs $k = 0$ to $1$, but $X$ takes the values $-1$ and $+1$, not $0$ and $1$; the sum should be over $k \in \{-1, 1\}$. The subsequent algebra does use the two values $-1$ and $+1$ correctly.]

Specifically,

$$
\begin{aligned}
\mathbf{P}(X = 1 \mid Z = z) \;=\; p_{X|Z}(1 \mid z)
&\;=\; \frac{p_X(1) f_{Z|X}(z \mid 1)}{\sum_{k=0}^{1} p_X(k) f_{Z|X}(z \mid k)} \\[2mm]
&\;=\; \frac{p\,\tfrac{1}{2}\lambda e^{-\lambda|z-1|}}{(1-p)\tfrac{1}{2}\lambda e^{-\lambda|z+1|} + p\,\tfrac{1}{2}\lambda e^{-\lambda|z-1|}} \\[2mm]
&\;=\; \frac{p\,e^{-\lambda|z-1|}}{(1-p)e^{-\lambda|z+1|} + p\,e^{-\lambda|z-1|}} \\[2mm]
&\;=\; \frac{p\,e^{-\lambda|z-1|}}{(1-p)e^{-\lambda|z+1|} + p\,e^{-\lambda|z-1|}} \cdot \frac{e^{\lambda|z-1|}}{e^{\lambda|z-1|}} \\[2mm]
&\;=\; \frac{p}{(1-p)e^{-\lambda(|z+1|-|z-1|)} + p}
\end{aligned}
$$

[SOLUTION GAP: the step from $f_Y$ to $f_{Z|X}(z\mid x) = \tfrac12\lambda e^{-\lambda|z-x|}$ — i.e. that given $X=x$, $Z = x + Y$ is the Laplacian density shifted by $x$ — is used without comment.]

The final manipulations are to ease interpretations for $p \to 0^+$, $p \to 1^-$, $\lambda \to 0^+$, and $\lambda \to \infty$. Easily

$$\lim_{p \to 0^+} \mathbf{P}(X = 1 \mid Z = z) \;=\; 0 \qquad \text{and} \qquad \lim_{p \to 1^-} \mathbf{P}(X = 1 \mid Z = z) \;=\; 1;$$

these make sense because the observation $z$ should become unimportant when value of $X$ becomes certain without it. Next,

$$\lim_{\lambda \to 0^+} \mathbf{P}(X = 1 \mid Z = z) \;=\; p,$$

which makes sense because the distribution of $Y$ becomes very flat as $\lambda \to 0^+$, making the observation uninformative. Finally,

$$\lim_{\lambda \to \infty} \mathbf{P}(X = 1 \mid Z = z) \;=\;
\begin{cases} 1, & \text{if } |z+1| > |z-1|, \\ 0, & \text{if } |z+1| < |z-1|, \end{cases}
\;=\;
\begin{cases} 1, & \text{if } z > 0, \\ 0, & \text{if } z < 0; \end{cases}$$

this makes sense because $\lambda \to \infty$ makes the $Y$ negligible.

[SOLUTION GAP: the evaluation of $\lim_{\lambda\to\infty}$ of $(1-p)e^{-\lambda(|z+1|-|z-1|)}+p$ (namely that the exponential tends to $0$ or $\infty$ according to the sign of $|z+1|-|z-1|$) is not shown; nor is the equivalence $|z+1|>|z-1| \iff z>0$.]

---

## Problem 2 — Posterior PDF of a Bernoulli success probability (beta distribution)

### Statement

Let $Q$ be a continuous random variable with PDF

$$f_Q(q) \;=\; \begin{cases} 6q(1-q), & \text{if } 0 \le q \le 1, \\ 0, & \text{otherwise.} \end{cases}$$

This $Q$ represents the probability of success of a Bernoulli random variable $X$, i.e.,

$$\mathbf{P}(X = 1 \mid Q = q) \;=\; q.$$

Find $f_{Q|X}(q|x)$ for $x \in \{0, 1\}$ and all $q$.

### Official solution

We need to apply the version of Bayes rule for a continuous random variable conditioned on a discrete random variable:

$$f_{Q|X}(q \mid x) \;=\; \frac{f_Q(q) p_{X|Q}(x \mid q)}{p_X(x)} \;=\; \frac{f_Q(q) p_{X|Q}(x \mid q)}{\int_0^1 f_Q(q) p_{X|Q}(x \mid q)\, dq}.$$

For $x = 0$ and $q \in [0,1]$,

$$
\begin{aligned}
f_{Q|X}(q \mid 0) &\;=\; \frac{f_Q(q) p_{X|Q}(0 \mid q)}{\int_0^1 f_Q(q) p_{X|Q}(0 \mid q)\, dq} \;=\; \frac{6q(1-q)\cdot(1-q)}{\int_0^1 6q(1-q)(1-q)\, dq} \\[2mm]
&\;=\; \frac{6q(1-q)\cdot(1-q)}{1/2} \;=\; 12q(1-q)^2 .
\end{aligned}
$$

For $x = 1$ and $q \in [0,1]$,

$$
\begin{aligned}
f_{Q|X}(q \mid 1) &\;=\; \frac{f_Q(q) p_{X|Q}(1 \mid q)}{\int_0^1 f_Q(q) p_{X|Q}(1 \mid q)\, dq} \;=\; \frac{6q(1-q)\cdot q}{\int_0^1 6q(1-q)q\, dq} \\[2mm]
&\;=\; \frac{6q(1-q)\cdot q}{1/2} \;=\; 12q^2(1-q).
\end{aligned}
$$

The distributions $f_Q(q)$, $f_{Q|X}(q \mid 0)$, and $f_{Q|X}(q \mid 1)$ are all in the family of *beta distributions*, which arise again in Chapter 8.

[SOLUTION GAP: the two normalizing integrals are each stated to equal $1/2$ without evaluation; e.g. $\int_0^1 6q(1-q)^2 dq = 6(\tfrac12 - \tfrac23 + \tfrac14) = \tfrac12$ and $\int_0^1 6q^2(1-q)\,dq = 6(\tfrac13 - \tfrac14) = \tfrac12$.]

[SOLUTION GAP: the solution does not restate that $f_{Q|X}(q\mid x) = 0$ for $q \notin [0,1]$, although "for all $q$" was asked.]

---

## Problem 3 — Derived distribution of $Y = g(X)$ for standard normal $X$

### Statement

Let $X$ have the normal distribution with mean $0$ and variance $1$, i.e.,

$$f_X(x) \;=\; \frac{1}{\sqrt{2\pi}} e^{-x^2/2}.$$

Also, let $Y = g(X)$ where

$$g(t) \;=\; \begin{cases} -t, & \text{for } t \le 0; \\ \sqrt{t}, & \text{for } t > 0, \end{cases}$$

as shown to the right.

Find the probability density function of $Y$.

[FIGURE: Plot of $g(t)$ versus $t$ shown to the right of the problem statement. Horizontal axis labeled $t$, ticked at $-5$, $0$, $5$; vertical axis labeled $g(t)$, ticked at $0,1,2,3,4,5$. For $t \le 0$ the curve is the straight line $g(t) = -t$, descending from the value $5$ at $t=-5$ down to $0$ at $t=0$. For $t > 0$ the curve is the concave square-root branch $g(t) = \sqrt{t}$, rising from $0$ at $t=0$ to about $2.24$ at $t=5$. The two branches meet at the origin with a "V"-like kink (vertical tangent on the right branch at $0$). | raster/rec11_p01.png]

### Official solution

Because of the definition of $g$, the random variable $Y$ takes on only nonnegative values. Thus $f_Y(y) = 0$ for any negative $y$. For $y > 0$,

$$
\begin{aligned}
F_Y(y) &\;=\; \mathbf{P}(Y \le y) \\
&\;=\; \mathbf{P}\big(X \in [-y, 0]\big) + \mathbf{P}\big(X \in (0, y^2]\big) \\
&\;=\; \big(F_X(0) - F_X(-y)\big) + \big(F_X(y^2) - F_X(0)\big) \\
&\;=\; F_X(y^2) - F_X(-y).
\end{aligned}
$$

Taking the derivative of $F_Y(y)$ (and using the chain rule),

$$
\begin{aligned}
f_Y(y) &\;=\; 2y f_X(y^2) + f_X(-y) \\
&\;=\; \frac{1}{\sqrt{2\pi}}\left(2y e^{-y^4/2} + e^{-y^2/2}\right).
\end{aligned}
$$

[SOLUTION GAP: the inversion of the event $\{Y\le y\}$ into $\{X\in[-y,0]\}\cup\{X\in(0,y^2]\}$ (i.e. $-t \le y \iff t \ge -y$ on the left branch, and $\sqrt{t}\le y \iff t \le y^2$ on the right branch) is stated without derivation. Also the sign in the chain rule for $\frac{d}{dy}\big[-F_X(-y)\big] = +f_X(-y)$ is not shown explicitly.]

---

*(Both PDFs end with the standard MIT OpenCourseWare page: "MIT OpenCourseWare, http://ocw.mit.edu, 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010. For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.")*
