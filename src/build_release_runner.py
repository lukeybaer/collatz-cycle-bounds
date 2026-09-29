from pathlib import Path
root=Path(__file__).resolve().parent
s=(root/'run_native.ps1').read_text()
s=s.replace('Add-Type -Path $source',"Add-Type -Path $source -CompilerOptions '/optimize+'")
s=s.replace('config=$cfg',"compilerOptimization='release /optimize+'\n  config=$cfg")
(root/'run_reference_release.ps1').write_text(s)
print('Created release runner for unchanged BigInteger reference source.')
