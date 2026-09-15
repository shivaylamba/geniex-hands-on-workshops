# GenieX: 101 → 201 → 301

> **Self-guided team edition:** start with [the internal walkthrough](../../INTERNAL-WALKTHROUGH.md) and the numbered top-level workshop folders. The implementation and detailed challenge resources below are shared by that edition.

A two-hour, code-first workshop. **[Participants start here](../../START-HERE.md).**

Build one progressively more reliable local assistant using the same small cached model throughout. 101 introduces inference; 201 adds source selection; 301 adds validation, adversarial tests, and evaluation. The level numbers describe progression within this event, not separate two-hour courses.

- [Exact structure and learning objectives](WORKSHOP-PLAN.md)
- [101 lab](labs/101-first-inference.md), [201 lab](labs/201-build-context.md), [301 lab](labs/301-evaluate-reliability.md)
- [Participant worksheet](WORKSHEET.md)
- [Instructor guide and answer key](INSTRUCTOR-GUIDE.md)
- [Device verification](VERIFICATION.md)

## Repository map

| Path | Purpose |
|---|---|
| `app.py` | Shared GenieX runner: inspect, infer, evaluate, and save JSONL |
| `data/documents.json` | Fictional event documents, including outdated and untrusted records |
| `data/cases.json` | Five known-answer cases; deliberately small, not a production benchmark |
| `starter/retrieval.py` | Working but incorrect baseline to replace in 201 |
| `starter/policy.py` | JSON-only acceptance baseline to replace in 301 |
| `solution/` | Reference implementations, opened only after attempting the exercises |
| `tests/test_challenges.py` | Offline implementation checks; solution is the default target |
| `verification/` | Recorded local-model runs, including failures |
| `output/` | Ignored directory for your own experiment logs |

There are no credentials, cloud calls, paid APIs, embeddings downloads, or vector database dependencies in the application. Setup requires internet. Offline operation must be checked after caching on each event machine. Do not enter private event or attendee data during demonstrations.
