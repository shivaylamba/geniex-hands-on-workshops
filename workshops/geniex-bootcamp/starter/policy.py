"""Lab 301 baseline: JSON parsing alone does not verify evidence."""
import json

def validate_answer(raw, selected):
    # Deliberately weak baseline. Return (accepted: bool, reasons: list[str]).
    try:
        json.loads(raw)
        return True, []
    except ValueError:
        return False, ["Invalid JSON"]
