# rec13 — Recitation 13 (October 21, 2010)

Covers: Law of Iterated Expectations (including generalizations to conditioning on multiple random variables), Law of Total Variance, conditional expectation/variance as random variables, sum of a random number of independent random variables (random sums), continuous uniform breaking-stick example.

Sources: MIT6_041F10_rec13.pdf (questions), MIT6_041F10_rec13_sol.pdf (solutions)

---

## Preamble (from the problem sheet)

For the problems below, recall the Law of Iterated Expectations and the Law of Total Variance:

$$\mathbf{E}[X] = \mathbf{E}\big[\mathbf{E}[X|Y]\big]$$

$$\mathrm{var}(X) = \mathbf{E}\big[\mathrm{var}(X|Y)\big] + \mathrm{var}\big(\mathbf{E}[X|Y]\big).$$

---

## Problem 1 — Generalizations of the law of iterated expectations

### Statement

Let $X$, $Y$, and $Z$ be discrete random variables. Show the following generalizations of the law of iterated expectations.

(a) $\mathbf{E}[Z] = \mathbf{E}\big[\mathbf{E}[Z \mid X, Y]\big]$.

(b) $\mathbf{E}[Z \mid X] = \mathbf{E}\big[\mathbf{E}[Z \mid X, Y] \mid X\big]$.

(c) $\mathbf{E}[Z] = \mathbf{E}\Big[\mathbf{E}\big[\mathbf{E}[Z \mid X, Y] \mid X\big]\Big]$.

### Official solution

**(a)** We begin by writing the definition for $\mathbf{E}[Z \mid X, Y]$

$$\mathbf{E}[Z \mid X = x, Y = y] = \sum_{z} z\, p_{Z|X,Y}(z \mid x, y)$$

Since $\mathbf{E}[Z \mid X, Y]$ is a function of the random variables $X$ and $Y$, and is equal to $\mathbf{E}[Z \mid X = x, Y = y]$ whenever $X = x$ and $Y = y$, which happens with probability $p_{X,Y}(x, y)$, using the expected value rule, we have

$$
\begin{aligned}
\mathbf{E}\big[\mathbf{E}[Z \mid X, Y]\big]
&= \sum_{x}\sum_{y} \mathbf{E}[Z \mid X = x, Y = y]\, p_{X,Y}(x, y) \\
&= \sum_{x}\sum_{y}\sum_{z} z\, p_{Z|X,Y}(z \mid x, y)\, p_{X,Y}(x, y) \\
&= \sum_{x}\sum_{y}\sum_{z} z\, p_{X,Y,Z}(x, y, z) \\
&= \mathbf{E}[Z]
\end{aligned}
$$

[SOLUTION GAP: the step from $\sum_x\sum_y\sum_z z\,p_{X,Y,Z}(x,y,z)$ to $\mathbf{E}[Z]$ — i.e. marginalizing the joint PMF over $x$ and $y$ to get $p_Z(z)$ — is not written out.]

**(b)** We start with the definition for $\mathbf{E}[Z \mid X, Y]$ which is a function of the random variables $X$ and $Y$, and is equal to $\mathbf{E}[Z \mid X = x, Y = y]$ whenever $X = x$ and $Y = y$, so

$$\mathbf{E}[Z \mid X = x, Y = y] = \sum_{z} z\, p_{Z|X,Y}(z \mid x, y)$$

Proceeding as above, but conditioning on the event $X = x$, we have

$$
\begin{aligned}
\mathbf{E}\big[\mathbf{E}[Z \mid X, Y = y] \mid X = x\big]
&= \sum_{y} \mathbf{E}[Z \mid X = x, Y = y]\, p_{Y|X}(y \mid x) \\
&= \sum_{y}\sum_{z} z\, p_{Z|X,Y}(z \mid x, y)\, p_{Y|X}(y \mid x) \\
&= \sum_{y}\sum_{z} z\, p_{Y,Z|X}(y, z \mid x) \\
&= \mathbf{E}[Z \mid X = x]
\end{aligned}
$$

Since this is true for all possible values of $x$, we have $\mathbf{E}\big[\mathbf{E}[Z \mid Y, X] \mid X\big] = \mathbf{E}[Z \mid X]$.

[SOURCE TYPO?: the left-hand side of the displayed chain is written $\mathbf{E}\big[\mathbf{E}[Z \mid X, Y = y] \mid X = x\big]$, mixing the random variable $Y$ with the realized value $Y = y$ inside the inner conditional; it should read $\mathbf{E}\big[\mathbf{E}[Z \mid X, Y] \mid X = x\big]$.]

[SOLUTION GAP: the last equality $\sum_y\sum_z z\,p_{Y,Z|X}(y,z\mid x) = \mathbf{E}[Z \mid X = x]$ — marginalizing over $y$ to obtain $p_{Z|X}(z\mid x)$ — is asserted without the intermediate step.]

**(c)** We take expectations of both sides of the formula in part (b) to obtain

$$\mathbf{E}\big[\mathbf{E}[Z \mid X]\big] = \mathbf{E}\Big[\mathbf{E}\big[\mathbf{E}[Z \mid X, Y] \mid X\big]\Big].$$

By the law of iterated expectations, the left-hand side above is $\mathbf{E}[Z]$, which establishes the desired result.

---

## Problem 2 — Breaking a stick twice (Example 4.17, page 223 in text)

### Statement

Example 4.17, page 223 in text.

We start with a stick of length $\ell$. We break it at a point which is chosen randomly and uniformly over its length, and keep the piece that contains the left end of the stick. We then repeat the same process on the piece that we were left with.

(a) What is the expected value of the length of the piece that we are left with after breaking twice?

(b) What is the variance of the length of the piece that we are left with after breaking twice?

### Official solution

Let $Y$ be the length of the piece after we break for the first time. Let $X$ be the length after we break for the second time.

**(a)** The law of iterated expectations states:

$$\mathbf{E}[X] = \mathbf{E}[\mathbf{E}[X|Y]]$$

We have $\mathbf{E}[X|Y] = \dfrac{Y}{2}$ and $E[Y] = \dfrac{l}{2}$. So then:

$$\mathbf{E}[X] = \mathbf{E}[\mathbf{E}[X|Y]] = \mathbf{E}[Y/2] = \frac{1}{2}\mathbf{E}[Y] = \frac{1}{2}\cdot\frac{l}{2} = \frac{l}{4}$$

[SOURCE TYPO?: the solution writes the stick length as an italic lowercase $l$ here (and non-bold $E[Y]$), whereas the problem statement and part (b) use the script $\ell$; these denote the same quantity.]

[SOLUTION GAP: it is asserted without derivation that $\mathbf{E}[X\mid Y] = Y/2$, i.e. that given $Y$ the second break point is uniform on $[0, Y]$.]

**(b)** We use the Law of Total Variance to find $\mathrm{var}(X)$:

$$\mathrm{var}(X) = \mathbf{E}[\mathrm{var}(X \mid Y)] + \mathrm{var}(\mathbf{E}[X \mid Y]).$$

Recall that the variance of a uniform random variable distributed over $[a, b]$ is $(b - a)^2/12$. Since $Y$ is uniformly distributed over $[0, \ell]$, we have

$$
\begin{aligned}
\mathrm{var}(Y) &= \frac{\ell^2}{12}, \\
\mathrm{var}(X \mid Y) &= \frac{Y^2}{12}.
\end{aligned}
$$

We know that $\mathbf{E}[X \mid Y] = Y/2$, and so

$$\mathrm{var}(\mathbf{E}[X \mid Y]) = \mathrm{var}(Y/2) = \frac{1}{4}\mathrm{var}(Y) = \frac{\ell^2}{48}.$$

Also,

$$
\begin{aligned}
\mathbf{E}[\mathrm{var}(X \mid Y)] &= \mathbf{E}\left[\frac{Y^2}{12}\right] \\
&= \int_{0}^{\ell} \frac{y^2}{12} f_Y(y)\, dy \\
&= \frac{1}{12}\cdot\frac{1}{\ell}\int_{0}^{\ell} y^2\, dy \\
&= \frac{\ell^2}{36}.
\end{aligned}
$$

[SOLUTION GAP: the evaluation $\frac{1}{12\ell}\int_0^\ell y^2\,dy = \frac{1}{12\ell}\cdot\frac{\ell^3}{3} = \frac{\ell^2}{36}$ is done in one step.]

Combining these results, we obtain

$$\mathrm{var}(X) = \mathbf{E}[\mathrm{var}(X \mid Y)] + \mathrm{var}(\mathbf{E}[X \mid Y]) = \frac{\ell^2}{36} + \frac{\ell^2}{48} = \frac{7\ell^2}{144}.$$

---

## Problem 3 — Widgets in boxes in a crate (random sum)

### Statement

Widgets are stored in boxes, and then all boxes are assembled in a crate. Let $X$ be the number of widgets in any particular box, and $N$ be the number of boxes in a crate. Assume that $X$ and $N$ are independent integer-valued random variables, with expected value equal to 10, and variance equal to 16. Evaluate the expected value and variance of $T$, where $T$ is the total number of widgets in a crate.

### Official solution

Let $X_i$ denote the number of widgets in the $i^{th}$ box. Then $T = \sum_{i=1}^{N} X_i$.

$$
\begin{aligned}
\mathbf{E}[T] &= \mathbf{E}\Big[\mathbf{E}\Big[\sum_{i=1}^{N} X_i \Big| N\Big]\Big] \\
&= \mathbf{E}\Big[\sum_{i=1}^{N} \mathbf{E}[X_i | N]\Big] \\
&= \mathbf{E}\Big[\sum_{i=1}^{N} \mathbf{E}[X]\Big] \\
&= \mathbf{E}[X]\cdot\mathbf{E}[N] = 100.
\end{aligned}
$$

[SOLUTION GAP: the step $\mathbf{E}[X_i \mid N] = \mathbf{E}[X]$ uses the independence of $X_i$ and $N$ and the fact that all $X_i$ have the same distribution as $X$; this is not spelled out. Likewise $\mathbf{E}\big[\sum_{i=1}^{N}\mathbf{E}[X]\big] = \mathbf{E}[N\,\mathbf{E}[X]] = \mathbf{E}[X]\mathbf{E}[N]$ is compressed into one line.]

and,

$$
\begin{aligned}
\mathrm{var}(T) &= \mathbf{E}\big[\mathrm{var}(T|N)\big] + \mathrm{var}\big(\mathbf{E}[T|N]\big) \\
&= \mathbf{E}\left[\mathrm{var}\left(\sum_{i=1}^{N} X_i \Big| N\right)\right] + \mathrm{var}\left(\mathbf{E}\left[\sum_{i=1}^{N} X_i \Big| N\right]\right) \\
&= \mathbf{E}[N\,\mathrm{var}(X)] + \mathrm{var}(N\,\mathbf{E}[X]) \\
&= (\mathrm{var}(X))\mathbf{E}[N] + (\mathbf{E}[X])^2\,\mathrm{var}(N) \\
&= 16\cdot 10 + 100\cdot 16 = 1760.
\end{aligned}
$$

[SOLUTION GAP: the identity $\mathrm{var}\big(\sum_{i=1}^{N} X_i \mid N\big) = N\,\mathrm{var}(X)$ requires that the $X_i$ be independent of each other (and of $N$); the problem statement only says $X$ and $N$ are independent, and the solution does not justify this step. Similarly $\mathrm{var}(N\mathbf{E}[X]) = (\mathbf{E}[X])^2\mathrm{var}(N)$ is used without comment.]

---

## Figures

No figures, plots, diagrams, or trees appear anywhere in either the problem sheet (raster/rec13_p01.png, raster/rec13_p02.png) or the solutions (raster/rec13_sol_p01.png, raster/rec13_sol_p02.png, raster/rec13_sol_p03.png, raster/rec13_sol_p04.png). Both documents are pure text/formula.

## Source notes

- Question sheet: 1 content page (raster/rec13_p01.png) plus a final MIT OpenCourseWare citation page (raster/rec13_p02.png). Footer of page 1: "Textbook problems are courtesy of Athena Scientific, and are used with permission."
- Solutions: 3 content pages (raster/rec13_sol_p01.png through rec13_sol_p03.png) plus a final MIT OpenCourseWare citation page (raster/rec13_sol_p04.png).
- Both documents carry the header: Massachusetts Institute of Technology / Department of Electrical Engineering & Computer Science / 6.041/6.431: Probabilistic Systems Analysis / (Fall 2010).
- Title block on the problem sheet: "Recitation 13 / October 21, 2010"; on the solutions: "Recitation 13 Solutions / October 21, 2010". Solution page footers read "Page 1 of 3", "Page 2 of 3", "Page 3 of 3"; the problem sheet footer reads "Page 1 of 1". Solution page 1 ends mid-problem-2 (with the sentence defining $Y$ and $X$), and parts 2(a), 2(b) and all of problem 3's $\mathbf{E}[T]$ derivation appear on solution page 2; only the $\mathrm{var}(T)$ derivation appears on solution page 3.
