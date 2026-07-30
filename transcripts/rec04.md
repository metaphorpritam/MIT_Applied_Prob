# rec04 — Recitation 4 (September 21, 2010)

Covers: Counting / combinatorics — the birthday problem, non-attacking rook placements on a chessboard, hypergeometric probabilities, derivation of the multinomial coefficient via slot-arrangements, multinomial probabilities.

Sources: MIT6_041F10_rec04.pdf (questions, incl. "Recitation 4: Extra Handout"), MIT6_041F10_rec04_sol.pdf (official solutions)

Course header on every page: Massachusetts Institute of Technology, Department of Electrical Engineering & Computer Science, 6.041/6.431: Probabilistic Systems Analysis (Fall 2010). Footer on the question page and on the Extra Handout page: "Textbook problems are courtesy of Athena Scientific, and are used with permission." (right side: "Page 1 of 1"). The solution pages carry no Athena footer, only "Page 1 of 2" / "Page 2 of 2". Solution header reads "Recitation 4 Solutions / September 21, 2010"; the Extra Handout is a separate one-page document headed "Recitation 4: Extra Handout / September 21, 2010". Both PDFs end with an MIT OpenCourseWare boilerplate page (http://ocw.mit.edu, "6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010", terms-of-use notice).

---

## Problem 1 — The birthday problem

### Statement

Problem 1.50, page 67 in the text.

**The birthday problem.** Consider $n$ people who are attending a party. We assume that every person has an equal probability of being born on any day during the year, independently of everyone else, and ignore the additional complication presented by leap years (i.e., nobody is born on February 29). What is the probability that each person has a distinct birthday?

**Extra Handout, item 1 (Recitation 4: Extra Handout, September 21, 2010):** As part of the solution to problem 1, plotted below are the probabilities of each person having a distinct birthday versus $n$ the number of people present.

[FIGURE: Two stacked line/marker plots (green open-square markers connected along a smooth decreasing curve), enclosed in a single black rectangular border, captioned "Image by MIT OpenCourseWare." TOP PANEL: linear-scale plot of $P(n)$ (y-axis, bold label "P(n)", ticks 0.0, 0.2, 0.4, 0.6, 0.8, 1.0) versus $n$ (x-axis, bold label "n", ticks 0, 20, 40, 60, 80), light-blue dashed gridlines, blue axis frame. The curve starts at $P\approx 1.0$ at $n=0$, has a sigmoid-like fall crossing $P=0.5$ near $n\approx 23$, is near $0.1$ by $n\approx 40$, and is visually flat at 0 from about $n\approx 60$ onward. BOTTOM PANEL: same quantity on a logarithmic y-axis, $P(n)$ ticks from $10^{0}$ down to $10^{-10}$ (decades $10^0,10^{-1},\dots,10^{-10}$), x-axis $n$ with ticks 0, 20, 40, 60, 80, 100, 120, 140, light-blue dashed gridlines. The curve starts flat near $10^{0}$ for small $n$ and bends steadily downward with increasing (concave) steepness, reaching $10^{-10}$ at about $n\approx 122$, where the data ends. | raster/rec04_p02.png]

[FIGURE: The identical two-panel figure (linear $P(n)$ vs $n$ on top, log-scale $P(n)$ vs $n$ below, green open-square markers, black surrounding border, "Image by MIT OpenCourseWare." caption) is reproduced inside the official solution to Problem 1. | raster/rec04_sol_p01.png]

### Official solution

The sample space consists of all possible choices for the birthday of each person. Since there are $n$ persons, and each has 365 choices for their birthday, the sample space has $365^n$ elements. Let us now consider those choices of birthdays for which no two persons have the same birthday. Assuming that $n \le 365$, there are 365 choices for the first person, 364 for the second, etc., for a total of $365 \cdot 364 \cdots (365 - n + 1)$. Thus,

$$\mathbf{P}(\text{no two birthdays coincide}) = \frac{365 \cdot 364 \cdots (365 - n + 1)}{365^n}.$$

It is interesting to note that for $n$ as small as 23, the probability that there are two persons with the same birthday is larger than $1/2$.

[The two-panel plot described above appears here in the solution PDF.]

---

## Problem 2 — 8 non-attacking rooks on a chessboard

### Statement

Imagine that 8 rooks are randomly placed on a chessboard. Find the probability that all the rooks will be safe from one another, i.e. that there is no row or column with more than one rook.

### Official solution

As we have done before, we will count the number of favorable positions in which we can safely place 8 rooks, and then divide this by the total number of positions for 8 rooks on a $8 \times 8$ chessboard. First we count the number of favorable positions for the rooks. We will place the rooks one by one. For the first rook, there are no constraints, so we have 64 choices. Placing this rook, however, eliminates one row and one column. Thus for our second rook, we can imagine that the illegal column and row have been removed, thus leaving us with a $7 \times 7$ chessboard, and thus with 49 choices. Similarly, for the third rook we have 36 choices, for the fourth 25, etc... There are $64 \cdot 63 \cdots 57$ total ways we can place 8 rooks without any restrictions, and therefore the probability we are after is:

$$\frac{64 \cdot 49 \cdot 36 \cdot 25 \cdot 16 \cdot 9 \cdot 4}{\frac{64!}{56!}}.$$

[SOURCE TYPO?: The numerator lists only 7 factors ($8^2, 7^2, 6^2, 5^2, 4^2, 3^2, 2^2$) for 8 rooks; by the stated one-by-one argument the eighth rook has $1^2 = 1$ choice, so the product should be $64 \cdot 49 \cdot 36 \cdot 25 \cdot 16 \cdot 9 \cdot 4 \cdot 1 = (8!)^2$. The written product is numerically equal (since the missing factor is 1), but the pattern is visibly truncated.]

[SOLUTION GAP: The solution does not note that this ordered count treats the 8 rooks as distinguishable in both numerator and denominator (hence the ordering factors cancel), nor does it simplify the answer to a closed form such as $(8!)^2 \cdot 56!/64! = 8!/\binom{64}{8}$ or give a numerical value. It also does not restate the denominator $64 \cdot 63 \cdots 57$ as $64!/56!$ explicitly in words — it simply switches notation between the sentence and the displayed fraction.]

---

## Problem 3 — Hypergeometric probabilities

### Statement

Problem 1.61, page 69 in the text.

**Hypergeometric probabilities.** An urn contains $n$ balls, out of which exactly $m$ are red. We select $k$ of the balls at random, without replacement (i.e., selected balls are not put back into the urn before the next selection). What is the probability that $i$ of the selected balls are red?

### Official solution

See textbook, Problem 1.61, page 69.

[SOLUTION GAP: The entire solution is deferred to the textbook. No derivation, no formula, and no numerical answer is given in the recitation solution PDF.]

---

## Problem 4 — Multinomial coefficient (slot/segment derivation)

### Statement

**Multinomial coefficient.** Derive the multinomial coefficient (the number of partitions of $n$ distinct items into groups of $n_1, \ldots, n_r$) using a different argument than the one in class. Consider $n$ items which can be placed into $n$ slots and divide the group of $n$ slots into segments of length $n_1, \ldots, n_r$ slots. Derive the multinomial coefficient by showing how many different ways can the $n$ items be arranged into the $r$ segments.

### Official solution

The group of $n$ slots is divided into segments of length $n_1, \ldots, n_r$ slots. The $n$ items can be arranged in $n!$ ways, where each arrangement corresponds to a partition into the $r$ segments. But all arrangements within a single segment lead to the same partition, where there are $n_i!$ ways to arrange the items within $i$th segment. Thus, for each segment we must divide by the number of ways to arrange the items within that segment. The solution is then:

$$\frac{\text{Ways to arrange } n \text{ items}}{(\text{Ways to arrange items in segment } 1) \cdots (\text{Ways to arrange items in segment r})} = \frac{n!}{n_1! \cdots n_r!}$$

[SOLUTION GAP: The solution does not explicitly verify that the map from arrangements to partitions is exactly $n_1!\cdots n_r!$-to-one (i.e. that every partition arises from the same number of arrangements), nor does it state the constraint $n_1 + \cdots + n_r = n$, nor write the result in the notation $\binom{n}{n_1,\ldots,n_r}$.]

---

## Problem 5 — Multinomial probabilities

### Statement

**Multinomial probabilities.** At each draw, there is a probability $p_i$ ($i = 1, \ldots, r$) of getting a ball of color $i$. Draw $n$ objects. What is the probability of obtaining exactly $n_i$ of each color $i$?

### Official solution

The probability of drawing a particular sequence of balls containing exactly $n_i$ of color $i$ balls is $p_1^{n_1} \cdots p_r^{n_r}$. The number of possible sequences containing $n_i$ of color $i$ balls is the number of ways to form a partition of $n$ distinct slots into subsets of cardinality $n_1, \ldots, n_r$ which is $\binom{n}{n_1, \ldots, n_r}$. Therefore, the probability of obtaining exactly $n_i$ balls of color $i$ is:

$$\binom{n}{n_1, \ldots, n_r} p_1^{n_1} \cdots p_r^{n_r}$$

[SOLUTION GAP: The solution does not state the independence of successive draws (which is what makes every particular sequence have probability $p_1^{n_1}\cdots p_r^{n_r}$), does not state the constraint $n_1 + \cdots + n_r = n$ (and $\sum_i p_i = 1$), and does not expand $\binom{n}{n_1,\ldots,n_r} = n!/(n_1!\cdots n_r!)$ using the Problem 4 result.]
