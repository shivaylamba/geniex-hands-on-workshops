# 201: Build an evidence-aware local assistant

**Duration:** 40 minutes. **Previous:** [101](../101-local-inference/README.md). **Next:** break, then [301](../301-reliability-lab/README.md).

## What you will build

Write the selector deciding which documents reach the model. Handle stale information, untrusted content, irrelevant questions, and a budget. This is lexical retrieval, not a vector database or a complete retrieval solution.

## Prerequisites and files

Complete 101 and reuse its device, environment, and model. No new download. Run everything from the repository root.

| File | Purpose |
|---|---|
| [starter/retrieval.py](../workshops/geniex-bootcamp/starter/retrieval.py) | Your implementation |
| [documents.json](../workshops/geniex-bootcamp/data/documents.json) | Current, archived, and untrusted inputs |
| [test_challenges.py](../workshops/geniex-bootcamp/tests/test_challenges.py) | Executable requirements |
| [Detailed challenge](../workshops/geniex-bootcamp/labs/201-build-context.md) | Progressive hints after an attempt |

## Step 1 — Classify and predict (5 minutes)

Read every document's status and text. Predict the selected IDs for room, laptop owner, and keynote speaker questions. Decide what should happen when there is no evidence.

Why should a keyword-heavy archived source lose? Why should document text not override the application's instructions? Write your reasoning. Trust labels are supplied fixture metadata; your selector does not establish trust by itself.

## Step 2 — Define a general policy (5 minutes)

Implement `select_context(question, documents, max_chars=360)`:

1. Reject nonpositive budgets with `ValueError`.
2. Keep only `current` documents.
3. Lowercase words and exclude common words that do not establish relevance.
4. Score positive question/document word overlap; exclude zero overlap.
5. Break equal scores by ascending document ID.
6. Count each source as `len(id) + len(text) + 4` characters. Include whole sources that fit; skip oversized ones and consider later ones.
7. Return an empty list if nothing qualifies. Never invent a source or hardcode answers.

The character convention is not a token-accurate context bound. Prompt and template overhead still matter.

## Step 3 — Implement and test (15 minutes)

Replace the first-document baseline. Decompose the work into eligibility, scoring, ordering, and budget. Test **your starter**:

```powershell
$previousWorkshopTrack = $env:WORKSHOP_TRACK
try {
    $env:WORKSHOP_TRACK = 'starter'
    .\.venv\Scripts\python.exe -m pytest workshops/geniex-bootcamp/tests/test_challenges.py -k retrieval -q
} finally {
    $env:WORKSHOP_TRACK = $previousWorkshopTrack
}
```

Initially all six retrieval tests fail; a correct implementation passes them. Do not edit assertions to make the report green. If stuck for five minutes, read one hint in the detailed challenge and explain it before continuing.

```powershell
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --evaluate --inspect
```

The room selection includes `current-room` and excludes archived/untrusted sources. Keynote selects nothing. Extra eligible sources mentioning workshop can fit; explain the relevance-versus-distraction cost.

## Step 4 — Make the supplied tests insufficient (8 minutes)

Create `workshops/geniex-bootcamp/tests/test_my_retrieval.py`. Use `from test_challenges import component` and call `component('retrieval').select_context(question, docs, budget)` on new fictional documents.

Assert behavior for a huge top-ranked document, a keyword-stuffed archived source, or deterministic ties. Run the new file using the same temporary `WORKSHOP_TRACK=starter` setting. Have your partner predict IDs and budget arithmetic before running it.

Probe `--question "Where is the session located?" --inspect`. If synonyms defeat lexical matching, document the limitation instead of adding a hardcoded answer.

## Step 5 — Reconnect to inference (7 minutes)

```powershell
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --policy solution --evaluate --output output/201-selected-context.jsonl
```

This uses **your selector** and the reference evidence validator to isolate retrieval. Compare `selected_ids`, `raw`, `accepted`, and `reasons`. Correct input can still produce malformed or unsupported output; rejection is not automatically a selector bug.

Checkpoint: six retrieval tests and your new case pass against the starter; your worksheet records a tradeoff and limitation. Open the [reference implementation](../workshops/geniex-bootcamp/solution/retrieval.py) only after an attempt and label any borrowed code honestly.

**Take five minutes, swap roles, then open [301](../301-reliability-lab/README.md).**
