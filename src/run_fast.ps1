param(
  [Parameter(Mandatory=$true)][string]$Config,
  [int]$Workers=8,
  [int]$Split=1,
  [long]$NodeLimit=2000000000,
  [int]$Batch=1,
  [string]$Label='native-fast'
)
$ErrorActionPreference='Stop'
$cfg=Get-Content -LiteralPath $Config -Raw | ConvertFrom-Json
$resultDir=Split-Path -Parent (Resolve-Path -LiteralPath $Config)
$source=Join-Path $PSScriptRoot 'PrefixKernelFast.cs'
$metadata=[ordered]@{
  startedUtc=[DateTime]::UtcNow.ToString('o')
  configHash=(Get-FileHash -LiteralPath $Config -Algorithm SHA256).Hash
  sourceHash=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
  config=$cfg
  workers=$Workers
  batch=$Batch
  split=$Split
  nodeLimit=$NodeLimit
  label=$Label
  powershell=$PSVersionTable.PSVersion.ToString()
  runtime=[Environment]::Version.ToString()
  logicalProcessors=[Environment]::ProcessorCount
}
$metadata | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-metadata.json'))
Add-Type -Path $source
$journal=Join-Path $resultDir ($Label+'-journal.jsonl')
$result=[CollatzFast.Kernel]::Run([int]$cfg.m,[string]$cfg.low,[string]$cfg.high,[string[]]$cfg.targets,[int]$cfg.depth,$NodeLimit,$Workers,$Split,$journal,$Batch)
$result | Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-result.json'))
$result
