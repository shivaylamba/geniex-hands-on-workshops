# GenieX 101: Build Your First Local AI Application on Snapdragon

In this 2.5-hour workshop you will run a language model locally on the Snapdragon NPU, use the real GenieX Python SDK, and build a Local Briefing Assistant that turns a text file into a concise briefing or action table.

> **Taking the workshop? Begin with [`START-HERE.md`](START-HERE.md).** It identifies the first file to open, separates pre-work from timed workshop work, and links every lab in order.

## What you will produce

By the end, your application will:

- read and validate a local UTF-8 notes file;
- construct role-based messages for multiple output modes;
- run the pinned Q4_0 model through GenieX and `llama_cpp` on the Hexagon NPU;
- stream generated text;
- report TTFT, token counts, prefill speed, decode speed, and stop reason; and
- save an optional local result.

The completed solution also checks the structure of generated action tables and warns when the model violates the output contract. Participants still verify facts against the source.

## Before the workshop

Complete [setup/README.md](setup/README.md), then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\workshops\geniex-101\setup\verify_environment.ps1
```

Do not begin with a model download during the event. Pair with a known-good machine if the pinned model is not cached.

## Learning journey

| Time | Lab | Evidence |
|---:|---|---|
| 0–25 min | Readiness and architecture | You can trace application → SDK → runtime → compute |
| 25–45 min | First CLI inference | A local response from the pinned model |
| 45–80 min | First Python inference | Streaming output plus a profile |
| 80–90 min | Break | Every pair reaches the build checkpoint |
| 90–125 min | Local Briefing Assistant | Working `brief` and `actions` modes |
| 125–140 min | Observe and improve | One controlled comparison |
| 140–150 min | Demo and exit ticket | Architecture, evidence, and limitation explained |

## Labs

Follow the sequence from [`START-HERE.md`](START-HERE.md). The first timed workshop file is [`labs/00-readiness.md`](labs/00-readiness.md).

1. [Lab 0 — Readiness and architecture](labs/00-readiness.md)
2. [Lab 1 — First local inference from the CLI](labs/01-cli-first-inference.md)
3. [Lab 2 — First inference from Python](labs/02-python-first-inference.md)
4. [Lab 3 — Build the Local Briefing Assistant](labs/03-local-briefing-assistant.md)
5. [Lab 4 — Observe and improve](labs/04-observe-and-improve.md)

## Run the completed solution

From the repository root:

```powershell
.\.venv\Scripts\python.exe .\workshops\geniex-101\solution\app.py `
  --file .\workshops\geniex-101\starter\sample-data\event-notes.txt `
  --mode actions `
  --device npu `
  --max-new-tokens 220
```

Use `--dry-run` to validate application input and messages without loading a model. Use `--no-stream` to compare the experience of waiting for the complete response.

## Validate the repository

```powershell
.\.venv\Scripts\python.exe -m pytest .\workshops\geniex-101\tests -q
```

Hardware validation results are recorded in [VERIFICATION.md](VERIFICATION.md). The full curriculum and publication rationale are in [WORKSHOP-PLAN.md](WORKSHOP-PLAN.md).

## Responsible use

Model output can be incorrect. The sample prompts require the model to use only the supplied notes and write `unknown` for missing values, but application developers must still verify generated claims against the source. Treat local files as untrusted data, and never paste access tokens into prompts or commit them to the repository.
