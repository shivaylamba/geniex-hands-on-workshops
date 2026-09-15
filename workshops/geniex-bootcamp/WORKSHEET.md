# Participant worksheet

Pair / names: __________  Device: __________  Date: __________

Use your own notes or a local copy. Do not commit personal information or private prompts to the public repository. All provided event facts are fictional.

## 101: predict before running

1. Expected room and source ID: __________
2. What the first-document baseline will select: __________
3. Observed `selected_ids` and raw answer: __________
4. Why this is an input-selection, generation, or validation issue: __________
5. In your own words: model vs runtime vs compute device: __________

## 201: make a policy decision

| Question | Predicted selected IDs | Actual selected IDs | Why eligible / excluded? |
|---|---|---|---|
| Workshop room | | | |
| Laptop owner | | | |
| Keynote speaker | | | |
| Your new case | | | |

- Our stopword / ranking choice and rationale: __________
- Budget used for our new case (show arithmetic): __________
- What our selector does when the first result cannot fit: __________
- New test name, expected result, actual result: __________
- A synonym question that defeats lexical matching: __________
- One change we would investigate next, and its cost: __________

## 301: state a hypothesis, then measure

Hypothesis: __________

Independent variable: __________  Fixed variables: __________

Model/version/device: __________  Run filenames: __________

| Configuration | Cases × repeats | Contract pass | Fixture pass | Joint pass | Mean generation wall ms | TTFT range ms | Truncations |
|---|---|---|---|---|---|---|---|
| Short output | | | | | | | |
| Longer output | | | | | | | |

Record counts as `numerator/denominator`, not only percentages. Exclude model loading from generation wall time and report load separately: __________

Manual review:

| Case / raw answer | Contract result | Fixture result | Human judgment and source | What failed: system or evaluator? |
|---|---|---|---|---|
| Accepted case | | | | |
| Rejected case (or explain none) | | | | |
| Peer-authored case | | | | |

- Did the data support the hypothesis? What alternative explanation remains? __________
- Why a real quotation can accompany a false answer: __________
- One false rejection or false acceptance in the fixture checker: __________
- Our new test and what it still cannot prove: __________
- How the UI should behave after rejection: __________

## Final demo

Prepare a 90-second demo; the instructor will sample pairs and collect the rest asynchronously:

1. **20 seconds:** show your selector and the policy decision you made.
2. **20 seconds:** show your validator and one rejected answer.
3. **30 seconds:** show one experiment result and one adversarial or evaluator failure.
4. **20 seconds:** choose unattended release, supervised source-viewing prototype, or do not ship. Explain what evidence would change your decision.

Release decision: __________

Remaining risk and next test: __________

Completion means you can defend these answers. Green reference tests or copied solution code alone are insufficient.
