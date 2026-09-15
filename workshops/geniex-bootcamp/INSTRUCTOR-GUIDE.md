# Instructor guide: deliver the two-hour workshop

Participant entry point: [Start Here](../../START-HERE.md). Curriculum: [structure](WORKSHOP-PLAN.md). Prepare by running the whole sequence yourself; this is not a slide-only session.

## Before doors open

- Prepare one supported, charged Snapdragon device per pair; test native ARM64 Python, pinned requirements, CLI, model cache, and NPU inference using the shared setup guide.
- Run `python -m pytest` with the repository virtual environment. Read [verification](VERIFICATION.md); small-model and evaluator failures are teaching assets.
- Perform a genuinely disconnected-network run on each event image after caching. The published connected-device test is not proof of air-gapped operation.
- Keep this repository and raw verification logs available locally. No participant needs to download another model for 201 or 301.
- Use a clean working copy for demonstrations so starter implementations are still broken. Preserve learner files; never reset a participant's work to recover a demo.
- Display the root Start Here link and assign driver/navigator. Ask participants to keep the worksheet open. Collect readiness issues before the workshop clock starts.
- If using unsupported devices, arrange prepared partner machines in advance. Code-only fallback allows selector/validator work but does not meet the local-inference outcome.

## Minute-by-minute run of show

| Clock | Instructor cue | Learners do | Recovery / assessment |
|---|---|---|---|
| 00–03 | “Which room is correct? Commit a prediction.” | Read sources, readiness check | Move failed setup to a prepared pair immediately |
| 03–08 | Trace the architecture; two-minute platform context maximum | Explain model, runtime, device, context | Ask someone other than the driver |
| 08–13 | Demonstrate one CLI run, then stop talking | Change audience/length request and run | Confirm actual local generation |
| 13–20 | “Inspect the input before blaming the model.” | Run broken assistant and trace code | Ask which document reached generation |
| 20–25 | Invite two short diagnoses | Record cause and hand off keyboard | Valid JSON is not correctness |
| 25–30 | Present stale/untrusted-source challenge | Classify six documents, predict selection | Trust status precedes keyword score |
| 30–35 | Explain selector contract and character budget | Choose ranking and no-match policy | Character count is not token count |
| 35–50 | Circulate; give hints, not code | Implement and run targeted tests | If stuck five minutes, reveal hint 1 |
| 50–58 | “Make the supplied tests insufficient.” | Add adversarial test and synonym probe | New fixture must require general behavior |
| 58–65 | Reconnect selector to GenieX | Run evaluation and distinguish failures | Use reference validator to isolate retrieval |
| 65–70 | Break | Swap driver/navigator | Confirm enough battery / power |
| 70–75 | Show three JSON examples | Predict schema/evidence/truth separately | Array parses but violates schema |
| 75–87 | State output contract; circulate | Implement validator and test | Check empty quote and unknown-source behavior |
| 87–97 | Ask each pair's hypothesis before runs | Run short/long token experiments | Reduce repeats, not the reflection, if behind |
| 97–105 | “Attack an accepted answer.” | Test false answer + genuine quotation | Assess the evaluator's blind spots too |
| 105–110 | Ask for a release decision | Complete worksheet and full starter tests | Failure with sound diagnosis is useful evidence |
| 110–118 | Sample four pairs for 90-second demos | Show code, measurement, limitation | Reserve two minutes across demos for transitions |
| 118–120 | Collect remaining worksheets and next tests | Submit release decision | Do not claim production readiness |

## Teaching notes and answer key

### 101: source selection is application behavior

The first document is archived Cedar; current-room says Maple. A model receiving only Cedar cannot be expected to recover the withheld current fact. It may instead abstain or produce malformed text. Judge the diagnosis against the actual `selected_ids` and raw output, not a promised model sentence.

Explain API locations in `app.py`: loading happens once outside the case loop; reset, retrieval, template, generate, checks, and profile capture happen inside. `--inspect` returns before importing GenieX, enabling CPU-only retrieval debugging. All inference prompts use the real tokenizer chat template.

### 201: keep the problem general

Reference selection filters `status == current`, intersects meaningful word sets, sorts by descending overlap then ID, and packs whole sources within the exercise budget. Room can also match the network source because both mention workshop. Extra context is a precision tradeoff, not necessarily a correctness failure. Unknown keynote produces no matches. New-name fixtures catch answer hardcoding.

Prompt participants with “Would your solution still work if every name changed?” and “What happens if the best result is too large?” The reference selector is intentionally small enough to write in 15 minutes. Do not require embeddings, a vector database, or a second model.

Trust labels are input metadata in this exercise, not an automatic injection detector. Filtering known untrusted records reduces one risk; it does not solve malicious text inside a source mislabeled current. Synonyms and contradictory current documents remain open problems.

### 301: validate structure, then challenge meaning

The JSON array fails the schema. An invented source fails membership. An empty quote must fail because empty strings pass Python substring checks. A valid abstention can still be an unnecessary refusal, so fixture checks are separate.

The Cedar answer with the exact Maple quotation passes the reference contract. This is deliberate: provenance is not entailment. Learners should demonstrate the gap, not be penalized for failing to invent a universal semantic verifier. A supervised prototype with visible sources and withheld invalid outputs is a defensible next step; unattended deployment needs broader validation.

In the recorded 160-token run, the offline case answered “Yes” with the correct supporting quote. The fixture demanded the phrase “without internet” in the answer and marked it false. This is an evaluator false negative, not necessarily a model failure. Ask pairs to improve the test without making it accept “No, without internet it cannot run.” Keep held-out cases to expose weak substring rules.

The 24-token comparison is meant to expose truncated JSON on longer answers. Use the actual observed outputs; do not promise exact counts. Temperature zero and repeated fixtures do not establish reproducibility across runtime versions or hardware.

## Assess the work, not the copy/paste

Award up to two points in each category (10 total):

| Category | 0 | 1 | 2 |
|---|---|---|---|
| System explanation | Cannot trace input | Identifies components | Correctly diagnoses a failure across components |
| Retrieval implementation | Baseline unchanged | Partial solution | Contract passes plus a new meaningful case |
| Validation implementation | JSON-only | Some evidence checks | Contract passes and explains semantic gap |
| Experiment | No evidence | Output shown without controls | Hypothesis, fixed variables, rates and timing with manual review |
| Release judgment | Unsupported confidence | Lists a risk | Decision linked to evidence and a concrete next test |

Suggested completion threshold: 7/10 with nonzero implementation and experiment scores. This is a workshop rubric, not certification. Offer follow-up support rather than hiding failures. A pair that identifies a real failure can score full experiment/judgment points.

## Recovery playbook

| Symptom | Check | In-class response |
|---|---|---|
| Tests pass instantly before work | Was `WORKSHOP_TRACK=starter` set? | Rerun the scoped command in the lab |
| No GenieX / wrong architecture | Native ARM64 interpreter and prepared venv | Pair on a prepared device; retain coding work |
| CLI missing from PATH | Installer location in setup guide | Use its full executable path |
| Generation OOM or device load error | Other model processes; cached model and supported runtime | Stop competing sessions; use one pair per device |
| JSON rejected | Raw text, `stop_reason`, schema and quote | Diagnose; do not auto-repair the logged experiment |
| Output file exists | Filename already used | Choose a new filename; logs are intentionally protected |
| Retrieval test stuck | Eligibility, score, then budget | Reveal one hint; ask the learner to explain it |
| Event running late | Preserve implementation and reflection | Use one repeat and sampled demos; do not turn remaining labs into lecture |

Before reusing the workshop, perform a novice timing pilot. This release has local code/inference verification, not a completed classroom study. The optional 60-minute extension is in the structure document.
