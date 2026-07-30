---
title: Note G4 Iterated Expectations and Arrival Processes
type: concept
status: active
aliases: [G4]
tags: [notes, g4]
sources:
  - ../notes/04_expectation_processes.html
  - ../notes/src/fragments/g4_s0.html
  - ../notes/src/fragments/g4_s1.html
  - ../notes/src/fragments/g4_s2.html
  - ../notes/src/fragments/g4_s3.html
  - ../notes/src/fragments/g4_s4.html
  - ../notes/src/fragments/g4_s5.html
  - ../transcripts/_g4_review.json
links:
  relates: [Notes Plan, MIT 6.041 Course, Note G3 Continuous Random Variables, Note G5 Markov Chains]
---

# Note G4 Iterated Expectations and Arrival Processes

`notes/04_expectation_processes.html` — 3.4 MB, 27 figures, 6 widgets, 36 practice
items; the authoring pass solved 42 examples and filled 52 gaps. Covers
[[MIT 6.041 Course]] L12–L15 with rec13–15 (plus rec12, see below). Tracked in
[[Notes Plan]]; assembled by [[Build Pipeline]].

## Section map

- **§0 Orientation** — two themes: $\mathbb{E}[X\mid Y]$ is itself a random variable,
  and a random process is an infinite family of random variables.
- **§1 Conditional expectation as a random variable** — $\mathbb{E}[X\mid Y=y]$ versus
  $\mathbb{E}[X\mid Y]$, the law of iterated expectations, conditional variance and the
  law of total variance, L12's worked *and* unworked examples, and rec12 worked in full.
- **§2 Random sums and the Bernoulli process** — the two laws sharpened on rec13 P1–P2,
  the sum of a random number of random variables, the Bernoulli process and its first
  properties, interarrival times / memorylessness / the fresh-start property, the
  Pascal PMF for the $k$th success, and merging and splitting.
- **§3 The Poisson process I** — the three defining properties, binomial $\to$ Poisson
  derived rather than asserted, the exponential first interarrival, the Erlang $k$th
  arrival time, and the Bernoulli/Poisson dictionary with rec14.
- **§4 Poisson II** — Poisson fishing as a warm-up, merging independent Poisson
  processes, splitting, random incidence for the Poisson process, length-biasing in
  general renewal processes, and rec15 fully worked.
- **§5 Synthesis, gotchas, and the bridge to Markov chains** — the conditioning toolkit
  on one page, one process on two clocks, the four expensive mistakes, and where the
  independence goes next.

## Widgets

`w-g4s1-vardecomp` (total-variance decomposer: two groups, sliders for means and
spreads) · `w-g4s2-bernoulli` (sample path plus interarrival histogram) ·
`w-g4s3-binpois` (slide $n$ with $np = \lambda t$ held fixed) · `w-g4s4-merge`
(competing exponentials: who arrives first?) · `w-g4s4-pin` (drop a pin on the time
axis — which interval do you land in?) · `w-g4s4-incidence` (histogram of observed
interval lengths).

## Flagship worked problems

Recitation 12 in full · rec13 P1–P2 as the two-laws warm-up · rec14's
Bernoulli/Poisson dictionary problems · Poisson fishing · random incidence and the
length-biasing paradox, both analytically and by simulation · rec15 end to end ·
the binomial-to-Poisson limit derived step by step.

## Review stats

`transcripts/_g4_review.json` — **38 issues**: 1 critical, 9 major, 28 minor,
distributed 4/7/7/9/4/7 across §0–§5; 33 fixes, then a consistency pass with 15 edits
including 2 cross-note repairs. The major at §1.5 was an arithmetically incoherent
antiderivative evaluation inside a filled `[SOLUTION GAP]` — the sort of thing only
line-by-line re-derivation catches.

## Special notes — the recitation offset

From recitation 12 on, recitation $N$ stops tracking lecture $N$. **rec12 is G3
material** (continuous random variables), so rather than drop it, it is worked in full
as §1.5 of this note; G4's own aligned recitations are rec13–15. The full offset was
established by topic-mapping rec16–24 before G5 launched (rec16/17 = review, rec18/19 =
Markov, rec20–22 = limits/Bayesian, rec23/24 = classical), the recitation columns in
[[Notes Plan]] were corrected to match, and every downstream review agent was briefed
with explicit offset hints.

Prev: [[Note G3 Continuous Random Variables]] · Next: [[Note G5 Markov Chains]].
