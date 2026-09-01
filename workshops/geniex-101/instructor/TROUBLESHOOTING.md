# GenieX 101 troubleshooting

Work from the top of the relevant path. Do not change several variables at once.

## `platform.machine()` reports `AMD64`

Cause: x86 Python or an emulated environment is first on `PATH`.

1. Run `Get-Command python`.
2. Install or select native Windows ARM64 Python 3.10+.
3. Delete only the workshop `.venv` after confirming its exact repository path, recreate it with ARM64 Python, and reinstall requirements.

## `geniex` is not recognized

1. Open a new PowerShell window after installing the CLI.
2. Check `%LOCALAPPDATA%\GenieX CLI\geniex.exe`.
3. Run the readiness script; it checks that fallback location automatically.

## `import geniex` fails

Confirm the active interpreter and reinstall into it:

```powershell
.\.venv\Scripts\python.exe -m pip install -r .\workshops\geniex-101\requirements.txt
.\.venv\Scripts\python.exe -c "import geniex; print(geniex.version())"
```

## Model starts downloading

The pinned cache was not staged or the identifier/precision differs. Stop the download, pair the participant with a ready device, and restore the cache outside teaching time. Do not paste Hugging Face tokens into a shared terminal.

## Model is cached but Python downloads again

Compare the exact model identifier and precision in `setup/versions.json`, `geniex list`, and the application command. Confirm both tools use the same Windows user profile and default GenieX cache.

## Model load fails on NPU

1. Run `geniex config get chipset`.
2. Run `.\.venv\Scripts\geniex-py.exe devices`.
3. Confirm `llama_cpp` lists `HTP0` / Hexagon.
4. Retry the pinned model with the published command.
5. Use `--device cpu` only as a learning fallback and label the result as CPU, not NPU.

## Output exceeds context or memory

Use the workshop sample, keep input below 12,000 characters, and reduce `--max-new-tokens`. A larger runtime context uses more KV-cache memory.

## Output invents an owner or date

This is an output-quality failure, not a runtime failure. Check that the prompt requires `unknown`, compare every field with the source, and record the failure for discussion.

## First run is much slower

Separate model load/cold-start behavior from generation profile metrics. Warm state and caching differ. Do not report one run as a benchmark.
