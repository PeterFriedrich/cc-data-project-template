# TODO

The source of truth for what's left. Read first every session; update in place.

**Format contract** (`tools/todo_archive.py` depends on it): top-level items are
`- [ ]` / `- [x]` lines directly under `## Open work`; `###` sub-headings may
group them; closed items are moved to `docs/TODO_archive.md` by the tool, which
leaves a one-line stub under `## Done`. An open item can be stale — reproduce the
symptom and re-measure the stated cause before acting on it.

## Open work

### Template improvement (opened 2026-09-29)

- [ ] **A. Harvest from active repos.** Read `edmonton-tax-viz` (main source), `physics_sim`/`chemistry_sim`, `PeterFriedrich.github.io` for apparatus that postdates the extraction; read `alberta-regional-viz`/`edmonton-permit-speed` for *drift* (what a fresh instance had to customise at once = template gap). Output: a ranked candidate list, each tagged generic vs project-specific, in `docs/FINDINGS_harvest.md`. Done when the owner has approved/declined each candidate; porting is follow-up items.
- [ ] **E. Onboard instances to copier.** (opened 2026-09-29, S03; restored 2026-09-30 — it was glued onto item C's line by an edit and archived with it.) `alberta-regional-viz`: **connected** (its PR #1, `_commit: 9ded929`, SCOPE.md + BRIEF.md on master); the #14 update was handed to an alberta session 2026-09-30. `edmonton-permit-speed`: not started — same procedure (`docs/COPIER.md` §"Connect a project made before copier"; find its base commit first, it was made 2026-09-25). Done when both are on master at the template's current `_commit`.
- [ ] **F. Parallel sessions on one repo.** (opened 2026-10-02 at the owner's request, via `server`.) **Revisit after the `edmonton-tax-viz` trial** that started 2026-10-02 (a second session, `edmonton-tax-viz-report`, in a git worktree on branch `report-desk`). Its working rules are the "Parallel sessions" section of tax-viz's `CLAUDE.md` (its PR #641); the worktree convention, with `.venv`, `data/raw` and auto-memory symlinked to the main clone, is in `/home/opc/CLAUDE.md` §"Other agents". Known breakage in the template apparatus (checked 2026-10-02 against tax-viz's copies): (1) **handoff names collide**: each session takes the next `sNNN` from its own branch, so a per-session suffix (e.g. `-report`) is needed; (2) **`scripts/handoff_gap.py` misfires after a cross-merge**: the newest handoff by name may be the other session's, giving false positives (its commits) and false negatives (a reset baseline), and `SUBSTANTIVE` skips `notebooks/`; (3) **`.githooks/pre-push` blocks a long-lived branch** once its first PR merges, so use a fresh branch per PR. Possible shapes: a `bootstrap.sh` worktree mode, a "Parallel sessions" slot in the `CLAUDE.md` skeleton, session-aware handoff naming and `handoff_gap.py`. Done when the trial's outcome is known and each shape is ported or declined.
- [ ] **G. Harness recommendations from the 2026-10-12 research (via `edmonton-tax-viz`).** Sources, outside any repo: `/home/opc/research/claude-code/harness_*_2026-10-12.md`. Taken for the template, each a small doc or skeleton edit for the owner to OK: (1) `docs/TOKEN_EFFICIENCY.md` says always-loaded context is measured in **bytes, not lines**. Today the template `CLAUDE.md` is 57 lines / 7.7 KB, plus 6.3 KB from `/home/opc/CLAUDE.md`, and no guard counts lines. Measure a byte budget before writing a guard for it. (2) A **removal pass**: trial `/doctor prompt-audit` (2.1.283+) on the template's `CLAUDE.md` and skills, record what it flags, and only then decide on a recurring pass. (4)+(5) `CLAUDE.md` skeleton, Code Style: each guard gets a fixture with one thing deliberately wrong that it must reject, and a test's expected values come from an independent source, never from running the code (arXiv 2610.11835). Declined: (6) cross-model review. There's no cross-model reviewer in the workflow, the evidence is single-author preprints with planted errors, and 2603.12123 was revised. Item (3) is H. Done when each taken edit is merged or declined by the owner.
- [ ] **H. Open GitHub issues in the SessionStart message.** (opened 2026-10-12, via `edmonton-tax-viz`; built in the **template**, not as a second fork of tax-viz's `handoff_gap.py`.) Automated checks file issues that only email the owner, and the `gh issue list` rule in `CLAUDE.md` depends on a session remembering it. **Plan first** (it changes hook behaviour): a separate script, not `handoff_gap.py`; `gh issue list --state open --limit 20` with a short timeout, or a cached list; fail silent like `template_drift.py`; say nothing when there are no open issues. Done when merged and pulled by one instance.
- [ ] **I. A `REVIEW.md` for data projects.** (opened 2026-10-18, owner, from Anthropic's "Solving code review" post: https://claude.dev/blog/solving-code-review-at-anthropic/.) The post has code owners write a `REVIEW.md` saying what failure looks like in the repo, capping nits, listing paths to skip, and asking for a file and line as evidence. For a data project failure is "a published number is silently wrong". Check first what `/code-review` actually reads in this Claude Code version. Done when a skeleton is merged or the owner declines it.

## Done

Closed items moved out of `## Open work` live in **`docs/TODO_archive.md`** — one line each below, reasoning there.

- [x] **C. Direction of flow: template → instances.** — DONE 2026-09-29 · `docs/TODO_archive.md`

- [x] **D. Align Claude web with Claude Code: a project spec sheet.** — DONE 2026-09-29 · `docs/TODO_archive.md`

- [x] **B. Outside research via Claude web.** — DONE 2026-09-29 · `docs/TODO_archive.md`
