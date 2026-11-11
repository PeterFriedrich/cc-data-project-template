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
| 2026-11-11 | Template N target 3: the two merge-gate guards with no tests of their own (`check_decisions_log.py`, `check_doc_citations.py`) | `project-audit`; brief `AUDIT_merge_gate_guards.md` (out of repo); 127 inputs through each guard's `check()`; the template, tax-viz, alberta and permit-speed measured read-only; each guard gutted in a scratch clone; CI history | `docs/FINDINGS_merge_gate_guards.md` | Decisions log: L0 CONDITIONAL (a write-time question; 13 of 21 template rows are tagged), L1 test rule CONDITIONAL (an unparseable date skips it), supersession rule UNSOUND (22 wordings pass; 4 candidate rows in tax-viz), L2 and L3 CONDITIONAL. Doc citations: L0 CONDITIONAL (the section check ran on 0 of 733 citations in three repos), L1 UNSOUND (one citation hides the next; `.github/` never scanned; string literals skipped), L2 CONDITIONAL (its one red CI run was a false alarm), L3 CONDITIONAL. No test notices either guard gutted. Nothing wrong found in the four repos' live citations | TODO W (fixes, with P1 and T1); F8, F9 → owner; tax-viz items → `edmonton-tax-viz` via `template` |
| 2026-11-11 | The session safety net: `scripts/handoff_gap.py` with its SessionStart and SessionEnd hooks, and `.githooks/pre-push` (covers the `handoff_gap.py` part of N target 3) | `project-audit`; brief `AUDIT_session_safety_net.md` (out of repo); 51 runs of the script and 18 pushes through the hook in scratch clones with a stand-in `gh`; 10 mutations against the tests; the 17 other copies, 187 transcripts and the hooks reference read | `docs/FINDINGS_session_safety_net.md` | L0 CONDITIONAL (silent with no handoff yet, with an uncommitted file in `session-summary/`, for work off `HEAD` or unpushed, and in a depth-1 clone; the session-end notice may reach nobody, unverified). L1 UNSOUND as a default (a seven-path include-list; 0 of 8 copier projects changed it; civic-map's `site/` and the template's own product are outside it). L2 CONDITIONAL (sound on this server; reported not to run in a cloud VM; a `gh` error looks like "no PR"). L3 CONDITIONAL. 7 of 10 mutations pass the suite, deleting the hook among them. No lost work found in 18 repos | TODO X (fixes, with P3 and T2); the session-end channel check and F4 → owner; other repos' items → their sessions via `template` |

## Queued — briefed, not yet run

Briefs live out of repo, in `/home/opc/research/cc-data-project-template/audits/` (a `docs/AUDIT_*.md` here would ship to every project through copier). Each runs in its own fresh session (Fable 5.1, own worktree), queued 2026-11-10 (S13).

- **The planned PR-tier check** (TODO J, on hold): `AUDIT_pr_tier_check.md`.

## Never audited (candidates, roughly ranked)

Template targets, from TODO N (targets 1–2 done 2026-10-20; the two merge-gate guards and `handoff_gap.py` of target 3 done 2026-11-11):
- 3. The rest of the guards with no tests of their own: `template_drift.py`, `todo_archive.py`, `retrieval_report.py`
- 4. Do the docs agree? (`CHANGE_PIPELINE.md` / README / `CLAUDE.md` / skills; size)
- 5. Skills: `handoff`, `steward`, `project-audit`
- 6. Backlog and ledgers
