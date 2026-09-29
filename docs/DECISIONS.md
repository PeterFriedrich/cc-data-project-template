# Decisions Index

Append-only. **One ROW per locked decision** — when, what, why (including what
was rejected), and a pointer to where the argument lives in full. When a decision
locks, add a row; when one is superseded, strike it (`~~...~~`) or mark it
`SUPERSEDED <date>` in place and add the successor — don't delete history.

**What a row owes you:**

1. ⚠️ **EVERY ROW CARRIES A POINTER TO A DOC** — not only to code. Code moves;
   the argument has to live somewhere prose can hold it.
   `scripts/check_doc_citations.py` checks that every pointer resolves.
2. **The row is a self-contained summary** and may paraphrase the argument.
3. **The pointer is the authority.** When a row and its target disagree, the
   target wins and the row gets fixed.
4. **A row names the test that protects it**, or carries `[unverifiable]`.
   `scripts/check_decisions_log.py` enforces this on the merge gate (and that a
   superseded row is marked where it stands).

| When | Decision | Full reasoning |
|------|----------|----------------|
| 2026-09-29 | **Template changes reach instances through copier; the template stays untagged** (owner, S03). New projects start with `copier copy`, not "Use this template"; the template's own ledgers ship as `.jinja` skeletons and its handoffs/findings are excluded, pinned by `test_render_carries_every_template_file_and_nothing_else`. Untagged so copier tracks HEAD — a tag would make every untagged change silently never arrive. `edmonton-tax-viz` stays out (a source, not an instance). Rejected: plugin distribution (cloud sessions don't install repo-declared plugins); a hand-rolled manifest + drift check; an `owner_name` question (the three-way merge keeps "Peter" edits, measured on an alberta dry run). | `docs/COPIER.md`; `docs/FINDINGS_harvest.md` §"C (sync direction): recommendation" |
| 2026-09-29 | **Claude web gets a brief generated from the repo, not a hand-written one** (owner, S03). `scripts/make_brief.py` builds it from `CLAUDE.md`, `docs/SCOPE.md`, `DECISIONS.md`, `TODO.md`, `DATA_ISSUES.md`; a public repo commits it as `docs/BRIEF.md` and syncs it into a private claude.ai Project, with `test_committed_brief_is_current` failing the gate when stale (falsified by `test_check_goes_red_when_a_source_changes`); a private repo pastes stdout, because the GitHub integration 404s on private repos (#98050). Deferred: `ingest_reply.py` (one call site). Rejected: the brief-less smallest slice for public repos, since the owner's main projects are public. | `docs/CLAUDE_WEB.md`; `docs/FINDINGS_harvest.md` §"D (spec sheet): recommendation" |
