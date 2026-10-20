# FINDINGS: does the template reach its projects? (TODO N target 1)

Run 2026-10-20 (S10), template `master` at `2f0685c`. A decision audit,
top-down. Evidence comes from each project's GitHub `master` (shallow clones in
the session scratchpad, read-only), its git history and `gh` data, then
answers from four project sessions, marked "per `<session>`". Ledger row:
`docs/AUDIT_LEDGER.md`, 2026-10-20.

## Scope

The data projects in `/home/opc/CLAUDE.md`'s table that the template is meant
to serve: `alberta-regional-viz`, `data-science-study`, `drive-landscape`,
`edmonton-civic-map`, `edmonton-open-data-landscape`, `edmonton-permit-speed`,
and `edmonton-tax-viz`, which is hand-ported by decision. `ai-safety` has no
template files and isn't listed as made from the template, so it's out of
scope.

## Decision stack

| Level | Question | Verdict |
|---|---|---|
| L0 | Should one template push its changes into every project at all? | SOUND |
| L1 | Is every data project connected to the channel? | CONDITIONAL |
| L2 | Do updates land faithfully, and what has each project forked? | CONDITIONAL |
| L3 | Does a session learn that the template moved? | SOUND (one quirk) |
| L4 | Is the distribution code right? | not audited here (target 3) |

### L0: one template, pushed to projects. SOUND

Across the five copier projects, **162 of 184** shipped files are
byte-identical to the template at each project's own `_commit`. Every other
difference is project content in a slot the template leaves for it
(`requirements*.txt`, `.gitignore`, `CLAUDE.md`'s project lines, the fit
table, `DATA_ISSUES` rows), except the two forks in L2. `data-science-study`
differs in **0 of 35**. The apparatus is generic, so pushing it beats every
project keeping its own copy.

- *Sharpest counter:* projects are variants, and every update costs a
  session's time plus conflicts (the fit table, `tests.yml`, alberta's
  synced-path list).
- *What would change it:* forks that grow beyond the slots, or update cost
  that rises faster than what updates deliver.

### L1: is every project connected? CONDITIONAL

5 of 7 data projects are on copier.

- **`edmonton-permit-speed`: never connected.** It has no
  `.copier-answers.yml`, and 15 of the template's 47 shipped files are
  absent, including `CHANGE_PIPELINE.md`, `template_drift.py` and
  `make_brief.py`. It was created 2026-09-26 with `gh repo create --template`,
  three days before copier was adopted. Per `edmonton-permit-speed`, there's
  no blocker and no session ever picked up the step. It has hand-ported one
  change, template #31, as its PR #5. TODO E has been open since 2026-09-29.
- **`edmonton-tax-viz`: hand-ported by decision** (DECISIONS 2026-09-29,
  `docs/COPIER.md` §"Not a copier project").
  - 16 of the 47 shipped files are absent; most are deliberate variants (its
    `edmonton-audit` skill instead of `project-audit`).
  - Its `CHANGE_PIPELINE.md` header records the port: "master `5b48600`,
    2026-10-19".
  - Every template pipeline rule since then is missing there: the `Risk:` /
    `Tested: … not covered` / `Undo:` lines, `Cause: … missed by`, step 4.5,
    step 1.7's "fix the class", the explainer offer. All of them came from
    PRs #44–#59; `5b48600` is template #41 and had none of them (checked). tax-viz PRs
    #760–#764 carry none of the lines.
  - Per `edmonton-tax-viz`, a port is triggered "almost always" by a message
    from the `template` session, sometimes by the owner, and never by a
    tax-viz session noticing. The project whose evidence shaped those PRs
    gets them only when the template pushes them there.
- **The route that created permit-speed is still open.** The template is
  public with `is_template: true`. GitHub's "Use this template" copies 14 of
  the repo's own state files, including `docs/DECISIONS.md` with its 16
  rows, the handoffs and `TODO.md`. Four docs say not to use the button
  (`README.md`, `docs/COPIER.md`, `docs/DECISIONS.md`, `/home/opc/CLAUDE.md`),
  but the button is a rule with nothing enforcing it, and one repo setting
  removes it. Per `edmonton-permit-speed`, its S01 found and deleted a leaked
  copy of the template's S01 handoff (2026-09-25), which is exactly this route.
- *Sharpest counter:* 5 of 7 is fine for a solo owner, and the two gaps are
  known (TODO E; the tax-viz decision).
- *What would change it:* permit-speed connected, and a tax-viz trigger that
  doesn't depend on the template remembering to push.

### L2: do updates land faithfully? CONDITIONAL

How often, from GitHub's history of each `.copier-answers.yml`:

| Project | `_commit` | Template date | Updates | Last update | Merges behind (shipping) | Shipped files changed since |
|---|---|---|---|---|---|---|
| alberta-regional-viz | `e79c7b1` | 2026-10-15 | 7 after connect | 2026-10-16 | 27 (21) | 16 |
| data-science-study | `bbc82eb` | 2026-10-15 | 1 after start | 2026-10-16 | 31 (24) | 19 |
| drive-landscape | `538c23c` | 2026-10-15 | 4 after start | 2026-10-16 | 28 (21) | 16 |
| edmonton-civic-map | `5b48600` | 2026-10-19 | 5 after start | 2026-10-19 | 21 (16) | 11 |
| edmonton-open-data-landscape | `bbc82eb` | 2026-10-15 | 2 after start | 2026-10-16 | 31 (24) | 19 |

The last round was pulled 0–1 days after the template commit. The lag since
then is a deliberate hold: per S09, there's one update per project once the
blog-post walk is done.

Fidelity:

- **`_commit` is a claim, not proof that the update landed.** Replaying
  alberta's first update (bf5f568 → 9ded929) in a scratch clone, copier
  delivered `docs/SCOPE.md`, the `copier` pin in `requirements-ci.txt` and a
  `requirements.txt` conflict. Alberta's commit 06a32d6 took none of the
  three. `SCOPE.md` arrived later by alberta's PR #1, and the pin never did:
  per `alberta-regional-viz`, the file has had one commit, its initial one.
  That particular drop was harmless (see F6), but nothing would notice a
  harmful one. The drift notice compares `_commit`, not content.
- **alberta's synced-path fork: intended, and costly at each update.** Its
  `handoff/SKILL.md` sync-check command, `docs/CLAUDE_WEB.md` synced-file list and
  `CLAUDE.md` add `docs/SCOPE_candidates.md` to the claude.ai synced set. Per
  `alberta-regional-viz`, this is deliberate; the `data/DATA.md` half was
  upstreamed as template #16. It conflicted on 3022d3d and e455544, and has to
  be hand-resolved each time the template edits that list. The template gives
  a project no place to add synced paths without editing three template files.
- **civic-map's `tests.yml`: extra steps, conflict-prone.** Its site build and
  browser checks live in the template's `test` job. Per `edmonton-civic-map`,
  pulling 5b48600 conflicted (one hunk, about 2 minutes), and then again on a
  rebase. A bad resolution would silently drop a site step, and no guard
  checks that particular steps exist. Its "Check the built site" step was
  duplicated by its own #70 and fixed in its #72 after this run reported it.
- *Sharpest counter:* the conflicts are rare and cheap, two minutes.
- *What would change it:* a fork scan run after each update that comes back
  clean, and extension points for synced paths and CI steps.

### L3: does a session learn the template moved? SOUND, with one quirk

- `scripts/template_drift.py` ran in each of the five clones. Each printed the
  notice with the correct compare link, and each project's
  `.claude/settings.json` wires it to SessionStart. `core.hooksPath` is set in
  all five local clones.
- **Quirk:** each project runs its own copy of the script, so its `IGNORED`
  list is one update stale. Alberta's notice lists `docs/ASSUMPTIONS.md`,
  which `_skip_if_exists` means no update changes. That's only noise. The
  missed case, where the template stops ignoring a path, would be silent, but
  hasn't happened.

## Findings → actions

| # | Finding | Verdict | Action |
|---|---|---|---|
| F1 | GitHub "Use this template" is live on a public repo and copies 14 own-state files | WARN | The owner turns off Settings → "Template repository" (`gh api -X PATCH repos/PeterFriedrich/cc-data-project-template -F is_template=false`). It's a repo setting, so it's the owner's call. |
| F2 | permit-speed isn't connected; no blocker | CONDITIONAL | TODO E, done in the `copier update` round |
| F3 | tax-viz gets template changes only when the template pushes them | CONDITIONAL | TODO O: per-file "ported from `<commit>`" markers, plus a notice that names only template commits touching those files, silent otherwise (per `edmonton-tax-viz`). It's a hook change: plan first, owner's call. |
| F4 | `_commit` advances even when a hunk is dropped | WARN | TODO O: after each update, diff shipped files against the template at the new `_commit`; every difference is a slot or a recorded fork (the method below) |
| F5 | No project-owned place for extra synced paths or CI steps; both conflict at each update | WARN | TODO O: an extension point for each, scoped with alberta and civic-map |
| F6 | `requirements-ci.txt` ships `copier==9.18.2` to projects, but only the template's own `tests/test_copier.py` (not shipped) imports it | WARN (minor) | TODO O: split the template-only pin out |
| F7 | `project-audit` tells the auditor to write `docs/AUDIT_<target>.md`, and in the template that file would ship to every project (the step-0 class again). This run put its method here instead. | WARN | TODO O: exclude template briefs without excluding `AUDIT_LEDGER.md`'s skeleton, or point the skill at `FINDINGS_*` for the template |

## Method (re-run)

Run from the template root, with each project's `master` shallow-cloned to
`$S/repos/<project>` (`git clone --depth 1`); local clones can have stale
`origin/master`, as civic-map's did in this run.

1. **Connected?** `.copier-answers.yml` `_commit` from GitHub
   (`gh api repos/<r>/contents/.copier-answers.yml`).
2. **How far behind?** First-parent merges in `<_commit>..origin/master`,
   counting the ones whose diff touches a path where
   `template_drift.reaches_project()` is true.
3. **What forked?** For each file shipped at `_commit` (skipping `.jinja`
   ledgers, `_skip_if_exists` files and the answers file), compare
   `git show <_commit>:<f>` with the project's copy: identical, modified
   (count the +/− lines) or missing. For hand-ported projects, compare
   against template HEAD instead.
4. **Does the notice fire?** Run `python3.12 scripts/template_drift.py` inside
   each clone.
5. **Ask** only what files can't show: why something forked, what triggers a
   port, what a conflict cost.

## What this run got wrong

- **A confident negative, wrong.** I told `edmonton-tax-viz` that nothing
  recorded which template commit it had ported from. Its
  `CHANGE_PIPELINE.md` header does. I also gave it the range as #47–#60; it's
  #42–#62, and the missing rules came from #44–#59. My grep searched for phrasings I'd guessed
  ("ported up to", "template commit") instead of reading the ported file's
  header. The session corrected it.
- **Mis-framed a drop as a fork.** The fork scan reported alberta's
  `requirements-ci.txt` as "drops the copier pin" (a local edit). In fact
  the update delivered the pin and the session's commit never took it. A scan
  against `_commit` can't tell a deletion apart from a hunk that was never
  committed; only a replay can.
- **Stale refs.** My first pass at update history read local `origin/master`,
  which showed civic-map at `e79c7b1`; GitHub has `5b48600`. I re-read
  everything from GitHub.
- **An unmeasured claim, said aloud.** Mid-run I told the owner every project
  pulled "within about 1–3 days" of a template change. I had only measured
  the last round (0–1 days).
- **Limit:** the fork scan applies today's `IGNORED` and `_skip_if_exists`
  lists to older commits. That's harmless for these five `_commit`s, but not
  in general.
