# Workshop structure: two hours of building with GenieX

> **Historical plan.** Use [the current workday-copilot structure](../../WORKSHOP-STRUCTURE.md) for this branch. The source-selection project below is retained for reference.

## Outcome and scope

Participants leave with a local assistant that selects evidence, generates an answer on Snapdragon, rejects several classes of invalid output, and records a small evaluation. They must explain a remaining failure and defend a release decision. A plausible answer is not enough.

This replaces the short introductory build as the main event. **101 is only the first 25 minutes.** The next 80 minutes are two increasingly demanding implementation segments. Setup is prework. Total scheduled time is exactly 120 minutes, including a five-minute break and ten-minute demo.

| Segment | Minutes | Core teaching | Learner work | Observable completion |
|---|---:|---|---|---|
| 101 | 25 | Inference, token/context budgets, model/runtime/device distinction | Predict, run, trace, diagnose stale evidence | Explain why the room answer is wrong without blaming everything on the model |
| 201 | 40 | Retrieval as a policy; relevance, trust, budgets, abstention | Implement filtering and ranking, design a new fixture, test a constraint | Retrieval checks pass and unseen data works without hardcoded answers |
| Break | 5 | — | Swap pair roles | — |
| 301 | 40 | Output contracts versus semantic correctness; quality/latency measurement | Implement a validator, run A/B experiments, attack a peer's claim | Validator checks pass, measurements recorded, a limitation demonstrated |
| Demo | 10 | Evidence-based communication | Show code, failed case, tradeoff, release decision | Rubric supported by evidence |

The design uses a repeated **brief explanation → prediction → build → test → reflection** pattern. Instructor exposition occupies about 20–25 minutes across the entire event; the rest is learner investigation, implementation, discussion, break, and demos. The schedule is a delivery design, not a claim of completed live classroom timing validation.

## Architecture learners should understand

```text
Question + local documents
          |
    201 source selection (Python, CPU; trust + relevance + budget)
          |
    Chat template + selected context
          |
    GenieX model / runtime -> Snapdragon compute (NPU in this release)
          |
    Generated text + timing profile
          |
    301 output checks (Python, CPU) -> accept or withhold + reason
          |
    Fixture checks and human review -> release decision
```

On-device inference does not mean every line of Python runs on the NPU. Model loading, prompt construction, retrieval, generation, and validation are different responsibilities. Q4_0 describes quantization, not a device. Context contains input instructions and source text; output tokens need room too. A character budget is an intentionally simple teaching constraint, **not a tokenizer-accurate context bound**.

GenieX provides a common interface over supported inference runtimes. Its Python API supports loading, chat templating, generation, and profiling. The platform documentation describes runtime and chipset differences; support must be checked per device. See [official Python API](https://geniex.aihub.qualcomm.com/en/run/python/api-reference) and [supported platforms](https://geniex.aihub.qualcomm.com/en/get-started/platforms), checked 15 September 2026. This release uses GenieX 0.5.0 and a cached GGUF; it does not ask learners to compile a model.

### Broader Qualcomm context (two minutes, not a product tour)

Situate this within the user's Snapdragon Multiverse workshop program: this module teaches **GenieX local application development**. AI Hub model preparation and deployment and Arduino UNO Q hardware application work are separate workshop topics, not prerequisites or dependencies here. Do not imply this Windows NPU lab runs unchanged on UNO Q. Link the [GenieX introduction](https://geniex.aihub.qualcomm.com/en/get-started/what-is-geniex) and [upstream repository](https://github.com/qualcomm/GenieX) for further study.

## Why these advanced segments belong here

201 changes the data path, not just the prompt. Learners must choose between relevant, obsolete, and malicious content under a budget. 301 changes the acceptance policy and experimental method: valid JSON, grounded quotation, and correct answers are separate properties. Both segments require code and a decision for which a copied command is insufficient.

This is retrieval-augmented generation using a tiny lexical selector, not a claim to teach production vector search. Trust labels are supplied fixtures; a production ingestion system would have to establish them. The reference validator cannot prove semantic entailment or prevent every prompt injection. These boundaries are assessed explicitly.

## Delivery and assessment

- Pair developers where useful, one tested device per pair. Keep the model cached before the clock starts.
- Do not reveal the reference code until a learner has made an attempt and written a prediction.
- Require a new case, not just green supplied tests. A passing reference fixture set is not a production-readiness certificate.
- Use the worksheet and 10-point demo rubric in the instructor guide. Failed inference is valid evidence when diagnosed honestly.
- Keep the main path small-model, text-only. No fine-tuning, model compilation, multimodal inputs, agent tool execution, or network services in the two-hour release.

## Optional three-hour extension (add 60 minutes)

The 120-minute version is complete on its own. If the event is three hours, add: 20 minutes implementing an improved relevance strategy against peer-authored cases; 20 minutes testing an explicit CPU-versus-NPU comparison if both paths are prepared; 15 minutes designing a user-facing withheld-answer experience with error reasons; five minutes for a second release review. Keep model, prompt, question set, token limit, and measurement definitions fixed in the device comparison. Do not hide new downloads inside the extension.

## Publication and maintenance action plan

| Item | Owner role | Release gate |
|---|---|---|
| Code, detailed labs, reference solutions, and tests | Workshop maintainer | Tests and a real-device evaluation recorded |
| Participant navigation and single-file handoff | Workshop maintainer | All current files included; links checked |
| Event-machine preparation | Event technical lead | Each machine passes setup and disconnected-network rehearsal |
| Live timing pilot with two novice participants | Instructor | Check actual task durations and adjust hints before the first event |
| New chipset or dependency version | Technical lead | Re-run device verification; publish version and measured limitations |
| Event feedback | Instructor | Record where pairs needed help; update next release without weakening tasks |

The first two items are repository deliverables. The live timing pilot and fleet/network rehearsal remain organizer tasks; a local execution test cannot substitute for them.
