# 101 — Understand GenieX and get a useful first result

**25 minutes.** Before this lab, complete [setup](../INTERNAL-WALKTHROUGH.md#setup-before-class). Next: [201](../201-evidence-assistant/README.md). Keep [your worksheet](../workshops/workday-copilot/WORKSHEET.md) open.

## Goal and checkpoint

Explain what GenieX supplies, run a local model, and turn a project note into a readable summary. Checkpoint: show real output and point to the exact model call, not just an installation success message.

## 1. Meet the problem — 3 minutes

You have an hour before your next meeting. Your portfolio website needs work. What should you tackle, and what should you tell a teammate?

Read [the fictional note and tasks](../workshops/workday-copilot/data/workday.json). Without AI, pick two tasks and calculate their duration. Keep that prediction; you will compare it with the copilot later. Ask: does a summary alone solve this problem?

## 2. Put GenieX in the architecture — 7 minutes

[GenieX](https://geniex.aihub.qualcomm.com/en/get-started/what-is-geniex) is an on-device generative-AI runtime with developer interfaces. It is not the model weights, an agent framework, or your application's safety policy.

```text
Your input → Python application → chat template → GenieX → local model → generated text
                 ↑                                                    |
                 └──────── validate / show / request next step ────────┘
```

This lab uses the Python SDK and a quantized GGUF model through the llama.cpp runtime with NPU compute requested. “2B” is model parameter scale; Q4_0 is the selected quantization; `npu` is a compute request. Python reads JSON and performs arithmetic on the CPU. Do not claim every operation runs on the NPU.

Qualcomm AI Hub preparation/profiling and Arduino UNO Q application development are other tracks in the program, not prerequisites here. GenieX is the execution layer we need for this local text application.

Partner challenge: label the model, runtime, application logic, and device separately. Who should enforce “do not send the message”? Answer: the application must provide no sending capability; prompting alone is insufficient.

## 3. Run the useful baseline — 7 minutes

From the repository root:

```powershell
.\.venv\Scripts\python.exe workshops/workday-copilot/app.py --mode summary --output output/my-summary-1.json
Get-Content output/my-summary-1.json
```

Expected: `status: summary_ready`, a draft based on the project note, and real generation metrics. Wording and sentence count can vary; manually check accuracy. No plan has been validated yet.

Open [app.py](../workshops/workday-copilot/app.py). Find these operations:

1. Load the fixed synthetic JSON input.
2. Load the model through `AutoModelForCausalLM.from_pretrained`.
3. Format messages with `apply_chat_template`.
4. Call `generate` and record the output.
5. Save a review-only result using the human-specified filename.

The [official Python API reference](https://geniex.aihub.qualcomm.com/en/run/python/api-reference) documents these interfaces. The model is reset before each call so our full message history is not added to stale generation state.

## 4. Make one change — 5 minutes

Change only the project note in the JSON file: make checking page titles the top priority. Keep the task IDs and durations unchanged. Predict the summary, then rerun to `output/my-summary-2.json`. Compare the two files.

Does the summary reflect your change? Does it invent completed work? Record an observed weakness even when the program exits successfully. Restore the original note manually before 201, keeping your observation in the worksheet.

## 5. Explain the next step — 3 minutes

A summary generates text in one call. The next lab lets the model request tools, see their results, and decide what to request next. That is useful when the answer requires inspecting data and checking a constraint, rather than just rephrasing a note.

Hint ladder: inspect the JSON input → find the summary system message → compare raw text with the note. If loading fails, return to setup; do not change model IDs randomly during class.

Proceed to [201: build the planning tool](../201-evidence-assistant/README.md).
