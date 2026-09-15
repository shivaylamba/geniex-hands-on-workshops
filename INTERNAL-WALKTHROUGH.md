# Internal team walkthrough: run and present the GenieX workshop

This is the starting document to share with teammates. It explains how to prepare a laptop, walk through the workshop independently, and present the result. It contains no private operational information; it is published in the public workshop repository for reuse.

## 0. Read this before running anything

### What will I build?

A small local event-information assistant. In 101 you run a model and discover an outdated room answer. In 201 you write source selection so only relevant, eligible documents reach the model. In 301 you write output checks, measure quality/latency tradeoffs, and demonstrate a limitation. All event documents are fictional.

You need basic Python functions, lists, dictionaries, and exceptions. You do not need previous model training experience. The same model is reused throughout; 201 and 301 are deeper application engineering, not larger downloads.

### Did everything work on our laptop?

The executable workflow has been rerun on our Snapdragon X Elite laptop, including a fresh Python virtual environment. Read [TEAM-REHEARSAL.md](verification/TEAM-REHEARSAL.md) for exact counts, environment, failures, and raw evidence. A CLI readiness-check issue was found and corrected during this rehearsal.

**Working end to end does not mean every answer is correct.** The starter is deliberately wrong. Even the completed application can reject model output or miss semantic errors; this is what 301 teaches. We have not repeated the Windows installer, tested every laptop, established air-gapped operation, or conducted a live novice timing pilot.

### Choose your mode

| Mode | Use when | Code you run | What it establishes |
|---|---|---|---|
| Learner | You want the full learning experience | Start with `--track starter`, implement the two functions | You can make and explain the changes |
| Presenter rehearsal | You need to verify the demo before a meeting | Intentionally broken starter, then `--track solution` | The prepared machine can execute the workflow |
| Code-only fallback | No supported device is available | Inspection and unit tests only | Python logic works; local inference remains unverified |

Do not call reference-code execution your own completed exercise. Do not call code-only fallback an end-to-end device test.

### File map and schedule

| Order | Open | Time | Your output |
|---|---|---:|---|
| Prework | Steps 1–3 below | Variable, before class | Working CLI, Python environment, cached model |
| 1 | [101-local-inference/README.md](101-local-inference/README.md) | 25 min | Real generation and baseline diagnosis |
| 2 | [201-evidence-assistant/README.md](201-evidence-assistant/README.md) | 40 min | Selector, six passing supplied checks, new case |
| Break | Swap pair roles | 5 min | — |
| 3 | [301-reliability-lab/README.md](301-reliability-lab/README.md) | 40 min | Validator, experiment, limitation |
| Demo | Step 8 below | 10 min | Evidence-backed release decision |

Use [the worksheet](workshops/geniex-bootcamp/WORKSHEET.md) for your notes. The clock totals 120 minutes, excluding setup. Self-guided learners can take longer. Do not count installation as hands-on learning time.

## 1. Check the laptop and install the CLI

### 1.1 Hardware gate

Use a Windows ARM64 laptop with a supported Snapdragon chipset. This edition was exercised on a Dell Latitude 7455, Snapdragon X Elite X1E80100, about 32 GB RAM. We are not claiming that this is a minimum-memory requirement or that all Snapdragon devices behave identically. Check [supported platforms](https://geniex.aihub.qualcomm.com/en/get-started/platforms) for another machine.

Open PowerShell and inspect:

```powershell
Get-CimInstance Win32_Processor | Select-Object Name
Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer,Model,SystemType
```

You should identify a supported Snapdragon processor and ARM64 system. An Intel/AMD x64 laptop is not a substitute for this NPU lab. Plug into power, close unrelated model processes, and allow several GB of space for software in addition to the roughly 2.4 GiB cache.

### 1.2 Install from the official source

Open [Qualcomm's Windows ARM64 CLI installation page](https://geniex.aihub.qualcomm.com/en/run/cli/install/#windows-arm64). Download its Windows installer and follow the installation prompts. Do not use a third-party mirror or the Linux shell instructions.

The page currently notes an unsigned installer. On a managed laptop, follow your organization's software approval process if Windows warns or blocks execution; this workshop does not require disabling Defender, SmartScreen, or corporate controls. Ask IT for an approved installation if necessary.

Open a new PowerShell window after installation:

```powershell
Get-Command geniex -ErrorAction SilentlyContinue
geniex --help
geniex version
geniex config get chipset
```

Expected: command help, CLI/runtime versions, and a chipset value. Our CLI is v0.5.0. If the current official installer delivers a different version, record that fact and rehearse before teaching; do not silently describe it as the tested version.

### 1.3 If `geniex` is not found

The official page's `where.exe` example assumes the executable is already discoverable. A shell alias cannot locate an unknown install by itself. On our laptop, the installer used the per-user location below:

```powershell
$geniexCli = Join-Path $env:LOCALAPPDATA 'GenieX CLI\geniex.exe'
Test-Path -LiteralPath $geniexCli
& $geniexCli --help
& $geniexCli version
Set-Alias -Name geniex -Value $geniexCli
```

Only run the executable/alias lines if `Test-Path` is true. If false, use the actual approved installer location. The alias lasts for the current PowerShell session; repeat it in a new terminal or have IT manage PATH. No global execution-policy change is needed.

Checkpoint: `geniex --help` runs, version is recorded, and the chipset can be read. Do not proceed while commands are missing.

## 2. Get the repository and prepare native Python

### 2.1 Clone the team edition

Install Git through your normal approved process if `git --version` is unavailable. Then, from a directory where you keep projects:

```powershell
git clone https://github.com/shivaylamba/geniex-hands-on-workshops.git
cd geniex-hands-on-workshops
Get-Location
Test-Path .\INTERNAL-WALKTHROUGH.md
```

The last command must print `True`. **Every remaining workshop command assumes this repository root**, not a numbered workshop subfolder. The review branch is `codex/team-walkthrough`; the new repository's main branch also contains the published team edition.

If you already have this edition, inspect `git status` before pulling or switching branches. Preserve your edits. Use a second clone for a clean rehearsal instead of resetting learner work.

### 2.2 Check the Python architecture

Follow the [official GenieX Python installation requirements](https://geniex.aihub.qualcomm.com/en/run/python/install). Use a maintained, organization-approved ARM64 Python 3.10+ build, not an AMD64 build running under emulation:

```powershell
python -c "import platform,sys; print(platform.python_version()); print(platform.machine()); print(sys.executable)"
```

The architecture must be `ARM64` (or the corresponding native ARM64 identifier). A wrong interpreter must be corrected before creating the environment. Our existing laptop interpreter is Python 3.12.8; that is a test observation, **not a recommendation to install an old interpreter**. Python's [3.12.8 release page](https://www.python.org/downloads/release/python-3128/) notes supersession and revoked installer certificates. Have IT select a maintained ARM64 build, then run this rehearsal with it.

### 2.3 Create and install the isolated environment

For a fresh clone:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -c "import platform,geniex; print(platform.machine()); print(geniex.version())"
```

The requirements include a dependency lock from this rehearsal, including GenieX 0.5.0 and pytest 9.1.1. Expected: no broken requirements, native architecture, and the SDK version. Use the virtual-environment executable explicitly throughout; activation and changing PowerShell execution policy are unnecessary.

Do not overwrite an existing environment with an unknown interpreter. For a clean-room check, create another environment under a distinct name and substitute its executable consistently. Our verification used `.venv-team` with fresh Python packages, but reused the already installed CLI, drivers, and cache.

### 2.4 Verify runtime discovery

```powershell
.\.venv\Scripts\python.exe -c "import geniex; geniex.init(); print(geniex.get_runtime_list()); print(geniex.get_compute_unit_list('llama_cpp')); geniex.deinit()"
```

On our prepared laptop, output includes `llama_cpp` and a Hexagon/HTP compute entry. Names may differ on another supported setup. Discovery does not prove generation works; the next gate runs it.

## 3. Cache the model and pass readiness

### 3.1 Download once, before the workshop

```powershell
geniex pull --model-type llm unsloth/Qwen3.5-2B-GGUF:Q4_0
geniex list
```

This fixes the exercise's model type and precision. The text weights are 1,214,873,856 bytes (~1.13 GiB). GenieX also caches a ~1.23 GiB projector from this repository; the visible cache is approximately 2.4 GiB even though the workshop uses text only. Do not mistake cache size for parameter count or promise a one-GB total download.

The [official quickstart](https://geniex.aihub.qualcomm.com/en/run/cli/quickstart) distinguishes GGUF/llama.cpp from AI Hub/QAIRT and recommends Q4_0 for Hexagon use. This workshop keeps the previously validated 2B model rather than adopting a different example model during setup. Model distribution terms must be checked before redistributing a prebuilt cache.

### 3.2 Run readiness and the first real inference

```powershell
powershell -ExecutionPolicy Bypass -File .\workshops\geniex-101\setup\verify_environment.ps1
geniex infer unsloth/Qwen3.5-2B-GGUF:Q4_0 --compute npu --think=false --max-tokens 80 -p "Explain on-device AI in two sentences."
.\.venv\Scripts\python.exe -m pytest -q
```

The first command invokes a repository-local checker in a child PowerShell process; it does not change machine-wide policy. Follow IT policy if script execution is restricted.

Expected readiness: five passing checks and `Environment ready for GenieX 101.` That last string is retained from the shared setup helper; it gates the whole current sequence. Expected tests on an unchanged release: **33 passing tests**. Expected inference: generated text, not a specific memorized sentence.

Tests default to the reference implementations. These 33 passes validate the supplied code, not your untouched starter. The later labs explicitly select learner code.

### 3.3 Offline claim: verify separately

These rehearsals use cached models on a connected laptop. They do not prove air-gapped behavior. Before promising an offline event, with local access and IT approval, disconnect the test machine's network after caching and repeat the CLI and Python examples. Restore connectivity afterward. Do not disconnect a remote-access machine merely to complete this checklist.

Readiness exit: you know the hardware and versions, have a cached model, have generated actual text, and have passing reference tests. Only now start the two-hour clock.

## 4. Walk through 101 yourself

Open [101-local-inference/README.md](101-local-inference/README.md) and follow its five numbered steps. Run the CLI, the small standalone Python example, and the broken assistant. Inspect sources before interpreting the model answer.

Your files are [hello_geniex.py](101-local-inference/hello_geniex.py) for the minimal API path and [app.py](workshops/geniex-bootcamp/app.py) for the full pipeline. Record the room prediction in the worksheet before running.

Expected lesson, not guaranteed sentence: the starter selects archived Cedar instead of current Maple. A different generated answer does not fix the missing-current-source problem. Identify the application component responsible.

## 5. Build 201 yourself

Open [201-evidence-assistant/README.md](201-evidence-assistant/README.md). Edit only `workshops/geniex-bootcamp/starter/retrieval.py` for the selector, then add your own test under the bootcamp tests directory.

The six retrieval tests initially fail. Follow the temporary `WORKSHOP_TRACK=starter` command exactly. A bare repository-wide pytest run defaults to the solution and will conceal whether your implementation is still wrong.

Your exit evidence: six passing learner retrieval checks, your new adversarial case, inspected sources for all five fixtures, and an actual `--track starter --policy solution --evaluate` run. That mixed configuration deliberately isolates retrieval from validation, which you have not built yet.

Take the five-minute break and change pair roles.

## 6. Build 301 yourself

Open [301-reliability-lab/README.md](301-reliability-lab/README.md). Edit `workshops/geniex-bootcamp/starter/policy.py`; validate schema and evidence, then run 24-token versus 160-token experiments. Use new filenames to preserve observations.

The policy starts with two passing checks and eight failures; the completed contract has ten passes. Together with retrieval there are 16 challenge checks. Extra tests you write will increase the count.

Read raw answers as well as summary counts. The fixture evaluator is intentionally narrow and can reject a supported “Yes.” A real quotation can also accompany a false answer. Neither JSON validity nor source provenance guarantees semantic truth.

Finish the worksheet with a hypothesis, controlled variable, both result tables, manual review, an adversarial case, and a release decision. Do not claim production readiness based on five development fixtures.

## 7. Run a presenter rehearsal without doing the exercises

Use this on a **clean checkout** to verify the machine before presenting. It does not edit starter files, install software, delete results, or simulate a participant completing the exercises.

```powershell
.\.venv\Scripts\python.exe scripts/rehearse_workshop.py --output output/team-rehearsal-01
```

It runs dependency/readiness checks, CLI help and generation, both small SDK examples, reference tests, intentional starter failures, both inspection paths, four evaluation runs, and protective error checks. It writes a new evidence directory. Our warm-cache run took minutes, not hours; duration varies by hardware and runtime state.

If the CLI is installed in a custom location:

```powershell
.\.venv\Scripts\python.exe scripts/rehearse_workshop.py --cli 'C:\approved-tools\GenieX\geniex.exe' --output output/team-rehearsal-02
```

Replace that illustrative path with your actual approved executable location. The script does not install there.

Read `summary.json`, not just the last terminal line:

```powershell
$rehearsal = Get-Content output/team-rehearsal-01/summary.json -Raw | ConvertFrom-Json
$rehearsal.workflow_passed
$rehearsal.steps | Format-Table step,passed,exit_code,expected_exit_code,elapsed_seconds
$rehearsal.experiments | ConvertTo-Json -Depth 5
```

`workflow_passed: true` means every process/check ran as expected and the expected number of nonempty generation records was produced. It **does not** require every generated answer to pass validation. The starter tests intentionally exit 1; invalid arguments and overwrite protection intentionally exit 2. Those are expected passes in the harness, not hidden errors.

If you've already completed the starter, its intentional-failure stage may stop the rehearsal. Use a second clean clone, not a destructive reset. The script assumes the five stock fixtures; added cases should be evaluated directly and described separately.

## 8. Present it to the team

### Ten-minute internal overview

1. **Minute 0–1:** open this file and explain the deliverable: a local assistant plus evidence about its limitations.
2. **Minute 1–3:** show a CLI or small SDK generation. State the device, model, precision, and requested compute. Do not promise identical prose.
3. **Minute 3–5:** inspect the broken selector, then reference selection. Show exactly which source changed.
4. **Minute 5–7:** show an evaluation JSONL with raw output, rejection reason, and timings. Explain the three different pass rates.
5. **Minute 7–9:** demonstrate a false answer with a real quotation, or the fixture's false rejection of “Yes.” Ask the team whether they would ship it unattended.
6. **Minute 9–10:** open the numbered folders and assign teammates the self-guided sequence. Point to the worksheet and explain how to test starter code.

For a live comparison without changing learner code:

```powershell
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track starter --inspect
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track solution --inspect
.\.venv\Scripts\python.exe workshops/geniex-bootcamp/app.py --track solution --evaluate --output output/team-demo.jsonl
```

Say explicitly that the last command uses the completed reference. Keep the published rehearsal logs ready as a fallback, clearly labeled as recorded rather than live.

### Ninety-second participant demo

Show your selector (20 seconds), validator/rejection (20 seconds), experiment plus limitation (30 seconds), and release decision/next test (20 seconds). Sample four pairs during the ten-minute workshop close and collect the remaining worksheets. The [instructor guide](workshops/geniex-bootcamp/INSTRUCTOR-GUIDE.md) contains a ten-point assessment rubric and recovery timings.

## 9. Troubleshooting and stopping rules

| Symptom | Likely check | Safe next action |
|---|---|---|
| `geniex` not found | Installer location / new shell | Use verified full path or session alias |
| Corporate installer block | Software approval | Ask IT; do not disable security controls |
| Python says AMD64 | Wrong interpreter | Create a new environment with approved ARM64 Python |
| `No module named geniex` | Wrong environment or incomplete install | Use explicit `.venv` executable and rerun dependency installation |
| No Hexagon entry or load error | Supported platform, drivers, runtime | Validate approved driver/runtime setup; use a prepared pair |
| Environment CLI check fails | Version and chipset exit codes | Run both directly; current checker consumes full output before checking status |
| Model missing or prompt to download | Cache, model ID, Q4_0 | Finish prework; do not switch model during class |
| JSON truncated | `stop_reason` and token count | Preserve the run and compare a larger output budget |
| Output rejected despite plausible prose | Exact schema, source, quotation | Inspect reasons; do not silently repair evaluation results |
| All tests pass before coding | Default solution target | Rerun the learner-targeted commands |
| Rehearsal fails intentional-starter step | Starter already modified | Use a second clean clone; preserve your work |
| Output already exists | Reused experiment name | Choose a new filename or directory |
| Device overloaded / allocation error | Other model processes and memory | Stop your own competing runs and retry serially |

Do not spend the class downloading software. Pair with a ready device or explicitly use code-only fallback. Do not claim unsupported hardware, disconnected-network operation, or a fixed model accuracy from another person's logs.

## 10. Before distributing this to an event

- Rehearse on each intended machine image; record versions and model/cache provenance.
- Confirm organizational approval for software and model redistribution.
- Run a novice timing pilot; this agenda has not been empirically validated with a class.
- Keep learner and reference code separate; preserve participant outputs and label recorded demos.
- Review logs before sharing. The supplied fixtures are fictional; do not publish attendee data or private prompts.
- For this repo's AI handoff, stage new files, run `python scripts/build_ai_bundle.py`, stage the bundle, and check with `--check`.

## Sources and scope

Checked 15 September 2026: [official Windows CLI installation](https://geniex.aihub.qualcomm.com/en/run/cli/install/#windows-arm64), [Python installation](https://geniex.aihub.qualcomm.com/en/run/python/install), [CLI quickstart](https://geniex.aihub.qualcomm.com/en/run/cli/quickstart), and [GenieX upstream](https://github.com/qualcomm/GenieX). The [UNO Q collection](https://github.com/aaishikasb/uno-q-workshops) informed the numbered-workshop presentation, not the GenieX API or hardware facts. This guide's commands and outputs are grounded in the supplied source code and local rehearsal, with untested boundaries called out above.
