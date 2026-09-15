"""Rehearse the prepared Windows ARM64 workshop; never installs or edits learner code.

Run from a clean checkout after setup. An existing output directory is never reused.
Success means the workflow executed, NOT that every model answer was correct.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import statistics
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "workshops/geniex-bootcamp/app.py"


def summarize(records):
    if not records:
        raise ValueError("No generation records were produced")
    return {
        "generations": len(records),
        "policy_pass": sum(row["accepted"] for row in records),
        "fixture_pass": sum(row["reference_pass"] for row in records),
        "joint_pass": sum(row["accepted"] and row["reference_pass"] for row in records),
        "truncated": sum(row["stop_reason"] in {"length", "limit", "max_tokens"} for row in records),
        "generation_wall_ms_mean": round(statistics.mean(row["generation_wall_ms"] for row in records), 2),
        "ttft_ms_min": min(row["ttft_ms"] for row in records),
        "ttft_ms_max": max(row["ttft_ms"] for row in records),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New directory for evidence")
    parser.add_argument("--cli", type=Path, help="Full path if GenieX CLI is not discoverable")
    args = parser.parse_args()
    cli = args.cli or shutil.which("geniex")
    if not cli:
        cli = Path(os.environ.get("LOCALAPPDATA", "")) / "GenieX CLI/geniex.exe"
    if not Path(cli).is_file():
        parser.error("GenieX CLI not found; install it or pass --cli")
    if args.output.exists():
        parser.error("Output directory exists; choose a new rehearsal directory")
    args.output.mkdir(parents=True)
    summary = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "architecture": platform.machine(),
        "geniex": importlib.metadata.version("geniex"),
        "packages": {name: importlib.metadata.version(name) for name in
                     ["geniex", "pytest", "tqdm", "colorama", "iniconfig", "packaging", "pluggy", "pygments"]},
        "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "source_sha256": {}, "steps": [], "experiments": {},
        "scope": "Prepared-machine execution; not an installer or disconnected-network test",
    }
    source_paths = [APP, ROOT / "requirements.txt", Path(__file__).resolve(),
                    ROOT / "requirements-lock.txt", ROOT / "101-local-inference/hello_geniex.py",
                    ROOT / "workshops/geniex-101/setup/verify_environment.ps1"]
    for folder in ["starter", "solution", "data", "tests"]:
        source_paths.extend(path for path in (APP.parent / folder).iterdir() if path.is_file())
    for path in sorted(source_paths):
        canonical = path.read_bytes().replace(b"\r\n", b"\n")
        summary["source_sha256"][path.relative_to(ROOT).as_posix()] = hashlib.sha256(canonical).hexdigest()

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["WORKSHOP_TRACK"] = "solution"

    def step(name, command, expected=0, environment=None):
        print(f"RUN {name}", flush=True)
        start = time.perf_counter()
        result = subprocess.run([str(item) for item in command], cwd=ROOT, env=environment or env,
                                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
        output = (result.stdout + "\n" + result.stderr).replace(str(ROOT), "<REPO>").replace(str(Path.home()), "<USER>")
        (args.output / f"{name}.txt").write_text(output, encoding="utf-8")
        row = {"step": name, "exit_code": result.returncode, "expected_exit_code": expected,
               "passed": result.returncode == expected, "elapsed_seconds": round(time.perf_counter() - start, 2)}
        summary["steps"].append(row)
        print(f"{'PASS' if row['passed'] else 'FAIL'} {name} ({row['elapsed_seconds']}s)", flush=True)
        if not row["passed"]:
            raise RuntimeError(f"{name} exited {result.returncode}; see {name}.txt")

    try:
        step("dependency-check", [sys.executable, "-m", "pip", "check"])
        step("environment", ["powershell", "-ExecutionPolicy", "Bypass", "-File",
                             ROOT / "workshops/geniex-101/setup/verify_environment.ps1",
                             "-PythonPath", sys.executable, "-GenieXCliPath", cli])
        step("cli-help", [cli, "--help"])
        step("cli-generation", [cli, "infer", "unsloth/Qwen3.5-2B-GGUF:Q4_0", "--compute", "npu",
                                "--think=false", "--max-tokens", "80", "-p",
                                "Explain on-device AI in two sentences."])
        step("sdk-hello", [sys.executable, ROOT / "101-local-inference/hello_geniex.py"])
        step("sdk-custom-question", [sys.executable, ROOT / "101-local-inference/hello_geniex.py",
             "--question", "Explain on-device AI to an event organizer in one sentence."])
        step("reference-tests", [sys.executable, "-m", "pytest", "-q"])
        starter_env = dict(env, WORKSHOP_TRACK="starter")
        step("intentional-starter-failures", [sys.executable, "-m", "pytest",
             "workshops/geniex-bootcamp/tests/test_challenges.py", "-q", "--tb=short"],
             expected=1, environment=starter_env)
        step("inspect-starter", [sys.executable, APP, "--track", "starter", "--evaluate", "--inspect"])
        step("inspect-solution", [sys.executable, APP, "--track", "solution", "--evaluate", "--inspect"])
        for name, track, tokens, repeats in [
            ("baseline", "starter", 160, 1), ("completed", "solution", 160, 1),
            ("short", "solution", 24, 2), ("long", "solution", 160, 2),
        ]:
            destination = args.output.resolve() / f"{name}.jsonl"
            step(name, [sys.executable, APP, "--track", track, "--evaluate", "--repeats", repeats,
                        "--max-tokens", tokens, "--output", destination])
            records = [json.loads(line) for line in destination.read_text(encoding="utf-8").splitlines()]
            if len(records) != 5 * repeats or any(not row["raw"].strip() for row in records):
                raise RuntimeError(f"{name}: expected nonempty generations for all five stock cases")
            summary["experiments"][name] = summarize(records)
        # Check that protective CLI errors work before model loading.
        step("overwrite-protection", [sys.executable, APP, "--output", args.output.resolve() / "baseline.jsonl"], expected=2)
        step("invalid-budget", [sys.executable, APP, "--context-chars", "0"], expected=2)
        summary["workflow_passed"] = True
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as error:
        summary["workflow_passed"] = False
        summary["error"] = str(error).replace(str(ROOT), "<REPO>")
        print(f"Rehearsal stopped: {error}", file=sys.stderr)
    finally:
        summary["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary["experiments"], indent=2))
    print(f"Workflow passed: {summary['workflow_passed']}; model quality is reported separately.")
    return 0 if summary["workflow_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
