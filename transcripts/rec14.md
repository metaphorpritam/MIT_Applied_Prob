# rec14 — Recitation 14 (October 26, 2010)

Covers: Bernoulli process; geometric random variables (mean and variance); merging of independent Bernoulli processes; Pascal (k-th order) PMF; shifted geometric; random sums (law of total expectation/variance for a random number of terms); coupon-collector expected value via sum of geometrics and harmonic-sum asymptotics.

Sources: `MIT6_041F10_rec14.pdf` (questions), `MIT6_041F10_rec14_sol.pdf` (solutions)

Course header (both PDFs): Massachusetts Institute of Technology, Department of Electrical Engineering & Computer Science, 6.041/6.431: Probabilistic Systems Analysis (Fall 2010).

---

## Problem 1 — Mosquito and tick bites (Bernoulli processes and merging)

### Statement

You are visiting the rainforest, but unfortunately your insect repellent has run out. As a result, at each second, a mosquito lands on your neck with probability 0.5. If one lands, with probability 0.2 it bites you, and with probability 0.8 it never bothers you, independently of other mosquitoes.

**(a)** What is the expected time between successive mosquito bites? What is the variance of the time between successive mosquito bites?

**(b)** In addition, a tick lands on your neck with probability 0.1. If one lands, with probability 0.7 it bites you, and with probability 0.3, it never bothers you, independently of other ticks and mosquitoes. Now, what is expected time between successive bug bites? What is the variance of the time between successive bug bites?

### Official solution

**(a)** Let $X = $ (time between successive mosquito bites) $=$ (time until the next mosquito bite).

The mosquito bites occur according to a Bernoulli process with parameter $p = 0.5 \cdot 0.2 = 0.1$. $X$ is a geometric random variable, so,

$$\mathbf{E}[X] = \frac{1}{p} = \frac{1}{0.1} = 10.$$

$$\mathrm{var}(X) = \frac{1-p}{p^2} = \frac{1-0.1}{0.1^2} = 90.$$

**(b)** Mosquito bites occur according to a Bernoulli process with parameter $p = 0.1$. Tick bites occur according to another independent Bernoulli process with parameter $q = 0.1 \cdot 0.7 = 0.07$. Bug bites (mosquito or tick) occur according to a merged Bernoulli process from the mosquito and tick processes. Therefore, the probability of success at any time point for the merged Bernoulli process is

$$r = p + q - pq = 0.1 + 0.07 - 0.1 \cdot 0.07 = 0.163.$$

Let $Y$ be the time between successive bug bites. As before, $Y$ is a geometric random variable, so

$$\mathbf{E}[Y] = \frac{1}{r} = \frac{1}{0.163} \approx 6.135.$$

$$\mathrm{var}(Y) = \frac{1-r}{r^2} = \frac{1-0.163}{0.163^2} \approx 31.503$$

---

## Problem 2 — Al's and Bob's coin-flipping trials

### Statement

Al performs an experiment comprising a series of independent trials. On each trial, he simultaneously flips a set of three fair coins.

**(a)** Given that Al has just had a trial with 3 *tails*, what is the probability that both of the next two trials will also have this result?

**(b)** Whenever all three coins land on the same side in any given trial, Al calls the trial a success.

&nbsp;&nbsp;&nbsp;&nbsp;**i.** Find the PMF for $K$, the number of trials up to, but *not* including, the second success.

&nbsp;&nbsp;&nbsp;&nbsp;**ii.** Find the expectation and variance of $M$, the number of tails that occur *before* the first success.

**(c)** Bob conducts an experiment like Al's, except that he uses 4 coins for the first trial, and then he obeys the following rule: Whenever all of the coins land on the same side in a trial, Bob permanently removes one coin from the experiment and continues with the trials. He follows this rule until the *third* time he removes a coin, at which point the experiment ceases. Find $E[N]$, where $N$ is the number of trials in Bob's experiment.

### Official solution

**(a)** In this case, since the trials are independent, the given information is irrelevant.

$$\mathbf{P}(\text{next 2 trials result in 3 tails}) = \left(\tfrac{1}{8}\right)^2 = \tfrac{1}{64}.$$

**(b) i.** The second order Pascal PMF for random variable $N$, as defined in the text, is the probability of the second success comes on the $n^{th}$ trial. Thus, the random variable, $K$, is a shifted version of the second order Pascal PMF, i.e. $K = N - 1$. So, the probability that 1 success comes in the first $k$ trials, where the next trial will result in the second success, can be expressed as:

$$p_K(k) = \binom{k}{1}\left(\frac{1}{4}\right)^{2}\left(\frac{3}{4}\right)^{k-1}, \quad k \ge 1.$$

[SOLUTION GAP: the success probability $1/4$ (= P(all three coins same side) = $2/8$) is never computed explicitly; it appears directly in the PMF.]

[SOURCE TYPO?: the sentence "the probability of the second success comes on the $n^{th}$ trial" is ungrammatical (should read "the probability that the second success comes on the $n$th trial"). Also, "the probability that 1 success comes in the first $k$ trials, where the next trial will result in the second success" describes exactly one success in the first $k$ trials; the wording "1 success comes in the first $k$ trials" is loose.]

**ii.** The number of tails before the first success, $M$, can be written as a random sum:

$$M = X_1 + X_2 + \cdots + X_N,$$

where $X_i$ is the number of tails that occur on (unsuccessful) trial $i$, and $N$ is the number of unsuccessful trials (i.e. trials before the first success). We notice that $X$ is equally likely to be either 1 or 2, and that $N$ is a shifted geometric: $N = R - 1$, where $R$ is a geometric random variable with parameter $\frac{1}{4}$. Now we can apply our random sum formulae.

$$E[M] = E[X]E[N] = \left(\frac{3}{2}\right)(4-1) = \frac{9}{2}$$

$$\mathrm{var}(M) = E[N]\,\mathrm{var}(X) + (E[X])^2\,\mathrm{var}(N) = (4-1)\left(\frac{1}{4}\right) + \left(\frac{3}{2}\right)^{2}(12) = \frac{111}{4}.$$

[SOLUTION GAP: the numbers $E[X] = 3/2$, $\mathrm{var}(X) = 1/4$ (for $X$ uniform on $\{1,2\}$) and $\mathrm{var}(N) = \mathrm{var}(R) = (1-p)/p^2 = 12$ are inserted without derivation; only $E[N] = 4-1 = 3$ is shown arithmetically. The final arithmetic $3/4 + 27 = 111/4$ is also not shown.]

**(c)** $N$, the number of trials in Bob's experiment, can be expressed as the sum of 3 independent random variables, $X$, $Y$, and $Z$. $X$ is the number of trials until Bob removes the first coin, $Y$ the number of additional trials until he removes the second coin, and $Z$ the additional number until he removes the third coin. We see that $X$ is a geometric random variable with parameter $\frac{1}{8}$, $Y$ is geometric with parameter $\frac{1}{4}$, and $Z$ geometric with parameter $\frac{1}{2}$. Hence,

$$E[N] = E[X] + E[Y] + E[Z] = 8 + 4 + 2 = 14.$$

[SOLUTION GAP: the parameters $1/8$, $1/4$, $1/2$ are stated without showing that P(all $m$ coins same side) $= 2/2^m$ for $m = 4, 3, 2$ coins respectively.]

---

## Problem 3 — Signing $n$ papers drawn with replacement (coupon collector)

### Statement

Suppose there are $n$ papers in a drawer. You draw a paper and sign it, and then, instead of filing it away, you place the paper back into the drawer. If any paper is equally likely to be drawn each time, independent of all other draws, what is the expected number of papers that you will draw before signing all $n$ papers? You may leave your answer in the form of a summation.

### Official solution

Let $M$ be the total number of draws you make until you have signed all $n$ papers. Let $T_i$ be the number of draws you make until drawing the next unsigned paper after having signed $i$ papers. Then $M = T_0 + \cdots + T_{n-1}$.

We can view the process of selecting the next unsigned paper after having signed $i$ papers as a sequence of independent Bernoulli trials with probability of success $p_i = \frac{n-i}{n}$, since there are $n-i$ unsigned papers out of a total of $n$ papers and receiving any paper is equally likely in a particular draw. The PMF governing the number of attempts we make until we succeed in drawing the next unsigned paper after having signed $i$ papers is geometric. More concretely, the probability that it takes $k$ tries to draw the next unsigned paper after having signed $i$ papers is

$$\mathbf{P}(T_i = k) = (1 - p_i)^{k-1} p_i.$$

With this model, the expected value of $M$, the number of draws you make until you sign all $n$ papers is:

$$\mathbf{E}[M] = \mathbf{E}\left[\sum_{i=0}^{n-1} T_i\right] = \sum_{i=0}^{n-1} \mathbf{E}[T_i] = \sum_{i=0}^{n-1} \frac{n}{n-i} = n \sum_{k=1}^{n} \frac{1}{k}.$$

For large $n$, this is on the order of: $n \int_1^n \frac{1}{x}\,dx = n \log n$.

[SOLUTION GAP: the step $\mathbf{E}[T_i] = 1/p_i = n/(n-i)$ is used implicitly (geometric mean), and the re-indexing $k = n - i$ that turns $\sum_{i=0}^{n-1} n/(n-i)$ into $n\sum_{k=1}^n 1/k$ is not shown. The asymptotic statement uses $\int_1^n dx/x = \log n$ without comment on the harmonic-sum approximation.]

---

## Figures

No figures, plots, diagrams, or trees appear in either the question PDF or the solution PDF. Page `raster/rec14_p02.png` and page `raster/rec14_sol_p03.png` are the standard MIT OpenCourseWare boilerplate pages (MIT OpenCourseWare, http://ocw.mit.edu, "6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010", terms-of-use link) and contain no problem content.
