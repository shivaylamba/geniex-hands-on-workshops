"""Check a strict response contract; quote existence is not semantic entailment."""
import json

def validate_answer(raw, selected):
    try:
        answer = json.loads(raw)
    except (ValueError, TypeError):
        return False, ["Invalid JSON"]
    fields = {"answer", "source_id", "quote"}
    if not isinstance(answer, dict) or set(answer) != fields:
        return False, ["Expected exactly answer, source_id, quote"]
    if any(not isinstance(answer[key], str) for key in fields):
        return False, ["All fields must be strings"]
    if not answer["answer"].strip():
        return False, ["Empty answer"]
    if answer["source_id"] == "none":
        valid = answer["answer"].strip().lower() == "unknown" and answer["quote"] == ""
        return valid, [] if valid else ["Unsupported answer must be unknown with an empty quote"]
    source = next((doc for doc in selected if doc["id"] == answer["source_id"]), None)
    if source is None:
        return False, ["Source was not selected"]
    if source.get("status") != "current":
        return False, ["Source is not current"]
    if not answer["quote"].strip() or answer["quote"] not in source["text"]:
        return False, ["Quote is empty or absent from the source"]
    return True, []
