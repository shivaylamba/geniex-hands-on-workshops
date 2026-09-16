# Local workday copilot — application files

Attendees begin at [START-HERE](../../START-HERE.md), not by guessing which script to run. Instructors use [the walkthrough](../../INTERNAL-WALKTHROUGH.md).

| File | Responsibility | Learner interaction |
|---|---|---|
| [data/workday.json](data/workday.json) | Synthetic project note and trusted task records | Inspect, predict, then personalize |
| [app.py](app.py) | GenieX model loading, generation, evidence output | Trace the SDK call in 101 |
| [agent.py](agent.py) | Bounded loop, JSON parser, allowlist, observations | Explain in 201; challenge in 301 |
| [starter.py](starter.py) | Missing planning tool | Implement in 201 |
| [solution.py](solution.py) | Reference planning tool | Compare after attempting |
| [tests/test_copilot.py](tests/test_copilot.py) | Hardware-independent checks | Add an edge case in 301 |
| [WORKSHEET.md](WORKSHEET.md) | Predictions, experiments, demonstration | Complete throughout |

All terminal commands run from the repository root. Nothing here searches the user's files, sends messages, or modifies tasks. The fixed fixture is trusted application input except that its note text is treated as untrusted model context. Supporting arbitrary uploaded task databases would require additional schema, duration, and size validation.
