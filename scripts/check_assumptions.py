"""Assumptions-index guard: every row is well-formed, and a VERIFIED row names a real test.

``docs/ASSUMPTIONS.md`` lists the premises a published number rests on that no
guard proves. An index nobody checks drifts. Every list in the source project
that wasn't executed or tested did, so this checks the part that is mechanical:

  1. **A STATUS FROM THE FOUR.** The status cell starts with VERIFIED, SUPPORTED,
     UNVERIFIED or ACCEPTED. A qualifier may follow ("SUPPORTED (2025 only)").
  2. **VERIFIED MEANS A TEST THAT EXISTS.** A VERIFIED row cites ``test_x`` /
     ``verify-x.js`` / ``check_x.py`` that resolves, by the same rule as
     ``check_decisions_log.py``. A renamed or deleted test otherwise leaves the
     row claiming a proof that is gone.
  3. **A SIZE ON EVERY UNPROVEN ROW.** Ranking audit targets needs one, even if
     it says "unknown" or points at the notebook that computes it.
  4. **AN EVIDENCE POINTER ON EVERY ROW, AND IDs UNIQUE.** Whether a ``.md``
     pointer resolves is ``check_doc_citations.py``'s job; it scans this doc.

⚠️ It does NOT check that the index is complete: that a premise in the project's
own registers (a notebook's sized rows, a ``confidence`` field in a data file)
has a row here. Those registers differ per project, so each project writes that
test itself. Nor does it check that a row is TRUE.

Columns are found by header name, so a project may add its own (``Build``,
``Lens``) and split the index into several tables. A table counts as part of the
index when its header has a ``Status`` column. A missing doc passes.

Exit codes: 0 ok; 8 a row fails a check (2 is argparse's).

Usage:
    python scripts/check_assumptions.py
    python scripts/check_assumptions.py --root /path/to/checkout
"""

import argparse
import re
import sys
from pathlib import Path

from check_decisions_log import TEST_ID, known_tests

ROOT = Path(__file__).resolve().parent.parent
ASSUMPTIONS = "docs/ASSUMPTIONS.md"

EXIT_OK = 0
EXIT_FAIL = 8

STATUSES = ("VERIFIED", "SUPPORTED", "UNVERIFIED", "ACCEPTED")
# Header names seen in the projects using the index: "If wrong (rough size)", "Size".
SIZE = re.compile(r"size|if wrong", re.I)
EVIDENCE = re.compile(r"evidence", re.I)
SEPARATOR = re.compile(r"^\|\s*:?-{3,}")


def cells(line: str) -> list[str]:
    """Split on unescaped ``|`` only, as check_decisions_log does."""
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def tables(md: str) -> list[tuple[int, list[str], list[tuple[int, list[str]]]]]:
    """Each markdown table as (header lineno, header cells, [(lineno, cells)])."""
    found, block = [], []
    for lineno, line in enumerate(md.splitlines() + [""], 1):
        if line.startswith("|"):
            block.append((lineno, line))
            continue
        if len(block) >= 2 and SEPARATOR.match(block[1][1]):
            found.append((block[0][0], cells(block[0][1]), [(n, cells(l)) for n, l in block[2:]]))
        block = []
    return found


def column(header: list[str], pattern: re.Pattern) -> int | None:
    return next((i for i, h in enumerate(header) if pattern.search(h)), None)


def check(root: Path = ROOT) -> list[str]:
    path = root / ASSUMPTIONS
    if not path.is_file():
        return []
    tests = known_tests(root)
    failures: list[str] = []
    seen: dict[str, int] = {}
    for head_no, header, rows in tables(path.read_text(errors="ignore")):
        status_col = column(header, re.compile(r"^\W*status", re.I))
        if status_col is None:
            continue
        size_col, ev_col = column(header, SIZE), column(header, EVIDENCE)
        for name, col in (("size (\"If wrong\" or \"Size\")", size_col), ("evidence", ev_col)):
            if col is None:
                failures.append(f"{ASSUMPTIONS}:{head_no}  table has no {name} column")
        for lineno, row in rows:
            where = f"{ASSUMPTIONS}:{lineno}"
            get = lambda i: row[i] if i is not None and i < len(row) else ""  # noqa: E731
            rid = get(0)
            if rid in seen:
                failures.append(f"{where}  ID `{rid}` already used on line {seen[rid]}")
            seen.setdefault(rid, lineno)
            word = re.match(r"\W*([A-Z]+)", get(status_col))
            status = word.group(1) if word else ""
            if status not in STATUSES:
                failures.append(f"{where}  status `{get(status_col)}` is not one of {', '.join(STATUSES)}")
            if status == "VERIFIED":
                text = " ".join(row)
                cited = {c for c in TEST_ID.findall(text) if c in tests or c + ".py" in tests}
                if not cited:
                    failures.append(f"{where}  VERIFIED but names no existing test (test_x / verify-x.js / check_x.py)")
            elif size_col is not None and not get(size_col).strip("—- "):
                failures.append(f"{where}  {status or 'row'} with no size: say roughly what moves if it's wrong, or \"unknown\"")
            if ev_col is not None and not get(ev_col).strip("—- "):
                failures.append(f"{where}  no evidence pointer")
    return failures


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", type=Path, default=ROOT)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    failures = check(args.root)
    for f in failures:
        print(f"FAIL  {f}")
    if failures:
        print(f"\n{len(failures)} failure(s) in {ASSUMPTIONS}")
        return EXIT_FAIL
    print(f"OK  {ASSUMPTIONS}: every row has a known status, a size and a pointer; "
          f"every VERIFIED row names a test that exists")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
