---
title: Note G1 Probability Fundamentals
type: concept
status: active
aliases: [G1]
tags: [notes, g1]
sources:
  - ../notes/01_probability_basics.html
  - ../notes/src/fragments/g1_s0.html
  - ../notes/src/fragments/g1_s1.html
  - ../notes/src/fragments/g1_s2.html
  - ../notes/src/fragments/g1_s3.html
  - ../notes/src/fragments/g1_s4.html
  - ../notes/src/fragments/g1_s5.html
  - ../transcripts/_g1_review.json
links:
  relates: [Notes Plan, MIT 6.041 Course, Note G2 Discrete Random Variables]
---

# Note G1 Probability Fundamentals

`notes/01_probability_basics.html` — 3.3 MB, 32 figures, 8 widgets, 65 practice
items. Covers [[MIT 6.041 Course]] L01–L04 with rec01–04. First note built, so it
also carries the reading conventions the other six inherit (notation table, B&T
citation style, `§N.k` numbering). Tracked in [[Notes Plan]]; assembled by
[[Build Pipeline]].

## Section map

- **§0 How to read these notes; the landscape of probability** — what a probabilistic
  model is, the roadmap, and how lectures, recitations and the book interleave.
- **§1 Probabilistic models and the axioms** — sample space $\Omega$, events and the
  three axioms, the discrete uniform law, continuous models where probability = area,
  why finite additivity is not enough, a decision procedure for picking the right law,
  and rec01 solved in full.
- **§2 Conditioning, total probability, and Bayes' rule** — conditional probability as a
  re-normalized universe, the multiplication/chain rule, total probability, Bayes,
  a which-tool decision guide, and Monty Hall.
- **§3 Independence** — sequential models and the biased coin, independence of two
  events, conditional independence, independence of a collection, independent trials
  (the drunk tightrope walker), and the noisy channel with repetition coding.
- **§4 Counting** — probability by counting, the basic counting principle,
  permutations and $k$-permutations, $\binom{n}{k}$ derived two ways, binomial
  probabilities, partitions and the multinomial coefficient, rec04's three problems
  fully solved, and a which-counting-object recipe.
- **§5 Synthesis, cheatsheet, and the bridge to random variables** — how the pieces fit,
  the master cheatsheet, G1's top gotchas, the outcomes-to-random-variables bridge,
  and mixed practice where the reader picks the tool.

## Widgets

`w-g1s1-sumz` (probability = area for $\{X+Y\le z\}$) · `w-g1s1-romeo` (Romeo &
Juliet meeting window $w$) · `w-g1s2-bayes` (posterior vs prior explorer) ·
`w-g1s2-monty` (running win frequencies, stick vs switch) · `w-g1s3-twocoin` (how a
run of heads makes future heads likelier) · `w-g1s3-repcode` (majority-decoder error
vs $n$ and $\epsilon$) · `w-g1s4-birthday` (collision probability, drag $n$) ·
`w-g1s4-hyper` (hypergeometric vs its binomial cousin).

## Flagship worked problems

Romeo & Juliet, $P(\text{meet}) = 7/16$, confirmed against B&T p. 23 · the radar
detection tree, posterior $0.3426$ · Monty Hall, closed form plus a 200k-trial
simulation converging to $0.334/0.666$ · the drunk tightrope walker · repetition
coding over a binary symmetric channel · birthday collisions, even odds first at
$m = 253$ · rec01 and all three rec04 problems solved end to end.

## Review stats

`transcripts/_g1_review.json` — **47 issues**: 1 critical (§3.6), 11 major, 35 minor,
distributed 6/10/11/9/6/5 across §0–§5. The standout major was a flowchart logic
error where the countable branch fed the discrete uniform law. 49 fixes applied,
8 cross-fragment items deferred to a consistency pass that renumbered 65 practice
items and normalized 49 B&T citations.

## Special notes

- G1 and G2 review artifacts use a `{issues, fixes}` object with a per-section fix
  journal; G3–G7 are plain issue arrays. Anything counting issues across the course
  has to handle both shapes.
- Next: [[Note G2 Discrete Random Variables]].
