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

## Done

Closed items moved out of `## Open work` live in **`docs/TODO_archive.md`** — one line each below, reasoning there.

- [x] **C. Direction of flow: template → instances.** — DONE 2026-09-29 · `docs/TODO_archive.md`

- [x] **D. Align Claude web with Claude Code: a project spec sheet.** — DONE 2026-09-29 · `docs/TODO_archive.md`

- [x] **B. Outside research via Claude web.** — DONE 2026-09-29 · `docs/TODO_archive.md`
