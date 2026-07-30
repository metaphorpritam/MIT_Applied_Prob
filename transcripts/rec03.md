# rec03 — Recitation 3 (September 16, 2010)

Covers: independence of events, conditional independence, independent trials / random walk (drunk tightrope walker), binary symmetric-type noisy communication channel with unequal error probabilities, majority-rule repetition coding, Bayes' rule for decoding, independence of an event with itself, independence of $A$ and $B^c$, conditional independence given an independent event.

Sources: MIT6_041F10_rec03.pdf (problems), MIT6_041F10_rec03_sol.pdf (solutions)

Header block on every content page: Massachusetts Institute of Technology, Department of Electrical Engineering & Computer Science, 6.041/6.431: Probabilistic Systems Analysis (Fall 2010), followed by a horizontal rule.

Title line on the problem set: "Recitation 3: September 16, 2010". Title lines on the solution set (two centered bold lines): "Recitation 3: Solutions" / "September 16, 2010".

Footer on the question pages: left, "Textbook problems are courtesy of Athena Scientific, and are used with permission."; right, "Page 1 of 2" (raster/rec03_p01.png) and "Page 2 of 2" (raster/rec03_p02.png). The solutions page has no Athena Scientific footer — only the right-hand "Page 1 of 1" (raster/rec03_sol_p01.png), i.e. the entire solution set is one page.

---

## Problem 1 — Two fair coin tosses: unconditional vs. conditional independence

### Statement

Example 1.20, page 37 in the text.

Consider two independent fair coin tosses, in which all four possible outcomes are equally likely. Let

$$
\begin{aligned}
H_1 &= \{\text{1st toss is a head}\},\\
H_2 &= \{\text{2nd toss is a head}\},\\
D &= \{\text{the two tosses produced different results}\}.
\end{aligned}
$$

(a) Are the events $H_1$ and $H_2$ (unconditionally) independent?

(b) Given event $D$ has occurred, are the events $H_1$ and $H_2$ (conditionally) independent?

### Official solution

1. See the textbook, Example 1.20, page 37.

[SOLUTION GAP: The entire solution is deferred to the textbook. No computation of $\mathbf{P}(H_1)$, $\mathbf{P}(H_2)$, $\mathbf{P}(H_1\cap H_2)$, nor of the conditional probabilities $\mathbf{P}(H_1\mid D)$, $\mathbf{P}(H_2\mid D)$, $\mathbf{P}(H_1\cap H_2\mid D)$ is given, and no conclusion (independent unconditionally, not conditionally independent given $D$) is stated in the handout.]

---

## Problem 2 — Drunk tightrope walker (random walk)

### Statement

Imagine a drunk tightrope walker, in the middle of a really long tightrope, who manages to keep his balance, but takes a step forward with probability $p$ and takes a step back with probability $(1-p)$.

(a) What is the probability that after two steps the tightrope walker will be at the same place on the rope?

(b) What is the probability that after three steps, the tightrope walker will be one step forward from where he began?

(c) Given that after three steps he has managed to move ahead one step, what is the probability that the first step he took was a step forward?

### Official solution

**(a)** In order to wind up in the same place after two steps, the tightrope walker can either step forwards, then backwards, or vice versa. Therefore the required probability is:

$$2 \cdot p \cdot (1-p).$$

**(b)** The probability that after three steps he will be one step ahead of his starting point is the probability that out of 3 steps in total, 2 of them are forwards, and one is backwards. This equals:

$$3 \cdot p^{2} \cdot (1-p).$$

**(c)** Given that out of his three steps only one is backwards, the sample space for the experiment is:

$$\{(F,F,B);\,(F,B,F);\,(B,F,F)\}$$

where $F$ denotes a step forwards, and $B$ a step backwards. Each of these sample points is equally likely, therefore the probability that his first step is a step forward is $\frac{2}{3}$.

[SOLUTION GAP: In (a) the solution does not spell out the independence argument $\mathbf{P}(FB) = p(1-p)$ and $\mathbf{P}(BF) = (1-p)p$ before adding them. In (b) the combinatorial factor $3 = \binom{3}{2}$ is asserted without derivation. In (c) the claim that the three conditional sample points are equally likely is asserted without the explicit computation $\mathbf{P}(\text{each}) = p^2(1-p)$ and without writing the conditional-probability ratio $\mathbf{P}(\text{first step }F \mid \text{one step ahead}) = 2p^2(1-p)/\big(3p^2(1-p)\big)$.]

---

## Problem 3 — Communication through a noisy channel

### Statement

Problem 1.31, page 60 in the text.

**Communication through a noisy channel.** A binary (0 or 1) message transmitted through a noisy communication channel is received incorrectly with probability $\epsilon_0$ and $\epsilon_1$, respectively (see the figure). Errors in different symbol transmissions are independent. The channel source transmits a 0 with probability $p$ and transmits a 1 with probability $1-p$.

[FIGURE: Binary channel transition diagram ("butterfly" / crossover diagram). Two transmitted symbols on the left, labeled 0 (top-left) and 1 (bottom-left); two received symbols on the right, labeled 0 (top-right) and 1 (bottom-right). Four straight arrows, each pointing left-to-right: (i) horizontal top arrow from left 0 to right 0, labeled "1-e0" (i.e. $1-\epsilon_0$) above it; (ii) diagonal arrow from left 0 down to right 1, labeled "e0" ($\epsilon_0$) near its upper portion; (iii) diagonal arrow from left 1 up to right 0, labeled "e1" ($\epsilon_1$) near its lower portion; (iv) horizontal bottom arrow from left 1 to right 1, labeled "1-e1" ($1-\epsilon_1$) below it. The two diagonals cross in the middle. Caption: "Figure 1: Error probabilities in a binary communication channel." Note: the figure renders the epsilons as plain "e0"/"e1" while the body text uses $\epsilon_0$, $\epsilon_1$. | raster/rec03_p01.png]

(a) What is the probability that a randomly chosen symbol is received correctly?

(b) Suppose that the string of symbols 1011 is transmitted. What is the probability that all the symbols in the string are received correctly?

(c) In an effort to improve reliability, each symbol is transmitted three times and the received symbol is decoded by majority rule. In other words, a 0 (or 1) is transmitted as 000 (or 111, respectively), and it is decoded at the receiver as a 0 (or 1) if and only if the received three-symbol string contains at least two 0s (or 1s, respectively). What is the probability that a transmitted 0 is correctly decoded?

(d) Suppose that the scheme of part (c) is used. What is the probability that a 0 was transmitted given that the received string is 101?

### Official solution

3. See the textbook, Problem 1.31, page 60.

[SOLUTION GAP: The entire solution is deferred to the textbook. None of parts (a)–(d) is worked in the handout — no total-probability computation $p(1-\epsilon_0) + (1-p)(1-\epsilon_1)$ for (a), no product $(1-\epsilon_1)(1-\epsilon_0)(1-\epsilon_1)(1-\epsilon_1)$ for (b), no majority-rule expression $(1-\epsilon_0)^3 + 3(1-\epsilon_0)^2\epsilon_0$ for (c), and no Bayes' rule computation for (d).]

---

## Problem 4 — Independence: self-independence, complements, conditional independence

### Statement

(a) Can an event $A$ be independent of itself?

(b) Problem 1.43(a) on page 63 in text.

Let $A$ and $B$ be independent events. Use the definition of independence to prove that the events $A$ and $B^c$ are independent.

(c) Problem 1.44 on page 64 in text.

Let $A$, $B$, and $C$ be independent events, with $\mathbf{P}(C) > 0$. Prove that $A$ and $B$ are conditionally independent of $C$.

[SOURCE TYPO?: In (c) the phrase "conditionally independent of $C$" is loose wording; the intended statement is that $A$ and $B$ are conditionally independent *given* $C$. The handout reproduces the textbook phrasing verbatim.]

### Official solution

**(a)** $A$ is independent of itself if and only if $\mathbf{P}(A \cap A) = \mathbf{P}(A)\mathbf{P}(A)$. Since $A \cap A = A$ then $A$ must satisfy $\mathbf{P}(A) = (\mathbf{P}(A))^{2}$. Therefore, $A$ is independent of itself if and only if $\mathbf{P}(A) = 1$ or $\mathbf{P}(A) = 0$.

**(b)** See solution to Problem 1.43(a) in text on pages 63-64.

**(c)** See solution to Problem 1.44 in text on page 64.

[SOLUTION GAP: (b) and (c) are deferred entirely to the textbook. No proof of $\mathbf{P}(A \cap B^c) = \mathbf{P}(A) - \mathbf{P}(A\cap B) = \mathbf{P}(A)(1-\mathbf{P}(B))$ is given for (b), and no proof that $\mathbf{P}(A\cap B \mid C) = \mathbf{P}(A\mid C)\mathbf{P}(B\mid C)$ is given for (c). In (a) the algebraic step from $\mathbf{P}(A) = \mathbf{P}(A)^2$ to $\mathbf{P}(A)\in\{0,1\}$ is stated without the factorization $\mathbf{P}(A)(1-\mathbf{P}(A))=0$.]

---

## Back matter (both PDFs)

Final page of each PDF is the standard MIT OpenCourseWare notice:

> MIT OpenCourseWare
> http://ocw.mit.edu
> 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability
> Fall 2010
> For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

(raster/rec03_p03.png and raster/rec03_sol_p02.png — no figures, boilerplate only.)
