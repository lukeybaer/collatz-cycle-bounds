$ErrorActionPreference='Stop'
Add-Type -Path (Join-Path $PSScriptRoot 'WideInteger.cs')
$receipt=[CollatzWide.Arithmetic]::RunArithmeticTests(100000)
$results=Join-Path (Split-Path $PSScriptRoot -Parent) 'results'
$receipt | Set-Content -LiteralPath (Join-Path $results 'wide-arithmetic-test.json')
$receipt
