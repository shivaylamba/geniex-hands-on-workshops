# Device verification — 15 September 2026

## What was actually checked

The shared runner executed **30 real generations** on this device using GenieX with `device_map="npu"`: five broken-baseline cases, five reference cases, and two ten-generation output-budget experiments. No hosted model was substituted. This verifies the local inference path, not a hardware utilization trace or production reliability.

- Device: Dell Latitude 7455, Snapdragon X Elite X1E80100, approximately 32 GB RAM, Windows ARM64.
- Interpreter: native ARM64 Python 3.12.8; GenieX Python package 0.5.0.
- Model: `unsloth/Qwen3.5-2B-GGUF`, Q4_0, cached text weights 1,214,873,856 bytes (~1.13 GiB). The cached projector is 1,325,684,416 bytes; total cache approximately 2.4 GiB. The app loads text inference only.
- Shared release/model provenance: [existing version manifest](../geniex-101/setup/versions.json). The new workshop uses the same prepared environment and cached model. That manifest's date is the earlier setup verification, not this experiment date.
- Context: `n_ctx=2048`; source-character budget 360; thinking disabled in the chat template; temperature 0.0; reset before every case. No explicit random seed is supplied. Outputs varied across repeats.
- **33 automated tests passed:** 14 existing 101 tests, 16 new implementation challenges, three new runner/evaluator tests. The untouched learner challenges intentionally produced **14 failures and two passes** when targeted at `starter`.

## Recorded observations

| Run | Count | Policy acceptance | Fixture answer pass | Joint pass | Mean generation wall ms | TTFT range ms | Token-limit stops |
|---|---:|---:|---:|---:|---:|---:|---:|
| [Broken starter, 160 tokens](verification/baseline-npu.jsonl) | 5 | 5/5 (JSON-only) | 0/5 | 0/5 | 2240.00 | 366.71–383.66 | 0 |
| [Reference, 160 tokens, first run](verification/solution-npu.jsonl) | 5 | 5/5 | 4/5 | 4/5 | 1971.56 | 304.32–445.30 | 0 |
| [Reference, 24 tokens, two repeats](verification/short-npu.jsonl) | 10 | 0/10 | 0/10 | 0/10 | 1604.15 | 302.05–450.42 | 10 |
| [Reference, 160 tokens, two repeats](verification/long-npu.jsonl) | 10 | 8/10 | 6/10 | 6/10 | 2353.45 | 302.08–450.48 | 0 |

Model load times were respectively 3000.8, 3530.4, 2697.5, and 2346.1 ms. They are recorded separately and excluded from generation wall time. Each JSONL row includes input question, selected source IDs, raw model text, policy reasons, fixture result, token counts, stop reason, timings, and configuration.

Policy acceptance for the starter is only JSON parsing; it is **not** the reference evidence contract. `reference_pass` is a narrow source-ID/word check, not human-assessed accuracy. Joint pass means both automated checks pass, not that an answer is necessarily true.

### Useful failures retained, not cleaned up

1. The broken selector supplies archived Cedar to every question. Its JSON-only policy accepts all five outputs, including the wrong room and an unrelated signage answer.
2. With correct retrieval, a supported answer of “Yes” to the offline question fails the fixture's expected phrase “without internet.” This is a clear evaluator false negative worth discussing in 301.
3. In the longer repeated run, one unknown answer uses a full sentence instead of the required literal `unknown`; another combines `source_id: none` with a nonempty quote. Both are withheld by the reference contract.
4. All ten 24-token generations hit the length limit, including unknown-case variants whose JSON formatting used more tokens than the concise answer in another run. Lower latency did not produce usable accepted answers.
5. An automated adversarial test proves that a false Cedar answer with a genuine Maple quotation passes the provenance contract. A separate fixture rejects it. This is a deliberately documented semantic-validation gap.

Do not turn the small observed samples into a general accuracy or speedup claim. The fixture set is used during development, outputs are not independent benchmark samples, and thermal/device state was not controlled as a formal performance study.

## Reproduce from repository-root PowerShell

Use fresh output filenames; the runner refuses overwrites. The shared [setup guide](../geniex-101/setup/README.md) prepares dependencies and cache.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --evaluate --output workshops/geniex-bootcamp/output/baseline-recheck.jsonl
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track solution --evaluate --output workshops/geniex-bootcamp/output/solution-recheck.jsonl
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track solution --evaluate --repeats 2 --max-tokens 24 --output workshops/geniex-bootcamp/output/short-recheck.jsonl
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track solution --evaluate --repeats 2 --max-tokens 160 --output workshops/geniex-bootcamp/output/long-recheck.jsonl
```

## Not yet verified

- Live classroom pacing with novice participants: the 120-minute agenda needs an instructor timing pilot.
- Other chipsets, operating systems, dependency versions, or models.
- Fully disconnected-network execution for this new runner on an event fleet. These runs used a cached model on a connected device. Application locality is not proof of whole-machine network isolation.
- Production security, prompt-injection resistance, semantic correctness, or an unattended-release threshold.

These are workshop exercises and reference implementations, not a production-ready assistant.
