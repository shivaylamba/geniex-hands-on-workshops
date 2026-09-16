# Why a workday copilot?

## Selection criteria

The participant should recognize the problem immediately, produce something they could adapt, and make real engineering decisions. The workshop must explain GenieX before introducing agent behavior. It should work with the already-cached small model, need no live service credentials, and keep side effects out of a beginner room.

| Candidate | Familiar outcome | Teaching advantage | Why not the primary build? |
|---|---|---|---|
| Notes-to-actions workday copilot | Choose useful work and draft an update | Model decisions + deterministic tools + review boundary | Selected; small synthetic fixture keeps setup predictable |
| Study-session planner | Turn study notes into a time-boxed plan | Same tools, easy personalization | Good alternative audience skin; not separate runtime work |
| Local document Q&A | Ask questions about personal documents | Grounding and retrieval | Valuable later, but source-selection mechanics dominated the earlier edition |
| Travel/booking agent | Produce an itinerary and book it | Recognizable but many external dependencies | Live data, credentials, transactions, and costs distract from GenieX |
| Autonomous developer agent | Read and change a codebase | Powerful advanced application | Shell and filesystem authority are inappropriate for this introductory scope |

## One application, progressively deeper

101 answers “what is GenieX and how do I call a local model?” through summarization.

201 answers “how does a model become part of an application that does useful work?” through a tool loop and a learner-written planning function.

301 answers “what must ordinary software enforce when a model is unreliable?” through bad requests, constrained budgets, injection, tests, and human review.

The useful artifact is a reviewable plan and update, not autonomous execution. Participants can adapt the fixture to a study session, community project, or daily team planning without changing the basic interfaces. The portfolio example is illustrative, not required domain knowledge.

## Architecture and boundaries

```text
User budget + goal
        |
Python orchestrator -- formatted messages --> GenieX --> local model
        ^                                            |
        |                 proposed JSON action <-----+
        |
strict parser / permission check
        |
read note | list tasks | check plan --> observation --> next model call
        |
finish only after a valid plan --> proposed plan + untrusted draft --> human review
```

The model selects requests; the application executes only allowlisted operations. No external agent framework or native function-call protocol is required. A two-field JSON interface keeps the implementation inspectable. Models may still choose badly or fail to follow that protocol.

GenieX is the local generation layer. Its official overview describes runtime/backend and language-interface choices; this workshop selects the Python + GGUF route instead of teaching all combinations. The app's tools, permissions, and loop are our own Python code. [Official GenieX overview](https://geniex.aihub.qualcomm.com/en/get-started/what-is-geniex), [source repository](https://github.com/qualcomm/GenieX).

The SDK integration uses loading, chat formatting, generation, and state reset. Context and output are bounded; short outputs are checked before use. We do not promise semantic correctness because text matches a JSON schema. [Official Python API](https://geniex.aihub.qualcomm.com/en/run/python/api-reference).

## What we deliberately defer

Live calendars, email sending, arbitrary local file access, shell tools, retrieval indexes, production UI, deployment packaging, multimodal input, model compilation, and cross-device benchmarks. Each deserves separate prerequisites and risk controls. GenieX serving and other interfaces can be subsequent workshops, not extra beginner setup.

## Teaching pattern and sources

We adopt prerequisites up front, a sequential working build, short checkpoints, and learn-by-changing behavior. The original text, examples, timings, code, and exercises here are independently authored. NVIDIA's self-paced onboarding uses a staged hands-on progression; its instructor-led training emphasizes practical application. Those are instructional references, not an assertion of certification or endorsement.

- [NVIDIA AI Workbench onboarding project](https://github.com/NVIDIA/workbench-example-onboarding-project)
- [NVIDIA instructor-led workshops](https://www.nvidia.com/en-us/training/instructor-led-workshops/)
- [Qualcomm AI Hub getting started](https://workbench.aihub.qualcomm.com/docs/hub/getting_started.html) for a separate compilation/profiling track; cloud-hosted device jobs are not equivalent to this laptop's local inference.

Reviewed 2026-09-16. Current capability statements should be rechecked before future delivery. The two-hour schedule is a proposed teaching design, not a measured novice completion guarantee.
