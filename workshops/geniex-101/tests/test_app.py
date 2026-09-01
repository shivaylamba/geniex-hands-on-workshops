from __future__ import annotations

from pathlib import Path

import pytest

from solution.app import main, read_notes


def test_read_notes_accepts_utf8_text(tmp_path: Path) -> None:
    source = tmp_path / "notes.txt"
    source.write_text("A useful note.\n", encoding="utf-8")
    assert read_notes(source) == "A useful note."


def test_read_notes_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        read_notes(tmp_path / "missing.txt")


def test_read_notes_rejects_empty_file(tmp_path: Path) -> None:
    source = tmp_path / "empty.txt"
    source.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="empty"):
        read_notes(source)


def test_dry_run_uses_real_application_path(tmp_path: Path, capsys) -> None:
    source = tmp_path / "notes.txt"
    source.write_text("Arjun will validate laptops by Friday.", encoding="utf-8")
    exit_code = main(["--file", str(source), "--mode", "actions", "--dry-run"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Dry run passed" in captured.out
    assert "Mode: actions" in captured.out
