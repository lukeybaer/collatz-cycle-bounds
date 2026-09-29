$ErrorActionPreference='Stop'
Push-Location $PSScriptRoot
try {
    ./src/run_reference_release.ps1 -Config results/fourth-power-J38-grafted-config-m100-lo1-hi15.json -Workers 8 -Split 1 -NodeLimit 100000000000 -Label fresh-m100
} finally { Pop-Location }
