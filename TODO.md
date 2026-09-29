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
- [ ] **B. Outside research via Claude web.** Write a research prompt (public Claude Code starter repos, `CLAUDE.md`/skill/hook conventions) that excludes what the 2026-09-18 report in `research/cc-data-project-template/` already covered; save it there. **Prompt written 2026-09-29:** `research/cc-data-project-template/template_improvement_research_prompt_2026-09-29.md` (out of repo) — waiting on the owner to send it to Claude web; its Q3 feeds item C. Done when the prompt is saved and the reply is triaged into candidates.
- [ ] **C. Direction of flow: template → instances.** Proposal: template is canonical; a manifest of template-owned files + a drift-check script lets each instance see which owned files are behind and pull on purpose (instances diverge — e.g. edmonton's `edmonton-audit` replaced `project-audit` — so blind copies clobber). Note the README's own trigger for plugin packaging ("the first time a workflow fix has to be hand-copied into a second project") has already fired: the steward skill was hand-copied into `edmonton-permit-speed`. **Needs owner sign-off (new module).**
- [ ] **D. Align Claude web with Claude Code: a project spec sheet.** Claude web sees only what is pasted, so every research prompt re-writes a "my situation" block and a "don't recommend back" list by hand (both 2026-09 prompts did). They go stale, and replies come back as prose that has to be hand-translated into repo items. Idea: one maintained spec sheet per project (what it is, stack, locked decisions, out of scope), ideally **generated** from `CLAUDE.md` + `DECISIONS.md` so it can't drift, plus a reply format that maps onto `TODO.md`/`DECISIONS.md` rows. Research question 5 in the TODO B prompt covers prior art (llms.txt, claude.ai Projects/GitHub sync, MCP). Done when the owner picks a shape from that reply and the template carries it.

## Done
