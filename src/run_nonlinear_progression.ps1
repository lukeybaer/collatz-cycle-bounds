param([Parameter(Mandatory=$true)][string]$InputFile,[int]$Workers=4,[int]$Depth=16,[long]$NodeLimit=100000000,[int]$Take=0,[Parameter(Mandatory=$true)][string]$Label)
$ErrorActionPreference='Stop'
$source=Join-Path $PSScriptRoot 'NonlinearProgressionCapacityVerifier.cs'
$resultDir=Split-Path -Parent (Resolve-Path -LiteralPath $InputFile)
$meta=[ordered]@{startedUtc=[DateTime]::UtcNow.ToString('o');inputHash=(Get-FileHash -LiteralPath $InputFile -Algorithm SHA256).Hash;sourceHash=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash;workers=$Workers;depth=$Depth;nodeLimit=$NodeLimit;take=$Take;compilerOptimization='release /optimize+'}
$meta|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-metadata.json'))
Add-Type -Path $source -CompilerOptions '/optimize+'
$result=[CollatzNonlinearProgressionAudit.Checker]::Run((Get-Content -LiteralPath $InputFile -Raw),$Workers,$Depth,$NodeLimit,$Take)
$result|Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-result.json'))
($result|ConvertFrom-Json)|Select-Object status,full_input,capacity_exceptions_discharged,capacity_kind,linear_coefficient_certified,map_id,conditional_only,assumed_cycle_minimum,J,classes,seeds,restart_seeds,threshold_seeds,singleton_seeds,nodes,singleton_steps,bigint_steps,max_depth,seconds|ConvertTo-Json
