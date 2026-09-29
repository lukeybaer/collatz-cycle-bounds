param([Parameter(Mandatory=$true)][string]$InputFile,[int]$Workers=4,[int]$Depth=16,[long]$NodeLimit=100000000,[int]$Take=0,[Parameter(Mandatory=$true)][string]$Label,[switch]$DumpLimits)
$ErrorActionPreference='Stop'
$source=Join-Path $PSScriptRoot 'J41FlexibleProgressionVerifier.cs'
$resultDir=Split-Path -Parent (Resolve-Path -LiteralPath $InputFile)
$logs=Join-Path $resultDir 'log2-mantissa-table.json'
$metadataPath=Join-Path $resultDir ($Label+'-metadata.json')
if(Test-Path -LiteralPath $metadataPath) {throw 'Refusing to overwrite run label'}
$meta=[ordered]@{startedUtc=[DateTime]::UtcNow.ToString('o');inputHash=(Get-FileHash -LiteralPath $InputFile).Hash;sourceHash=(Get-FileHash -LiteralPath $source).Hash;logTableHash=(Get-FileHash -LiteralPath $logs).Hash;workers=$Workers;depth=$Depth;nodeLimit=$NodeLimit;take=$Take;compilerOptimization='release /optimize+'}
$meta|ConvertTo-Json|Set-Content -LiteralPath $metadataPath
Add-Type -Path $source -CompilerOptions '/optimize+'
$inputText=Get-Content -LiteralPath $InputFile -Raw
$logText=Get-Content -LiteralPath $logs -Raw
if($DumpLimits) {
 [CollatzFlexibleNonlinearProgressionAuditJ41.Checker]::DumpLimits($inputText,$logText,$Depth) | Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-thresholds.json'))
}
$result=[CollatzFlexibleNonlinearProgressionAuditJ41.Checker]::Run($inputText,$logText,$Workers,$Depth,$NodeLimit,$Take,(Join-Path $resultDir ($Label+'-classes.jsonl')))
$result|Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-result.json'))
($result|ConvertFrom-Json)|Select-Object status,full_input,capacity_exceptions_discharged,capacity_kind,linear_coefficient_certified,map_id,conditional_only,J,classes,seeds,restart_seeds,threshold_seeds,singleton_seeds,nodes,singleton_steps,bigint_steps,max_depth,seconds|ConvertTo-Json
