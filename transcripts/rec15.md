# rec15 — Recitation 15 (October 28, 2010)

Covers: Exponential random variables and memorylessness; mixtures of exponentials (total probability / total expectation); Erlang distribution; Poisson processes — merging, splitting, competing processes; sum of a random number of random variables (mean and variance); binomial and geometric PMFs arising from Poisson splitting.

Sources: MIT6_041F10_rec15.pdf (questions), MIT6_041F10_rec15_sol.pdf (solutions)

Header block on every page: Massachusetts Institute of Technology, Department of Electrical Engineering & Computer Science, 6.041/6.431: Probabilistic Systems Analysis (Fall 2010).

Footnote on question page: "Textbook problems are courtesy of Athena Scientific, and are used with permission."

No figures, plots, diagrams, or trees appear anywhere in either document.

---

## Problem 1 — Type-A / type-B light bulbs (Text problem 6.14)

### Statement

1. Problem 6.14 (a)-(c),(h)-(j), page 330 in text.

[SOURCE TYPO?: The heading says parts "(a)-(c),(h)-(j)" of textbook problem 6.14, but the parts actually reproduced and lettered below run (a) through (f). The textbook's parts (h)-(j) have evidently been re-lettered (d)-(f) here.]

Beginning at time $t = 0$, we begin using bulbs, one at a time, to illuminate a room. Bulbs are replaced immediately upon failure. Each new bulb is selected independently by an equally likely choice between a type-A bulb and a type-B bulb. The lifetime, $X$, of any particular bulb of a particular type is a random variable, independent of everything else, with the following PDF:

$$\text{for type-A Bulbs:}\quad f_X(x) = \begin{cases} e^{-x}, & x \ge 0, \\ 0, & \text{otherwise;} \end{cases}$$

$$\text{for type-B Bulbs:}\quad f_X(x) = \begin{cases} 3e^{-3x}, & x \ge 0, \\ 0, & \text{otherwise.} \end{cases}$$

(a) Find the expected time until the first failure.

(b) Find the probability that there are no bulb failures before time $t$.

(c) Given that there are no failures until time $t$, determine the conditional probability that the first bulb used is a type-A bulb.

(d) Determine the probability that the total period of illumination provided by the first two type-B bulbs is longer than that provided by the first type-A bulb.

(e) Suppose the process terminates as soon as a total of exactly 12 bulb failures have occurred. Determine the expected value and variance of the total period of illumination provided by type-B bulbs while the process is in operation.

(f) Given that there are no failures until time $t$, find the expected value of the time until the first failure.

### Official solution

**(a)** Let $X$ be the time until the first bulb failure. Let $A$ (respectively, $B$) be the event that the frist bulb is of type $A$ (respectively, $B$). Since the two bulb types are equally likely, the total expectation theorem yields

$$\mathbf{E}[X] = \mathbf{E}[X|A]\mathbf{P}(A) + \mathbf{E}[X|B]\mathbf{P}(B) = 1 \cdot \frac{1}{2} + \frac{1}{3} \cdot \frac{1}{2} = \frac{2}{3}.$$

[SOURCE TYPO?: "the frist bulb" — should read "the first bulb".]

**(b)** Let $D$ be the event of no bulb failures before time $t$. Using the total probability theorem, and the exponential distributions for bulbs of the two types, we obtain

$$\mathbf{P}(D) = \mathbf{P}(D|A)\mathbf{P}(A) + \mathbf{P}(D|B)\mathbf{P}(B) = \frac{1}{2}e^{-t} + \frac{1}{2}e^{-3t}.$$

**(c)** We have

$$\mathbf{P}(A|D) = \frac{\mathbf{P}(A \cap D)}{\mathbf{P}(D)} = \frac{\frac{1}{2}e^{-t}}{\frac{1}{2}e^{-t} + \frac{1}{2}e^{-3t}} = \frac{1}{1 + e^{-2t}}.$$

**(d)** The lifetime of the first type-A bulb is $X_A$, with PDF given by:

$$f_{X_A}(x) = \begin{cases} e^{-x} & x \ge 0 \\ 0 & \text{elsewhere} \end{cases}$$

Let $Y$ be the total lifetime of two type-B bulbs. Because the lifetime of each type-B bulb is exponential with $\lambda = 3$, the sum $Y$ has an Erlang distribution of order 2 with $\lambda = 3$. Its PDF is:

$$f_Y(y) = \begin{cases} 9ye^{-3y} & y \ge 0 \\ 0 & \text{elsewhere} \end{cases}$$

$$
\begin{aligned}
P(G) &= P(Y \ge X_A) \\
&= \int_{-\infty}^{\infty} f_Y(y) \int_{-\infty}^{y} f_{X_A}(x)\,dx\,dy \\
&= \int_{0}^{\infty} 9ye^{-3y} \int_{0}^{y} e^{-x}\,dx\,dy = 9\int_{0}^{\infty} ye^{-3y} - e^{-x}\Big|_{x=0}^{x=y}\, dy \\
&= 9\int_{0}^{\infty} ye^{-3y}(1 - e^{-y})\,dy = 9\int_{0}^{\infty} ye^{-3y} - ye^{-4y}\,dy \\
&= 9\left(-\frac{1}{3}ye^{-3y} - \frac{1}{9}e^{-3y} + \frac{1}{4}ye^{-4y} + \frac{1}{16}e^{-4y}\right)\Big|_{y=0}^{y=\infty} \\
&= 9\left(\frac{1}{9} - \frac{1}{16}\right) = \frac{7}{16}
\end{aligned}
$$

[SOURCE TYPO?: the event $G$ is used ($P(G) = P(Y \ge X_A)$) but is never defined anywhere in the solution; from context $G = \{Y \ge X_A\}$, the event that the first two type-B bulbs together outlast the first type-A bulb. Also note the strict/non-strict mismatch: the problem asks for "longer than" ($Y > X_A$) while the solution computes $P(Y \ge X_A)$ — immaterial for continuous random variables.]

[SOURCE TYPO?: the third displayed line is typeset literally as $9\int_0^\infty ye^{-3y} - e^{-x}\big|_{x=0}^{x=y}\,dy$, i.e. the factor $ye^{-3y}$ and the evaluated antiderivative $-e^{-x}\big|_{x=0}^{x=y}$ are juxtaposed without parentheses, so it reads as a difference rather than the intended product $9\int_0^\infty ye^{-3y}\left(-e^{-x}\right)\big|_{x=0}^{x=y}\,dy$.]

[SOLUTION GAP: the antiderivative of $ye^{-3y} - ye^{-4y}$ is written down without showing the integration-by-parts work, and the evaluation of the bracket at $y = 0$ and $y \to \infty$ (giving $0 - (-\frac{1}{9} + \frac{1}{16})$) is not displayed.]

A simpler solution involving no integrals is as follows:

The bulb failure times of interest (1st type-$A$, 2nd type-$B$) may be thought of as the arrival times of two independent Poisson processes of rate $\lambda_A = 1$ and $\lambda_B = 3$. We may imagine that these two processes were split from a joint Poisson process of rate $\lambda_A + \lambda_B$, where the splitting probabilities for each arrival are $P(A) = \frac{\lambda_A}{\lambda_A + \lambda_B} = 1/4$ to process $A$ and $P(B) = \frac{\lambda_B}{\lambda_A + \lambda_B} = 3/4$ to process $B$. Now we may just focus on whether arrivals to the joint process go to process $A$ or to process $B$. Each arrival to the joint process corresponds to an independent trial. There are two possible outcomes: the arrival is handed to process A with probability $P(A)$ or the arrival is handed to process B with probability $P(B)$. Then our event of interest occurs when either the first arrival goes to A, or the first arrival goes to B followed by the second going to A. So the corresponding probability is

$$P(A \text{ or } BA) = P(A) + P(BA) = P(A) + P(B)P(A) = 7/16$$

[SOLUTION GAP: the numeric substitution $\frac{1}{4} + \frac{3}{4}\cdot\frac{1}{4} = \frac{7}{16}$ is not shown.]

**(e)** Let $V$ be the total period of illumination provided by type-B bulbs while the process is in operation. Let $N$ be the number of light bulbs, out of the first 12, that are of type-B. Let $X_i$ be the period of illumination from the $i$th type-B bulb. We then have $V = Y_1 + \cdots Y_N$. Note that $N$ is a binomial random variable, with parameters $n = 12$ and $p = 1/2$, so that

$$\mathbf{E}[N] = 6, \qquad \mathrm{var}(N) = 12 \cdot \frac{1}{2} \cdot \frac{1}{2} = 3.$$

[SOURCE TYPO?: the summands are defined as $X_i$ but the sum is written $V = Y_1 + \cdots Y_N$; the $Y$'s should be $X$'s. Also the summation is written without a final "+" before $Y_N$.]

Furthermore, $\mathbf{E}[X_i] = 1/3$ and $\mathrm{var}(X_i) = 1/9$. Using the formulas for the mean and variance of the sum of a random number of random variables, we obtain

$$\mathbf{E}[V] = \mathbf{E}[N]\mathbf{E}[X_i] = 2,$$

and

$$\mathrm{var}(V) = \mathrm{var}(X_i)\mathbf{E}[N] + (\mathbf{E}[X_i])^2\mathrm{var}(N) = \frac{1}{9}\cdot 6 + \frac{1}{9}\cdot 3 = 1$$

**(f)** Using the notation in parts (a)-(c), and the result of part (c), we have

$$
\begin{aligned}
\mathbf{E}[T|D] &= t + \mathbf{E}[T - t|D \cap A]\mathbf{P}(A|D) + \mathbf{E}[T - t|D \cap B]\mathbf{P}(B|D) \\
&= t + 1 \cdot \frac{1}{1 + e^{-2t}} + \frac{1}{3}\left(1 - \frac{1}{1 + e^{-2t}}\right) \\
&= t + \frac{1}{3} + \frac{2}{3}\cdot\frac{1}{1 + e^{-2t}}.
\end{aligned}
$$

[SOURCE TYPO?: the random variable is called $T$ here, whereas in parts (a)-(c) the time until the first failure was called $X$.]

[SOLUTION GAP: the memorylessness argument justifying $\mathbf{E}[T - t \mid D \cap A] = 1$ and $\mathbf{E}[T - t \mid D \cap B] = 1/3$ is not stated, and the algebra combining $\frac{1}{1+e^{-2t}} + \frac{1}{3} - \frac{1}{3}\cdot\frac{1}{1+e^{-2t}}$ into $\frac{1}{3} + \frac{2}{3}\cdot\frac{1}{1+e^{-2t}}$ is not shown.]

---

## Problem 2 — Service station with type A and type B jobs (Text problem 6.15)

### Statement

2. Problem 6.15 (a)-(c), p. 331 in text.

A service station handles jobs of two types, A and B. (Multiple jobs can be processed simultaneously.) Arrivals of the two job types are independent Poisson processes with parameters $\lambda_A = 3$ and $\lambda_B = 4$ per minute, respectively. Type A jobs stay in the service station for exactly one minute. Each type B job stays in the service station for a random but integer amount of time which is geometrically distributed, with mean equal to 2, and independent of everything else. The service station started operating at some time in the remote past.

(a) What is the mean, variance, and PMF of the total number of jobs that arrive within a given three-minute interval?

(b) We are told that during a 10-minute interval, exactly 10 new jobs arrived. What is the probability that exactly 3 of them are of type A?

(c) At time 0, no job is present in the service station. What is the PMF of the number of type B jobs that arrive in the future, but before the first type A arrival?

### Official solution

**(a)** The total arrival process corresponds to the merging of two independent Poisson processes, and is therefore Poisson with rate $\lambda = \lambda_A + \lambda_B = 7$. Thus, the number $N$ of jobs that arrive in a given three-minute interval is a Poisson random variable, with $\mathbf{E}[N] = 3\lambda = 21$, $\mathrm{var}(N) = 21$, and PMF

$$p_N(n) = \frac{(21)^n e^{-21}}{n!}, \qquad n = 0, 1, 2, \ldots.$$

**(b)** Each of these 10 jobs has probability $\lambda_A/(\lambda_A + \lambda_B) = 3/7$ of being type A, independently of the others. Thus, the binomial PMF applies and the desired probability is equal to

$$\binom{10}{3}\left(\frac{3}{7}\right)^3\left(\frac{4}{7}\right)^7$$

**(c)** Each future arrival is of type A with probability $\lambda_A/(\lambda_A + \lambda_B) = 3/7$ of being type A, independently of the others. Thus, the number $K$ of arrivals until the first type A arrival is geometric with parameter $3/7$. The number of type B arrivals before the first type A arrival is equal to $K - 1$, and its PMF is similar to a geometric, except that it is shifted by one unit to the left. In particular,

$$p_K(k) = \left(\frac{3}{7}\right)\left(\frac{4}{7}\right)^k, \qquad k = 0, 1, 2, \ldots.$$

[SOURCE TYPO?: the opening sentence is redundant in the original — "Each future arrival is of type A with probability $\lambda_A/(\lambda_A + \lambda_B) = 3/7$ of being type A" — the phrase "of being type A" is a leftover from part (b) and duplicates "is of type A".]

[SOURCE TYPO?: the displayed PMF is labelled $p_K(k)$, but by the text it is the PMF of $K - 1$ (the number of type B arrivals), not of $K$ itself; $K$ is geometric on $\{1,2,\ldots\}$.]

---

## Problem 3 — $\mathbf{P}(X < Y < Z)$ for three independent exponentials

### Statement

3. Let $X$, $Y$, and $Z$ be independent exponential random variables with parameters $\lambda$, $\mu$, and $\nu$, respectively. Find $\mathbf{P}(X < Y < Z)$.

### Official solution

The event $\{X < Y < Z\}$ can be expressed as $\{X < \min\{Y, Z\}\} \cap \{Y < Z\}$. Let $Y$ and $Z$ be the 1st arrival times of two independent Poisson processes with rates $\mu$ and $\nu$. By merging the two processes, it should be clear that $Y < Z$ if and only if the first arrival of the merged process comes from the original process with rate $\mu$, and thus

$$\mathbf{P}(Y < Z) = \frac{\mu}{\mu + \nu}.$$

Let $X$ be the 1st arrival time of a third independent Poisson process with rate $\lambda$. Now $\{X < \min\{Y, Z\}\}$ if and only if the first arrival of the Poisson process obtained by merging the two processes with rates $\lambda$ and $\mu + \nu$ comes from the original process with rate $\lambda$, and thus

$$\mathbf{P}(X < \min\{Y, Z\}) = \frac{\lambda}{\lambda + \mu + \nu}.$$

Note that the event $\{X < \min\{Y, Z\}\}$ is independent of the event $\{Y < Z\}$, as the time of the first arrival of the merged process with rate $\mu + \nu$ is independent of whether that first arrival comes from the process with rate $\mu$ or the process with rate $\nu$. Hence,

$$
\begin{aligned}
\mathbf{P}(X < Y < Z) &= \mathbf{P}(X < \min\{Y, Z\}) \cdot \mathbf{P}(Y < Z) \\
&= \frac{\lambda\mu}{(\lambda + \mu + \nu)(\mu + \nu)}.
\end{aligned}
$$

[SOLUTION GAP: the fact that $\min\{Y,Z\}$ is exponential with rate $\mu + \nu$ (used implicitly via the merging argument) is asserted rather than derived.]

---

Both PDFs close with an MIT OpenCourseWare page: "MIT OpenCourseWare, http://ocw.mit.edu, 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010. For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms."
