# FINDINGS — harvest from the active repos (2026-09-29, S02)

**Question:** what apparatus has been built or fixed in the active repos since the
template was extracted (2026-09-18) that the template should carry? And, from the
repos *made from* the template, what did each one change right away, since that
points to a gap in the template?

**Sources read** (the active list in `server-ops/gdocs/backups/1A_project_list.md`):

| Repo | Role | How read |
|---|---|---|
| `edmonton-tax-viz` @ `ef592a2` | source (370 commits since 2026-09-17) | `CLAUDE.md` diff; every template-owned file diffed; apparatus commits since extraction; heads of the meta-docs (`FINDINGS_guard_*`, `STALENESS_LEDGER`, `VERIFICATION`, `STACK`, the findings register) |
| `physics_sim`, `chemistry_sim` | ports to a JS project (no Python pipeline) | template-owned files diffed; `CLAUDE.md` additions |
| `PeterFriedrich.github.io` | port to an Astro site | template-owned files diffed; `CLAUDE.md` additions |
| `alberta-regional-viz` (09-18), `edmonton-permit-speed` (09-25) | made from the template | byte-compared against the template, to measure drift |

**Status: every candidate below is PROPOSED.** None is ported. Each one needs the
owner's yes or no, and each yes becomes its own `TODO.md` item.

---

## Tier 1: generic, already measured in a source repo, small to port

| # | Candidate | Evidence | Port |
|---|---|---|---|
| 1 | **The template ships its own guard scripts untested.** Its only test is `tests/test_loaded_path.py`. Edmonton tests every one of the same scripts: `test_handoff_gap`, `test_check_decisions_log`, `test_check_doc_citations`, `test_todo_archive`, `test_retrieval_report`, `test_ci_workflows`. | `ls tests/` in both repos. Every instance inherits scripts that nothing checks. | Port the generic tests and strip the edmonton fixtures from them. `test_ci_workflows` pins the merge gate's *membership* (`FINDINGS_proxy_guards.md` F3: pytest once ran only on a weekly cron). |
| 2 | **The retrieval log can't see a doc read through Bash.** The template's hook matches only `Read\|Grep\|Glob`. | edmonton `4971a80`: "8 tracked docs consulted through Bash, 0 logged". A prune decided on "never opened" would target the docs that are actually in use. | Add the Bash `PostToolUse` matcher. Port the report's two-regime caveat (`BASH_HOOK_SINCE`) and `test_retrieval_report.py`. |
| 3 | **The handoff skill should end with a "safe to /clear" verdict.** The owner runs `/handoff` *instead of* `/clear`, and no hook can gate `/clear`. | edmonton `576f16e`: land the handoff on master, prove it with `merge-base --is-ancestor`, then end on exactly one ✅/❌ line. | About 13 lines in `.claude/skills/handoff/SKILL.md`. |
| 4 | **A findings register in `AUDIT_LEDGER.md`:** one row per finding, tagged by class, public reach, how it was found, and status. | edmonton `26648fb`: 137 findings from 54 audits. **`guard-blind` is the top class (32)** and `claim` is next (30, of which 9 reached the public site). Before it existed, patterns were recalled, not counted. | Add the section, the class table, and a Step 5 line in `project-audit`. |
| 5 | **Two template scripts assume Python and `master`.** Both JS ports had to fork `.githooks/pre-push` (`master` → `main`) and `check_decisions_log.py` (`tests/test_*.py` → `*.test.js`). They also had to rewrite `test_loaded_path.py` as `loaded-path.test.js`. | Diffs in physics_sim and chemistry_sim, identical in both. | Detect the default branch (`git symbolic-ref refs/remotes/origin/HEAD`). Move the test-ID globs to one constant at the top of the script. Once those fork points are gone, candidate C's drift check can compare the files byte for byte. |
| 6 | **Give `CLAUDE.md` a `## Commands` / `## Verification` slot.** | Added independently by physics_sim, chemistry_sim and github.io: the commands CI runs, plus "look at the screenshot, 'no errors' is not 'looks right'". | One placeholder section. |
| 7 | **Sharper `CLAUDE.md` rules from edmonton:** (a) **`SessionStart` is the hook that reaches a session**, because it fires after `/clear` and after compaction; `SessionEnd` fires too late to act on, and `PreCompact` can't carry a message. (b) **A green digest still gets closed**, since a list that always shows a stale ✅ is how the next ❌ gets skimmed past. (c) In a remote VM, **if the budget may run out, stop, write the handoff, commit and push.** | edmonton `CLAUDE.md` Session Management; `FINDINGS_guard_burst.md` §2a. | Wording edits in `CLAUDE.md` and `docs/REMOTE_VM.md`. |

## Tier 2: generic but conditional (a doc or an opt-in, not a default)

| # | Candidate | When it pays | Evidence |
|---|---|---|---|
| 8 | **A third audit family, (c) Guard audit**, with three questions: *does it fire on the defect? can its trigger occur in this repo? does anyone read the output?* Right now the skill has only (a) decision and (b) correctness. | Once a repo has more than a few guards. | `guard-blind` is the top class in #4. `FINDINGS_vacuous_guards.md` V1: a rate-copy check passed because the number appeared in a *code comment* while the public blurb showed a retired rate. `FINDINGS_guard_channels.md`: Q2/Q3. |
| 9 | **A brief overrides the skill.** A `docs/*_AUDIT_*.md` brief wins over the audit skill's default steps, and a brief whose session executes nothing adds no ledger row. | When audits are delegated to another model or session. | edmonton-audit §"Before Step 1"; the `FABLE_AUDIT_*` → `FINDINGS_*` pairs. |
| 10 | **An evidence recheck:** a scheduled re-run of notebooks whose invariants are *meant to keep passing*. "Could not check" is reported separately and louder, and a failure may be good news (the publisher fixed the defect). | When `DATA_ISSUES.md` rows have published evidence. | edmonton `c3ebb67`: evidence three weeks stale looked a day old after a cosmetic re-render. |
| 11 | **Record audit progress off the loaded path** (`STALENESS_LEDGER.md`), and never write a dated tag into the item being measured. | When `TODO.md` is large. | A sample of 15 items untouched for 60+ days found **7 stale (47%)**. A dated tag moved items out of their own cohort mid-pass. Worth a rule in `TOKEN_EFFICIENCY.md` even without the file. |
| 12 | **A symbol map for one large file:** `tools/codemap.py` plus a `PostToolUse` hook that regenerates it on edit. | Any file over a few thousand lines. | edmonton S79: scanning `web/index.html` (~7,300 lines) was the main context cost. |
| 13 | **`docs/STACK.md`**, with a section on what the project deliberately does NOT use. | Once dependencies exist. | Answers "should we add X?" before anyone proposes it. |
| 14 | **Lock reader-facing wording:** a `COPY_DECISIONS.md` for wording decisions plus a README-claims test. | Projects that publish copy. | edmonton `test_readme_claims.py`: the README headline asserted the one framing the project had rejected three times. |
| 15 | **A heartbeat for scheduled Actions** (`generate_status.py`). GitHub disables a cron workflow after 60 days of repo inactivity. | The first time a scheduled workflow is added. Belongs in README's "deliberately NOT here" note. | edmonton `generate_status.py` docstring. |

## Declined: specific to one project

`CONTROLS_MATRIX`, `TRANSITIONS`, `MOBILE_USABILITY`, `PERFORMANCE`, `UI`,
`VIZ_STACK`, the `SPEC_*` files, edmonton's domain `check_*.py` family,
`DATA_INTEGRITY.md` (its content is specific to edmonton, and its shape as a
brief for a model is covered by #9), and `PROJECT_AUDIT.md` (a point-in-time
snapshot).

## Drift observations (input to TODO item C)

- **The two repos made from the template are byte-identical to it**, apart from
  `alberta-regional-viz`, which is **missing the 2026-09-24 additions**: rule 8
  in `TOKEN_EFFICIENCY.md` and the steward skill, because it was created on
  09-18. `edmonton-permit-speed` (09-25) got them. Nothing tells a repo that the
  template moved on.
- **Nothing flowed back either.** All three improvements in Tier 1 #2–#3 were
  made in edmonton after the extraction and stayed there. physics_sim and
  chemistry_sim copied the template's handoff skill byte for byte, so they miss
  the safe-to-clear verdict too.
- **Every repo rewrites "the owner" as "Peter"** in its comments, so owned files
  are never byte-identical even when their logic is. A drift check needs either
  instances that keep owned files verbatim, or a comparison that ignores this.
- The README's own trigger for plugin packaging ("the first time a workflow fix
  has to be hand-copied into a second project") **has already fired**: the
  steward skill and the cache doc were hand-copied into `edmonton-permit-speed`.

## What this run got wrong

- **It measured files, not behaviour.** "Byte-identical" and "missing" come from
  `cmp` and `ls`. I did not run any instance's hooks to confirm that they fire.
- **I read edmonton through headers and docstrings, not in full.** A candidate
  that lives only inside a long findings doc's body could be missed. The
  `REVIEW_doc_apparatus_2026-09-15*` set in `docs/external/` wasn't opened, and
  it is the outside review most likely to hold more candidates.
- **The ranking is my own judgement.** Tier 1 means it was measured and is cheap
  to port. It does not mean the owner already wants it.
