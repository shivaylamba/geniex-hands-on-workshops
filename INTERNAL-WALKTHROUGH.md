# Internal walkthrough — run and teach the local workday copilot

Share this page with teammates who want to rehearse independently. It is a public instructor note, not a private operations document. Attendees follow [START-HERE.md](START-HERE.md).

## The story you are teaching

“I have an hour before my next meeting. Read my project note, select useful work that fits, and draft an update.”

101 teaches the local model call. 201 turns it into a bounded tool-using application. 301 separates successful execution from reliable behavior. The user gets a proposed plan, not an automatically executed workday. Nothing is sent and no calendar is connected.

[The rationale](workshops/workday-copilot/USE-CASE-DESIGN.md) explains alternatives and the technology boundaries. [The verification report](verification/WORKDAY-COPILOT.md) distinguishes real laptop runs from scripted tests.

## Setup before class

### 1. Check the device

This edition targets supported Snapdragon Windows ARM64 laptops. Our rehearsal machine is a Dell Latitude 7455, Snapdragon X Elite X1E80100, about 32 GB RAM. That is an observation, not a minimum specification.

```powershell
Get-CimInstance Win32_Processor | Select-Object Name
Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer,Model,SystemType
```

Compare another device with [Qualcomm's supported platforms](https://geniex.aihub.qualcomm.com/en/get-started/platforms). An x64 Intel/AMD laptop is not proof of this NPU path. Pair on a supported prepared device; code-only participation is possible but must be labeled.

### 2. Install the official CLI

Follow [Windows ARM64 installation](https://geniex.aihub.qualcomm.com/en/run/cli/install/#windows-arm64). Use the official installer and your organization's software approval process. Do not disable operating-system protections to make installation work.

In a new PowerShell:

```powershell
Get-Command geniex -ErrorAction SilentlyContinue
geniex version
geniex config get chipset
```

If the command is not on PATH, check the actual installation location. On our prepared device it is:

```powershell
$geniexCli = Join-Path $env:LOCALAPPDATA 'GenieX CLI\geniex.exe'
Test-Path -LiteralPath $geniexCli
```

Only if that returns True:

```powershell
Set-Alias -Name geniex -Value $geniexCli
geniex --help
geniex version
```

The alias lasts only for this terminal. CLI 0.5.0 is our recorded version; rehearse if your approved installation differs. Stop here if the executable or chipset cannot be discovered.

### 3. Clone this exact branch

Use a fresh directory for rehearsal, so you do not overwrite participant work:

```powershell
git clone --branch codex/geniex-workday-agent https://github.com/shivaylamba/geniex-hands-on-workshops.git geniex-workday-workshop
cd geniex-workday-workshop
git branch --show-current
Test-Path workshops/workday-copilot/app.py
```

Expected branch: `codex/geniex-workday-agent`; expected path result: True. Existing clones should inspect `git status` and preserve edits before switching. Do not reset learner code.

Every command below runs from this repository root.

### 4. Create native Python environment

Follow the [official Python installation guidance](https://geniex.aihub.qualcomm.com/en/run/python/install). Have IT select a maintained ARM64 Python build. Our already-installed 3.12.8 was used for rehearsal; this is not a recommendation to install that old release.

```powershell
python -c "import platform,sys; print(platform.python_version()); print(platform.machine()); print(sys.executable)"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -c "import platform,geniex; print(platform.machine()); print(geniex.version())"
```

Confirm native ARM64, not emulated AMD64. The pinned dependencies include GenieX 0.5.0 and pytest 9.1.1. No environment activation or machine-wide PowerShell policy change is needed. Use an alternate new environment name if `.venv` already contains unrelated work.

Check runtime discovery:

```powershell
.\.venv\Scripts\python.exe -c "import geniex; geniex.init(); print(geniex.get_runtime_list()); print(geniex.get_compute_unit_list('llama_cpp')); geniex.deinit()"
```

Our output includes llama.cpp and a Hexagon/HTP compute entry. Discovery alone is not an inference test.

### 5. Cache the model once

```powershell
geniex pull --model-type llm unsloth/Qwen3.5-2B-GGUF:Q4_0
geniex list
```

The text weights are approximately 1.13 GiB; the current download also includes an approximately 1.23 GiB projector, for around 2.4 GiB of model cache. Allow additional space for software. We use text only. Check model distribution terms before redistributing cached assets. Initial installation/downloads require connectivity; cached execution was tested on a connected machine, not an air-gapped one.

See the [official quickstart](https://geniex.aihub.qualcomm.com/en/run/cli/quickstart) for the CLI and runtime distinction. Keep the same model throughout this workshop.

### 6. Pass the real readiness gate

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe workshops/workday-copilot/app.py --mode summary --output output/preflight-summary.json
.\.venv\Scripts\python.exe workshops/workday-copilot/app.py --track solution --budget 60 --output output/preflight-agent.json
```

On the unchanged branch, tests should report 60 passes: 27 new copilot tests plus 33 retained legacy tests. They default to reference code. Expected inference shape: summary_ready, then draft_ready with a valid plan and a review-only draft. Generated wording may vary. Read the trace and plan; do not just look at the exit code.

Evidence files never overwrite. For repeats, use new filenames. A blocked application returns code 2; a successful summary or draft returns 0. A blocked model run may still mean the host boundary worked correctly.

## Rehearse the attendee journey

For a repeatable presenter check, run `.\.venv\Scripts\python.exe scripts/rehearse_workday.py --output-dir output/my-rehearsal-1`. It runs tests and six real-device scenarios, preserving logs and source hashes in a new directory. Inspect all outcomes: its basic smoke-check exit code does not certify draft accuracy or every scenario's task completion.

1. Open [101](101-local-inference/README.md). Predict the summary, run it, change the note, compare, then restore the note.
2. Open [201](201-evidence-assistant/README.md). Set COPILOT_TRACK=starter for tests. Confirm the untouched function fails. Implement it or, for a presenter rehearsal only, compare with solution.py.
3. Run the agent on the selected track. Inspect each tool request and observation. T1 + T2 totals 50 minutes; prose about extra work is not independently verified.
4. Open [301](301-reliability-lab/README.md). Add one test; run the 30-minute scenario and either injection or impossible-budget scenario.
5. Complete [the worksheet](workshops/workday-copilot/WORKSHEET.md). Prepare a demo that includes a limitation.

If you are rehearsing without implementing learner code, use --track solution in application commands and leave COPILOT_TRACK unset for tests. Clearly label this presenter/reference mode. Do not claim to have completed learner tasks.

## Facilitation plan

| Clock | Lead action | Participant evidence |
|---|---|---|
| 0–3 | Ask “what would you do with one free hour?” | Two chosen tasks and manual sum |
| 3–10 | Draw the model/runtime/app/device distinction | Annotated diagram |
| 10–25 | Guide the first run and one changed input | Two summaries and a comparison |
| 25–35 | Explain the tool loop and contract; show failing starter check | Predicted action sequence |
| 35–51 | Coach implementation; swap driver after eight minutes | Working planning function |
| 51–65 | Run and explain the agent | Trace with actual observations |
| 65–70 | Break and role swap | — |
| 70–87 | Threat-model and add a test | One participant-authored check |
| 87–100 | Compare real scenarios | Two evidence files |
| 100–110 | Improve one behavior and decide release readiness | Before/after and limitation |
| 110–120 | Invite 60-second demos and debrief | Explanation, not just screenshots |

Use hint ladders from the labs before revealing code. Ask “which layer owns this failure?” rather than immediately giving the answer. Early finishers can adapt the note to a study session or hobby project while preserving the same trusted task schema. Keep the application scope bounded.

## Instructor answer notes

- T1 + T2 = 50; adding T4 fills 60. T3 alone exceeds 60.
- At 30 minutes, T2 + T4 fits; priority awareness is still a model-quality question.
- At five minutes, no provided task fits. A blocked result is expected.
- The agent can read/list in either order, but must observe both and validate a plan before finishing.
- Host tools provide data and arithmetic; model prose can still misstate facts or imply work is complete.
- A prompt injection may alter prose even if no forbidden tool can execute.
- A valid revised plan replaces the old one; an invalid revision clears prior approval.
- The tiny model may produce malformed JSON or repeat calls. Count errors toward the same bound.
- A scripted fake-model test proves the host behavior for that script, not successful real inference.

## Troubleshooting and recovery

| Symptom | Inspect | Recovery |
|---|---|---|
| CLI or import missing | Installation path, selected Python | Return to setup, not a random package upgrade |
| Wrong architecture/runtime | ARM64 output and supported hardware | Use a prepared device or label code-only |
| Starter tests fail immediately | NotImplementedError | Implement the contract; this initial failure is intentional |
| Tests pass but app blocks | COPILOT_TRACK vs --track, first trace error | Select the intended code and fix one cause |
| Model emits bad JSON | Raw request and parser error | Keep the rejected trace; retry once with a new filename |
| Eight calls with no draft | Unaffordable tasks/repeated requests | Inspect as a 301 failure; do not remove the bound |
| Output file already exists | Chosen filename | Use a new filename; preserve evidence |
| Plan seems right, prose is wrong | Draft against validated plan | Reject/edit the draft manually; no auto-send exists |

For a live device failure, inspect the committed real traces in the verification folder and run deterministic tests. State plainly that this is a trace-based fallback, not a fresh device demo. Do not pretend the saved run just occurred.

## Release rubric and rehearsal limits

One point each: explain GenieX's role; implement and explain the tool; demonstrate real observations; test a failure; state a justified limitation. Target 4/5 with the permissions explanation mandatory.

Before teaching on new hardware, rerun setup and all planned scenarios. Recheck installation docs and model terms; document versions and actual outcomes. This run did not reinstall Windows, drivers, or the CLI, certify all Snapdragon devices, establish disconnected operation, or validate novice completion times.

The earlier event-information edition remains in [the historical walkthrough](LEGACY-INTERNAL-WALKTHROUGH.md). Do not mix that edition's counts or app commands into this branch's attendee flow.
