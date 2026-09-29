$ErrorActionPreference='Stop'
Add-Type -Path @((Join-Path $PSScriptRoot 'WideInteger.cs'),(Join-Path $PSScriptRoot 'PrefixKernel128.cs')) -CompilerOptions '/optimize+'
$results=Join-Path (Split-Path $PSScriptRoot -Parent) 'results'
$cases=Get-Content -LiteralPath (Join-Path $results 'singleton-test-cases.json') -Raw | ConvertFrom-Json
$count=0; $fallbacks=0
foreach($case in $cases) {
  $data=[CollatzWide.Data]::new([int]$case.m,[string]$case.original,[string]$case.original,[string[]]$case.targets,[int]$case.m)
  $kernel=[CollatzWide.Kernel]::new($data,1000000)
  $kernel.TestSingleton([string]$case.original,[string]$case.current)
  if (($kernel.Survivors -gt 0) -ne $case.expected) {throw "Singleton mismatch in case $count"}
  $fallbacks+=$kernel.BigFallbacks; $count++
}
if($fallbacks -eq 0) {throw 'Overflow fallback was not exercised'}
$receipt=@{status='passed';cases=$count;bigIntegerFallbacks=$fallbacks;method='UInt128 singleton iteration and overflow fallback compared with Python direct shortcut iteration'} | ConvertTo-Json
$receipt | Set-Content -LiteralPath (Join-Path $results 'singleton-test-receipt.json')
$receipt
