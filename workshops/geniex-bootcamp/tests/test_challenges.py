"""Set WORKSHOP_TRACK=starter to see the intentional lab failures."""
import importlib.util
import json
import os
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
TRACK = os.environ.get("WORKSHOP_TRACK", "solution")

def component(name):
    spec = importlib.util.spec_from_file_location("challenge_" + name, ROOT / TRACK / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_retrieval_prefers_current_source():
    docs = json.loads((ROOT / "data/documents.json").read_text())
    selected = component("retrieval").select_context("What is the workshop room?", docs)
    assert selected and selected[0]["id"] == "current-room"
    assert all(doc["status"] == "current" for doc in selected)

def test_retrieval_obeys_budget():
    docs = [{"id": "long", "status": "current", "text": "room " * 100},
            {"id": "short", "status": "current", "text": "room Maple"}]
    selected = component("retrieval").select_context("room", docs, 40)
    assert [doc["id"] for doc in selected] == ["short"]
    assert sum(len(doc["id"]) + len(doc["text"]) + 4 for doc in selected) <= 40

def test_retrieval_can_abstain():
    docs = [{"id": "x", "status": "current", "text": "Doors open at nine."}]
    assert component("retrieval").select_context("keynote speaker", docs) == []

def test_retrieval_generalizes_to_new_names():
    docs = [{"id": "second", "status": "current", "text": "Tara owns badges."},
            {"id": "first", "status": "current", "text": "Omar owns transport."}]
    selected = component("retrieval").select_context("Who owns transport?", docs)
    assert selected[0]["id"] == "first"


def test_retrieval_rejects_invalid_budget():
    with pytest.raises(ValueError):
        component("retrieval").select_context("room", [], 0)


def test_retrieval_breaks_ties_by_id():
    docs = [{"id": "z", "status": "current", "text": "room Oak"},
            {"id": "a", "status": "current", "text": "room Pine"}]
    assert [doc["id"] for doc in component("retrieval").select_context("room", docs)] == ["a", "z"]

SOURCE = [{"id": "r", "status": "current", "text": "Room Maple."}]

@pytest.mark.parametrize("payload", [
    [], {"answer": "Maple"},
    {"answer": 7, "source_id": "r", "quote": "Room Maple."},
    {"answer": "Cedar", "source_id": "missing", "quote": "Room Maple."},
    {"answer": "Cedar", "source_id": "r", "quote": "Room Cedar."},
    {"answer": "Maple", "source_id": "r", "quote": ""},
    {"answer": "Cedar", "source_id": "none", "quote": ""},
])
def test_policy_rejects_bad_evidence(payload):
    assert component("policy").validate_answer(json.dumps(payload), SOURCE)[0] is False

def test_policy_accepts_supported_answer_and_abstention():
    validate = component("policy").validate_answer
    assert validate(json.dumps({"answer": "Maple", "source_id": "r", "quote": "Room Maple."}), SOURCE)[0]
    assert validate(json.dumps({"answer": "unknown", "source_id": "none", "quote": ""}), [])[0]

def test_policy_rejects_archived_source():
    docs = [{"id": "old", "status": "archived", "text": "Room Cedar."}]
    raw = json.dumps({"answer": "Cedar", "source_id": "old", "quote": "Room Cedar."})
    assert component("policy").validate_answer(raw, docs)[0] is False

def test_policy_rejects_broken_json():
    assert component("policy").validate_answer('{"answer":', SOURCE)[0] is False
