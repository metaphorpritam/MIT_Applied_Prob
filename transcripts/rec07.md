# rec07 — Recitation 7 (September 30, 2010)

Covers: joint PMFs of two discrete random variables, the expected value rule for functions of two random variables, linearity of expectation, marginal PMFs, conditional PMFs and conditional expectation, independence and conditional independence of discrete random variables, expected number of tosses via recursive/total-expectation arguments.

Sources: MIT6_041F10_rec07.pdf, MIT6_041F10_rec07_sol.pdf

Massachusetts Institute of Technology
Department of Electrical Engineering & Computer Science
6.041/6.431: Probabilistic Systems Analysis (Fall 2010)

---

## Problem 1 — Expected value rule for a function of two random variables; linearity of expectation

### Statement

**Problem 2.35, page 130 in the text.** Verify the expected value rule

$$\mathbf{E}[g(X,Y)] = \sum_x \sum_y g(x,y)\, p_{X,Y}(x,y),$$

using the expected value rule for a function of a single random variable. Then, use the rule for the special case of a linear function, to verify the formula

$$\mathbf{E}[aX + bY] = a\mathbf{E}[X] + b\mathbf{E}[Y],$$

where $a$ and $b$ are given scalars.

### Official solution

See the textbook, Problem 2.35, page 130.

[SOLUTION GAP: The entire derivation is skipped — the solutions handout defers to the textbook. No verification of the expected value rule and no derivation of linearity of expectation is given in this document.]

---

## Problem 2 — Joint PMF on $\{1,2,3\}^2$ with unspecified entries

### Statement

Random variables $X$ and $Y$ can take any value in the set $\{1,2,3\}$. We are given the following information about their joint PMF, where the entries indicated by a $*$ are left unspecified:

[FIGURE: Scatter/dot diagram of a joint PMF on a 3×3 grid. Horizontal axis labeled $x$ with tick marks at 1, 2, 3; vertical axis labeled $y$ with tick marks at 1, 2, 3. Nine solid black dots sit at all grid points $(x,y)$, each annotated above with its probability mass:
 - Row $y=3$: at $x=1$ label "1/12"; at $x=2$ label "1/12"; at $x=3$ label "*".
 - Row $y=2$: at $x=1$ label "2/12"; at $x=2$ label "*"; at $x=3$ label "*".
 - Row $y=1$: at $x=1$ label "1/12"; at $x=2$ label "2/12"; at $x=3$ label "0".
| raster/rec07_p01.png]

Equivalent table form (rows = $y$, columns = $x$):

| $y \backslash x$ | 1 | 2 | 3 |
|---|---|---|---|
| 3 | 1/12 | 1/12 | * |
| 2 | 2/12 | * | * |
| 1 | 1/12 | 2/12 | 0 |

(a) What is $p_X(1)$?

(b) Provide a clearly labeled sketch of the conditional PMF of $Y$ given that $X = 1$.

(c) What is $\mathbf{E}[Y \mid X = 1]$?

(d) Is there a choice for the unspecified entries that would make $X$ and $Y$ independent?

Let $B$ be the event that $X \le 2$ and $Y \le 2$. We are told that conditioned on $B$, the random variables $X$ and $Y$ are independent.

(e) What is $p_{X,Y}(2,2)$?
(If there is not enough information to determine the answer, say so.)

(f) What is $p_{X,Y\mid B}(2,2 \mid B)$?
(If there is not enough information to determine the answer, say so.)

### Official solution

**(a)**

$$\begin{aligned}
p_X(1) &= \mathbf{P}(X=1, Y=1) + \mathbf{P}(X=1, Y=2) + \mathbf{P}(X=1, Y=3)\\
&= 1/12 + 2/12 + 1/12 = 1/3
\end{aligned}$$

**(b)** The solution is a sketch of the following conditional PMF:

$$p_{Y\mid X}(y \mid 1) = \frac{p_{Y,X}(y,1)}{p_X(1)} = \begin{cases}
1/4, & \text{if } y = 1,\\
1/2, & \text{if } y = 2,\\
1/4, & \text{if } y = 3,\\
0, & \text{otherwise.}
\end{cases}$$

[SOURCE TYPO?: the numerator is written $p_{Y,X}(y,1)$ (subscript order $Y,X$ with arguments $(y,1)$) rather than the $p_{X,Y}(1,y)$ notation used elsewhere in the solution; the two orderings are used inconsistently within the same document, although $p_{Y,X}(y,1)$ is itself self-consistent.]

[SOLUTION GAP: the requested "clearly labeled sketch" (bar plot of the conditional PMF over $y = 1,2,3$ with heights $1/4$, $1/2$, $1/4$) is not drawn in the solutions handout — only the formula is given. No figure appears here in the source.]

**(c)**

$$\mathbf{E}[Y \mid X = 1] = \sum_{y=1}^{3} y\, p_{Y\mid X}(y \mid 1) = 1\cdot\frac{1}{4} + 2\cdot\frac{1}{2} + 3\cdot\frac{1}{4} = 2$$

**(d)** Assume that $X$ and $Y$ are independent. Because $p_{X,Y}(3,1) = 0$ and $p_Y(1) = 1/4$, $p_X(3)$ must equal zero. This further implies $p_{X,Y}(3,2) = 0$ and $p_{X,Y}(3,3) = 0$. All the remaining probability mass must go to $(X,Y) = (2,2)$, making $p_{X,Y}(2,2) = 5/12$, $p_X(2) = 8/12$, and $p_Y(2) = 7/12$. However, $p_{X,Y}(2,2) \ne p_X(2)\cdot p_Y(2)$, contradicting the assumption; thus $X$ and $Y$ are not independent.

[SOLUTION GAP: the intermediate arithmetic is skipped — why $p_Y(1) = 1/4$ (i.e. $1/12 + 2/12 + 0$), how "all the remaining probability mass" ($1 - 7/12 = 5/12$) is forced into $(2,2)$, and the numerical check $p_X(2)\cdot p_Y(2) = (8/12)(7/12) = 56/144 \ne 5/12$ are all left to the reader.]

A simpler explanation uses only two $X$ values and two $Y$ values for which all four $(X,Y)$ pairs have specified probabilities. Note that if $X$ and $Y$ are independent, then $p_{X,Y}(1,3)/p_{X,Y}(1,1)$ and $p_{X,Y}(2,3)/p_{X,Y}(2,1)$ must be equal because they must both equal $p_Y(3)/p_Y(1)$. This necessary equality does not hold, so $X$ and $Y$ are not independent.

[SOLUTION GAP: the two ratios are not evaluated; the reader must check $p_{X,Y}(1,3)/p_{X,Y}(1,1) = (1/12)/(1/12) = 1$ versus $p_{X,Y}(2,3)/p_{X,Y}(2,1) = (1/12)/(2/12) = 1/2$.]

**(e)** Knowing that $X$ and $Y$ are conditionally independent given $B$, we must have

$$\frac{p_{X,Y}(1,1)}{p_{X,Y}(1,2)} = \frac{p_{X,Y}(2,1)}{p_{X,Y}(2,2)}$$

since the $(X,Y)$ pairs in the equality are all in $B$. Thus

$$p_{X,Y}(2,2) = \frac{p_{X,Y}(1,2)\, p_{X,Y}(2,1)}{p_{X,Y}(1,1)} = \frac{(2/12)(2/12)}{1/12} = \frac{4}{12} = \frac{1}{3}.$$

**(f)** Since $\mathbf{P}(B) = 9/12 = 3/4$, we normalize to obtain

$$p_{X,Y\mid B}(2,2) = \frac{p_{X,Y}(2,2)}{\mathbf{P}(B)} = 4/9.$$

[SOLUTION GAP: the computation of $\mathbf{P}(B)$ is skipped — it is $p_{X,Y}(1,1) + p_{X,Y}(2,1) + p_{X,Y}(1,2) + p_{X,Y}(2,2) = 1/12 + 2/12 + 2/12 + 4/12 = 9/12$. The final division $(1/3)/(3/4) = 4/9$ is also stated without steps.]

---

## Problem 3 — Expected number of tosses until two consecutive identical outcomes

### Statement

**Problem 2.33, page 128 in the text.** A coin that has probability of heads equal to $p$ is tossed successively and independently until a head comes twice in a row or a tail comes twice in a row. Find the expected value of the number of tosses.

### Official solution

See the textbook, Problem 2.33, page 128.

[SOLUTION GAP: The entire solution is skipped — the solutions handout defers to the textbook. No recursion, conditioning argument, or final closed-form expression for the expected number of tosses is given in this document.]

---

*Textbook problems are courtesy of Athena Scientific, and are used with permission.*

Both PDFs end with a second page containing only MIT OpenCourseWare boilerplate:
"MIT OpenCourseWare, http://ocw.mit.edu, 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010. For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms."
