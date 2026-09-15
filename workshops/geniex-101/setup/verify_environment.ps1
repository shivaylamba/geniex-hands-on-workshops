[CmdletBinding()]
param(
    [string]$PythonPath,
    [string]$GenieXCliPath,
    [string]$ModelId = "unsloth/Qwen3.5-2B-GGUF",
    [switch]$SkipModel
)

$ErrorActionPreference = "Stop"
$results = [System.Collections.Generic.List[object]]::new()
$workshopDir = Split-Path -Parent $PSScriptRoot
$repoRoot = (Resolve-Path (Join-Path $workshopDir "..\..")).Path

function Add-Check {
    param([string]$Name, [bool]$Passed, [string]$Details)
    $script:results.Add([pscustomobject]@{
        Check = $Name
        Passed = $Passed
        Details = $Details
    })
    $symbol = if ($Passed) { "[PASS]" } else { "[FAIL]" }
    $color = if ($Passed) { "Green" } else { "Red" }
    Write-Host "$symbol $Name - $Details" -ForegroundColor $color
}

if (-not $PythonPath) {
    $venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $venvPython) {
        $PythonPath = $venvPython
    } else {
        $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
        if ($pythonCommand) { $PythonPath = $pythonCommand.Source }
    }
}

if (-not $GenieXCliPath) {
    $cliCommand = Get-Command geniex -ErrorAction SilentlyContinue
    if ($cliCommand) {
        $GenieXCliPath = $cliCommand.Source
    } else {
        $installedCli = Join-Path $env:LOCALAPPDATA "GenieX CLI\geniex.exe"
        if (Test-Path -LiteralPath $installedCli) { $GenieXCliPath = $installedCli }
    }
}

Write-Host "GenieX workshop environment verification" -ForegroundColor Cyan
Write-Host "Workshop: $workshopDir"

$computer = Get-CimInstance Win32_ComputerSystem
$processor = Get-CimInstance Win32_Processor | Select-Object -First 1
$operatingSystem = Get-CimInstance Win32_OperatingSystem
$isArmSystem = $computer.SystemType -match "ARM64" -and $operatingSystem.OSArchitecture -match "ARM"
$isSnapdragon = $processor.Name -match "Snapdragon"
Add-Check "Snapdragon ARM64 device" ($isArmSystem -and $isSnapdragon) "$($computer.Manufacturer) $($computer.Model); $($processor.Name)"

if (-not $PythonPath -or -not (Test-Path -LiteralPath $PythonPath)) {
    Add-Check "Native Python" $false "Python executable was not found"
} else {
    try {
        $probeCode = "import platform,sys; print(platform.python_version() + '|' + platform.machine() + '|' + sys.executable)"
        $pythonProbe = (& $PythonPath -c $probeCode).Split('|', 3)
        $versionOk = [version]$pythonProbe[0] -ge [version]"3.10"
        $architectureOk = $pythonProbe[1] -match "ARM64|aarch64"
        Add-Check "Native Python" ($versionOk -and $architectureOk) "Python $($pythonProbe[0]) $($pythonProbe[1]) at $($pythonProbe[2])"
    } catch {
        Add-Check "Native Python" $false $_.Exception.Message
    }
}

if ($PythonPath -and (Test-Path -LiteralPath $PythonPath)) {
    try {
        $sdkCode = "import geniex; geniex.init(); print(geniex.version() + '|' + ','.join(geniex.get_runtime_list()) + '|' + str(geniex.get_compute_unit_list('llama_cpp'))); geniex.deinit()"
        $sdkProbe = (& $PythonPath -c $sdkCode).Split('|', 3)
        $hasLlama = $sdkProbe[1].Split(',') -contains "llama_cpp"
        $hasNpu = $sdkProbe[2] -match "HTP0|Hexagon"
        Add-Check "GenieX Python SDK" ($hasLlama -and $hasNpu) "$($sdkProbe[0]); runtimes: $($sdkProbe[1]); Hexagon detected: $hasNpu"
    } catch {
        Add-Check "GenieX Python SDK" $false $_.Exception.Message
    }
}

if (-not $GenieXCliPath -or -not (Test-Path -LiteralPath $GenieXCliPath)) {
    Add-Check "GenieX CLI" $false "geniex.exe was not found"
} else {
    try {
        # Consume complete native-command output before selecting display lines.
        # Early pipeline termination can leave an unreliable native exit status.
        $versionOutput = @(& $GenieXCliPath version)
        $versionExit = $LASTEXITCODE
        $chipsetOutput = @(& $GenieXCliPath config get chipset)
        $chipsetExit = $LASTEXITCODE
        $cliVersion = $versionOutput | Select-Object -First 1
        $chipset = $chipsetOutput | Select-Object -First 1
        Add-Check "GenieX CLI" ($versionExit -eq 0 -and $chipsetExit -eq 0) "$cliVersion; chipset: $chipset; version exit: $versionExit; config exit: $chipsetExit; path: $GenieXCliPath"
    } catch {
        Add-Check "GenieX CLI" $false $_.Exception.Message
    }
}

if (-not $SkipModel) {
    if (-not $GenieXCliPath -or -not (Test-Path -LiteralPath $GenieXCliPath)) {
        Add-Check "Pinned model cache" $false "Cannot inspect cache without the GenieX CLI"
    } else {
        try {
            $modelList = (& $GenieXCliPath list | Out-String)
            $modelFound = $modelList -match [regex]::Escape($ModelId)
            Add-Check "Pinned model cache" $modelFound $(if ($modelFound) { "$ModelId is cached" } else { "$ModelId is not cached" })
        } catch {
            Add-Check "Pinned model cache" $false $_.Exception.Message
        }
    }
}

$failed = @($results | Where-Object { -not $_.Passed })
Write-Host ""
if ($failed.Count -eq 0) {
    Write-Host "Environment ready for GenieX 101." -ForegroundColor Green
    exit 0
}

Write-Host "$($failed.Count) check(s) failed. Follow setup/README.md before the workshop." -ForegroundColor Red
exit 1
