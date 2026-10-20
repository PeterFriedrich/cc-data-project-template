"""Guards on what `copier copy` gives a new project (`copier.yml`, `docs/COPIER.md`).

This repo is the template AND a project with its own backlog, decisions and
handoffs. The render must carry every template file and none of that state:
a leak hands a new project someone else's open work as its own, and a drop
is a guard or doc the instance silently never gets.

Excluded from renders (`copier.yml`), since it tests this repo's copier config.
"""
import fnmatch
import subprocess
import sys
from pathlib import Path

import pytest

copier = pytest.importorskip("copier")

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import check_assumptions as ca  # noqa: E402 -- its table parser finds the ledger rows
import check_fit_table as cf  # noqa: E402

# This repo's own state: must never appear in a render.
OWN_STATE = ["session-summary/*.md", "docs/FINDINGS_*.md", "docs/BRIEF.md"]
# Template-only machinery: also absent from a render.
TEMPLATE_ONLY = ["copier.yml", "tests/test_copier.py"]
SUFFIX = ".jinja"


@pytest.fixture(scope="module")
def render(tmp_path_factory) -> Path:
    dst = tmp_path_factory.mktemp("instance")
    copier.run_copy(str(REPO), str(dst), defaults=True, unsafe=True, quiet=True)
    return dst


def _files(root: Path) -> set[str]:
    return {p.relative_to(root).as_posix() for p in root.rglob("*")
            if p.is_file() and ".git" not in p.relative_to(root).parts}


def _tracked() -> set[str]:
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                         cwd=REPO, capture_output=True, text=True, check=True)
    return {ln for ln in out.stdout.splitlines() if (REPO / ln).is_file()}


def test_render_carries_every_template_file_and_nothing_else(render):
    """Membership, both ways: what the repo holds, minus own state and template
    machinery, with each `.jinja` skeleton standing in for its plain sibling."""
    expected = set()
    for f in _tracked():
        if any(fnmatch.fnmatch(f, pat) for pat in OWN_STATE + TEMPLATE_ONLY):
            continue
        if f.endswith(SUFFIX):
            f = f[: -len(SUFFIX)]
            if "{{" in f:
                f = ".copier-answers.yml"
        expected.add(f)
    got = _files(render)
    assert not expected - got, f"missing from a new project: {sorted(expected - got)}"
    assert not got - expected, f"unexpected in a new project: {sorted(got - expected)}"


def test_ledgers_render_as_skeletons_not_this_repos_state(render):
    for name in ("TODO.md", "docs/DECISIONS.md", "docs/TODO_archive.md", "docs/AUDIT_LEDGER.md"):
        assert (render / name).read_text() == (REPO / f"{name}{SUFFIX}").read_text(), name
    assert "- [ ] <first item" in (render / "TODO.md").read_text()
    for name in ("docs/DECISIONS.md", "docs/AUDIT_LEDGER.md"):
        rows = [ln for ln in (render / name).read_text().splitlines() if ln.startswith("| 20")]
        assert rows == [], f"template's own rows leaked from {name}: {rows}"


@pytest.mark.parametrize("name", ["docs/ASSUMPTIONS.md", "docs/DATA_ISSUES.md"])
def test_unskeletoned_ledgers_stay_empty_in_the_template(render, name):
    """These two ship as the template's own file, with no `.jinja` skeleton,
    because the template publishes no number and reads no outside data. A row
    here would reach every new project (and, for DATA_ISSUES, every update)."""
    ledgers = [t for t in ca.tables((render / name).read_text()) if ca.column(t[1], ca.STATUS) is not None]
    assert ledgers, f"{name}: no table with a Status column; this test no longer finds the ledger"
    rows = [f"line {n}" for _, _, body in ledgers for n, _ in body]
    assert not rows, (f"{name} has rows ({', '.join(rows)}): give it a `{name}{SUFFIX}` skeleton "
                      "first, as docs/DECISIONS.md has, so the rows stay the template's own")


def test_render_records_where_it_came_from(render):
    """`copier update` reads `_commit`; without it an instance can never update."""
    answers = (render / ".copier-answers.yml").read_text()
    assert "_commit:" in answers and "_src_path:" in answers


def test_drift_notice_ignores_exactly_what_never_reaches_a_project(render):
    """`scripts/template_drift.py` hardcodes which template paths never reach an
    existing project (it runs in the instance, which has no copier.yml). If its
    list falls behind copier.yml, sessions get notices for template-internal
    edits (noise) or none for real ones (a silent miss)."""
    import importlib.util
    import yaml  # noqa: requirements -- a copier dependency; this test never reaches an instance

    spec = importlib.util.spec_from_file_location("template_drift", REPO / "scripts" / "template_drift.py")
    drift = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(drift)

    skip = set(yaml.safe_load((REPO / "copier.yml").read_text())["_skip_if_exists"])
    tracked = _tracked()
    rendered = _files(render)
    wrong = []
    for f in sorted(tracked):
        name = f[: -len(SUFFIX)] if f.endswith(SUFFIX) else f
        shadowed = not f.endswith(SUFFIX) and f"{f}{SUFFIX}" in tracked
        reaches = ("{{" in name or name in rendered) and not shadowed and name not in skip
        if drift.reaches_project(f) != reaches:
            wrong.append(f"{f}: script says {drift.reaches_project(f)}, copier says {reaches}")
    assert not wrong, "template_drift.IGNORED disagrees with copier.yml:\n" + "\n".join(wrong)


def test_template_table_matches_fit_steps():
    """The template ships every fit row `not evaluated` and none of its own
    (README). A PR that adds, renames or drops a row must update FIT_STEPS too.
    Here, not in test_check_fit_table.py: instances answer rows and add theirs."""
    rows = cf.fit_rows((cf.ROOT / cf.PIPELINE).read_text())
    assert [r[1] for _, r in rows] == cf.FIT_STEPS
    assert cf.check(cf.ROOT) == ([], len(cf.FIT_STEPS))
