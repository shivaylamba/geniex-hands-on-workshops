# Lab 3 — Build the Local Briefing Assistant

**Time:** 35 minutes
**Goal:** Extend the working starter into a useful two-mode application.

Work in `starter/`. The completed behavior is visible in `solution/`, but use it only after the progressive hints.

## Stage 1 — Add actions mode

Change `prompts.py` so `build_messages()` accepts `actions`. Its contract is:

- return a Markdown table;
- use columns `Owner | Action | Due date`;
- include assigned and unresolved work; and
- write `unknown` rather than invent missing fields.

Use one row per distinct action, copy full dates, and do not convert current-state facts or general yes/no questions into action rows. If the notes ask who will do work, that is an unresolved action and its owner is `unknown`.

Then allow `brief` and `actions` in `app.py`.

## Stage 2 — Strengthen input handling

Add clear errors for:

- a path that is not a file;
- an empty file;
- non-UTF-8 content; and
- input longer than 12,000 characters.

## Stage 3 — Improve the experience

Add at least two:

- `--audience`;
- `--max-new-tokens`;
- `--no-stream`;
- `--save`; or
- a third `developer-update` mode.

## Test your build

```powershell
Push-Location .\workshops\geniex-101\starter
..\..\..\.venv\Scripts\python.exe .\app.py `
  --file .\sample-data\event-notes.txt `
  --mode actions
Pop-Location
```

Check the output against the source. Maya, Arjun, and Priya have explicit work. Printed signage and the help desk have no assigned owner. Do not accept invented dates or owners.

The completed solution performs a deterministic structural check on the generated action table. A structural pass does not prove the facts are correct; it only confirms the required Markdown shape. If the small workshop model violates the contract, report and discuss the failure instead of silently accepting it.

## Progressive hints

1. **Concept:** keep system rules separate from source data and wrap the notes in explicit delimiters.
2. **API:** the GenieX-specific path does not need to change when adding a new application mode.
3. **Code:** compare your function signatures with `solution/prompts.py` and `solution/app.py` before reading their bodies.

## Next lab

Continue to [`04-observe-and-improve.md`](04-observe-and-improve.md).
