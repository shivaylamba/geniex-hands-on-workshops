"""Runner plumbing checks, separate from learner implementation challenges."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bootcamp_app", ROOT / "app.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


def test_evidence_contract_is_not_semantic_truth():
    docs = [{"id": "current-room", "status": "current", "text": "The workshop room is Maple."}]
    raw = json.dumps({"answer": "Cedar", "source_id": "current-room", "quote": docs[0]["text"]})
    assert app.load_component("solution", "policy").validate_answer(raw, docs)[0]
    case = json.loads((ROOT / "data/cases.json").read_text())[0]
    assert not app.reference_check(raw, case)


def test_fixture_check_can_reject_a_supported_short_answer():
    case = json.loads((ROOT / "data/cases.json").read_text())[-1]
    raw = json.dumps({"answer": "Yes", "source_id": "network", "quote": "The workshop must run without internet after setup."})
    docs = json.loads((ROOT / "data/documents.json").read_text())
    assert app.load_component("solution", "policy").validate_answer(raw, docs)[0]
    assert not app.reference_check(raw, case)


def test_runner_resets_each_case_rejects_truncation_and_saves(monkeypatch, tmp_path):
    class FakeModel:
        resets = 0

        def __init__(self):
            self.tokenizer = SimpleNamespace(apply_chat_template=lambda *a, **kw: "prompt")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def reset(self):
            self.resets += 1

        def generate(self, prompt, **kwargs):
            return SimpleNamespace(
                text='{"answer":"unknown","source_id":"none","quote":""}',
                profile=SimpleNamespace(ttft=123000, decode_speed=20, generated_tokens=12,
                                        prompt_tokens=40, stop_reason="max_tokens"),
            )

    model = FakeModel()
    monkeypatch.setitem(sys.modules, "geniex", SimpleNamespace(
        AutoModelForCausalLM=SimpleNamespace(from_pretrained=lambda *a, **kw: model)))
    destination = tmp_path / "runs.jsonl"
    args = argparse.Namespace(track="solution", policy=None, evaluate=True, inspect=False,
                              question="room", model="fake", device="npu", repeats=2,
                              context_chars=360, max_tokens=12, output=destination)
    records = app.run(args)
    assert model.resets == len(records) == 10
    assert all(not row["accepted"] for row in records)
    assert all(row["ttft_ms"] == 123 for row in records)
    assert all("Generation reached the token limit" in row["reasons"] for row in records)
    assert [json.loads(line) for line in destination.read_text().splitlines()] == records
