# rec02 — Recitation 2 (September 14, 2010)

Covers: conditional probability, comparing conditional probabilities under different conditioning events, discrete uniform sample spaces (two dice), total probability theorem, Bayes' rule (chess tournament), sequential/tree models and the Monty Hall problem

Sources: MIT6_041F10_rec02.pdf (questions), MIT6_041F10_rec02_sol.pdf (solutions)

Course header (appears on every page of both PDFs):
Massachusetts Institute of Technology — Department of Electrical Engineering & Computer Science — 6.041/6.431: Probabilistic Systems Analysis (Fall 2010)

Footnote on question page 1: "Textbook problems are courtesy of Athena Scientific, and are used with permission."

---

## Problem 1 — Alice's two-heads claim (Problem 1.15, page 56–57 in the text)

### Statement

Problem 1.15, page 56-57 in the text.

A coin is tossed twice. Alice claims that the event of two heads is at least as likely if we know that the first toss is a head than if we know that at least one of the tosses is a head. Is she right? Does it make a difference if the coin is fair or unfair? How can we generalize Alice's reasoning?

### Official solution

Let $A$ be the event that the first toss is a head and let $B$ be the event that the second toss is a head. We must compare the conditional probabilities $\mathbf{P}(A\cap B\mid A)$ and $\mathbf{P}(A\cap B\mid A\cup B)$. We have

$$\mathbf{P}(A \cap B\mid A) = \frac{\mathbf{P}((A \cap B) \cap A)}{\mathbf{P}(A)} = \frac{\mathbf{P}(A \cap B)}{\mathbf{P}(A)},$$

and

$$\mathbf{P}(A \cap B\mid A \cup B) = \frac{\mathbf{P}((A \cap B) \cap (A \cup B))}{\mathbf{P}(A \cup B)} = \frac{A \cap B}{A \cup B}.$$

[SOURCE TYPO?: the final fraction is printed in the PDF as $\dfrac{A\cap B}{A\cup B}$ — the $\mathbf{P}(\cdot)$ operators are missing; it should read $\dfrac{\mathbf{P}(A\cap B)}{\mathbf{P}(A\cup B)}$. Verified against raster/rec02_sol_p01.png.]

Since $\mathbf{P}(A \cup B) \ge \mathbf{P}(A)$, the first conditional probability above is at least as large, so Alice is right, regardless of whether the coin is fair or not. In the case where the coin is fair, that is, if all four outcomes $HH, HT, TH, TT$ are equally likey, we have

$$\frac{\mathbf{P}(A \cap B)}{\mathbf{P}(A)} = \frac{1/4}{1/2} = \frac{1}{2}, \qquad \frac{\mathbf{P}(A \cap B)}{\mathbf{P}(A \cup B)} = \frac{1/4}{3/4} = 1/3.$$

[SOURCE TYPO?: "equally likey" — should be "equally likely"; printed this way in the PDF.]

A generalization of Alice's reasoning is that if $A$, $B$, and $C$ are events such that $B \subset C$ and $A \cap B = A \cap C$ (for example, if $A \subset B \subset C$), then the event $A$ is at least as likely if we know that $B$ has occurred than if we know that $C$ has occurred. Alice's reasoning corresponds to the special case where $C = A \cup B$.

[SOLUTION GAP: the solution does not explicitly state the numerator values $\mathbf{P}(A\cap B)=1/4$, $\mathbf{P}(A)=1/2$, $\mathbf{P}(A\cup B)=3/4$ derivation from the four equally likely outcomes; it also does not prove the stated generalization, only asserts it.]

---

## Problem 2 — Two fair 6-sided dice (Problem 1.14, page 56 in the text)

### Statement

Problem 1.14, page 56 in the text.

We roll two fair 6-sided dice. Each one of the 36 possible outcomes is assumed to be equally likely.

(a) Find the probability that doubles are rolled.

(b) Given that the roll results in a sum of 4 or less, find the conditional probability that doubles are rolled.

(c) Find the probability that at least one die roll is a 6.

(d) Given that the two dice land on different numbers, find the conditional probability that at least one die roll is a 6.

### Official solution

(a) Each possible outcome has probability $1/36$. There are 6 possible outcomes that are doubles, so the probability of doubles is $6/36 = 1/6$.

(b) The conditioning event (sum is 4 or less) consists of the 6 outcomes

$$\{(1,1), (1,2), (1,3), (2,1), (2,2), (3,1)\},$$

2 of which are doubles, so the conditional probability of doubles is $2/6 = 1/3$.

(c) There are 11 possible outcomes with at least one 6, namely, $(6,6)$, $(6,i)$, and $(i,6)$, for $i = 1, 2, \ldots, 5$. Thus, the probability that at least one die is a 6 is $11/36$.

(d) There are 30 possible outcomes where the dice land on different numbers. Out of these, there are 10 outcomes in which at least one of the rolls is a 6. Thus, the desired conditional probability is $10/30 = 1/3$.

[SOLUTION GAP: in (d) the counts $30 = 36 - 6$ and $10 = 11 - 1$ are stated without derivation.]

---

## Problem 3 — Chess tournament (Example 1.13, page 29, and Example 1.17, page 33, in the text)

### Statement

Example 1.13, page 29, and Example 1.17, page 33, in the text.

You enter a chess tournament where your probability of winning a game is 0.3 against half of the players (call them type 1), 0.4 against a quarter of the players (call them type 2), and 0.5 against the remaining quarter of the players (call them type 3). You play a game against a randomly chosen opponent.

(a) What is the probability of winning?

(b) Suppose that you win. What is the probability that you had an opponent of type 1?

### Official solution

(a) See the textbook, Example 1.13, page 29.

(b) See the textbook, Example 1.17, page 33.

[SOLUTION GAP: the entire solution to Problem 3 is delegated to the textbook — no computation whatsoever is shown in the recitation solution PDF. Neither the total-probability computation for (a) nor the Bayes' rule computation for (b) appears in the source.]

---

## Problem 4 — The Monty Hall Problem (Example 1.12, page 27 in the text)

### Statement

Example 1.12, page 27 in the text.

**The Monty Hall Problem.** This is a much discussed puzzle, based on an old American game show. You are told that a prize is equally likely to be found behind any one of three closed doors in front of you. You point to one of the doors. A friend opens for you one of the remaining two doors, after making sure that the prize is not behind it. At this point, you can stick to your initial choice, or switch to the other unopened door. You win the prize if it lies behind your final choice of a door. Consider the following strategies:

(a) Stick to your initial choice.

(b) Switch to the other unopened door.

(c) You first point to door 1. If door 2 is opened, you do not switch. If door 3 is opened, you switch.

Which is the best strategy?

### Official solution

See the textbook, Example 1.12 (The Monty Hall Problem), page 27.

An alternative solution is given below:

Let $P_i$ denote the event where the prize is behind door $i$, $C_i$ denote the event where you initially choose door $i$, and $O_i$ denote the event where your friend opens door $i$. The corresponding probability tree is:

[FIGURE: Three-stage probability tree (sequential tree diagram) drawn left-to-right, occupying the entirety of solution page 2 (no other text on that page besides the course header and the "Page 2 of 3" footer). An unlabeled filled-dot root node sits at the far left, mid-height, with three straight branches: one rising to the upper right, one horizontal, one descending to the lower right.

Stage 1 (prize location): branch labels $\mathbf{P}(P_1)$ (on the rising branch, label written along the slope), $\mathbf{P}(P_2)$ (on the horizontal branch), $\mathbf{P}(P_3)$ (on the descending branch), leading to nodes labeled $P_1$ (upper third of page), $P_2$ (middle), $P_3$ (lower third). Node labels are printed to the left of each dot.

Stage 2 (your initial choice): each $P_i$ node fans into three branches — one rising, one horizontal, one descending — to nodes labeled $C_1$, $C_2$, $C_3$, with branch labels $\mathbf{P}(C_1\mid P_i)$, $\mathbf{P}(C_2\mid P_i)$, $\mathbf{P}(C_3\mid P_i)$ respectively (each label typeset along its slanted branch).

Stage 3 (friend opens a door): terminal leaves are filled dots labeled $O_j$ at the far right.

- From $P_1$: $C_1$ splits into two branches labeled $\mathbf{P}(O_2\mid P_1\cap C_1)$ (rising) $\to O_2$ and $\mathbf{P}(O_3\mid P_1\cap C_1)$ (descending) $\to O_3$; $C_2$ has a single horizontal branch labeled $1 \to O_3$; $C_3$ has a single horizontal branch labeled $1 \to O_2$.
- From $P_2$: $C_1$ has a single horizontal branch labeled $1 \to O_3$; $C_2$ splits into $\mathbf{P}(O_1\mid P_2\cap C_2)$ (rising) $\to O_1$ and $\mathbf{P}(O_3\mid P_2\cap C_2)$ (descending) $\to O_3$; $C_3$ has a single horizontal branch labeled $1 \to O_1$.
- From $P_3$: $C_1$ has a single horizontal branch labeled $1 \to O_2$; $C_2$ has a single horizontal branch labeled $1 \to O_1$; $C_3$ splits into two branches labeled $\mathbf{P}(O_1\mid P_3\cap C_3)$ (rising, drawn to the leaf marked $O_2$) and $\mathbf{P}(O_2\mid P_3\cap C_3)$ (descending, drawn to the leaf marked $O_1$).

All internal nodes and leaves are filled dots. Counts: 1 root, 3 prize nodes, 9 choice nodes, and 12 leaves total (per prize node: one $C_i$ that splits into 2 leaves plus two $C_j$ with a single leaf each, i.e. 4 leaves per prize node × 3 = 12). No probability values (1/3 etc.) are written on the tree — only symbolic $\mathbf{P}(\cdot)$ expressions and the deterministic $1$'s. | raster/rec02_sol_p02.png]

[SOURCE TYPO?: in the $P_3$ sub-tree of the figure, the branch labeled $\mathbf{P}(O_1\mid P_3\cap C_3)$ terminates at the leaf labeled $O_2$ and the branch labeled $\mathbf{P}(O_2\mid P_3\cap C_3)$ terminates at the leaf labeled $O_1$ — i.e. the two leaf labels appear swapped relative to the branch labels (all other sub-trees have matching branch/leaf labels). Verified against raster/rec02_sol_p02.png.]

(a) The probability of winning when not switching from your initial choice is the probability that the prize is behind the door you initially chose:

$$
\begin{aligned}
\mathbf{P}(\text{Win when not switching}) &= \mathbf{P}(P_1 \cap C_1) + \mathbf{P}(P_2 \cap C_2) + \mathbf{P}(P_3 \cap C_3)\\
&= \mathbf{P}(P_1)\mathbf{P}(C_1|P_1) + \mathbf{P}(P_2)\mathbf{P}(C_2|P_2) + \mathbf{P}(P_3)\mathbf{P}(C_3|P_3)\\
&= \mathbf{P}(P_1)\mathbf{P}(C_1) + \mathbf{P}(P_2)\mathbf{P}(C_2) + \mathbf{P}(P_3)\mathbf{P}(C_3)\\
&= 1/3 \cdot (\mathbf{P}(C_1) + \mathbf{P}(C_2) + \mathbf{P}(C_3))\\
&= 1/3
\end{aligned}
$$

[SOLUTION GAP: the step from $\mathbf{P}(C_i|P_i)$ to $\mathbf{P}(C_i)$ silently uses independence of your initial choice from the prize location; and the last step silently uses $\mathbf{P}(C_1)+\mathbf{P}(C_2)+\mathbf{P}(C_3)=1$. Neither is stated.]

(b) The probability of winning when switching from your initial choice is the probability that the prize is behind the remaining (unopened) door:

$$
\begin{aligned}
\mathbf{P}(\text{Win when switching}) &= \mathbf{P}(P_1 \cap C_2 \cap O_3) + \mathbf{P}(P_1 \cap C_3 \cap O_2) + \mathbf{P}(P_2 \cap C_1 \cap O_3)\\
&\quad + \mathbf{P}(P_2 \cap C_3 \cap O_1) + \mathbf{P}(P_3 \cap C_1 \cap O_2) + \mathbf{P}(P_3 \cap C_2 \cap O_1)\\
&= \mathbf{P}(P_1 \cap C_2) + \mathbf{P}(P_1 \cap C_3) + \mathbf{P}(P_2 \cap C_1) + \mathbf{P}(P_2 \cap C_3)\\
&\quad + \mathbf{P}(P_3 \cap C_1) + \mathbf{P}(P_3 \cap C_2)\\
&= \mathbf{P}(P_1)\mathbf{P}(C_2) + \mathbf{P}(P_1)\mathbf{P}(C_3) + \mathbf{P}(P_2)\mathbf{P}(C_1) + \mathbf{P}(P_2)\mathbf{P}(C_3)\\
&\quad + \mathbf{P}(P_3)\mathbf{P}(C_1) + \mathbf{P}(P_3)\mathbf{P}(C_2)\\
&= 2/3 \cdot (\mathbf{P}(C_1) + \mathbf{P}(C_2) + \mathbf{P}(C_3))\\
&= 2/3
\end{aligned}
$$

[SOLUTION GAP: the first-to-second line drops the $O_j$ terms because the corresponding conditional probability is 1 (from the tree) — this is not stated. The grouping that produces the factor $2/3$ (each $\mathbf{P}(P_i)=1/3$ appearing twice) is also not shown.]

(c) Given $C_1$, that you first choose door 1, with the new strategy of switching only if door 3 is opened, you win if the prize behind door 1 and door 2 is opened or if the prize is behind door 2 and door 3 is opened.

[SOURCE TYPO?: "you win if the prize behind door 1 and door 2 is opened" — the verb "is" is missing; should read "if the prize is behind door 1".]

$$
\begin{aligned}
\mathbf{P}(\text{Win with new strategy}|C_1) &= \mathbf{P}(P_1 \cap O_2|C_1) + \mathbf{P}(P_2 \cap O_3|C_1)\\
&= \mathbf{P}(P_1|C_1)\mathbf{P}(O_2|P_1 \cap C_1) + \mathbf{P}(P_2|C_1)\mathbf{P}(O_3|P_2 \cap C_1)\\
&= \mathbf{P}(P_1)\mathbf{P}(O_2|P_1 \cap C_1) + \mathbf{P}(P_2)\mathbf{P}(O_3|P_2 \cap C_1)\\
&= 1/3 \cdot \mathbf{P}(O_2|P_1 \cap C_1) + 1/3 \cdot 1\\
&= 1/3 \cdot (\mathbf{P}(O_2|P_1 \cap C_1) + 1)
\end{aligned}
$$

[SOLUTION GAP: the substitution $\mathbf{P}(O_3|P_2\cap C_1)=1$ is used without comment (if the prize is behind door 2 and you chose door 1, the friend must open door 3).]

Given that your initial choice is door 1, the probability of winning under this new strategy is dependent on how your friend decides which of doors 2 or 3 to open if the prize also lies behind door 1. If he always picks door 2, then $\mathbf{P}(O_2|P_1\cap C_1) = 1$ and $\mathbf{P}(\text{Win with new strategy}|C_1) = 2/3$. If he picks between doors 2 and 3 with equal probability then $\mathbf{P}(O_2|P_1 \cap C_1) = 1/2$ and $\mathbf{P}(\text{Win with new strategy}|C_1) = 1/2$.

[SOLUTION GAP: the question asks "Which is the best strategy?" — the solution computes the three probabilities (1/3, 2/3, and 1/3·(P(O_2|P_1∩C_1)+1) ∈ {2/3, 1/2}) but never states an explicit conclusion that switching (strategy (b)) is best.]

---

## Back matter

Both PDFs end with an MIT OpenCourseWare page:

> MIT OpenCourseWare
> http://ocw.mit.edu
> 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability
> Fall 2010
> For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

(Question PDF page 2 = raster/rec02_p02.png; solution PDF page 4 = raster/rec02_sol_p04.png.)

Page footers: the question PDF page 1 is footed "Page 1 of 1" (with the Athena Scientific footnote on the same rule line, at left). The solution PDF pages are footed "Page 1 of 3", "Page 2 of 3", "Page 3 of 3"; the solution PDF carries no Athena Scientific footnote. Page 1 of the solutions holds problems 1, 2, 3 and the preamble of problem 4 (definitions of $P_i$, $C_i$, $O_i$); page 2 is the probability tree alone; page 3 holds parts (a), (b), (c) of problem 4.
