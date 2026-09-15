# Second requested end-to-end check — 15 September 2026

The published GenieX team edition at `ec322b993a920f6cbee43b9b6fbce02415d8a14e` was rerun from its clean working tree on the same Snapdragon X Elite laptop, using the prepared native ARM64 `.venv-team` environment and cached model.

Command: `.\.venv-team\Scripts\python.exe scripts/rehearse_workshop.py --output output/double-check-2026-09-15`.

**All 16 execution checks passed their expected outcomes, 33 unit tests passed, and 33 real generations completed** (CLI: one; standalone SDK examples: two; evaluations: 30). Intentional starter-test failures and invalid-argument/overwrite errors behaved as expected. No software/model reinstall or disconnected-network test was performed.

| Evaluation | Generations | Policy accepted | Fixture pass | Joint pass | Token-limit stops | Mean generation ms |
|---|---:|---:|---:|---:|---:|---:|
| Broken baseline | 5 | 5/5 (JSON only) | 0/5 | 0/5 | 0 | 1651.86 |
| Completed reference | 5 | 4/5 | 3/5 | 3/5 | 0 | 2254.94 |
| 24-token ceiling | 10 | 1/10 | 1/10 | 1/10 | 8 | 1531.06 |
| 160-token ceiling | 10 | 8/10 | 7/10 | 7/10 | 0 | 2579.54 |

A successful workflow still does not imply every model answer is valid or correct. The fixture evaluator also has documented limitations. These small samples are classroom observations, not production accuracy or controlled hardware benchmark claims.

The new local raw logs remain in the ignored output directory; the prior complete published evidence and reproduction instructions remain in [TEAM-REHEARSAL.md](TEAM-REHEARSAL.md). No new functional code change was needed for this repeat check.
