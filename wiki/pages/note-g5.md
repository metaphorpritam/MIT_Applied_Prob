---
title: Note G5 Markov Chains
type: concept
status: active
aliases: [G5]
tags: [notes, g5]
sources:
  - ../notes/05_markov_chains.html
  - ../notes/src/fragments/g5_s0.html
  - ../notes/src/fragments/g5_s1.html
  - ../notes/src/fragments/g5_s2.html
  - ../notes/src/fragments/g5_s3.html
  - ../notes/src/fragments/g5_s4.html
  - ../notes/src/fragments/g5_s5.html
  - ../transcripts/_g5_review.json
links:
  relates: [Notes Plan, MIT 6.041 Course, Note G4 Iterated Expectations and Arrival Processes, Note G6 Limit Theorems and Bayesian Inference]
---

# Note G5 Markov Chains

`notes/05_markov_chains.html` — 5.4 MB, 42 figures (the most of any note), 4 widgets,
46 practice items. Covers [[MIT 6.041 Course]] L16–L18 with rec18–19, plus rec16–17
folded in as a checkpoint. Tracked in [[Notes Plan]]; assembled by
[[Build Pipeline]].

## Section map

- **§0 Orientation: dependence, compressed into a state** — the Markov property in words
  and symbols, the $p_{ij}$ versus $r_{ij}(n)$ notation fixed up front, and the three
  questions the note answers.
- **§1 The Markov model and $n$-step transition probabilities** — states, transition
  probabilities and the Markov property; the checkout counter built out of its Bernoulli
  ingredients; the Chapman–Kolmogorov recursion; the two-state chain computed (filling
  in L16 slide 5); rec18 modeling and probabilities by inspection.
- **§2 Classification of states** — accessibility, recurrence and transience; recurrent
  classes and the decomposition of a chain; periodicity; the steady-state convergence
  theorem and the two distinct ways it fails.
- **§3 Steady-state probabilities, balance equations, birth–death chains** — from the
  $n$-step recursion to the balance equations, solving them, what $\pi_j$ actually
  counts, birth–death chains and the cut (local balance) equations, the queue with load
  factor $\rho$ as $\rho \to 1$, and the phone company as an inhomogeneous birth–death
  chain (L18 slide 4).
- **§4 Absorption probabilities and expected time to absorption** — absorbing states,
  expected time to absorption, gambler's ruin, mean first passage and mean recurrence
  times, conditioning on *which* absorbing state you reach, and rec19 (Josephina changes
  courses) in full.
- **§5 Synthesis and a G3/G4 checkpoint** — the three question types on one page,
  classification-first plus five gotchas, Checkpoint I on continuous random variables
  (rec16), Checkpoint II on the Poisson process (rec17), and the bridge to G6.

## Widgets

`w-g5s1-nstep` ($n$-step evolution: pick a chain, a start state, a horizon) ·
`w-g5s2-periodic` (periodic vs aperiodic: $P(X_n = 1)$ for the two-state chain) ·
`w-g5s3-bdqueue` (birth–death queue: how the load factor reshapes the steady state) ·
`w-g5s4-ruin` (gambler's ruin: drag $p$, the target $m$, the starting fortune $i$).

## Flagship worked problems

The checkout-counter chain derived from its Bernoulli ingredients · the two-state chain
computed to close L16 slide 5 · the phone-company inhomogeneous birth–death chain
(L18 slide 4) · gambler's ruin in closed form with the $\rho = (1-p)/p$ ratio ·
rec18's modeling problem · rec19 "Josephina changes courses", all parts.

## Review stats

`transcripts/_g5_review.json` — **50 issues**: 4 critical, 16 major, 30 minor,
distributed 3/10/5/14/9/9 across §0–§5; 47 fixes. The worst critical was a
boundary-row model inconsistency in the checkout chain (a blocked arrival treated as
lost in the prose but as state-changing in the boxed result) that had propagated to six
places; others were stale numbers drifted from their compute JSON. The consistency pass
needed only 4 edits and found 0 cross-note mismatches — by G5 the conventions were
holding.

## Special notes — the rec16/17 checkpoint

rec16 and rec17 are review recitations carrying no new Markov material (see the
recitation offset on [[Note G4 Iterated Expectations and Arrival Processes]]). Rather
than skip them, they became §5.3 and §5.4: a continuous-random-variable checkpoint and
a Poisson-process checkpoint that close the G3/G4 loop before the reader moves on. Also
noted during review: rec18 P2 has no copyright-clear source figure, and a
"B&T's Figure 7.14" reference in `g5_s3.html` was carried as a known polish item.

Prev: [[Note G4 Iterated Expectations and Arrival Processes]] · Next:
[[Note G6 Limit Theorems and Bayesian Inference]].
