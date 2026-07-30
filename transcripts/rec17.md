# rec17 — Recitation 17 (November 4, 2010)

Covers: Poisson processes (conscious/subconscious response streams), Poisson PMF over an interval, competing/merged Poisson processes, Poisson splitting and thinning, sums of independent exponentials (convolution → hypoexponential / Erlang), geometric and shifted-geometric PMFs, memorylessness, random incidence in an Erlang arrival process

Sources: MIT6_041F10_rec17.pdf (questions), MIT6_041F10_rec17_sol.pdf (solutions)

Header block on both PDFs: Massachusetts Institute of Technology, Department of Electrical Engineering & Computer Science, 6.041/6.431: Probabilistic Systems Analysis (Fall 2010).

Footer on question sheet: "Textbook problems are courtesy of Athena Scientific, and are used with permission."

---

## Problem 1 — Iwana Passe: conscious and subconscious Poisson response streams

### Statement

Iwana Passe is taking a multiple-choice exam. You may assume that the number of questions is infinite. *Simultaneously, but independently,* her conscious and subconscious faculties are generating answers for her, each in a Poisson manner. (Her conscious and subconscious are always working on different questions.) Conscious responses are generated at the rate $\lambda_c$ responses per minute. Subconscious responses are generated at the rate $\lambda_s$ responses per minute. Assume $\lambda_c \neq \lambda_s$. Each conscious response is an independent Bernoulli trial with probability $p_c$ of being correct. Similarly, each subconscious response is an independent Bernoulli trial with probability $p_s$ of being correct. Iwana responds only once to each question, and you can assume that her time for recording these conscious and subconscious responses is negligible.

(a) Determine $p_K(k)$, the probability mass function for the number of *conscious responses* Iwana makes in an interval of $T$ minutes.

(b) If we pick any question to which Iwana has responded, what is the probability that her answer to that question:

&nbsp;&nbsp;&nbsp;&nbsp;i. Represents a conscious response

&nbsp;&nbsp;&nbsp;&nbsp;ii. Represents a conscious correct response

(c) If we pick an interval of $T$ minutes, what is the probability that in that interval Iwana will make exactly $r$ conscious responses *and* $s$ subconscious responses?

(d) Determine the probability density function for random variable $X$, where $X$ is the time from the start of the exam until Iwana makes her first conscious response which is preceded by at least one subconscious response.

### Official solution

**(a)** $K$ has a Poisson distribution with average arrival time $\mu = \lambda_c T$

$$p_K(k) = \frac{(\lambda_c T)^k e^{-\lambda_c T}}{k!}, \quad k = 0, 1, 2, \ldots ; \; T \geq 0.$$

[SOURCE TYPO?: the source says "average arrival time $\mu = \lambda_c T$"; $\lambda_c T$ is the average *number of arrivals* (the Poisson mean), not a time.]

**(b)** i. $\mathbf{P}(\text{conscious response}) = \left(\dfrac{\lambda_c}{\lambda_c + \lambda_s}\right).$

ii. $\mathbf{P}(\text{conscious correct response}) = \mathbf{P}(\text{conscious resp})\,\mathbf{P}(\text{correct resp} \mid \text{conscious resp}) = \left(\dfrac{\lambda_c}{\lambda_c + \lambda_s} p_c\right).$

[SOLUTION GAP: part (b)i states the merged-Poisson competition result $\lambda_c/(\lambda_c+\lambda_s)$ without deriving it (e.g. via $\mathbf{P}(X_c < X_s)$ for independent exponentials, or via the splitting property of a merged Poisson process).]

**(c)** Since the conscious and subconscious responses are generated independently,

$$\mathbf{P}(r \text{ conscious responses and } s \text{ subconscious responses in interval } T)$$
$$= \mathbf{P}(r \text{ conscious responses in } T)\,\mathbf{P}(s \text{ unconscious responses in } T)$$
$$= \frac{(\lambda_c T)^r e^{-\lambda_c T}}{r!} \cdot \frac{(\lambda_s T)^s e^{-\lambda_s T}}{s!}$$

[SOURCE TYPO?: the middle line writes "$s$ unconscious responses" where the problem says *subconscious*.]

**(d)** Let $X_s =$ the time from the start of the exam to the time of the 1st subconscious response, and $X_c =$ the time from the 1st subconscious response to the time of the next conscious response.

Note that $X_s$ and $X_c$ are independent exponentially distributed random variables with parameters $\lambda_s$ and $\lambda_c$, respectively.

$$
\begin{aligned}
f_{X_s}(x_s) &= \lambda_s e^{-\lambda_s x_s} \text{ when } x_s \geq 0\\
&= 0 \text{ otherwise}\\
f_{X_c}(x_c) &= \lambda_c e^{-\lambda_c x_c} \text{ when } x_c \geq 0\\
&= 0 \text{ otherwise}
\end{aligned}
$$

$X = X_s + X_c$. So its PDF is the convolution of the two exponential distributions. For $x \geq 0$

$$
\begin{aligned}
f_X(x) &= \int_{-\infty}^{\infty} \lambda_s e^{-\lambda_s(x - x_c)} \lambda_c e^{-\lambda_c x_c}\, dx_c\\
&= \int_0^x \lambda_s \lambda_c e^{-\lambda_s x} e^{(\lambda_s - \lambda_c) x_c}\, dx_c \quad \text{because } x - x_c > 0\\
&= \lambda_s \lambda_c e^{-\lambda_s x} \int_0^x e^{(\lambda_s - \lambda_c) x_c}\, dx_c\\
&= \frac{\lambda_s \lambda_c}{\lambda_s - \lambda_c} e^{-\lambda_s x}\left(e^{(\lambda_s - \lambda_c)x} - 1\right) \quad \text{because } \lambda_s \neq \lambda_c\\
&= \frac{\lambda_s \lambda_c}{\lambda_s - \lambda_c}\left(e^{-\lambda_c x} - e^{-\lambda_s x}\right)
\end{aligned}
$$

[SOLUTION GAP: the step from the first integral to the second silently applies the limits — the integrand is nonzero only for $0 \le x_c \le x$ (needing $x_c \ge 0$ and $x - x_c \ge 0$); the source justifies it only with the parenthetical "because $x - x_c > 0$". The evaluation of $\int_0^x e^{(\lambda_s-\lambda_c)x_c} dx_c = \frac{e^{(\lambda_s-\lambda_c)x} - 1}{\lambda_s - \lambda_c}$ is also done in one line.]

[SOLUTION GAP: the solution never remarks that this interpretation of "first conscious response preceded by at least one subconscious response" relies on the memoryless/fresh-start property at the instant of the 1st subconscious response, which makes $X_c$ exponential($\lambda_c$) and independent of $X_s$.]

---

## Problem 2 — Shem the policeman: accidents, radio calls, merging and splitting

### Statement

Shem, a local policeman, drives from intersection to intersection in times that are independent and all exponentially distributed with parameter $\lambda$. At each intersection he observes (and reports) a car accident with probability $p$. (This activity does not slow his driving at all.) Independently of all else, Shem receives extremely brief radio calls in a Poisson manner with an average rate of $\mu$ calls per hour.

(a) Determine the PMF for $N$, the number of intersections Shem visits up to and including the one where he reports his first accident.

(b) Determine the PDF for $Q$, the length of time Shem drives between reporting accidents.

(c) What is the PMF for $M$, the number of accidents which Shem reports in two hours?

(d) What is the PMF for $K$, the number of accidents Shem reports between his receipt of two successive radio calls?

(e) We observe Shem at a random instant long after his shift has begun. Let $W$ be the total time from Shem's last radio call until his next radio call. What is the PDF of $W$?

### Official solution

**(a)** Since we are looking for the number of "trials" up to and including the first "success," $N$ is a geometric random variable with parameter $p$.

$$p_N(n) = (1 - p)^{n-1} p, \quad n \geq 1.$$

**(b)** The length of time spent driving to each intersection is exponentially distributed with parameter $\lambda$. Since the probability of Shem observing an accident at a given intersection is $p$, the distribution of the length of time in between accident reports is exponential but with parameter $p\lambda$ (think of Poisson splitting). Thus,

$$f_Q(q) = (p\lambda) e^{-q p \lambda}, \quad q \geq 0.$$

[SOLUTION GAP: the splitting claim is asserted, not derived — no argument is given that a Bernoulli($p$) thinning of a Poisson($\lambda$) process yields a Poisson($p\lambda$) process.]

**(c)** Since the interarrival time of accidents is exponentially distributed with parameter $p\lambda$, the number of arrivals in a given amount of time $\tau$ is a Poisson random variable with parameter $p\lambda\tau$. Thus,

$$\mathbf{P}(m \text{ arrivals in 2 hours}) = p_M(m) = \frac{e^{-2p\lambda}(2p\lambda)^m}{m!}, \quad m \geq 0.$$

**(d)** We can view the radio calls to Shem and the accident reports as independent Poisson processes with arrival rates $\mu$ and $p\lambda$, respectively. When the two independent Poisson processes are joined, the resultant is a Poisson process with arrival rate $\mu + p\lambda$. Furthermore, the probability of an arrival from the radio calls is $\dfrac{\mu}{\mu + p\lambda}$. Since we are interested in the number of reported accidents between two radio calls, we can view this is a shifted Geometric random variable with parameter $\dfrac{\mu}{\mu + p\lambda}$. Thus,

$$p_K(k) = \left(\frac{p\lambda}{\mu + p\lambda}\right)^k \left(\frac{\mu}{\mu + p\lambda}\right), \quad k \geq 0.$$

[SOURCE TYPO?: "we can view this is a shifted Geometric random variable" — "is" should read "as".]

**(e)** If we begin to observe Shem's radio calls at some random instant in time, due to the memoryless property of Poisson interarrivals, the distribution until he recieves the next call will still be exponential with parameter $\mu$. Also, the time from the previous call until the point at which we begin to observe Shem is also an exponential distribution with parameter $\mu$. Thus, $W = X_1 + X_2$, where $X_1$ and $X_2$ have exponential distributions, i.e. $W$ is a second order Erlang PDF.

$$f_W(w) = (\mu)^2 w e^{-w\mu}$$

[SOURCE TYPO?: "recieves" is misspelled in the source (should be "receives").]

[SOLUTION GAP: no range is stated for $f_W(w)$ (implicitly $w \geq 0$), and the backward-time exponential claim (time since the last call is also exponential($\mu$)) is asserted without justification.]

---

## Problem 3 — Random incidence in an Erlang arrival process (textbook 6.27)

### Statement

Problem 6.27, page 337 in the textbook. **Random incidence in an Erlang arrival process.** Consider an arrival process in which the interarrival times are independent Erlang random variables or order 2, with mean $2/\lambda$. Assume that the arrival process has been ongoing for a very long time. An external observer arrives at a given time $t$. Find the PDF of the length of the interarrival interval that contains $t$.

[SOURCE TYPO?: "Erlang random variables or order 2" — should be "of order 2".]

### Official solution

3. See problem 6.27, page 337 in the textbook.

[SOLUTION GAP: the entire solution is omitted and delegated to the textbook. No derivation of the length-biased (random incidence) density is provided in this handout.]

---

## Notes on figures

No figures, diagrams, trees, or plots appear in either the question sheet or the solution sheet for rec17 — both documents are pure text and displayed equations.

## Back-matter (both PDFs)

MIT OpenCourseWare, http://ocw.mit.edu — 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010. For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.
