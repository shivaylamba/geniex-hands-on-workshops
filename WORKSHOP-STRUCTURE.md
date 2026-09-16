# Workshop structure — GenieX local workday copilot

**Audience:** developers comfortable with basic Python; no prior model-training experience.

**Promise:** understand what GenieX does, then build a local assistant that reads a project note, chooses tasks within a time budget, and drafts a review-only teammate update.

**Format:** 120 minutes, one progressively deeper project, one prepared supported Snapdragon Windows ARM64 device per pair. Setup and model downloads are prework. 101/201/301 are segments of this workshop, not three separately timed courses.

| Segment | Time | Explain | Learner decision/build | Evidence |
|---|---:|---|---|---|
| [101](101-local-inference/README.md) | 25 | Model vs runtime vs application; first SDK call | Predict and change the project-note summary | Two outputs + architecture explanation |
| [201](201-evidence-assistant/README.md) | 40 | Action → host tool → observation → next action | Implement task lookup, sums, and budget validation | Own passing tests + actual agent trace |
| Break | 5 | — | Swap driver/reviewer | — |
| [301](301-reliability-lab/README.md) | 40 | Permission boundaries and model failure | Add an edge-case test, run comparisons, improve one behavior | New test + observations + limitation |
| Share | 10 | What is and is not ready | Defend a release judgment | 60-second demo |

## Roles and files

- Attendee opens [START-HERE.md](START-HERE.md), then the three numbered lab READMEs.
- Workshop lead opens [INTERNAL-WALKTHROUGH.md](INTERNAL-WALKTHROUGH.md) for setup, timing, questions, expected reasoning, and recovery.
- Learner edits [starter.py](workshops/workday-copilot/starter.py) and adds a test in [test_copilot.py](workshops/workday-copilot/tests/test_copilot.py).
- Everyone records evidence in [WORKSHEET.md](workshops/workday-copilot/WORKSHEET.md).
- Reviewer reads [verification](verification/WORKDAY-COPILOT.md), including blocked runs and inaccurate prose.

## Assessment

Can the participant explain GenieX's role, implement the tool, identify real observations, test a failure, and state a justified limitation? The output must remain a human-reviewed proposal. Unsupported-device/code-only participation does not count as an inference test.

## Intentionally outside this workshop

No fine-tuning, arbitrary filesystem access, real email/calendar integration, shell tools, cloud credentials, production agent framework, or cross-device benchmark. These are follow-on workshop choices, not hidden prerequisites.

For rationale and alternative use cases, read [USE-CASE-DESIGN.md](workshops/workday-copilot/USE-CASE-DESIGN.md). For a reusable 60/90/120-minute scaffold, use [Qualcomm AI Topic](https://github.com/shivaylamba/qualcomm-ai-workshop-template).
