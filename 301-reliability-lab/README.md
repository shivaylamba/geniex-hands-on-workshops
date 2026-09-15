# 301: Validate, challenge, and measure the assistant

**Duration:** 40 minutes, then ten minutes of demos. **Previous:** [201](../201-evidence-assistant/README.md).

## What you will build

An acceptance policy, a controlled experiment, and an evidence-backed release decision. Valid JSON, authentic quotations, and correct answers are different properties.

## Prerequisites and files

Complete 201 or explicitly choose the reference selector for rehearsal. Reuse the same model/device. Edit [starter/policy.py](../workshops/geniex-bootcamp/starter/policy.py), read [fixture expectations](../workshops/geniex-bootcamp/data/cases.json), and complete [the worksheet](../workshops/geniex-bootcamp/WORKSHEET.md). [Detailed challenge and hints](../workshops/geniex-bootcamp/labs/301-evaluate-reliability.md).

## Step 1 — Predict what slips through (5 minutes)

The starter accepts anything JSON can parse. Predict its response to an array, an invented source, and this object:

```json
{"answer":"Cedar","source_id":"current-room","quote":"The workshop room is Maple."}
```

Ask separately: does it parse, obey the schema, quote a selected source, and answer correctly?

## Step 2 — Implement the contract (12 minutes)

Write `validate_answer(raw, selected)` returning `(bool, reasons)`:

- Reject malformed JSON without crashing.
- Require exactly three string fields: `answer`, `source_id`, `quote`; reject empty answers.
- Abstention requires `answer: unknown`, `source_id: none`, and an empty quote.
- Otherwise the source must be a selected current document, with a nonempty verbatim quotation.
- Give useful rejection reasons; do not secretly repair the model's output.

```powershell
$previousWorkshopTrack = $env:WORKSHOP_TRACK
try {
    $env:WORKSHOP_TRACK = 'starter'
    .\.venv\Scripts\python.exe -m pytest workshops/geniex-bootcamp/tests/test_challenges.py -k 'not retrieval' -q
} finally {
    $env:WORKSHOP_TRACK = $previousWorkshopTrack
}
```

Initially two checks pass and eight fail; the completed contract passes all ten. Remember `'' in text` is true in Python. Type-check untrusted output before reading its fields. The common runner separately rejects known token-limit stops.

## Step 3 — Change one variable and measure (10 minutes)

Write a hypothesis first: does a 24-token output ceiling reduce time at the cost of usable answers? Keep model, input, device, selector, and policy fixed.

```powershell
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --evaluate --repeats 2 --max-tokens 24 --output output/301-short.jsonl
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --evaluate --repeats 2 --max-tokens 160 --output output/301-long.jsonl
```

Read and calculate:

```powershell
$rows = @(Get-Content output/301-long.jsonl | ForEach-Object { $_ | ConvertFrom-Json })
$rows | Select-Object case,repeat,accepted,reference_pass,ttft_ms,generation_wall_ms,stop_reason
$rows | Measure-Object generation_wall_ms -Average -Minimum -Maximum
"Policy pass: $(@($rows | Where-Object accepted).Count)/$($rows.Count)"
"Fixture pass: $(@($rows | Where-Object reference_pass).Count)/$($rows.Count)"
"Joint pass: $(@($rows | Where-Object { $_.accepted -and $_.reference_pass }).Count)/$($rows.Count)"
```

Repeat for the short file. Report counts and denominators; load time is separate from generation. TTFT is not full response latency. Two repeats give a classroom observation, not a statistically established hardware benchmark.

`accepted` measures the policy plus truncation guard. `reference_pass` checks expected source IDs and answer words, not semantic truth. Manually review at least one accepted and rejected answer.

## Step 4 — Attack the checks (8 minutes)

The Cedar/Maple payload passes the reference provenance validator despite being false. Write `tests/test_my_policy.py` to demonstrate the gap or a targeted defense. Import `component` from `test_challenges` to target learner code consistently.

Now inspect the offline fixture. A supported “Yes” can fail because the checker expects “without internet” in the answer. Design a case separating a helpful paraphrase from a misleading answer that contains those words. Discuss false rejections as well as false acceptances.

Would a stricter rule reject valid paraphrases? Should the interface show sources and withhold uncertain answers instead of pretending they are trusted?

## Step 5 — Decide what is ready (5 minutes)

Run all challenge tests with `WORKSHOP_TRACK=starter`, without a `-k` filter, and your new tests. Sixteen green challenge checks establish this small contract, not production readiness.

Finish with one rate, one latency observation, one raw output, and one remaining risk. Choose unattended release, supervised source-viewing prototype, or no release. An evidence-backed “not ready” is a successful workshop outcome.

**Use the [90-second team demo format](../INTERNAL-WALKTHROUGH.md#8-present-it-to-the-team). Label reference code and published logs as such.**
