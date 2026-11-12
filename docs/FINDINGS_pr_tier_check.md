# Findings: the planned PR-tier check (`check_pr_body.py`, TODO J)

Run 2026-11-12 by `template-audit-tier` (`claude-fable-5-2`, own worktree),
`project-audit` on the PR-tier-check brief (out of repo, in
`/home/opc/research/cc-data-project-template/audits/`). The target is a plan,
not code: `TODO.md` item J as it stands on template `master` at `ebc0c3c`.
Ledger row: `docs/AUDIT_LEDGER.md`, 2026-11-12.

Method. Every repo was fetched before it was read (`git fetch`, then `gh`).
467 merged PRs came from `gh` for eight repos: the template (85), tax-viz (its
last 160), civic-map (77), open-data-landscape (44), drive-landscape (46),
alberta (39), permit-speed (10) and data-science-study (6). Each PR's files
and their added/modified status came from its merge commit. A scratch
prototype of the check, written from J's text, was run over all 467. The last
30 code PRs in tax-viz, the last 30 in civic-map and 23 in alberta were then
read by hand: 83 PRs, in the appendix. Two open points were tested instead of
argued: a copier update in a scratch clone, and a body edit on this PR.

Nothing is built or fixed in this PR. `TODO.md` is not edited: the proposed
changes to J's plan have their own section below, for the owner.

## Verdicts

| Level | Verdict | In one line |
|---|---|---|
| L0. Should the tier be gated at all? | **CONDITIONAL** | The review line has the trial behind it. The tier comparison would have changed two PRs in the window, both already known and both already reviewed. Its one consumer is self-merge, which needs one bit: low or not. As written the check also fails 57 docs-only PRs for not saying "low" (F1–F3). |
| L1. Does a path list capture the tier? | **UNSOUND** as written, **CONDITIONAL** with F4's fix | The plan doesn't say what a path in no glob gets. With the template defaults the computed tier is below what the PR did in 27 of 53 code PRs in two projects, a publish of served data among them. tax-viz's own list misses 4 of 30. All 31 misses are paths a list could name (F4–F9). |
| L2. The open points | **CONDITIONAL** | Each has an answer. Where the list lives and whether a body edit re-runs CI were measured (F10–F13). |
| L3. Gaming and drift | Review line **UNSOUND** as written; the rest **CONDITIONAL** | 6 of the 22 review lines on required paths say "skipped", and a check that a line exists passes them. A PR can lower its own tier by editing the list. Nothing keeps a list current (F14–F16). |

L1's failure is one missing rule, and the brief asks L2 and L3 separately, so
they were still run. They assume F4's fix.

**Is J worth building as written? No.** Replayed over the 126 PRs merged
2026-10-19 to 11-11 it goes red on 80, and 57 of those are docs-only PRs
missing a line that would say "low". It would accept `Risk: low` on civic-map 74,
which published redrawn ward data. It passes "Code review: skipped (not run)". With
the edits below, the review half is worth building now. The tier half is
worth building only if self-merge is still wanted, and then as a floor the
check computes, not a line it grades.

## What was measured

**The window in `docs/TODO_archive.md` §M (2026-10-19 to 11-04).** 88 PRs in
the eight repos. §M counted 94; this run finds 91 to 95 depending on the
boundary hours (see "What this run got wrong"). The comparable tallies agree:
20 tagged low, and 58 with no tier here against §M's 60.

| | 10-19 to 11-04 | 11-05 to 11-11 | Both |
|---|---|---|---|
| Merged PRs | 88 | 38 | 126 |
| Docs-only (every file is `.md` or a handoff) | 59 | 30 | 89 |
| Carry a `Risk:` line | 30 | 19 | 49 |
| Stated tier equals / above / below the computed one | 25 / 3 / 2 | 18 / 1 / 0 | 43 / 4 / 2 |
| **Fail as J is written** | **60** | **20** | **80** |
| of those, docs-only with no `Risk:` line | 39 | 18 | 57 |
| of those, code PRs with no `Risk:` line | 19 | 1 | 20 |
| of those, stated below computed | 2 | 0 | 2 |
| of those, a review-required path with no review line and nothing else wrong | 0 | 1 | 1 |
| Fail if a PR computed low needs no line (E2) | 19 | 2 | 21 |
| Touch a review-required path (`src/` `scripts/` `tools/` `notebooks/`) | 22 | 8 | 30 |
| of those: line says a review ran / says skipped / no line | 10 / 6 / 6 | 6 / 0 / 2 | 16 / 6 / 8 |

The two PRs stated below computed are the two known misses, tax-viz 774 and
776. The replay finds no third.

**The hand replay (appendix).** Computed tier against what the PR really did,
read from its body and file list by step 2.2's rule text. tax-viz is replayed
with its own list plus the one served writer DECISIONS 2026-11-08 names.
civic-map and alberta have written no list, so they get the template defaults.

| Project (list used) | Code PRs read | Computed = really | Computed below | Computed above |
|---|---|---|---|---|
| edmonton-tax-viz (its own) | 30 | 25 | 4 | 1 |
| edmonton-civic-map (template defaults) | 30 | 15 | 15 | 0 |
| alberta-regional-viz (template defaults) | 23 | 11 | 12 | 0 |
| All | 83 | 51 | 31 | 1 |

| Kind of miss (computed below what it did) | PRs | Where |
|---|---|---|
| S. Served or committed output data is in the diff, under a path no glob rates high | 16 | civic-map 7 (`site/public/data/`), alberta 8 (`data/processed/`), tax-viz 1 (`web/data/`) |
| U. The changed code is in no glob at all | 12 | civic-map 6 (`site/`, `prototype/`, `bootstrap.sh`), alberta 4 (`notebooks/`, `tools/`, `data/`), tax-viz 2 (`requirements.txt`, skill code under `.claude/`) |
| P. `src/` behind a published number, medium by the default glob | 2 | civic-map |
| W. A served-output writer the list doesn't name (the 774 kind) | 1 | tax-viz 742 |

Of the 83, 11 carry a stated tier: 8 equal what the PR did, 2 are below (774,
776) and 1 is above (tax-viz 796, `high (web/)` where its own list says
medium).

**How much of each repo the list covers.** Tracked files other than `.md` and
handoffs, at each fetched `master`, that match no tier glob:

| Repo (list) | Tracked | In no glob | Largest |
|---|---|---|---|
| edmonton-civic-map (default) | 2,893 | 2,859 (98%) | `site/` 2,831 |
| data-science-study (default) | 23 | 12 (52%) | |
| edmonton-open-data-landscape (default) | 63 | 28 (44%) | `data/` 17 |
| alberta-regional-viz (default) | 63 | 27 (42%) | `data/` 12, `notebooks/` 4 |
| template (default) | 38 | 14 (36%) | |
| edmonton-permit-speed (its own) | 33 | 11 (33%) | |
| drive-landscape (default) | 45 | 14 (31%) | |
| edmonton-tax-viz (its own) | 324 | 24 (7%) | `data/` 11, `main.py` |

`.githooks/` and `.claude/` are in no glob in all eight. Across the 467 PRs,
100 changed at least one file other than `.md` that no glob covers.

## L0. Should the tier be gated at all?

**F1. Across the window the tier comparison changes two PRs, and the review
had already run on both.** Of 88 PRs the check as written fails 60. 39 are
docs-only PRs with no `Risk:` line. 19 are code PRs with no line: 13 sit in
four repos whose pipeline has no tier rule or leaves its row `not evaluated`
(civic-map 5, drive 3, open-data 3, alberta 2), 3 are template PRs from before
the line existed (PR 53 was the first), and 3 are tax-viz PRs from 10-19 and
10-20, the day before it ported the rule. Only open-data 46 came after its
repo had the rule text. The remaining 2 are tax-viz 774 and 776. Both carried
a `/code-review medium` tally when they merged, and the review, not the tier,
found 776's wrong coefficient. A correct tier on those two would have changed
what step 3.1 asks of the owner (read the diff, named hunks). It would not
have found anything.

**F2. A missing line on a low PR carries no information, and failing it
contradicts an owner instruction.** The check computes the tier before it
reads the body. For a docs-only PR it computes low, then fails because the
body doesn't say "low". 57 of the 80 failures through 11-11 are this. In
tax-viz the owner asked for the opposite on 2026-10-21 (its step 2.2:
"A docs-only PR skips them ... terse bodies for docs and editorial changes"),
and 31 of its 43 PRs since 10-19 are docs-only, 29 of them with no `Risk:`
line. All 31 are docs-only by path: no code hid behind the exemption.

**F3. The tier has one mechanical consumer, and it needs one bit.** Step 3.1's
medium and high differ only in what the owner does before merging, which no
check sees. The consumer is self-merge of low (DECISIONS 2026-11-04). Two
projects already self-merge on that bit without a check: tax-viz
("docs-only PRs are self-merged", its fit table) and permit-speed ("the owner
lets sessions merge docs-only PRs"). So the question the check can answer for
self-merge is "is the computed tier low", and the body line adds nothing to
that answer.

What the line does add is a way to go up. 4 of the 49 stated tiers are above
the computed one, and three of the four are right: civic-map 79 and 80 say
high for `src/` behind a published number, and template 61 says medium because a
skill file "reaches every project". A path list can't make those calls.

*Sharpest argument against gating the tier:* the check asks the author to
type a value CI has just computed and fails them when it differs. *Against
dropping it:* the body is what the owner reads at merge time, and the two
known misses were both a session's judgment sitting where a path rule
belonged. *Evidence that would change this:* TODO L's baseline of fixes after
a merge, split by tier. It was meant to come before J and isn't built, so
there is no count of what a wrong tier has cost.

## L1. Does a path list capture the tier?

**F4. The plan doesn't say what a path in no glob gets, and with the natural
reading (nothing) the product itself is outside the list.** J describes "glob
→ tier" with defaults from step 2.2: `.github/workflows/` high, `src/` and
`scripts/` medium, docs low. In civic-map the app (`site/`), the served data
(`site/public/data/`), the build config and `prototype/` match nothing. Three
of its PRs compute low or nothing while changing what the public sees:

- civic-map 74, "Publish the held refresh": 23 served files change;
  the body says "Your merge publishes this". Computed low.
- civic-map 68, a banner on both served pages. Computed nothing.
- civic-map 60, the shareable link: new site code. Computed low.

This is the fault the safety-net audit found in `SUBSTANTIVE` on 2026-11-11
(`docs/FINDINGS_session_safety_net.md`, L1): an include-list fails silent on
everything it doesn't name, and 0 of 8 copier projects had changed that list.
Here 2 of 9 projects have written a tier list (tax-viz and permit-speed, as
prose in their pipeline), 4 answer the row `not evaluated`, and 3 run a
pipeline from before the row existed.

**F5. Every one of the 31 misses is a path, so a list can express them. The
defaults can't.** A fuller list per project, written by this run after reading
the PRs, brings the misses to 0 of 83 and puts 8 PRs above what they did
(mostly new `src/` code with nothing served yet). That list is hindsight. It
shows the misses are nameable, not that a project would have named them.

**F6. The default tier list and the default review list disagree.** J's
review globs are `src/` `scripts/` `tools/` `notebooks/`. Step 2.2's tier
defaults name neither `tools/` nor `notebooks/`. alberta 29 adds
`tools/data_map.py` and a notebook: review required, tier low.

**F7. tax-viz's list, the most complete one, still leaves out three files that
write served data.** DECISIONS 2026-11-08 has each project name its served
writers as high. Reading the fetched `master`: `main.py` names twelve output
paths under `web/data/`, `scripts/generate_status.py` writes `web/data/status.json`,
and `scripts/build_reference_layers.py` writes `web/data/reference.geojson`.
None is high in its list; `main.py`, at the repo root, matches no glob at all.
tax-viz 742 changed where `build_reference_layers.py` fetches from (medium by
the list) and 738 changed the served file itself (`web/` is medium). Also in
no glob: `requirements-ci.txt`, which is what the weekly refresh installs
(tax-viz 681 bumped a pin there), and `.githooks/pre-push`.

**F8. "Tests only added" can't be read from which files changed.** tax-viz 765
added 30 lines and removed none in an existing test file. By file status that
is a changed test, medium. Counting removed lines under `tests/` would tell
the two apart.

**F9. "Docs" is not the same as low.** A data contract lives in a doc:
civic-map's `docs/SPEC_data_schema.md` changed in 13 of its 30 code PRs, and
38 docs-only PRs across the repos change a `SPEC_*.md`. In the template
`docs/CHANGE_PIPELINE.md`, `CLAUDE.md` and the skills are what every project
receives. Of the 32 PRs tagged low through 11-11, 14 touch `DECISIONS.md`, a
`SPEC_*.md`, `CHANGE_PIPELINE.md`, `CLAUDE.md` or a skill. That is fine while
the owner merges. It matters the day low means self-merge: a session could
merge its own decision row. Also, low must be a list of paths, not a file
extension: tax-viz serves `web/verified/*.md`.

*Sharpest argument against L1:* the two known misses were judgment replacing a
path rule, and the replay shows the path rule replacing judgment would be
wrong more often than the judgment was, wherever the list is the default.
*Evidence that would change it:* a project list written before the PRs it is
scored on. permit-speed's is the only candidate and it has two code PRs.

## L2. The open points

**F10. Where the list lives: defaults in the script, the project's additions
in a file copier writes once.** Tested in a scratch clone of the template and
a scratch project made from it with copier 9.18.2:

| File in the template | An existing project's next `copier update` | After the project edits it and the template changes it |
|---|---|---|
| Listed in `_skip_if_exists` | The file arrives | The project's copy is untouched: no conflict, and the template's change never arrives |
| Shipped normally | The file arrives | One conflict block (`<<<<<<< before updating`) |

So a single shipped list file reproduces the fit-table problem, and a
`_skip_if_exists` file alone means a default added later (say `.githooks/`)
reaches no existing project. `check_fit_table.py` already has the answer:
its step list ships inside the script, which projects don't edit. Do the same
with two layers: the floor (workflows, the paths the template itself ships)
in `check_pr_body.py`, and the project's own globs in a `_skip_if_exists`
file. The format should be JSON. `handoff_gap.py` has to run on Python 3.6,
which has no TOML reader, and CI gets a YAML reader only through the `copier`
pin that TODO O4 wants to drop. TODO X3 and O3 each ask for a project-owned
path file too (bot-output paths; extra synced paths). One file can hold all
three.

**F11. A body edit does not re-run CI today, in any repo.** All eight
`tests.yml` files use a bare `pull_request:` trigger, which GitHub runs on
opened, synchronize and reopened. Tested on this run's own PR: see "The body
edit test" below. Body edits are rare now: 5 of 123 PRs since 10-19 in
seven of the repos. But all 5 came after the last commit and before the
merge, and once a body can fail CI the fix is always a body edit. Adding `edited` to the trigger types re-runs
the whole job per edit: a median 19 s in the template, 59 s in tax-viz, 63 s
in civic-map. Two limits. GitHub's "Re-run jobs" replays the original event,
so it would grade the old body (from GitHub's documentation, not tested here).
And `tests.yml` is forked in civic-map and hand-ported in tax-viz, so the
trigger change won't arrive there by itself.

**F12. The `web/` default is the wrong question.** Of the eight repos only tax-viz
and drive have a `web/` folder; civic-map's page is `site/`. Whether `web/` requires a review
is each project's line in its own file. The default that matters is F4's. For
tax-viz the trial's gap has one data point now: PR 796 (`web/index.html`,
merged 11-10) ran `/code-review medium` and fixed 5 of 9 findings.

**F13. A fork or bot PR with no body: no case exists, so no special rule.**
All 467 PRs are by the owner's account and none is from a fork. No repo has a
Dependabot or Renovate config. The bots here never open a PR: tax-viz's
`data-bot` and civic-map's `github-actions[bot]` push refreshed data straight
to `master`, so the check never sees them and has to do nothing on a `push`
event. An empty body should fail the same way a missing line does. Pass the
body through an environment variable, never inside a `run:` line, since the
body is free text. Reopen this if a bot starts opening PRs: it can't write
the lines.

## L3. Gaming and drift

**F14. A check that the `Code review:` line exists passes "skipped (not
run)".** Of the 30 PRs on review-required paths since 10-19, 22 carry the
line. 16 report a review and 6 say skipped:

- permit-speed 8: "Code review: skipped (not run)", on a PR it rates high
  itself, for the two scripts that hold its archive's data contract.
- template 42 and 52: skipped, each with a reason, on a new hook check and a
  new guard. Template 53: skipped for a one-list edit.
- permit-speed 7 and civic-map 71: skipped because the code is the template's,
  taken as shipped.

None of these hid anything; each says what happened. But the check as planned
would have changed none of them, and for the 8 with no line the cheapest way
to green is the same sentence. Three more things in the same lines:

- **The format varies.** 4 of the 16 genuine lines read "Code review
  (medium): ..." or "**Code review (medium):** ...", which a match on
  `Code review:` rejects. One `Risk:` sits mid-sentence (tax-viz 789), two are
  bold, and 6 of the 49 come after the fifth line of the body.
- **The level isn't checked.** Template 62 ran `low` on `scripts/`, where J
  says `medium`.
- **Template updates.** 4 of the 30 are `copier update` PRs. Requiring a
  60k-token review of code already reviewed upstream is waste, so a rule that
  fails "skipped" needs one named exception.

Offline, CI can't prove a review ran. It can make the body state the level
and a finding count, which turns an omission into a false statement. Whether
"skipped" then fails or passes in plain sight is the owner's call.

**F15. A PR can lower its own tier.** If the check reads the list from the PR
branch, a PR that edits the list is graded by its own edit. `check_fit_table`
already compares against the base branch for the same reason. Read the list
from the base, and rate the list file and `check_pr_body.py` high in the
built-in floor. Putting code where no glob looks is F4. Splitting a PR in two
is not prevented by anything, and doesn't need to be: each half is graded.

**F16. Nothing in the plan keeps a list current.** tax-viz's list is three
weeks old and misses `main.py` (F7). With F4's fix the list maintains itself:
the first PR to touch an unnamed path fails until the path is named. Served
writers need their own keeper, since a new writer is a new file under an
already-listed folder. A project test can do it from a source that exists:
every script its publish workflow runs is high (tax-viz's `refresh.yml` runs
15).

## Proposed changes to J's plan (the owner decides; `TODO.md` is unchanged)

- **E1. A changed path in no glob fails, naming the path** (F4, F16). The
  built-in floor rates what the template ships (`.claude/`, `.githooks/`,
  `bootstrap.sh`, `requirements*.txt`, `.copier-answers.yml`, `tools/`,
  `notebooks/`, `data/`). That leaves each project its own names to list
  once: none in four projects, `web/` in drive, 4 in tax-viz (`main.py`
  among them) and 10 in civic-map. The softer
  alternative is "unnamed means medium", which never goes red but would still
  rate civic-map's served data medium.
- **E2. A PR computed low needs no `Risk:` line** (F2). A missing line means
  low. Fail when the computed tier is medium or high and the line is missing
  or lower. This depends on E1: without it civic-map 74 passes with no line
  at all. Through 11-11 it cuts the failures from 80 to 21.
- **E3. The author may state a higher tier, never a lower one** (F3). Keep
  the line for that.
- **E4. Self-merge, if it comes, keys on the computed tier**, not the stated
  one, and "low" is a path list the owner has read (F3, F9): handoffs,
  `TODO.md`, findings. Whether a PR that adds a `DECISIONS.md` row or changes
  a `SPEC_*.md` can self-merge is the owner's call.
- **E5. Two layers for the list** (F10): the floor in the script, the
  project's globs in a `_skip_if_exists` JSON file, shared with X3 and O3.
  The fit-table row points at the file. A test pins that the file parses and
  that no project glob lowers a floor path.
- **E6. Read the list from the base branch; the list file and the check are
  high** (F15).
- **E7. Trigger and input** (F11, F13): `pull_request` with `types: [opened,
  synchronize, reopened, edited]`; do nothing on `push`; body from an
  environment variable; an empty body is a missing line.
- **E8. The review line** (F14): accept `Code review:` and `Code review
  (level):`, anywhere in the body; print the expected form in the failure
  message. On a review-required path require a level at or above the list's
  and a finding count. Owner's call: "skipped" fails, except `skipped
  (template update)` when `.copier-answers.yml` is in the diff; or "skipped"
  passes and the check only guarantees it is said.
- **E9. Give `tools/` and `notebooks/` a default tier** (F6), and tell added
  tests from changed ones by removed lines, or drop the distinction (F8).
- **E10. Served writers get a keeper** (F7, F16): a per-project test that
  every script the publish workflow runs is high. For tax-viz, pass on:
  `main.py`, `scripts/generate_status.py`, `scripts/build_reference_layers.py`
  and `requirements-ci.txt` are outside its high list (its repo, its call).
- **Order.** E7 and E8 alone are the review half and can ship first: they
  need no path list beyond the four review globs. E1, E2, E5 and E6 are the
  tier half and belong together. Build TODO L's baseline before deciding
  whether the tier half is worth its upkeep.

## The body edit test

Run on this audit's own PR, template 86, opened as a draft on `tests.yml` as
it stands (bare `pull_request:`).

| Step | Time (UTC, 2026-11-12) | Workflow runs on the branch |
|---|---|---|
| PR opened | 01:15:15 | 1 (`pull_request`, passed in 17 s) |
| Body edited once with `gh pr edit` (GitHub records the edit at 01:16:01) | 01:16:01 | 1 |
| Last look, four and a half minutes after the edit | 01:20:34 | 1, and one `test` check run on the head commit, started 01:15:22 |

No run started after the edit. So today a body that failed the check could
only be graded again by pushing a commit. What `edited` in the trigger types
would do was not tested: that needs a change to `tests.yml`, which is J's
build, not this audit's.

## Not checked

- No project session was asked anything. The PRs answered what the brief
  asked; why tax-viz 776 was written "low" is already in §M.
- The template's own 85 PRs, open-data-landscape, drive-landscape and
  permit-speed were replayed by the prototype but not read by hand.
  edmonton-nonprofit-map and recommendation-algorithms-explained have no
  merged PR in the window.
- Whether a failing review check would make reviews run. The data is lines
  in bodies, not transcripts.
- Private repos (permit-speed, data-science-study) have no required check, so
  there the check is advice (DECISIONS 2026-10-15).
- How the check reaches projects: none of the eight copier projects is at the
  template's current commit (`docs/FINDINGS_template_reach.md`).
- `Tested:`, `Undo:` and `Cause:` lines. J doesn't gate them.

## What this run got wrong

- **My first pattern for the review line had the fault F14 describes.** It
  matched `Code review:` at the start of a line and reported 12
  review-required PRs with no line since 10-19. Four of them have one, written
  "Code review (medium): ...". I found it only because three tax-viz PRs
  rated high showed no review, which didn't fit that session's habits, and I
  read the bodies. The count is 8. A check that reads a free-text line will
  make the same mistake unless the accepted forms are tested against real
  bodies first.
- **The replay reads each PR's merge commit, and for one PR that is not what
  CI would have seen.** alberta 16 was stacked under alberta 17, which merged
  two seconds earlier carrying 16's commits. 16's own merge commit holds only
  docs, so the replay calls it docs-only. Its PR diff had `src/` and a
  committed output. alberta therefore has 24 code PRs, not 23, and the 24th
  would be one more miss of kind S. It is not in the tables.
- **§M's 94 was not reproduced.** The eight repos give 88 PRs merged 10-19 to
  11-04 (UTC). Adding ai-safety (1) and regenx (2) gives 91, and shifting the
  boundary hours gives 91 to 95. The replay covers the 88.
- **"Really" is one reader's call.** It comes from each body and file list;
  the diff itself was opened for five PRs (tax-viz 710, 738, 742, 765 and the
  alberta pair above). alberta has published nothing outside its repo, so
  rating its committed output tables high follows the rule's wording, not a
  reader's harm.
- **The tax-viz list I replayed is my transcription** of the prose in its
  step 2.2 into globs. "A served column or file shape" has no glob; I added
  the one writer the 2026-11-08 decision names. Without it 774 computes
  medium and tax-viz has 5 misses of 30.
- **The fuller lists in F5 are hindsight**, as said there.
- **Two claims rest on GitHub's documentation, not on a test here:** that
  `edited` re-runs the job, and that "Re-run jobs" replays the old body.
- **The negatives, and how each was checked.** "No fork or bot PR": by
  listing the author and the cross-repository flag of all 467, not by a
  search that returned nothing. "No trigger includes `edited`": by reading
  each `tests.yml` at its fetched `master`; other workflows were not read.
  "No third PR stated below computed": true for the lists replayed, and F4
  is the reason it means little for the six repos on defaults.

## Appendix: the hand replay

Computed is the prototype's tier under the list named in "What was measured";
"none" means no glob matched. Really is the tier by step 2.2's rule text.
Kinds: S, U, P, W as in the table above; A, tests added inside an existing
file; T, the tiers agree but the change in the rated path is trivial; ok,
they agree. "Fuller list" is the tier under the list this run wrote
afterwards (F5).

| PR | Merged | Computed | Stated | Really | Kind | Fuller list | What it did |
|---|---|---|---|---|---|---|---|
| tax-viz 796 | 11-10 | medium | high | medium | ok | medium | one served panel; stated high, above its own list |
| tax-viz 794 | 11-10 | high | high | high | ok | high | refresh workflow |
| tax-viz 793 | 11-10 | high | high | high | ok | high | refresh workflow, new committed baseline |
| tax-viz 790 | 11-10 | high | high | high | ok | high | src; one neighbourhood +28 units |
| tax-viz 782 | 11-09 | medium | medium | medium | ok | medium |  |
| tax-viz 780 | 11-08 | medium | medium | medium | ok | medium |  |
| tax-viz 776 | 11-03 | high | low | high | ok | high | src; stated low (the known miss) |
| tax-viz 774 | 11-02 | high | medium | high | ok | high | tool writes a served file; high only because the writer is named; stated medium (the known miss) |
| tax-viz 773 | 11-03 | high | high | high | ok | high | scheduled workflow |
| tax-viz 765 | 10-20 | medium | none | low | A | medium | docs restore plus 30 added test lines in an existing file |
| tax-viz 761 | 10-19 | medium | none | medium | ok | medium | standalone notebook |
| tax-viz 760 | 10-19 | high | none | high | ok | high | src; refresh had failed |
| tax-viz 758 | 10-17 | medium | none | medium | ok | medium | web layout |
| tax-viz 756 | 10-17 | low | none | low | ok | low | docs, a new test file |
| tax-viz 753 | 10-16 | none | none | medium | U | medium | requirements.txt re-pin; no glob matches it |
| tax-viz 747 | 10-14 | none | none | medium | U | medium | new skill code under .claude/ (compose.py, render.js); no glob |
| tax-viz 743 | 10-14 | medium | none | medium | ok | medium |  |
| tax-viz 742 | 10-13 | medium | none | high | W | high | scripts/build_reference_layers.py writes served web/data/reference.geojson |
| tax-viz 740 | 10-13 | medium | none | medium | ok | medium |  |
| tax-viz 738 | 10-13 | medium | none | high | S | high | served web/data/reference.geojson changes, with its writer; web/ is medium |
| tax-viz 737 | 10-13 | medium | none | medium | ok | medium | ships a font |
| tax-viz 736 | 10-13 | medium | none | medium | ok | medium |  |
| tax-viz 735 | 10-13 | medium | none | medium | ok | medium |  |
| tax-viz 727 | 10-12 | medium | none | medium | ok | medium | hook script |
| tax-viz 725 | 10-12 | medium | none | medium | ok | medium |  |
| tax-viz 724 | 10-12 | medium | none | medium | T | medium | deletes four stray probes |
| tax-viz 719 | 10-10 | medium | none | medium | ok | medium |  |
| tax-viz 714 | 10-10 | low | none | low | ok | low | adds a 1,700-line CSV to a public repo: step 1.7's security trigger, which the plan doesn't check |
| tax-viz 711 | 10-10 | medium | none | medium | ok | medium |  |
| tax-viz 710 | 10-10 | high | none | high | T | high | data/*.json, but only a prose field changed |
| civic-map 80 | 11-04 | medium | high | high | P | high | src behind published office holders; loosens a fail-closed stop; schema doc |
| civic-map 79 | 11-03 | medium | high | high | S | high | served officeholders.json and its builder |
| civic-map 74 | 10-21 | low | none | high | S | high | publishes a held refresh: served address files |
| civic-map 73 | 10-21 | high | none | high | ok | high | refresh token |
| civic-map 72 | 10-20 | high | none | high | T | high | removes one duplicate CI step |
| civic-map 71 | 10-19 | high | none | high | ok | high | template update incl. tests.yml |
| civic-map 70 | 10-19 | high | none | high | ok | high | CI |
| civic-map 68 | 10-17 | none | none | medium | U | medium | served pages; site/ is in no glob |
| civic-map 60 | 10-17 | low | none | medium | U | medium | site code and smoke test; neither in a glob |
| civic-map 59 | 10-17 | high | none | high | ok | high | refresh workflow, new published file |
| civic-map 57 | 10-17 | medium | none | high | S | high | 358 served files rebuilt from a new licensed source |
| civic-map 55 | 10-16 | medium | none | medium | ok | medium | new page; medium only through a changed test |
| civic-map 54 | 10-16 | medium | none | high | P | high | the rules that decide whether a refresh publishes |
| civic-map 53 | 10-16 | high | none | high | ok | high |  |
| civic-map 51 | 10-16 | high | none | high | ok | high |  |
| civic-map 50 | 10-16 | high | none | high | ok | high |  |
| civic-map 49 | 10-16 | high | none | high | ok | high |  |
| civic-map 48 | 10-16 | low | none | medium | U | medium | bootstrap.sh and a prototype script |
| civic-map 47 | 10-16 | medium | none | high | S | high | new served staleness.json, diff check, schema |
| civic-map 45 | 10-16 | high | none | high | ok | high |  |
| civic-map 44 | 10-16 | medium | none | high | S | high | new served officeholders.json |
| civic-map 43 | 10-15 | high | none | high | ok | high |  |
| civic-map 42 | 10-16 | low | none | low | ok | low |  |
| civic-map 40 | 10-15 | medium | none | high | S | high | 2,808 served address files added |
| civic-map 39 | 10-15 | medium | none | high | S | high | first served boundary files; CI pins |
| civic-map 38 | 10-15 | medium | none | medium | ok | high | downloaders, nothing served yet |
| civic-map 36 | 10-15 | low | none | medium | U | medium | prototype script; no glob |
| civic-map 33 | 10-14 | medium | none | medium | ok | medium |  |
| civic-map 29 | 10-14 | low | none | medium | U | high | site data and page |
| civic-map 28 | 10-14 | none | none | medium | U | high | site data and page |
| alberta 37 | 10-21 | high | none | high | ok | high | template update incl. tests.yml |
| alberta 35 | 10-19 | medium | none | high | S | high | committed output series changes, with src |
| alberta 32 | 10-16 | high | none | high | ok | high |  |
| alberta 31 | 10-16 | medium | none | medium | ok | medium |  |
| alberta 29 | 10-15 | low | none | medium | U | medium | tools/ and notebooks/ have no default tier |
| alberta 27 | 10-10 | medium | none | high | S | high | 96 rows leave a committed output |
| alberta 26 | 10-10 | low | none | medium | U | medium | notebook |
| alberta 25 | 10-10 | low | none | medium | U | medium | notebook, requirements.txt |
| alberta 23 | 10-03 | medium | none | high | S | high | three committed outputs; denominators redefined |
| alberta 20 | 10-03 | medium | none | medium | ok | high |  |
| alberta 19 | 10-02 | medium | none | high | S | high | new committed output |
| alberta 18 | 10-02 | medium | none | medium | ok | medium |  |
| alberta 17 | 10-02 | medium | none | high | S | high | new regions.csv column (the PR calls it a data contract); outputs |
| alberta 14 | 10-02 | medium | none | high | S | high | committed output changes |
| alberta 13 | 10-02 | low | none | medium | U | high | new committed input table under data/ |
| alberta 12 | 10-02 | medium | none | high | S | high | corrections applied to a committed output |
| alberta 11 | 10-02 | medium | none | high | S | high | new committed parse output |
| alberta 8 | 10-01 | medium | none | medium | ok | medium |  |
| alberta 7 | 10-01 | medium | none | medium | ok | high |  |
| alberta 6 | 10-01 | medium | none | medium | ok | medium |  |
| alberta 3 | 09-30 | none | none | low | ok | low | answers file only |
| alberta 2 | 09-30 | low | none | low | ok | medium |  |
| alberta 1 | 09-29 | medium | none | medium | ok | medium |  |
