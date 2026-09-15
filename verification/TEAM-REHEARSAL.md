# Team edition: actual laptop rehearsal

> A later user-requested [double-check](DOUBLE-CHECK-2026-09-15.md) reran all 16 steps successfully with 33 additional real generations.

Date: 15 September 2026. This report is the evidence behind [the internal walkthrough](../INTERNAL-WALKTHROUGH.md), not a claim that every model answer was correct.

## Scope

A new `.venv-team` was created on the same Dell Latitude 7455 / Snapdragon X Elite X1E80100 laptop. Dependencies were freshly installed and then locked in [requirements-lock.txt](../requirements-lock.txt). It used native ARM64 Python 3.12.8, GenieX SDK/CLI 0.5.0, the existing approved CLI/runtime installation, existing device drivers, and the previously cached Qwen3.5-2B Q4_0 model. The SDK discovered llama_cpp and Hexagon/HTP compute.

The 1,214,873,856-byte text weight file was rehashed locally and matched the existing manifest: `cd70221bebaee0503e0f6717e174250cd7825aa88438b3aabec9ad55731d9bb1`. The model's total cache also includes its projector; see [prior provenance](../workshops/geniex-101/setup/versions.json).

The interpreter version is an observation about this laptop, not a recommendation to install that old version. New team machines should use an approved maintained native interpreter and rerun verification.

## An issue found and fixed

The first rehearsal stopped at readiness: the checker reported CLI failure even though direct version and chipset commands subsequently exited successfully. Its native CLI calls were piped through `Select-Object -First 1`, terminating output consumption early and relying on the final exit status.

The checker now consumes each command fully and captures/checks both exit codes before selecting display text. The repeated rehearsals passed with this change. The initial failed evidence is preserved in [the first summary](team-rehearsal-2026-09-15/summary.json) and [environment output](team-rehearsal-2026-09-15/environment.txt). This was a checker problem, not evidence that the NPU could not run.

## Final end-to-end run

**Result: all 16 rehearsal steps passed their expected outcomes; 33 unit tests passed; 33 real generations completed** (one CLI, two minimal SDK examples, and 30 evaluation generations). The final warm-cache rehearsal took approximately 91 seconds on this device. That is machine execution time, not the two-hour learner workshop duration.

| Final experiment | Generations | Policy pass | Fixture pass | Joint pass | Truncated | Mean generation ms |
|---|---:|---:|---:|---:|---:|---:|
| Broken baseline, 160 tokens | 5 | 5/5 (JSON-only) | 1/5 | 1/5 | 0 | 1915.16 |
| Completed reference, 160 tokens | 5 | 4/5 | 3/5 | 3/5 | 0 | 2245.16 |
| Completed reference, 24 tokens | 10 | 2/10 | 1/10 | 1/10 | 8 | 1501.66 |
| Completed reference, 160 tokens, two repeats | 10 | 8/10 | 7/10 | 7/10 | 0 | 2379.87 |

These rates are not interchangeable: the baseline policy is merely JSON parsing; the completed policy checks schema/evidence; the fixture checker only checks expected source IDs and answer terms. Joint pass means both automated checks pass, not semantic correctness.

The authoritative run is [team-rehearsal-2026-09-15-final/summary.json](team-rehearsal-2026-09-15-final/summary.json), produced by:

```powershell
.\.venv-team\Scripts\python.exe scripts/rehearse_workshop.py --output verification/team-rehearsal-2026-09-15-final
```

The directory is checked in and must not be overwritten; use a new output directory when reproducing. The summary records versions, source hashes, timestamps, per-step status, and experiment metrics. Its `base_commit` identifies the original base; source hashes identify the tested working files before the team-edition publication commit.

The rehearsal includes:

- Dependency checks and five hardware/environment/cache readiness checks.
- CLI help and a real CLI generation.
- Both standalone SDK example commands, including a changed question.
- All 33 reference tests and the expected 14 failing / two passing untouched starter challenges.
- Starter and reference inspection of all five questions without model loading.
- Four real-model evaluations: baseline, completed reference, short budget, long budget.
- Refusal to overwrite an existing output and rejection of an invalid budget.

Detailed result counts are in the summary and raw JSONL. The interpretation is deliberately separate: **workflow success is not model-quality success**. The completed model is still capable of invalid abstentions and other errors, and the word-based fixture checker has known blind spots.

The changed-question minimal SDK example also invented a biometric-personalization scenario. Nothing in the workshop collects biometric data; that sentence is ungrounded model output, not an application capability. This provides another concrete reason to distinguish a successful inference call from a factual explanation. The raw output is retained rather than polished into an invented success.

## Reading the evidence

| File in the final run | What it proves or illustrates |
|---|---|
| `environment.txt` | Native device, SDK runtime discovery, CLI exits, cached model |
| `cli-generation.txt` | Actual CLI inference output and runtime profile |
| `sdk-hello.txt`, `sdk-custom-question.txt` | Both documented minimal Python examples ran |
| `reference-tests.txt` | Reference code tests passed |
| `intentional-starter-failures.txt` | Learner scaffolds are meaningfully incomplete |
| `baseline.jsonl` | Archived-source and JSON-only-policy failures |
| `completed.jsonl` | Completed selector/validator with real model outputs |
| `short.jsonl`, `long.jsonl` | Same fixture set under two output budgets |
| `overwrite-protection.txt`, `invalid-budget.txt` | Expected safety/argument errors occurred before generation |

Raw output can differ across repeated runs even at temperature zero. Every question is reset independently; no explicit random seed is supplied. Five development fixtures and two repeats are not a production accuracy benchmark.

## What remains untested

- Windows CLI installer execution from a clean operating-system image, driver installation, and cold model download. Existing installations/caches were reused.
- Every teammate's hardware or a maintained interpreter different from the one on this laptop.
- Fully disconnected-network operation; these were connected-device runs with cached weights.
- Live classroom timing and learning outcomes with novice participants.
- Production semantic correctness, prompt-injection resistance, or unattended deployment.

The first full corrected run before adding the standalone SDK examples is retained in [team-rehearsal-2026-09-15-r2](team-rehearsal-2026-09-15-r2/summary.json). Use the final run for the published walkthrough.
