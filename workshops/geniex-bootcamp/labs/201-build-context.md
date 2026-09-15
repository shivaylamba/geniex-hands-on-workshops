# 201 — Build context selection (40 minutes)

**Previous:** [101](101-first-inference.md). **Next:** five-minute break, then [301](301-evaluate-reliability.md).

## Your mission and deliverable

Replace [starter/retrieval.py](../starter/retrieval.py) with a general-purpose selector. You will decide which evidence reaches the model. Deliver a tested function, one new case, and a written tradeoff. Do not edit the runner to hardcode answers or remove difficult fixtures.

## 0–5 minutes: classify the evidence before coding

Read all six [documents](../data/documents.json). Mark which are eligible, which are outdated, and which contain instructions that must not be followed. Predict selected IDs for room, laptop owner, and keynote speaker questions. The fixture's `status` is a supplied trust decision; keyword matching alone must not override it.

With your partner, choose what happens when no trustworthy source matches. “Return every document” and “return no documents” have different hallucination risks. Write your decision.

## 5–10 minutes: define the contract

Implement `select_context(question, documents, max_chars=360)` with this teaching contract:

1. Reject nonpositive budgets with `ValueError`.
2. Consider only documents whose status is `current`.
3. Rank by overlap between meaningful lowercase words in the question and document text. You choose the stopwords; exclude common question/function words to avoid false matches.
4. Drop zero-overlap documents; break equal scores deterministically by document ID.
5. Return whole documents within the supplied budget. Count each as `len(id) + len(text) + 4`; skip one that does not fit and consider the next.
6. Return an empty list when nothing qualifies. Do not invent a source.

This character accounting is an exercise convention. JSON serialization, instructions, chat-template markers, and output also occupy model context. It is not a guarantee against tokenizer context overflow. Production code should budget with the actual tokenizer.

Discuss one limitation before coding: “location” and “room” may be semantically similar without sharing a token. This selector does not solve that.

## 10–25 minutes: implement and test

Edit only [starter/retrieval.py](../starter/retrieval.py) for the implementation. Run the retrieval tests against your code:

```powershell
$previousWorkshopTrack = $env:WORKSHOP_TRACK
try {
    $env:WORKSHOP_TRACK = 'starter'
    .\.venv\Scripts\python.exe -m pytest workshops/geniex-bootcamp/tests/test_challenges.py -k retrieval -q
} finally {
    $env:WORKSHOP_TRACK = $previousWorkshopTrack
}
```

The initial starter is intentionally wrong; failures are your work queue. Read each assertion. The default pytest command targets the **solution**, so it cannot establish that your edits work unless you set `WORKSHOP_TRACK=starter` as above.

Run the no-model inspection too:

```powershell
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --evaluate --inspect
```

Expected checkpoint: the room selection includes `current-room`, never `archive-room` or `untrusted-note`; the keynote question returns no documents. More than one eligible source may fit. Explain whether extra matches are useful or distracting.

<details><summary>Hint 1: if you are stuck after five minutes</summary>

Break the function into three stages: eligible candidates, scored candidates, budgeted output. Test them mentally on the room question. A lowercase set of words makes overlap a set intersection.

</details>

<details><summary>Hint 2: if ranking or budget is confusing</summary>

Use `re.findall(r"[a-z0-9]+", text.lower())` and remove a small stopword set. Store each positive overlap score alongside its document. Sort with key `(-score, document['id'])`. Maintain a running character total. An oversized first result must not stop consideration of a smaller later result.

</details>

<details><summary>Reference implementation: open only after an attempt</summary>

Compare [solution/retrieval.py](../solution/retrieval.py). Describe one difference from your approach and why it matters. Copying it without an explanation does not meet the build checkpoint.

</details>

## 25–33 minutes: make the supplied tests insufficient

Create `workshops/geniex-bootcamp/tests/test_my_retrieval.py`. Write an independent pytest test using new fictional documents, not just renamed expected answers. You can import the helper with `from test_challenges import component`, then call `component('retrieval').select_context(...)`.

Choose one adversarial scenario:

- An archived document repeats the question keywords many times.
- The highest-scoring eligible document cannot fit, but a lower-ranked one can.
- Two equal-score sources arrive in the opposite order; results must still be deterministic.

Before running it, have your partner predict both the selected IDs and the budget used. Run the same environment-scoped pytest command, replacing the test path with your new file. Do not inspect the solution to design the expected answer.

Then ask a synonym question such as “Where is the session located?” using `--question` with `--inspect`. Does lexical overlap miss the relevant source? Record this as a known limitation rather than hardcoding that single question into your function.

## 33–40 minutes: connect your code to the model

```powershell
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --policy solution --evaluate --output workshops/geniex-bootcamp/output/201-context.jsonl
```

Here the selector is **your code**; the evidence validator is the reference code so that you can evaluate retrieval without waiting for 301. Compare selected sources with the 101 baseline. Record a case where a correct source did not guarantee a correct or accepted answer. If none occurs, explain why that still does not prove reliability.

Checkpoint: retrieval tests pass against your starter, your new adversarial case passes, and your worksheet explains one relevance-versus-budget tradeoff. A small model may still fail the output format; that is not automatically a retrieval bug.

**Take the five-minute break. Swap driver/navigator. Next: [301](301-evaluate-reliability.md).**
