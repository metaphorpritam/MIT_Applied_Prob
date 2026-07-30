export const meta = {
  name: 'review-note',
  description: 'Adversarial review of a built note: math lens, render lens, pedagogy lens; then per-section fixes',
  phases: [
    { title: 'Review', detail: 'independent lenses (Opus 5 medium)', model: 'opus' },
    { title: 'Fix', detail: 'per-section fixers for confirmed issues', model: 'opus' },
  ],
}

// args: { slug, noteFile, shotsDir, sections: [0,1,...], transcripts: ['L01',...],
//         mathSplit: [[secs...],[secs...]] }
const ROOT = 'd:/Python-UV/MIT_Applied_Prob'
const A = typeof args === 'string' ? JSON.parse(args) : args
const { slug, noteFile, shotsDir, sections, transcripts, mathSplit } = A

const ISSUES_SCHEMA = {
  type: 'object',
  required: ['lens', 'issues'],
  properties: {
    lens: { type: 'string' },
    issues: {
      type: 'array',
      items: {
        type: 'object',
        required: ['section', 'severity', 'description'],
        properties: {
          section: { type: 'integer', description: 'section number the issue is in' },
          severity: { type: 'string', enum: ['critical', 'major', 'minor'] },
          description: { type: 'string', description: 'specific: what is wrong, where (sub-section/figure/formula), and what correct looks like' },
        },
      },
    },
  },
}

const FIX_SCHEMA = {
  type: 'object',
  required: ['section', 'fixed', 'skipped'],
  properties: {
    section: { type: 'integer' },
    fixed: { type: 'array', items: { type: 'string' } },
    skipped: { type: 'array', items: { type: 'string' }, description: 'issues NOT fixed + why (disagree/cannot reproduce)' },
  },
}

const commonCtx = `Note under review: ${ROOT}/notes/${noteFile} (assembled from fragments ${ROOT}/notes/src/fragments/${slug}_s*.html).
Ground-truth transcripts: ${transcripts.map(t => `${ROOT}/transcripts/${t}.md`).join(', ')}.
Compute scripts + JSON: ${ROOT}/computes/${slug}_s*.py/.json. Style contract: ${ROOT}/notes/_build/STYLE_CONTRACT.md.${A.hint ? `\nKNOWN SUSPECTS (verify these first): ${A.hint}` : ''}`

phase('Review')
const lensJobs = []

// Math lenses (split sections between two agents)
for (let i = 0; i < mathSplit.length; i++) {
  const secs = mathSplit[i]
  lensJobs.push(() => agent(`ADVERSARIAL MATH REVIEW (lens: math-${i}) of sections ${secs.join(', ')} of a probability study note. Assume errors exist; find them.
${commonCtx}

For EACH of your sections (fragments ${secs.map(n => `${slug}_s${n}.html`).join(', ')}):
1. Read the fragment. Re-derive EVERY derivation independently — every algebra step, every probability computation, every stated theorem condition. Check substituted numeric values by recomputing (run python via 'uv run' freely).
2. Cross-check every claim against the ground-truth transcripts (the notes must agree with the verified source; deviations must be flagged unless they are marked expansions).
3. Check every number in prose/tables against the computes JSON; rerun the compute script if suspicious.
4. Check LaTeX validity for MathJax (unbalanced $, \\text misuse, raw < > that should be &lt; &gt;, broken \\frac...).
5. Widget JS math: read the draw() code, verify formulas match the derived math.
Report ONLY real, specific issues (severity: critical = wrong math/wrong number; major = misleading/uncited/contract violation; minor = style). No praise, no padding. lens='math-${i}'.`,
    { label: `review:math-${i}`, phase: 'Review', schema: ISSUES_SCHEMA, model: 'opus', effort: 'medium' }))
}

// Render lens — reads the screenshots
lensJobs.push(() => agent(`ADVERSARIAL RENDER REVIEW (lens: render) of a built HTML study note.
${commonCtx}
Screenshots of the rendered page: Glob ${shotsDir}/*.png and Read EVERY one. Naming: s<N>_p<K>.png = print-rendered page K of section N (full coverage, print CSS hides sidebar and widget controls); s<N>_live.png = live viewport of section N's top (sidebar TOC, widget controls and canvases visible).
Hunt for: raw unrendered LaTeX ($..$ visible, \\frac visible), overlapping/clipped text, figures with overlapping labels or crossing arrows or illegible text, blank/broken widget canvases (a widget frame with empty white plot area or missing controls), broken figure images (alt-text boxes), tables overflowing, headings colliding, missing figure captions, orphaned placeholders like {{IMG:...}}.
Also: aesthetic judgment — cramped spacing, figures ridiculously large/small, inconsistent numbering visible on screen (Fig. N.k sequence per section).
Map each finding to its section number (from the s<N> filename prefix). Report ONLY real, visible issues with the exact screenshot filename. lens='render'.`,
    { label: 'review:render', phase: 'Review', schema: ISSUES_SCHEMA, model: 'opus', effort: 'medium' }))

// Pedagogy/completeness lens
lensJobs.push(() => agent(`ADVERSARIAL PEDAGOGY & COMPLETENESS REVIEW (lens: pedagogy).
${commonCtx}
Inventories: ${ROOT}/transcripts/_summary.json (unsolved_examples/gaps per source) and ${ROOT}/transcripts/_verification.json (residual concerns).
1. For each source transcript of this note (${transcripts.join(', ')}): list its [UNSOLVED EXAMPLE]s and [DERIVATION GAP]/[SOLUTION GAP]s, then verify EACH is actually solved/filled somewhere in the note fragments (grep ${ROOT}/notes/src/fragments/${slug}_s*.html). Missing ones are CRITICAL.
2. Check the user's quality contract per topic: interpretation box present? at least one gotcha? 1-3 practice questions with solutions? citations (srcref) present? recipe/flowchart at decision points?
3. Check narrative flow: does each section open with motivation, do sections reference each other correctly, does the numbering match the sidebar structure (h2/h3 hierarchy sane)?
4. Check practice questions are actually solvable from the material and their hidden solutions are correct (spot-check by solving 3-4 yourself).
Report specific gaps only. lens='pedagogy'.`,
    { label: 'review:pedagogy', phase: 'Review', schema: ISSUES_SCHEMA, model: 'opus', effort: 'medium' }))

const lensResults = (await parallel(lensJobs)).filter(Boolean)
const allIssues = lensResults.flatMap(r => (r.issues || []).map(i => ({ ...i, lens: r.lens })))
const bySec = {}
for (const i of allIssues) (bySec[i.section] = bySec[i.section] || []).push(i)
log(`review found ${allIssues.length} issues (${allIssues.filter(i => i.severity === 'critical').length} critical) across sections ${Object.keys(bySec).join(',')}`)

phase('Fix')
const fixResults = await parallel(Object.entries(bySec).map(([sec, issues]) => () =>
  agent(`You are fixing confirmed review issues in section ${sec} of study note ${noteFile}.
${commonCtx}
Your fragment: ${ROOT}/notes/src/fragments/${slug}_s${sec}.html. Its computes: ${ROOT}/computes/${slug}_s${sec}*.py. Its figures: ${ROOT}/notes/img/${slug}_s${sec}_*.png.

ISSUES (from independent reviewers — verify each before fixing; if a reviewer is wrong, skip with reason):
${issues.map((i, k) => `${k + 1}. [${i.severity}/${i.lens}] ${i.description}`).join('\n')}

Rules: fix in the FRAGMENT (not the built HTML); recompute numbers via the compute script when they change; regenerate + re-view any figure you touch; keep the style contract; keep section-local figure numbering consecutive. Return the structured JSON (section=${sec}).`,
    { label: `fix:s${sec}`, phase: 'Fix', schema: FIX_SCHEMA, model: 'opus', effort: 'medium' })
))

return {
  issues: allIssues,
  fixes: fixResults.filter(Boolean),
  critical_count: allIssues.filter(i => i.severity === 'critical').length,
}