# Findings: the two merge-gate guards with no tests of their own (TODO N target 3)

Run 2026-11-11 by `template-audit-guards` (`claude-fable-5-2`, own worktree),
`project-audit` on the merge-gate-guards brief (out of repo, in
`/home/opc/research/cc-data-project-template/audits/`). Targets:
`scripts/check_decisions_log.py` and `scripts/check_doc_citations.py`, template
`master` at `f6bb0f9`. Ledger row: `docs/AUDIT_LEDGER.md`, 2026-11-11.

Project evidence is read-only, from the local clones: tax-viz `40ef2a6`
(`master`), alberta `611a718` (branch `claude/s13-handoff`; its `docs/` and
`scripts/` match `origin/master`), permit-speed `0789580` (`master`). Every
project number below comes from running **the template's** copy of a guard
against that tree (`--root`, or its functions). tax-viz runs its own fork in CI.

Method: 127 smallest inputs, each passed to the guard's own `check()` (the
appendix lists all of them); the four repos measured; each guard gutted in a
scratch clone to see whether a test notices; CI history from `gh run list`.
Both guards exit 0 on all four repos today.

## Verdicts

| Level | `check_decisions_log.py` | `check_doc_citations.py` |
|---|---|---|
| L0. Worth gating a merge on? | **CONDITIONAL.** It buys a question at write time and a check that a cited test exists. The tag is the majority answer in the template (13 of 21 rows), and the step has never been red in CI. | **CONDITIONAL.** The line-number ban is sound. The "resolves" half has had nothing to check in three of the four repos: the section check ran on 0 of their 733 citations. |
| L1. Can a wrong row or citation pass? | Test rule **CONDITIONAL**: it holds only while the date cell parses (F7). Supersession rule **UNSOUND** as "every superseded row is marked": 22 natural wordings pass, and tax-viz holds 4 candidate cases (F8). | **UNSOUND**, beyond what TODO P1 already covers: one citation hides the next (9–14% of citations, F1), `.github/` is never opened (F2), anything in a string literal is skipped (F3). |
| L2. Can a correct one fail? | **CONDITIONAL.** No false alarm in the four logs today. 11 inputs fail wrongly; one tells the author to mark an innocent row as superseded (F11). | **CONDITIONAL.** Its one red CI run in the four repos' history was a false alarm (F5). 10 inputs. |
| L3. Code | **CONDITIONAL.** The OK line counts nothing, zero rows pass, an impossible date is a traceback (F12). | **CONDITIONAL.** Exclusion by substring, docs keyed by basename, no count in the OK line (F2, F6). |
| Tests | No test notices either guard gutted: 95 passed with each one returning nothing (F14). | |

Of the 127 inputs, 15 are baselines that behave. Of the other 112, 90 pass
when a correct guard would fail, 21 fail when it would pass, and 1 crashes. I
chose the inputs to break the guards, so that split is not a rate. Six of the
112 are known or by design, and the appendix marks them.

## What was measured

| | template | tax-viz | alberta | permit-speed |
|---|---|---|---|---|
| Decision rows (since `CUTOFF`) | 21 (21) | 391 (97) | 24 (24) | 1 (1) |
| Rows since `CUTOFF`: tagged / cite a test | 13 / 9 | 21 / 80 | 10 / 14 | 1 / 0 |
| Supersessions the guard acts on | 1 | 35 | 4 | 0 |
| …that name a date carrying several rows | 1 | 28 | 4 | 0 |
| Files the citation guard scans | 28 | 284 | 42 | 27 |
| Citations reaching its checks | 291 | 3,468 | 304 | 138 |
| …where the section check ran | 0 | 143 | 0 | 0 |
| …where the handoff-path check ran | 0 | 9 | 0 | 0 |
| Citations hidden by the one before (F1) | 47 | 362 | 30 | 17 |
| Citations skipped as quoted (F3), of which in `.py` | 66, 61 | 147, 115 | 69, 68 | 61, 61 |
| Citations in tracked files never opened (F4) | 49 | 319 | 45 | 32 |
| Warnings | 64 | 18 | 14 | 28 |

CI history, `tests.yml`: 171 runs in the template, 1,000 listed in tax-viz
(the listing cap; 2026-09-04 to 2026-11-10), 116 in alberta, 26 in
permit-speed. Seven failed. Six failed at pytest. One failed at "Check doc
citations" (alberta, 2026-09-26). "Check decisions log" has never failed.
Sessions run the guards before the PR (change pipeline step 1.5) and nothing
logs those runs, so this counts CI only.

## Already known: is the status right?

- **"Neither has a test file of its own."** True in the template. tax-viz has
  both: `tests/test_check_decisions_log.py` (17 tests) and
  `tests/test_check_doc_citations.py` (15). `docs/FINDINGS_harvest.md` Tier 1
  #1 said so on 2026-09-29; it is still unported under TODO A.
- **"`check_doc_citations.py` is only run by another test."** No test runs it.
  The one mention in `tests/` writes an empty file with that name. Proof: with
  `check_citations` returning nothing, pytest still reports 95 passed.
- **55 warnings.** 64 at `f6bb0f9`. Seven of them say a skill file "does not
  exist"; it exists under `.claude/skills/`, where the guard doesn't look. In
  tax-viz 11 of 18 warnings are false in the same way.
- **P1 (backticked `§N`, `§"title"`).** Still open, and the scope is right:
  don't widen it past the backtick. In tax-viz 619 of the 665 unchecked `§N`
  have only a backtick between the name and the `§`. Of the other 46, at least
  6 are another doc's section that happens to follow (F1's mirror image).
  What P1 would turn red today: for `§"title"`, two lines in the template,
  both the known out-of-repo path, and none of alberta's 57, permit-speed's 10
  or tax-viz's 6. For backticked `§N`, one in tax-viz (a `§2.2` that names a
  numbered step, not a heading) and one in the template (the dead example
  `docs/FINDINGS_enforced_claims.md` quotes on purpose).
- **T1 (`glob` misses nested tests).** Also breaks `check_assumptions.py`,
  which imports `known_tests`. `FINDINGS_harvest.md` Tier 1 #5 is the same
  family: tests outside the three hardcoded places (inputs E2, E9).
- **"Names a test that exists, not that it tests the decision."** Unchanged.
  One variant: a row passes by citing `check_decisions_log.py` itself (D14).
  `check_assumptions.py` refuses format guards as proof (`NOT_PROOF`); this
  guard has no such list.

## L0. Is each check worth gating a merge on?

**Decisions log: CONDITIONAL.** The docstring claims only "the question asked
at write time", and the README says the same. Sharpest argument against: where
the answer is a self-applied tag most of the time (13 of 21 in the template,
10 of 24 in alberta), the gate certifies a label. Where it is not (tax-viz, 80
of 97 cite a test), no file shows whether the gate caused the test. What would
change the verdict: a count of rows where the rule made someone write a test.
Not in any file; not asked.

**Doc citations: CONDITIONAL.** The line-number ban is decidable and tax-viz's
history justifies it. The other half, "citations resolve", checked nothing in
the template, alberta or permit-speed: their 84 `§"title"` pointers are never
checked, and they hold no live `§N`. There the guard is a line-number ban
that has gone red once, wrongly (F5). What would change the verdict: P1.

## L1. Citation guard: what passes while wrong

**F1. One citation hides the next.** The pattern consumes 40 characters after
each doc name, so a second name inside that tail is never examined.

    See README.md and quirks.md:207.          exit 0   (quirks.md alone: exit 5)
    [quirks.md](../data/quirks.md#L207)       exit 0
    README.md and spec.md §9                  exit 0

Hidden citations: 47 of 338 in the template, 362 of 3,830 in tax-viz, 30 of
334 in alberta, 17 of 155 in permit-speed. In tax-viz they include 6 bare `§N`
the guard would otherwise check and 69 backticked ones P1 would. All resolve
today. Fix: read the tail with a lookahead.

**F2. Exclusion is a substring test on the absolute path.** `.git` is a
substring of `.github`, so `.github/` is never scanned though `SCAN_DIRS`
lists it: `tests.yml` is dropped in all four repos, and tax-viz's four other
workflows with it. `_site` drops tax-viz's `scripts/build_site.py` (its fork
has the same line). A
checkout folder named `my_site` or `owner.github.io` scans zero files and
prints the same OK line (C5c, C5d; CLI exit 0). Fix: match path components
under the root, print the file and citation counts, fail on zero files.

**F3. Anything after an odd number of double quotes is a "mention".** That
rule exists so prose can quote the banned form. It also skips every citation
inside a string literal, a quote that wraps a line, or a line with an inch
mark (C4a–C4d). In the three template-born repos 190 of 196 skipped citations
are in `.py` files. In tax-viz 31 of the skipped are `§N` pointers, among
them ones a script prints into a report, which a reader actually sees. All
resolve today. The handoff-path check has the same exemption (C16).

**F4. Tracked files the guard never opens.** `.claude/` (skills), `tests/`,
`notebooks/`, `web/`, `.githooks/`, root files other than three, and the
suffixes `.sh`, `.jinja`, `.txt`. The template has 28 such files holding 49
citations, 17 of them in skills, which sessions follow as instructions.
tax-viz has 148 holding 319. None would fail today except lines that quote the banned form.

## L1. Decisions guard: what passes while wrong

**F7. A row whose date cell doesn't parse skips the test rule.** `when` is
`None`, and the rule only applies to a parsed date on or after `CUTOFF`.

    | Nov 11, 2026 | **New, no test, no tag.** | p |     exit 0
    | **2026-11-11** | **New, no test, no tag.** | p |   exit 0
    | **New, no test.** | 2026-11-11 | p |              exit 0
    | 2025-11-11 | **New, year typo, no test.** | p |    exit 0

No row below the first post-`CUTOFF` row is undated or older in any of the
four logs, so nothing has slipped through. tax-viz pins "month-only dates are
grandfathered" in a test, for its old rows. Fix: below the first
post-`CUTOFF` row, a row without a full date fails, and so does a date
earlier than the row above.

**F8. A supersession is recognised by five verbs in one word order.** 22
wordings pass with the old row unmarked (D8): "Replaces", "Withdraws",
"Corrects", "Reversing", "The 2026-10-01 row is superseded", "Supersedes the
previous row", a target named by topic, a target more than eight words after
the verb, an announcement in the pointer cell. In tax-viz:

- Four rows reverse, correct or withdraw part of the row above in words the
  guard misses, and the row above carries no mark: the 2026-08-28 loading-text
  row ("deliberately reversing the same-day row above"), two 2026-09-01 rows
  ("SCOPE CORRECTION to the row above", "WITHDRAWS the load finding in the row
  above"), and the 2026-09-15 row ("the earlier row's … are corrected here").
  I read the announcing phrase and the start of each row above, not the full
  rows. They are candidates for tax-viz to confirm.
- Three more were announced in unseen wording and marked anyway ("amending
  the 2026-09-20 row's", "amends this morning's … row", and the second date
  in "Reopens the 2026-09-21 and 2026-09-22 rows"). Of 36 dated marks in the
  log, the guard sees the announcement behind 31.

**F9. The target is "any row of that date".** An announcement passes when any
one row carrying the named date is marked. 28 of tax-viz's 35 announcements
name a date with several rows (median 4, up to 10); alberta's 4 name dates
with 3 to 7. Any `~~` in the target also counts as a mark, so one struck
clause from an earlier amendment satisfies a later full supersession (D6, D7).
No real miss found: the one doubled case in tax-viz (two 2026-07-28 rows)
points at one row, which is marked.

**F10. An unescaped pipe cuts the row.** `cells()` says it handles a pipe
inside inline code; it handles only `\|`. Everything after the pipe is
unchecked: a dangling test ID and a supersession both pass (D3). Four tax-viz
rows are cut this way; one hides a test ID (it exists). The false-alarm side
is E8.

**F13. Two header claims no guard backs.** The `docs/DECISIONS.md` header,
shipped to every project, says "EVERY ROW CARRIES A POINTER TO A DOC" and
that the citation guard "checks that every pointer resolves". A row with an
empty pointer cell passes both guards (D9). Four tax-viz rows dated
2026-10-12 to 2026-10-14 have no third cell. The second claim is true of no
pointer in the template's own log until P1 lands.

## L2. What fails while right

**F5. The line-number ban fires on ordinary prose.** `lines?` has no word
boundary and may sit 12 characters after the name; a colon followed by any
digits counts.

    quirks.md: 14 columns documented.         exit 5
    quirks.md baseline 2021 figures.          exit 5
    quirks.md has guidelines 3 and 4.         exit 5

This is the one time either guard went red in CI. Alberta's line read:
"see `DECISIONS.md`. FIR lines 1912/1922", where the numbers are FIR line codes.
Commit `6ef5af5` fixed it by rewording the prose. Fix: `\blines?`, and a colon
form with no space.

**F11. Decisions guard false alarms** (none present in the four logs today):

    | 2026-11-11 | **Hold out 20%: `test_size=0.2`.** [unverifiable] | p |
        cites `test_size`, which does not exist
    | 2026-11-11 | **New.** tax-viz retracted its report 2026-11-10. [unverifiable] | p |
        supersedes 2026-11-10 (L3) but none of those rows is marked — strike it
    | 2026-11-11 | **Hook matcher stays `Read|Grep|Glob`.** [unverifiable] | p |
        names no test (the tag sits after the pipe)

The second is the costly one: obeying the message marks an unrelated row
SUPERSEDED. Also: a struck row whose test was deleted with the decision fails
until history is edited (E5); a test name with a capital, or an `async def`
test, can't be cited (E3, E4).

## L3. Code

**F6. Citation guard, smaller.** (a) A doc with an ordinary lowercase name
turns that word into a citation everywhere: "both methods: 2 passes" fails
when `docs/methods.md` exists (A3, A4), and the word hides what follows it
(C1d). No template-born repo has a lowercase doc; tax-viz has three. (b) Docs
are keyed by basename, so a second README under `docs/` replaces the root one
(C7). No collision exists in the four repos. (c) A `# 9 retries` comment in a
fenced block counts as section 9 (C8). (d) `errors="ignore"` drops a Latin-1
`§`, so the citation is never seen (C13). (e) Spellings the ban misses: `L207`,
`(L207)`, `:L207`, `:~207`, a backtick before the colon (C10). I searched the
four repos for them and found none in use.

**F12. Decisions guard, smaller.** (a) The OK line reports no counts, and a
log the parser reads zero rows from prints it too: a bullet-list log, an
indented table, a UTF-16 file (D10, D11; CLI exit 0). (b) An impossible date
such as 2026-02-30 is a `ValueError` traceback, exit 1, not exit 6. (c)
`CUTOFF` lives in a copier-delivered script. alberta, permit-speed, civic-map
and drive-landscape carry the template's date and all postdate it. regenx, a hand-port, moved it and
marked the line. A project that adopts with an older log has to fork a
shipped file. (d) `def test_x` inside a string fixture counts as a test (D5).

**F14. Tests.** In a scratch clone at `f6bb0f9`: `check_citations` made to
return nothing, 95 passed; both decision checks made to return nothing, 95
passed; `known_tests` made to return an empty set, 1 failed (through
`check_assumptions.py`). So the shared helpers are covered indirectly and the
two guards' own checks are not covered at all. tax-viz's 32 tests call both
checks directly (read, not run here). Three of them pin a hole above as
intended: a quoted
citation is a mention (F3), a missing doc only warns (P1), a month-only date
is grandfathered (F7).

## Fix order proposed (TODO W; nothing is fixed in this PR)

1. Port tax-viz's two test files unchanged, then add the appendix inputs.
2. Citation guard, with P1: F1 lookahead, F2 path components and counts, F5
   word boundary. Then decide F3 and F4 (plan first).
3. Decisions guard, with T1: F7, F12 (a) and (b), F10.
4. F8 and F9 are the owner's call: a wider verb list raises F11's false
   alarms, and a fixed token in the announcing row changes how rows are written.
5. F13: reword the header sentence, or leave it for P1.
6. For `edmonton-tax-viz`, in its own repo: the four F8 rows, the F2 files its
   fork never scans, the F13 rows, and the one `§2.2` P1 will turn red.

## Not checked

- **Local runs.** Whether a guard has stopped a wrong row or citation before
  a push. Nothing records it.
- **tax-viz's forks.** I ran the template's scripts on its tree. Its copies
  differ in docstrings, in `SCAN_FILES`, and may differ in behaviour.
- **The other template projects** (civic-map, drive-landscape,
  open-data-landscape, data-science-study, nonprofit-map, the filter-bubble
  project). The brief named three.
- **Whether sessions reword prose to satisfy a guard.** One commit says so
  (`6ef5af5`); a search of commit messages can't see the rest.
- **Whether the F8 rows are full supersessions.** See F8.

## What this run got wrong

- **Renaming my fixture flipped a baseline.** I renamed the probe's citing
  file to `docs/notes.md` to keep this doc free of new warnings. It then
  counted as a project doc, the word "notes" in one input became a citation,
  and its tail hid the line-number form after it: a baseline went from fail
  to pass. That is F1 and F6 (a) in my own instrument. I noticed only because
  the total moved from 111 to 112. It is now its own input (C1d).
- **One false-alarm input passed for the wrong reason.** It cited a doc my
  fixture didn't contain, so the guard never saw a citation. For one run it
  read as "no false alarm here".
- **My re-implementation attached a section to the wrong doc.** To count
  hidden citations I rewrote the matcher, with a looser `§` search. It called
  two hidden tax-viz citations dead; both were another doc's `§`. I was about
  to recommend widening P1 the same way. The headline zero (section check ran
  on 0 citations) comes from counting inside the guard's own code instead.
- **I took the brief's "no test file" as covering tax-viz.** I found its 32
  tests while diffing the forks, after writing the probes, and then found
  that `FINDINGS_harvest.md` had said so six weeks ago. That doc was not in
  the brief's grounding order, and I didn't look.
- **An exit code read through a pipe.** My first run printed `tail`'s status,
  not the guard's. No claim used it; exit codes here are from direct runs.
- **A mutation that never applied.** A fourth mutation (splitting cells on
  every pipe) didn't match the source text, and pytest passed on an unchanged
  file. It is not reported as a result.
- **The F8 rows rest on partial reads.** The skill says to read decision
  rows in full; for another repo's 391-row log I read phrases. Hence
  "candidates".
- **This file failed the citation guard twice, both false alarms it
  describes.** The alberta quote wrapped a line, so it stopped counting as a
  mention (F3) and "FIR lines" fired again (F5); and one appendix input used
  the real README's name before a colon and a digit. I reworded both to get
  green, which is the habit F5 says the guard teaches.

## Appendix: the inputs

Each line is one input and what the guard did. Decision rows sit under the
standard three-column header; `p` stands for any pointer cell; `OLD` is the
row `| 2026-10-01 | **Old rule.** [unverifiable] | p |`; `test_real` and
`scripts/check_real.py` exist. Citation inputs are one line in `docs/log.md`
unless a file is named; the repo holds `docs/spec.md` (sections 1 and 2),
`data/quirks.md` and a README. Three inputs are described, not quoted,
because the literal text would trip the citation guard in this file.
`[known]` marks inputs already covered by P1, T1 or the harvest findings;
`[by design]` marks one the header asks for.

**Baselines: the guard does the right thing (15)**

```
D0a     | 2026-11-11 | **New.** | p |   -> fails
D0b     | 2026-11-11 | **New.** `test_real` | p |   -> exit 0
D0c     | 2026-11-11 | **New.** `test_gone` | p |   -> fails
D0d     | 2026-11-11 | **New.** [unverifiable] | p |   -> exit 0
D0e     OLD + | 2026-11-11 | Supersedes the 2026-10-01 row. [unverifiable] | p |   -> fails
D0f     same, old row carries SUPERSEDED 2026-11-11   -> exit 0
D1.7    | 2026-11-11 (S14) | **New, no test, no tag.** | p |   -> fails
D1.8    |  2026-11-11 | **New, no test, no tag.** | p |   -> fails
C0a     docs/log.md: See spec.md §9.   -> fails
C0b     docs/log.md: See spec.md §2.   -> exit 0
C0c     docs/log.md: See quirks.md:207.   -> fails
C0d     docs/log.md: See quirks.md line 207.   -> fails
C2b     [the data notes](../data/quirks.md#L207)   -> fails
C10.7   quirks.md, around line 207   -> fails
C10.11  quirks.md §207   -> fails
```

**Decisions log: exits 0, should fail (40)**

```
D1.0    | Nov 11, 2026 | **New, no test, no tag.** | p |
D1.1    | **2026-11-11** | **New, no test, no tag.** | p |
D1.2    | 2026-11 | **New, no test, no tag.** | p |
D1.3    |  | **New, no test, no tag.** | p |
D1.4    | 11/11/2026 | **New, no test, no tag.** | p |
D1.5    | S14 | **New, no test, no tag.** | p |
D1.6    | ~~2026-11-11~~ | **New, no test, no tag.** | p |
D1.9    | **New, no test.** | 2026-11-11 | p |  (date in the wrong cell)
D2      | 2026-11-10 | ok [unverifiable] | p |  ⏎  | 2025-11-11 | **New, year typo, no test.** | p |
D3      OLD + | 2026-11-11 | `test_real` holds; matcher `Read|Grep` now supersedes the 2026-10-01 row; see `test_gone` | p |
D5      row cites `test_ghost`; tests/test_a.py holds it only inside a string fixture
D6      target row has one clause struck (~~x~~); new row supersedes the whole row; no mark
D7      two 2026-10-01 rows, A marked SUPERSEDED 2026-11-11 by an earlier 11-11 row; a second 11-11 row supersedes B; B unmarked
D8.0    OLD + | 2026-11-11 | Replaces the 2026-10-01 row. [unverifiable] | p |
D8.1    OLD + | 2026-11-11 | Overrides the 2026-10-01 row. [unverifiable] | p |
D8.2    OLD + | 2026-11-11 | Overturns the 2026-10-01 row. [unverifiable] | p |
D8.3    OLD + | 2026-11-11 | Withdraws the 2026-10-01 row. [unverifiable] | p |
D8.4    OLD + | 2026-11-11 | Revokes the 2026-10-01 row. [unverifiable] | p |
D8.5    OLD + | 2026-11-11 | Undoes the 2026-10-01 row. [unverifiable] | p |
D8.6    OLD + | 2026-11-11 | Corrects the 2026-10-01 row. [unverifiable] | p |
D8.7    OLD + | 2026-11-11 | Updates the 2026-10-01 row. [unverifiable] | p |
D8.8    OLD + | 2026-11-11 | The 2026-10-01 row is superseded. [unverifiable] | p |
D8.9    OLD + | 2026-11-11 | The 2026-10-01 row is retracted. [unverifiable] | p |
D8.10   OLD + | 2026-11-11 | The 2026-10-01 row no longer holds. [unverifiable] | p |
D8.11   OLD + | 2026-11-11 | This will supersede the 2026-10-01 row. [unverifiable] | p |
D8.12   OLD + | 2026-11-11 | Reversing the 2026-10-01 row. [unverifiable] | p |
D8.13   OLD + | 2026-11-11 | Retracting the 2026-10-01 row. [unverifiable] | p |
D8.14   OLD + | 2026-11-11 | A reversal of the 2026-10-01 row. [unverifiable] | p |
D8.15   OLD + | 2026-11-11 | An amendment to the 2026-10-01 row. [unverifiable] | p |
D8.16   OLD + | 2026-11-11 | Supersedes the old-rule row. [unverifiable] | p |
D8.17   OLD + | 2026-11-11 | Supersedes the previous row. [unverifiable] | p |
D8.18   OLD + | 2026-11-11 | Supersedes the earlier decision. [unverifiable] | p |
D8.19   OLD + | 2026-11-11 | Supersedes, after the owner asked alberta and tax-viz and permit-speed once more, the 2026-10-01 row. [unverifiable] | p |
D8.20   OLD + | 2026-11-11 | Supersedes the 1 October row. [unverifiable] | p |
D8.x    OLD + | 2026-11-11 | **New.** [unverifiable] | Supersedes the 2026-10-01 row; p |
D9      | 2026-11-11 | **New.** [unverifiable] |  |   (empty pointer cell; header says EVERY ROW CARRIES A POINTER)
D10a    log as a bullet list: - 2026-11-11: **New, no test.**
D10b    table rows indented two spaces
D11     DECISIONS.md saved as UTF-16, one new row with no test
D14     | 2026-11-11 | **New.** Enforced by `check_decisions_log.py`. | p |  (the guard cites itself)  [known]
```

**Decisions log: fails, should pass (11); the last crashes instead of exiting 6 (1)**

```
E1      | 2026-11-11 | **Hold out 20%: `test_size=0.2`.** [unverifiable] | p |
E2      | 2026-11-11 | **Links.** `tools/check_links.py` | p |  (tools/check_links.py exists)  [known]
E3      | 2026-11-11 | **CRS.** `test_area_uses_EPSG3776` | p |  (the test exists)
E4      | 2026-11-11 | **Fetch.** `test_fetch` | p |  (async def test_fetch exists)
E5      | 2026-10-01 | ~~**Old rule.** `test_old_rule`~~ SUPERSEDED 2026-11-11 | p | + successor; test_old_rule deleted with the rule
E6a     | 2026-11-10 | **Innocent.** [unverifiable] | p |  ⏎  | 2026-11-11 | **New.** tax-viz retracted its report 2026-11-10. [unverifiable] | p |
E6b     | 2026-11-11 | **New.** The owner reversed the plan 2026-11-11. [unverifiable] | p |
E7      | 2026-11-11 | **New.** | [unverifiable] p |  (tag in the pointer cell)
E8      | 2026-11-11 | **Hook matcher stays `Read|Grep|Glob`.** [unverifiable] | p |
E9      | 2026-11-11 | **Page loads.** `verify-load.js` | p |  (web/tests/verify-load.js exists)  [known]
E10     | 2026-02-30 | **Typo date.** [unverifiable] | p |
E11     old row marked lower-case: superseded 2026-11-11  [by design]
```

**Doc citations: exits 0, should fail (50)**

```
C1a     See README.md and quirks.md:207.
C1b     Read `docs/spec.md`, then `data/quirks.md` line 207.
C1c     README.md and spec.md §9
C2a     [spec.md](spec.md) §9
C1d     a doc named docs/notes.md exists; log.md: [the data notes](../data/quirks.md#L207)
C2c     [quirks.md](../data/quirks.md#L207)
C3.0    spec.md, §9
C3.1    spec.md (§9)
C3.2    **spec.md** §9
C3.3    spec.md's §9
C3.4    spec.md: §9
C3.5    spec.md at §9
C3.6    spec.md §1 and §9
C3.7    spec.md §§1, 9
C3.8    spec.md — §9
C3.9    `spec.md` §9  [known]
C4a     He said "check it  ⏎  later" and cited quirks.md:207.   (quote wraps a line)
C4b     scripts/x.py: raise SystemExit("see quirks.md:207")
C4c     The 6" pipe rule is in quirks.md:207.
C4d     docs/ci.yml: run: echo "see spec.md §9"
C5a     docs/web_site_plan.md: See quirks.md:207.
C5b     .github/workflows/x.yml: # see quirks.md:207
C5c     checkout folder named my_site; docs/log.md: See quirks.md:207.
C5d     checkout folder named owner.github.io; docs/log.md: See quirks.md:207.
C6.0    .claude/skills/x/steps.md: see quirks.md:207
C6.1    tests/test_x.py: see quirks.md:207
C6.2    web/index.html: see quirks.md:207
C6.3    notebooks/n.md: see quirks.md:207
C6.4    bootstrap.sh: see quirks.md:207
C6.5    docs/notes.txt: see quirks.md:207
C6.6    docs/x.md.jinja: see quirks.md:207
C6.7    src/x.R: see quirks.md:207
C6.8    CONTRIBUTING.md: see quirks.md:207
C6.9    .githooks/pre-push: see quirks.md:207
C8      spec.md holds a fenced bash block with '# 9 retries'; log.md: spec.md §9
C10.0   quirks.md L207
C10.1   quirks.md, l. 207
C10.2   quirks.md ln 207
C10.3   quirks.md (L207)
C10.4   quirks.md:~207
C10.5   quirks.md @207
C10.6   `quirks.md`:207
C10.8   quirks.md:L207
C10.9   quirks.md row 207
C10.10  quirks.md#207
C11     docs/specs/fire.md exists (## 1. One); log.md: fire.md §9
C12     methods.md §3  (no such doc anywhere)  [known]
C13     log.md saved as Latin-1: See spec.md §9.
C16     (described) one unclosed double quote, then the path of a handoff file that does not exist
C7b     (described) the reverse: only the README under docs/ has '## 9. Nine'; TODO cites section 9 of the root README
```

**Doc citations: fails, should pass (10)**

```
C7a     (described) root README has a heading '## 9. Nine', a second README under docs/ has none; TODO cites section 9 of README
A1.0    quirks.md: 14 columns documented.
A1.1    quirks.md: 2026-11-11 refreshed.
A1.2    quirks.md baseline 2021 figures.
A1.3    quirks.md has guidelines 3 and 4.
A1.4    quirks: 3 open questions.
A1.5    quirks.md outlines 2 joins.
A1.6    See quirks.md for deadlines 2026 onward.
A3      docs/methods.md exists; src/x.py: # both methods: 2 passes each
A4      docs/methods.md exists; log.md: the methods section 4 of the paper
```
