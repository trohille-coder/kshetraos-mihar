"""Structural checks for the repository's markdown documentation.

These complement the (style-focused) markdownlint pass in CI by asserting the
things that actually matter for this docs-first repo: every doc has a single
top-level title, heading levels never skip, and local links/images resolve to
files that exist.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from conftest import REPO_ROOT, markdown_files

_HEADING_RE = re.compile(r"^(#{1,6})\s+\S")
_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")

MD_FILES = markdown_files()
MD_IDS = [str(p.relative_to(REPO_ROOT)) for p in MD_FILES]


def _headings(text: str) -> list[tuple[int, str]]:
    """Return (level, title) for headings outside of fenced code blocks."""
    headings: list[tuple[int, str]] = []
    in_fence = False
    for line in text.splitlines():
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = _HEADING_RE.match(line)
        if m:
            headings.append((len(m.group(1)), line.strip("# ").strip()))
    return headings


def test_repo_has_markdown_docs() -> None:
    assert MD_FILES, "expected at least one markdown doc in the repo"


@pytest.mark.parametrize("md_path", MD_FILES, ids=MD_IDS)
def test_exactly_one_h1(md_path: Path) -> None:
    headings = _headings(md_path.read_text(encoding="utf-8"))
    h1s = [title for level, title in headings if level == 1]
    assert len(h1s) == 1, (
        f"{md_path.name} must have exactly one top-level (#) heading, found {len(h1s)}"
    )


@pytest.mark.parametrize("md_path", MD_FILES, ids=MD_IDS)
def test_first_heading_is_h1(md_path: Path) -> None:
    headings = _headings(md_path.read_text(encoding="utf-8"))
    assert headings, f"{md_path.name} has no headings"
    assert headings[0][0] == 1, f"{md_path.name} must start with an H1"


@pytest.mark.parametrize("md_path", MD_FILES, ids=MD_IDS)
def test_heading_levels_do_not_skip(md_path: Path) -> None:
    headings = _headings(md_path.read_text(encoding="utf-8"))
    prev = 0
    for level, title in headings:
        assert level <= prev + 1, (
            f"{md_path.name}: heading '{title}' (H{level}) skips a level "
            f"(previous was H{prev})"
        )
        prev = level


@pytest.mark.parametrize("md_path", MD_FILES, ids=MD_IDS)
def test_local_links_resolve(md_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")
    broken: list[str] = []
    for target in _LINK_RE.findall(text):
        target = target.strip()
        # Skip external links, anchors, and mail links.
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        # Strip any in-page anchor from a relative path (e.g. ./foo.md#section).
        path_part = target.split("#", 1)[0]
        if not path_part:
            continue
        resolved = (md_path.parent / path_part).resolve()
        if not resolved.exists():
            broken.append(target)
    assert not broken, f"{md_path.name} has broken local links: {broken}"


@pytest.mark.parametrize("md_path", MD_FILES, ids=MD_IDS)
def test_no_trailing_whitespace(md_path: Path) -> None:
    offenders = [
        i
        for i, line in enumerate(md_path.read_text(encoding="utf-8").splitlines(), 1)
        if line != line.rstrip()
    ]
    assert not offenders, f"{md_path.name} has trailing whitespace on lines {offenders}"
