param(
 [Parameter(Mandatory=$true)][string]$InputFile,
 [int]$Workers=8,
 [switch]$Reference,
 [string]$Label='basin'
)
$ErrorActionPreference='Stop'
$source=Join-Path $PSScriptRoot 'BasinVerifier.cs'
$resultDir=Split-Path -Parent (Resolve-Path -LiteralPath $InputFile)
$meta=[ordered]@{
 startedUtc=[DateTime]::UtcNow.ToString('o');
 inputHash=(Get-FileHash -LiteralPath $InputFile -Algorithm SHA256).Hash;
 sourceHash=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash;
 referencePath=$Reference.IsPresent;workers=$Workers;compilerOptimization='release /optimize+';
 powershell=$PSVersionTable.PSVersion.ToString();runtime=[Environment]::Version.ToString()
}
$meta | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-metadata.json'))
Add-Type -Path $source -CompilerOptions '/optimize+'
$result=[CollatzBasin.Verifier]::Run((Get-Content -LiteralPath $InputFile -Raw),$Reference.IsPresent,$Workers)
$result | Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-result.json'))
($result | ConvertFrom-Json) | Select-Object status,all_enter_verified_basin,seeds,odd_steps,max_steps,max_bits,bigint_steps,seconds | ConvertTo-Json
