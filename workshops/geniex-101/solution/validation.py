"""Deterministic checks for generated output contracts."""

from __future__ import annotations


EXPECTED_ACTION_HEADER = ["owner", "action", "due date"]


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def validate_action_table(text: str) -> list[str]:
    """Return structural issues in a generated Markdown action table."""
    table_lines = [line.strip() for line in text.splitlines() if line.strip().startswith("|")]
    if not table_lines:
        return ["No Markdown table was found."]

    issues: list[str] = []
    header = [cell.lower() for cell in _cells(table_lines[0])]
    if header != EXPECTED_ACTION_HEADER:
        issues.append("The first row is not the required Owner | Action | Due date header.")

    if len(table_lines) < 3:
        issues.append("The table does not contain a separator and at least one data row.")
        return issues

    separator = _cells(table_lines[1])
    if len(separator) != 3 or any(not cell or set(cell) - {"-", ":"} for cell in separator):
        issues.append("The second row is not a valid three-column Markdown separator.")

    for row_number, line in enumerate(table_lines[2:], start=3):
        if len(_cells(line)) != 3:
            issues.append(f"Table row {row_number} does not have exactly three cells.")
    return issues
