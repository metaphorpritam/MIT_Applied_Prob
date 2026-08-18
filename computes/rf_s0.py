# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Numbers quoted in fragments/rf_s0.html (R - Reference & Enrichment, section 0).

Section 0 is orientation prose: it quotes no probability values, only counts of
the corpus it points at.  Every one of those counts is recomputed here from the
files themselves so that nothing in the section is hand-asserted.

Outputs: printed report + computes/rf_s0.json
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent          # .../MIT_Applied_Prob
FRAG = ROOT / "notes" / "src" / "fragments"
AUDIT = ROOT / "cheatsheet_audit.json"

out: dict[str, object] = {}

# ---------------------------------------------------------------- teaching notes
# The seven teaching notes are the fragment families g1..g7; the question bank is
# qb; this page is rf.
frags = sorted(p.name for p in FRAG.glob("*.html"))
note_frags = [f for f in frags if re.match(r"^g[1-7]_s\d+\.html$", f)]
groups = sorted({f[:2] for f in note_frags})
out["n_teaching_notes"] = len(groups)                       # 7
out["n_note_fragments"] = len(note_frags)                   # sections across G1-G7
out["note_groups"] = groups

# Sections per note, excluding the s0 orientation and s5 summary fragments:
# each note has numbered teaching sections s1..s4.
per_note = Counter(f[:2] for f in note_frags)
out["fragments_per_note"] = dict(sorted(per_note.items()))
out["teaching_sections_per_note"] = sorted(
    {sum(1 for f in note_frags if f[:2] == g and re.search(r"_s[1-4]\.html$", f))
     for g in groups}
)                                                            # [4]
out["n_teaching_sections_total"] = sum(
    1 for f in note_frags if re.search(r"_s[1-4]\.html$", f)
)                                                            # 28

# ---------------------------------------------------------------- question bank
# Question cards carry class "ex qcard" with an id qNN.
qb_text = "".join(
    (FRAG / f).read_text(encoding="utf-8") for f in frags if f.startswith("qb_")
)
qids = sorted(int(m) for m in set(re.findall(r'class="ex qcard" id="q(\d+)"', qb_text)))
out["qb_cards_present_now"] = len(qids)
# The bank's own stated size (qb_s0 declares it); recorded so the two can be
# compared once every qb fragment has landed.
m = re.search(r"holds <b>(\d+) questions</b>", qb_text)
out["qb_declared_size"] = int(m.group(1)) if m else None

# ------------------------------------------- where the distribution facts live
# The audit's structural finding: the named-distribution facts (PMF/PDF, mean,
# variance) are spread over the per-note summary fragments rather than sitting in
# one table.  Recompute which fragments actually carry such a summary table.
DIST_WORDS = ["Bernoulli", "Binomial", "Geometric", "Poisson", "Uniform",
              "Exponential", "Normal", "Erlang"]
summary_tables = []
for f in note_frags:
    txt = (FRAG / f).read_text(encoding="utf-8")
    if "<table" not in txt:
        continue
    hits = sum(1 for w in DIST_WORDS if w in txt)
    if hits >= 5 and ("\\operatorname{var}" in txt or "variance" in txt.lower()):
        summary_tables.append((f, hits, txt.count("<table")))
out["fragments_with_distribution_tables"] = [f for f, _, _ in summary_tables]
out["n_fragments_with_distribution_tables"] = len(summary_tables)

# ---------------------------------------------------------------- the audit
audit = json.loads(AUDIT.read_text(encoding="utf-8"))
verdicts = Counter(x["verdict"] for x in audit["items"])
out["audit_items_total"] = len(audit["items"])
out["audit_verdicts"] = dict(verdicts)
out["audit_covered"] = verdicts["COVERED"]
out["audit_partial"] = verdicts["PARTIAL"]
out["audit_out_of_syllabus"] = verdicts["MISSING_OUT_OF_SYLLABUS"]
out["audit_in_syllabus_gaps"] = verdicts["MISSING_IN_SYLLABUS"]
out["audit_covered_or_partial_pct"] = round(
    100.0 * (verdicts["COVERED"] + verdicts["PARTIAL"]) / len(audit["items"]), 1
)

# ---------------------------------------------------------------- report
print("=" * 66)
print("rf_s0 — orientation counts")
print("=" * 66)
print(f"teaching notes (G1-G7)            : {out['n_teaching_notes']}")
print(f"note fragments on disk            : {out['n_note_fragments']} "
      f"({out['fragments_per_note']})")
print(f"numbered teaching sections s1-s4  : {out['n_teaching_sections_total']} "
      f"({out['teaching_sections_per_note']} per note)")
print(f"question cards present now        : {out['qb_cards_present_now']}")
print(f"question bank declared size       : {out['qb_declared_size']}")
print(f"fragments carrying a distribution summary table: "
      f"{out['n_fragments_with_distribution_tables']}")
for f, hits, nt in summary_tables:
    print(f"    {f:14s} distribution-name hits={hits:2d} tables={nt}")
print(f"cheatsheet audit items            : {out['audit_items_total']}")
for k, v in sorted(verdicts.items()):
    print(f"    {k:26s} {v:4d}")
print(f"covered or partial                : {out['audit_covered_or_partial_pct']}%")

(Path(__file__).parent / "rf_s0.json").write_text(
    json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print("\nwrote computes/rf_s0.json")
