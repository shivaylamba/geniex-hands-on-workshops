# 201 — Build a local tool-using copilot

**40 minutes.** Requires [101](../101-local-inference/README.md). Next: [301](../301-reliability-lab/README.md). The folder name is retained for existing links; this lab now builds a workday copilot.

## Goal and checkpoint

Implement the deterministic planning tool the model needs. Then inspect a real multi-step trace: the model proposes a tool call, Python validates and executes it, and the observation informs the next call.

Your deliverable is your own `check_plan`, passing learner tests, and either a reviewable draft or an explained blocked trace. Reading the solution alone does not complete the exercise.

## 1. Predict and trace — 6 minutes

Read [agent.py](../workshops/workday-copilot/agent.py), focusing on `run_agent`. Predict the shortest successful sequence before running it.

| Model request | Host behavior | Permission |
|---|---|---|
| `read_note` | Return the one bundled note | No arbitrary filename |
| `list_tasks` | Return the bundled task list | Read-only |
| `check_plan` | Check IDs and total against the user's budget | Cannot change budget |
| `finish` | Return a draft only after a valid plan | No sending |

The model chooses its next request; the host does not hard-code a four-step answer. It may retry, choose a different plan, or run out of steps. The loop is limited to eight generations by default. This is application-level orchestration on GenieX, not a claim that GenieX itself is an agent framework.

## 2. Make the red test meaningful — 4 minutes

Open [starter.py](../workshops/workday-copilot/starter.py). Only one function is missing; all model plumbing is supplied.

```powershell
$env:COPILOT_TRACK = 'starter'
.\.venv\Scripts\python.exe -m pytest workshops/workday-copilot/tests/test_copilot.py -q -k plan
Remove-Item Env:COPILOT_TRACK
```

Expected before you edit: failures involving `NotImplementedError`. Explain the first failure with your partner. Action-parser tests are already implemented and are not the coding task.

## 3. Implement the contract — 16 minutes

Implement `check_plan(task_ids, tasks, budget)` in starter.py:

- Require an integer budget from 1 through 240; reject booleans.
- Require a nonempty list of unique known string task IDs.
- Look up trusted task durations and sum them in Python.
- Reject a plan exceeding the user-supplied budget with `ValueError`.
- Return selected records in requested order, IDs, total, budget, and remaining minutes.

For T1 + T2 with a 60-minute budget, the total is 50 and remaining time is 10. For T3 at the same budget, reject it. Do not remove or edit supplied tests to make them pass.

Driver writes code; reviewer checks the contract. Swap after eight minutes.

Hint 1: create a dictionary indexed by task ID. Hint 2: validate IDs before looking them up. Hint 3: compare sets to detect duplicates, but preserve the input order in the returned plan. Open [solution.py](../workshops/workday-copilot/solution.py) only after an honest attempt.

## 4. Test your implementation, then run it — 10 minutes

```powershell
$env:COPILOT_TRACK = 'starter'
.\.venv\Scripts\python.exe -m pytest workshops/workday-copilot/tests -q
Remove-Item Env:COPILOT_TRACK
.\.venv\Scripts\python.exe workshops/workday-copilot/app.py --track starter --budget 60 --output output/my-agent-60.json
Get-Content output/my-agent-60.json
```

The supplied suite contains 27 tests before you add any. Bare pytest defaults to the solution, so do not omit the environment selector when checking your function. The application uses the separate `--track starter` selector.

Expected successful shape: `draft_ready`, a host-validated plan within 60 minutes, a draft, and a trace. T1 + T2 is sensible; other affordable selections are not automatically useful. Check priorities and prose yourself. No exact generated sentence is required.

If blocked, inspect the first trace error. Did the model request an unknown tool, select an unaffordable task, or did your function fail? Fix one cause and rerun with a new filename. Do not relax permissions to obtain a green status.

## 5. Explain what you built — 4 minutes

Point to the observation that changed the model's next decision. Identify the deterministic fact (sum of durations) and the judgment call (what is useful). Why should the language model not authorize a larger budget for itself?

Presenter-only recovery: use `--track solution` and label it reference code. Learners should still explain the difference.

Take a five-minute break, swap roles, and open [301](../301-reliability-lab/README.md).
