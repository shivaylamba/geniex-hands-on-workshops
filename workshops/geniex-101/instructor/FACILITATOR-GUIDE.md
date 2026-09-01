# GenieX 101 facilitator guide

## Teaching stance

The workshop promise is a working local application, not coverage of every GenieX feature. Keep theory attached to something participants can point to in a command, diagram, code path, or profile.

Use a gradual release:

1. **I do:** demonstrate a prepared CLI inference.
2. **We do:** identify the Python inference boundaries together.
3. **You do with support:** pairs extend the starter.
4. **You explain:** pairs show evidence and one limitation.

## Before participants enter

- Run `setup/verify_environment.ps1` on every device.
- Run the CLI prompt and solution app from `setup/README.md`.
- Confirm the model is cached and repeat Python inference with networking disconnected.
- Restore networking for documentation access.
- Put each machine on AC power and prevent sleep during the session.
- Open the repository root in the editor and a native ARM64 PowerShell terminal.
- Keep one spare device, a local repository archive, screenshots, and a two-minute backup recording ready.

For more than 25 participants, assign one instructor and one environment-support person. Environment support owns installation/cache problems; the instructor continues the learning path.

## Module notes

### Hook and readiness

Ask participants which parts of a prepared local inference still need the internet. Run a cached prompt, disconnect networking, and run it again. Say explicitly that setup and model acquisition may require a network even though this inference path does not.

If a readiness check remains red after five minutes, pair the participant with a green machine.

### Architecture

Do not teach Snapdragon silicon internals. The required mental model is interface → SDK → runtime → compute. Emphasize that on-device does not automatically mean NPU-only and that runtime/model format determines available compute choices.

### CLI inference

Have participants predict the output change before changing the audience. Ask two pairs to read their improved prompt, not their entire model response.

### Python path

Reveal one boundary at a time: load, format, generate, profile, release. Ask which lines would remain normal Python if GenieX were replaced; this makes the integration boundary visible.

### Application build

Use three public checkpoints on a board:

- input validated;
- brief generated; and
- actions mode plus profile working.

Offer concept hints before code hints. Ask participants to verify the action table against the notes—correct formatting is not evidence of factual correctness.

### Observation

Refuse “faster” claims without a named metric. TTFT is about when output starts; decode speed is output-token throughput; streaming mainly changes the experience of waiting.

## Assessment answers

- 101 path: local notes → Python application → GenieX Python API/SDK → `llama_cpp` → Hexagon NPU → generated tokens/profile.
- Community GGUF with fallback: `llama_cpp`.
- Chipset-specific Qualcomm AI Hub bundle: `qairt`.
- Production limitations include generated errors, prompt injection from untrusted files, limited evaluation, context/memory limits, single-user CLI UX, and missing operational controls.

## Completion standard

A participant completes the workshop when the application runs on Snapdragon, accepts the sample file, supports `brief` and `actions`, streams output, displays profile fields, and the participant can explain the inference path and one limitation.
