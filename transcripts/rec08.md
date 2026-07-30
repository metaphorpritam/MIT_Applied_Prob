# rec08 — Recitation 8 (October 5, 2010)

Covers: continuous random variables, PDF normalization, cumulative distribution functions (CDFs), mixed discrete/continuous waiting-time problem, exponential random variable (CDF, mean, variance), distribution of the max and min of independent exponentials

Sources: MIT6_041F10_rec08.pdf (questions), MIT6_041F10_rec08_sol.pdf (solutions)

Course header on both documents:
Massachusetts Institute of Technology — Department of Electrical Engineering & Computer Science — 6.041/6.431: Probabilistic Systems Analysis (Fall 2010).

Document titles under the header rule: the question sheet reads "Recitation 8 / October 5, 2010"; the solution sheet reads "Recitation 8 Solutions / October 5, 2010".

Footer note on the question sheet: "Textbook problems are courtesy of Athena Scientific, and are used with permission." (right-hand footer "Page 1 of 1"). The solution sheet has no textbook-credit footer; its footers read "Page 1 of 2" and "Page 2 of 2", and the MIT header block is repeated at the top of solution page 2.

No figures, plots, diagrams, or trees appear anywhere in either document (all pages are pure text/equations). Page 2 of the question PDF and page 3 of the solution PDF are the standard MIT OpenCourseWare boilerplate page (http://ocw.mit.edu, "6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010", terms-of-use link).

---

## Problem 1 — Normalizing a quadratic PDF and finding its CDF

### Statement

Let $Z$ be a continuous random variable with probability density function

$$
f_z(z) = \begin{cases} \gamma(1 + z^2), & \text{if } -2 < z < 1,\\ 0, & \text{otherwise.} \end{cases}
$$

[SOURCE TYPO?: the question sheet writes the density with a lowercase subscript, $f_z(z)$, whereas the standard notation (and the solution sheet) uses the uppercase random-variable subscript $f_Z(z)$.]

(a) For what value of $\gamma$ is this possible?

(b) Find the cumulative distribution function of $Z$.

### Official solution

**(a)** We know that the PDF must integrate to 1. Therefore we have

$$
\int_{-\infty}^{\infty} f_Z(z)\,dz \;=\; \int_{-2}^{1} \gamma(1+z^2) \;=\; \gamma\left(z + \tfrac{1}{3}z^3\right)\Big|_{-2}^{1} \;=\; 6\gamma .
$$

[SOURCE TYPO?: the second integral $\int_{-2}^{1}\gamma(1+z^2)$ is printed without the differential $dz$.]

From this we conclude $\gamma = 1/6$.

[SOLUTION GAP: the arithmetic evaluating $\gamma\left(z+\frac{1}{3}z^3\right)\big|_{-2}^{1}$ to $6\gamma$ is not shown, and the step from $6\gamma = 1$ to $\gamma = 1/6$ is stated without work.]

**(b)** To find the CDF, we integrate:

$$
F_Z(z) \;=\; \int_{-\infty}^{z} f_Z(t)\,dt \;=\;
\begin{cases}
0, & \text{if } z < -2,\\[2pt]
\dfrac{1}{6}\left(t + \dfrac{1}{3}t^3\right)\Big|_{-2}^{\,z}, & \text{if } -2 \le z \le 1,\\[6pt]
1, & \text{if } z > 1
\end{cases}
$$

$$
\;=\;
\begin{cases}
0, & \text{if } z < -2,\\[2pt]
\dfrac{1}{6}\left(z + \dfrac{1}{3}z^3 + \dfrac{14}{3}\right), & \text{if } -2 \le z \le 1,\\[6pt]
1, & \text{if } z > 1.
\end{cases}
$$

[SOLUTION GAP: the evaluation of the antiderivative at the lower limit $t=-2$, which produces the constant $14/3$, is not shown.]

---

## Problem 2 — Al's waiting time for a taxi or bus (textbook Problem 3.9)

### Statement

Problem 3.9, pages 186–187 in the text.

The taxi stand and the bus stop near Al's home are in the same location. Al goes there at a given time and if a taxi is waiting, (this happens with probability $2/3$) he boards it. Otherwise he waits for a taxi or a bus to come, whichever comes first. The next taxi will arrive in a time that is uniformly distributed between 0 and 10 minutes, while the next bus will arrive in exactly 5 minutes. Find the CDF and the expected value of Al's waiting time.

### Official solution

See textbook, Problem 3.9, page 187.

[SOLUTION GAP: the entire solution is omitted — the recitation solution sheet only refers the reader to the textbook (Bertsekas & Tsitsiklis, *Introduction to Probability*), page 187. No CDF and no expected value are computed in the source document.]

---

## Problem 3 — The exponential random variable: CDF, mean, variance, max and min

### Statement

Let $\lambda$ be a positive number. The continuous random variable $X$ is called **exponential** with parameter $\lambda$ when its probability density function is

$$
f_X(x) = \begin{cases} \lambda e^{-\lambda x}, & \text{if } x \ge 0,\\ 0, & \text{otherwise.} \end{cases}
$$

(a) Find the cumulative distribution function (CDF) of $X$.

(b) Find the mean of $X$.

(c) Find the variance of $X$.

(d) Suppose $X_1$, $X_2$, and $X_3$ are independent exponential random variables, each with parameter $\lambda$. Find the PDF of $Z = \max\{X_1, X_2, X_3\}$.

(e) Find the PDF of $W = \min\{X_1, X_2\}$.

### Official solution

**(a)** For $x \ge 0$,

$$
F_X(x) \;=\; \int_{-\infty}^{x} f_X(t)\,dt \;=\; \int_{0}^{x} \lambda e^{-\lambda t}\,dt \;=\; \left[-e^{-\lambda t}\right]_{0}^{x} \;=\; 1 - e^{-\lambda x}.
$$

For $x < 0$, we have $F_X(x) = \int_{-\infty}^{x} f_X(t)\,dt = 0$. Thus we conclude

$$
F_X(x) = \begin{cases} 0, & \text{if } x < 0,\\ 1 - e^{-\lambda x}, & \text{if } x \ge 0. \end{cases}
$$

**(b)** The key step in the following computation uses integration by parts, whereby

$$
\int_{0}^{\infty} u\,dv \;=\; uv\Big|_{0}^{\infty} \;-\; \int_{0}^{\infty} v\,du
$$

is applied with $u = x$ and $v = -e^{-\lambda x}$:

$$
\mathbf{E}[X] \;=\; \int_{-\infty}^{\infty} x f_X(x)\,dx \;=\; \int_{0}^{\infty} x\lambda e^{-\lambda x}\,dx \;=\; \left[-xe^{-\lambda x}\right]_{0}^{\infty} + \int_{0}^{\infty} e^{-\lambda x}\,dx \;=\; \frac{1}{\lambda}.
$$

[SOLUTION GAP: the boundary term $\left[-xe^{-\lambda x}\right]_{0}^{\infty} = 0$ and the evaluation $\int_0^\infty e^{-\lambda x}dx = 1/\lambda$ are combined into the final answer without intermediate steps.]

**(c)** Integrating by parts with $u = x^2$ and $v = -e^{-\lambda x}$ in the second line below gives

$$
\begin{aligned}
\mathbf{E}[X^2] &= \int_{-\infty}^{\infty} x^2 f_X(x)\,dx \;=\; \int_{0}^{\infty} x^2 \lambda e^{-\lambda x}\,dx \\
&= \left[-x^2 e^{-\lambda x}\right]_{0}^{\infty} + 2\int_{0}^{\infty} x e^{-\lambda x}\,dx \;=\; \frac{2}{\lambda}\mathbf{E}[X] \;=\; \frac{2}{\lambda^2}.
\end{aligned}
$$

[SOLUTION GAP: the boundary term is dropped without comment, and the identification $2\int_0^\infty x e^{-\lambda x}dx = \frac{2}{\lambda}\mathbf{E}[X]$ (i.e. inserting the factor $\lambda$ to recognize the mean integral) is not spelled out.]

Combining with the previous computation, we obtain

$$
\operatorname{var}(X) \;=\; \mathbf{E}[X^2] - (\mathbf{E}[X])^2 \;=\; \frac{2}{\lambda^2} - \left(\frac{1}{\lambda}\right)^2 \;=\; \frac{1}{\lambda^2}.
$$

**(d)** The maximum of a set is upper bounded by $z$ when each element of the set is upper bounded by $z$. Thus for any positive $z$,

$$
\begin{aligned}
\mathbf{P}(Z \le z) &= \mathbf{P}(\max\{X_1, X_2, X_3\} \le z) \;=\; \mathbf{P}(X_1 \le z,\, X_2 \le z,\, X_3 \le z)\\
&= \mathbf{P}(X_1 \le z)\,\mathbf{P}(X_2 \le z)\,\mathbf{P}(X_3 \le z)\\
&= (1 - e^{-\lambda z})^3,
\end{aligned}
$$

where the third equality uses the independence of $X_1$, $X_2$, and $X_3$.

[Note: the count is correct as printed — in the source the chain has four equality signs: (1) $\mathbf{P}(Z\le z)=\mathbf{P}(\max\{X_1,X_2,X_3\}\le z)$, (2) $=\mathbf{P}(X_1\le z, X_2\le z, X_3\le z)$, (3) $=\mathbf{P}(X_1\le z)\mathbf{P}(X_2\le z)\mathbf{P}(X_3\le z)$ (this is the independence step), (4) $=(1-e^{-\lambda z})^3$.]

Thus,

$$
F_Z(z) = \begin{cases} 0, & \text{if } z < 0,\\ (1 - e^{-\lambda z})^3, & \text{if } z \ge 0. \end{cases}
$$

Differentiating the CDF gives the desired PDF:

$$
f_Z(z) = \begin{cases} 0, & \text{if } z < 0,\\ 3\lambda e^{-\lambda z}(1 - e^{-\lambda z})^2, & \text{if } z \ge 0. \end{cases}
$$

**(e)** The minimum of a set is lower bounded by $w$ when each element of the set is lower bounded by $w$. Thus for any positive $w$,

$$
\begin{aligned}
\mathbf{P}(W \ge w) &= \mathbf{P}(\min\{X_1, X_2\} \ge w) \;=\; \mathbf{P}(X_1 \ge w,\, X_2 \ge w)\\
&= \mathbf{P}(X_1 \le w)\,\mathbf{P}(X_2 \le w)\\
&= \left(e^{-\lambda w}\right)^2 \;=\; e^{-2\lambda w}
\end{aligned}
$$

where the third equality uses the independence of $X_1$ and $X_2$.

[SOURCE TYPO?: the second line is printed as $\mathbf{P}(X_1 \le w)\,\mathbf{P}(X_2 \le w)$, but it must be $\mathbf{P}(X_1 \ge w)\,\mathbf{P}(X_2 \ge w)$ — the inequality directions are reversed relative to the preceding and following lines, and only $\mathbf{P}(X_i \ge w) = e^{-\lambda w}$ gives the stated result $\left(e^{-\lambda w}\right)^2$.]

[Note: as in part (d), "the third equality" is correct as printed — the chain's equality signs are (1) $\mathbf{P}(W\ge w)=\mathbf{P}(\min\{X_1,X_2\}\ge w)$, (2) $=\mathbf{P}(X_1\ge w, X_2\ge w)$, (3) $=\mathbf{P}(X_1\ge w)\mathbf{P}(X_2\ge w)$ (the independence step, printed with reversed inequalities as noted above), (4) $=(e^{-\lambda w})^2$, (5) $=e^{-2\lambda w}$.]

Thus,

$$
F_W(w) = \begin{cases} 0, & \text{if } w < 0,\\ 1 - e^{-2\lambda w}, & \text{if } w \ge 0. \end{cases}
$$

We can recognize this as the CDF of an exponential random variable with parameter $2\lambda$. The PDF is

$$
f_W(w) = \begin{cases} 0, & \text{if } w < 0,\\ 2\lambda e^{-2\lambda w}, & \text{if } w \ge 0. \end{cases}
$$
