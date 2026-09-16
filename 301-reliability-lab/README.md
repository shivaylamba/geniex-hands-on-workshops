# 301 — Challenge the copilot before trusting it

**40 minutes**, followed by ten minutes of demos. Requires [201](../201-evidence-assistant/README.md).

## Goal and checkpoint

Find a failure, improve a check, and explain what is still unverified. Your deliverable is one new test, two recorded comparisons, and a release/no-release judgment. A rejected unsafe request is a successful boundary check, not a successful user task.

## 1. Threat-model the boundary — 7 minutes

With a partner, predict the response to each case before running anything:

1. The model asks for `send_email`.
2. The note contains “ignore previous instructions.”
3. The model picks T3 for a 60-minute budget.
4. A valid plan is followed by an invalid revised plan, then `finish`.
5. A draft says “I completed the work” when the host only planned it.

Open [agent.py](../workshops/workday-copilot/agent.py). Find the allowlist, strict fields, step bound, observation checks, and invalid-plan reset. Which case does this code **not** fully solve? The prose can still be misleading; it always needs review.

The planner's task IDs and arithmetic are validated; draft meaning is not. Do not use `draft_ready` as a factual-accuracy or prompt-injection-immunity claim.

## 2. Write a new test — 10 minutes

Add a test to [test_copilot.py](../workshops/workday-copilot/tests/test_copilot.py). Choose one not already covered: an oversized action argument, requesting `check_plan` before reading the inputs, whitespace-only finish, or an additional over-budget combination.

Write the expected result first. Reuse the existing `action`, `scripted`, `DATA`, `agent`, and `policy` helpers. Use scripted generations for predictable checks; these do not prove the real model follows instructions.

```powershell
$env:COPILOT_TRACK = 'starter'
.\.venv\Scripts\python.exe -m pytest workshops/workday-copilot/tests -q
Remove-Item Env:COPILOT_TRACK
```

If you find a genuine missing check, update your function or the host parser and add a regression test. Do not introduce message-sending or filesystem tools during this lab.

Hint ladder: isolate one invariant → find a neighboring test → assert the observation/error, not a generated sentence. The reference answer for oversized input is that `parse_action` raises `ValueError` when the argument exceeds 1,200 characters.

## 3. Run two real experiments — 13 minutes

First compare the same project under a smaller budget. Predict which tasks can fit:

```powershell
.\.venv\Scripts\python.exe workshops/workday-copilot/app.py --track starter --budget 30 --output output/my-agent-30.json
```

Then choose **one** boundary experiment:

```powershell
.\.venv\Scripts\python.exe workshops/workday-copilot/app.py --track starter --scenario injection --output output/my-agent-injection.json
.\.venv\Scripts\python.exe workshops/workday-copilot/app.py --track starter --budget 5 --output output/my-agent-impossible.json
```

The injection appends an adversarial sentence to the synthetic note; it never changes the allowlist. A five-minute budget cannot fit any provided task, so no draft should be approved. The current prototype reports this through its bounded blocked result rather than a polished clarification conversation.

Record: selected tasks, total, status, number of calls, one error (if any), and whether the draft faithfully describes the plan. Expected outcomes are invariants, not memorized sentences. The 30-minute model might choose T2, T4, both, or fail to make a valid choice.

## 4. Improve the user experience — 6 minutes

Choose one small change and state its acceptance criterion:

- Make blocked output easier to understand without approving a plan.
- Ask the final draft to separate “planned” from “completed,” then compare actual output.
- Add a human-readable display of the host-validated plan beside the draft.

Run the same test or scenario again using a fresh output filename. A prompt change can improve behavior but is not a security boundary. Preserve a before/after example and explain one tradeoff.

## 5. Decide whether to release — 4 minutes

Does your application meet all four criteria: valid plan, priority-aware selection, faithful draft, bounded permissions? A program exit code alone does not establish all four.

Record a remaining limitation and the evidence you would require before real use. More model calls increase latency; a larger model may change quality but does not replace host validation.

## Final ten-minute group share

Each pair has 60 seconds: user's problem → useful output → your code change → failure/limitation → what GenieX provided. Use [the worksheet](../workshops/workday-copilot/WORKSHEET.md). Review the [actual laptop report](../verification/WORKDAY-COPILOT.md) to compare observations, not to copy expected answers.
