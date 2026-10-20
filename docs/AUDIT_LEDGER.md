# AUDIT LEDGER — what has been audited, when, and what came back

One row per **executed audit run**. This is the coverage map the audit docs
don't give individually: briefs are reusable *instruments*, findings docs record
*one run's output*, and the `project-audit` skill deliberately picks ONE target
per session — so nothing else says what has and hasn't been looked at. This does.

Rules: add a row when an audit **executes** (not when a brief is written); every
row carries a **pointer to the findings doc**; verdicts are **point-in-time** — a
row says the target was audited *as of that date*, not that it's still clean
after later changes. Not part of any session's mandatory reading — open it to
scope an audit or to check what has already been covered. Audits are framed
top-down, fundamental decisions first.

## Executed audits

| Date | Target / scope | Instrument | Output | Verdict (one line) | Outstanding |
|------|----------------|------------|--------|--------------------|-------------|
| 2026-10-20 | Template N target 1: does the template reach its projects? (7 data projects) | `project-audit`, decision family; GitHub masters + 4 project sessions | `docs/FINDINGS_template_reach.md` | L0 SOUND (162/184 shipped files identical); L1 CONDITIONAL (permit-speed unconnected, tax-viz only on push, "Use this template" live); L2 CONDITIONAL (`_commit` isn't proof; synced-path and CI-step forks conflict); L3 SOUND | F1 owner: template flag; F2 → TODO E; F3–F7 → TODO O |

## Queued — briefed, not yet run

## Never audited (candidates, roughly ranked)

Template targets, from TODO N (target 1 done 2026-10-20):
- 2. Are the README's "Enforced" claims true?
- 3. Guards with no tests of their own (`check_decisions_log.py`, `check_doc_citations.py`, then the rest)
- 4. Do the docs agree? (`CHANGE_PIPELINE.md` / README / `CLAUDE.md` / skills; size)
- 5. Skills: `handoff`, `steward`, `project-audit`
- 6. Backlog and ledgers
