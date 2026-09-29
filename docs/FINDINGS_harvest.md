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

## Research round (TODO B): triage of the Claude web reply

**Source:** `research/cc-data-project-template/template_improvement_reply_2026-09-29.md`,
kept outside the repo, answering `…_research_prompt_2026-09-29.md`.

**Spot-checked 2026-09-29 before building on it:**
- Every cited GitHub issue and PR exists and says what the reply says:
  `anthropics/claude-code` #87497, #97096 and #98050;
  `akaszubski/autonomous-dev` #1727; `wasaybuilds/proof-of-done` #9;
  `serpro69/claude-toolbox` (149★).
- The load-bearing claim is **confirmed on the live docs**. In the carry-over
  table of `code.claude.com/docs/en/cloud-environments`, "Plugins and
  marketplaces declared in your repo's `.claude/settings.json`" reads **No**,
  while repo hooks, `.claude/skills/` and `CLAUDE.md` read Yes. Hooks apply only
  "in a session with one repository".
- #87497 is **closed as NOT_PLANNED by the stale bot**. It was not fixed.
- **Not checked:** the arXiv IDs, `/team-onboarding`, and copier's
  `_skip_if_exists` behaviour on update (the reply quotes copier's docs for it).
- **The reply missed one thing** that is on the same docs page: "Cloud sessions
  automatically load skills you enable on claude.ai". That is a route for
  skills only, not for hooks.

### New candidates

| # | Candidate | Source label | My read |
|---|---|---|---|
| R1 | **Pinned subject counts.** Every guard asserts `== <measured n>` subjects, never `>= 1`, and a falsification run asserts the mutant was actually applied. | B, measured (#1727) | **Adopt.** It hits the top finding class directly, and it is the concrete form of Tier 2 #8. Cheap to do in the template's own guards once #1 (tests) exists. |
| R2 | **A Stop-hook gate**: re-run the fast guards when Claude says it's done, and exit 2 so any failure goes back to Claude. | A for the mechanism; no measurement | **Adopt, scoped.** Run the guard scripts only, not the full suite (edmonton has ~875 tests). Needs a `stop_hook_active` loop cap. It moves guard output onto a channel the agent has to read. |
| R3 | **A protected-path PreToolUse hook** on tests and guards. | A (a recipe, copied everywhere) | **Adapt, don't adopt.** A blanket *deny* collides with this template's own rule that a decision is "a test first", so sessions write and edit tests all the time. Use `ask` on *existing* guard files, or R4, instead. It must match `Bash` too, or `sed -i` walks straight past it. |
| R4 | **Test-tamper detection at Stop**: diff the tests against a baseline taken at session start, and flag deleted or weakened assertions. | B (one repo) | **Prefer this over R3.** It flags weakening without blocking legitimate test-writing. Medium effort. |
| R5 | **Deny `--no-verify`** for Claude. | B (one report) | **Adapt to `ask`.** `CLAUDE.md` names `git push --no-verify` as the documented escape hatch, so a deny would contradict it. |
| R6 | **A guard heartbeat ledger**: each guard writes `{guard, subjects_checked, verdict}`, and a meta-test fails on a missing or stale entry. | The reply's own inference | **Hold** until R1 lands. Much of it overlaps R1 plus the SessionStart hook. |
| R7 | **Mutation testing** (mutmut, pinned version) scoped to the guard scripts, on demand or weekly, never as a merge gate. | B (one detailed report) | **Later.** It needs #1 first, since you can't mutation-test scripts that have no tests. It fits the audit skill as one guard module per run. |
| R8 | **One guard config file** (`guards.toml`: `test_glob`, `default_branch`), with detection as the fallback and a pinned-count check on the glob. | Inference, consistent with 3 repos | **Adopt.** It supersedes Tier 1 #5's "one constant at the top". The pinned count catches a Python glob left in a JS repo, which would otherwise check zero tests and pass. |

### C (sync direction): recommendation

The reply recommends **copier for everything that lives in the repo**, a plugin
later and only for CLI-only extras, and **backflow by diffing an instance
against a template render at its recorded `_commit`.** Given the confirmed docs
row, I agree with the direction, with three amendments:

1. **edmonton-tax-viz should not become a copier instance.** Its owned files
   are deliberately edmonton-specific (e.g. `edmonton-audit` in place of
   `project-audit`), so every `copier update` would conflict. It stays a
   *source*, and backflow from it is the backport diff only.
2. **Onboard one instance first.** The candidate is `edmonton-permit-speed`,
   which is byte-identical to the template today, so the first `copier copy`
   reconciles nothing. Add the others only if that goes cleanly. The six-at-once
   plan in the reply is the expensive version.
3. **An `owner_name` answer fixes the cosmetic drift**, which was the
   observation that made a hand-rolled byte-compare drift check unworkable.

Copier is a new dependency and changes how every instance gets updated, so it
**needs the owner's sign-off** (CLAUDE.md: propose first).

### D (spec sheet): recommendation

The reply proposes a generated `BRIEF.md`, a CI gate that fails whenever it is
stale, a private claude.ai Project synced through the GitHub integration, and an
`ingest_reply.py`. It says itself that none of that loop is published practice.
**I'd take the smallest slice:**

1. **`make_brief.py`, run on demand, printing to stdout.** No committed file,
   so nothing can go stale and no CI gate is needed. The only hand-kept part is a
   short `SCOPE.md` ("out of scope / don't recommend back"), which has to exist
   anyway.
2. **A required output block at the end of every research prompt**: fenced
   tables whose columns match `TODO.md` / `DECISIONS.md` rows. This costs
   nothing, and this round already half-did it.
3. **Defer** the committed `BRIEF.md` with its CI gate, the GitHub-integration
   sync (#98050 is *open*: private repos 404), and `ingest_reply.py`. The last
   is an abstraction with one call site so far; revisit it after three rounds.

## What this run got wrong

- **It measured files, not behaviour.** "Byte-identical" and "missing" come from
  `cmp` and `ls`. I did not run any instance's hooks to confirm that they fire.
- **I read edmonton through headers and docstrings, not in full.** A candidate
  that lives only inside a long findings doc's body could be missed. The
  `REVIEW_doc_apparatus_2026-09-15*` set in `docs/external/` wasn't opened, and
  it is the outside review most likely to hold more candidates.
- **The triage verdicts are my own judgement too.** In particular, R3 and R5
  depart from the reply because of this template's own rules, and a reader who
  weighs agent tampering more heavily could reasonably reverse them.
- **The ranking is my own judgement.** Tier 1 means it was measured and is cheap
  to port. It does not mean the owner already wants it.
