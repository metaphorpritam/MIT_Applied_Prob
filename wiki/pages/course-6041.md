---
title: MIT 6.041 Course
type: source
status: active
aliases: [6.041, 6.431, course, probabilistic systems analysis]
tags: [course, overview]
sources:
  - ../transcripts/_manifest.json
links:
  relates: [Notes Plan, Build Pipeline]
---

# MIT 6.041 Course

MIT 6.041/6.431 **Probabilistic Systems Analysis & Applied Probability**, Fall 2010,
lecturer John Tsitsiklis. Textbook: Bertsekas & Tsitsiklis, *Introduction to
Probability*, 2nd ed. (539-page PDF in `recitations/book/`).

## Materials

- 25 lecture slide handouts (`lecture_notes/*_LNN.pdf`, 2-up layout, 3–4 pages each)
- 24 recitations: problems (`recitations/questions/*_recNN.pdf`) + official solutions
  (`recitations/solutions/*_recNN_sol.pdf`); recitation N follows lecture N
- Grading artifacts on L01 slide 1 (quizzes Oct 12 / Nov 2, final)

## Verified lecture topics (from slide 1 of each deck)

L01 intro/models · L02 conditioning+Bayes · L03 independence · L04 counting ·
L05 RVs+PMF+E · L06 var, conditional PMF · L07 multiple discrete RVs ·
L08 continuous RVs · L09 multiple continuous · L10 continuous Bayes, derived dist. ·
L11 derived dist., convolution, cov/corr · L12 conditional expectation, sums of random
number of RVs · L13 Bernoulli process · L14 Poisson I · L15 Poisson II ·
L16–L18 Markov chains I–III · L19 limit theorems/WLLN · L20 CLT ·
L21 Bayesian inference I · L22 Bayesian LMS/linear-LMS · L23 classical statistics,
CIs · L24 MLE · L25 binary hypothesis testing.

## Extraction hazards (why we vision-transcribe)

Lecture PDFs have broken font encoding: plain text extraction is interleaved
across slide columns AND garbles digits/punctuation ("Sections olqkolr" =
"Sections 1.1–1.2"). Ground truth = page rasters in `raster/` (150 DPI).
Recitation PDFs extract cleanly but their figures are vector → invisible to
image extraction; captured via page rasters instead. See [[Build Pipeline]].
