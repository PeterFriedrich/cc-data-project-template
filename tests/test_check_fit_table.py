"""Tests for scripts/check_fit_table.py: a template update can't silently drop fit-table rows."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check_fit_table as cf  # noqa: E402

HEADER = "| Stage | Step | This project |\n|---|---|---|\n"


def _row(step: str, answer: str = "adopted: habit", stage: str = "") -> str:
    return f"| {stage} | {step} | {answer} |\n"


def _repo(tmp_path, body: str, tail: str = "\n## After\n\ntext\n"):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "CHANGE_PIPELINE.md").write_text(
        "# Change pipeline\n\n## This project's fit\n\nIntro.\n\n" + HEADER + body + tail)
    return tmp_path


def _all(answer: str = "adopted: habit") -> str:
    return "".join(_row(s, answer) for s in cf.FIT_STEPS)


def test_template_table_matches_fit_steps():
    """A PR that adds, renames or drops a fit row must update FIT_STEPS too."""
    rows = cf.fit_rows((cf.ROOT / cf.PIPELINE).read_text())
    assert [r[1] for _, r in rows] == cf.FIT_STEPS


def test_this_repo_passes():
    failures, unanswered = cf.check(cf.ROOT)
    assert failures == [] and unanswered == len(cf.FIT_STEPS)


def test_missing_doc_passes(tmp_path):
    assert cf.check(tmp_path) == ([], 0)


def test_answered_table_passes(tmp_path):
    assert cf.check(_repo(tmp_path, _all())) == ([], 0)


def test_not_evaluated_is_counted_not_failed(tmp_path):
    assert cf.check(_repo(tmp_path, _all("not evaluated"))) == ([], len(cf.FIT_STEPS))


def test_project_rows_are_allowed(tmp_path):
    failures, _ = cf.check(_repo(tmp_path, _all() + _row("Our own step", "adopted: `tests.yml`")))
    assert failures == []


def test_missing_row_fails(tmp_path):
    """Keeping the project's side of the conflict drops the template's new rows."""
    failures, _ = cf.check(_repo(tmp_path, "".join(_row(s) for s in cf.FIT_STEPS[1:])))
    assert len(failures) == 1 and cf.FIT_STEPS[0] in failures[0] and "missing" in failures[0]


def test_repeated_row_fails(tmp_path):
    failures, _ = cf.check(_repo(tmp_path, _all() + _row(cf.FIT_STEPS[3])))
    assert len(failures) == 1 and "repeats" in failures[0]


def test_empty_answer_fails(tmp_path):
    body = _all().replace(_row(cf.FIT_STEPS[2]), _row(cf.FIT_STEPS[2], ""))
    failures, _ = cf.check(_repo(tmp_path, body))
    assert len(failures) == 1 and "no answer" in failures[0]


def test_unresolved_conflict_fails(tmp_path):
    """The shape copier produced on civic-map: both whole tables in one block."""
    body = "<<<<<<< before updating\n" + _all() + "=======\n" + _all("not evaluated") + ">>>>>>> after updating\n"
    failures, _ = cf.check(_repo(tmp_path, body))
    assert sum("conflict marker" in f for f in failures) == 2
    assert sum("repeats" in f for f in failures) == len(cf.FIT_STEPS)


def test_marker_outside_the_table_fails(tmp_path):
    failures, _ = cf.check(_repo(tmp_path, _all(), tail="\n## After\n\n<<<<<<< before updating\nx\n"))
    assert len(failures) == 1 and "conflict marker" in failures[0]


def test_setext_underline_is_not_a_marker(tmp_path):
    failures, _ = cf.check(_repo(tmp_path, _all(), tail="\nTitle\n=======\n"))
    assert failures == []


def test_missing_section_fails(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "CHANGE_PIPELINE.md").write_text("# Change pipeline\n")
    failures, _ = cf.check(tmp_path)
    assert len(failures) == 1 and "no `## This project's fit`" in failures[0]


def test_another_sections_table_is_not_the_fit_table(tmp_path):
    """A fit section that lost its table must not borrow the next section's."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "CHANGE_PIPELINE.md").write_text(
        "## This project's fit\n\nIntro, table gone.\n\n## Other\n\n" + HEADER + _all())
    failures, _ = cf.check(tmp_path)
    assert len(failures) == len(cf.FIT_STEPS) and all("missing" in f for f in failures)
