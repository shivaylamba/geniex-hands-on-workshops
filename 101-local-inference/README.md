# 101: Run a local model and diagnose a broken assistant

**Duration:** 25 minutes after setup. **Next:** [201](../201-evidence-assistant/README.md).

## What you will learn

Generate text through GenieX's CLI and Python SDK, identify the requested compute device, and locate a stale-source bug. You do not train or fine-tune a model here.

## Session prerequisites

Complete [setup steps 1–3](../INTERNAL-WALKTHROUGH.md#1-check-the-laptop-and-install-the-cli). You need a supported Snapdragon Windows ARM64 laptop, native ARM64 Python, the GenieX CLI/SDK, and cached Q4_0 weights. One prepared device per pair is sufficient. There is no UNO Q board or wiring step.

Keep repository-root PowerShell, this page, and [the worksheet](../workshops/geniex-bootcamp/WORKSHEET.md) open side by side.

## Step 1 — Predict the failure (3 minutes)

Open [the documents](../workshops/geniex-bootcamp/data/documents.json). Find the room in the first document and in `current-room`. These are fictional records.

Write before executing: which room should we tell an attendee? What room will a first-document selector see? Could a bigger model reliably recover a fact the application never supplies?

## Step 2 — Understand the path (5 minutes)

```text
Question -> source selection -> chat template -> GenieX runtime
         -> model generation on requested compute -> text -> output checks
```

The model ID identifies the weights; `Q4_0` identifies their quantized representation; `npu` requests compute. Python file handling and ranking still run on the CPU. Context must accommodate instructions, source text, template, and output. Explain this diagram to your partner.

AI Hub preparation/deployment and Arduino UNO Q development are adjacent topics in the broader workshop program, not prerequisites for this lab. This module teaches GenieX application development.

## Step 3 — Run the CLI and SDK (5 minutes)

After configuring `geniex` in the setup note:

```powershell
geniex infer unsloth/Qwen3.5-2B-GGUF:Q4_0 --compute npu --think=false --max-tokens 80 -p "Explain on-device AI in two sentences."
.\.venv\Scripts\python.exe 101-local-inference/hello_geniex.py
```

Both should produce text without a hosted-model API key. The SDK example prints load time, TTFT, token count, and stop reason. Exact prose varies. A token-limit stop is different from a process crash.

Open [hello_geniex.py](hello_geniex.py). Locate model loading, chat templating, and generation. The `with` block releases the model. Change only the question:

```powershell
.\.venv\Scripts\python.exe 101-local-inference/hello_geniex.py --question "Explain on-device AI to an event organizer in one sentence."
```

Predict what changes. Does a request for a shorter answer guarantee a lower time to first token?

Read the explanation critically. In our rehearsal the changed question elicited an invented biometric-personalization scenario; this app does not collect biometric data. Successful generation does not make the explanation factual. Mark any unsupported claim before presenting it to someone else.

## Step 4 — Inspect before inferring (7 minutes)

```powershell
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --inspect
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --output output/101-baseline.jsonl
Get-Content output/101-baseline.jsonl | ForEach-Object { $_ | ConvertFrom-Json } | Format-List question,selected_ids,raw,accepted,reasons
```

Inspection loads no model. Untouched starter code selects `archive-room`. Inference saves a result file; choose a new name when rerunning because overwrites are refused.

`accepted: true` currently means JSON parsing succeeded, not that the answer is correct. `reference_pass` is null for a custom single question; known-answer checks require `--evaluate`.

In [app.py](../workshops/geniex-bootcamp/app.py), trace selection, `build_messages`, template, generation, and validation. Loading happens outside the case loop; reset happens for each independent case. Which component should change first?

## Step 5 — Explain your diagnosis (5 minutes)

Give a 30-second explanation containing expected source, selected source, raw answer, and fix location. Your partner should repeat the explanation in their own words.

Checkpoint: both interfaces ran, you identified stale input, and you distinguish parseable from correct. If inference fails, use [recorded evidence](../verification/TEAM-REHEARSAL.md) as explicitly labeled reference, not as your own run.

## Troubleshooting

- CLI not found: reopen PowerShell or repeat the full-path alias step in the internal guide.
- SDK import fails: use the virtual-environment executable, not another system Python.
- Missing weights: repeat setup checks; do not change models mid-lesson.
- Wrong room: expected baseline behavior; temperature is not the first fix.

**Continue to [201](../201-evidence-assistant/README.md).**
