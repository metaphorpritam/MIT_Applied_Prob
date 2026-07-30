# rec16 — Recitation 16 (November 2, 2010)

Covers: continuous random variables, normalizing a piecewise-constant PDF, expectation and second moment by integration, derived distribution of a linear function $Y=2X+1$, joint PDF of independent continuous RVs and geometric computation of $P(X\le W)$, conditional PDFs / Bayes for continuous RVs, normal (Gaussian) standardization and use of the $\Phi$ table, derived distribution of $S=24/W$ via CDF, random sums (law of iterated expectations, law of total variance), mixture PDF from a discrete conditioning variable, Bayes' rule for a discrete-given-continuous posterior, conditional independence and $E[A\mid N]=E[A\mid B,N]$.

Sources: MIT6_041F10_rec16.pdf (questions), MIT6_041F10_rec16_sol.pdf (solutions)

Header block on both PDFs: Massachusetts Institute of Technology, Department of Electrical Engineering & Computer Science, 6.041/6.431: Probabilistic Systems Analysis (Fall 2010). Questions PDF title block: "Recitation 16 / (6.041/6.431 Spring 2007 Quiz 2) / November 2, 2010" (2 pages). Solutions PDF title block: "Recitation 16 Solutions / (6.041/6.431 Spring 2007 Quiz 2 Solutions) / November 2, 2010" (6 pages).

---

## Problem 1 — Marathon race times: piecewise-uniform PDF, joint PDF, conditioning, normal noise, derived distribution

### Statement

Xavier and Wasima are participating in the 6.041 MIT marathon, where race times are defined by random variables¹. Let $X$ and $W$ denote the race time of Xavier and Wasima respectively. All race times are in hours. Assume the race times for Xavier and Wasima are independent (i.e. $X$ and $W$ are independent). Xavier's race time, $X$, is defined by the following density

$$
f_X(x) = \begin{cases}
2c, & \text{if } 2 \le x < 3,\\
c, & \text{if } 3 \le x \le 4,\\
0, & \text{otherwise,}
\end{cases}
$$

where $c$ is an unknown constant. Wasima's race time, $W$, is uniformly distributed between 2 and 4 hours. The density of $W$ is then

$$
f_W(w) = \begin{cases}
\tfrac{1}{2}, & \text{if } 2 \le w \le 4,\\
0, & \text{otherwise.}
\end{cases}
$$

**(a)**
 (i) Find the constant $c$
 (ii) Compute $\mathbf{E}[X]$
 (iii) Compute $\mathbf{E}[X^2]$
 (iv) Provide a fully labeled sketch of the PDF of $2X + 1$

**(b)** Compute $\mathbf{P}(X \le W)$.

**(c)** Wasima is using a stopwatch to time herself. However, the stopwatch is faulty; it over-estimates her race time by an amount that is uniformly distributed between $0$ and $\frac{1}{10}$ hours, which is independent of the actual race time. Thus, if $T$ is the time measured by the stopwatch, then we have

$$
f_{T|W}(t|w) = \begin{cases}
10, & \text{if } w \le t \le w + \tfrac{1}{10} \ \text{ and } 2 \le w \le 4,\\
0, & \text{otherwise.}
\end{cases}
$$

Find $f_{W|T}(w|t)$, when $t = 3$.

**(d)** Wasima realizes her stopwatch is faulty and buys a new stopwatch. Unfortunately, the new stopwatch is also faulty; this time, the watch adds random noise $N$ that is normally distributed with mean $\mu = \frac{1}{60}$ hours and variance $\sigma^2 = \frac{4}{3600}$. Find the probability that the watch over-estimates the actual race time by more than 5 minutes, $\mathbf{P}(N > \frac{5}{60})$. For full credit express your final answer as a number.

**(e)** Wasima has a sponsor for the marathon! If Wasima finishes the marathon in $w$ hours, the sponsor pays her $\frac{24}{w}$ thousand dollars. Define

$$
S = \frac{24}{W}
$$

Find the PDF of $S$.

¹ A runner's race time is defined as the time required for a given runner to complete the marathon.

### Official solution

**(a) (i)** The plot for the PDF of $X$ is shown in Figure 1. The PDF has to integrate to 1, so the area under $f_X(x)$ is $2c+c$, which must equal 1. Therefore $c = 1/3$.

Integration of the PDF:

$$
\int_2^4 f_X(x)\,dx = 1
$$
$$
\text{which breaks up to } \int_2^3 2c\,dx + \int_3^4 c\,dx = 1
$$
$$
= 2c + c = 1
$$
$$
\text{and } c = 1/3.
$$

[FIGURE: Step-function plot of the PDF of $X$. Horizontal axis labeled $x$ with tick marks at 1, 2, 3, 4; vertical axis labeled $f_X(x)$ with tick marks at $c$ and $2c$. The curve is 0 up to $x=2$, then a rectangle of height $2c$ over $2\le x\le 3$, then a rectangle of height $c$ over $3\le x\le 4$, then 0. Caption: "Figure 1: PDF of X". | raster/rec16_sol_p01.png]

**(ii)**

$$
\mathbf{E}[X] = \int_2^4 x f_X(x)\,dx = \int_2^3 x\cdot 2/3\,dx + \int_3^4 x\cdot 1/3\,dx
$$
$$
= 1/3\cdot(3^2 - 2^2) + 1/6\cdot(4^2 - 3^2) = 5/3 + 17/6
$$
$$
= 17/6.
$$

[SOURCE TYPO?: the middle line reads "$=5/3+17/6$", but $1/6\cdot(4^2-3^2) = 7/6$, and $5/3 + 7/6 = 17/6$ which matches the stated final answer. So "$17/6$" in the middle line should be "$7/6$".]

**(iii)**

$$
\mathbf{E}[X^2] = \int_2^4 x^2 f_X(x)\,dx = \int_2^3 x^2\cdot 2/3\,dx + \int_3^4 x^2\cdot 1/3\,dx
$$
$$
= 2/9\cdot(3^3 - 2^3) + 1/9\cdot(4^3 - 3^3) = 38/9 + 37/9
$$
$$
= 25/3.
$$

**(iv)** Let $Y = 2X + 1$. The range of $Y$ is not from 2 to 4, but now $5 \le y \le 9$. The shape of the PDF of $Y$ should look like the PDF of $X$, but scaled by a factor such that it normalizes to 1. The range of $Y$ is double the range of $X$, so the density is half. Plot shown below in Figure 2.

Since $Y = g(X)$ is a linear function of $X$, we can use the formula for the derived distribution for a linear function. $Y = 2X+1$, so $f_Y(y) = \frac{1}{2} f_X\!\left(\frac{y-1}{2}\right)$ for $5 \le y \le 9$. Figure 2 matches this distribution.

[FIGURE: Step-function plot of the PDF of $Y = 2X+1$. Horizontal axis labeled $y$ with tick marks at 1 through 9; vertical axis labeled $f_Y(y)$ with tick marks at $c/2$ and $c$ (note $c$ is drawn above $c/2$). The density is 0 for $y<5$, a rectangle of height $c$ over $5\le y\le 7$, a rectangle of height $c/2$ over $7\le y\le 9$, then 0. Caption: "Figure 2: PDF of $Y = 2X + 1$". | raster/rec16_sol_p02.png]

**(b)** First we calculate the joint PDF. It should have a non-zero joint density for the region, $2 \le x \le 4$ and $2 \le w \le 4$. However, it is not uniform within this entire square, as we have seen often in class. Due to the piece-wise uniform density of $X$, the square is partitioned into two rectangles of uniform joint densities. $X$ and $W$ are independent, so the joint density is just the product of the marginals.

$$
\begin{aligned}
f_{X,W}(x,w) &= f_X(x) f_W(w)\\
&= f_X(x)\cdot 1/2\\
&= \begin{cases}
c1 = 2/3\cdot 1/2 = 1/3, & 2 \le x \le 3,\ 2 \le w \le 4.\\
c2 = 1/3\cdot 1/2 = 1/6, & 3 \le x \le 4,\ 2 \le w \le 4.
\end{cases}
\end{aligned}
$$

Variables $c1$ and $c2$ are used to denote the different joint densities, and are shown in the joint plot.
As a check, the joint PDF should be normalized to 1, which it is.
The joint PDF for $X$ and $W$ is shown in Figure 3.

Looking at the plot of the joint PDF, $\mathbf{P}(X \le W)$ is the region above the $X = W$ line. See Figure 4. We calculate the probability of interest by weighting the areas of the two parts of the shaded regions by $c_1$ and $c_2$:

$$
\mathbf{P}(X \le W) = 1/2\cdot 1/6 + 3/2\cdot 1/3 = 1/12 + 1/2
$$
$$
= 7/12.
$$

[FIGURE: Two side-by-side 2-D plots on the $X$–$W$ plane, horizontal axis $X$ (ticks 1,2,3,4), vertical axis $W$ (ticks 1,2,3,4).
Left (Figure 3, "Joint PDF of X and W"): the square $2\le X\le 4$, $2\le W\le 4$ drawn as an outlined box, split by a vertical line at $X=3$ into a left sub-rectangle labeled $c1$ (over $2\le X\le3$) and a right sub-rectangle labeled $c2$ (over $3\le X\le4$).
Right (Figure 4, "$\mathbf{P}(X\le W)$"): the same square with the 45° line $X = W$ drawn as a straight line from the origin, entering the square at its lower-left corner $(2,2)$, crossing the internal divider at $(3,3)$, exiting at the upper-right corner $(4,4)$, and continuing beyond, labeled $X=W$ at its top right (outside the square). The portion of the square lying above/left of that line is hatched with 45° diagonal shading — i.e. the **trapezoid** $\{2\le X\le 3,\ X\le W\le 4\}$ within the $c1$ strip (area $3/2$) plus the **triangle** $\{3\le X\le 4,\ X\le W\le 4\}$ within the $c2$ strip (area $1/2$). The sub-rectangle labels $c1$ and $c2$ are still shown at height $W\approx 3$. | raster/rec16_sol_p03.png]

[SOURCE TYPO?: in the weighting "$1/2\cdot 1/6 + 3/2\cdot 1/3$", the shaded area in the $c_2$ strip is the triangle of area $1/2$ (weighted by $c_2 = 1/6$) and the shaded area in the $c_1$ strip is the trapezoid of area $3/2$ (weighted by $c_1 = 1/3$); the terms are correct but written in the opposite order from the labels $c_1, c_2$ in the sentence above. Note also the arithmetic ordering: $1/2\cdot 1/6 = 1/12$ and $3/2\cdot 1/3 = 1/2$, so $1/12 + 1/2 = 7/12$.]

The graphical way is the easy solution. Of course, one can integrate:

$$
\begin{aligned}
\mathbf{P}(X \le W) &= \int_2^3\!\!\int_x^4 1/3\ dw\,dx + \int_3^4\!\!\int_x^4 1/6\ dw\,dx\\
&= \frac{1}{3}\int_2^3 (4-x)\,dx + \frac{1}{6}\int_3^4 (4-x)\,dx\\
&= 7/12
\end{aligned}
$$

[SOLUTION GAP: the final numeric evaluation of the two integrals ($\frac13\cdot\frac32 + \frac16\cdot\frac12$) is not shown — the answer $7/12$ is stated directly.]

**(c)** Be careful here, that $T$ is the race time measured by the stopwatch, not just the over-estimated race time. Remember also that $T$ and $W$ are independent.

$$
f_{W|T}(w|3) = \frac{f_{W,T}(w,3)}{f_T(3)}
$$
$$
\text{where } f_{W,T}(w,3) = f_W(w) f_T(3) = 10\cdot 1/2 = 5 \text{ for } 2 \le w \le 4.
$$
$$
\text{and where } f_T(3) = \int_{3-1/10}^{3} f_{W,T}(w,3)\,dw = 5\cdot(1/10) = 1/2.
$$

Therefore,

$$
f_{W|T}(w|3) = \begin{cases}
10, & \text{if } (3 - 1/10) \le w \le 3 \ \text{ and } t = 3,\\
0, & \text{otherwise.}
\end{cases}
$$

[SOURCE TYPO?: (1) The sentence "Remember also that $T$ and $W$ are independent" is wrong — $T = W + (\text{noise})$, so $T$ and $W$ are certainly not independent; the independence is between $W$ and the added noise. (2) The line "$f_{W,T}(w,3) = f_W(w) f_T(3)$" should be $f_{W,T}(w,3) = f_W(w) f_{T|W}(3|w) = (1/2)\cdot 10 = 5$; the factor labels $10$ and $1/2$ are also swapped relative to which density supplies them.]

[SOLUTION GAP: the limits of the integral for $f_T(3)$ (namely that $f_{W,T}(w,3)$ is nonzero only for $3-1/10 \le w \le 3$, coming from the constraint $w \le t \le w + 1/10$ with $t=3$) are used without derivation.]

**(d)** $N$ is Normal(1/60, 4/3600). We standardize $N$ to have mean 1 and standard deviation 1 to utilize the Normal table.

$$
\begin{aligned}
\mathbf{P}\!\left(N > \tfrac{5}{60}\right) &= 1 - \mathbf{P}\!\left(N < \tfrac{5}{60}\right)\\
&= 1 - \mathbf{P}\!\left(\frac{N - 1/60}{2/60} < \frac{5/60 - 1/60}{2/60}\right)\\
&= 1 - \Phi(2).
\end{aligned}
$$

Looking it up, $\Phi(2) = 0.9772$.

So, $\mathbf{P}\!\left(N > \tfrac{5}{60}\right) = 1 - 0.9772 = 0.0028.$

[SOURCE TYPO?: the text says "standardize $N$ to have mean 1 and standard deviation 1" — standardization gives mean **0** and standard deviation 1.]

[SOURCE TYPO?: the printed final number in the solutions PDF (page 4 of 6) is literally "$1 - 0.9772 = 0.0028$", which is an arithmetic slip in the official solution. The correct value is $1 - 0.9772 = \mathbf{0.0228}$. Use $0.0228$.]

Note on the standardization step as printed: $\sigma = \sqrt{4/3600} = 2/60$, so the standardized variable is $\frac{N - 1/60}{2/60}$ and the threshold becomes $\frac{5/60 - 1/60}{2/60} = \frac{4/60}{2/60} = 2$.

**(e)** Use derived distributions to find the CDF of $S$, then differentiate with respect to $s$ to find the PDF of $S$. The range of $S$ is determined from the range of $W$. Since $2 \le w \le 4$ for a nonzero PDF of $W$, $24/4 \le s \le 24/2$ for a nonzero PDF of $S$.

$$
\begin{aligned}
\mathbf{P}(S \le s) &= \mathbf{P}(24/W \le s) = \mathbf{P}(W \ge 24/s)\\
&= 1 - F_W(24/s) = 1 - \int_2^{24/s} f_W(w)\,dw\\
&= 1 - (12/s - 1) = 2 - 12/s
\end{aligned}
$$

Taking the derivative with respect to $s$,

$$
f_S(s) = \frac{d}{ds}(2 - 12/s) = \begin{cases}
12/s^2, & \text{if } 6 \le s \le 12\\
0, & \text{otherwise.}
\end{cases}
$$

[SOLUTION GAP: the evaluation $\int_2^{24/s}\frac12\,dw = \frac12(24/s - 2) = 12/s - 1$ is compressed into one step.]

---

## Problem 2 — Random sums of normals: mean, variance, correlation, mixture PDF, conditional independence

### Statement

Consider the following family of **independent** random variables $N, A_1, B_1, A_2, B_2, \ldots$, where $N$ is a nonnegative discrete random variable and each $A_i$ or $B_i$ is normal with mean 1 and variance 1. Let $A = \sum_{i=1}^{N} A_i$ and $B = \sum_{i=1}^{N} B_i$. Recall that the sum of a fixed number of independent normal random variables is normal.

**(a)** Assume $N$ is geometrically distributed with a mean of $1/p$.
 (i) Find the mean, $\mu_a$, and the variance, $\sigma_a^2$, of $A$.
 (ii) Find $c_{ab}$, defined by $c_{ab} = \mathbf{E}[AB]$.

**(b)** Now assume that $N$ can take only the values 1 (with probability 1/3) and 2 (with probability 2/3).
 (i) Give a formula for the PDF of $A$.
 (ii) Find the conditional probability $\mathbf{P}(N = 1 \mid A = a)$.

**(c)** Is it true that $\mathbf{E}[A \mid N] = \mathbf{E}[A \mid B, N]$ ? Either provide a proof, or an explanation why the equality does not hold.

### Official solution

**(a) (i)** This is a random sums problem so the mean and variance of $A$ is found using the laws of iterated expectations and total variance.

$$
\begin{aligned}
\mu_a &= \mathbf{E}[A] = \mathbf{E}[\mathbf{E}[A \mid N]] = \mathbf{E}[N\,\mathbf{E}[A_i]] = \mathbf{E}[A_i]\mathbf{E}[N]\\
&= 1/p.\\[4pt]
\sigma_a^2 &= \mathrm{var}(A) = \mathbf{E}[\mathrm{var}(A \mid N)] + \mathrm{var}(\mathbf{E}[A \mid N]) = \mathbf{E}[N\,\mathrm{var}(A_i)] + \mathrm{var}(N\,\mathbf{E}[A_i])\\
&= \mathrm{var}(A_i)\mathbf{E}[N] + \mathbf{E}[A_i]^2\,\mathrm{var}(N) = 1/p + p/(1-p)\\
&= 1/p^2.
\end{aligned}
$$

[SOURCE TYPO?: the geometric variance is $\mathrm{var}(N) = (1-p)/p^2$, so the middle expression should read $1/p + (1-p)/p^2$, which indeed equals $1/p^2$. As printed, "$p/(1-p)$" is inconsistent with the stated final answer.]

**(ii)**

$$
\begin{aligned}
c_{ab} = \mathbf{E}[AB] &= \mathbf{E}[(A_1 + A_2 + A_3 + \ldots A_N)(B_1 + B_2 + B_3 + \ldots B_N)]\\
&= \mathbf{E}\big[\mathbf{E}[(A_1 + A_2 + A_3 + \ldots A_N)(B_1 + B_2 + B_3 + \ldots B_N)\mid N]\big]\\
&= \mathbf{E}[N\mathbf{E}[A_i]\,N\mathbf{E}[B_i]] = \mathbf{E}[N^2\mathbf{E}[A_i]\mathbf{E}[B_i]] = \mathbf{E}[A_i]\mathbf{E}[B_i]\mathbf{E}[N^2]\\
&= 1\cdot 1\cdot(\mathrm{var}(N) + \mathbf{E}[N]^2) = (1-p)/p^2 + 1/p^2\\
&= (2-p)/p^2.
\end{aligned}
$$

[SOLUTION GAP: the step $\mathbf{E}[(\sum_{i\le N} A_i)(\sum_{i\le N} B_i)\mid N] = N\mathbf{E}[A_i]\cdot N\mathbf{E}[B_i]$ uses conditional independence of the $A$'s and $B$'s given $N$ without justification.]

**(b) (i)** If $N = 1$, $A = A_1$, which has a Normal distribution with mean 1 and variance 1.
If $N = 2$, $A = A_1 + A_2$, which is the sum of two Normals. Therefore the distribution of $A$ is Normal$(1+1, 1+1)$ or Normal$(2,2)$.
Using total probability theorem, we find:

$$
\begin{aligned}
f_A(a) &= f_{A|N=1}(a)P_N(1) + f_{A|N=2}(a)P_N(2)\\
&= \text{Normal}(1,1)\cdot 1/3 + \text{Normal}(2,2)\cdot 2/3\\
&= \frac{1}{3\sqrt{2\pi}} e^{-(a-1)^2/2} + \frac{2}{3\sqrt{4\pi}} e^{-(a-2)^2/4}.
\end{aligned}
$$

**(ii)**

$$
\mathbf{P}(N = 1 \mid A = a) = \frac{\mathbf{P}(A = a, N = 1)\delta}{\mathbf{P}(A = a)\delta}.
$$
$$
\text{where } \mathbf{P}(A = a)\delta = f_A(a) \text{ was found in part (a)}
$$
$$
\text{and the joint is } P(A = a)P(N = 1)\delta = f_A(a)P_N(1).
$$

Then,

$$
\mathbf{P}(N = 1 \mid A = a) = \frac{\frac{1}{3\sqrt{2\pi}} e^{-(a-1)^2/2}}{\frac{1}{3\sqrt{2\pi}} e^{-(a-1)^2/2} + \frac{2}{3\sqrt{4\pi}} e^{-(a-2)^2/4}}.
$$

[SOURCE TYPO?: the intermediate line "the joint is $P(A=a)P(N=1)\delta = f_A(a)P_N(1)$" is loose/incorrect notation — the joint should be $f_{A|N=1}(a)P_N(1)\delta$, i.e. $\frac{1}{\sqrt{2\pi}}e^{-(a-1)^2/2}\cdot\frac13$, which is what actually appears in the numerator of the final display. Also "was found in part (a)" should say "part (b)(i)".]

**(c)** Yes they are equal.

As a first check, they are both random variables. $A$ and $B$ are not independent from one another because they both depend on the RV $N$ for the random sum. But, if we condition on $N$, then $A$ and $B$ are independent (hence they are conditionally independent). Is that what the right side of the equation states?

These expectations are equal if the PDFs of $A \mid N$ and $A \mid (B,N)$ are equal. Once $N$ is known, knowing $B$ doesn't change what ones knows about $A$, so this not only shows that $A$ and $B$ are conditionally independent, given $N$, but $A \mid N$ has the same information as $A, B \mid N$.

Conditional independence of events $X$ and $Y$ on $Z$ is defined as:

$$
\mathbf{P}(X \cap Y \mid Z) = \mathbf{P}(X \mid Z)\mathbf{P}(Y \mid Z)
$$
$$
\text{or, equivalently}
$$
$$
\mathbf{P}(X \mid Y \cap Z) = \mathbf{P}(X \mid Z)
$$

Therefore, we show that the equality holds here.

$$
\mathbf{E}[A \mid N] = \mathbf{E}[A \mid B, N]
$$
$$
\int a f_{A|N}(a \mid n)\,da = \int a f_{A|B,N}(a|b,n)\,da
$$

The above statement is equal if the PDFs are equal:

$$
\begin{aligned}
f_{A|N}(a \mid n) &= f_{A|B,N}(a \mid b, n) = \frac{f_{A,B,N}(a,b,n)}{f_{B,N}(b,n)}\\
&= \frac{f_{A,B|N}(a,b \mid n)P_N(n)}{f_{B|N}(b \mid n)P_N(n)} = \frac{f_{A|N}(a \mid n) f_{B|N}(b \mid n)}{f_{B|N}(b \mid n)}\\
&= f_{A|N}(a \mid n).
\end{aligned}
$$

So $\mathbf{E}[A \mid N] = \mathbf{E}[A \mid B, N]$ is true.

---

Both PDFs close with the MIT OpenCourseWare page: "MIT OpenCourseWare, http://ocw.mit.edu, 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010. For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms."
