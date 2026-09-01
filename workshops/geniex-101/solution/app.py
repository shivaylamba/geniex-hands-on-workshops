"""Command-line entry point for the GenieX 101 Local Briefing Assistant."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from .inference import format_profile, run_geniex
    from .prompts import SUPPORTED_MODES, build_messages
    from .validation import validate_action_table
except ImportError:
    from inference import format_profile, run_geniex
    from prompts import SUPPORTED_MODES, build_messages
    from validation import validate_action_table


DEFAULT_MODEL = "unsloth/Qwen3.5-2B-GGUF"
DEFAULT_PRECISION = "Q4_0"
MAX_INPUT_CHARACTERS = 12_000


def read_notes(path: Path, max_characters: int = MAX_INPUT_CHARACTERS) -> str:
    """Read and validate a UTF-8 notes file."""
    if not path.exists():
        raise ValueError(f"Input file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"Input path is not a file: {path}")

    try:
        text = path.read_text(encoding="utf-8").strip()
    except UnicodeDecodeError as exc:
        raise ValueError("Input must be a UTF-8 text file.") from exc

    if not text:
        raise ValueError("Input file is empty.")
    if len(text) > max_characters:
        raise ValueError(
            f"Input is {len(text):,} characters; the workshop limit is {max_characters:,}."
        )
    return text


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a local briefing from a UTF-8 notes file with GenieX."
    )
    parser.add_argument("--file", type=Path, required=True, help="Path to a UTF-8 notes file")
    parser.add_argument("--mode", choices=SUPPORTED_MODES, default="brief")
    parser.add_argument("--audience", default="developer event team")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--precision", default=DEFAULT_PRECISION)
    parser.add_argument("--device", default="npu", help="npu, gpu, cpu, hybrid, or explicit device map")
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--thinking", action="store_true", help="Enable thinking on models that support it")
    parser.add_argument("--no-stream", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Validate input and show messages without loading a model")
    parser.add_argument("--save", type=Path, help="Optional path for the generated response")
    args = parser.parse_args(argv)

    if not 1 <= args.max_new_tokens <= 2048:
        parser.error("--max-new-tokens must be between 1 and 2048")
    if not 0.0 <= args.temperature <= 2.0:
        parser.error("--temperature must be between 0.0 and 2.0")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        notes = read_notes(args.file)
        messages = build_messages(args.mode, notes, args.audience)
    except ValueError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2

    print(
        f"Mode: {args.mode} | Notes: {len(notes):,} chars | "
        f"Model: {args.model}:{args.precision} | Device: {args.device}"
    )

    if args.dry_run:
        print("\nDry run passed. Messages prepared:")
        for message in messages:
            print(f"- {message['role']}: {len(message['content']):,} characters")
        return 0

    print("\nGenerated response:\n")
    try:
        result = run_geniex(
            messages,
            model_id=args.model,
            precision=args.precision,
            device=args.device,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            enable_thinking=args.thinking,
            stream=not args.no_stream,
            on_chunk=(lambda chunk: print(chunk, end="", flush=True)),
        )
    except Exception as exc:
        print(f"\nInference error: {exc}", file=sys.stderr)
        return 1

    if args.no_stream:
        print(result.text)
    else:
        print()

    print(f"\nPerformance\n{format_profile(result.profile)}")

    if args.mode == "actions":
        contract_issues = validate_action_table(result.text)
        if contract_issues:
            print("\nOutput contract: REVIEW REQUIRED")
            for issue in contract_issues:
                print(f"- {issue}")
            print("- Verify every owner, action, and date against the source notes.")
        else:
            print("\nOutput contract: structure passed; factual verification is still required.")

    if args.save:
        args.save.parent.mkdir(parents=True, exist_ok=True)
        args.save.write_text(result.text + "\n", encoding="utf-8")
        print(f"Saved response to {args.save.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
