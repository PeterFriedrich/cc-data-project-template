# Findings: the planned user-level rules home

Run 2026-11-11 by `template-audit-rules` (Fable 5.1, own worktree), `project-audit`
decision family, on the brief `AUDIT_user_rules_home.md` (out of repo, in
`/home/opc/research/cc-data-project-template/audits/`). The target is a **plan**:
nothing is installed. Audited as of: the draft dated 2026-11-05, the live
`~/.claude/settings.json`, server-ops at `e7a4e40`, and the memory folders as they
stood today.

This repo is public, so rules are named by memory filename only and no rule text
is quoted. Proposed edits to the draft, with quotes, are in
`/home/opc/research/cc-data-project-template/user_rules_draft_audit_2026-11-11.md`.
Answers from `server` are marked "per `server`"; they are unverified unless a
file is named beside them.

## Verdicts

| Level | Question | Verdict |
|---|---|---|
| L0 | Should cross-project rules be centralised at all? | **CONDITIONAL**: sound for reach, not for drift; holds only if L3 is fixed or knowingly accepted, and new corrections get a path into the home |
| L1 | Is the core / skills split right? | **CONDITIONAL**: the core's own test is applied unevenly, 12 memories lose their always-loaded line, and no skill trigger has been tested |
| L2 | Is the draft faithful to the sources? | **CONDITIONAL**: the four merges are faithful; moving project-scoped text to every project changes what five memories mean |
| L3 | Safety and switchover | **UNSOUND as written**: neither control the plan names exists |

L3 is the lowest level, so nothing beneath it is mooted. It does decide the
order: the L3 fixes come before anything is installed.

## What was measured

| Fact | Value | How |
|---|---|---|
| Real memory folders (5 more are symlinks to a main clone's) | 20 | a scratch script over `~/.claude/projects/*/memory`, symlinks resolved |
| Filenames in two or more real folders / drifted | 27 / 4 | md5 per copy; matches the brief |
| Size, one copy of each | 65.8 KB | largest copy |
| Projects holding 26 of the 27 | 3 (`edmonton-tax-viz`, `edmonton-permit-speed`, `alberta-regional-viz`) | the 27th is in three other projects |
| Other live sessions on the box / of which hold the rules | 20 / 4 | `ListAgents`; the three projects plus one worktree |
| Draft core | 1,691 bytes, 11 rule lines + 2 dated decisions | the draft's fenced block |
| tax-viz index bytes for the 26 memories the draft moves or deletes | 6,265 of 10,415 | `MEMORY.md` lines by link target |
| Skill-housed memories with no core line | 12 of 21 | draft §2 against §3 |
| Sessions that opened a promoted memory's body | 7 of 61 transcripts since 2026-10-01 (three projects); 11 reads in 131 logged sessions since 2026-09-16 | transcripts; `~/.claude/retrieval-log.jsonl` |
| Proposed skill sizes, verbatim | `verification` 25.2 KB, `git-pr` 12.5 KB, `research-intake` 10.1 KB, `data-audit` 5.4 KB, `design-decisions` 5.4 KB | sum of bodies |
| Git checkouts under `/home/opc` / with another organisation's origin / with no pre-push hook file | 34 / 4 / 12 | `git remote get-url`, `.githooks/pre-push` |
| Deny rules on `~/.claude/**` | 0 | live settings = `security/claude-permissions.json` |
| Ask rules on the rule paths | 12, all `Edit(...)` or `Write(...)`, none for Bash | same |
| Pull requests ever opened in server-ops | 0 | `gh pr list --state all` |

## L0. Centralise at all? CONDITIONAL

**For.** The drift the plan cites has cost nothing so far: in all four drifted
files the newer copy is a superset of the older one (diffed), and no two copies
disagree. The real gap is reach. The rules sit in three projects because
`bootstrap.sh` copied them there once (copy dates 2026-09-18 and 2026-09-26); the
other 16 live sessions have none of them. A user-level file fixes that, and
per-project copies cannot.

**Sharpest argument against.** The plan moves prose from one always-loaded place
to another, and the sources themselves record that this does not work for the
rules that matter most. `verify-commits-reached-master` records the same failure
nine times with the rule written down, and says a hook stopped it. This repo
already holds that position (`docs/CHANGE_PIPELINE.md` step 1.8: prefer a guard or
hook). The plan contains no hook. A user-level hook in `~/.claude/settings.json`
would reach every session on the box, including the 12 checkouts with no
pre-push hook, and it is the one form of rule that does not depend on being read.

**Second argument.** The plan handles a snapshot, not a flow. Today a correction
becomes a memory in the same turn, with no prompt. After the move the home
changes only by a merged change in another repo, and a session's standing
instruction is still to write auto-memory. New cross-project corrections will
keep landing in one project's memory, and step 5 stops the seeding that at least
carried them to new projects. The four drifts were each a session appending an
incident to its local copy; that path closes and nothing replaces it.

**Would change the verdict.** To SOUND: a stated path for a new correction (who
proposes it, where, and how it reaches the home), and the L3 conditions. To
UNSOUND: evidence that the rules already reach unseeded projects some other way.
I found none, but did not measure how often the owner repeats a correction in an
unseeded project (see "Not checked").

## L1. The split. CONDITIONAL

**F1. The draft's test for a core line is "applies in every turn, in every
project", and four lines fail it while the draft keeps them.** The research-reply
line is one job and names a path that exists only on this box. The
reintroduce-the-bug line is one job (writing a check). The partner-names line
applies to public repos. The PR-state line applies where a PR is open. Three of
those four are right to keep, for a reason the draft does not state: the miss is
permanent or silent, and a skill may not load. The test should say so: a line is
core if it applies everywhere, **or** if missing it once cannot be undone. By
that test `terse-pr-bodies-for-editorial-changes` belongs in the core too (its
own text says the miss cannot be undone), and it has no core line.

**F2. Five of the 11 core rules already load in every copier project.** The
push line, the PR-state and reached-the-trunk line, the stale-backlog line, the
re-verify line and the falsify line restate this repo's `CLAUDE.md` skeleton and
`docs/CHANGE_PIPELINE.md` steps 1.2, 1.5, 1.6 and 2.1. The explainer line (draft
§5) restates step 1.1. For the 9 projects on this skeleton (8 by copier, plus tax-viz) they would load twice, in two
wordings. For the other checkouts they are new, which is the point of the core.
The core should carry them and the skeleton should then drop them (TODO R is the
place), or the core should leave them out; not both. The tone line also repeats
the `outputStyle` setting, which the source memory explains is deliberate.

**F3. Twelve memories lose their always-loaded line.** Today each memory has a
one-line hook in `MEMORY.md`, loaded every session. Under the draft, 12 of the 21
skill-housed memories have no core line and are reachable only if a skill loads:
all of `data-audit` (4) and `design-decisions` (3), plus
`commit-before-falsifying`, `same-length-sed-leaves-stale-pyc`,
`confirm-the-server-you-measure`, `pr-merge-method-merge-commit` and
`terse-pr-bodies-for-editorial-changes`. The draft counts the saved bytes
(about 4.5 KB in tax-viz) and not this change of mechanism.

**F4. The premise that the incidents must travel with the rule is not what
happens today.** The draft keeps every incident in the skill body because "the
incidents are the evidence a rule needs to be followed". In the 61 retained
transcripts of the three projects, a promoted memory's body was opened in 7
sessions, and several of those were edits to it. The working rule today is the
index line. A skill that loads 12 to 25 KB to deliver seven one-line rules is a
cost with no measured benefit. Proposed shape: `SKILL.md` holds the rules in a
few hundred bytes each, and the incidents sit in a reference file beside it,
opened when a rule is questioned.

**F5. No trigger has been tested, and two descriptions cannot work as
written.** `verification` is meant to load when "reporting a check result",
which is most turns of most sessions; a model will not call a skill that often,
so in practice the trigger is unknown. `git-pr` is meant to load on every commit
to a PR branch, the same problem. The box has no base rate to lean on: of the 62
`Skill` calls in 168 retained transcripts, 56 are to procedure skills someone
runs on purpose (review, handoff, audit, session launch) and 6 to tool skills
(charts, artifacts). None is a habit skill that must load itself. Test before deleting anything: for each skill, three
fresh sessions given the job in the owner's usual words, without naming the
skill; record whether it loaded.

**F6. `data-audit` belongs to this template, not to the user level.** Its four
memories only apply to data projects. `audit-decisions-top-down` is already
step 3(a) of this repo's `project-audit` skill, and the tax-viz memory
`guards-must-measure-data-not-metadata` (not in the draft) is already in its
appendix. Adding the other three to that appendix ships them by copier, reaches
cloud sessions, and avoids two skills answering one job.

**F7. The selection rule is a proxy.** The draft's scope is "filenames that
appear in more than one project". Duplication came from `bootstrap.sh` copying,
so it measures what was seeded, not what applies everywhere. It misses: one rule
held under two filenames (`claude-web-sync-paths` here,
`claude-web-sync-give-paths` in `drive-landscape`; both are now a skeleton line
and can go); owner preferences recorded once outside the three seeded projects
(`send-prompts-via-senduserfile`, `search-what-owner-names`,
`read-session-summary-means-handoff`); and box facts held only by tax-viz that
every project on this machine hits (`oracle-box-stale-ca-bundle`,
`ugrep-rejects-complex-patterns`, `pgrep-watchers-match-themselves`,
`oracle-box-has-no-web-fonts`, the timing half of `run-verify-scripts-alone`).
The box facts are `server`'s, for `/home/opc/CLAUDE.md`.

**F8. The core has an append-only list.** "User decisions (dated)" has no cap
and no rule for what earns a row. It is the part of the core most likely to grow
back into the index it replaces. One of its two rows repeats a core line.

**Sharpest argument against L1.** The split optimises bytes loaded, and the
evidence (F4) says bytes were never loaded; what the split actually changes is
which rules keep a guaranteed line, and it removes that from 12.
**Would change the verdict:** trigger trials (F5) showing each skill loads on
its job at a rate the owner accepts.

## L2. Faithful to the sources? CONDITIONAL

**Draft §1 passes.** All four merges are right as proposed: each newer copy
only adds. `commit-before-falsifying` is the one case where the newest copy is
alberta's and not tax-viz's. The draft's count (27, 4) and
its per-file descriptions match the files.

**F9. The push line widens a standing authorisation.**
`push-proactively-all-envs` names one project. The skeleton extends it to copier
projects. The core line extends it to every checkout on the box, including four
whose origin belongs to another organisation and server-ops, where a push to
`main` is a deploy. That may be what the owner wants. It is a new decision, and
the draft presents it as a restatement.

**F10. The reached-the-trunk line is wrong under a squash merge.** The core
line gives the ancestor test without the caveat that
`pr-merge-method-merge-commit` and `verify-commits-reached-master` both carry
(under squash the original commit never lands). The owner's merges do come out
as squash (this repo's `docs/DECISIONS.md`, 2026-10-19 and TODO H). As written
the line reports stranded work that is not stranded.

**F11. Verbatim text carries one project's permissions to every project.**
The `git-pr` bodies include a tax-viz allowance to put docs commits straight on
the default branch, and instructions for merging a PR oneself.
`merge-docs-only-myself` is correctly kept per project in draft §4, but
`pr-merge-method-merge-commit` links to it and assumes it. This repo's
2026-11-04 decision is no self-merge yet. A session in another project would
read these as its own permissions.

**F12. "This project" changes meaning when the text moves.** The 21 bodies
hold 15 phrases of the form this repo / this project / this box, 33 repo paths
or PR numbers, and 7 links to memories outside the promoted set (one of which
exists nowhere). One body states a fact about what "this project"
authenticates to that is true of tax-viz and false of server-ops and
`drive-landscape`. "Verbatim" is the wrong rule for a move across projects:
each body needs its project named where it says "this".

**F13. Three smaller losses.** (a) `reverify-after-the-last-edit` has a
second rule (check the run after a merge) that the core line drops and that the
`verification` trigger will not reach. (b) `prompt-handoff-clear-at-boundaries`
has two cues and a caution; the core keeps one cue. (c) The draft trims
`verify-relayed-external-advice` to "the five strongest" incidents. The file
records seven instances in at least four distinct classes and one
counter-instance that narrowed the rule. Trim by class, one incident each, and
keep the counter-instance, or the rule reverts to its earlier, wrong form.

**Draft §4, checked.** `run-verify-scripts-alone`: neither other project has
those scripts, so deleting their copies is right, except the timing half (F7).
`merge-docs-only-myself`: tax-viz and permit-speed both record it in their own
`CHANGE_PIPELINE.md` fit table, as the draft says. `disk-scratch-discipline`:
covered by `/home/opc/CLAUDE.md`; its three copies are in projects the draft
does not name. `direct-tone-no-claude-isms` and `push-proactively-all-envs`:
covered, subject to F9.

**Sharpest argument against L2.** The draft checks that no words were lost and
not that the words still mean the same thing in a project they were not written
in. **Would change the verdict:** F9 to F12 answered in the draft.

## L3. Safety and switchover. UNSOUND as written

The plan names two controls. Neither exists.

**F14. "Denies on `~/.claude/**` for project sessions" (draft §6 step 2) was
not applied.** The live settings have no such deny (confirmed by `server`, and
by `security/HARDENING.md` 2026-11-05). What exists is 12 ask rules on the Edit
and Write tools for six paths. Checked against each write path:

| Write path | Covered by a rule? |
|---|---|
| Edit / Write tool on the core, `skills/`, `commands/`, `plugins/`, `settings.json` | yes, ask |
| Bash: `cp`, `mv`, `sed -i`, `tee`, a redirect, `python -c`, `git` writing into those paths | no rule; in auto mode the classifier decides |
| The same, in tax-viz | its local settings allow its venv's `python -c`, which skips the classifier (`.claude/settings.local.json`; also F6 of `server`'s 2026-11-10 audit) |
| A symlink from `~/.claude/skills/<x>` into a working tree | the target is outside every rule |
| Each project's `MEMORY.md` and memory folder | none, by decision; loads every session with the same standing as the core |
| `~/.claude/skills/synced/` | written by the harness's own sync, outside any PR |

Per `server`, a Bash write was tested once, from its own session, and the
classifier blocked it; it has not been tested from a project session. I did not
test it either (see "Not checked").

**F15. "Installed from merged main only" is not a control, because every
session can write `main`.** server-ops is private on a plan where GitHub refuses
branch protection (403, checked). It has never had a PR. A daily cron pushes
whatever `HEAD` is. Its scripts run from the working tree, which no rule
protects. Every session uses the owner's one GitHub login, so even on a
protected public repo a session can merge as the owner; protection on this repo,
tax-viz and alberta has admin enforcement off and requires no review (checked).
Per `server`: the source folder, the install mechanism and who runs it are all
"not decided", and only a separate credential for sessions fixes this.

**F16. A planted line would pass review.** The owner merges within minutes;
this repo's 2026-11-04 decision row counts 94 merged PRs in about two weeks. A change to a 25 KB
skill body is the kind of diff that gets merged unread. Short rule files (F4)
are also the safety fix: a planted imperative is visible in a 1 KB file.

**F17. The plan protects one file while files of equal standing stay open.**
A line planted in a project's `MEMORY.md` has the same per-turn authority as
the core in that project, and reaches the sibling session where the folder is
symlinked. The draft states no precedence between the core, a project's
`CLAUDE.md` and its memory. At least one project memory
(`branch-and-pr-workflow`) forbids what a `git-pr` body permits (F11).

**F18. Switchover: two versions will coexist, with no end date.** Step 4 has
each project session delete its own copies "in the same window". Six sessions
must each act, none can act for another, and nothing checks that they did. A
session that does not act keeps the old copies beside the new skills; for the
alberta copies that means the older text of three drifted files. Running
sessions keep their loaded index and do not have the core until restarted. The
index lines must be removed with the files, which the draft does not say. The
deleted files have no backup (auto-memory is in no repo), so a loss in the merge
could not be repaired after step 4.

**F19. The approved design is recorded in no file.** Per `server` it exists
only in a message to `template`, summarised in the draft's header. server-ops'
TODO, DECISIONS and latest handoff (2026-10-30) do not mention it. The draft is
therefore the only record, and it is wrong on step 2 (F14).

**Sharpest argument against L3.** The honest baseline is that
`/home/opc/CLAUDE.md` and the user-level hooks already reach every session with
exactly this protection, so the core adds a third such target and not a new
class of risk. That is an argument for accepting the risk knowingly. It is not
what the plan says: the plan says the write path is closed.

**Would change the verdict.** To CONDITIONAL: the owner accepts, in a file,
that the core has classifier-level protection only; or sessions get a credential
that cannot write the rules repo's `main`. Either way: the install is a copy of
`origin/main` blobs (never a symlink), it prints the diff against what is
installed, and a check lists stale copies after the switchover.

## Order proposed

1. Record the design and its real protection level in server-ops (F19, F14).
2. Decide F9, F11 and the precedence line (F17); these are the owner's.
3. Rewrite the skills as short rules plus a reference file (F4, F12, F16); move
   `data-audit` to this template (F6); settle the doubled lines (F2).
4. Run the trigger trials (F5). A skill that does not load keeps core lines.
5. Copy the memory folders somewhere outside `~/.claude`, install, then delete
   copies and index lines, then run the stale-copy check (F18).
6. Add the hook for the rule that failed nine times as prose (L0), if the owner
   wants it at user level.

## Not checked

- **A Bash write into `~/.claude` from a project session.** This run was told
  not to edit `~/.claude`, so F14's Bash rows rest on the rule list, `server`'s
  one test and its 2026-11-10 audit.
- **Whether skills trigger.** No trial was run (F5 is a proposal).
- **How often the owner repeats a correction** in a project that was never
  seeded. That number decides L0 and is in no file I found.
- **Cloud and laptop sessions.** Neither reads this box's `~/.claude`. Per
  `server`: laptop deferred, cloud not decided.
- **Which of two skills with one name wins** (user-level against a project's
  own). A project can create its own skill folder with no prompt.

## What this run got wrong

- **My first inventory reported 50 duplicated filenames, not 27.** It counted
  the five memory folders that are symlinks to a main clone's folder as copies.
  That is the class under audit (duplication measured by filename) in my own
  instrument. The fixed script resolves symlinks first.
- **My first count returned zero memory files in every project.** The folder
  names begin with a dash, and `ls` and `cat` read them as options. A zero that
  clean should have been distrusted at once; it was, but only because the
  number contradicted the brief.
- **"Bodies are rarely opened" (F4) is a negative, and my first evidence could
  not see one reader.** The retrieval log records tool calls, and the harness
  can place a recalled memory in context with no tool call. I then searched the
  transcripts for any line carrying a promoted filename: it appears as the
  loaded index in 50 sessions and in a tool call in 7, with no third kind. The
  transcripts only go back to 2026-10-01, so the claim holds for six weeks, not
  for the life of the memories.
- **A session count printed 1 for 131 sessions** because I read the wrong key
  from the log. It did not reach a finding.
- **I counted `Skill` calls "the user named" with a crude text match** and
  dropped that split from F5 because I could not stand behind it. F5 uses only
  which skills were called.
- **F2's "five of 11" is my reading of which lines restate the skeleton.** The
  proposed-edits file lists the pairs so the owner can disagree line by line.
