param([Parameter(Mandatory=$true)][string]$InputFile,[int]$Workers=4,[int]$Depth=16,[long]$NodeLimit=1000000,[int]$Take=0,[string]$Label='family')
$ErrorActionPreference='Stop'
$source=Join-Path $PSScriptRoot 'FlexibleNonlinearFamilyCapacity.cs'
$resultDir=Split-Path -Parent (Resolve-Path -LiteralPath $InputFile)
$meta=[ordered]@{startedUtc=[DateTime]::UtcNow.ToString('o');inputHash=(Get-FileHash -LiteralPath $InputFile -Algorithm SHA256).Hash;sourceHash=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash;workers=$Workers;depth=$Depth;nodeLimit=$NodeLimit;take=$Take;compilerOptimization='release /optimize+'}
$meta|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-metadata.json'))
Add-Type -Path $source -CompilerOptions '/optimize+'
$logs=Join-Path $resultDir 'log2-mantissa-table.json'
(Get-FileHash -LiteralPath $logs -Algorithm SHA256).Hash | Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-logtable.sha256'))
$result=[CollatzFlexibleNonlinearFamilies.Checker]::Run((Get-Content -LiteralPath $InputFile -Raw),(Get-Content -LiteralPath $logs -Raw),$Workers,$Depth,$NodeLimit,$Take)
$result|Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-result.json'))
($result|ConvertFrom-Json)|Select-Object status,full_input,capacity_exceptions_discharged,capacity_kind,linear_coefficient_certified,map_id,J,classes,seeds,restart_seeds,basin_seeds,singleton_seeds,nodes,singleton_steps,max_depth,seconds|ConvertTo-Json
