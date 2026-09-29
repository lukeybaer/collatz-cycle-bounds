$ErrorActionPreference='Stop'
Add-Type -Path @((Join-Path $PSScriptRoot 'WideInteger.cs'),(Join-Path $PSScriptRoot 'PrefixKernel128.cs')) -CompilerOptions '/optimize+'
$results=Join-Path (Split-Path $PSScriptRoot -Parent) 'results'
$cases=Get-Content -LiteralPath (Join-Path $results 'native-test-cases.json') -Raw | ConvertFrom-Json
$count=0
foreach($case in $cases) {
  $data=[CollatzWide.Data]::new([int]$case.m,[string]$case.low,[string]$case.high,[string[]]$case.targets,[int]$case.m)
  $kernel=[CollatzWide.Kernel]::new($data,1000000)
  $kernel.Visit([CollatzWide.Kernel]::Root($data))
  $actual=@($kernel.Seeds | ForEach-Object { $_.ToString() } | Sort-Object)
  $expected=@($case.expected | Sort-Object)
  if (($actual -join ',') -ne ($expected -join ',')) {throw "Mismatch in case $count"}
  $count++
}
$receipt=@{status='passed';cases=$count;method='UInt128 kernel compared with Python direct shortcut iteration'} | ConvertTo-Json
$receipt | Set-Content -LiteralPath (Join-Path $results 'kernel128-test-receipt.json')
$receipt
