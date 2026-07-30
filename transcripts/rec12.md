# rec12 — Recitation 12 (October 19, 2010)

Covers: correlation coefficient and its invariance under affine transformations; derived distributions — PDF of the difference of two independent exponentials (CDF method and total probability / convolution method); transformation of independent standard normals to polar coordinates (Rayleigh radius, uniform angle, independence of $R$ and $\Theta$); Schwarz inequality for expectations via a variational (least-squares) argument.

Sources: `MIT6_041F10_rec12.pdf` (problems), `MIT6_041F10_rec12_sol.pdf` (solutions)

Course header on every page: Massachusetts Institute of Technology, Department of Electrical Engineering & Computer Science, 6.041/6.431: Probabilistic Systems Analysis (Fall 2010).

Footer on problem sheet: "Textbook problems are courtesy of Athena Scientific, and are used with permission. Page 1 of 1."

Solution sheet title block: "Recitation 12 Solutions / October 19, 2010"; its footer carries only a page number, "Page N of 6" (6 content pages, plus a trailing MIT OCW citation page).

---

## Problem 1 — Correlation coefficient is invariant under affine transformation of one variable

### Statement

Show $\rho(aX + b, Y) = \rho(X, Y)$.

### Official solution

$$
\begin{aligned}
\rho(aX + b, Y)
&= \frac{\operatorname{cov}(aX + b, Y)}{\sqrt{\operatorname{var}(aX + b)(\operatorname{var}(Y))}} \\[2mm]
&= \frac{\mathbf{E}\big[(aX + b - \mathbf{E}[aX + b])(Y - \mathbf{E}[Y])\big]}{\sqrt{a^{2}\operatorname{var}(X)\operatorname{var}(Y)}} \\[2mm]
&= \frac{\mathbf{E}\big[(aX + b - a\mathbf{E}[X] - b)(Y - \mathbf{E}[Y])\big]}{a\sqrt{\operatorname{var}(X)\operatorname{var}(Y)}} \\[2mm]
&= \frac{a\,\mathbf{E}\big[(X - \mathbf{E}[X])(Y - \mathbf{E}[Y])\big]}{a\sqrt{\operatorname{var}(X)\operatorname{var}(Y)}} \\[2mm]
&= \frac{\operatorname{cov}(X, Y)}{\sqrt{\operatorname{var}(X)\operatorname{var}(Y)}} \\[2mm]
&= \rho(X, Y)
\end{aligned}
$$

[SOURCE TYPO?: In going from line 2 to line 3 the source writes $\sqrt{a^{2}\operatorname{var}(X)\operatorname{var}(Y)} = a\sqrt{\operatorname{var}(X)\operatorname{var}(Y)}$, i.e. it uses $a$ rather than $|a|$; strictly $\sqrt{a^2} = |a|$, so the identity as written presumes $a > 0$ (for $a < 0$ one gets $\rho(aX+b,Y) = -\rho(X,Y)$).]

[SOLUTION GAP: The step $\operatorname{var}(aX+b) = a^{2}\operatorname{var}(X)$ is used without derivation, and the outer factor $(\operatorname{var}(Y))$ inside the square root is written with redundant parentheses in the first line.]

As an example where this property of the correlation coefficient is relevant, consider the homework and exam scores of students in a class. We expect the homework and exam scores to be positively correlated and thus have a positive correlation coefficient. Note that, in this example, the above property will mean that the correlation coefficient will not change whether the exam is out of 105 points, 10 points, or any other number of points.

---

## Problem 2 — Romeo and Juliet: PDF of the difference of two independent exponentials

### Statement

Romeo and Juliet have a date at a given time, and each, independently, will be late by amounts of time, $X$ and $Y$, respectively, that are exponentially distributed with parameter $\lambda$.

(a) Find the PDF of $Z = X - Y$ by first finding the CDF and then differentiating.

(b) Find the PDF of $Z$ by using the total probability theorem.

### Official solution

**(a)** When $z \ge 0$:

$$
\begin{aligned}
F_Z(z) = \mathbf{P}(X - Y \le z)
&= \mathbf{P}(X \le Y + z) \\[2mm]
&= \int_{0}^{\infty}\!\!\int_{0}^{y+z} f_{X,Y}(x, y')\,dx\,dy \\[2mm]
&= \int_{0}^{\infty} \lambda e^{-\lambda y} \int_{0}^{y+z} \lambda e^{-\lambda x}\,dx\,dy \\[2mm]
&= \lambda^{\lambda y}\left(1 - e^{-\lambda(y+z)}\right) dy \\[2mm]
&= 1 + \frac{e^{-\lambda z}}{2} e^{-2\lambda y}\bigg|_{y=0}^{y=\infty} \\[2mm]
&= 1 - \frac{1}{2} e^{-\lambda z} \qquad z \ge 0
\end{aligned}
$$

[SOURCE TYPO?: The fourth line is printed as "$\lambda^{\lambda y}\left(1 - e^{-\lambda(y+z)}\right) dy$" — the integral sign $\int_0^\infty$ is missing and $\lambda e^{-\lambda y}$ has been mis-set as $\lambda^{\lambda y}$. It should read $\int_0^\infty \lambda e^{-\lambda y}\left(1 - e^{-\lambda(y+z)}\right) dy$.]

[SOURCE TYPO?: In the second line the integrand is written $f_{X,Y}(x, y')$ with a primed $y'$, while the outer differential is $dy$ (unprimed). The prime appears to be spurious.]

[SOLUTION GAP: The evaluation of $\int_0^\infty \lambda e^{-\lambda y}\left(1 - e^{-\lambda(y+z)}\right) dy$ into the antiderivative form $1 + \frac{e^{-\lambda z}}{2}e^{-2\lambda y}$ is not shown, nor is the substitution of the limits $y=0,\ y=\infty$ that yields $1 - \tfrac12 e^{-\lambda z}$.]

When $z < 0$:

$$
\begin{aligned}
\mathbf{P}(X \le Y + z)
&= \int_{0}^{\infty}\!\!\int_{0}^{y+z} f_{X,Y}(x, y)\,dx\,dy \\[2mm]
&= \int_{0}^{\infty} \lambda e^{-\lambda x} \int_{x-z}^{\infty} \lambda e^{-\lambda y}\,dy\,dx \\[2mm]
&= \int_{0}^{\infty} \lambda e^{-\lambda x} e^{-\lambda(x - z)}\,dx \\[2mm]
&= e^{\lambda z} \int_{0}^{\infty} \lambda e^{-2\lambda x}\,dx \\[2mm]
&= \frac{1}{2} e^{\lambda z} \qquad z \le 0
\end{aligned}
$$

[SOLUTION GAP: The exchange of the order of integration between the first and second lines (rewriting the region $\{x \le y+z,\ x,y\ge 0\}$ as $\{y \ge x-z,\ x \ge 0\}$) is done silently.]

$$
F_Z(z) =
\begin{cases}
1 - \dfrac{1}{2} e^{-\lambda z} & z \ge 0 \\[3mm]
\dfrac{1}{2} e^{\lambda z} & z < 0
\end{cases}
$$

$$
f_Z(z) = \frac{d}{dz} F_Z(z) =
\begin{cases}
\dfrac{\lambda}{2} e^{-\lambda z} & z \ge 0 \\[3mm]
\dfrac{\lambda}{2} e^{\lambda z} & z < 0
\end{cases}
$$

Hence,

$$
f_Z(z) = \frac{\lambda}{2} e^{\lambda |z|}
$$

[SOURCE TYPO?: The boxed conclusion is printed as $f_Z(z) = \frac{\lambda}{2}e^{\lambda|z|}$, but the case-by-case result (and the part (b) answer on page 3) is $f_Z(z) = \frac{\lambda}{2}e^{-\lambda|z|}$. The minus sign in the exponent is missing here.]

**(b)** Solving using the total probability theorem, we have:

$$
\begin{aligned}
f_Z(z) &= \int_{-\infty}^{\infty} f_X(x) f_{Z|X}(z\,|\,x)\,dx \\[2mm]
&= \int_{-\infty}^{\infty} f_X(x) f_{Y|X}(x - z\,|\,x)\,dx \\[2mm]
&= \int_{-\infty}^{\infty} f_X(x) f_Y(x - z)\,dx
\end{aligned}
$$

[SOLUTION GAP: The change of variable from $f_{Z|X}(z|x)$ to $f_{Y|X}(x-z|x)$ (using $Z = X - Y \Rightarrow Y = X - z$, whose Jacobian has magnitude 1) is asserted without justification; the last step uses independence of $X$ and $Y$ without comment.]

First when $z < 0$, we have:

$$
\begin{aligned}
\int_{-\infty}^{\infty} f_X(x) f_Y(x - z)\,dx
&= \int_{0}^{\infty} \lambda e^{-\lambda x}\,\lambda e^{-\lambda(x - z)}\,dx \\[2mm]
&= \lambda e^{\lambda z}\int_{0}^{\infty} \lambda e^{-2\lambda x}\,dx \\[2mm]
&= \frac{\lambda}{2} e^{\lambda z}
\end{aligned}
$$

[SOLUTION GAP: The restriction of the lower limit from $-\infty$ to $0$ — because $f_X(x)=0$ for $x<0$, and for $z<0$ the constraint $x-z\ge 0$ is automatic — is not stated.]

Then, when $z \ge 0$ we have:

$$
\begin{aligned}
\int_{-\infty}^{\infty} f_X(x) f_Y(x - z)\,dx
&= \int_{z}^{\infty} \lambda e^{-\lambda x}\,\lambda e^{-\lambda(x - z)}\,dx \\[2mm]
&= \lambda e^{\lambda z}\int_{z}^{\infty} \lambda e^{-2\lambda x}\,dx \\[2mm]
&= \frac{\lambda}{2} e^{\lambda z} e^{-2\lambda z} \\[2mm]
&= \frac{\lambda}{2} e^{-\lambda z}
\end{aligned}
$$

[SOLUTION GAP: The lower limit changing to $z$ (since $f_Y(x-z)=0$ unless $x \ge z$) is not explained.]

$$
f_Z(z) = \frac{\lambda}{2} e^{-\lambda |z|} \qquad \forall z
$$

---

## Problem 3 — Textbook Problem 4.16 (p. 248): polar coordinates of a standard normal pair

### Statement

Problem 4.16, page 248 in text.

Let $X$ and $Y$ be independent standard normal random variables. The pair $(X, Y)$ can be described in polar coordinates in terms of random variables $R \ge 0$ and $\Theta \in [0, 2\pi]$, so that

$$
X = R\cos\Theta, \qquad Y = R\sin\Theta.
$$

Show that $R$ and $\Theta$ are independent (i.e. show $f_{R,\Theta}(r, \theta) = f_R(r) f_\Theta(\theta)$).

(a) Find $f_R(r)$.

(b) Find $f_\Theta(\theta)$.

(c) Find $f_{R,\Theta}(r, \theta)$.

### Official solution

**(a)** We have $X = R\cos(\Theta)$ and $Y = R\sin(\Theta)$. Recall that in polar coordinates, the differential area is $dA = dx\,dy = r\,dr\,d\theta$. So

$$
\begin{aligned}
F_R(r) = \mathbf{P}(R \le r)
&= \int_{0}^{r}\!\!\int_{0}^{2\pi} f_X(r'\cos\theta) f_Y(r'\sin\theta)\,d\theta\; r'\,dr' \\[2mm]
&= \int_{0}^{r}\!\!\int_{0}^{2\pi} \frac{1}{2\pi} e^{-(r')^{2}/2}\,d\theta\; r'\,dr' \\[2mm]
&= \int_{0}^{r} r' e^{-(r')^{2}/2}\,dr' \int_{0}^{2\pi} \frac{d\theta}{2\pi} \\[2mm]
&= \int_{0}^{r^{2}/2} e^{-u}\,du \qquad (u = (r')^{2}/2)
\end{aligned}
$$

$$
F_R(r) =
\begin{cases}
1 - e^{-r^{2}/2} & r \ge 0 \\
0 & r < 0
\end{cases}
$$

$$
\begin{aligned}
f_R(r) = \frac{d}{dr} F_R(r) &= (-1/2)(2r)\left(-e^{-r^{2}/2}\right) \\[2mm]
&= r e^{-r^{2}/2}, \qquad r \ge 0
\end{aligned}
$$

[SOLUTION GAP: The step $f_X(r'\cos\theta)f_Y(r'\sin\theta) = \frac{1}{2\pi}e^{-(r')^2/2}$ uses $\frac{1}{\sqrt{2\pi}}e^{-x^2/2}\cdot\frac{1}{\sqrt{2\pi}}e^{-y^2/2}$ with $x^2+y^2=(r')^2$ — not shown. Also the evaluation $\int_0^{r^2/2} e^{-u}du = 1 - e^{-r^2/2}$ is skipped between the last display and the case expression.]

[SOURCE TYPO?: In the derivative line, the source writes $(-1/2)(2r)(-e^{-r^2/2})$; the chain-rule factors are grouped oddly (the two minus signs cancel to give $+re^{-r^2/2}$), so it is arithmetically correct but the placement of $(-1/2)$ makes the intermediate expression look like it came from differentiating $-e^{-r^2/2}$ rather than $1-e^{-r^2/2}$.]

**(b)**

$$
\begin{aligned}
F_\Theta(\theta) = \mathbf{P}(\Theta \le \theta)
&= \int_{0}^{\theta}\!\!\int_{0}^{\infty} f_X(r\cos\theta') f_Y(r\sin\theta')\,r\,dr\;d\theta' \\[2mm]
&= \int_{0}^{\theta}\!\!\int_{0}^{\infty} \frac{1}{2\pi} e^{-r^{2}/2}\,r\,dr\;d\theta' \\[2mm]
&= \int_{0}^{\infty} r e^{-r^{2}/2}\,dr \int_{0}^{\theta} \frac{d\theta'}{2\pi} \\[2mm]
&= \frac{\theta}{2\pi}\int_{0}^{\infty} e^{-u}\,du \qquad (u = r^{2}/2) \\[2mm]
&= \frac{\theta}{2\pi}\left(-e^{-u}\right)\bigg|_{0}^{\infty} = \frac{\theta}{2\pi} \qquad 0 \le \theta \le 2\pi
\end{aligned}
$$

$$
F_\Theta(\theta) =
\begin{cases}
0 & \theta < 0 \\
\dfrac{\theta}{2\pi} & 0 \le \theta \le 2\pi \\
1 & \theta \ge 2\pi
\end{cases}
$$

$$
f_\Theta(\theta) = \frac{d}{d\theta} F_\Theta(\theta) = \frac{1}{2\pi} \qquad 0 \le \theta \le 2\pi
$$

**(c)**

$$
\begin{aligned}
F_{R,\Theta}(r, \theta) = P(R \le r, \Theta \le \theta)
&= \int_{0}^{\theta}\!\!\int_{0}^{r} \frac{1}{2\pi} r' e^{-(r')^{2}/2}\,dr'\,d\theta' \\[2mm]
&= \int_{0}^{\theta}\!\!\int_{0}^{r^{2}/2} \frac{1}{2\pi} e^{-u}\,du\,d\theta' \qquad (u = (r')^{2}/2) \\[2mm]
&= \int_{0}^{\theta} \frac{1}{2\pi}\left(1 - e^{-r^{2}/2}\right) d\theta' \\[2mm]
&= \frac{\theta}{2\pi}\left(1 - e^{-r^{2}/2}\right) \qquad r \ge 0,\quad \theta > 2\pi
\end{aligned}
$$

[SOURCE TYPO?: The condition on the last line is printed "$r \ge 0,\ \theta > 2\pi$", but this branch is the one valid for $0 \le \theta \le 2\pi$, as the case expression immediately below confirms.]

$$
F_{R,\Theta}(r, \theta) =
\begin{cases}
\dfrac{\theta}{2\pi}\left(1 - e^{-r^{2}/2}\right) & r \ge 0,\quad 0 \le \theta \le 2\pi \\[3mm]
1 - e^{-r^{2}/2} & r \ge 0,\quad \theta > 2\pi \\[2mm]
0 & \text{otherwise}
\end{cases}
$$

$$
f_{R,\Theta}(r, \theta) = \frac{\partial}{\partial r}\frac{\partial}{\partial \theta} F_{R,\Theta}(r, \theta) = \frac{1}{2\pi} r e^{-r^{2}/2} \qquad r \ge 0,\quad 0 \le \theta \le 2\pi
$$

[SOLUTION GAP: The final conclusion that $f_{R,\Theta}(r,\theta) = f_R(r)f_\Theta(\theta) = \left(re^{-r^2/2}\right)\left(\tfrac{1}{2\pi}\right)$, and hence that $R$ and $\Theta$ are independent — which was the actual thing to "show" in the problem statement — is never stated explicitly; the reader must compare with parts (a) and (b).]

*Note:* The PDF of $R^{2}$ is exponentially distributed with parameter $\lambda = 1/2$. This is a very convenient way to generate normal random variables from independent uniform and exponential random variables. We can generate an arbitrary random variable $X$ with CDF $F_X$ by first generating a uniform random variable and then passing the samples from the uniform distribution through the function $F_X^{-1}$. But since we don't have a closed-form expression for the CDF of a normal random variable, this method doesn't work. However, we do have a closed-form expression for the exponential distribution. Therefore, we can generate an exponential distribution with parameter $1/2$ and we can generate a uniform distribution in $[0, 2\pi]$, and with these two distributions we can generate standard normal distributions.

[SOURCE TYPO?: "The PDF of $R^2$ is exponentially distributed" — a PDF is not itself distributed; the intended statement is "$R^2$ is exponentially distributed with parameter $\lambda = 1/2$."]

---

## Problem 4 — Textbook Problem 4.20 (p. 250): Schwarz inequality

### Statement

Problem 4.20, page 250 in text. **Schwarz inequality**.

Show that for any random variables $X$ and $Y$, we have

$$
(\mathbf{E}[XY])^{2} \le \mathbf{E}[X^{2}]\mathbf{E}[Y^{2}].
$$

### Official solution

Problem 4.20, page 250 in text. See text for the proof.

An alternative proof is given below:

Consider the problem of picking a parameter $\alpha$ to minimize the expected squared difference between two random variables $X$ and $Y$. Consider

$$
J(\alpha) = \mathbf{E}\left[(X - \alpha Y)^{2}\right]
$$

with $Y \ne 0$. We start with a variational calculation to find $\alpha$ that minimizes $J(\alpha)$. The value of $\alpha$ which minimizes $J(\alpha)$ is found by setting the first derivative of $J(\alpha)$ to zero (since, for $Y \ne 0$, $\frac{d^{2}}{d\alpha^{2}} J(\alpha) = 2\mathbf{E}[Y^{2}] > 0$).

[FIGURE: MATLAB-style line plot of a convex (parabolic) curve, drawn as a thin blue solid line inside a plain rectangular axes box with a light dotted grid (roughly 7 evenly spaced vertical dotted gridlines and 8 horizontal ones). Vertical axis labeled $J(\alpha)$, written horizontally (not rotated) just outside the left edge of the box, at about mid-height; horizontal axis labeled $\alpha$, centered below the box. No numeric tick labels or tick marks on either axis, and no drawn axis arrows. The parabola enters at the top-left corner of the box, descends, flattens to a single interior minimum located essentially at the horizontal center of the box (the minimum sits about one-fifth of the box height above the bottom edge), then rises symmetrically and exits at the top-right corner. A straight arrow runs from lower-right up-and-left, its head touching the curve just to the right of the minimum point; the label at the arrow's tail (inside the box, lower-right region) reads $\frac{dJ}{d\alpha} = 0$. | raster/rec12_sol_p05.png]

$$
\frac{d}{d\alpha} J(\alpha) = \frac{d}{d\alpha}\left(\mathbf{E}[X^{2}] - 2\alpha \mathbf{E}[XY] + \alpha^{2}\mathbf{E}[Y^{2}]\right) = 0
$$

$$
\rightarrow\ \alpha = \frac{\mathbf{E}[XY]}{\mathbf{E}[Y^{2}]} \text{ minimizes } J(\alpha).
$$

[SOLUTION GAP: The expansion $\mathbf{E}[(X-\alpha Y)^2] = \mathbf{E}[X^2] - 2\alpha\mathbf{E}[XY] + \alpha^2\mathbf{E}[Y^2]$ is used implicitly, and the differentiation itself ($-2\mathbf{E}[XY] + 2\alpha\mathbf{E}[Y^2] = 0$) is skipped — only the resulting $\alpha$ is stated.]

Then

$$
\begin{aligned}
J\!\left(\frac{\mathbf{E}[XY]}{\mathbf{E}[Y^{2}]}\right)
&= \mathbf{E}\left[\left(X - \frac{\mathbf{E}[XY]}{\mathbf{E}[Y^{2}]} Y\right)^{2}\right] \ge 0 \\[2mm]
&= \mathbf{E}[X^{2}] - 2\frac{(\mathbf{E}[XY])^{2}}{\mathbf{E}[Y^{2}]} + \frac{(\mathbf{E}[XY])^{2}\mathbf{E}[Y^{2}]}{(\mathbf{E}[Y^{2}])^{2}} \\[2mm]
&= \mathbf{E}[X^{2}] - \frac{(\mathbf{E}[XY])^{2}}{\mathbf{E}[Y^{2}]} \ge 0
\end{aligned}
$$

Rearranging this expression gives the Schwarz inequality for expected values:

$$
\mathbf{E}[X^{2}]\mathbf{E}[Y^{2}] \ge (\mathbf{E}[XY])^{2}
$$

Note that in the above derivation, we assumed $Y \ne 0$ so that $\mathbf{E}[Y^{2}] > 0$. If we assume $Y = 0$ then the Schwarz inequality will hold with equality since then $\mathbf{E}[XY] = 0$ and $\mathbf{E}[Y^{2}] = 0$.

[SOURCE TYPO?: The condition is written "$Y \ne 0$" / "$Y = 0$" (the random variable itself), where the mathematically relevant condition is $\mathbf{E}[Y^2] \ne 0$, i.e. $Y = 0$ with probability 1.]

---

## Back matter (both PDFs)

MIT OpenCourseWare, http://ocw.mit.edu
6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010
For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.
