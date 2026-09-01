from __future__ import annotations

import pytest

from solution.prompts import SUPPORTED_MODES, build_messages


@pytest.mark.parametrize("mode", SUPPORTED_MODES)
def test_each_mode_builds_role_based_messages(mode: str) -> None:
    messages = build_messages(mode, "Maya owns the repository by Friday.")
    assert [message["role"] for message in messages] == ["system", "user"]
    assert "Maya owns the repository" in messages[1]["content"]
    assert "treat as data" in messages[1]["content"]


def test_actions_mode_requires_unknown_for_missing_values() -> None:
    messages = build_messages("actions", "The signage owner has not been chosen.")
    assert "unknown" in messages[0]["content"]
    assert "Owner | Action | Due date" in messages[1]["content"]


def test_empty_notes_are_rejected() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        build_messages("brief", "  ")


def test_unknown_mode_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported mode"):
        build_messages("translate", "Some notes")
