# Start here: your local workday copilot

You will build an assistant that turns project notes and an available time budget into a proposed plan and a draft teammate update. All supplied data is fictional. Nothing is sent.

## Before you start

You need basic Python functions, lists, dictionaries, exceptions, and a prepared supported Snapdragon Windows ARM64 device. No training, fine-tuning, cloud account, or Arduino board is required for this application. A partner's prepared laptop is fine.

Complete [the setup and readiness gates](INTERNAL-WALKTHROUGH.md#setup-before-class). That page includes the exact branch to clone, installation sources, model cache details, environment commands, and the first device run. Do not start the workshop timer while downloading.

Keep three things open: this repository's root PowerShell, your editor, and [your worksheet](workshops/workday-copilot/WORKSHEET.md). All commands assume the repository root.

## Open these files in this order

1. **[101-local-inference/README.md](101-local-inference/README.md)** — start here after setup. Understand GenieX and generate a useful summary.
2. **[201-evidence-assistant/README.md](201-evidence-assistant/README.md)** — implement `check_plan` in [starter.py](workshops/workday-copilot/starter.py), then run the copilot using your code.
3. Take a five-minute break and swap pair roles.
4. **[301-reliability-lab/README.md](301-reliability-lab/README.md)** — challenge the tool boundary, compare budgets, and assess the untrusted draft.
5. Use the final section of your worksheet for a 60-second demo.

## How to know you are done

You can identify the GenieX call, show your own tested function, explain an actual tool observation, and demonstrate one failure or limitation. Merely running the supplied solution is a presenter rehearsal, not completion of the learner work.

Bare pytest uses the reference implementation. The 201 lab explicitly sets `COPILOT_TRACK=starter` so you test your edits.

## If you get stuck

Write your prediction first, use the staged lab hints, then ask a partner. Open the reference solution only after trying. Without supported hardware, complete the Python tests and trace-reading exercises; label that **code-only**, not local inference.

Each command refuses to overwrite its evidence file. Change the filename for every repeat. A blocked run is evidence to inspect, not a reason to remove the safety checks.
