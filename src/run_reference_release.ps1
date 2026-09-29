param(
  [Parameter(Mandatory=$true)][string]$Config,
  [int]$Workers=8,
  [int]$Split=1,
  [long]$NodeLimit=2000000000,
  [string]$Label='native'
)
$ErrorActionPreference='Stop'
$cfg=Get-Content -LiteralPath $Config -Raw | ConvertFrom-Json
$resultDir=Split-Path -Parent (Resolve-Path -LiteralPath $Config)
$source=Join-Path $PSScriptRoot 'PrefixKernel.cs'
$metadata=[ordered]@{
  startedUtc=[DateTime]::UtcNow.ToString('o')
  configHash=(Get-FileHash -LiteralPath $Config -Algorithm SHA256).Hash
  sourceHash=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
  compilerOptimization='release /optimize+'
  config=$cfg
  workers=$Workers
  split=$Split
  nodeLimit=$NodeLimit
  label=$Label
  powershell=$PSVersionTable.PSVersion.ToString()
  runtime=[Environment]::Version.ToString()
  logicalProcessors=[Environment]::ProcessorCount
}
$metadata | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-metadata.json'))
Add-Type -Path $source -CompilerOptions '/optimize+'
$journal=Join-Path $resultDir ($Label+'-journal.jsonl')
$result=[CollatzExact.Kernel]::Run([int]$cfg.m,[string]$cfg.low,[string]$cfg.high,[string[]]$cfg.targets,[int]$cfg.depth,$NodeLimit,$Workers,$Split,$journal)
$result | Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-result.json'))
$result
