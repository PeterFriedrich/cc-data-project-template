# Findings: the session safety net (`handoff_gap.py`, `.githooks/pre-push`)

Run 2026-11-11 by `template-audit-safety` (`claude-fable-5-2`, own worktree),
`project-audit` on the session-safety-net brief (out of repo, in
`/home/opc/research/cc-data-project-template/audits/`). Targets:
`scripts/handoff_gap.py` with its two hooks in `.claude/settings.json`, and
`.githooks/pre-push`, template `master` at `9d8fe7a`. Ledger row:
`docs/AUDIT_LEDGER.md`, 2026-11-11. Covers the `handoff_gap.py` part of TODO N
target 3.

Method: each behaviour broken on purpose in scratch clones, never the working
tree. 51 runs of `handoff_gap.py`, 18 pushes through the real hook against a
bare scratch origin with a stand-in `gh`, and 10 mutations run against the test
suite. The appendix lists every run. Other repos were read only: 17 carry a
copy of `handoff_gap.py` and 15 a copy of the hook. Each was read at its local
`origin` trunk ref, without a fetch; three of those refs were two commits
behind the remote, corrected below (see "What this run got wrong"). The hooks
reference was
fetched from `code.claude.com/docs/en/hooks` the same day; Claude Code here is
2.1.322, `gh` 2.103.2.

Nothing is fixed in this PR. Fixes are TODO X.

## Verdicts

| Level | Verdict | In one line |
|---|---|---|
| L0. Is "silence means nothing is owed" the right contract? | **CONDITIONAL** | True only once a handoff is committed, nothing uncommitted sits in `session-summary/`, and the work is on `HEAD`. Six tested states are "could not check" and look the same as "nothing owed" (F1–F5). The session-end half may reach nobody (F6, unverified). Silence never means "pushed". |
| L1. Does `SUBSTANTIVE` cover what counts as work? | **UNSOUND** as a default | It is a list of seven paths, so every other folder fails silent. 0 of 8 copier projects changed it. civic-map's app (`site/`) and data-science-study's whole product (`studies/`) are outside it; in the template 16 of 95 commits can fire it (F7). |
| L2. Does fail-open let the exact failure through? | **CONDITIONAL** | Sound on this server (`gh` installed and logged in, hooks on in all 15 repos). Reported not to run in a cloud VM, the one place the docs say it matters most (F8). A `gh` error looks the same as "no PR" (F9). |
| L3. Code | **CONDITIONAL** | A git failure prints a false "hooks are off" (F14). Handoff names are sorted as text (F15). Small items in F16. |
| Tests | | 7 of 10 mutations pass the suite, including deleting the hook and unwiring both Claude hooks (F17). |

L1 is unsound for `handoff_gap.py` only. `pre-push` is a separate mechanism, so
L2 was still run. The L3 items for `gap()` matter less if L1 is redesigned.

## What was measured

Trunk commits since `handoff_gap.py` arrived in each repo, merges excluded,
classified with that repo's own `SUBSTANTIVE`. "Other" is a commit that touches
neither a listed path nor only `docs/`, `TODO.md` and handoffs. It is an upper
bound on missed work: it includes README and `CLAUDE.md` edits and bot commits.

| Repo (how it got the script) | Commits | Can fire | Docs only | Other | What "other" touches |
|---|---|---|---|---|---|
| template | 95 | 16 | 51 | 28 | `README.md` 19, `.claude/` 6, `CLAUDE.md` 6, `bootstrap.sh` 2, `copier.yml` 1 |
| edmonton-tax-viz (hand-port) | 486 | 187 | 253 | 46 | `notebooks/` 13, `CLAUDE.md` 10, `data/` 8, `.claude/` 7 |
| alberta-regional-viz (copier) | 92 | 34 | 33 | 25 | `data/` 15 (`.md` files), `CLAUDE.md` 8, `notebooks/` 3 |
| edmonton-civic-map (copier) | 89 | 25 | 31 | 33 | `data/` 16, `prototype/` 10, `site/` 9 (2 by the refresh bot) |
| drive-landscape (copier) | 62 | 31 | 24 | 7 | `CLAUDE.md` 5, `data/` 2 |
| edmonton-open-data-landscape (copier) | 53 | 14 | 29 | 10 | `data/` 7 (5 are weekly snapshots) |
| edmonton-permit-speed (copier) | 16 | 5 | 4 | 7 | `data/` 5, `CLAUDE.md` 4 |
| data-science-study (copier) | 6 | 0 | 2 | 4 | `studies/` 3 |
| chemistry_sim, physics_sim, math-stats, transition-sim (hand-ports, own list) | 119 | 79 | 36 | 4 | `README.md`, `CLAUDE.md` |
| PeterFriedrich.github.io (hand-port, own list) | 6 | 1 | 4 | 1 | `README.md` |
| landing_page (hand-port, own list) | 2 | 0 | 0 | 2 | `wp-content/` 1, `CLAUDE.md` 1 |
| regenx_app_refactor (hand-port, own list) | 2 | 0 | 1 | 1 | `CLAUDE.md` |

edmonton-nonprofit-map and recommendation-algorithms-explained hold one commit
each, so they have no row. server-ops counts everything except `docs/`,
`TODO.md` and handoffs, so nothing is "other" there by construction.

What sessions were actually told, from the 187 transcripts on this box
(2026-10-01 to 2026-11-11):

| | Count |
|---|---|
| SessionStart hook results recorded | 72 |
| …that carried a handoff-gap notice | 17, in 15 sessions across 8 projects |
| SessionEnd hook results recorded | 0 |

So the session-start channel works and is used. Of the 15 notices whose
handoff name I could parse, only one handoff is named twice (civic-map, a
resumed session), which reads as notices being acted on, not skimmed.

## Already known: is the status right?

- **The hook reads `HEAD`, not the pushed refs (TODO P3).** Right, and wider
  than written. See F10: two more ways through, and three wrong blocks.
- **`master` is hardcoded (TODO T2).** Right. T2 should say what it costs: on a
  `main` repo the unedited hook blocks nothing (run P5). No repo is exposed
  today: all 6 `main` repos with a hook carry an edited copy. server-ops's
  copy of `handoff_gap.py` still asks for `origin/master` on a `main` repo, so
  its branch reminder can never fire.
- **`.githooks` in `SUBSTANTIVE` breaks a hooks test (TODO T note).** Right.
  The cost of leaving it out: a commit that changes the hook itself is not
  named (run B4).
- **The 2026-10-20 run passed the hook except for P3.** Still true for what it
  ran: one push through git with the real `gh`. Its "Session end: PASS on the
  channel" should read unverified. It took the channel from the script's
  docstring, and the docstring cites the wrong row of the reference (F6).
- **TODO F's three breakages** (handoff names collide, a cross-merge misfires,
  a long-lived branch is blocked): not re-run.

## L0. Is silence true?

The docstring's contract is narrower than the README's. The docstring says
silence means "no code has moved since it was last committed". The README says
the hook "is silent when nothing is owed". The states below are silent, and in
each the script did not check.

| State | Silent? | Is silence true? |
|---|---|---|
| A handoff committed, no work since | yes | True. |
| No origin (A9); detached `HEAD` (A7); a worktree (B2a–c) | reports normally | True. The docstring says a detached `HEAD` exits silent. It doesn't, and shouldn't. |
| No handoff yet (F1) | yes | False. |
| An uncommitted `.md` in `session-summary/` (F2) | yes | False. |
| Work on another local branch; work committed, never pushed (F4) | yes | False for "nothing can be lost". |
| Shallow clone, depth 1 (F5) | yes | False. |
| git missing or failing (A10) | yes for the gap | Can't check; by design. |

**F1. A project is unguarded until its first handoff is committed.** A fresh
copier project ships `session-summary/` with a `.gitkeep`. With no `.md` there
`gap()` returns before looking at anything: two commits and a dirty file in
`src/` produce nothing (A1, A2). Live: edmonton-nonprofit-map and
recommendation-algorithms-explained have no handoff (one commit each, so
nothing is owed yet).

**F2. An uncommitted `.md` in `session-summary/` turns the whole check off.**
The script takes the last file by name, asks git when it was last committed,
and stops if the answer is empty. So a freshly written handoff that isn't
committed yet silences two owed commits, and a file changed after it (A3, A3b).
A stray `notes.md` does the same (A4). tax-viz pins the handoff case as
intended (`test_uncommitted_handoff_is_silent`: "the comparison has no
footing"). The template has neither that test nor a decision row. The argument
against: a footing exists, the newest *committed* handoff, and "a handoff is
written but not committed" is the state a session-end check exists to name.
The `handoff` skill writes the file and never says to commit it.

**F3. The baseline moves without a handoff being written.** A tracked
`README.md` in `session-summary/` sorts after every dated name and becomes "the
handoff" for good: the commit before it is never named (A5). A one-character
edit to the newest handoff resets the baseline the same way (A6).

**F4. Nothing in the net looks at whether work is pushed.** `gap()` compares
against `HEAD` only. Two commits on another local branch, unpushed and
unmerged, are silent from `master` (A8). Work and its handoff committed on a
local branch and never pushed are silent at session end (U1). The hook guards a
push that happens, not one that doesn't. Survey of 18 repos today: 5 commits
exist on no remote. Four of them landed on the trunk as an equal patch (`git
cherry`), and the fifth was made today in server-ops. So nothing is lost now,
and nothing would say so if it were.

**F5. A depth-1 clone is silent; a deeper shallow clone under-counts.** With
three owed commits, depth 1 names none, depth 2 names one, depth 3 names two
(B1). Whether a cloud VM clones shallow is not recorded anywhere I found.

**F6. The session-end notice may reach nobody (unverified).** The script
writes the notice to stderr and exits 0, citing the reference's "Shows stderr
to user only". That phrase is in the reference's table of what happens on
**exit 2**. For exit 0 the reference says stderr goes to the debug log ("To
read it yourself … enable debug logging"). No test covers the channel: removing
the write passes the suite (M4). I could not settle it by experiment. The live
test (a scratch repo with marker hooks, ended by hand) was refused by this
session's permission mode, and I did not work around it. The transcripts hold
0 SessionEnd results against 72 for SessionStart, which fits but proves
nothing: transcripts may not record that event. The README row "Session end:
… the hook names what's owed" is marked "Enforced notice" on this basis. The
script takes about 60 ms in four repos, so the 1.5 s SessionEnd timeout is not
a factor.

## L1. What real work slips past `SUBSTANTIVE`

**F7. The list is an include-list, and no copier project has changed it.**
`docs/COPIER.md` tells a repo that hand-copies the script to edit the list.
Nothing tells a copier project to, and all 8 carry the default. A commit to any
of these is silent (B4): `notebooks/`, `data/`, `site/`, `app/`, `.claude/`,
`.githooks/`, `CLAUDE.md`, `copier.yml`, `requirements.txt`, `bootstrap.sh`,
`pyproject.toml`, `Dockerfile`.

- **A static site or web app.** civic-map's app is in `site/`, not `web/`: 7
  session commits there are invisible (the share link, the alpha banner,
  republished boundary data), with 10 more in `prototype/`.
- **A data project.** Mostly covered. `data/` commits are nearly all `.md` files.
  `notebooks/` is the gap (tax-viz 13, three of them to verified notebooks,
  which gate its weekly publish); TODO F already names it.
- **A project with no code.** data-science-study's product is `studies/`: 0 of
  6 commits can fire. It has a handoff on `master`; the check is silent there
  only because `studies/` is not in the list.
- **The template itself.** Its product is `docs/`, `.claude/`, `CLAUDE.md` and
  `copier.yml`. Since the newest handoff (2026-10-30) 12 commits landed over 12
  days, two audits among them, and the hook has said nothing.
- The hand-ports that set their own list are fine (the four sims: 4 of 119
  commits are "other", all README or `CLAUDE.md`). landing_page's list has
  `docker/`, `site/` and `public/` but not `wp-content/`, where one of its two
  commits went.

The sharpest argument: an include-list fails silent on every folder a project
adds, and a guard that is silent when wrong is what this template exists to
prevent. server-ops's copy inverts it (everything except `docs/`, `TODO.md`
and handoffs), which fails loud. What would change the verdict: evidence that
the docs-heavy projects would then be nagged after every commit, which is the
reason `docs/` was left out (tax-viz DECISIONS, 2026-09-16).

Since the run (same day): civic-map and data-science-study each opened a PR
that sets its own list (their PRs 82 and 6, both open). civic-map's adds a
case an exclude-list must handle: a path a bot writes. Its weekly refresh
commits to `site/public/data`, and counted as work that would report a handoff
owed after every Monday run. It drops the path with the pathspec
`:(exclude)site/public/data`. Skipping by author would not cover every
project: three of civic-map's four refresh commits are authored
`github-actions[bot]` (the two made after its move to `HEARTBEAT_TOKEN` among
them) and one carries the owner's name, as do all five of
open-data-landscape's weekly snapshot commits.

## L2. What fail-open lets through

The control works: on a branch whose PR is merged, one new commit is blocked
(P0), and re-pushing what is already merged passes (P0b). An open or closed PR
passes (P14).

**F8. In a cloud VM the hook is reported to do nothing.**
PeterFriedrich.github.io's `docs/REMOTE_VM.md` records that `gh` is not
installed there, "so the hook exits early and guards nothing here". The
template's `docs/REMOTE_VM.md` says the hook "matters MOST here" and does not
mention it. With `gh` off the PATH the push of a stranded commit goes through
with no output (P1). Per that repo's doc; I could not run a cloud VM.

**F9. A `gh` error is indistinguishable from "no PR".** Rate limit, expired
login and network failure all exit non-zero, and the hook exits 0 without a
word (P2). Failing open is the decision and stands. Saying one line on stderr
when `gh` exists but failed would cost nothing. `gh` had 4,991 of 5,000
GraphQL points left when checked, with every session on the box sharing one
login.

**F10. The `HEAD` check: two more ways through, three wrong blocks.** Same
root as P3. Through: a push from a detached `HEAD` (P4), and a local branch
pushed to a differently named merged branch (P10). Wrongly blocked while
`HEAD` sits on a merged branch with one local commit: deleting another remote
branch, pushing a tag, pushing `master` (P12a–c). The hook's comment says it
never guards a branch delete; no line does that.

**F11. After a squash merge the hook blocks a push with nothing new.** It
counts commits by ancestry, so every commit of a squash-merged branch counts as
unmerged (P6a: "2 commit(s)" with nothing new). With a real new commit the
block is right, but the count and the printed `cherry-pick` list include the
merged commits (P6b). Squash is rare here but present: the four local-only
commits in F4 each landed as an equal patch and not as an ancestor (a squash,
a rebase or a cherry-pick), in four repos.

**F12. A hook that lost its executable bit is skipped, and the reminder is
silent.** git prints a hint and pushes (P7). `hooks_reminder` checks that the
file exists, not that it can run. All 15 copies are executable today; a
hand-port written fresh would not be.

**Branch name reused; two PRs from one branch.** `gh pr view <branch>` picked
the newer of two merged PRs on one branch (tax-viz `feat/transit-lens`: 38
over 36). The case that matters, an open PR on a branch with an older merged
one, has not happened in tax-viz's 797 PRs (796 merged, 1 open, 0 closed), so
it stays untested.

## L3. Code

**F14. A git failure reads as "hooks are off".** `hooks_reminder` treats a
failed `git config` like an unset value. With git off the PATH the session
start prints "The repo's git hooks are off … Run `git config core.hooksPath
.githooks`" (A10). Any git failure does it, a 15-second timeout included.

**F15. "Newest" is the last name as text.** No date is parsed, so no timezone
bug exists. But `-` sorts before `.` and `_`, and `S10` before `S8`: a second
handoff on one day can sort before the first (B3a–c). tax-viz's history has
three such pairs (`s100` before `s99`, `-s230-report` before `-s230`). The
direction is safe: the notice repeats and names the wrong file.

**F16. Smaller.**
- A new folder of five untracked files counts as "1 uncommitted file" (A12).
- A merge commit that itself edits `scripts/` is not named (A11).
- Under Python 3.6 with a C locale the plain mode ends in a traceback. The two
  hook modes are fine.
- An absolute `core.hooksPath` pointing at the main clone makes a worktree say
  hooks are off while the hook runs (B2d). No repo is set up that way.
- The hook has no timeout on `gh`: a 20-second `gh` is a 20-second push (P13).
- Read, not run: a failed `git status` counts as zero dirty files, and the
  branch reminder counts by ancestry, so squash-merged branches never count.

**F17. Tests.** The template's test file covers the two reminders; its header
says the handoff-gap half "is not ported here yet" (tax-viz has 28 tests, the
template 12). The hook has no test.

| Mutation | Suite |
|---|---|
| M1 `gap()` always returns None | 1 failed |
| M3 `SUBSTANTIVE` cut to `docs` | 1 failed |
| M5 session start prints plain text | 3 failed |
| M2 uncommitted work never counted | passes |
| M4 session end writes nothing | passes |
| M6 the oldest handoff is taken as newest | passes |
| M7 merges counted | passes |
| M8 the hook exits 0 on its first line | passes |
| M9 the hook deleted | passes |
| M10 both hooks removed from `.claude/settings.json` | passes |

## The copies in other repos

Read only. Drift is listed only where it changes behaviour.

| Copy | Differs from the template in behaviour |
|---|---|
| alberta, open-data-landscape, permit-speed, nonprofit-map, recommendation (copier) | No. Identical. |
| civic-map, drive-landscape, data-science-study (copier, behind) | No `hooks_reminder`: a fresh clone gets no hooks-off notice. Comes with their next `copier update`. |
| edmonton-tax-viz (and its report worktree) | No `hooks_reminder`. Hook identical apart from comments. |
| The four sims, PeterFriedrich.github.io | Own `SUBSTANTIVE`, `main` in the hook. No branch reminder, no `hooks_reminder`. |
| landing_page | Own `SUBSTANTIVE` (misses `wp-content/`), `origin/main`. No hook. |
| regenx_app_refactor | Own `SUBSTANTIVE`, `TRUNK = "main"`, trunk read from `origin/HEAD` (TODO T2). |
| server-ops | Exclude-list `SUBSTANTIVE`. Branch reminder asks for `origin/master` on a `main` repo. No hook. |

The brief names three hand-ports. There are nine: the four sims,
PeterFriedrich.github.io and server-ops also carry one. `core.hooksPath` is
set in all 15 repos that have a hook, and each hook names its repo's real
trunk.

## Fix order proposed (TODO X; nothing is fixed in this PR)

1. Tests first: port tax-viz's handoff-gap tests, and add a hook test with a
   stand-in `gh` (F17).
2. The owner checks the session-end channel by hand, then the script exits 2
   there or the hook and its README row go (F6).
3. `SUBSTANTIVE`, plan first: an exclude-list by default, or a project-owned
   list of extra paths (F7).
4. The false silences in `gap()` and the reminder (F1–F3, F12, F14, F15).
5. The hook, with P3 and T2: read the pushed refs, compare by patch, say when
   `gh` failed (F9–F11).
6. Docs: whether `gh` exists in a cloud VM (F8); the docstring's two wrong
   statements (detached `HEAD`, the stderr citation).
7. The owner's call: a session-end line for commits on no remote (F4).

No decision locked or reopened, so no `docs/DECISIONS.md` row. The template
keeps `docs/ASSUMPTIONS.md` row-free by test, so no row there.

## Not checked

- The session-end channel, live (F6): refused by the permission mode.
- Anything in a cloud VM: whether `gh` exists (F8), whether the clone is
  shallow (F5), whether a push there goes through git at all.
- Which PR `gh` picks when a branch has an open PR and an older merged one.
- Claude Code started from a subfolder. Run by hand with the project
  directory set to `scripts/`, the hook command is silent; I don't know
  whether Claude Code would load the hook there.
- Whether the 17 delivered notices were each followed by a handoff.
- TODO F's cross-merge cases.

## What this run got wrong

- **My first timing was a silent pass.** It showed 3 ms per repo because the
  interpreter path was relative after a `cd`, so the script never ran and the
  error went to `/dev/null`. Re-run with an absolute path: about 60 ms. This is
  the class being audited, in my own instrument.
- **My first "gh not installed" run had `gh` installed.** The real `gh` was
  still on the PATH and failed for another reason, so the run tested F9, not
  F8. Redone with a PATH that has no `gh`.
- **I nearly reported four stranded commits.** Five commits exist on no
  remote; `git cherry` showed four had landed as equal patches. "On no remote"
  over-counts wherever a PR was squash-merged.
- **I took F2 for a discovery.** tax-viz pins it as intended. It is reported
  as a decision I argue against, not a bug nobody knew.
- **The "other" column over-states missed work.** It mixes README edits and
  bot commits with real work, so the table gives per-folder counts and the text
  uses those. The measuring script also could not parse server-ops's list.
- **The filename check compares neighbours only**, so three inversions in
  tax-viz is a floor.
- **I read three stale trunk refs and reported one false state from them**
  (caught by `template`). The first version of this doc said
  data-science-study's only handoff sat on an unmerged branch, so `master` had
  no baseline. It merged as that repo's PR 5 on 2026-10-30; the handoff is on
  `master`, and the check is silent there only because `studies/` is not
  listed. Cause: I may not fetch in another repo, so I read each local
  `origin` trunk ref, and that one was last updated three minutes before the
  merge. I did not compare the refs with the remote, which `git ls-remote`
  does without writing. Done afterwards for all 17: alberta and drive-landscape
  were stale the same way, each missing one handoff commit and its merge from
  the same morning. Their rows and data-science-study's are corrected (one
  more docs-only commit each); no verdict moves. A local ref is a reading as
  of its last fetch, which is the "guards measure data, not metadata" class.
- **F6 rests on a negative.** "No transcript records a SessionEnd result" is
  the highest-risk claim shape, and I could not find the reader or prove there
  is none. It is marked unverified for that reason.

## Appendix: the runs

`handoff_gap.py --session-start` unless noted. "Notice" means the gap message
appeared; "silent" means no output, exit 0.

| Run | State | Result |
|---|---|---|
| C1 | one commit in `scripts/` after the handoff | notice (control) |
| C2 | one uncommitted file in `scripts/`; also with `--session-end` | notice, both |
| A1 | no `session-summary/`; 2 commits and 1 dirty file | silent |
| A2 | every handoff archived; 1 commit | silent |
| A3, A3b | 2 owed commits and a new untracked handoff; plus 1 dirty file | silent, both |
| A4 | 1 owed commit and an untracked `notes.md` in `session-summary/` | silent |
| A5 | 1 owed commit, then a tracked `README.md` in `session-summary/` | silent; later commits are measured from the README |
| A6 | 1 owed commit, then a one-character edit to the handoff | silent |
| A7 | detached `HEAD`, 1 owed commit | notice |
| A8 | 2 commits on another local branch, `HEAD` on `master` | silent |
| A9 | no origin, 1 owed commit | notice |
| A10 | git off the PATH, 1 owed commit | no gap notice; false "hooks are off" |
| A11 | a merge commit that itself edits `scripts/` | silent |
| A12 | 5 untracked files in a new `src/` folder | notice, "1 uncommitted file" |
| B1 | shallow clone of 3 owed commits, depth 1 / 2 / 3 / 10 | silent / 1 / 2 / 3 named |
| B2a–c | new worktree; 1 commit in it; the main clone meanwhile | silent / notice / silent |
| B2d | worktree, absolute `core.hooksPath` to the main clone | false "hooks are off" |
| B3a–c | `-evening` beside `_S12`; `_S8` and `_S10`; `.md` and `-b.md` | notice names the older file, each |
| B4 | one commit to each of 15 paths outside the list | silent, all 15 |
| U1 | work and handoff committed on a local branch, never pushed (`--session-end`) | silent |
| — | Python 3.6, C locale: plain / `--session-end` / `--session-start` | traceback / notice with escapes / notice |
| — | the two hook command strings from `.claude/settings.json`, run as written | notice on stdout (start) and stderr (end), exit 0 |
| — | the start command with the project directory set to `scripts/` | silent |

Pushes through `.githooks/pre-push`. The branch `feat` has a merged PR unless
noted, and one commit made after the merge.

| Run | State | Result |
|---|---|---|
| P0 | on `feat`, push `feat` | blocked (control) |
| P0b | no new commit | pushed |
| P1 | `gh` not on the PATH | pushed |
| P2 | `gh` exits 1 | pushed, no output |
| P3 | on `master`, push `feat` (known) | pushed |
| P4 | detached `HEAD`, push `HEAD:feat` | pushed |
| P5 | trunk is `main`, hook unedited | pushed |
| P6a | squash-merged, no new commit | blocked, "2 commit(s)" |
| P6b | squash-merged, one new commit | blocked, "3 commit(s)"; three listed to cherry-pick |
| P7 | hook not executable | pushed, git hint only; reminder silent |
| P9 | a worktree on `feat`, relative `core.hooksPath` | blocked |
| P10 | local `feat-local` pushed to remote `feat` | pushed |
| P12a–c | on `feat`: delete another branch; push a tag; push `master` | blocked, all three |
| P13 | `gh` takes 20 s | blocked after 20 s |
| P14a–b | PR open; PR closed unmerged | pushed, both |
