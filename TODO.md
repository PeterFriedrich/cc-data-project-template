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
- [ ] **C. Direction of flow: template → instances.** Proposal: template is canonical; a manifest of template-owned files + a drift-check script lets each instance see which owned files are behind and pull on purpose (instances diverge — e.g. edmonton's `edmonton-audit` replaced `project-audit` — so blind copies clobber). Note the README's own trigger for plugin packaging ("the first time a workflow fix has to be hand-copied into a second project") has already fired: the steward skill was hand-copied into `edmonton-permit-speed`. **Research reply recommends copier** (confirmed: cloud sessions don't install repo-declared plugins); my amended version is in `docs/FINDINGS_harvest.md` §C. **Needs owner sign-off (new dependency).**
## Done

Closed items moved out of `## Open work` live in **`docs/TODO_archive.md`** — one line each below, reasoning there.

- [x] **D. Align Claude web with Claude Code: a project spec sheet.** — DONE 2026-09-29 · `docs/TODO_archive.md`

- [x] **B. Outside research via Claude web.** — DONE 2026-09-29 · `docs/TODO_archive.md`
