param(
 [Parameter(Mandatory=$true)][string]$Config,
 [Parameter(Mandatory=$true)][string]$ParentJournal,
 [Parameter(Mandatory=$true)][string]$ParentMetadata,
 [Parameter(Mandatory=$true)][string]$Label,
 [int]$Workers=8,[int]$Split=2,[long]$NodeLimit=2000000000
)
$ErrorActionPreference='Stop'
$cfg=Get-Content -LiteralPath $Config -Raw|ConvertFrom-Json
$parent=Get-Content -LiteralPath $ParentMetadata -Raw|ConvertFrom-Json
$resultDir=Split-Path -Parent (Resolve-Path -LiteralPath $Config)
$wide=Join-Path $PSScriptRoot 'PrefixKernel128.cs'
$arithmetic=Join-Path $PSScriptRoot 'WideInteger.cs'
$resume=Join-Path $PSScriptRoot 'ResumePrefixKernel.cs'
$configHash=(Get-FileHash -LiteralPath $Config).Hash
$sourceHash=(Get-FileHash -LiteralPath $wide).Hash
$arithmeticHash=(Get-FileHash -LiteralPath $arithmetic).Hash
if($parent.configHash -ne $configHash -or $parent.sourceHash -ne $sourceHash -or $parent.arithmeticHash -ne $arithmeticHash) {throw 'Parent source or configuration differs'}
if($parent.split -ne $Split) {throw 'Parent partition depth differs'}
$journal=Join-Path $resultDir ($Label+'-journal.jsonl')
$metadataPath=Join-Path $resultDir ($Label+'-metadata.json')
if((Test-Path -LiteralPath $journal) -or (Test-Path -LiteralPath $metadataPath)) {throw 'Refusing to overwrite a run label'}
# Opening without write sharing proves the checkpoint writer has closed it.
$checkpointStream=[System.IO.File]::Open((Resolve-Path -LiteralPath $ParentJournal),[System.IO.FileMode]::Open,[System.IO.FileAccess]::Read,[System.IO.FileShare]::Read)
try {
 $parentHash=[Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData($checkpointStream))
 $meta=[ordered]@{
  startedUtc=[DateTime]::UtcNow.ToString('o');configHash=$configHash;sourceHash=$sourceHash;arithmeticHash=$arithmeticHash
  resumeSourceHash=(Get-FileHash -LiteralPath $resume).Hash
  parentJournal=(Resolve-Path -LiteralPath $ParentJournal).Path;parentJournalHash=$parentHash
  parentMetadata=(Resolve-Path -LiteralPath $ParentMetadata).Path;parentMetadataHash=(Get-FileHash -LiteralPath $ParentMetadata).Hash
  config=$cfg;workers=$Workers;split=$Split;nodeLimit=$NodeLimit;label=$Label
  compilerOptimization='release /optimize+';powershell=$PSVersionTable.PSVersion.ToString();runtime=[Environment]::Version.ToString()
 }
 $meta|ConvertTo-Json -Depth 20|Set-Content -LiteralPath $metadataPath
 Add-Type -Path @((Join-Path $PSScriptRoot 'PrefixKernel.cs'),$arithmetic,$wide,$resume) -CompilerOptions '/optimize+'
 $result=[CollatzCheckpoint.Resumer]::Run([int]$cfg.m,[string]$cfg.low,[string]$cfg.high,[string[]]$cfg.targets,[int]$cfg.depth,$NodeLimit,$Workers,$Split,$journal,(Resolve-Path -LiteralPath $ParentJournal).Path,$parentHash)
 $result|Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-result.json'))
 $result
} finally {$checkpointStream.Dispose()}
