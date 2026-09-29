$ErrorActionPreference='Stop'
Add-Type -Path (Join-Path $PSScriptRoot 'PrefixKernel.cs')
$results=Join-Path (Split-Path $PSScriptRoot -Parent) 'results'
$cases=Get-Content -LiteralPath (Join-Path $results 'native-test-cases.json') -Raw | ConvertFrom-Json
$count=0
foreach($case in $cases) {
  $data=[CollatzExact.Data]::new([int]$case.m,[string]$case.low,[string]$case.high,[string[]]$case.targets,[int]$case.m)
  $kernel=[CollatzExact.Kernel]::new($data,1000000)
  $state=[CollatzExact.State]::new(1,0,0,$data.Low,$data.High,1,0,0)
  $kernel.Visit($state)
  $actual=@($kernel.Seeds | ForEach-Object { $_.ToString() } | Sort-Object)
  $expected=@($case.expected | Sort-Object)
  if (($actual -join ',') -ne ($expected -join ',')) {throw "Mismatch in case $count"}
  $count++
}
$receipt=@{status='passed';cases=$count;method='Compiled BigInteger branch search compared with Python direct shortcut iteration'} | ConvertTo-Json
$receipt | Set-Content -LiteralPath (Join-Path $results 'native-test-receipt.json')
$receipt
