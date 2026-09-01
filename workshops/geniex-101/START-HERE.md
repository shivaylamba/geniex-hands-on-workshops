# Start here — GenieX 101

This is the canonical starting page for participants.

## Which file do I open first?

- **Before the event:** open [`setup/README.md`](setup/README.md). Install the prerequisites and pre-cache the model.
- **At the start of the timed workshop:** open [`labs/00-readiness.md`](labs/00-readiness.md). This is the first lab.
- **Facilitators:** also open [`instructor/RUN-OF-SHOW.md`](instructor/RUN-OF-SHOW.md) and [`instructor/FACILITATOR-GUIDE.md`](instructor/FACILITATOR-GUIDE.md).

Do not begin in `WORKSHOP-PLAN.md`. That file explains curriculum design and publication decisions; it is not the participant lesson sequence.

## Before the timed workshop

The model and software should already be installed. From the repository root, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\workshops\geniex-101\setup\verify_environment.ps1
```

You should see five passing checks and this final line:

```text
Environment ready for GenieX 101.
```

If any check fails, follow [`setup/README.md`](setup/README.md). Do not spend timed workshop minutes downloading the model; ask the facilitator for a prepared device or partner.

## Workshop sequence

Complete the files in this exact order. Each lab contains its goal, commands, activity, questions, and checkpoint.

| Order | Open this file | What you will do | Continue when… |
|---:|---|---|---|
| 1 | [`labs/00-readiness.md`](labs/00-readiness.md) | Verify the device and trace the inference architecture | All readiness checks pass and you can explain the path |
| 2 | [`labs/01-cli-first-inference.md`](labs/01-cli-first-inference.md) | Run the pinned model from the GenieX CLI on the NPU | You can identify model, precision, compute, prompt, and output |
| 3 | [`labs/02-python-first-inference.md`](labs/02-python-first-inference.md) | Run the starter and inspect load, template, generate, profile, and release | Streaming inference and performance output work |
| 4 | [`labs/03-local-briefing-assistant.md`](labs/03-local-briefing-assistant.md) | Extend the starter into a two-mode local application | `brief` and `actions` modes run on the sample file |
| 5 | [`labs/04-observe-and-improve.md`](labs/04-observe-and-improve.md) | Compare two variants and complete the exit ticket | You have measurements, a quality observation, and a limitation |

## Files you will edit

During the build, work only in:

```text
workshops/geniex-101/starter/
├── app.py
├── inference.py
├── prompts.py
└── sample-data/
    └── event-notes.txt
```

The completed reference is in `solution/`. Do not start there. Lab 3 tells you when and how to use progressive hints before consulting the solution.

## Your first workshop action

Open [`labs/00-readiness.md`](labs/00-readiness.md) now and run its verification command.

After its checkpoint, use the **Next lab** link at the bottom of the page.
