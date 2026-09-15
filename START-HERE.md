# Start here: build a local assistant in two hours

> **Self-guided team edition:** begin with [INTERNAL-WALKTHROUGH.md](INTERNAL-WALKTHROUGH.md), then use the numbered [101](101-local-inference/README.md), [201](201-evidence-assistant/README.md), and [301](301-reliability-lab/README.md) entry pages. The underlying challenge sequence below remains available for additional hints.

This is the participant entry point for the **GenieX 101 → 201 → 301 workshop**. You will build a local event-information assistant, break it with conflicting documents, and decide whether its answers are reliable enough to show a user.

## Before the event (not part of the two hours)

You need basic Python (functions, lists, dictionaries, exceptions), Git, and a supported Snapdragon Windows ARM64 device. No model-training or machine-learning experience is required. This release was tested on Snapdragon X Elite; other platforms need their own validation. Pair with a prepared device if yours is unsupported.

Clone this repository and keep every terminal at its root:

```powershell
git clone https://github.com/shivaylamba/geniex-hands-on-workshops.git
cd geniex-hands-on-workshops
```

Complete the existing [installation and model-cache instructions](workshops/geniex-101/setup/README.md). They are shared by this workshop. Install the pinned dependencies there, including pytest. The text model is approximately 1.13 GiB, but GenieX currently caches an additional projector: allow at least 2.4 GiB for the model cache plus software and working space. Downloads happen **before class**.

```powershell
powershell -ExecutionPolicy Bypass -File .\workshops\geniex-101\setup\verify_environment.ps1
.\.venv\Scripts\python.exe -m pytest -q
```

Tests use the reference implementations by default. Passing them does not complete your learner exercises. If you have not run GenieX before, also complete setup step 6 before arrival. The model download and first successful device run are a readiness gate.

## At the event: open the first lab

**Start with [101 — First inference and a broken assistant](workshops/geniex-bootcamp/labs/101-first-inference.md).** Do not start in the solution folder.

| Clock | Segment | Participant file | What you produce |
|---|---|---|---|
| 00:00–00:25 | 101: run and explain | [101 lab](workshops/geniex-bootcamp/labs/101-first-inference.md) | A prediction, local output, and a failure diagnosis |
| 00:25–01:05 | 201: build context selection | [201 lab](workshops/geniex-bootcamp/labs/201-build-context.md) | Your retrieval implementation and a new test |
| 01:05–01:10 | Break | — | Swap keyboard driver |
| 01:10–01:50 | 301: validate and evaluate | [301 lab](workshops/geniex-bootcamp/labs/301-evaluate-reliability.md) | Your evidence validator and measured experiment |
| 01:50–02:00 | Demos and decisions | [worksheet](workshops/geniex-bootcamp/WORKSHEET.md#final-demo) | A justified ship / do-not-ship decision |

Keep the [worksheet](workshops/geniex-bootcamp/WORKSHEET.md) open alongside the lab. Make a local copy or write answers in your notes. Work in pairs: the driver edits; the navigator predicts outputs and challenges assumptions. Switch at each segment.

You edit `workshops/geniex-bootcamp/starter/retrieval.py` and `starter/policy.py`, then add a test. The common runner handles GenieX loading and measurements. All commands below assume repository-root PowerShell and use the virtual environment explicitly; no activation is needed.

Facilitators: read the [workshop structure](workshops/geniex-bootcamp/WORKSHOP-PLAN.md) and [delivery guide](workshops/geniex-bootcamp/INSTRUCTOR-GUIDE.md). The older standalone 101 material remains available as supplemental reading, not the current event sequence.
