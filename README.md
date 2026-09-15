# GenieX hands-on workshops

Build a local AI assistant on a Snapdragon Windows laptop, then improve its source selection and test its reliability. This is a community-authored collection, not an official Qualcomm training release.

**Team members and presenters: open [INTERNAL-WALKTHROUGH.md](INTERNAL-WALKTHROUGH.md) first.** It contains stepwise installation, execution order, expected results, troubleshooting, and a presenter rehearsal.

> [!IMPORTANT]
> Finish software installation and model caching before class. Use a supported Snapdragon Windows ARM64 device and native ARM64 Python. No additional model is downloaded between the three segments.

## Workshops

| Workshop | Hands-on outcome | Time | Materials |
|---|---|---:|---|
| 101: Local inference | Run CLI and SDK; diagnose stale evidence | 25 min | [Open workshop](101-local-inference/README.md) |
| 201: Evidence assistant | Implement source selection and a new test | 40 min | [Open workshop](201-evidence-assistant/README.md) |
| Break | Swap pair roles | 5 min | — |
| 301: Reliability lab | Build validation, attack outputs, measure tradeoffs | 40 min | [Open workshop](301-reliability-lab/README.md) |
| Demos | Defend a release decision | 10 min | [Team demo](INTERNAL-WALKTHROUGH.md#8-present-it-to-the-team) |

Total: 120 minutes, excluding setup. See the [new laptop rehearsal report](verification/TEAM-REHEARSAL.md) for actual results and limitations. Working commands do not imply every model answer is correct.

## Supporting materials

- [Small Python SDK example](101-local-inference/hello_geniex.py)
- [Learner code](workshops/geniex-bootcamp/starter/) and [reference code](workshops/geniex-bootcamp/solution/)
- [Common runner](workshops/geniex-bootcamp/app.py), [worksheet](workshops/geniex-bootcamp/WORKSHEET.md), and [instructor guide](workshops/geniex-bootcamp/INSTRUCTOR-GUIDE.md)
- [Automated presenter rehearsal](scripts/rehearse_workshop.py)

The numbered folders use the navigational style of the [UNO Q collection](https://github.com/aaishikasb/uno-q-workshops): prerequisites, setup, run, understand, and experiment. These GenieX lessons are independently authored; Arduino hardware instructions do not apply here.

This edition was developed on `codex/team-walkthrough` for a separate GenieX repository. The [original repository](https://github.com/shivaylamba/geniex-workshop) remains unchanged on main.

The [older standalone 101 materials](workshops/geniex-101/README.md) remain as supplemental references. Their original timing and advanced-topic proposals are not the current event plan.

## Single-file AI handoff

[`AI_AGENT_BUNDLE.md`](AI_AGENT_BUNDLE.md) contains a complete text snapshot of every other tracked repository file for AI systems that accept only one Markdown input.

Maintainers: stage new files, run `.\.venv\Scripts\python.exe scripts/build_ai_bundle.py`, then stage the bundle. Use `--check` to verify it matches the current tracked working-tree contents.
