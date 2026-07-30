# rec19 — Recitation 19 (November 16, 2010)

Covers: Markov chains; classification of states (transient/recurrent); absorption probabilities; expected time to absorption; conditional (on absorbing state) transition probabilities; steady-state probabilities; mean recurrence time and its relation to steady-state probabilities.

Sources: MIT6_041F10_rec19.pdf, MIT6_041F10_rec19_sol.pdf

Header block on both PDFs: Massachusetts Institute of Technology, Department of Electrical Engineering & Computer Science, 6.041/6.431: Probabilistic Systems Analysis (Fall 2010). The question sheet is titled "Recitation 19: November 16, 2010" (1 page); the solution sheet is titled "Recitation 19 Solutions: November 16, 2010" (5 pages, footers "Page 1 of 5" … "Page 5 of 5"). Footer of the question sheet: "Textbook problems are courtesy of Athena Scientific, and are used with permission." / "Page 1 of 1".

---

## Problem 1 — Josephina's course changes (Markov chain: absorption, expected times, steady state)

### Statement

1. Josephina is currently a 6-1 student. On each day that she is a 6-1 student, she has a probability of $1/2$ of being a course 6-1 student the next day. Otherwise, she has an equally likely chance of becoming a 6-2 student, a 6-3 student, a course 9 student or a course 15 student the next day. On any day she is a 6-3 student, she has a probability of $1/4$ of switching to course 9, a probability of $3/8$ of switching to 6-1 and a probability of $3/8$ of switching to 6-2 the next day. On any day she is a 6-2 student, she has a probability of $1/2$ of switching to course 15, a probability of $3/8$ of switching to 6-1 and a probability of $1/8$ of switching to 6-3 the next day.

In answering the questions below, assume Josephina will be a student forever. Also assume, for parts (a)-(f) that if Josephina switches to course 9 or course 15, she will stay there and will not change her course again.

**(a)** What is the probability that she eventually will leave course 6?

**(b)** What is the probability that she will eventually be in course 15?

**(c)** What is the expected number of days until she leaves course 6?

**(d)** Every time she switches into 6-1 from 6-2 or 6-3, she buys herself an ice cream cone at Tosci's. She can only afford so much ice cream, so after she's eaten 2 ice cream cones, she stops buying herself ice cream. What is the expected number of ice cream cones she buys herself before she leaves course 6?

**(e)** Her friend Oscar started out just like Josephina. He is now in course 15. You don't know how long it took him to switch. What is the expected number of days it took him to switch to course 15?

**(f)** Josephina decides that course 15 is not in her future. Accordingly, when she is a course 6-1 student, she stays 6-1 for another day with probability $1/2$, and otherwise she has an equally likely chance of becoming any of the other options. When she is 6-2, her probability of entering 6-1 or 6-3 are in the same proportion as before. What is the expected number of days until she is in course 9?

**(g)** For this part only, assume that when Josephina is in course 9 she is equally likely to stay in course 9 or switch to course 15. Similarly, if she is in course 15, she is equally likely to stay in course 15 or switch to course 9. Calculate the probability of Josephina being in each course on any given day far into the future.

**(h)** Suppose that if she is course 9 or course 15, she has probability $1/8$ of returning to 6-1, and otherwise she remains in her current course. What is the expected number of days until she is 6-1 again? (Notice that we know today she is 6-1, so if tomorrow she is still 6-1, then the number of days until she is 6-1 again is 1).

### Official solution

**(a)** The Markov chain is shown below.

[FIGURE: Markov chain state-transition diagram, 5 circular states. Top-left state "9" with a self-loop labeled 1; top-right state "15" with a self-loop labeled 1; center state "6-1" with a self-loop labeled 1/2; bottom-left state "6-3"; bottom-right state "6-2". Directed arcs with labels: 6-1 → 9 labeled 1/8; 6-3 → 9 (long arc up the left side) labeled 1/4; 6-1 → 15 labeled 1/8; 6-2 → 15 (long arc up the right side) labeled 1/2; 6-3 → 6-1 labeled 3/8; 6-1 → 6-3 labeled 1/8; 6-2 → 6-1 labeled 3/8; 6-1 → 6-2 labeled 1/8; 6-3 → 6-2 (upper of the two bottom arcs) labeled 3/8; 6-2 → 6-3 (lower bottom arc) labeled 1/8. States 9 and 15 are absorbing. | raster/rec19_sol_p01.png]

By inspection, the states 6-1, 6-2, and 6-3 are all transient, since they each have paths leading to either state 9 or state 15, from which there is no return. Therefore she eventually leaves course 6 with probability $\boxed{1}$.

**(b)** This is the absorption probability for the recurrent class consisting of the state course-15. Let us denote the probability of being absorbed by state 15 conditioned on being in state $i$ as $a_i$. Then

$$a_{15} = 1$$
$$a_9 = 0$$
$$a_{6-1} = \frac{1}{2}a_{6-1} + \frac{1}{8}(1) + \frac{1}{8}a_{6-2} + \frac{1}{8}(0) + \frac{1}{8}a_{6-3}$$
$$a_{6-2} = \frac{1}{2}(1) + \frac{3}{8}a_{6-1} + \frac{1}{8}a_{6-3}$$
$$a_{6-3} = \frac{1}{4}(0) + \frac{3}{8}a_{6-1} + \frac{3}{8}a_{6-2}$$

Solving this system of equations yields

$$a_{6-1} = \frac{105}{184} \approx 0.571$$

[SOLUTION GAP: the algebra of solving the 3×3 linear system for $a_{6-1}, a_{6-2}, a_{6-3}$ is not shown; only the final values are given.]

We will keep the other $a_i$'s around as well - they will be useful later:

$$a_{6-2} = 0.77717$$
$$a_{6-3} = 0.50543$$

**(c)** This is the expected time until absorption for the transient state $6-1$. Let $\mu_i$ be the expected time until absorption conditioned on being in state $i$. Then

$$\mu_{15} = 0$$
$$\mu_9 = 0$$
$$\mu_{6-1} = 1 + \frac{1}{2}\mu_{6-1} + \frac{1}{8}(0) + \frac{1}{8}\mu_{6-2} + \frac{1}{8}(0) + \frac{1}{8}\mu_{6-3}$$
$$\mu_{6-2} = 1 + \frac{1}{2}(0) + \frac{3}{8}\mu_{6-1} + \frac{1}{8}\mu_{6-3}$$
$$\mu_{6-3} = 1 + \frac{1}{4}(0) + \frac{3}{8}\mu_{6-1} + \frac{3}{8}\mu_{6-2}$$

Solving this system of equations yields

$$\mu_{6-1} = \frac{162}{46} = \frac{81}{23} \approx 3.522$$

[SOLUTION GAP: the elimination steps solving the 3×3 system are not shown.]

**(d)** The student buys one ice cream cone every time she goes from 6-2 to 6-1 or from 6-3 to 6-1, and buys no more than 2 ice cream cones. Let us denote $v_i(j)$ as the conditional probability that given that she is in state $i$, that she transitions from $6-2$ to $6-1$ or from $6-3$ to $6-1$ $j$ additional times. Then we are interested in the expected value of the random variable $N$, which denotes the number of cones bought before leaving course 6, and takes on the values 0, 1, or 2. So

$$\mathbf{E}[N] = (0)v_{6-1}(0) + (1)v_{6-1}(1) + (2)(1 - v_{6-1}(0) - v_{6-1}(1))$$

We use the total probability theorem, conditioning on the next day, to yield the following set of equations:

$$v_{15}(0) = 1$$
$$v_9(0) = 1$$
$$v_{6-1}(0) = \frac{1}{2}v_{6-1}(0) + \frac{1}{8}v_{6-2}(0) + \frac{1}{8}v_{6-3}(0) + \frac{1}{8}(1) + \frac{1}{8}(1)$$
$$v_{6-2}(0) = \frac{3}{8}(0) + \frac{1}{8}v_{6-3}(0) + \frac{1}{2}(1)$$
$$v_{6-3}(0) = \frac{3}{8}(0) + \frac{3}{8}v_{6-2}(0) + \frac{1}{4}(1)$$

Solving this system of equations yields:

$$v_{6-1}(0) = \frac{46}{61} \approx 0.754$$

We still need to find $v_{6-1}(1)$, and we do this by again conditioning on the following day and solving the following set of equations:

$$v_{6-1}(1) = \frac{1}{2}v_{6-1}(1) + \frac{1}{8}v_{6-2}(1) + \frac{1}{8}v_{6-3}(1) + \frac{1}{8}(0) + \frac{1}{8}(0)$$
$$v_{6-2}(1) = \frac{3}{8}v_{6-1}(0) + \frac{1}{8}v_{6-3}(1) + \frac{1}{2}(0)$$
$$v_{6-3}(1) = \frac{3}{8}v_{6-1}(0) + \frac{3}{8}v_{6-2}(1) + \frac{1}{4}(0)$$

Notice in the second and third equations that when she transitions into state 6-1, there should be no additional transitions from 6-2 to 6-1 or from 6-3 to 6-1 after the second day in order for there to be a total of one such transition. Solving this system of equations yields:

$$v_{6-1}(1) = \frac{690}{3721} \approx 0.185$$

[SOLUTION GAP: neither linear system for $v_i(0)$ nor $v_i(1)$ is solved explicitly; only the final $v_{6-1}(\cdot)$ values are given.]

Finally, we can solve for the expected number of cones:

$$\mathbf{E}[N] = (0)v_{6-1}(0) + (1)v_{6-1}(0) + (2)(1 - v_{6-1}(0) - v_{6-1}(1))$$
$$= \frac{690}{3721} + 2\left(\frac{225}{3721}\right)$$
$$= \frac{1140}{3721} \approx 0.306$$

[SOURCE TYPO?: In this final display the second term is printed as $(1)v_{6-1}(0)$, but it must be $(1)v_{6-1}(1)$ — as written correctly in the first display of part (d) — since the numerical substitution that follows uses $690/3721 = v_{6-1}(1)$.]

[SOLUTION GAP: the value $1 - v_{6-1}(0) - v_{6-1}(1) = 225/3721$ is stated without showing $46/61 = 2806/3721$ and the subtraction $3721 - 2806 - 690 = 225$.]

**(e)** We want to find the expected time to absorption conditioned on the event that the student eventually ends up in state 15, which we will call $A$. So

$$\mathbf{P}_{i,j|A} = \mathbf{P}(X_{n+1} = j \mid X_n = i, A)$$
$$= \frac{\mathbf{P}(A \mid X_{n+1} = j, X_n = i)\,\mathbf{P}(X_{n+1} = j \mid X_n = i)}{\mathbf{P}(A \mid X_n = i)}$$
$$= \frac{\mathbf{P}(A \mid X_{n+1} = j)\,\mathbf{P}(X_{n+1} = j \mid X_n = i)}{\mathbf{P}(A \mid X_n = i)}$$
$$= \frac{a_j \mathbf{P}_{i,j}}{a_i}$$

where $a_k$ is the absorption probability of eventually ending up in state 15 conditioned on being in state $k$, which we found in part (b). So we may modify our chain with these new conditional probabilities and calculate the expected time to absorption on the new chain. Note that state 9 now disappears. Also, note that $\mathbf{P}_{j,j|A} = \mathbf{P}_{j,j}$, but $\mathbf{P}_{i,j|A} \neq \mathbf{P}_{i,j}$ for $i \neq j$, which means that we may not simply renormalize the transition probabilities in a uniform fashion after conditioning on this event. Let us denote the new expected time to absorption, conditioned on being in state $i$ as $\tilde{\mu}_i$. Our system of equations now becomes

$$\tilde{\mu}_{15} = 0$$
$$\tilde{\mu}_{6-1} = 1 + \frac{a_{6-1}}{a_{6-1}}\frac{1}{2}\tilde{\mu}_{6-1} + 0 + \frac{a_{6-2}}{a_{6-1}}\frac{1}{8}\tilde{\mu}_{6-2} + 0 + \frac{a_{6-3}}{a_{6-1}}\frac{1}{8}\tilde{\mu}_{6-3}$$
$$\tilde{\mu}_{6-2} = 1 + 0 + \frac{a_{6-1}}{a_{6-2}}\frac{3}{8}\tilde{\mu}_{6-1} + \frac{a_{6-3}}{a_{6-2}}\frac{1}{8}\tilde{\mu}_{6-3}$$
$$\tilde{\mu}_{6-3} = 1 + 0 + \frac{a_{6-1}}{a_{6-3}}\frac{3}{8}\tilde{\mu}_{6-1} + \frac{a_{6-2}}{a_{6-3}}\frac{3}{8}\tilde{\mu}_{6-2}$$

Solving this system of equations yields

$$\tilde{\mu}_{6-1} = \frac{1763}{483} \approx 3.65$$

[SOLUTION GAP: the numerical substitution of the $a_i$ values and the solution of the resulting 3×3 system are not shown.]

**(f)** The new Markov chain is shown below.

[FIGURE: Markov chain state-transition diagram, 4 circular states (state 15 removed). Top state "9" with a self-loop labeled 1 (absorbing); center state "6-1" with a self-loop labeled 1/2; bottom-left state "6-3"; bottom-right state "6-2". Directed arcs with labels: 6-1 → 9 labeled 1/6; 6-3 → 9 (long arc up the left side) labeled 1/4; 6-3 → 6-1 labeled 3/8; 6-1 → 6-3 labeled 1/6; 6-1 → 6-2 labeled 1/6; 6-2 → 6-1 labeled 3/4; 6-3 → 6-2 (upper bottom arc) labeled 3/8; 6-2 → 6-3 (lower bottom arc) labeled 1/4. | raster/rec19_sol_p04.png]

This is another expected time to absorption question on the new chain. Let us define $\mu_k$ to be the expected number of days it takes the student to go from state $k$ to state 9 in this new Markov chain:

$$\mu_{6-1} = 1 + \frac{1}{2}\mu_{6-1} + \frac{1}{6}\mu_{6-2} + \frac{1}{6}\mu_{6-3} + \frac{1}{6}(0)$$
$$\mu_{6-2} = 1 + \frac{3}{4}\mu_{6-1} + \frac{1}{4}\mu_{6-3}$$
$$\mu_{6-3} = 1 + \frac{3}{8}\mu_{6-1} + \frac{3}{8}\mu_{6-2} + \frac{1}{4}(0)$$

Solving this system of equations yields:

$$\mu_{6-1} = \frac{86}{13} \approx 6.615$$

[SOLUTION GAP: the elimination steps are not shown. Also, the new 6-2 row is asserted implicitly: "her probability of entering 6-1 or 6-3 are in the same proportion as before" gives $3/8 : 1/8 = 3:1$, hence $3/4$ and $1/4$ — this renormalization is not spelled out.]

**(g)** States 6-1, 6-2 and 6-3 are now transient. States 9 and 15 form a recurrent class. By symmetry, 9 and 15 have the same steady state probability of $1/2$.

[FIGURE: Markov chain state-transition diagram (boxed, shaded blue nodes; credit line "Image by MIT OpenCourseWare."). Same layout as the part-(a) chain: state "9" top-left, state "15" top-right, state "6-1" center, "6-3" bottom-left, "6-2" bottom-right. Differences from (a): state 9 has a self-loop labeled 1/2 and an arc 9 → 15 labeled 1/2; state 15 has a self-loop labeled 1/2 and an arc 15 → 9 labeled 1/2. All other arcs unchanged: 6-1 self-loop 1/2; 6-1 → 9 labeled 1/8; 6-1 → 15 labeled 1/8; 6-1 → 6-3 labeled 1/8; 6-1 → 6-2 labeled 1/8; 6-3 → 9 labeled 1/4; 6-3 → 6-1 labeled 3/8; 6-3 → 6-2 labeled 3/8; 6-2 → 15 labeled 1/2; 6-2 → 6-1 labeled 3/8; 6-2 → 6-3 labeled 1/8. | raster/rec19_sol_p04.png]

States 6-1, 6-2 and 6-3 are now transient. States 9 and 15 form a recurrent class. By symmetry, 9 and 15 have the same steady state probability of $1/2$.

[Note: the sentence above appears twice in the PDF — once before the figure and once after it.]

[SOLUTION GAP: the answer for the transient states (steady-state probability 0 for 6-1, 6-2, 6-3) is only implied by calling them transient; it is not stated numerically.]

**(h)** The corresponding Markov chain is the same as the one in part (a) except $p_{9,6-1} = \frac{1}{8}$, $p_{9,9} = \frac{7}{8}$, $p_{15,6-1} = \frac{1}{8}$, $p_{15,15} = \frac{7}{8}$ instead of $p_{9,9} = 1$, $p_{15,15} = 1$.

We can consider state 6-1 as an absorbing state. Let $\mu_k$ be the expected number of transitions until absorption if we start at state $k$

$$\mu_9 = \frac{1}{8} + \frac{7}{8}(1 + \mu_9) \Rightarrow \mu_9 = 8$$
$$\mu_{15} = \frac{1}{8} + \frac{7}{8}(1 + \mu_{15}) \Rightarrow \mu_{15} = 8$$
$$\mu_{6-3} = \frac{3}{8} + \frac{3}{8}(1 + \mu_{6-2}) + \frac{1}{4}(1 + \mu_9)$$
$$\mu_{6-2} = \frac{3}{8} + \frac{1}{8}(1 + \mu_{6-3}) + \frac{1}{2}(1 + \mu_{15})$$
$$\Rightarrow \mu_{6-2} = \frac{344}{61}, \quad \mu_{6-3} = \frac{312}{61}$$

[SOLUTION GAP: the two-equation solve for $\mu_{6-2}$ and $\mu_{6-3}$ is not shown.]

Let $R$ be the number of days until she is 6-1 again. We find $\mathbf{E}[R]$ by using the total expectation theorem, conditioned on what happens on the first transition.

$$\mathbf{E}[R] = \mathbf{E}[\mathbf{E}[R \mid X_2]]$$
$$= \frac{1}{2}(1) + \frac{1}{8}(1 + \mu_9) + \frac{1}{8}(1 + \mu_{15}) + \frac{1}{8}(1 + \mu_{6-2}) + \frac{1}{8}(1 + \mu_{6-3})$$
$$= \frac{265}{61}$$

[SOLUTION GAP: the arithmetic combining the terms into $265/61$ is not shown.]

Notice that this chain consists of a single recurrent aperiodic class. Another approach to solving this problem uses the steady state probabilities of this chain, which are $\pi_{6-1} = \frac{61}{265}$, $\pi_{6-2} = \frac{11}{265}$, $\pi_{6-3} = \frac{9}{265}$, $\pi_9 = \frac{79}{265}$, $\pi_{15} = \frac{105}{265}$. The expected frequency of visits to 6-1 is $\pi_{6-1}$, so the expected number of days between visits to 6-1 is $\frac{1}{\pi_{6-1}}$.$^1$ Since she is currently 6-1, the expected number of days until she is 6-1 again is $\frac{1}{\pi_{6-1}} = \frac{265}{61}$.

[SOLUTION GAP: the steady-state balance equations that produce these $\pi$ values are not shown; the values are simply quoted.]

$^1$ See problem 7.34 on page 399 of the text for a more detailed explanation of this correspondence between mean recurrence times and steady-state probabilities.

---

Back matter (both PDFs, final page): MIT OpenCourseWare, http://ocw.mit.edu, 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010. For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.
