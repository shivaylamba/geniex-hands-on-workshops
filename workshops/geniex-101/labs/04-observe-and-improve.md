# Lab 4 — Observe and improve

**Time:** 15 minutes
**Goal:** Make one controlled comparison without overclaiming.

Choose one comparison:

- `--max-new-tokens 100` versus `200`;
- streaming versus `--no-stream`; or
- a concise source file versus a longer source file.

Run each variant twice. Record:

| Variant | Run | TTFT (ms) | Prompt tokens | Generated tokens | Decode tok/s | Quality note |
|---|---:|---:|---:|---:|---:|---|
| A | 1 | | | | | |
| A | 2 | | | | | |
| B | 1 | | | | | |
| B | 2 | | | | | |

Discuss:

1. Which metric describes perceived start-up responsiveness?
2. Which describes output-token throughput?
3. Did streaming change generation speed, perceived responsiveness, or both?
4. What would a credible benchmark require beyond these four runs?

## Exit ticket

- Trace the inference path.
- Choose `llama_cpp` or `qairt` for a model scenario.
- Point to load, template, generate, stream, profile, and release in code.
- Name one limitation of the prototype.

## Finish

Return to [`../START-HERE.md`](../START-HERE.md) if you need the repository map, or show your completed application to the facilitator.
