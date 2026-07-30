# rec06 — Recitation 6 (September 28, 2010)

Covers: joint PMFs of discrete random variables, conditional PMFs, conditional expectation and conditional variance, functions of two random variables (min), expectation of a product, conditioning on an event, variance of the geometric distribution.

Sources: MIT6_041F10_rec06.pdf, MIT6_041F10_rec06_sol.pdf

Massachusetts Institute of Technology
Department of Electrical Engineering & Computer Science
6.041/6.431: Probabilistic Systems Analysis (Fall 2010)

---

## Problem 1 — Four-sided die determines number of coin flips (joint/conditional PMFs)

### Statement

Consider an experiment in which a fair four-sided die (with faces labeled 0, 1, 2, 3) is thrown once to determine how many times a fair coin is to be flipped. In the sample space of this experiment, random variables $N$ and $K$ are defined by

- $N$ = the result of the die roll
- $K$ = the total number of heads resulting from the coin flips

(a) Determine and sketch $p_N(n)$

(b) Determine and tabulate $p_{N,K}(n,k)$

(c) Determine and sketch $p_{K|N}(k \mid 2)$

(d) Determine and sketch $p_{N|K}(n \mid 2)$

### Official solution

**(a)** The first part can be completed without reference to anything other than the die roll:

[FIGURE: PMF stem plot of $p_N(n)$. Vertical axis labeled $p_N(n)$ with a single tick mark at height 1/4; horizontal axis labeled $n$ with ticks at 0, 1, 2, 3. Four equal-height impulses (vertical bars) of height 1/4 rise at $n = 0, 1, 2, 3$. | raster/rec06_sol_p01.png]

So $p_N(n) = 1/4$ for $n \in \{0,1,2,3\}$, and $0$ otherwise.

**(b)** When $N = 0$, the coin is not flipped at all, so $K = 0$. When $N = n$ for $n \in \{1, 2, 3\}$, the coin is flipped $n$ times, resulting in $K$ with a distribution that is conditionally binomial. The binomial probabilities are all multiplied by $1/4$ because $p_N(n) = 1/4$ for $n \in \{0, 1, 2, 3\}$. The joint PMF $p_{N,K}(n,k)$ thus takes the following values and is zero otherwise:

|        | $k = 0$ | $k = 1$ | $k = 2$ | $k = 3$ |
|--------|---------|---------|---------|---------|
| $n = 0$ | $1/4$  | $0$     | $0$     | $0$     |
| $n = 1$ | $1/8$  | $1/8$   | $0$     | $0$     |
| $n = 2$ | $1/16$ | $1/8$   | $1/16$  | $0$     |
| $n = 3$ | $1/32$ | $3/32$  | $3/32$  | $1/32$  |

**(c)** Conditional on $N = 2$, $K$ is a binomial random variable. So we immediately see that

$$
p_{K|N}(k|2) = \begin{cases}
1/4, & \text{if } k = 0, \\
1/2, & \text{if } k = 1, \\
1/4, & \text{if } k = 2, \\
0, & \text{otherwise.}
\end{cases}
$$

This is a normalized row of the table in the previous part.

[FIGURE: PMF stem plot of $p_{K|N}(k \mid 2)$. Vertical axis with tick marks labeled 1/4 and 1/2; horizontal axis labeled $k$ with ticks at 0, 1, 2. Impulses: height 1/4 at $k = 0$, height 1/2 at $k = 1$, height 1/4 at $k = 2$. | raster/rec06_sol_p01.png]

**(d)** To get $K = 2$ heads, there must have been at least 3 coin tosses, so only $N = 3$ and $N = 4$ have positive conditional probability given $K = 2$.

[SOURCE TYPO?: The sentence should read "there must have been at least 2 coin tosses, so only $N = 2$ and $N = 3$ have positive conditional probability given $K = 2$." $N$ takes values in $\{0,1,2,3\}$ only, so "$N = 4$" cannot occur, and the computation that immediately follows is for $p_{N|K}(2 \mid 2)$ and $p_{N|K}(3 \mid 2)$.]

$$
p_{N|K}(2 \mid 2) = \frac{\mathbf{P}(\{N = 2\} \cap \{K = 2\})}{\mathbf{P}(\{K = 2\})} = \frac{1/16}{1/16 + 1/32 + 1/32 + 1/32} = 2/5.
$$

[SOURCE TYPO?: The denominator is written as a four-term sum $1/16 + 1/32 + 1/32 + 1/32$. From the table, $\mathbf{P}(K = 2) = p_{N,K}(2,2) + p_{N,K}(3,2) = 1/16 + 3/32$, i.e. only two nonzero terms. The written sum evaluates to the same $5/32$ (the $3/32$ having been split into three $1/32$'s), so the numerical answer $2/5$ is correct.]

Similarly, $p_{N|K}(3 \mid 2) = 3/5$.

[SOLUTION GAP: The computation $p_{N|K}(3 \mid 2) = \dfrac{3/32}{5/32} = 3/5$ is not shown; only the answer is stated.]

[FIGURE: PMF stem plot of $p_{N|K}(n \mid 2)$. Vertical axis labeled $p_{N|K}(n|2)$; horizontal axis labeled $n$ with ticks at 2 and 3. Impulse of height 2/5 at $n = 2$ (labeled "2/5") and a taller impulse of height 3/5 at $n = 3$ (labeled "3/5"). | raster/rec06_sol_p02.png]

---

## Problem 2 — Eight equally likely points in the $(x,y)$ plane

### Statement

Consider an outcome space comprising eight equally likely event points, as shown below:

[FIGURE: Scatter/point-mass diagram in the $x$–$y$ plane. Vertical axis labeled $y$ with ticks 0, 1, 2, 3; horizontal axis labeled $x$ with ticks 0, 1, 2, 3, 4. Eight solid dots, each annotated with probability (1/8), at the points: $(0,3)$, $(4,3)$, $(2,2)$, $(4,2)$, $(0,1)$, $(2,1)$, $(4,1)$, $(4,0)$. | raster/rec06_p01.png]

(a) Which value(s) of $x$ *maximize(s)* $\mathbf{E}[Y \mid X = x]$?

(b) Which value(s) of $y$ *maximize(s)* $\mathrm{var}(X \mid Y = y)$?

(c) Let $R = \min(X, Y)$. Prepare a neat, fully labeled sketch of $p_R(r)$,

(d) Let $A$ denote the event $X^2 \ge Y$. Determine numerical values for the quantities $\mathbf{E}[XY]$ and $\mathbf{E}[XY \mid A]$.

### Official solution

**(a)** $x = 0$ maximizes $\mathbf{E}[Y \mid X = x]$ since

$$
\mathbf{E}[Y \mid X = x] = \begin{cases}
2, & \text{if } x = 0, \\
3/2, & \text{if } x = 2, \\
3/2, & \text{if } x = 4, \\
\text{undefined}, & \text{otherwise.}
\end{cases}
$$

[SOLUTION GAP: The individual conditional expectations are stated without derivation. E.g. given $X = 0$ the points are $(0,3)$ and $(0,1)$, each conditionally probability $1/2$, giving $\mathbf{E}[Y \mid X = 0] = 2$; given $X = 2$ the points are $(2,2),(2,1)$; given $X = 4$ the points are $(4,3),(4,2),(4,1),(4,0)$. None of this arithmetic is shown.]

**(b)** $y = 3$ maximizes $\mathrm{var}(X \mid Y = y)$ since

$$
\mathrm{var}(X \mid Y = y) = \begin{cases}
0, & \text{if } y = 0, \\
8/3, & \text{if } y = 1, \\
1, & \text{if } y = 2, \\
4, & \text{if } y = 3, \\
\text{undefined}, & \text{otherwise.}
\end{cases}
$$

[SOLUTION GAP: The conditional variances are stated without derivation. E.g. given $Y = 1$, $X$ is uniform on $\{0,2,4\}$ so the mean is 2 and the variance is $8/3$; given $Y = 3$, $X$ is uniform on $\{0,4\}$ so the variance is 4. No arithmetic is shown.]

**(c)**

[FIGURE: PMF stem plot of $p_R(r)$ for $R = \min(X,Y)$. Vertical axis labeled $p_R(r)$ with tick marks at 1/8, 1/4, 3/8; horizontal axis labeled $r$ with ticks at 0, 1, 2, 3. Impulses: height 3/8 at $r = 0$, height 1/4 at $r = 1$, height 1/4 at $r = 2$, height 1/8 at $r = 3$. | raster/rec06_sol_p02.png]

[SOLUTION GAP: Only the sketch is given; the mapping of each of the eight sample points to $R = \min(X,Y)$ is not shown. (Namely $(0,3)\to0$, $(0,1)\to0$, $(4,0)\to0$; $(2,1)\to1$, $(4,1)\to1$; $(2,2)\to2$, $(4,2)\to2$; $(4,3)\to3$.)]

**(d)** By traversing the points top to bottom and left to right, we obtain

$$
\mathbf{E}[XY] = \frac{1}{8}\left(0 \cdot 3 + 4 \cdot 3 + 2 \cdot 2 + 4 \cdot 2 + 0 \cdot 1 + 2 \cdot 1 + 4 \cdot 1 + 4 \cdot 0\right) = \frac{15}{4}.
$$

Conditioning on $A$ removes the point masses at $(0,1)$ and $(0,3)$. The conditional probability of each of the remaining point masses is thus $1/6$, and

$$
\mathbf{E}[XY \mid A] = \frac{1}{6}\left(4 \cdot 3 + 2 \cdot 2 + 4 \cdot 2 + 2 \cdot 1 + 4 \cdot 1 + 4 \cdot 0\right) = 5.
$$

---

## Problem 3 — Example 2.17: Variance of the geometric distribution

### Statement

**Example 2.17. Variance of the geometric distribution.** You write a software program over and over, and each time there is probability $p$ that it works correctly, independent of previous attempts. What is the variance of $X$, the number of tries until the program works correctly?

### Official solution

See the textbook, Example 2.17, pages 105–106.

[SOLUTION GAP: The entire solution is delegated to the textbook (Bertsekas & Tsitsiklis, *Introduction to Probability*, Example 2.17, pp. 105–106). No derivation and not even the final answer $\mathrm{var}(X) = (1-p)/p^2$ is given in the recitation solution handout.]

---

*Textbook problems are courtesy of Athena Scientific, and are used with permission.*

*MIT OpenCourseWare, http://ocw.mit.edu — 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010. For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.*
