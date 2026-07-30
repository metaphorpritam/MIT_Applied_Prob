# rec01 — Recitation 1 (September 9, 2010)

Covers: probability axioms (nonnegativity, additivity, normalization), set algebra on events (complements, disjoint decompositions), the two-event union/inclusion–exclusion formula, complement rule, discrete probabilistic models with unequal weights (loaded die), continuous/geometric sample spaces (uniform on a square — Romeo & Juliet), continuity property of probability measures (monotone increasing/decreasing sequences of events).

Sources: `MIT6_041F10_rec01.pdf` (problems), `MIT6_041F10_rec01_sol.pdf` (solutions)

Course header on both documents: Massachusetts Institute of Technology, Department of Electrical Engineering & Computer Science, 6.041/6.431: Probabilistic Systems Analysis (Fall 2010).

Dagger marker: the last item on both documents is labelled **G1†**. Neither PDF prints an explanatory footnote for the † symbol on the rastered pages — no "Required for 6.431; optional for 6.041" text appears anywhere on `rec01_p01.png` or `rec01_sol_p01.png`. (That reading of † is the standard 6.041/6.431 course convention, but it is *not* stated in this document.)

Footer note on the problem set only (`rec01_p01.png`, below the body, above the bottom rule): "Textbook problems are courtesy of Athena Scientific, and are used with permission." The solutions PDF has **no** footer note — only the bottom horizontal rule.

---

## Problem 1 — Derivation of $\mathbf{P}(\text{symmetric difference})$ from the axioms

### Statement

Give a mathematical derivation of the formula

$$\mathbf{P}\big((A \cap B^c) \cup (A^c \cap B)\big) = \mathbf{P}(A) + \mathbf{P}(B) - 2\,\mathbf{P}(A \cap B).$$

Your derivation should be a sequence of steps, with each step justified by appealing to one of the probability axioms.

### Official solution

Since the events $A \cap B^c$ and $A^c \cap B$ are disjoint, we have, using the additivity axiom,

$$\mathbf{P}\big((A \cap B^c) \cup (A^c \cap B)\big) = \mathbf{P}(A \cap B^c) + \mathbf{P}(A^c \cap B).$$

Since $A = (A \cap B) \cup (A \cap B^c)$ is the union of two disjoint sets, we have, again by the additivity axiom,

$$\mathbf{P}(A) = \mathbf{P}(A \cap B) + \mathbf{P}(A \cap B^c),$$

so that

$$\mathbf{P}(A \cap B^c) = \mathbf{P}(A) - \mathbf{P}(A \cap B).$$

Similarly,

$$\mathbf{P}(B \cap A^c) = \mathbf{P}(B) - \mathbf{P}(A \cap B).$$

[SOLUTION GAP: the "Similarly" step is asserted without writing out the parallel decomposition $B = (A \cap B) \cup (A^c \cap B)$ and the corresponding additivity application.]

Therefore,

$$
\begin{aligned}
\mathbf{P}(A \cap B^c) + \mathbf{P}(A^c \cap B)
&= \mathbf{P}(A) - \mathbf{P}(A \cap B) + \mathbf{P}(B) - \mathbf{P}(A \cap B) \\
&= \mathbf{P}(A) + \mathbf{P}(B) - 2\,\mathbf{P}(A \cap B).
\end{aligned}
$$

---

## Problem 2 — Geniuses and chocolate lovers (Problem 1.5, p. 54 in the text)

### Statement

Problem 1.5, page 54 in the text.

Out of the students in a class, 60% are geniuses, 70% love chocolate, and 40% fall into both categories. Determine the probability that a randomly selected student is neither a genius nor a chocolate lover.

### Official solution

Let

$$
\begin{aligned}
A &\;:\; \text{The event that the randomly selected student is a genius.}\\
B &\;:\; \text{The event that the randomly selected student loves chocolate.}
\end{aligned}
$$

From the properties of probability laws proved in lecture, we have

$$
\begin{aligned}
1 &= \mathbf{P}(A \cup B) + \mathbf{P}\big((A \cup B)^c\big) \\
&= \mathbf{P}(A) + \mathbf{P}(B) - \mathbf{P}(A \cap B) + \mathbf{P}(A^c \cap B^c) \\
&= 0.6 + 0.7 - 0.4 + \mathbf{P}(A^c \cap B^c) \\
&= 0.9 + \mathbf{P}(A^c \cap B^c).
\end{aligned}
$$

[SOLUTION GAP: the second line silently uses two facts without proof here — the inclusion–exclusion identity $\mathbf{P}(A \cup B) = \mathbf{P}(A) + \mathbf{P}(B) - \mathbf{P}(A \cap B)$, and De Morgan's law $(A \cup B)^c = A^c \cap B^c$.]

Therefore

$$
\begin{aligned}
&\mathbf{P}(\text{A randomly selected student is neither a genius nor a chocolate lover}) \\
&= \mathbf{P}(A^c \cap B^c) \;=\; 1 - 0.9 \;=\; 0.1.
\end{aligned}
$$

---

## Problem 3 — Loaded six-sided die

### Statement

A six-sided die is loaded in a way that each even face is twice as likely as each odd face. Construct a probabilistic model for a single roll of this die, and find the probability that a 1, 2, or 3 will come up.

### Official solution

Let $c$ denote the probability of a single odd face. Then the probability of a single even face is $2c$, and by adding the probabilities of the 3 odd faces and the 3 even faces, we get $9c = 1$. Thus, $c = 1/9$. The desired probability is

$$\mathbf{P}(\{1, 2, 3\}) = \mathbf{P}(\{1\}) + \mathbf{P}(\{2\}) + \mathbf{P}(\{3\}) = c + 2c + c = 4c = 4/9.$$

[SOLUTION GAP: the normalization sum is compressed — $3c + 3(2c) = 9c = 1$ is stated in words but the arithmetic ($3c + 6c$) is not written out. The solution also does not explicitly display the full model (sample space $\Omega = \{1,2,3,4,5,6\}$ with $\mathbf{P}(\{1\}) = \mathbf{P}(\{3\}) = \mathbf{P}(\{5\}) = 1/9$ and $\mathbf{P}(\{2\}) = \mathbf{P}(\{4\}) = \mathbf{P}(\{6\}) = 2/9$), even though "construct a probabilistic model" was asked.]

---

## Problem 4 — Romeo and Juliet (Example 1.5, p. 13 in the text)

### Statement

Example 1.5, page 13 in the text.

Romeo and Juliet have a date at a given time, and each will arrive at the meeting place with a delay between 0 and 1 hour, with all pairs of delays being equally likely. The first to arrive will wait for 15 minutes and will leave if the other has not yet arrived. What is the probability that they will meet?

### Official solution

See the textbook, Example 1.5, page 13.

[SOLUTION GAP: the entire solution is deferred to the textbook. No derivation, no sample-space description, and no numerical answer are given in the recitation solutions document. The associated textbook figure (the unit square $[0,1]^2$ of delay pairs with the shaded band $|x - y| \le 1/4$) is likewise not reproduced here.]

---

## Problem G1† — Continuity property of probabilities (Problem 1.13, p. 56 in the text)

Item label in both PDFs: **G1†** (a "G" = graduate-level item; the † superscript is printed but never explained on these pages — by course convention it means required for 6.431, optional for 6.041, though the document itself does not say so).

### Statement

Problem 1.13, page 56 in the text. **Continuity property of probabilities.**

(a) Let $A_1, A_2, \ldots$ be an infinite sequence of events that is "monotonically increasing," meaning that $A_n \subset A_{n+1}$ for every $n$. Let $A = \cup_{n=1}^{\infty} A_n$. Show that $\mathbf{P}(A) = \lim_{n \to \infty} \mathbf{P}(A_n)$. *Hint:* Express the event $A$ as a union of countably many disjoint sets.

(b) Suppose now that the events are "monotonically decreasing," i.e., $A_{n+1} \subset A_n$ for every $n$. Let $A = \cap_{n=1}^{\infty} A_n$. Show that $\mathbf{P}(A) = \lim_{n \to \infty} \mathbf{P}(A_n)$. *Hint:* Apply the result of the previous part to the complements of the events.

(c) Consider a probabilistic model whose sample space is the real line. Show that

$$\mathbf{P}\big([0, \infty)\big) = \lim_{n \to \infty} \mathbf{P}\big([0, n]\big) \qquad \text{and} \qquad \lim_{n \to \infty} \mathbf{P}\big([n, \infty)\big) = 0.$$

### Official solution

See the textbook, Problem 1.13, page 56.

[SOLUTION GAP: the entire solution is deferred to the textbook. No proof of any of parts (a), (b), (c) appears in the recitation solutions document.]

---

## Figures

No figures, diagrams, trees, or plots appear anywhere in either PDF. Both documents are pure text/formula on page 1; page 2 of each is the standard MIT OpenCourseWare boilerplate page.

Page 2 boilerplate (identical in both PDFs):

> MIT OpenCourseWare
> http://ocw.mit.edu
> 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability
> Fall 2010
> For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

Raster pages consulted: `raster/rec01_p01.png`, `raster/rec01_p02.png`, `raster/rec01_sol_p01.png`, `raster/rec01_sol_p02.png`.

---

## Transcription notes / anomalies

- The raw text extraction of the problem PDF mangled G1(b): it rendered "Let $A = {}_{n=1}A_n$ ... Apply the result of the $\cap_{n=1}^{\infty}$ previous part" — a line-wrap artifact. The raster page confirms the correct reading is "Let $A = \cap_{n=1}^{\infty} A_n$" and "Apply the result of the previous part". Corrected above.
- The raw text extraction rendered G1(c) as "P([0, ∞)) = lim P([0, n]) and lim P([n, ∞)) = 0. n→∞ n→∞" — the $n \to \infty$ subscripts were detached and floated to end of line. Corrected above from the raster.
- The raw text extraction produced "0 .1" (spurious space) in Problem 2 and "P({1, 2 , 3})" in Problem 3; the raster shows "0.1" and "$\mathbf{P}(\{1,2,3\})$".
- Problem 1 solution writes $\mathbf{P}(B \cap A^c)$ in the "Similarly" line but $\mathbf{P}(A^c \cap B)$ in the "Therefore" line. These denote the same event (intersection is commutative), so this is a cosmetic inconsistency, not an error.
- No source typos detected beyond the extraction artifacts listed above; all formulas were verified against `raster/rec01_p01.png` and `raster/rec01_sol_p01.png`.
- A previous version of this transcript asserted a footnote "†Required for 6.431; optional for 6.041" on both documents. Verified against the rasters (including a 2× zoom of the bottom 14% of each page 1): **no such footnote exists**. The only footer text anywhere is the Athena Scientific line on the problem sheet. Corrected above.
- Document titles differ between the two PDFs: the problem sheet's centered title block reads "Recitation 1 / September 9, 2010"; the solutions sheet reads "Recitation 1: Solutions / September 9, 2010".
- Both page-1 headers are followed by a full-width horizontal rule under "(Fall 2010)"; both pages end with a full-width horizontal rule. No other rules, boxes, or marginal notes appear.
