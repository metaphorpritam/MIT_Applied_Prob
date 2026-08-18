# Session log

Append-only. One entry per working session — what was read, what changed, what's next. Newest at the bottom.

## 2026-07-28 10:55 UTC — tags: session

Session 1: read skills; ingested 74 sources -> corpus; built PageIndex (944pp/880 nodes); rasterized 215 pages; init wiki; built+smoke-tested note template (sidebar TOC, plot.js widgets, build_note.py — JS must load in <head>); transcribed all 49 sources (92 unsolved examples, 167 gaps, 148 figures, 220 anomalies inventoried in transcripts/_summary.json); adversarial verify pass launched. Next: finish verify, caption corpus figures, build G1 notes.

## 2026-07-28 11:03 UTC — tags: session

Transcript verification done: 49/49, 19 clean, 30 fixed (fabricated labels caught, tree branching corrected). Corpus figures captioned (46) + index rebuilt. Reports in transcripts/_verification.json. Launching G1 authoring.

## 2026-07-28 15:33 UTC — tags: session

G1 authoring workflow hit session token limit (resets 21:00 IST): s0 done (roadmap fig + computes), s1-s5 failed pre-write. Resume via Workflow resumeFromRunId wf_1f43c537-922 (s0 cached). Hourly wakeups armed until reset.

## 2026-07-28 15:54 UTC — tags: session, g1

G1 authoring complete (6/6): 25 examples solved, 38 gaps filled, 53 practice Qs, 32 figures, 8 widgets. Assembled+built 01_probability_basics.html (3.15MB, validations pass). Screenshot sweep running; adversarial review next. Author-confirmed: R&J P(meet)=7/16 vs book p.23; radar posterior 0.3426; Monty 200k-sim 0.334/0.666.

## 2026-07-28 16:30 UTC — tags: session, g2

G2 authoring done (6/6): built 02_discrete_rvs.html (3.2MB, 25 figs, 4 widgets); shots running. Known issue for review: s0 roadmap guessed peer split (s3-s5 labels may mismatch actual scopes). G1 review in flight.

## 2026-07-28 16:48 UTC — tags: session, g1

G1 review done: 47 issues (1 crit §3.6, 11 major incl. flowchart logic error — countable branch fed uniform law, 35 minor), 49 fixes applied by 6 fixers; 8 cross-fragment skips -> consistency agent running (practice numbering, B&T cite style). Saved transcripts/_g1_review.json. G2 review in flight. Next: G1 rebuild + re-shoot + hub flip.

## 2026-07-28 21:21 UTC — tags: session, recovery

Session limit hit (resets 02:00 IST) killed G2 review (4 lenses, 0 results) + G1 consistency agent (died before edits). Token-free work done: G1 rebuilt WITH 49 review fixes (3.2MB), re-shoot running, hub statuses updated. QUEUE AFTER 02:00: (1) relaunch G1 consistency agent (practice numbering, B&T cites, decision-guide practice check), (2) resume G2 review workflow wf_743e61c1-510 with same args+hint, (3) after G2 fixes: rebuild+reshoot G2, (4) G3 authoring workflow (L08-L11 + rec08-11). Hourly keepalive wakeups armed.

## 2026-07-28 21:24 UTC — tags: session, recovery

02:51 IST reset recovery: relaunched G1 consistency agent + resumed G2 review (hint wired) + launched G3 authoring (L08-L11+rec08-11; rec10 used as checkpoint set in s5; consistency lessons baked into author prompts). G1 re-shot post-fixes (81 pages clean).

## 2026-07-28 21:41 UTC — tags: session, g1

G1 COMPLETE: consistency pass (65 practice items renumbered, 33+16 B&T cites normalized, decision-guide practices verified) + final build green (3.2MB, 32 figs, 8 widgets). Hub card flipped. Full chain: author -> build -> shoot(80) -> 3-lens review (47 issues) -> 49 fixes -> re-shoot(81) -> consistency -> done. G2 review + G3 authoring still in flight.

## 2026-07-28 21:45 UTC — tags: session, g2

G2 review done: 49 issues (2 crit, 25 major, 22 minor), 46 fixes. Stars: scipy/numpy geometric-convention claim FALSIFIED by reviewer actually running both libs; all 3 hint suspects confirmed+fixed; mathbf{E}->mathbb{E} uniform (0 left). Rebuilt 3.28MB. Re-shoot running; consistency pass queued after. Saved transcripts/_g2_review.json.

## 2026-07-28 21:54 UTC — tags: session, g3

G3 authored 6/6 (rec08 P3e source typo caught+corrected by author; Buffon's needle solved; 38 figs, 5 widgets incl. convolution animator). Fixed validator false-positive (book Fig cite convention: 'its Figure x.y') + unclosed p in s2. Built 5.9MB, shot 95 imgs, review launched with 7 author-concern hints. G2 consistency agent still running.

## 2026-07-28 21:56 UTC — tags: session, handoff

SESSION 1 CLOSING (10% ctx left). G1 DONE. G2: consistency agent in flight at close - verify fragments, rebuild 02, flip hub. G3: review wf_22ffd7da-af2 in flight - harvest journal, extract+verify fixes, rebuild 03, re-shoot --redo, consistency agent, flip hub. Then G4 (L12-15+rec12-15), G5 (L16-18+rec16-18), G6 (L19-22+rec19-22), G7 (L23-25+rec23-24) via g3_author_workflow.js template + review_note_workflow.js. End-of-project: wiki concept pages, pageindex the notes+transcripts, final audit, hub all-green, browser UX check.

## 2026-07-28 21:57 UTC — tags: session, g2

G2 COMPLETE (consistency: 34 renumbers, 49 cite fixes, 1 real G1-crossref fix; builds green; hub flipped). Only G3 review wf_22ffd7da-af2 still in flight this session. Leftover flagged: g2_s4 'Problem 4.A/B/C' label style — cosmetic, revisit if desired.

## 2026-07-29 06:27 UTC — tags: session, g4

11:55 resume: G3 review resumed (wf_22ffd7da-af2, same hints). G4 authoring launched (g4_author_workflow.js in scratchpad; conventions+G1-G3 section maps baked in). Meta/target files for 04 written.

## 2026-07-29 07:04 UTC — tags: session, g4

G4 built (first-try clean assembly!) + shot (65pp, 0 fail) + review launched wf_68b6202a-f40 with offset hints. G4 authors: 42 solved, 52 gaps, 31 practice, 27 figs. G3 review still in flight (wf_22ffd7da-af2 resumed).

## 2026-07-29 07:08 UTC — tags: session, g3

G3 review done: 56 issues (2 crit incl. dice-convolution off-by-one in compute, 21 major, 33 minor), 53 fixes. Rebuilt 5.9MB; re-shoot --redo + consistency agent running. G4 review wf_68b6202a-f40 in flight. After both: flip G3+G4 hub cards, launch G5 (VERIFY rec16-18 coverage by topic first - offset!).

## 2026-07-29 09:47 UTC — tags: session, recovery

15:15 reset recovery: G4 review resumed (lenses cached, render+6 fixers live); G3 consistency agent relaunched; rec16-24 topic map verified (rec16/17=review->G5 checkpoint, rec18/19=G5, rec20-22=G6, rec23/24=G7); G5 authoring launched. G3 re-shoot s2/s4 pending after consistency (run shoot_sections g3 <dir> without --redo).

## 2026-07-29 09:57 UTC — tags: session, g3

G3 COMPLETE (consistency: 42 edits incl. 12 cross-note cite fixes; builds green; hub flipped). Notes Plan recitation columns corrected for offset. G5 authoring status update in flight; s2/s4 G3 shots refresh queued.

## 2026-07-29 10:07 UTC — tags: session, g4

G4 review done (38 issues: 1 crit, 9 major, 28 minor; 33 fixes), rebuilt 3.3MB, re-shot clean. G4 consistency agent + G5 authoring in flight. After both: flip G4+G5 cards, G5 build/shoot/review, then G6+G7 briefs (rec20-22 / rec23-24).

## 2026-07-29 10:15 UTC — tags: session, g4

G4 COMPLETE (consistency: 15 edits, 2 cross-note fixes; builds green; hub flipped). 4 of 7 done. G5 authoring far along (g5_s3 exists; known issue for G5 polish: 'B&T's Figure 7.14' at g5_s3:524). Next: G5 build/shoot/review, G6+G7 briefs.

## 2026-07-29 10:35 UTC — tags: session, g5, g6

G5 shot complete (80 imgs), review launched wf_25540004-8c9 (8 hints incl. rec18 P2 copyright absence). G6 authoring launched (forward-ref 'Figure N.k' convention now in author prompts).

## 2026-07-29 14:58 UTC — tags: session, recovery

20:27 resume after 8:10pm reset: G5 review + G6 authoring both relaunched (both had 0 cached agents). G7 brief still to write (L23-25+rec23-24, template: g6 script).

## 2026-07-29 15:26 UTC — tags: session, g5

G5 review done: 50 issues (4 crit: checkout boundary-row model inconsistency propagated 6 places, stale MC numbers vs JSON; 16 major, 30 minor), 47 fixes. Rebuilt 5.3MB. Re-shoot + consistency agent running (accepted small risk of concurrent fragment edits vs shots — shots archival at this stage). G6 authoring continues.

## 2026-07-29 15:30 UTC — tags: session, g5

G5 COMPLETE (consistency: 4 edits, 0 cross-note mismatches — convention discipline holding; builds green; hub flipped). 5 of 7 done. G6 authoring in flight; G7 next.

## 2026-07-29 15:36 UTC — tags: session, handoff

SESSION CHECKPOINT (10% ctx): G6 authored 6/6 + built 4.2MB (fixed 2 orphan p-closers in g6_s1 lines 530/533) + hub card unlocked. G6 workflow wf_16f884fb-085 may still emit final notification (5/6 returned when built). NEXT QUEUE: (1) shoot g6 -> review (hints: none major; check g6_s1 orphan-closer area renders; conventions) -> fixes -> rebuild -> consistency -> flip. (2) G7 authoring wf_415f7fa2-465 in flight -> same chain when done (assemble may need fig-ref/p-tag fixes as usual). (3) Closing pass: wiki concept pages, pageindex ingest of notes/ + transcripts/ + rebuild index, final audit, hub all-green, browser UX check.

## 2026-07-30 06:48 UTC — tags: session, recovery

API recovered; G6 review + G7 authoring relaunched (both from cached runIds). Dark mode queued after G7 (dark chrome + white figure plates, toggle in sidebar, rebuild all notes).

## 2026-07-30 07:11 UTC — tags: session, handoff

FINAL HANDOFF (2% ctx): G1-G5 done. G6 review wf_aa03bd42-b94 + G7 authoring wf_415f7fa2-465 RUNNING at close — next session: recovery ritual, harvest journals, then per queue: G6 fixes->rebuild->reshoot->consistency->flip; G7 assemble->build->shoot->review->polish->flip; DARK MODE polish (dark chrome+white plates+sidebar toggle, rebuild all); closing pass (concept pages, pageindex notes+transcripts, audit, hub all-green, browser UX check). G5 shots complete (15 filled).

## 2026-07-30 09:52 UTC — tags: session, milestone

MILESTONE: ALL 7 NOTES EXIST AND ARE READABLE. G7 authored 6/6 (caught B&T 9.8c rounding slip!) + built 5.1MB/30 figs/5 widgets + card unlocked + shots running. G6 fixers in flight. Remaining: G6 rebuild+polish+flip; G7 review+polish+flip; dark mode; closing pass.

## 2026-07-30 09:52 UTC — tags: session, g6

G6 review COMPLETE (10/10): critical CLT-section numbers fixed + ~20 more. Rebuilt. EDGE HEADLESS BROKEN system-wide (print-to-pdf outputs nothing, even on index.html) — G6 re-shoot + G7 shoot/review BLOCKED on Edge recovery; retry later (user closing browser may fix). G6 consistency agent launching now.

## 2026-07-30 10:09 UTC — tags: session, g6

G6 COMPLETE (consistency: 8 edits, 2 real cross-note fixes; builds green; card flipped). 6 of 7 done. BLOCKED: Edge headless still broken -> G7 shots+review wait; retry each wake. G7 is built+readable meanwhile. Then: G7 review chain, dark mode, closing pass.

## 2026-07-30 10:12 UTC — tags: session, g7

G7 shot via Chrome fallback (72pp clean; Chrome added to shooter candidates permanently). Final review launched wf_9c375e1a-a62 with 7 hints (OCR-mangled transcripts -> verify vs book; B&T 9.8c slip; finale design). After: fixes->rebuild->consistency->flip, then DARK MODE, then closing pass.

## 2026-07-30 10:46 UTC — tags: session, g7

G7 review done: 49 issues (4 crit incl. JS PRNG float-overflow in MLE widget — reviewer emulated IEEE-754 to prove it — and an alpha-budget-busting rejection region; 12 major, 33 minor), 50 fixes. Rebuilt 5.1MB, re-shot. Consistency agent (the last one!) running. Then: flip G7, DARK MODE, closing pass.

## 2026-07-30 11:07 UTC — tags: session, milestone

ALL SEVEN NOTES COMPLETE. G7 consistency: 84 edits (s3 shared-counter split, ML/MAP font unification, 3 cross-note fixes), builds green, card flipped. Totals across course: ~330 review issues found+fixed, 226 figures, 36 widgets. Next: DARK MODE, then closing pass.

## 2026-07-30 11:22 UTC — tags: session, closing

PROJECT CLOSING: hub regenerated (was 0 bytes — dark-mode script crash truncation, caught by wiki agent), all 7 cards green + dark toggle. Wiki: 11 pages, 78 edges, 0 errors, manifest hashed. PageIndex self-referential (181 sources incl. notes+transcripts). Course totals: ~330 review issues found+fixed, 226 figures, 36 widgets, 7 notes.

## 2026-07-30 16:26 UTC — tags: session, launch

Post-launch: feedback features (email box on hub + sidebar links in notes) deployed and verified live. skill_learnings.md written at project root (uncommitted — awaiting user decision on publishing it to the public repo). Site fully live at metaphorpritam.github.io/MIT_Applied_Prob.

## 2026-08-14 18:52 UTC — tags: session, expansion

Post-launch expansion: cheatsheet audit (189 items; 3 in-syllabus gaps, 1 dangling-citation defect). ALL 4 TIER-1 PATCHES LANDED+VERIFIED (g3_s2 joint CDF; g3_s4 binomial additivity + jointly-normal exception + named Cauchy-Schwarz so G6 cite resolves; g5 doubly-stochastic + detailed balance; g1 three-set I-E + stars-and-bars + hypergeometric variance). New pages in flight: qb (150 Qs, 103 written, s1/s4 resuming) + rf (reference/enrichment, s2 resuming). NOTE: connection-loss failures now a 3rd failure mode alongside token limits — computes survived, HTML did not; resume works.

## 2026-08-15 04:23 UTC — tags: session, qb, bugfix

QB render review found a REAL BUG affecting ALL 9 pages: print CSS had 'details.sol { open: true; }' — 'open' is an HTML attribute not a CSS property, so it was silently discarded and every printed/PDF copy carried ZERO solutions. Fixed with proper display rules + marker suppression; also hid .qbfilter in print, normalized qb_s7 h2 (was the only one carrying a Q-range, wrapping the TOC), code-wrapped qb_s2 srcref path. Verifying by re-shoot. Math/pedagogy lenses for qb and ALL rf lenses died on token limit (resets 3:30am) — must re-run: Workflow resume wf_dc345a8e-209 (qb) and wf_c8516af1-c35 (rf).

## 2026-08-18 21:07 UTC — tags: session, rf, review

RF review (8/8) found REAL defects, all fixed+verified: 9 TAB chars replacing \text (rendered as 'extExp(lambda)' garbage), order-statistic sd column asymmetric/wrong for j=4,5 (now symmetric 0.140859/0.178174/0.188982/...), simulated columns disagreeing with compute JSON, systematic off-by-one in EVERY section pointer on the navigation page (said §1-2 lookup/§3-4 enrichment; actual §1/§2-3), 'eighth and last'->ninth, '150 questions'->170, wrong independence inventory. Contrast with the qb math-0 lens which produced 2 hallucinated 'criticals'. LESSON: demand file+JSON evidence in review prompts; it separates the two.

## 2026-08-18 21:09 UTC — tags: session, qb, provenance

QB review round 2 (12/12): found a PROVENANCE defect class — math correct but quoted Monte-Carlo/enumeration figures stale or fabricated. qb_s1 Q10's compute block still computed a DELETED problem; qb_s2 Q46's block was for a different problem entirely; Q47 MC off by 0.005; EIGHT stale MC values in qb_s5; qb_s7 missing its srcref. All fixed+verified (q10/q46 compute blocks rewritten and re-run). The two hallucinated 'criticals' were correctly SKIPPED by the fixers thanks to the calibration warning. Lesson for skill_learnings: a compute script can drift out of sync with its prose when a question is re-modelled — reviewers must diff prose numbers against JSON keys, not just recompute.
