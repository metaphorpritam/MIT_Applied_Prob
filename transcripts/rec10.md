# rec10 — Recitation 10 (October 12, 2010)

Covers: probability identities / true-false conceptual checks (unions, complements, conditional probability, variance scaling), sequential sample spaces for repeated coin tosses, conditional probability and Bayes-style inversion, PMF of a discrete random variable from a sequential model, total expectation theorem, conditional PMF given an event, geometric random variable and expectation of a randomly terminated game.

Sources: MIT6_041F10_rec10.pdf (questions), MIT6_041F10_rec10_sol.pdf (solutions)

Solution document header note: "Recitation 10 Solutions (6.041/6.431 Spring 2010 Quiz 1 Solutions)" — the recitation reuses the Spring 2010 Quiz 1 and its official solutions.

No figures, plots, diagrams, or trees appear anywhere in either PDF; all content is text, formulas, and two small aligned tables (transcribed below as tables). Specifically: the 2.1 answer is a two-column aligned list (outcome / probability, no rules), and the 3.1 answer is a three-column ruled table with header row $\omega$ | $\mathbf{P}(\{\omega\})$ | $X(\omega)$.

Page structure: questions PDF = 2 content pages ("Page 1 of 2", "Page 2 of 2") plus a final MIT OpenCourseWare back-matter page; solutions PDF = 3 content pages ("Page 1 of 3" … "Page 3 of 3") plus the same back-matter page. Both back-matter pages read: "MIT OpenCourseWare / `http://ocw.mit.edu` / 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability / Fall 2010 / For information about citing these materials or our Terms of Use, visit: `http://ocw.mit.edu/terms`." — boilerplate only, no course content.

Every page of both PDFs carries the running header: "MASSACHUSETTS INSTITUTE OF TECHNOLOGY / Department of Electrical Engineering & Computer Science / 6.041/6.431: Probabilistic Systems Analysis / (Fall 2010)".

---

## Problem 1 — True/false identities (multiple choice)

### Statement

**Question 1.** The two parts of this question are about identities for a probabilistic model with sample space $\Omega$, events $A$ and $B$, and discrete random variable $X$. Any time conditioning on an event is indicated, the event has positive probability. An identity is *true* when it holds without any additional restrictions; it is *false* when there is any counterexample.

**1.1.** Which **one** of the following statements is **true**?

- (a) $\mathbf{P}(A \cap B)$ may be larger than $\mathbf{P}(A)$.
- (b) The variance of $X$ may be larger than the variance of $2X$.
- (c) If $A^c \cap B^c = \emptyset$, then $\mathbf{P}(A \cup B) = 1$.
- (d) If $A^c \cap B^c = \emptyset$, then $\mathbf{P}(A \cap B) = \mathbf{P}(A)\mathbf{P}(B)$.
- (e) If $\mathbf{P}(A) > 1/2$ and $\mathbf{P}(B) > 1/2$, then $\mathbf{P}(A \cup B) = 1$.

**1.2.** Which **one** of the following statements is **true**?

- (a) If $\mathbf{E}[X] = 0$, then $\mathbf{P}(X > 0) = \mathbf{P}(X < 0)$.
- (b) $\mathbf{P}(A) = \mathbf{P}(A \mid B) + \mathbf{P}(A \mid B^c)$
- (c) $\mathbf{P}(B \mid A) + \mathbf{P}(B \mid A^c) = 1$
- (d) $\mathbf{P}(B \mid A) + \mathbf{P}(B^c \mid A^c) = 1$
- (e) $\mathbf{P}(B \mid A) + \mathbf{P}(B^c \mid A) = 1$

### Official solution

**1.1.** Answer: **(c) is true because $A \cup B = (A^c \cap B^c)^c = \emptyset^c = \Omega$.**

[SOLUTION GAP: no counterexamples or refutations are given for the four false options (a), (b), (d), (e); only the correct choice is justified.]

**1.2.** Answer: **(e) is true because $B$ and $B^c$ partition $\Omega$.**

[SOLUTION GAP: no counterexamples are given for options (a)–(d); only the correct choice is justified.]

---

## Problem 2 — Heather and Taylor's unfair-coin game

### Statement

**Question 2.** *Provide **clear reasoning**; partial credit is possible*

Heather and Taylor play a game using independent tosses of an unfair coin. A head comes up on any toss with probability $p$, where $0 < p < 1$. The coin is tossed repeatedly until either the second time head comes up, in which case Heather wins; or the second time tail comes up, in which case Taylor wins. Note that a full game involves 2 or 3 tosses.

**2.1.** Consider a probabilistic model for the game in which the outcomes are the sequences of heads and tails in a full game. Provide a list of the outcomes and their probabilities of occurring.

**2.2.** What is the probability that Heather wins the game?

**2.3.** What is the conditional probability that Heather wins the game given that head comes up on the first toss?

**2.4.** What is the conditional probability that head comes up on the first toss given that Heather wins the game?

### Official solution

**2.1.** Because of the independence of the coin tosses, the outcomes and their probabilities are as follows:

| Outcome | Probability |
|---|---|
| **HH** | $p^2$ |
| **HTH** | $p^2(1-p)$ |
| **HTT** | $p(1-p)^2$ |
| **THH** | $p^2(1-p)$ |
| **THT** | $p(1-p)^2$ |
| **TT** | $(1-p)^2$ |

**2.2.** The event of Heather winning is $\{\mathbf{HH}, \mathbf{HTH}, \mathbf{THH}\}$. Adding the probabilities of the outcomes in this event gives

$$p^2 + p^2(1-p) + p^2(1-p) = p^2(3-2p).$$

**2.3.**

$$
\begin{aligned}
\mathbf{P}(\{\text{Heather wins}\} \mid \{\text{first toss H}\})
&= \frac{\mathbf{P}(\{\text{Heather wins}\} \cap \{\text{first toss H}\})}{\mathbf{P}(\{\text{first toss H}\})} \\[4pt]
&= \frac{\mathbf{P}(\{\mathbf{HH},\ \mathbf{HTH}\})}{\mathbf{P}(\{\text{first toss H}\})} \\[4pt]
&= \frac{p^2 + p^2(1-p)}{p} \;=\; p(2-p)
\end{aligned}
$$

[SOLUTION GAP: the denominator $\mathbf{P}(\{\text{first toss H}\}) = p$ is substituted without comment, and the algebra $\big(p^2 + p^2(1-p)\big)/p = p(2-p)$ is done in one step.]

**2.4.**

$$
\begin{aligned}
\mathbf{P}(\{\text{first toss H}\} \mid \{\text{Heather wins}\})
&= \frac{\mathbf{P}(\{\text{first toss H}\} \cap \{\text{Heather wins}\})}{\mathbf{P}(\{\text{Heather wins}\})} \\[4pt]
&= \frac{\mathbf{P}(\{\mathbf{HH},\ \mathbf{HTH}\})}{\mathbf{P}(\{\text{Heather wins}\})} \\[4pt]
&= \frac{p^2 + p^2(1-p)}{p^2(3-2p)} \;=\; \frac{2-p}{3-2p}
\end{aligned}
$$

[SOLUTION GAP: the cancellation $\big(p^2 + p^2(1-p)\big)/\big(p^2(3-2p)\big) = (2-p)/(3-2p)$ is shown in a single step.]

---

## Problem 3 — Casino game with a fair 4-sided die (bonus rolls)

### Statement

**Question 3.** *Provide **clear reasoning**; partial credit is possible*

A casino game using a **fair** 4-sided die (with labels 1, 2, 3, and 4) is offered in which a **basic game** has 1 or 2 die rolls:

- If the first roll is a 1, 2, or 3, the player wins the amount of the die roll, in dollars, and the game is over.
- If the first roll is a 4, the player wins \$2 and the amount of a second ("bonus") die roll in dollars.

Let $X$ be the payoff in dollars of the basic game.

**3.1.** Find the PMF of $X$, $p_X(x)$.

**3.2.** Find $\mathbf{E}[X]$.

**3.3.** Find the conditional PMF of the result of the first die roll given that $X = 3$. (Use a reasonable notation that you define explicitly.)

**3.4.** Now consider an **extended game** that can have any number of bonus rolls. Specifically:

- $*$ Any roll of a 1, 2, or 3 results in the player winning the amount of the die roll, in dollars, and the termination of the game.
- $*$ Any roll of a 4 results in the player winning \$2 and continuation of the game.

Let $Y$ denote the payoff in dollars of the extended game. Find $\mathbf{E}[Y]$.

### Official solution

**3.1.** Define a probabilistic model in which the outcomes are the sequences of rolls in a full game. The outcomes, their probabilities, and the resulting values of $X$ are as follows:

| $\omega$ | $\mathbf{P}(\{\omega\})$ | $X(\omega)$ |
|---|---|---|
| $(1)$ | $1/4$ | $1$ |
| $(2)$ | $1/4$ | $2$ |
| $(3)$ | $1/4$ | $3$ |
| $(4,1)$ | $1/16$ | $3$ |
| $(4,2)$ | $1/16$ | $4$ |
| $(4,3)$ | $1/16$ | $5$ |
| $(4,4)$ | $1/16$ | $6$ |

By gathering the probabilities of the possible values for $X$, we obtain

$$
p_X(x) \;=\;
\begin{cases}
1/4, & \textbf{for } x = 1, 2;\\
5/16, & \textbf{for } x = 3;\\
1/16, & \textbf{for } x = 4, 5, 6;\\
0, & \textbf{otherwise}.
\end{cases}
$$

[SOLUTION GAP: the value $p_X(3) = 5/16$ is obtained by combining $\mathbf{P}(\{(3)\}) = 1/4$ and $\mathbf{P}(\{(4,1)\}) = 1/16$, but this addition $1/4 + 1/16 = 5/16$ is not written out.]

**3.2.** It does not take too much arithmetic to compute $\mathbf{E}[X]$ using the PMF computed in the previous part. A more elegant solution is to use the total expectation theorem. Let $A$ be the event that the first roll is a 4. Then

$$
\mathbf{E}[X] \;=\; \underbrace{\mathbf{P}(A)}_{1/4}\,\underbrace{\mathbf{E}[X \mid A]}_{4.5} \;+\; \underbrace{\mathbf{P}(A^c)}_{3/4}\,\underbrace{\mathbf{E}[X \mid A^c]}_{2} \;=\; \frac{21}{8},
$$

where $\mathbf{E}[X \mid A] = 4.5$ because the conditional distribution is uniform on $\{3, 4, 5, 6\}$; and $\mathbf{E}[X \mid A^c] = 2$ because the conditional distribution is uniform on $\{1, 2, 3\}$.

(The under-braced values $1/4$, $4.5$, $3/4$, $2$ are typeset beneath the corresponding factors in the original.)

[SOLUTION GAP: the final arithmetic $\tfrac14 \cdot 4.5 + \tfrac34 \cdot 2 = \tfrac{21}{8}$ is not shown.]

**3.3.** Let $Z$ be the result of the first die roll, and let $B = \{X = 3\}$. By definition of conditioning,

$$
p_{Z\mid B}(z) \;=\; \frac{\mathbf{P}(\{Z = z\} \cap B)}{\mathbf{P}(B)}.
$$

By using values tabulated above,

$$
p_{Z\mid B}(z) \;=\;
\begin{cases}
4/5, & \textbf{for } z = 3;\\
1/5, & \textbf{for } z = 4;\\
0, & \textbf{otherwise}.
\end{cases}
$$

[SOLUTION GAP: the numerical evaluation is omitted — namely $\mathbf{P}(B) = 5/16$, $\mathbf{P}(\{Z=3\} \cap B) = 1/4$, $\mathbf{P}(\{Z=4\} \cap B) = 1/16$, giving $(1/4)/(5/16) = 4/5$ and $(1/16)/(5/16) = 1/5$.]

**3.4.** One could explicitly find the PMF of $Y$, but this is unnecessarily messy. Instead, let $L$ be the payoff of the last roll and let $W$ be the payoff of all of the earlier rolls. Then $Y = W + L$ by construction, and $\mathbf{E}[Y] = \mathbf{E}[W] + \mathbf{E}[L]$.

The last roll is uniformly distributed on $\{1, 2, 3\}$, so $\mathbf{E}[L] = 2$. The winnings on earlier rolls is $2(N-1)$ where $N$ is the number of rolls in the game. Since termination of the game can be seen as "success" on a Bernoulli trial with success probability of $3/4$, $N$ has the geometric distribution with parameter $3/4$. Thus,

$$
\mathbf{E}[W] \;=\; \mathbf{E}[2(N-1)] \;=\; 2\mathbf{E}[N] - 2 \;=\; 2 \cdot \frac{4}{3} - 2 \;=\; \frac{2}{3}.
$$

Combining the calculations,

$$
\mathbf{E}[Y] \;=\; \mathbf{E}[W] + \mathbf{E}[L] \;=\; \frac{2}{3} + 2 \;=\; \frac{8}{3}.
$$

(Many other methods of solution are possible.)

[SOLUTION GAP: the standard geometric-mean fact $\mathbf{E}[N] = 1/(3/4) = 4/3$ is used without derivation, and the claim that the last roll is uniform on $\{1,2,3\}$ (i.e. that $L$ is independent of $N$ in the needed sense) is asserted rather than justified.]
