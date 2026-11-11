"""The merge-gate guards against the inputs of their 2026-11-11 audit.

Each case is one input from ``docs/FINDINGS_merge_gate_guards.md`` §"Appendix:
the inputs", keyed by its ID there. A case the guard gets right today is a
plain test. A case it gets wrong is ``xfail(strict=True)``: the fix that closes
it turns the test red until someone moves it into the plain list, so every
change to what a guard fails on shows up here input by input (TODO W).

Not here: C12, a citation to a doc that exists nowhere, which warns by design
(projects create some docs later); E11, a lower-case mark, which the header
asks for.
"""

import sys
from datetime import timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check_decisions_log as dl  # noqa: E402
import check_doc_citations as dc  # noqa: E402

# raises= keeps a broken fixture from passing as a gap.
# Dates relative to CUTOFF, so a project that moves it keeps these meaningful.
NEW_D = (dl.CUTOFF + timedelta(days=55)).isoformat()   # the audit's 2026-11-11
PREV_D = (dl.CUTOFF + timedelta(days=54)).isoformat()  # 2026-11-10
OLD_D = (dl.CUTOFF + timedelta(days=14)).isoformat()   # 2026-10-01
YM = NEW_D[:7]
PRE_D = (dl.CUTOFF - timedelta(days=1)).isoformat()  # D2: a year typo lands before CUTOFF
GAP = pytest.mark.xfail(strict=True, raises=AssertionError, reason="audit 2026-11-11 gap; TODO W")

# --- decisions log ------------------------------------------------------------

HEADER = "# Decisions\n\n| When | Decision | Full reasoning |\n|---|---|---|\n"
OLD = f"| {OLD_D} | **Old rule.** [unverifiable] | p |"
TESTS = (
    "import pytest\n\n"
    "def test_real():\n    pass\n\n"
    "def test_area_uses_EPSG3776():\n    pass\n\n"
    "async def test_fetch():\n    pass\n"
)


def _log(tmp_path: Path, body: str, *, encoding: str = "utf-8") -> Path:
    for d in ("docs", "tests", "scripts", "tools", "web/tests"):
        (tmp_path / d).mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "DECISIONS.md").write_text(HEADER + body + "\n", encoding=encoding)
    (tmp_path / "tests" / "test_real.py").write_text(TESTS)
    (tmp_path / "scripts" / "check_real.py").write_text("")
    (tmp_path / "scripts" / "check_decisions_log.py").write_text("")  # D14 cites the guard
    (tmp_path / "tools" / "check_links.py").write_text("")
    (tmp_path / "web" / "tests" / "verify-load.js").write_text("")
    return tmp_path


def _fails(root: Path) -> bool:
    return dl.check(root) != []


NEW = "**New, no test, no tag.**"

D_RIGHT = {  # id: (body, should_fail)
    "D0a": (f"| {NEW_D} | **New.** | p |", True),
    "D0b": (f"| {NEW_D} | **New.** `test_real` | p |", False),
    "D0c": (f"| {NEW_D} | **New.** `test_gone` | p |", True),
    "D0d": (f"| {NEW_D} | **New.** [unverifiable] | p |", False),
    "D0e": (OLD + f"\n| {NEW_D} | Supersedes the {OLD_D} row. [unverifiable] | p |", True),
    "D0f": (OLD.replace("**Old rule.**", f"**Old rule.** SUPERSEDED {NEW_D}")
            + f"\n| {NEW_D} | Supersedes the {OLD_D} row. [unverifiable] | p |", False),
    "D1.7": (f"| {NEW_D} (S14) | {NEW} | p |", True),
    "D1.8": (f"|  {NEW_D} | {NEW} | p |", True),
}

_SUPERSEDE = {
    "D8.0": f"Replaces the {OLD_D} row.",
    "D8.1": f"Overrides the {OLD_D} row.",
    "D8.2": f"Overturns the {OLD_D} row.",
    "D8.3": f"Withdraws the {OLD_D} row.",
    "D8.4": f"Revokes the {OLD_D} row.",
    "D8.5": f"Undoes the {OLD_D} row.",
    "D8.6": f"Corrects the {OLD_D} row.",
    "D8.7": f"Updates the {OLD_D} row.",
    "D8.8": f"The {OLD_D} row is superseded.",
    "D8.9": f"The {OLD_D} row is retracted.",
    "D8.10": f"The {OLD_D} row no longer holds.",
    "D8.11": f"This will supersede the {OLD_D} row.",
    "D8.12": f"Reversing the {OLD_D} row.",
    "D8.13": f"Retracting the {OLD_D} row.",
    "D8.14": f"A reversal of the {OLD_D} row.",
    "D8.15": f"An amendment to the {OLD_D} row.",
    "D8.16": "Supersedes the old-rule row.",
    "D8.17": "Supersedes the previous row.",
    "D8.18": "Supersedes the earlier decision.",
    "D8.19": f"Supersedes, after the owner asked alberta and tax-viz and permit-speed once more, the {OLD_D} row.",
    "D8.20": "Supersedes the 1 October row.",
}

D_PASSES_WRONGLY = {  # should fail, exits 0
    "D1.0": f"| Nov 11, 2026 | {NEW} | p |",
    "D1.1": f"| **{NEW_D}** | {NEW} | p |",
    "D1.2": f"| {YM} | {NEW} | p |",
    "D1.3": f"|  | {NEW} | p |",
    "D1.4": f"| 11/11/2026 | {NEW} | p |",
    "D1.5": f"| S14 | {NEW} | p |",
    "D1.6": f"| ~~{NEW_D}~~ | {NEW} | p |",
    "D1.9": f"| **New, no test.** | {NEW_D} | p |",
    "D2": f"| {PREV_D} | ok [unverifiable] | p |\n| {PRE_D} | **New, year typo, no test.** | p |",
    "D3": OLD + f"\n| {NEW_D} | `test_real` holds; matcher `Read|Grep` now supersedes the {OLD_D} row; see `test_gone` | p |",
    "D6": f"| {OLD_D} | **Old rule.** ~~one clause~~ [unverifiable] | p |\n"
          f"| {NEW_D} | Supersedes the {OLD_D} row. [unverifiable] | p |",
    "D7": f"| {OLD_D} | **A.** SUPERSEDED {NEW_D} [unverifiable] | p |\n"
          f"| {OLD_D} | **B.** [unverifiable] | p |\n"
          f"| {NEW_D} | Supersedes the {OLD_D} A row. [unverifiable] | p |\n"
          f"| {NEW_D} | Supersedes the {OLD_D} B row. [unverifiable] | p |",
    "D8.x": OLD + f"\n| {NEW_D} | **New.** [unverifiable] | Supersedes the {OLD_D} row; p |",
    "D9": f"| {NEW_D} | **New.** [unverifiable] |  |",
    "D10a": f"- {NEW_D}: **New, no test.**",
    "D10b": f"  | {NEW_D} | {NEW} | p |",
    "D14": f"| {NEW_D} | **New.** Enforced by `check_decisions_log.py`. | p |",
    **{k: OLD + f"\n| {NEW_D} | {v} [unverifiable] | p |" for k, v in _SUPERSEDE.items()},
}

D_FAILS_WRONGLY = {  # should pass, fails
    "E1": f"| {NEW_D} | **Hold out 20%: `test_size=0.2`.** [unverifiable] | p |",
    "E2": f"| {NEW_D} | **Links.** `tools/check_links.py` | p |",
    "E3": f"| {NEW_D} | **CRS.** `test_area_uses_EPSG3776` | p |",
    "E4": f"| {NEW_D} | **Fetch.** `test_fetch` | p |",
    "E5": f"| {OLD_D} | ~~**Old rule.** `test_old_rule`~~ SUPERSEDED {NEW_D} | p |\n"
          f"| {NEW_D} | **New.** Supersedes the {OLD_D} row. [unverifiable] | p |",
    "E6a": f"| {PREV_D} | **Innocent.** [unverifiable] | p |\n"
           f"| {NEW_D} | **New.** tax-viz retracted its report {PREV_D}. [unverifiable] | p |",
    "E6b": f"| {NEW_D} | **New.** The owner reversed the plan {NEW_D}. [unverifiable] | p |",
    "E7": f"| {NEW_D} | **New.** | [unverifiable] p |",
    "E8": f"| {NEW_D} | **Hook matcher stays `Read|Grep|Glob`.** [unverifiable] | p |",
}


@pytest.mark.parametrize("case", sorted(D_RIGHT))
def test_decisions_input_right_today(tmp_path, case):
    body, should_fail = D_RIGHT[case]
    assert _fails(_log(tmp_path, body)) is should_fail


@GAP
@pytest.mark.parametrize("case", sorted(D_PASSES_WRONGLY))
def test_decisions_input_should_fail(tmp_path, case):
    assert _fails(_log(tmp_path, D_PASSES_WRONGLY[case]))


@GAP
def test_decisions_input_should_fail_D5(tmp_path):
    root = _log(tmp_path, f"| {NEW_D} | **New.** `test_ghost` | p |")
    (root / "tests" / "test_a.py").write_text('FIXTURE = """\ndef test_ghost():\n    pass\n"""\n')
    assert _fails(root)


@GAP
def test_decisions_input_should_fail_D11(tmp_path):
    assert _fails(_log(tmp_path, f"| {NEW_D} | {NEW} | p |", encoding="utf-16"))


@GAP
@pytest.mark.parametrize("case", sorted(D_FAILS_WRONGLY))
def test_decisions_input_should_pass(tmp_path, case):
    assert not _fails(_log(tmp_path, D_FAILS_WRONGLY[case]))


@pytest.mark.xfail(strict=True, raises=ValueError, reason="E10: traceback, not exit 6; TODO W3")
def test_decisions_input_E10_impossible_date_exits_6(tmp_path):
    root = _log(tmp_path, "| 2026-02-30 | **Typo date.** [unverifiable] | p |")
    assert dl.main(["--root", str(root)]) == dl.EXIT_FAIL


# --- doc citations ------------------------------------------------------------

def _repo(tmp_path: Path, files: dict[str, str], *, name: str = "repo") -> Path:
    root = tmp_path / name
    seed = {
        "docs/spec.md": "# Spec\n\n## 1. One\n\nx\n\n## 2. Two\n\ny\n",
        "data/quirks.md": "# Quirks\n\nshort\n",
        "README.md": "# Readme\n",
        **files,
    }
    for rel, text in seed.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return root


def _cites_fail(root: Path) -> bool:
    return dc.check_citations(root)[0] != []


C_RIGHT = {  # id: (text in docs/log.md, should_fail)
    "C0a": ("See spec.md §9.", True),
    "C0b": ("See spec.md §2.", False),
    "C0c": ("See quirks.md:207.", True),
    "C0d": ("See quirks.md line 207.", True),
    "C2b": ("[the data notes](../data/quirks.md#L207)", True),
    "C10.7": ("quirks.md, around line 207", True),
    "C10.11": ("quirks.md §207", True),
}

LINE = "see quirks.md:207"
C_PASSES_WRONGLY = {  # id: {path: text}; should fail, exits 0
    "C1a": {"docs/log.md": "See README.md and quirks.md:207."},
    "C1b": {"docs/log.md": "Read `docs/spec.md`, then `data/quirks.md` line 207."},
    "C1c": {"docs/log.md": "README.md and spec.md §9"},
    "C2a": {"docs/log.md": "[spec.md](spec.md) §9"},
    "C1d": {"docs/notes.md": "# Notes\n", "docs/log.md": "[the data notes](../data/quirks.md#L207)"},
    "C2c": {"docs/log.md": "[quirks.md](../data/quirks.md#L207)"},
    "C3.0": {"docs/log.md": "spec.md, §9"},
    "C3.1": {"docs/log.md": "spec.md (§9)"},
    "C3.2": {"docs/log.md": "**spec.md** §9"},
    "C3.3": {"docs/log.md": "spec.md's §9"},
    "C3.4": {"docs/log.md": "spec.md: §9"},
    "C3.5": {"docs/log.md": "spec.md at §9"},
    "C3.6": {"docs/log.md": "spec.md §1 and §9"},
    "C3.7": {"docs/log.md": "spec.md §§1, 9"},
    "C3.8": {"docs/log.md": "spec.md — §9"},
    "C3.9": {"docs/log.md": "`spec.md` §9"},
    "C4a": {"docs/log.md": 'He said "check it\nlater" and cited quirks.md:207.'},
    "C4b": {"scripts/x.py": 'raise SystemExit("see quirks.md:207")\n'},
    "C4c": {"docs/log.md": 'The 6" pipe rule is in quirks.md:207.'},
    "C4d": {"docs/ci.yml": 'run: echo "see spec.md §9"\n'},
    "C5a": {"docs/web_site_plan.md": "See quirks.md:207."},
    "C5b": {".github/workflows/x.yml": f"# {LINE}\n"},
    "C6.0": {".claude/skills/x/steps.md": LINE},
    "C6.1": {"tests/test_x.py": f"# {LINE}\n"},
    "C6.2": {"web/index.html": f"<!-- {LINE} -->"},
    "C6.3": {"notebooks/n.md": LINE},
    "C6.4": {"bootstrap.sh": f"# {LINE}\n"},
    "C6.5": {"docs/notes.txt": LINE},
    "C6.6": {"docs/x.md.jinja": LINE},
    "C6.7": {"src/x.R": f"# {LINE}\n"},
    "C6.8": {"CONTRIBUTING.md": LINE},
    "C6.9": {".githooks/pre-push": f"# {LINE}\n"},
    "C8": {"docs/spec.md": "# Spec\n\n## 1. One\n\n```bash\n# 9 retries\n```\n", "docs/log.md": "spec.md §9"},
    "C10.0": {"docs/log.md": "quirks.md L207"},
    "C10.1": {"docs/log.md": "quirks.md, l. 207"},
    "C10.2": {"docs/log.md": "quirks.md ln 207"},
    "C10.3": {"docs/log.md": "quirks.md (L207)"},
    "C10.4": {"docs/log.md": "quirks.md:~207"},
    "C10.5": {"docs/log.md": "quirks.md @207"},
    "C10.6": {"docs/log.md": "`quirks.md`:207"},
    "C10.8": {"docs/log.md": "quirks.md:L207"},
    "C10.9": {"docs/log.md": "quirks.md row 207"},
    "C10.10": {"docs/log.md": "quirks.md#207"},
    "C11": {"docs/specs/fire.md": "# Fire\n\n## 1. One\n", "docs/log.md": "fire.md §9"},
}


@pytest.mark.parametrize("case", sorted(C_RIGHT))
def test_citation_input_right_today(tmp_path, case):
    text, should_fail = C_RIGHT[case]
    assert _cites_fail(_repo(tmp_path, {"docs/log.md": text})) is should_fail


@GAP
@pytest.mark.parametrize("case", sorted(C_PASSES_WRONGLY))
def test_citation_input_should_fail(tmp_path, case):
    assert _cites_fail(_repo(tmp_path, C_PASSES_WRONGLY[case]))


@GAP
@pytest.mark.parametrize("folder", ["my_site", "owner.github.io"])
def test_citation_input_should_fail_by_checkout_name(tmp_path, folder):
    """C5c, C5d: the checkout's own folder name matches an excluded part."""
    assert _cites_fail(_repo(tmp_path, {"docs/log.md": "See quirks.md:207."}, name=folder))


@GAP
def test_citation_input_should_fail_C13(tmp_path):
    root = _repo(tmp_path, {})
    (root / "docs" / "log.md").write_bytes("Caf\xe9. See spec.md §9.".encode("latin-1"))
    assert _cites_fail(root)

