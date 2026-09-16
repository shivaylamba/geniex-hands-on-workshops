# GenieX: build a local workday copilot

“I have an hour. Read my project notes, help me choose what to do next, and draft an update.”

Build that application on a Snapdragon laptop in two hours. Start with a useful summary, add a model-decided tool loop, then challenge its decisions and permissions. This community workshop is not an official Qualcomm training release.

**Attendees: [START-HERE.md](START-HERE.md). Instructors and self-guided team members: [INTERNAL-WALKTHROUGH.md](INTERNAL-WALKTHROUGH.md).**

## What is GenieX doing here?

GenieX supplies local model execution and developer interfaces. Our Python application supplies tool permissions, time-budget checks, the loop, and human-review rules. The model suggests actions; ordinary code decides what can actually happen. See [the architecture and use-case rationale](workshops/workday-copilot/USE-CASE-DESIGN.md).

## Two-hour flow

The dedicated [WORKSHOP-STRUCTURE.md](WORKSHOP-STRUCTURE.md) maps objectives, learner decisions, files, and assessment.

| Segment | Minutes | What participants produce |
|---|---:|---|
| [101: Understand and run](101-local-inference/README.md) | 25 | A local project-note summary and architecture sketch |
| [201: Build the copilot](201-evidence-assistant/README.md) | 40 | Their own tested planning tool and an actual agent trace |
| Break / swap roles | 5 | A new driver and reviewer |
| [301: Challenge and improve](301-reliability-lab/README.md) | 40 | An edge-case test, two experiments, and a release judgment |
| Share | 10 | A 60-second demo explaining one limitation |

Setup and downloads happen before the clock starts. This is one progressive application, not three unrelated demonstrations. Timings are instructional targets, not novice-pilot measurements.

## What gets built?

The copilot can read one synthetic project note, list four tasks, check a proposed plan against the user's available minutes, and draft text. It cannot send messages, execute shell commands, browse files, or edit tasks. It saves an evidence JSON file only at the output path chosen by the human running the CLI.

- [Working application](workshops/workday-copilot/app.py), [agent loop](workshops/workday-copilot/agent.py)
- [Learner function](workshops/workday-copilot/starter.py), [reference implementation](workshops/workday-copilot/solution.py), [tests](workshops/workday-copilot/tests/test_copilot.py)
- [Participant worksheet](workshops/workday-copilot/WORKSHEET.md)
- [New laptop verification and limitations](verification/WORKDAY-COPILOT.md)
- [Reusable Qualcomm workshop template](https://github.com/shivaylamba/qualcomm-ai-workshop-template)

## Branch and earlier editions

This redesign lives on `codex/geniex-workday-agent`. Main remains unchanged. The old event-information application in `workshops/geniex-bootcamp/` and standalone `workshops/geniex-101/` are legacy references, **not the attendee route for this branch**. Their tests and historical verification remain available; they do not establish that this new copilot works. The retained 201 directory name exists for link compatibility, not because source selection is still the central project.

[AI_AGENT_BUNDLE.md](AI_AGENT_BUNDLE.md) is the single-file snapshot of tracked contents. Maintainers stage new files, run `python scripts/build_ai_bundle.py`, then stage the regenerated bundle. Use `--check` to verify it.
