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
## Done

Closed items moved out of `## Open work` live in **`docs/TODO_archive.md`** — one line each below, reasoning there.

- [x] **C. Direction of flow: template → instances.** — DONE 2026-09-29 · `docs/TODO_archive.md`

- [x] **D. Align Claude web with Claude Code: a project spec sheet.** — DONE 2026-09-29 · `docs/TODO_archive.md`

- [x] **B. Outside research via Claude web.** — DONE 2026-09-29 · `docs/TODO_archive.md`
