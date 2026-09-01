from __future__ import annotations

from solution.validation import validate_action_table


def test_valid_action_table_passes() -> None:
    text = """| Owner | Action | Due date |
|---|---|---|
| Maya | Freeze tag | 10 September 2026 |"""
    assert validate_action_table(text) == []


def test_missing_header_is_reported() -> None:
    text = """| Maya | Freeze tag | 10 September 2026 |
| Arjun | Test laptops | 14 September 2026 |"""
    issues = validate_action_table(text)
    assert any("required" in issue for issue in issues)
    assert any("separator" in issue for issue in issues)


def test_missing_table_is_reported() -> None:
    assert validate_action_table("Maya will freeze the tag.") == ["No Markdown table was found."]
