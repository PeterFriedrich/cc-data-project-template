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
| 2026-10-20 | Template N target 2: are the README's "Enforced" claims true? | `project-audit`, correctness family; each mechanism broken on purpose in a scratch clone; protection on 8 repos | `docs/FINDINGS_enforced_claims.md` | 9 PASS; doc-citation guard FAIL (backticked `§N` and `§"title"` never checked; tax-viz 25 dead, CI green); protection WARN (3 of 4 public projects unprotected); pre-push WARN (guards HEAD, not pushed refs); surfaced FAIL: archive append-only has no CI guard (tax-viz lost 3,449 lines for 26 days) | TODO P; protection is the owner's |
| 2026-11-11 | The planned user-level rules home (a plan; nothing installed): the 2026-11-05 draft, 27 duplicated memories, `server`'s hardening | `project-audit`, decision family; brief `AUDIT_user_rules_home.md` (out of repo); memory folders, live settings, server-ops read directly; `server` asked | `docs/FINDINGS_user_rules_home.md` | L0 CONDITIONAL (fixes reach, not drift; no path for new corrections; no hook); L1 CONDITIONAL (12 of 21 memories lose their always-loaded line; no skill trigger tested); L2 CONDITIONAL (the 4 merges are faithful; push scope widens; one project's permissions travel); L3 UNSOUND as written (no deny on `~/.claude/**`, Bash writes uncovered; every session can write server-ops `main`) | F14, F15, F18, F19 → `server`; F9, F11, F17 → owner; F2, F6 → `template` (TODO R, `project-audit` appendix); draft edits in `research/` |

## Queued — briefed, not yet run

Briefs live out of repo, in `/home/opc/research/cc-data-project-template/audits/` (a `docs/AUDIT_*.md` here would ship to every project through copier). Each runs in its own fresh session (Fable 5.1, own worktree), queued 2026-11-10 (S13).

- **Session safety net** (`handoff_gap.py`, `.githooks/pre-push`): `AUDIT_session_safety_net.md`. Covers N target 3's "then `handoff_gap.py`".
- **Merge-gate guards** (`check_decisions_log.py`, `check_doc_citations.py`): `AUDIT_merge_gate_guards.md`. N target 3.
- **The planned PR-tier check** (TODO J, on hold): `AUDIT_pr_tier_check.md`.

## Never audited (candidates, roughly ranked)

Template targets, from TODO N (targets 1–2 done 2026-10-20):
- 3. Guards with no tests of their own (`check_decisions_log.py`, `check_doc_citations.py`, then the rest)
- 4. Do the docs agree? (`CHANGE_PIPELINE.md` / README / `CLAUDE.md` / skills; size)
- 5. Skills: `handoff`, `steward`, `project-audit`
- 6. Backlog and ledgers
