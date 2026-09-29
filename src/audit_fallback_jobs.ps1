param([Parameter(Mandatory=$true)][string]$Config,[Parameter(Mandatory=$true)][string]$Label,[int]$Split=2)
$ErrorActionPreference='Stop'
$cfg=Get-Content -LiteralPath $Config -Raw|ConvertFrom-Json
$resultDir=Split-Path -Parent (Resolve-Path -LiteralPath $Config)
$selected=Get-Content -LiteralPath (Join-Path $resultDir ($Label+'-fallback-jobs.json')) -Raw|ConvertFrom-Json
$journal=Join-Path $resultDir ($Label+'-journal.jsonl')
if($selected.journal_sha256 -ne (Get-FileHash -LiteralPath $journal).Hash.ToLowerInvariant()) {throw 'Journal hash mismatch'}
foreach($suffix in @('-audit.json','-generator-audit.json','-partition-audit.json')) {
 if((Get-Content -LiteralPath (Join-Path $resultDir ($Label+$suffix)) -Raw|ConvertFrom-Json).status -ne 'passed') {throw 'Missing completed audit'}
}
$source=Join-Path $PSScriptRoot 'PrefixKernel.cs'
Add-Type -Path $source -CompilerOptions '/optimize+'
$data=[CollatzExact.Data]::new([int]$cfg.m,[string]$cfg.low,[string]$cfg.high,[string[]]$cfg.targets,[int]$cfg.depth)
$generator=[CollatzExact.Kernel]::new($data,[long]::MaxValue)
$generator.Jobs=[Collections.Generic.List[CollatzExact.State]]::new();$generator.Split=$Split
$generator.Visit([CollatzExact.State]::new(1,0,0,$data.Low,$data.High,1,0,0))
$rows=@();$watch=[Diagnostics.Stopwatch]::StartNew()
foreach($item in $selected.jobs) {
 $checker=[CollatzExact.Kernel]::new($data,[long]::MaxValue)
 $checker.Visit($generator.Jobs[[int]$item.job])
 $actual=$checker.Summary('complete',0)|ConvertFrom-Json
 foreach($key in @('nodes','singletons','descent','capacity','empty','survivors','odd_tail','even_tail')) {
  if($actual.$key -ne $item.receipt.$key) {throw "Reference job mismatch: $($item.job), $key"}
 }
 if($actual.survivors -ne 0) {throw 'Reference survivor'}
 $rows += [ordered]@{job=$item.job;wide_fallbacks=$item.receipt.big_fallbacks;reference=$actual}
 Write-Output "Reference fallback job $($item.job) passed; $($actual.nodes) nodes."
}
$result=[ordered]@{status='passed';scope='Full original BigInteger rerun of every job that invoked wide singleton fallback; not a full rerun of the remaining jobs';jobs=$rows;seconds=$watch.Elapsed.TotalSeconds;configHash=(Get-FileHash -LiteralPath $Config).Hash;referenceSourceHash=(Get-FileHash -LiteralPath $source).Hash;driverSourceHash=(Get-FileHash -LiteralPath $PSCommandPath).Hash;selectionHash=(Get-FileHash -LiteralPath (Join-Path $resultDir ($Label+'-fallback-jobs.json'))).Hash;journalHash=(Get-FileHash -LiteralPath $journal).Hash}
$result|ConvertTo-Json -Depth 10|Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-fallback-reference-audit.json'))
$result|Select-Object status,seconds,scope|ConvertTo-Json
