# Qualcomm Snapdragon Multiverse Workshops

Reusable, hands-on workshop materials for developers building with Qualcomm platforms.

## Workshops

- **Participants start here:** [Two-hour GenieX 101 → 201 → 301](START-HERE.md)
- [Workshop structure and learning objectives](workshops/geniex-bootcamp/WORKSHOP-PLAN.md)
- [Detailed labs, code, and assessment](workshops/geniex-bootcamp/README.md)
- [Facilitator delivery guide](workshops/geniex-bootcamp/INSTRUCTOR-GUIDE.md)
- [Device verification and recorded experiments](workshops/geniex-bootcamp/VERIFICATION.md)

101 is a 25-minute introduction. 201 adds 40 minutes of implementing source selection; 301 adds 40 minutes of validation, adversarial testing, and measured experiments. A five-minute break and ten-minute demo complete the two hours. Participants write code, author new cases, and defend a release decision.

The [older standalone 101 materials](workshops/geniex-101/README.md) remain as supplemental references. Their original timing and advanced-topic proposals are not the current event plan.

## Single-file AI handoff

[`AI_AGENT_BUNDLE.md`](AI_AGENT_BUNDLE.md) contains a complete text snapshot of every other tracked repository file for AI systems that accept only one Markdown input.

Maintainers: stage new files, run `.\.venv\Scripts\python.exe scripts/build_ai_bundle.py`, then stage the bundle. Use `--check` to verify it matches the current tracked working-tree contents.
