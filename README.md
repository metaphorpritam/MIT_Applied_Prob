# MIT 6.041 · Interactive Study Notes

The complete **MIT 6.041/6.431 Probabilistic Systems Analysis & Applied Probability**
course (Fall 2010, John Tsitsiklis) compiled into **seven interactive, adversarially
reviewed HTML study notes** — full step-by-step derivations, every recitation problem
solved, 226 regenerated figures, and 36 live widgets (Monty Hall simulator,
convolution animator, CLT animator, gambler's ruin explorer, …).

**Read online:** enable GitHub Pages (Settings → Pages → deploy from `main` / `docs/`)
and open the site root.

**Read offline:** download `mit6041_interactive_notes_offline.zip` from the site (or
build it — see below). Every note in the zip is a single self-contained HTML file:
open it in any browser, desktop or mobile. No installation, no folders.

## The seven notes

| # | Note | Lectures |
|---|------|----------|
| G1 | Probability Fundamentals — axioms, conditioning, Bayes, independence, counting | L01–L04 |
| G2 | Discrete Random Variables — PMFs, expectation, variance, joint PMFs | L05–L07 |
| G3 | Continuous Random Variables — PDFs, continuous Bayes, derived distributions | L08–L11 |
| G4 | Iterated Expectations & Arrival Processes — random sums, Bernoulli, Poisson | L12–L15 |
| G5 | Markov Chains — classification, steady state, absorption | L16–L18 |
| G6 | Limit Theorems & Bayesian Inference — Chebyshev, WLLN, CLT, MAP, LMS | L19–L22 |
| G7 | Classical Statistical Inference — CIs, maximum likelihood, regression, LRT | L23–L25 |

## How these were made

Compiled with a multi-agent pipeline: vision transcription of every lecture slide and
recitation page (double-verified against page rasters), section authoring with every
numerical value recomputed in Python (`computes/`), matplotlib figure regeneration,
then a four-lens adversarial review per note (~330 issues found and fixed) and a
consistency polish. Source transcripts are in `transcripts/`; note sources in
`notes/src/`; the build tooling in `notes/_build/`.

Rebuild both distributions (website → `docs/`, offline zip → `dist/`):

```bash
cd notes && uv run _build/make_release.py
```

## License & attribution

Compiled from [MIT OpenCourseWare](https://ocw.mit.edu) course 6.041/6.431
(Fall 2010, John Tsitsiklis) and the companion textbook *Introduction to
Probability*, 2nd ed. (Bertsekas & Tsitsiklis, Athena Scientific, 2008).

Content is licensed **CC BY-NC-SA 4.0**, per MIT OCW's terms. This is an
independent study resource — **not affiliated with or endorsed by MIT**.
The textbook itself is not included in this repository.
