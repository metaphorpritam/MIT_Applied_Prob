# rec20 — Recitation 20 (November 18, 2010)

Covers: estimation of a Bernoulli parameter by the sample mean; Chebyshev's inequality and Markov's inequality; weak law of large numbers; convergence in probability; convergence in the mean square and its relation to convergence in probability; counterexamples with heavy-tailed two-point PMFs; convergence of transformed i.i.d. uniform sequences

Sources: `questions_44bcdd8261dedf60074b86706b946899_MIT6_041F10_rec20.pdf.md` (MIT6_041F10_rec20.pdf), `solutions_9623ab63ef49131a9509a56e07253970_MIT6_041F10_rec20_sol.pdf.md` (MIT6_041F10_rec20_sol.pdf)

Massachusetts Institute of Technology
Department of Electrical Engineering & Computer Science
6.041/6.431: Probabilistic Systems Analysis (Fall 2010)

---

## Problem 1 — Estimating lightbulb quality: sample mean, Chebyshev bound, sample size

### Statement

In your summer internship, you are working for the world's largest producer of lightbulbs. Your manager asks you to estimate the quality of production, that is, to estimate the probability $p$ that a bulb produced by the factory is defectless. You are told to assume that all lightbulbs have the same probability of having a defect, and that defects in different lightbulbs are independent.

(a) Suppose that you test $n$ randomly picked bulbs, what is a good estimate $Z_n$ for $p$, such that $Z_n$ converges to $p$ in probability?

(b) If you test 50 light bulbs, what is the probability that your estimate is in the range $p \pm 0.1$?

(c) The management asks that your estimate falls in the range $p \pm 0.1$ with probability 0.95. How many light bulbs do you need to test to meet this specification?

### Official solution

**(a)** Let $X_i$ be a random variable indicating the quality of the $i$th bulb ("1" for good bulbs, "0" for bad ones). $X_i$'s are independent Bernoulli random variables. Let $Z_n$ be

$$Z_n = \frac{X_1 + X_2 + \ldots + X_n}{n}.$$

$$\mathbf{E}[Z_n] = p \qquad \operatorname{var}(Z_n) = \frac{n\operatorname{var}(X_i)}{n^2} = \frac{\sigma^2}{n},$$

where $\sigma^2$ is the variance of $X_i$.

Applying Chebyshev's inequality yields,

$$\mathbf{P}\left(|Z_n - p| \ge \epsilon\right) \le \frac{\sigma^2}{n\epsilon^2},$$

As $n \to \infty$, $\dfrac{\sigma^2}{n\epsilon^2} \to 0$ and $\mathbf{P}\left(|Z_n - p| \ge \epsilon\right) \to 0$.

Hence, $Z_n$ converges to $p$ in probability.

**(b)** By Chebychev's inequality,

$$\mathbf{P}\left(|Z_{50} - p| \ge 0.1\right) \le \frac{\sigma^2}{50(0.1)^2},$$

Since $X_i$ is a Bernoulli random variable, its variance $\sigma^2$ is $p(1-p)$, which is less than or equal to $\frac{1}{4}$. Thus,

$$\mathbf{P}\left(|Z_{50} - p| \ge 0.1\right) \le \frac{1/4}{50(0.1)^2} = 0.5$$

[SOLUTION GAP: the question asks for the probability that the estimate *is* in the range $p \pm 0.1$; the solution only bounds the probability of the complementary event by 0.5 and never states the resulting conclusion $\mathbf{P}(|Z_{50}-p| < 0.1) \ge 0.5$. It also does not justify $\max_p p(1-p) = 1/4$.]

**(c)** By Chebychev's inequality,

$$\mathbf{P}\left(|Z_n - p| \ge 0.1\right) \le \frac{\sigma^2}{n\epsilon^2} \le \frac{1/4}{n(0.1^2)}$$

To guarantee a probability 0.95 of falling in the desired range,

$$\frac{1/4}{n(0.1)^2} < 0.05,$$

which yields $n \ge 500$. Note that $n \ge 500$ guarantees the accuracy specification even for the highest variance, namely $1/4$. For smaller variances, we need smaller values of $n$ to guarantee the desired accuracy. For example, if $\sigma^2 = 1/16$, $n \ge 125$ would suffice.

[SOLUTION GAP: the algebra from $\frac{1/4}{n(0.1)^2} < 0.05$ to the sample size is omitted, as is the check $\frac{1/16}{n(0.1)^2} < 0.05 \Rightarrow n \ge 125$.]

[SOURCE TYPO?: the strict inequality $\frac{1/4}{n(0.1)^2} < 0.05$ gives $n > 500$, whereas the stated conclusion is $n \ge 500$ (at $n = 500$ the bound equals exactly 0.05); the mixing of $<$ and $\ge$ is inconsistent.]

---

## Problem 2 — Two-point PMFs $X_n$, $Y_n$: Chebyshev, convergence in probability vs. mean square

### Statement

2.

[FIGURE: Two discrete PMF stem (line-spectrum) plots side by side, drawn on separate axes.
LEFT plot — vertical axis labelled $p_{X_n}(x)$, horizontal axis labelled $x$. Two impulses (vertical arrows/stems): one at $x = 0$ of height labelled $1 - \frac{1}{n}$ (the tall stem, drawn on the vertical axis itself), and one at $x = 1$ of height labelled $\frac{1}{n}$ (the short stem). Tick marks on the $x$-axis at 0 and 1.
RIGHT plot — vertical axis labelled $p_{Y_n}(y)$, horizontal axis labelled $y$. Two impulses: one at $y = 0$ of height labelled $1 - \frac{1}{n}$ (tall stem on the vertical axis), and one at $y = n$ of height labelled $\frac{1}{n}$ (short stem). Tick marks on the $y$-axis at 0 and $n$.
Both short stems are drawn at the same (lower) height $\frac{1}{n}$, and both tall stems at height $1-\frac{1}{n}$. | raster/rec20_p01.png]

Let $X_n$ and $Y_n$ have the distributions shown above.

That is:
$$p_{X_n}(x) = \begin{cases} 1 - \frac{1}{n}, & x = 0 \\ \frac{1}{n}, & x = 1 \end{cases} \qquad p_{Y_n}(y) = \begin{cases} 1 - \frac{1}{n}, & y = 0 \\ \frac{1}{n}, & y = n \end{cases}$$

(a) Find the expected value and variance of $X_n$ and $Y_n$.

(b) What does the Chebyshev inequality tell us about the convergence of $X_n$? $Y_n$?

(c) Is $Y_n$ convergent in probability? If so, to what value?

(d) If a sequence of random variables converges in probability to $a$, does the corresponding sequence of expected values converge to $a$? Prove or give a counter example.

A sequence of random variables is said to converge to a number $c$ in the **mean square**, if

$$\lim_{n \to \infty} \mathbf{E}\left[(X_n - c)^2\right] = 0.$$

(e) Use Markov's inequality to show that convergence in the mean square implies convergence in probability.

(f) Give an example that shows that convergence in probability does not imply convergence in the mean square.

### Official solution

**(a)**

$$\mathbf{E}[X_n] = 0 \cdot \left(1 - \frac{1}{n}\right) + 1 \cdot \frac{1}{n} = \frac{1}{n}$$

$$\operatorname{var}(X_n) = \left(0 - \frac{1}{n}\right)^2 \cdot \left(1 - \frac{1}{n}\right) + \left(1 - \frac{1}{n}\right)^2 \cdot \left(\frac{1}{n}\right) = \frac{n-1}{n^2}$$

$$\mathbf{E}[Y_n] = 0 \cdot \left(1 - \frac{1}{n}\right) + n \cdot \frac{1}{n} = 1$$

$$\operatorname{var}(Y_n) = (0 - 1)^2 \cdot \left(1 - \frac{1}{n}\right) + (n-1)^2 \cdot \left(\frac{1}{n}\right) = n - 1$$

[SOLUTION GAP: the intermediate algebraic simplifications leading to $\frac{n-1}{n^2}$ and to $n-1$ are not shown.]

**(b)** Using Chebyshev's inequality, we have

$$\lim_{n \to \infty} \mathbf{P}\left(\left|X_n - \frac{1}{n}\right| \ge \epsilon\right) \le \lim_{n \to \infty} \frac{n-1}{n^2 \epsilon^2} = 0$$

Moreover, $\displaystyle\lim_{n \to \infty} \frac{1}{n} = 0$.

It follows that $X_n$ converges to 0 in probability. For $Y_n$, Chebyshev suggests that,

$$\lim_{n \to \infty} \mathbf{P}\left(|Y_n - 1| \ge \epsilon\right) \le \lim_{n \to \infty} \frac{n-1}{\epsilon^2} = \infty,$$

Thus, we cannot conclude anything about the convergence of $Y_n$ through Chebychev's inequality.

[SOLUTION GAP: the step combining "$X_n - \frac{1}{n} \to 0$ in probability" with "$\frac{1}{n} \to 0$" to conclude "$X_n \to 0$ in probability" is asserted, not proved.]

**(c)** For every $\epsilon > 0$,

$$\lim_{n \to \infty} \mathbf{P}\left(|Y_n| \ge \epsilon\right) \le \lim_{n \to \infty} \frac{1}{n} = 0,$$

Thus, $Y_n$ converges to zero in probability.

[SOLUTION GAP: the bound $\mathbf{P}(|Y_n| \ge \epsilon) \le \frac{1}{n}$ is stated without justification — it comes directly from the PMF (for $n > \epsilon$, the only outcome with $|Y_n| \ge \epsilon$ is $Y_n = n$, of probability $\frac{1}{n}$), not from Chebyshev.]

**(d)** The statement is false. A counter example is $Y_n$. It converges in probability to 0 yet its expected value is 1 for all $n$.

**(e)** Using the Markov bound, we have

$$\mathbf{P}\left(|X_n - c| \ge \epsilon\right) = P\left(|X_n - c|^2 \ge \epsilon^2\right) \le \frac{\mathbf{E}\left[(X_n - c)^2\right]}{c^2}.$$

[SOURCE TYPO?: the Markov bound denominator should be $\epsilon^2$, not $c^2$ — Markov applied to the nonnegative r.v. $|X_n - c|^2$ at level $\epsilon^2$ gives $\mathbf{E}[(X_n-c)^2]/\epsilon^2$. The printed $c^2$ appears to be a typo.]

Taking the limit as $n \to \infty$, we obtain

$$\lim_{n \to \infty} \mathbf{P}\left(|X_n - c| \ge \epsilon\right) = 0,$$

which establishes convergence in probability.

[SOLUTION GAP: the final limit uses the hypothesis $\lim_{n\to\infty}\mathbf{E}[(X_n-c)^2] = 0$ without explicitly invoking it.]

**(f)** A counter example is $Y_n$. $Y_n$ converges to 0 in probability, but

$$\mathbf{E}\left[(Y_n - 0)^2\right] = 0 \cdot \left(1 - \frac{1}{n}\right) + (n^2) \cdot \frac{1}{n} = n$$

Thus,

$$\lim_{n \to \infty} \mathbf{E}\left[(Y_n - 0)^2\right] = \infty,$$

and $Y_n$ does not converge to 0 in the mean square.

---

## Problem 3 — Convergence in probability of $X_i$, $X_i/i$, $(X_i)^i$ for i.i.d. uniform $[-1,1]$

### Statement

Random variable $X$ is uniformly distributed between $-1.0$ and $1.0$. Let $X_1, X_2, \ldots$, be independent identically distributed random variables with the same distribution as $X$. Determine which, if any, of the following sequences (all with $i = 1, 2, \ldots$) are convergent in probability. Give reasons for your answers. Include the limits if they exist.

(a) $X_i$

(b) $Y_i = \dfrac{X_i}{i}$

(c) $Z_i = (X_i)^i$

### Official solution

**(a)** No. Since $X_i$ for any $i \ge 1$ is uniformly distributed between $-1.0$ and $1.0$.

[SOLUTION GAP: no formal argument is given — the reason is left as the bare observation that the distribution of $X_i$ does not change with $i$ and so cannot concentrate at any point.]

**(b)** Yes, to 0. Since for $\epsilon > 0$,

$$\begin{aligned}
\lim_{i \to \infty} \mathbf{P}\left(|Y_i - 0| > \epsilon\right) &= \lim_{i \to \infty} \mathbf{P}\left(\left|\frac{X_i}{i} - 0\right| > \epsilon\right) \\
&= \lim_{i \to \infty}\left[\mathbf{P}\left(X_i > i\epsilon\right) + \mathbf{P}\left(X_i < -i\epsilon\right)\right] = 0.
\end{aligned}$$

[SOLUTION GAP: the evaluation of the two tail probabilities is skipped — for $i\epsilon > 1$ both are exactly 0, which is why the limit is 0.]

**(c)** Yes, to 0. Since for $\epsilon > 0$,

$$\begin{aligned}
\lim_{i \to \infty} \mathbf{P}\left(|Z_i - 0| > \epsilon\right) &= \lim_{i \to \infty} \mathbf{P}\left(\left|(X_i)^i - 0\right| > \epsilon\right) \\
&= \lim_{i \to \infty}\left[\mathbf{P}\left(X_i > \epsilon^{\frac{1}{i}}\right) + \mathbf{P}\left(X_i < -(\epsilon)^{\frac{1}{i}}\right)\right] \\
&= \lim_{i \to \infty}\left[\frac{1}{2}\left(1 - \epsilon^{\frac{1}{i}}\right) + \frac{1}{2}\left(1 - \epsilon^{\frac{1}{i}}\right)\right] = \lim_{i \to \infty}\left(1 - \sqrt[i]{\epsilon}\right) \\
&= 0.
\end{aligned}$$

[SOLUTION GAP: the step $\mathbf{P}(X_i > \epsilon^{1/i}) = \frac{1}{2}(1 - \epsilon^{1/i})$ uses the uniform-$[-1,1]$ CDF without showing it, and the final limit $\epsilon^{1/i} \to 1$ is not justified.]

[SOURCE TYPO?: the decomposition of $\{|(X_i)^i| > \epsilon\}$ into $\{X_i > \epsilon^{1/i}\} \cup \{X_i < -\epsilon^{1/i}\}$ ignores the parity of $i$: for even $i$, $(X_i)^i \ge 0$ and the event is still correctly $\{|X_i| > \epsilon^{1/i}\}$, so the numerical answer is unaffected, but the written justification implicitly treats $|(X_i)^i| > \epsilon$ as $(X_i)^i > \epsilon$ or $(X_i)^i < -\epsilon$. Also, the argument as written requires $0 < \epsilon < 1$ (for $\epsilon \ge 1$ the probabilities are 0 anyway); the case is not discussed.]

---

*(Both PDFs end with the standard MIT OpenCourseWare page: "MIT OpenCourseWare, http://ocw.mit.edu, 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010. For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.")*
