"""Derive an auditable optimization variant, retaining the original kernel."""
from pathlib import Path

root=Path(__file__).resolve().parent
s=(root/'PrefixKernel.cs').read_text()

def change(old,new,count=1):
    global s
    assert s.count(old)==count,(old,s.count(old),count)
    s=s.replace(old,new)

change('namespace CollatzExact {','namespace CollatzFast {')
change('public readonly int M,Depth,Bits;','public readonly int M,Depth,Bits,Batch;')
change('string[] targets,int depth) {','string[] targets,int depth,int batch=1) {')
change('M=m;Low=','M=m;Batch=batch;Low=')
change('Three=new BigInteger[Bits+1];Inverse=new BigInteger[Bits+1];',
       'Three=new BigInteger[Math.Max(Bits+1,1025)];Inverse=new BigInteger[Bits+1];')
change('for(int i=1;i<=Bits;i++){Three[i]=Three[i-1]*3;Inverse[i]=(Inverse[i-1]*inv3)&Mask;}',
       'for(int i=1;i<Three.Length;i++)Three[i]=Three[i-1]*3;\n        for(int i=1;i<=Bits;i++)Inverse[i]=(Inverse[i-1]*inv3)&Mask;')
change('x%=modulus;return x.Sign<0?x+modulus:x;',
       'return x&(modulus-1); /* All callers use a positive power of two. */')
change('BigInteger.Pow(3,k)*((n+1)>>k)-1',
       '(k<d.Three.Length?d.Three[k]:BigInteger.Pow(3,k))*((n+1)>>k)-1')
change('if(first==last){Single(first,(P*first+Q)>>S,c,used);return;}',
       'if(((last-first)>>(S+1))<d.Batch){for(var seed=first;seed<=last;seed+=mod)Single(seed,(P*seed+Q)>>S,c,used);return;}')
change('int workers,int split,string journal) {','int workers,int split,string journal,int batch=1) {')
change('new Data(m,low,high,targets,depth);','new Data(m,low,high,targets,depth,batch);')
(root/'PrefixKernelFast.cs').write_text(s)

p=(root/'run_native.ps1').read_text().replace('PrefixKernel.cs','PrefixKernelFast.cs').replace('CollatzExact.','CollatzFast.')
p=p.replace("[string]$Label='native'","[int]$Batch=1,\n  [string]$Label='native-fast'")
p=p.replace('workers=$Workers','workers=$Workers\n  batch=$Batch')
p=p.replace('$Workers,$Split,$journal)','$Workers,$Split,$journal,$Batch)')
(root/'run_fast.ps1').write_text(p)

t=(root/'test_native.ps1').read_text().replace('PrefixKernel.cs','PrefixKernelFast.cs').replace('CollatzExact.','CollatzFast.')
t=t.replace('$count=0','$count=0\nforeach($batch in @(1,4,16,64)) {')
t=t.replace('[int]$case.m)\n  $kernel','[int]$case.m,$batch)\n  $kernel')
t=t.replace('$receipt=@{','}\n$receipt=@{')
t=t.replace('native-test-receipt.json','fast-native-test-receipt.json')
(root/'test_fast.ps1').write_text(t)
print('Created separate fast source, runner, and four-batch comparison test.')
