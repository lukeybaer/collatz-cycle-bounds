param(
  [Parameter(Mandatory=$true)][string]$Config,
  [int]$Split=2,
  [Parameter(Mandatory=$true)][string]$Label
)
$ErrorActionPreference='Stop'
$cfg=Get-Content -LiteralPath $Config -Raw | ConvertFrom-Json
Add-Type -Path (Join-Path $PSScriptRoot 'PrefixKernel.cs')
$data=[CollatzExact.Data]::new([int]$cfg.m,[string]$cfg.low,[string]$cfg.high,[string[]]$cfg.targets,[int]$cfg.depth)
$kernel=[CollatzExact.Kernel]::new($data,2000000000)
$kernel.Jobs=[System.Collections.Generic.List[CollatzExact.State]]::new()
$kernel.Split=$Split
$state=[CollatzExact.State]::new(1,0,0,$data.Low,$data.High,1,0,0)
$kernel.Visit($state)
$resultDir=Split-Path -Parent (Resolve-Path -LiteralPath $Config)
$auditPath=Join-Path $resultDir ($Label+'-audit.json')
$audit=Get-Content -LiteralPath $auditPath -Raw | ConvertFrom-Json
if ($audit.status -ne 'passed') { throw 'Journal has not passed complete-run audit' }
if ($audit.jobs_expected -ne $kernel.Jobs.Count) { throw 'Job count mismatch' }
$summary=$kernel.Summary('generator_only',0) | ConvertFrom-Json
foreach ($key in @('nodes','singletons','descent','capacity','empty','survivors','odd_tail','even_tail')) {
  if ($summary.$key -ne $audit.generator_counters.$key) { throw "Generator counter mismatch: $key" }
}
$receipt=[ordered]@{
  status='passed'
  jobs=$kernel.Jobs.Count
  generator=$summary
  configHash=(Get-FileHash -LiteralPath $Config -Algorithm SHA256).Hash
  sourceHash=(Get-FileHash -LiteralPath (Join-Path $PSScriptRoot 'PrefixKernel.cs') -Algorithm SHA256).Hash
}
$receipt | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-generator-audit.json'))
$receipt | ConvertTo-Json -Depth 10
