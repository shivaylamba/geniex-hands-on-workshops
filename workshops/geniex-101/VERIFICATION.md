# GenieX 101 device verification

**Status:** Runtime and workshop path passed; small-model output limitations documented
**Date:** 1 September 2026
**Workshop release:** 0.1.0

## Verified environment

| Component | Verified value |
|---|---|
| Device | Dell Latitude 7455 |
| Processor | Snapdragon X Elite X1E80100, 12 cores |
| Memory | 31.6 GiB |
| Operating system | Windows 11 Enterprise ARM64, build 26200 |
| Python | 3.12.8 ARM64 |
| GenieX CLI | v0.5.0 |
| GenieX Python / SDK | 0.5.0 / v0.5.0 |
| QAIRT | v2.45.0.260326 |
| Detected `llama_cpp` devices | Adreno `GPUOpenCL`, Hexagon `HTP0`, Snapdragon CPU |
| Model | `unsloth/Qwen3.5-2B-GGUF`, `Q4_0`, text-only load |
| Weight file | 1,214,873,856 bytes; SHA-256 `cd70221bebaee0503e0f6717e174250cd7825aa88438b3aabec9ad55731d9bb1` |

The upstream Qwen3.5 repository also caused GenieX to cache `mmproj-F32.gguf` (1,325,684,416 bytes), so `geniex list` reports a 2.4 GiB cache entry. The workshop manifest marks the model as `llm`, and the text inference loads the 1.13 GiB Q4_0 weight file. Full pinned values are in `setup/versions.json`.

## Verification results

| Gate | Result | Evidence |
|---|---|---|
| Environment script | Pass | Five checks passed: device, native Python, SDK/Hexagon, CLI/chipset, model cache |
| Python compilation | Pass | Solution, starter, and tests compile without syntax errors |
| Automated tests | Pass | 14 tests passed in 0.06 seconds |
| Native CLI on NPU | Pass | 46 tokens, 18.2 tok/s, approximately 0.2 s to first token |
| Solution dry run | Pass | Source file and role messages validated without loading the model |
| Solution brief mode on NPU | Pass | Correct purpose/key points/question; 18.7 tok/s in the recorded run |
| Participant starter on NPU | Pass | Streaming response; 847.7 ms TTFT and 17.6 tok/s |
| Solution actions mode on NPU | Pass with quality warning | Inference succeeded; deterministic output checker correctly reported a malformed table |
| Cache/offline-scoped run | Pass | Inference exited 0 with `HF_HUB_OFFLINE=1` and HTTP/HTTPS proxies pointed to an unreachable local port |

## Commands exercised

Readiness:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\workshops\geniex-101\setup\verify_environment.ps1
```

Native CLI:

```powershell
geniex --skip-update infer unsloth/Qwen3.5-2B-GGUF:Q4_0 `
  --compute npu --think=false --max-tokens 80 `
  -p "Explain on-device AI in exactly two short sentences."
```

Tests:

```powershell
.\.venv\Scripts\python.exe -m pytest .\workshops\geniex-101\tests -q
```

Completed solution:

```powershell
.\.venv\Scripts\python.exe .\workshops\geniex-101\solution\app.py `
  --file .\workshops\geniex-101\starter\sample-data\event-notes.txt `
  --mode brief --device npu --max-new-tokens 180
```

## Representative observations

The first completed brief run reported:

```text
TTFT: 892.1 ms
Prompt: 382 tokens
Generated: 113 tokens
Prefill: 429.2 tok/s
Decode: 18.7 tok/s
Stop: eos
```

The final actions-mode validation run reported 1,217.9 ms TTFT, 449.2 tok/s prefill, and 17.8 tok/s decode. It found the named Maya, Arjun, and Priya assignments and the unassigned signage/help-desk work, but the 2B model omitted the required header/separator, shortened dates, and included two general questions as action rows. The application surfaced this as `Output contract: REVIEW REQUIRED`.

## Important finding: Python TTFT units

Hardware validation found a mismatch between the current documentation table and GenieX 0.5.0 behavior. The installed Python package's `geniex/generation/output.py` formats `ProfileData.ttft` as microseconds, and its CLI divides the value by `1e6` for seconds. The workshop solution therefore divides by 1,000 before displaying milliseconds. A raw value of `892123` is shown as `892.1 ms`, not `892123 ms`.

This conversion is covered by a unit test and must be rechecked when the pinned GenieX version changes.

## Quality conclusion

The runtime, NPU path, cache behavior, starter, completed application, profiling, tests, and facilitator commands are verified on the stated device. The small 2B model is suitable for a fast introductory inference workshop, but it is not consistently reliable at strict structured extraction. The workshop now makes that limitation visible through deterministic structure checks and source-verification exercises.

For a production-quality extraction demo, evaluate a larger or better instruction-following model as a separate model-quality decision; do not confuse that choice with whether GenieX inference itself works.
