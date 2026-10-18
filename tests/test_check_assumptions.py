"""Tests for scripts/check_assumptions.py: a malformed index row fails the gate."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check_assumptions as ca  # noqa: E402

HEADER = ("| ID | Assumption | Status | If wrong (rough size) | Evidence and test |\n"
          "|----|------------|--------|-----------------------|-------------------|\n")


def _repo(tmp_path, rows: str, header: str = HEADER, tests: str = ""):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "ASSUMPTIONS.md").write_text("# Assumptions index\n\n" + header + rows)
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_x.py").write_text(tests)
    return tmp_path


def test_this_repo_index_passes():
    assert ca.check(ca.ROOT) == []


def test_missing_doc_passes(tmp_path):
    assert ca.check(tmp_path) == []


def test_good_rows_pass(tmp_path):
    repo = _repo(tmp_path,
                 "| A1 | x | SUPPORTED (2025 only) | one year | `data/DATA.md` |\n"
                 "| A2 | y | **VERIFIED** | — | `test_year_rule` |\n",
                 tests="def test_year_rule():\n    pass\n")
    assert ca.check(repo) == []


def test_unknown_status_fails(tmp_path):
    failures = ca.check(_repo(tmp_path, "| A1 | x | PROBABLY | small | `data/DATA.md` |\n"))
    assert len(failures) == 1 and "PROBABLY" in failures[0] and "ASSUMPTIONS.md:5" in failures[0]


def test_verified_row_needs_real_test(tmp_path):
    failures = ca.check(_repo(tmp_path, "| A1 | x | VERIFIED | — | `test_renamed_away` |\n"))
    assert len(failures) == 1 and "names no existing test" in failures[0]


def test_unproven_row_needs_size(tmp_path):
    failures = ca.check(_repo(tmp_path, "| A1 | x | UNVERIFIED |  | `data/DATA.md` |\n"))
    assert len(failures) == 1 and "no size" in failures[0]


def test_row_needs_evidence(tmp_path):
    failures = ca.check(_repo(tmp_path, "| A1 | x | ACCEPTED | 0.1 pp | — |\n"))
    assert len(failures) == 1 and "no evidence" in failures[0]


def test_repeated_id_fails_across_tables(tmp_path):
    other = ("\n## Second table\n\n| # | Premise | Status | Size | Build | Evidence |\n"
             "|---|---|---|---|---|---|\n| A1 | z | ACCEPTED | 03 | public | `a.md` |\n")
    failures = ca.check(_repo(tmp_path, "| A1 | x | ACCEPTED | small | `b.md` |\n" + other))
    assert len(failures) == 1 and "already used on line 5" in failures[0]


def test_extra_columns_found_by_name(tmp_path):
    header = "| # | Lens | Premise | Status | Size | Build | Evidence |\n|---|---|---|---|---|---|---|\n"
    assert ca.check(_repo(tmp_path, "| B1 | Money | x | UNVERIFIED | unknown | full | `a.md` |\n",
                          header=header)) == []


def test_table_without_size_column_fails(tmp_path):
    header = "| ID | Assumption | Status | Evidence |\n|---|---|---|---|\n"
    failures = ca.check(_repo(tmp_path, "| A1 | x | ACCEPTED | `a.md` |\n", header=header))
    assert failures == ["docs/ASSUMPTIONS.md:3  table has no size (\"If wrong\" or \"Size\") column"]


def test_table_without_status_is_not_index(tmp_path):
    header = "| Term | Meaning |\n|---|---|\n"
    assert ca.check(_repo(tmp_path, "| A1 | anything |\n", header=header)) == []
