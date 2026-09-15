# 301 — Validate, attack, and evaluate (40 minutes)

**Previous:** [201](201-build-context.md). **Finish:** [final demo](../WORKSHEET.md#final-demo).

## Your mission and deliverable

The model is an untrusted text producer. Build an acceptance policy, measure its effect, and show a failure that survives your checks. Deliver [starter/policy.py](../starter/policy.py), an experiment table, and a release decision. “Everything parsed” is not the success criterion.

## 0–5 minutes: predict what the baseline accepts

The starter returns success for anything `json.loads` accepts. Without running it, predict its response to:

```json
[]
```

```json
{"answer":"Cedar","source_id":"current-room","quote":"The workshop room is Maple."}
```

```json
{"answer":"Maple","source_id":"invented","quote":"The room is Maple."}
```

Which is valid JSON? Which obeys the object schema? Which has a genuine source and quotation? Which actually answers the room question correctly? These are separate checks.

## 5–17 minutes: implement an evidence contract

Replace `validate_answer(raw, selected)` in the starter. Return `(accepted_boolean, list_of_reasons)`; do not raise on malformed model text. Requirements:

1. Parse JSON and require an object with **exactly** `answer`, `source_id`, and `quote`, all strings.
2. Require a nonempty answer.
3. Allow abstention only as `answer: "unknown"`, `source_id: "none"`, and an empty quote. Case-insensitive/trimmed `unknown` is acceptable.
4. Otherwise require a source ID in the selected current documents, plus a nonempty quote that occurs exactly in that source's text.
5. Return explanatory rejection reasons. Do not silently repair malformed JSON; that would hide a failure in this experiment.

Run your policy tests:

```powershell
$previousWorkshopTrack = $env:WORKSHOP_TRACK
try {
    $env:WORKSHOP_TRACK = 'starter'
    .\.venv\Scripts\python.exe -m pytest workshops/geniex-bootcamp/tests/test_challenges.py -k 'not retrieval' -q
} finally {
    $env:WORKSHOP_TRACK = $previousWorkshopTrack
}
```

<details><summary>Hint 1</summary>

Validate types before reading fields. A list is valid JSON but not the required object. Build a dictionary mapping selected IDs to documents; check membership before checking the quote.

</details>

<details><summary>Hint 2 / reference after an attempt</summary>

Handle `source_id == 'none'` as a separate branch. In the grounded branch, reject whitespace-only quotes before substring checking: the empty string is contained in every string. Compare [solution/policy.py](../solution/policy.py) only after trying.

</details>

The common runner also withholds token-limit-truncated generations. A rejected result is a result: show the reason and allow a user to rephrase or consult the source. Do not display rejected raw text as a trusted answer.

## 17–27 minutes: run a controlled experiment

Choose a hypothesis **before** running. Suggested: “A 24-token output limit is faster but causes more truncation than 160 tokens.” Keep model, device, documents, retrieval, policy, and questions fixed. Only change the token limit.

```powershell
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --evaluate --repeats 2 --max-tokens 24 --output workshops/geniex-bootcamp/output/301-short.jsonl
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --evaluate --repeats 2 --max-tokens 160 --output workshops/geniex-bootcamp/output/301-long.jsonl
```

Each command runs five cases twice, with model state reset per case. They load the model once per command. Repeated outputs can still be identical; two repeats are a classroom sample, not a statistical benchmark. If class time is tight, use one repeat and label the reduced sample. Existing output files are protected: choose a fresh filename when rerunning.

Read the JSONL and summarize your table:

```powershell
$experimentRows = Get-Content workshops/geniex-bootcamp/output/301-long.jsonl | ForEach-Object { $_ | ConvertFrom-Json }
$experimentRows | Select-Object case, accepted, reference_pass, ttft_ms, generation_wall_ms, stop_reason
$experimentRows | Measure-Object -Property generation_wall_ms -Average -Minimum -Maximum
```

Report three distinct rates:

- **Contract pass:** `accepted` is true: schema, source, quote, and no known truncation.
- **Fixture answer pass:** `reference_pass` is true: expected source and simple expected/forbidden answer terms.
- **Joint pass:** both are true. Neither individual rate is sufficient.

The fixture checker is deliberately narrow: substring checks miss paraphrases and can reward misleading sentences containing the expected word. It is not a semantic truth oracle. Include manual review of at least one accepted answer and one rejected answer, if present.

Measure time to first token separately from generation wall time and model load time. The pinned GenieX 0.5.0 implementation reports TTFT in microseconds, normalized by this runner to milliseconds. Do not compare load time with per-answer latency or claim a precise speedup from one observation.

## 27–35 minutes: adversarial peer review

Give your partner this apparently grounded payload:

```json
{"answer":"Cedar","source_id":"current-room","quote":"The workshop room is Maple."}
```

The reference evidence validator accepts it when the current-room source is selected. The room fixture check rejects it. Explain the gap: an authentic quotation does not prove that the answer follows from it.

Write a test in `tests/test_my_policy.py` using `from test_challenges import component`. Demonstrate this limitation or add a targeted defense for a newly defined case. If you strengthen the policy, explain why your rule may reject valid paraphrases. Do not claim universal semantic verification from a keyword rule.

Also add one fictional question to a copied evaluation set or discuss a proposed fixture with expected evidence: an unknown fact, a contradictory current source, or an untrusted instruction. What would a safe answer be? The runner uses `data/cases.json`; edit that local file only if you intend to rerun the expanded set and adjust its expected-source/term fields. Do not reuse the five supplied cases as both your only development data and proof of generalization.

## 35–40 minutes: decide, do not just demonstrate

Complete the worksheet: would you ship an unattended assistant, a source-viewing prototype, or neither? Support the decision with one observed output, one rate, one latency observation, and one unresolved risk. An honest “not ready” with a useful diagnosis is a successful lab outcome.

Run all bootcamp tests against your starter before the demo, using the same temporary environment variable and the directory `workshops/geniex-bootcamp/tests`. If blocked, show your failing assertion and what it teaches; do not silently switch to the solution and claim completion.

**Finish with the [final demo](../WORKSHEET.md#final-demo).**
