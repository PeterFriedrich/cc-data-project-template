# cc-data-project-template

A GitHub template for a Python data-analysis project worked on with Claude Code.
It carries the **workflow apparatus** — the parts that stop a session from
losing context, shipping a wrong number silently, or stranding work — and
nothing about any particular dataset.

Extracted from a project where every piece below was earned by a failure it
now prevents. The theme running through all of it: **a working guard on a
channel nobody reads is not a guard.**

## What's in it

| Piece | What it prevents |
|---|---|
| `CLAUDE.md` skeleton | Sessions that start without the rules, or with rules Claude can derive itself |
| `/handoff` skill + `scripts/handoff_gap.py` (SessionStart/End hooks) | Context wiped without a written record — the hook **names the unrecorded commits** and is silent when nothing is owed |
| `.githooks/pre-push` | Pushing to a branch whose PR already merged (work reaches origin, never master) |
| `tests/test_loaded_path.py` | The handoff pile growing into every session's mandatory reading; the archive being deleted instead of appended to |
| `scripts/check_decisions_log.py` | A decision recorded with no test protecting it; a superseded row left looking current |
| `scripts/check_doc_citations.py` | A doc citation that rots in place (line numbers banned; `§N` pointers verified) |
| `tools/todo_archive.py` | Closed work accumulating in the file read first every session |
| `tools/retrieval_report.py` + Read/Grep/Glob hook | Pruning docs on a guess instead of a read log |
| `steward` skill (read by the cloud harness on PR events) | Hourly check-ins burning turns overnight while a green PR waits on the owner's merge |
| `scripts/make_brief.py` + `docs/SCOPE.md` + `docs/CLAUDE_WEB.md` | A Claude web chat briefed from a hand-typed, stale "my situation" block — the brief is generated from the repo's own ledgers and, when committed, gated fresh by `tests/test_brief.py` |
| `copier.yml` + `docs/COPIER.md` + `tests/test_copier.py` | Template improvements that never reach a project — `copier update` merges them in, keeping the project's own edits |
| `scripts/template_drift.py` (SessionStart hook) | A project that never learns the template moved on — the hook **names the changed files** and is silent when the project is current |
| `docs/WEB_CACHE_BUSTING.md` | A deploy that looks half-shipped because the browser kept a stale CSS/JS/data file |
| `/project-audit` skill + `docs/AUDIT_LEDGER.md` | Audits that sweep broadly, re-run what was already run, or never record their verdict |
| `scripts/check_requirements.py` | A venv rebuild silently dropping a package someone installed by hand |
| `docs/ASSUMPTIONS.md` + `scripts/check_assumptions.py` | Unproven premises scattered across five docs; a VERIFIED claim whose test is gone |
| `docs/DECISIONS.md`, `docs/DATA_ISSUES.md`, `docs/TOKEN_EFFICIENCY.md`, `data/DATA.md` | Format contracts for the ledgers the guards read |
| `.github/workflows/tests.yml` | A merge gate that is offline, secret-free, and therefore never ignored for flaking |

## How a change goes, and where each step stands

As of 2026-10-19. The steps an agent follows, in order, are in
`docs/CHANGE_PIPELINE.md`; this table says how far along each one is. **Change
both in the PR that changes a step.** *Enforced* means a hook, test or CI step
fails or speaks without being asked. *Habit* means a written rule that nothing
checks: it holds only while a session remembers it. *Per project* means the
template has no data to ship, so each project fills it in.

| Stage | Step | Mechanism | Status |
|---|---|---|---|
| **Before the PR** | Plan first for a new module, a schema change or a CI change; a spec before any code | `CLAUDE.md`, `CONTRIBUTING.md` | Habit |
| | A decision that protects a number gets a test, and its row cites it | `check_decisions_log.py` | Enforced (the test exists; not that it tests the decision) |
| | An unproven premise gets a row in `docs/ASSUMPTIONS.md` | `check_assumptions.py` | Format enforced; adding the row is habit; completeness is a per-project test |
| | Tests and guards run locally, output shown | `pytest`, the `scripts/check_*.py` | Habit (CI catches it anyway) |
| | A second agent reviews the diff: `/code-review` | — | **Trial** in `edmonton-tax-viz`; the gate is TODO J |
| | Lint and type checks | — | **Missing** |
| **On every PR** | CI: pytest plus four guards; `master` requires the `test` check | `tests.yml`, branch protection | Enforced |
| | Every third-party import is pinned | `check_requirements.py` | Enforced |
| | Doc citations resolve; no line numbers | `check_doc_citations.py` | Enforced |
| | The description opens with a `Code review:` line | — | Trial, with `/code-review` |
| | A PR touching a claude.ai-synced file says so first | `CLAUDE.md` | Habit |
| | Security review: `/security-review` | — | **Missing**; matters most for deploy workflows and secrets |
| **Merging** | The owner merges on green CI. No person or bot reads the diff | — | As is; `/code-review` is the trial above |
| | No push to a branch whose PR already merged | `.githooks/pre-push` | Enforced (fails open) |
| | Checks rerun on the latest `master` before merge (merge queue) | — | **Missing**; branches needn't be up to date, so CI on the `master` push catches a bad combination after the fact |
| | Work confirmed on `master` with `git merge-base --is-ancestor` | `CLAUDE.md` | Habit |
| **After the merge** | Template changes reach projects by `copier update` | `copier.yml`, `template_drift.py` | Enforced notice; the update is run by hand |
| | Publish, with a gate before it ships | per project | Per project (`edmonton-tax-viz`: weekly `refresh.yml`, gated by verified notebooks) |
| | Seen before the public build | per project | Per project (`edmonton-tax-viz`: the full build vs the public map) |
| | Watch and roll back | automated issues, `git revert` | Habit: issues are read only at session start; no on-call |
| | A defect in someone else's data is logged with whether the publisher was told | `DATA_ISSUES.md` | Habit |

Around the changes, per session:

| Step | Mechanism | Status |
|---|---|---|
| Session start: commits since the last handoff are named | `handoff_gap.py` (SessionStart hook) | Enforced |
| Session start: template changes not yet pulled are named | `template_drift.py` (SessionStart hook) | Enforced |
| Session start: open GitHub issues are read | `gh issue list` rule in `CLAUDE.md` | Habit; a hook is TODO H |
| Session start: `TODO.md` and the latest handoff are read | `CLAUDE.md` | Habit |
| Audit: one target per run, a ledger row after; indexed assumptions are known, not new findings | `project-audit` skill, `AUDIT_LEDGER.md` | On request only |
| Audit: the skill is scored against bugs already confirmed | — | Planned, TODO K |
| Session end: `/handoff` before `/clear`; the hook names what's owed | `handoff` skill, `handoff_gap.py` | Enforced notice; the handoff is habit |

## Use it

Copier creates the project; it is the first step, not something run later.

```bash
pipx install copier       # once per machine; or: python3 -m pip install --user copier (Python >= 3.9)
gh repo create <owner>/<new-project> --private --clone
cd <new-project>
copier copy --trust gh:<owner>/cc-data-project-template .
./bootstrap.sh            # hooks path, venv, first pytest, memory seed prompt
```

Later, to pull template improvements into the project, run from inside it, on
a clean branch:

```bash
copier update --trust --defaults
```

Not GitHub's "Use this template": that copies this repo's own backlog and
handoffs, and leaves nothing for `copier update` to pull template changes
through later. Updating, and connecting a project made before copier:
`docs/COPIER.md`.

Then, in order:

1. Fill every `<placeholder>` in `CLAUDE.md`, `TODO.md`, `data/DATA.md`.
2. Write `docs/SPEC_phase1.md` before any code (`CONTRIBUTING.md`).
3. Keep `requirements-ci.txt` to what the merge gate needs.
4. Delete this section of the README and describe the project.

## What is deliberately NOT here

- Any dataset, downloader, pipeline stage or rendering code.
- A scheduled data-refresh workflow or a deploy workflow — add them when there
  is data to refresh and a site to deploy, each with its own pytest step.
- A plugin/marketplace packaging of `.claude/`. Cloud sessions don't install
  plugins a repo declares, so copier carries everything instead
  (`docs/FINDINGS_harvest.md` §"C (sync direction): recommendation").
