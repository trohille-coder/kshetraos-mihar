"""Shared fixtures and path helpers for the KshetraOS structural test suite."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

WORKFLOW_PATH = REPO_ROOT / "workflows" / "mihar-followup-desk.json"
WORKFLOW_SCHEMA_PATH = REPO_ROOT / "schemas" / "n8n-workflow.schema.json"
SHEETS_SCHEMA_PATH = REPO_ROOT / "sheets" / "schema.md"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def workflow() -> dict:
    with WORKFLOW_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture(scope="session")
def workflow_schema() -> dict:
    with WORKFLOW_SCHEMA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture(scope="session")
def sheets_schema_text() -> str:
    return SHEETS_SCHEMA_PATH.read_text(encoding="utf-8")


def markdown_files() -> list[Path]:
    """All tracked markdown docs in the repo (excluding vendored/hidden dirs)."""
    ignored = {".git", "node_modules", ".venv", "venv"}
    return sorted(
        p
        for p in REPO_ROOT.rglob("*.md")
        if not any(part in ignored for part in p.relative_to(REPO_ROOT).parts)
    )
