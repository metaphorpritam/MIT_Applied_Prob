# rec18 — Recitation 18 (November 9, 2010)

Covers: Markov chains — modeling a process as a Markov chain and justifying the Markov property, transition probabilities $p_{ij}$, transient / recurrent / absorbing states, first-passage ("first time entering a state") probabilities by inspection, geometric-series summation over first-passage times, state-occupancy probability after $n$ trials.

Sources: `MIT6_041F10_rec18.pdf` (problems, 2 content pages + 1 OCW page), `MIT6_041F10_rec18_sol.pdf` (solutions, 3 content pages + 1 OCW page)

The last page of each PDF (`rec18_p03.png`, `rec18_sol_p04.png`) is the standard MIT OpenCourseWare citation page — no mathematical content: "MIT OpenCourseWare, `http://ocw.mit.edu` / 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010 / For information about citing these materials or our Terms of Use, visit: `http://ocw.mit.edu/terms`."

Course header on every page: Massachusetts Institute of Technology, Department of Electrical Engineering & Computer Science, 6.041/6.431: Probabilistic Systems Analysis (Fall 2010).

Footer note on the problem pages: "Textbook problems are courtesy of Athena Scientific, and are used with permission."
Footer note on solution page 3: "†Required for 6.431; optional for 6.041" [ANOMALY: no problem in this recitation carries a † marker, yet the footnote is printed.]

---

## Problem 1 — Painting fish: green→blue Markov chain

### Statement

There are $n$ fish in a lake, some of which are green and the rest blue. Each day, Helen catches 1 fish. She is equally likely to catch any one of the $n$ fish in the lake. She throws back all the fish, but paints each green fish blue before throwing it back in. Let $G_i$ denote the event that there are $i$ green fish left in the lake.

(a) Show how to model this fishing exercise as a Markov chain, where $\{G_i\}$ are the states. Explain why your model satisfies the Markov property.

(b) Find the transition probabilities $\{p_{ij}\}$.

(c) List the transient and the recurrent states.

### Official solution

**a)** The number of remaining green fish at time $n$ completely determines all the relevant information of the system's entire history (relevant to predicting the future state.) Therefore it is immediate that the number of green fish is the state of the system and the process has the Markov property:

$$\mathbf{P}(X_{m+1} = j \mid X_m = i,\, X_{m-1} = i_{m-1}, \ldots, X_1 = i_1) = \mathbf{P}(X_{m+1} = j \mid X_m = i).$$

**b)** For $j > i$ clearly $p_{ij} = 0$, since a blue fish will never be painted green. For $0 \le i,\, j \le k$, we have the following:

$$p_{ij} = \mathbf{P}(i - j \text{ green fish are caught} \mid \text{current state} = i) = \begin{cases} \dfrac{n-i}{n} & j = i \\[6pt] \dfrac{i}{n} & j = i - 1 \\[6pt] 0 & \text{otherwise} \end{cases}$$

[SOURCE TYPO?: the range is written "For $0 \le i, j \le k$" but $k$ is never defined anywhere in this problem; the intended range is almost certainly $0 \le i, j \le n$ (the number of fish in the lake).]

**c)** The state 0 is an absorbing state since there is a positive probability that the system will enter it, and once it does, it will remain there forever. Therefore the state with 0 green fish is the only recurrent state, and all other states are then transient.

[SOLUTION GAP: the solution asserts "there is a positive probability that the system will enter it" without demonstrating that state 0 is reachable from every state $i$ (which follows from $p_{i,i-1} = i/n > 0$ for $i \ge 1$, so the chain steps down to 0 with positive probability); it also does not verify $p_{00} = 1$ explicitly, though this follows from the formula with $i = 0$.]

[SOLUTION GAP: part (a) does not explicitly write out the state space, the initial state, or a transition diagram; it only argues the Markov property verbally.]

---

## Problem 2 — (removed)

### Statement

Textbook problem removed due to copyright restrictions.
Drake, *Fundamentals of Applied Probability Theory*, Problem 5.02.

### Official solution

Textbook problem removed due to copyright restrictions.
Drake, *Fundamentals of Applied Probability Theory*, Problem 5.02.

[ANOMALY: problem 2 is absent from both the problem set and the solutions; numbering jumps from 1 to 3.]

---

## Problem 3 — Six-state Markov chain, probabilities by inspection

### Statement

Consider the following Markov chain, with states labelled from $s_0, s_1, \ldots, s_5$:

[FIGURE: Markov chain state-transition diagram. Six circular nodes. Five of them — $S_1$, $S_2$, $S_3$, $S_4$, $S_5$ — are drawn left to right along one horizontal row; the sixth node $S_0$ is drawn below, centered under $S_3$. Each of the five top nodes has a self-loop drawn above it, labelled: $S_1$: 1; $S_2$: 1/2; $S_3$: 1/4; $S_4$: 1/2; $S_5$: 1. Horizontal directed arrows along the top row: $S_2 \to S_1$ labelled 1/2 (arrow points left); $S_3 \to S_2$ labelled 1/4 (arrow points left); $S_3 \to S_4$ labelled 1/2 (arrow points right); $S_4 \to S_5$ labelled 1/2 (arrow points right). Three directed arrows leave $S_0$ and fan upward: $S_0 \to S_1$ labelled 1/3 (up-left), $S_0 \to S_3$ labelled 1/3 (straight up), $S_0 \to S_5$ labelled 1/3 (up-right). So $s_1$ and $s_5$ are absorbing; $s_3$ is the only node with two outgoing non-self transitions. Row sums: $s_1$: 1; $s_2$: 1/2 + 1/2; $s_3$: 1/4 + 1/4 + 1/2; $s_4$: 1/2 + 1/2; $s_5$: 1; $s_0$: 1/3 + 1/3 + 1/3. | raster/rec18_p01.png]

Given that the above process is in state $s_0$ just before the first trial, determine by inspection the probability that:

(a) The process enters $s_2$ for the first time as the result of the $k$th trial.

(b) The process never enters $s_4$.

(c) The process enters $s_2$ and then leaves $s_2$ on the next trial.

(d) The process enters $s_1$ for the first time on the third trial.

(e) The process is in state $s_3$ immediately after the $n$th trial.

### Official solution

**(a)** Let $A_k$ be the event that the process enters $s_2$ for first time on trial $k$. The only way to enter state $s_2$ for the first time on the $k$th trial is to enter state $s_3$ on the first trial, remain in $s_3$ for the next $k - 2$ trials, and finally enter $s_2$ on the last trial. Thus,

$$\mathbf{P}(A_k) = p_{03} \cdot p_{33}^{\,k-2} \cdot p_{32} = \left(\frac{1}{3}\right)\left(\frac{1}{4}\right)^{k-2}\left(\frac{1}{4}\right) = \frac{1}{3}\left(\frac{1}{4}\right)^{k-1} \qquad \text{for} \quad k = 2, 3, \ldots$$

**(b)** Let $A$ be the event that the process never enters $s_4$.

There are three possible ways for $A$ to occur. The first two are if the first transition is either from $s_0$ to $s_1$ or $s_0$ to $s_5$. This occurs with probability $\frac{2}{3}$. The other is if The first transition is from $s_0$ to $s_3$, and that the next change of state *after* that is to the state $s_2$. We know that the probability of going from $s_0$ to $s_3$ is $\frac{1}{3}$. Given this has occurred, and given a change of state occurs from state $s_3$, we know that the probability that the state transitioned to is the state $s_2$ is simply

$$\frac{\frac{1}{4}}{\frac{1}{4} + \frac{1}{2}} = \frac{1}{3}.$$

Thus, the probability of transitioning from $s_0$ to $s_3$ and then eventually transitioning to $s_2$ is $\frac{1}{9}$. Thus, the probability of never entering $s_4$ is $\frac{2}{3} + \frac{1}{9} = \frac{7}{9}$.

[SOURCE TYPO?: "The other is if The first transition is from $s_0$ to $s_3$" — spurious capital "The" mid-sentence.]

[SOLUTION GAP: the step from "the probability of going from $s_0$ to $s_3$ is $\frac13$" and "given a change of state, it goes to $s_2$ with probability $\frac13$" to the product $\frac13 \cdot \frac13 = \frac19$ is stated without the intermediate justification that the chain leaves $s_3$ with probability 1 eventually (i.e. summing the geometric series $\sum_{m\ge 0}(1/4)^m(1/4) = 1/3$ over the number of self-loops), which is what makes the conditional-on-change-of-state argument valid.]

**(c)**
$$\mathbf{P}(\{\text{process enters } s_2 \text{ and then leaves } s_2 \text{ on next trial}\})$$
$$= \mathbf{P}(\{\text{process enters } s_2\})\,\mathbf{P}(\{\text{leaves } s_2 \text{ on next trial}\} \mid \{\text{in } s_2\})$$
$$= \left[\sum_{k=2}^{\infty} \mathbf{P}(A_k)\right] \cdot \frac{1}{2}$$
$$= \left[\sum_{k=2}^{\infty} \frac{1}{3}\left(\frac{1}{4}\right)^{k-1}\right] \cdot \frac{1}{2}$$
$$= \frac{1}{6} \cdot \frac{\frac{1}{4}}{1 - \frac{1}{4}}$$
$$= \frac{1}{18}.$$

[SOLUTION GAP: the geometric series $\sum_{k=2}^{\infty} (1/4)^{k-1} = \frac{1/4}{1-1/4} = \frac13$ is evaluated in one jump; the factor $\frac13 \cdot \frac12 = \frac16$ is pulled out without comment.]

**(d)** This event can only happen if the sequence of state transitions is as follows:

$$s_0 \longrightarrow s_3 \longrightarrow s_2 \longrightarrow s_1.$$

Thus, $\mathbf{P}(\{\text{process enters } s_1 \text{ for first time on third trial}\}) = p_{03} \cdot p_{32} \cdot p_{21} = \frac{1}{3} \cdot \frac{1}{4} \cdot \frac{1}{2} = \frac{1}{24}$.

**(e)**
$$\mathbf{P}(\{\text{process in } s_3 \text{ immediately after the } N\text{th trial}\})$$
$$= \mathbf{P}(\{\text{moves to } s_3 \text{ in first trial and stays in } s_3 \text{ for next } N - 1 \text{ trials}\})$$
$$= \frac{1}{3}\left(\frac{1}{4}\right)^{n-1} \qquad \text{for } n = 1, 2, 3, \ldots$$

[SOURCE TYPO?: part (e) of the solution states the event using capital $N$ ("the $N$th trial", "next $N-1$ trials") but the final formula and the range use lowercase $n$; the problem statement uses lowercase $n$ throughout. Same index, inconsistent case.]
