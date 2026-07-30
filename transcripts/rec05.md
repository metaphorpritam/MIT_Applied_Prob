# rec05 — Recitation 5 (September 23, 2010)

Covers: expected value rule for functions of a random variable, mean/variance of a linear function, variance identity $\mathrm{var}(X)=E[X^2]-(E[X])^2$; binomial PMF, expectation and variance; expectation of transformed random variables ($aX+b$, $X^2$); size-biased vs. uniform sampling (bus/student paradox); St. Petersburg paradox and infinite expectation.

Sources: MIT6_041F10_rec05.pdf (questions, includes "Recitation 5: Extra Handout"), MIT6_041F10_rec05_sol.pdf (official solutions)

Header block on every page:
> Massachusetts Institute of Technology
> Department of Electrical Engineering & Computer Science
> 6.041/6.431: Probabilistic Systems Analysis
> (Fall 2010)

Title block under the header: on the question PDF page 1 "**Recitation 5** / September 23, 2010"; on the question PDF page 2 "**Recitation 5: Extra Handout** / September 23, 2010"; on the solutions PDF "**Recitation 5 Solutions** / September 23, 2010".

Footer on question pages: "Textbook problems are courtesy of Athena Scientific, and are used with permission." plus a page number at right — both question-PDF content pages are numbered "Page 1 of 1" (they are two separate one-page documents). The solutions PDF pages carry **no** Athena Scientific footer, only "Page 1 of 2" and "Page 2 of 2". (Final page of each PDF is the MIT OpenCourseWare boilerplate: http://ocw.mit.edu, "6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010. For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.")

---

## Problem 1 — Derivations: expected value rule, linear functions, variance identity

### Statement

1. (a) Derive the expected value rule for functions of random variables
$$\mathbf{E}[g(X)] = \sum_x g(x) p_X(x).$$

(b) Derive the property for the mean and variance of a linear function of a random variable $Y = aX + b$.
$$\mathbf{E}[Y] = a\mathbf{E}[X] + b, \qquad \mathrm{var}(Y) = a^2\,\mathrm{var}(X).$$

(c) Derive $\mathrm{var}(X) = \mathbf{E}[X^2] - (\mathbf{E}[X])^2$.

### Official solution

1. (a) See derivation in textbook pp. 84-85.

(b) See derivation in textbook p. 86.

(c) See derivation in textbook p. 87.

[SOLUTION GAP: All three derivations are deferred entirely to the textbook (Bertsekas & Tsitsiklis, *Introduction to Probability*, pp. 84–87). No algebra whatsoever is given in the solution handout.]

---

## Problem 2 — Marksman: binomial hits, profit, and squared profit

### Statement

2. A marksman takes 10 shots at a target and has probability 0.2 of hitting the target with each shot, independently of all other shots. Let $X$ be the number of hits.

(a) Calculate and sketch the PMF of $X$.

(b) What is the probability of scoring no hits?

(c) What is the probability of scoring more hits than misses?

(d) Find the expectation and the variance of $X$.

(e) Suppose the marksman has to pay \$3 to enter the shooting range and he gets \$2 dollars for each hit. Let $Y$ be his profit. Find the expectation and the variance of $Y$.

(f) Now let's assume that the marksman enters the shooting range for free and gets the number of dollars that is equal to the square of the number of hits. Let $Z$ be his profit. Find the expectation of $Z$.

### Official solution

(a) $X$ is a Binomial random variable with $n = 10$, $p = 0.2$. Therefore,
$$p_X(k) = \binom{10}{k} 0.2^k\, 0.8^{10-k}, \qquad \text{for } k = 0, \dots, 10$$
and $p_X(k) = 0$ otherwise.

[FIGURE: MATLAB-style scatter plot (open circle markers only, no stems, no connecting line) of the binomial(10, 0.2) PMF. Horizontal axis labeled "number of hits", integer ticks 0,1,2,…,10, range 0 to 10; vertical axis labeled "probability", ticks every 0.1 from 0 to 1 (labels 0, 0.1, 0.2, …, 0.9, 1), so the whole distribution sits in the bottom third of the frame. Boxed axes (tick marks on all four sides), no gridlines, no title, no legend. One small open circle per k: k=0 at ≈0.107, k=1 at ≈0.268, k=2 at ≈0.302 (the peak), k=3 at ≈0.201, k=4 at ≈0.088, k=5 at ≈0.026, and circles for k=6,7,8,9,10 that are still drawn but sit essentially on the horizontal axis (≈0.0055, 0.00079, 0.000074, 0.0000041, 0.0000001). | raster/rec05_sol_p01.png]

(b) $\mathbf{P}(\text{No hits}) = p_X(0) = (0.8)^{10} = \boxed{0.1074}$

(c) $\mathbf{P}(\text{More hists than misses}) = \sum_{k=6}^{10} p_X(k) = \sum_{k=6}^{10} \binom{10}{k} 0.2^k\, 0.8^{10-k} = \boxed{0.0064}$

[SOURCE TYPO?: "hists" should read "hits" — it appears this way in the printed solution.]

[SOLUTION GAP: The numerical evaluation of the five-term sum $\sum_{k=6}^{10}\binom{10}{k}0.2^k 0.8^{10-k}$ is not shown; only the final value 0.0064 is given.]

(d) Since $X$ is a Binomial random variable,
$$\mathbf{E}[X] = 10 \cdot 0.2 = \boxed{2} \qquad \mathrm{var}(X) = 10 \cdot 0.2 \cdot 0.8 = \boxed{1.6}$$

[SOLUTION GAP: The binomial mean/variance formulas $np$ and $np(1-p)$ are quoted without derivation.]

(e) $Y = 2X - 3$, and therefore
$$\mathbf{E}[Y] = 2\mathbf{E}[X] - 3 = \boxed{1} \qquad \mathrm{var}(Y) = 4\,\mathrm{var}(X) = \boxed{6.4}$$

(f) $Z = X^2$, and therefore
$$\mathbf{E}[Z] = \mathbf{E}[X^2] = (\mathbf{E}[X])^2 + \mathrm{var}(X) = \boxed{5.6}$$

[SOLUTION GAP: The arithmetic $2^2 + 1.6 = 5.6$ is not spelled out, and the rearrangement of the variance identity into $\mathbf{E}[X^2] = (\mathbf{E}[X])^2 + \mathrm{var}(X)$ is used without comment.]

---

## Problem 3 — Buses and job-seeking students (size-biased sampling)

### Statement

3. 4 buses carrying 148 job-seeking MIT students arrive at a job convention. The buses carry 40, 33, 25, and 50 students, respectively. One of the students is randomly selected. Let $X$ denote the number of students that were on the bus carrying this randomly selected student. One of the 4 bus drivers is also randomly selected. Let $Y$ denote the number of students on his bus.

(a) Which of $E[X]$ or $E[Y]$ do you think is larger? Give your reasoning in words.

(b) Compute $E[X]$ and $E[Y]$.

### Official solution

(a) We expect $\mathbf{E}[X]$ to be higher than $\mathbf{E}[Y]$ since if we choose the student, we are more likely to pick a bus with more students.

(b) To solve this problem formally, we first compute the PMF of each random variable and then compute their expectations.

$$p_X(x) = \begin{cases} 40/148 & x = 40 \\ 33/148 & x = 33 \\ 25/148 & x = 25 \\ 50/148 & x = 50 \\ 0 & \text{otherwise.} \end{cases}$$

and
$$\mathbf{E}[X] = 40\,\frac{40}{148} + 33\,\frac{33}{148} + 25\,\frac{25}{148} + 50\,\frac{50}{148} = 39.28$$

$$p_Y(y) = \begin{cases} 1/4 & y = 40, 33, 25, 50 \\ 0 & \text{otherwise.} \end{cases}$$

and
$$\mathbf{E}[Y] = 40\,\tfrac14 + 33\,\tfrac14 + 25\,\tfrac14 + 50\,\tfrac14 = 37$$

Clearly, $\mathbf{E}[X] > \mathbf{E}[Y]$.

[SOLUTION GAP: The justification for the size-biased PMF $p_X(x) = x/148$ (i.e., that a uniformly chosen student lies on the bus of size $x$ with probability $x/148$) is stated only implicitly; the intermediate arithmetic $(1600+1089+625+2500)/148 = 5814/148 = 39.28$ is not shown.]

---

## Problem 4 — St. Petersburg paradox

### Statement

4. Problem 2.21, page 123 in the text.

**St. Petersburg paradox.** You toss independently a fair coin and you count the number of tosses until the first tail appears. If this number is $n$, you receive $2^n$ dollars. What is the expected amount that you will receive? How much would you be willing to pay to play this game?

*(Textbook problems are courtesy of Athena Scientific, and are used with permission.)*

### Official solution

4. The expected value of the gain for a single game is infinite since if $X$ is your gain, then
$$\sum_{k=1}^{\infty} 2^k \cdot 2^{-k} = \sum_{k=1}^{\infty} 1 = \infty$$

Thus if you are faced with the choice of playing for given fee $f$ or not playing at all, and your objective is to make the choice that maximizes your expected net gain, you would be willing to pay any value of $f$. However, this is in strong disagreement with the behavior of individuals. In fact experiments have shown that most people are willing to pay only about \$20 to \$30 to play the game. The discrepancy is due to a presumption that the amount one is willing to pay is determined by the expected gain. However, expected gain does not take into account a persons attitude towards risk taking.

[SOURCE TYPO?: "at all,and" — missing space after the comma in the printed solution. Also "a persons attitude" should be "a person's attitude".]

[SOLUTION GAP: The derivation of $p_X(2^k) = 2^{-k}$ (probability that the first tail occurs on toss $k$, i.e. $k-1$ heads then a tail — for a fair coin this is $(1/2)^k$) is not shown; the sum is written down directly.]

Below are histograms showing the payout results for various numbers of simulations of this game:

[FIGURE: Two stacked MATLAB-style histograms of simulated payouts from the St. Petersburg game. Neither panel has axis labels or a legend; each has only a title. Bars are thin vertical blue lines. Since every possible payout is a power of 2, all bars sit at x = 2, 4, 8, 16, 32, 64, 128, 256, 512, …, so the picture is a tall cluster jammed against the left edge plus a few isolated spikes far to the right.
Top panel, titled "20 simulations, observed average = \$19.20": x-axis 0 to 300, labelled ticks every 50 (0, 50, 100, 150, 200, 250, 300); y-axis 0 to 15, labelled ticks at 0, 5, 10, 15. Bars (counts summing to 20): height ≈12 at x = 2, height ≈4 at x = 4, height 1 at x = 8, height 1 at x = 16, height 1 at x = 64, height 1 at x = 256. Nothing at x = 128 and nothing beyond 256.
Bottom panel, titled "200 simulations, observed average = \$11.16": x-axis 0 to 600, labelled ticks every 100 (0, 100, …, 600); y-axis 0 to 150, labelled ticks at 0, 50, 100, 150. Bars: height ≈107 at x = 2, ≈40 at x = 4, ≈26 at x = 8, ≈13 at x = 16, then short bars of height a few at x = 32 and x = 64, and single-count spikes at roughly x = 128, 256 and 512 (the last just short of the 512 mark near the right end of the data).
Both panels: boxed axes with tick marks on all four sides, no gridlines, heavily right-skewed / heavy-tailed shape illustrating why the sample average stays modest despite the infinite expectation. | raster/rec05_sol_p02.png]

---

## Appendix — Recitation 5: Extra Handout (September 23, 2010)

This is a separate one-page handout distributed with the recitation questions (page 2 of the question PDF).

**Recitation 5: Extra Handout — September 23, 2010**

1. To show some relavant computations to Problem 4, the results (plotted as histograms) of simulations of this game have been plotted below for various numbers of simulations.

[SOURCE TYPO?: "relavant" should be "relevant".]

[FIGURE: The same two stacked histograms as in the Problem 4 solution (identical plots, reproduced verbatim). Top panel: title "20 simulations, observed average = \$19.20", x-axis 0–300 with labelled ticks every 50, y-axis 0–15 with labelled ticks 0, 5, 10, 15, no axis labels; bars at the powers of 2 — height ≈12 at x = 2, ≈4 at x = 4, and unit-height bars at x = 8, 16, 64 and 256 (counts total 20). Bottom panel: title "200 simulations, observed average = \$11.16", x-axis 0–600 with labelled ticks every 100, y-axis 0–150 with labelled ticks 0, 50, 100, 150; bars at x = 2 (≈107), 4 (≈40), 8 (≈26), 16 (≈13), then very short bars at 32 and 64 and single-count spikes near 128, 256 and 512. Boxed axes, thin blue vertical bars, no gridlines. | raster/rec05_p02.png]
