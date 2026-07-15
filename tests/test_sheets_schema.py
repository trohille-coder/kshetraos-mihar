"""Contract tests for the Google Sheets CRM schema (``sheets/schema.md``).

These lock down the 16-column ``Mihar_Borrowers`` contract that the n8n
workflow and any future service layer depend on. Changing a column name,
type, or ordering here must be a deliberate, reviewed edit.
"""

from __future__ import annotations

import re

import pytest

EXPECTED_SHEET_NAME = "Mihar_Borrowers"

# Ordered (column_name, type) contract as documented in sheets/schema.md.
EXPECTED_COLUMNS: list[tuple[str, str]] = [
    ("borrower_id", "Text"),
    ("full_name", "Text"),
    ("phone_number", "Text"),
    ("village", "Text"),
    ("district", "Text"),
    ("loan_amount", "Number"),
    ("loan_disbursed_date", "Date"),
    ("due_date", "Date"),
    ("amount_due", "Number"),
    ("last_contact_date", "Date"),
    ("contact_status", "Dropdown"),
    ("follow_up_count", "Number"),
    ("whatsapp_sent", "Boolean"),
    ("repayment_status", "Dropdown"),
    ("officer_assigned", "Text"),
    ("notes", "Text"),
]

_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*([A-Za-z]+)\s*\|\s*(.+?)\s*\|\s*$"
)


def _parse_rows(text: str) -> list[tuple[int, str, str, str]]:
    rows: list[tuple[int, str, str, str]] = []
    for line in text.splitlines():
        m = _ROW_RE.match(line.strip())
        if m:
            rows.append((int(m.group(1)), m.group(2), m.group(3), m.group(4)))
    return rows


@pytest.fixture(scope="module")
def rows(sheets_schema_text: str) -> list[tuple[int, str, str, str]]:
    return _parse_rows(sheets_schema_text)


def test_sheet_name_declared(sheets_schema_text: str) -> None:
    assert f"`{EXPECTED_SHEET_NAME}`" in sheets_schema_text


def test_column_count(rows: list[tuple[int, str, str, str]]) -> None:
    assert len(rows) == len(EXPECTED_COLUMNS), (
        f"expected {len(EXPECTED_COLUMNS)} columns, found {len(rows)}"
    )


def test_row_numbers_are_sequential(rows: list[tuple[int, str, str, str]]) -> None:
    numbers = [r[0] for r in rows]
    assert numbers == list(range(1, len(numbers) + 1)), (
        f"column numbering must be 1..N in order, got {numbers}"
    )


def test_column_names_and_order(rows: list[tuple[int, str, str, str]]) -> None:
    actual = [(r[1], r[2]) for r in rows]
    assert actual == EXPECTED_COLUMNS


def test_column_names_unique(rows: list[tuple[int, str, str, str]]) -> None:
    names = [r[1] for r in rows]
    duplicates = {n for n in names if names.count(n) > 1}
    assert not duplicates, f"duplicate column names: {sorted(duplicates)}"


def test_every_column_has_description(rows: list[tuple[int, str, str, str]]) -> None:
    missing = [r[1] for r in rows if not r[3].strip()]
    assert not missing, f"columns missing a description: {missing}"


def test_trigger_logic_section_present(sheets_schema_text: str) -> None:
    assert "## Workflow Trigger Logic" in sheets_schema_text


@pytest.mark.parametrize(
    "column",
    ["repayment_status", "due_date", "whatsapp_sent"],
)
def test_trigger_logic_references_key_columns(
    sheets_schema_text: str, column: str
) -> None:
    # The documented trigger depends on these columns; guard against silent drift.
    _, _, trigger = sheets_schema_text.partition("## Workflow Trigger Logic")
    assert column in trigger, f"trigger logic must reference `{column}`"
