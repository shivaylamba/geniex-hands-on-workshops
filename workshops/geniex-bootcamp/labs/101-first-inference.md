# 101 — First inference and a broken assistant (25 minutes)

**Previous:** [Start here](../../../START-HERE.md). **Next:** [201](201-build-context.md).

## Your mission

An event attendee asks which room hosts the workshop. Your assistant has both an old announcement and a current one. Run the model locally, then identify where the wrong answer enters the application. Success means explaining the system, not getting lucky with a fluent response.

Open [the worksheet](../WORKSHEET.md), [documents](../data/documents.json), and [the runner](../app.py). These are fictional practice documents, not actual event instructions.

## 0–3 minutes: readiness and prediction

From repository-root PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\workshops\geniex-101\setup\verify_environment.ps1
```

If setup fails, use a prepared partner device and continue as navigator. Do not start a multi-gigabyte download during class.

Before running inference, write: What should the room answer be? Which source proves it? What answer might a program that reads only the first document give? Commit your prediction before you see the result.

## 3–8 minutes: the minimum mental model

Discuss the architecture diagram in the [structure file](../WORKSHOP-PLAN.md#architecture-learners-should-understand). The model predicts text from tokens; it does not automatically inspect your files or know which announcement is current. The application selects text and sends a formatted prompt. GenieX connects the application to an inference runtime and supported compute.

Distinguish these four settings out loud:

- `unsloth/Qwen3.5-2B-GGUF`: model repository; 2B is parameter count, not file size.
- `Q4_0`: the selected quantized weights.
- `npu`: requested compute path; Python retrieval still executes normally on the CPU.
- `max_tokens`: output ceiling, not an instruction to produce exactly that many tokens.

The runner uses a 2048-token context, disables thinking in the template, and resets the model between independent cases. Local inference can avoid sending prompts to a hosted inference service, but this does not prove that the whole machine has no network activity. Cache first; test offline separately.

## 8–13 minutes: make the NPU generate

```powershell
geniex infer unsloth/Qwen3.5-2B-GGUF:Q4_0 --compute npu --think=false --max-tokens 80 -p "Explain on-device AI in two sentences."
```

If `geniex` is not on PATH, use `& "$env:LOCALAPPDATA\GenieX CLI\geniex.exe"` in place of `geniex`. Record one output sentence. Explain to your partner which argument changes hardware and which changes output length.

Now make one intentional change: ask for a one-sentence explanation for a nontechnical attendee. Predict whether a shorter requested answer necessarily guarantees lower time to first token. Run again and compare. Do not treat two unrelated prompts as a controlled performance benchmark.

## 13–20 minutes: inspect before you infer

```powershell
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --inspect
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --output workshops/geniex-bootcamp/output/101-baseline.jsonl
```

The first command loads no model: it shows exactly what the selector supplies. The unmodified starter selects `archive-room`. The second command runs the shared Python inference path and saves its raw result and timings. Output may vary: a wrong room, an abstention, or malformed JSON are all possible. Inspect the saved `selected_ids` and `raw` fields, not only the acceptance flag.

Open `app.py` and find these operations: `select_context`, `apply_chat_template`, `from_pretrained`, `generate`, and `validate_answer`. Trace their data dependencies in execution order. Where would you fix stale evidence? Would increasing model size repair a selector that never provides the current document?

The starter's acceptance policy checks only that output parses as JSON. Therefore `accepted: true` does **not** mean the answer is correct. Circle this in your worksheet; you will repair it in 301.

## 20–25 minutes: pair diagnosis and checkpoint

Each pair gives a 30-second diagnosis: expected source, selected source, observed output, and the component to change first. The navigator must be able to explain the runner without the driver speaking.

Checkpoint:

- You generated text through GenieX on the prepared device, or observed your partner doing so.
- You recorded the stale-source failure and distinguished input selection from generation.
- You can explain why valid JSON is not evidence of a correct answer.

If inference fails, retain the retrieval prediction and use the [recorded runs](../VERIFICATION.md) as clearly labeled reference evidence. Do not claim that you ran them yourself. Continue with the CPU-only coding tests in 201.

**Next: [201 — Build context selection](201-build-context.md).**
