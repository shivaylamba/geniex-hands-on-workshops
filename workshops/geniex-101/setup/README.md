# GenieX 101 setup

> **Team edition:** use [INTERNAL-WALKTHROUGH.md](../../../INTERNAL-WALKTHROUGH.md) for the current step-by-step installation and locked dependencies. This older setup page is retained as background; its helper is shared by the new workshops.

Complete this before the timed workshop. Model download is intentionally excluded from class time.

## 1. Confirm the target machine

This release was verified on Windows ARM64 with a Snapdragon X Elite. GenieX requires a supported Snapdragon platform; an x86 or AMD64 Python environment is not sufficient.

```powershell
Get-CimInstance Win32_Processor | Select-Object Name
python -c "import platform; print(platform.machine())"
```

The Python command must print `ARM64`.

## 2. Install the native GenieX CLI

Download the installer from the [official GenieX CLI installation page](https://geniex.aihub.qualcomm.com/en/run/cli/install), run it, and open a new PowerShell window.

```powershell
geniex version
geniex config get chipset
```

## 3. Create the workshop environment

Run these commands from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\workshops\geniex-101\requirements-dev.txt
```

Verify that the SDK sees the Hexagon path:

```powershell
.\.venv\Scripts\geniex-py.exe devices
```

## 4. Pre-cache the workshop model

The release target is a 2-billion-parameter Qwen3.5 GGUF. Its Q4_0 language-model weight file is 1,214,873,856 bytes (about 1.13 GiB). The upstream repository also supplies a multimodal projector, so the current GenieX cache reports about 2.4 GiB total even though this workshop loads the model as text-only.

```powershell
geniex pull --model-type llm unsloth/Qwen3.5-2B-GGUF:Q4_0
geniex list
```

The model is public and ungated. Event organizers must still review and record its license before redistributing a prepared cache.

## 5. Run the readiness check

```powershell
powershell -ExecutionPolicy Bypass -File .\workshops\geniex-101\setup\verify_environment.ps1
```

All checks must pass. If `geniex` is installed but not on the current `PATH`, the script also checks `%LOCALAPPDATA%\GenieX CLI\geniex.exe`.

## 6. Prove the workshop path before arrival

```powershell
geniex infer unsloth/Qwen3.5-2B-GGUF:Q4_0 --compute npu --think=false --max-tokens 80 -p "Explain on-device AI in two sentences."

.\.venv\Scripts\python.exe .\workshops\geniex-101\solution\app.py `
  --file .\workshops\geniex-101\starter\sample-data\event-notes.txt `
  --mode brief `
  --device npu `
  --max-new-tokens 180
```

After the first successful load, disconnect networking and repeat the Python command to validate the prepared offline inference path.

### Pinned-version profile note

In GenieX 0.5.0, the Python package formats `ProfileData.ttft` as a microsecond value (`geniex/generation/output.py`) even though an earlier documentation table described milliseconds. The workshop solution normalizes it to milliseconds by dividing by 1,000. Revalidate this when changing the pinned GenieX version.
