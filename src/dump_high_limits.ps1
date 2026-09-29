param([Parameter(Mandatory=$true)][string]$InputFile,[Parameter(Mandatory=$true)][string]$Label)
$ErrorActionPreference='Stop'
$resultDir=Split-Path -Parent (Resolve-Path -LiteralPath $InputFile)
$meta=Get-Content -LiteralPath (Join-Path $resultDir ($Label+'-metadata.json')) -Raw|ConvertFrom-Json
$source=Join-Path $PSScriptRoot 'HighNonlinearProgressionVerifier.cs'
$logs=Join-Path $resultDir 'log2-mantissa-table.json'
if ((Get-FileHash -LiteralPath $InputFile).Hash -ne $meta.inputHash) {throw 'Input hash differs from completed run'}
if ((Get-FileHash -LiteralPath $source).Hash -ne $meta.sourceHash) {throw 'Source hash differs from completed run'}
if ((Get-FileHash -LiteralPath $logs).Hash -ne $meta.logTableHash) {throw 'Log table hash differs from completed run'}
$target=Join-Path $resultDir ($Label+'-thresholds.json')
if (Test-Path -LiteralPath $target) {throw 'Refusing to overwrite thresholds'}
Add-Type -Path $source -CompilerOptions '/optimize+'
$dataText=Get-Content -LiteralPath $InputFile -Raw
$logText=Get-Content -LiteralPath $logs -Raw
[CollatzHighNonlinearProgressionAudit.Checker]::DumpLimits($dataText,$logText,[int]$meta.depth)|Set-Content -LiteralPath $target
[ordered]@{status='regenerated';scope='Exact thresholds regenerated from source, input and log table matching the completed run';thresholdHash=(Get-FileHash -LiteralPath $target).Hash;metadataHash=(Get-FileHash -LiteralPath (Join-Path $resultDir ($Label+'-metadata.json'))).Hash;driverHash=(Get-FileHash -LiteralPath $PSCommandPath).Hash}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-threshold-regeneration.json'))
Get-FileHash -LiteralPath $target|Select-Object Hash
