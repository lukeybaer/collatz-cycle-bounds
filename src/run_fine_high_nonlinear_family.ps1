param([Parameter(Mandatory=$true)][string]$InputFile,[int]$Workers=2,[int]$Depth=16,[long]$NodeLimit=5000000,[int]$Take=0,[string]$Label='fine-family')
$ErrorActionPreference='Stop'
$source=Join-Path $PSScriptRoot 'FineHighNonlinearFamilyCapacity.cs'
$resultDir=Split-Path -Parent (Resolve-Path -LiteralPath $InputFile)
$logs=Join-Path $resultDir 'log2-mantissa-table-4096.json'
$meta=[ordered]@{startedUtc=[DateTime]::UtcNow.ToString('o');inputHash=(Get-FileHash -LiteralPath $InputFile -Algorithm SHA256).Hash;sourceHash=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash;workers=$Workers;depth=$Depth;nodeLimit=$NodeLimit;take=$Take;compilerOptimization='release /optimize+';logTableHash=(Get-FileHash -LiteralPath $logs -Algorithm SHA256).Hash;grid=4096}
$meta|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-metadata.json'))
Add-Type -Path $source -CompilerOptions '/optimize+'
$result=[CollatzFineHighNonlinearFamilies.Checker]::Run((Get-Content -LiteralPath $InputFile -Raw),(Get-Content -LiteralPath $logs -Raw),$Workers,$Depth,$NodeLimit,$Take)
$result|Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-result.json'))
($result|ConvertFrom-Json)|Select-Object status,full_input,capacity_exceptions_discharged,map_id,J,classes,seeds,restart_seeds,basin_seeds,singleton_seeds,nodes,singleton_steps,max_depth,seconds|ConvertTo-Json
