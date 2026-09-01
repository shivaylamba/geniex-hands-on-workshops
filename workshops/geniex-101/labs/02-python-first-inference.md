# Lab 2 — First inference from Python

**Time:** 25 minutes
**Goal:** Identify and run the load → format → generate → profile → release path.

Open `starter/inference.py` and find:

1. `AutoModelForCausalLM.from_pretrained()`;
2. `model.tokenizer.apply_chat_template()`;
3. `model.generate(..., stream=True)`;
4. `streamer.output.profile`; and
5. the context manager that releases the model.

Run the starter:

```powershell
Push-Location .\workshops\geniex-101\starter
..\..\..\.venv\Scripts\python.exe .\app.py `
  --file .\sample-data\event-notes.txt `
  --mode brief
Pop-Location
```

Record TTFT, generated tokens, and decode speed. These are observations from one run, not benchmark results.

GenieX 0.5.0 stores Python profile timing fields such as `ttft` in microseconds. The starter divides by 1,000 before displaying milliseconds. This is pinned-version behavior and must be rechecked when upgrading GenieX.

## Prediction challenge

In `starter/inference.py`, change `max_new_tokens` from 256 to 100. Predict which profile fields can change, then run again.

## Checkpoint

Explain why `apply_chat_template()` is different from joining strings manually, and why the model is loaded inside a context manager.
