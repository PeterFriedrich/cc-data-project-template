# FINDINGS: are the README's "Enforced" claims true? (TODO N target 2)

Run 2026-10-20 (S10), template `master` at `a9896e2`. A correctness audit:
each mechanism the README's pipeline tables mark *Enforced*, plus the
mechanisms in its "What it guards against" table, was **broken on purpose in a
scratch clone** to see whether it fails or speaks where someone reads it.
Project evidence is read-only, from the local clones (tax-viz `master`
`32fecec`) and GitHub. Ledger row: `docs/AUDIT_LEDGER.md`, 2026-10-20.

"Fires where someone reads it" here means: a CI step exits non-zero, which
reds the PR; a git hook exits non-zero inside `git push`, whose output the
session reads; a SessionStart hook prints `additionalContext`, which reaches
the model, and `systemMessage`, which reaches the owner.

## Verdicts

| Claim (README row) | Probe | Verdict |
|---|---|---|
| CI: pytest plus five guards; `master` requires `test` | each guard broken; `gh api …/branches/master/protection` on 8 repos | **WARN**: template true; 3 of 4 public projects unprotected |
| Every third-party import is pinned (`check_requirements.py`) | committed `import requests` | **PASS**, exit 7 |
| Doc citations resolve; no line numbers (`check_doc_citations.py`) | `line N`, `:N`, `§N`, `§"title"`, `"title"`, missing doc | **FAIL**: line numbers pass the check; "resolve" holds only for bare `§N` and handoff paths |
| A decision that protects a number gets a test (`check_decisions_log.py`) | new row with no test; new row citing a test that doesn't exist | **PASS**, exit 6 both |
| Unproven premise rows: format (`check_assumptions.py`) | status `PROBABLY` | **PASS**, exit 8 |
| (one of the five) fit table (`check_fit_table.py`) | a conflict marker | **PASS**, exit 9 |
| No push to a branch whose PR merged (`.githooks/pre-push`) | `git push --dry-run` of PR #62's branch plus 1 commit | **WARN**: fires through git; misses a push of a branch that isn't checked out |
| …and `handoff_gap.py` says when `core.hooksPath` isn't set | hooksPath unset | **PASS**: notice in both JSON keys |
| Session start: commits since the last handoff are named (`handoff_gap.py`) | a commit after the newest handoff | **PASS**: names the commit; `systemMessage` + `additionalContext` |
| Session start: template changes not yet pulled are named (`template_drift.py`) | target 1 ran it in 5 projects; JSON keys checked here | **PASS** |
| Session end: the hook names what's owed | `--session-end` with a gap | **PASS** on the channel (stderr, the only SessionEnd surface per the script's cited hooks reference); whether the owner sees it under `/clear` is unverified, and the SessionStart run after `/clear` carries the same notice |
| Committed brief gated fresh (`tests/test_brief.py`, top table) | `--write`, commit, then a new TODO item | **PASS**: 7 passed → 1 failed |

## Audit: doc-citation guard

**Verdict:** FAIL

**Finding.** The line-number ban works, in both spellings (`line 12` and
"COPIER.md:12", exit 5), and so do bare `§N` and handoff paths. Everything
else is weaker than "Doc citations resolve":

1. **A `§N` after a closing backtick is never checked.** The section match is
   `re.match(r"\s*(?:§|sections?\s+)\s*(\d+…)", tail)`, and `tail` starts with
   the backtick of `` `docs/X.md` ``. The backtick form is how these docs write
   citations. `` `docs/COPIER.md` §9 `` (COPIER.md has no numbered sections)
   exits 0. The template has no `§N` citations, but civic-map has 35 in this
   form (all resolve), drive-landscape 2 (both resolve), and **tax-viz 625, of
   which 8 are dead**: two point at `DECISIONS.md` rows, and one,
   "DATA.md §470", is a line number written as a section.
2. **`§"title"` is never checked.** The title match is `[`\s]*"…"`, so a `§`
   before the quote skips it, with not even a warning. The template has 18 such
   citations, and each resolves by the guard's own rule (the title appears in
   the cited doc). tax-viz has 25, **17 dead**, all pointing at a
   `TODO_archive.md` section that exists nowhere.
3. **A plain `"title"` that's missing only warns**, by design ("quoted-title
   misses warn only").
4. **A cited doc that doesn't exist only warns**, unless it's a
   `session-summary/` path. The docstring says exit 5 covers "a citation names
   a missing doc". In the template every one of the 49 warnings is a doc a
   project creates later (`BRIEF.md`, `ARCHITECTURE.md`, `RUNBOOK.md`,
   `REVIEW.md`, `SPEC_*.md`). A project's real typo would be one more warning
   in a CI log that already holds 49 of them, which step 4.4 calls not
   detection. The summary line also calls all of them "quoted-title
   warning(s)".

tax-viz's copy has the same section and title regexes, so its CI was green
over 25 dead citations. Reported to `edmonton-tax-viz` 2026-10-20. Per
`edmonton-tax-viz`, the 17 aren't mis-citations: the section they cite was
deleted (see "Surfaced" below). With fix (2) below, CI would have gone red
on the day of the deletion.

**Fix.** Allow the backtick before `§` in the section match, and fail a
`§"title"` whose doc exists but doesn't contain the title (the `§` marks it as
a pointer; a plain `"title"` stays a warning). For missing docs: exempt the
docs a project creates later, by name, and fail the rest; or keep the warning
but stop shipping 49 of them. The guard has no test file of its own (target 3),
so the fix brings one. Rollout: tax-viz's 25 citations must be fixed before it
ports this, or its CI goes red; civic-map and drive have none dead.

## Audit: CI merge gate and branch protection

**Verdict:** WARN

**Finding.** Template: `tests.yml` runs pytest plus the five guards with no
`continue-on-error`. Each guard exits non-zero on its broken input (5, 6, 7, 8,
9), `master` requires `test`, and admin override is on by decision (DECISIONS
2026-10-15). The gate has fired: a PR went red on 2026-10-06 (`docs/s04-handoff`).

Projects:

| Repo | Visibility | `master` requires `test` |
|---|---|---|
| drive-landscape | public | yes, but `enforce_admins: true`, unlike the recipe |
| edmonton-tax-viz | public | yes (`test`, `url-state`) |
| alberta-regional-viz | public | **no protection** |
| edmonton-civic-map | public | **no protection** |
| edmonton-open-data-landscape | public | **no protection** |
| data-science-study, edmonton-permit-speed | private | not available on the free plan (exempt by decision) |

The decision of 2026-10-15 was written as a new-project recipe step, and
alberta (made 09-18), open-data-landscape (09-30) and civic-map (10-10) all
predate it. Nothing retrofitted them, and the row is `[unverifiable]`, though
`gh api` can check it. No harm yet: all 142 PRs merged in those three repos
have a passing `test` check (latest rollup).

**Fix.** The owner turns protection on for the three repos (the recipe's
`gh api -X PUT` in `docs/COPIER.md` §"New project"), and decides whether
drive's `enforce_admins: true` stays. A check could make the row verifiable:
a session-start notice when a public repo's `master` doesn't require `test`.
It would need the network, and fail open like `template_drift.py`.

## Audit: pre-push hook

**Verdict:** WARN

**Finding.** Through git (`git push --dry-run`) with `core.hooksPath` set, a
merged branch plus one new commit is blocked: exit 1, and the BLOCKED text is
in the push output. With hooksPath unset, the session-start notice says so.
But the hook decides from `git symbolic-ref HEAD`, not from the refs on its
stdin, so `git push origin docs/todo-n-step0` while another branch is checked
out goes through (the dry run printed `46ba405..982ab22`). Sessions usually
push from the branch, so this is a narrow gap.

**Fix.** Read each `<local ref> <local sha> <remote ref> <remote sha>` line
on stdin, and check the remote branch's PR and that sha's commits, not
`HEAD`'s.

## Surfaced: the archive's append-only rule has no CI guard

**Verdict:** FAIL (outside the README's "Enforced" rows, found through them)

**Finding.** tax-viz commit 7d6a728 (2026-09-24, "docs: close the verify
build-gate TODO item") cut `docs/TODO_archive.md` from 3,465 lines to 16
(checked: `git show 7d6a728^:docs/TODO_archive.md | wc -l`). It was found 26
days later, by this run's dead citations, and per `edmonton-tax-viz` it's
being restored from `7d6a728^`. The template's `tools/todo_archive.py`
refuses to shrink the archive ("REFUSING TO WRITE — the archive would
SHRINK"). But that check runs only when the tool runs, and a session that
rewrites the file by hand bypasses it. How 7d6a728 truncated the file is
unconfirmed. Only `tests/test_copier.py` names the archive, and it tests the
render, not the file. Across all eight repos' histories this is the only
commit that shrank the archive.

**Fix.** A guard on the merge path, either of: (a) every `## Done` stub's
title in `TODO.md` appears in `docs/TODO_archive.md`, which needs no base
ref and would have failed 7d6a728; (b) with `--base`, as
`check_fit_table.py` does, the archive's line count never drops. (a) also
catches a stub whose item was never archived.

## What this run got wrong

- **Two probes were wrong at first.** I put the unpinned import in an
  untracked file, and the guard reads `git ls-files`. I nearly reported a
  working guard as broken; it exits 7 once the file is committed. A probe has
  to look like what CI sees.
- **A heading-only check, reported as a broken citation.** I told the owner
  that one of the template's 19 `§"title"` citations, in my own target-1
  findings doc, was broken. I had checked headings only; the guard's rule is
  body text, and "Not a copier project" is in `docs/COPIER.md`'s body. By the
  guard's rule, 0 of the template's citations are dead. The count is also 18,
  not 19: my first pattern double-counted one.
- **A false positive in my own script.** My title script resolved
  `/home/opc/CLAUDE.md §"Other agents"` against this repo's `CLAUDE.md`.
  The guard resolves by basename the same way, so fixing (2) as proposed would
  flag it falsely: out-of-repo paths need skipping.
- **A commit hash I made up.** The first draft's header named `master` at
  `9a3ed41`, a SHA I never read. It's `a9896e2`, fixed before the PR.
- **Not measured:** whether `systemMessage` text is visible on screen after
  `/clear`. The hooks reference is cited, not tested.
