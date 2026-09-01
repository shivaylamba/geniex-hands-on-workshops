# Lab 1 — First local inference from the CLI

**Time:** 20 minutes
**Goal:** Run the pinned model and improve a prompt through observation.

## Run one prompt

```powershell
geniex infer unsloth/Qwen3.5-2B-GGUF:Q4_0 `
  --compute npu `
  --think=false `
  --max-tokens 100 `
  -p "Explain on-device AI to a 12-year-old in two sentences."
```

If the command starts a download, stop and ask the facilitator for a prepared device—the model should already be cached.

## Change one variable

Run the same command for an application-developer audience. Then change only one of:

- audience;
- requested format; or
- response length.

Before running, predict what will change. Afterward, record what actually changed.

## Make a runtime decision

Choose a path for each scenario:

1. A compatible GGUF from Hugging Face with possible CPU fallback.
2. A pre-compiled Qualcomm AI Hub bundle optimized for your exact chipset.

Your choices should be `llama_cpp` for the first and `qairt` for the second. Explain why in one sentence each.

## Checkpoint

Point to the model identifier, precision, compute unit, prompt, and output in your command and result.

## Next lab

Continue to [`02-python-first-inference.md`](02-python-first-inference.md).
