"""Guards on what `copier copy` gives a new project (`copier.yml`, `docs/COPIER.md`).

This repo is the template AND a project with its own backlog, decisions and
handoffs. The render must carry every template file and none of that state:
a leak hands a new project someone else's open work as its own, and a drop
is a guard or doc the instance silently never gets.

Excluded from renders (`copier.yml`), since it tests this repo's copier config.
"""
import fnmatch
import subprocess
from pathlib import Path

import pytest

copier = pytest.importorskip("copier")

REPO = Path(__file__).resolve().parents[1]

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
    for name in ("TODO.md", "docs/DECISIONS.md", "docs/TODO_archive.md"):
        assert (render / name).read_text() == (REPO / f"{name}{SUFFIX}").read_text(), name
    assert "- [ ] <first item" in (render / "TODO.md").read_text()
    rows = [ln for ln in (render / "docs/DECISIONS.md").read_text().splitlines()
            if ln.startswith("| 20")]
    assert rows == [], f"template's own decision rows leaked: {rows}"


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
    import yaml  # a copier dependency

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
