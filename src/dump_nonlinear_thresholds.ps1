$ErrorActionPreference='Stop'
$source=Join-Path $PSScriptRoot 'NonlinearProgressionCapacityVerifier.cs'
$resultDir=Join-Path (Split-Path -Parent $PSScriptRoot) 'results'
Add-Type -Path $source -CompilerOptions '/optimize+'
$inputJson=Get-Content -LiteralPath (Join-Path $resultDir 'extended-capacity-J41-classes.json') -Raw
[CollatzNonlinearProgressionAudit.Checker]::DumpLimits($inputJson,16) | Set-Content -LiteralPath (Join-Path $resultDir 'nonlinear-progression-thresholds.json')
