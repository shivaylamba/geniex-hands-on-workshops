"""Functional starting point for the Local Briefing Assistant lab."""

from __future__ import annotations

import argparse
from pathlib import Path

from inference import run_geniex
from prompts import build_messages


MODEL_ID = "unsloth/Qwen3.5-2B-GGUF"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--mode", default="brief")
    args = parser.parse_args()

    if not args.file.is_file():
        print(f"Input error: file not found: {args.file}")
        return 2
    notes = args.file.read_text(encoding="utf-8").strip()
    if not notes:
        print("Input error: file is empty")
        return 2

    messages = build_messages(args.mode, notes)
    print("Generated response:\n")
    text, profile = run_geniex(
        messages,
        model_id=MODEL_ID,
        on_chunk=lambda chunk: print(chunk, end="", flush=True),
    )
    print(
        f"\n\nTTFT: {profile.ttft / 1_000.0:.1f} ms | "
        f"Generated: {profile.generated_tokens} tok | "
        f"Decode: {profile.decode_speed:.1f} tok/s"
    )
    return 0 if text else 1


if __name__ == "__main__":
    raise SystemExit(main())
