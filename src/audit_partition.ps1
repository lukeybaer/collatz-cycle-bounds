param([Parameter(Mandatory=$true)][string]$Config,[int]$Split=2,[Parameter(Mandatory=$true)][string]$Label)
$ErrorActionPreference='Stop'
$cfg=Get-Content -LiteralPath $Config -Raw | ConvertFrom-Json
$results=Split-Path -Parent (Resolve-Path -LiteralPath $Config)
$metadata=Get-Content -LiteralPath (Join-Path $results ($Label+'-metadata.json')) -Raw | ConvertFrom-Json
$wide=Join-Path $PSScriptRoot 'PrefixKernel128.cs'; $arithmetic=Join-Path $PSScriptRoot 'WideInteger.cs'
if((Get-FileHash -LiteralPath $Config).Hash -ne $metadata.configHash) {throw 'Config changed since launch'}
if((Get-FileHash -LiteralPath $wide).Hash -ne $metadata.sourceHash) {throw 'Kernel changed since launch'}
if((Get-FileHash -LiteralPath $arithmetic).Hash -ne $metadata.arithmeticHash) {throw 'Arithmetic changed since launch'}
Add-Type -Path @((Join-Path $PSScriptRoot 'PrefixKernel.cs'),$arithmetic,$wide,(Join-Path $PSScriptRoot 'PartitionAudit.cs')) -CompilerOptions '/optimize+'
$receipt=[CollatzPartitionAudit]::Compare([int]$cfg.m,[string]$cfg.low,[string]$cfg.high,[string[]]$cfg.targets,[int]$cfg.depth,$Split)
$receipt | Set-Content -LiteralPath (Join-Path $results ($Label+'-partition-audit.json'))
$receipt
