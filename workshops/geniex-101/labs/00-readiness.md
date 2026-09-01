# Lab 0 — Readiness and architecture

**Time:** 25 minutes
**Goal:** Prove that the environment is ready and explain where inference runs.

## Check the environment

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\workshops\geniex-101\setup\verify_environment.ps1
```

Do not continue until every check passes. Record your Python architecture, chipset, GenieX SDK version, available runtimes, and cached model.

## Trace the path

Put these components in execution order:

- your Python application;
- GenieX Python API;
- GenieX SDK;
- `llama_cpp` runtime;
- Hexagon NPU; and
- generated tokens plus the performance profile.

Answer with a partner:

1. Does Python itself execute the model?
2. Does on-device always mean NPU-only?
3. Which GenieX runtime accepts a compatible community GGUF?
4. Which runtime uses a chipset-specific Qualcomm AI Hub bundle?

## Checkpoint

You are ready when you can explain this path without looking at the diagram:

```text
local notes → Python app → GenieX SDK → llama.cpp → Hexagon NPU → tokens/profile
```
