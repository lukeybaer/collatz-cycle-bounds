"""Create a separate exact family producer with checked UInt128 singleton steps.

The original producer sources remain frozen. Only singleton evaluation changes;
full per-class counter comparisons against the BigInteger source are required.
"""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'src';R=ROOT/'results'
original=S/'FamilyCapacityPrecise.cs'
text=original.read_text()
old=''' void Single(BigInteger a,BigInteger n) {
  if(n<=0 || n.IsEven)throw new Exception("invalid singleton minimum");
  int steps=0;
  while(n>d.X) {
   if(++steps>1000000 || n.GetBitLength()>4096)throw new Exception("singleton limit at a="+a);
   n=3*n+1;n>>=Val(n);
  }
  Singles++;SingleSteps+=steps;
 }'''
new=''' static int Val128(UInt128 n) {
  if(n==0)throw new Exception("zero valuation");
  ulong low=(ulong)n;
  return low!=0?BitOperations.TrailingZeroCount(low):64+BitOperations.TrailingZeroCount((ulong)(n>>64));
 }
 void Single(BigInteger a,BigInteger n) {
  if(n<=0 || n.IsEven)throw new Exception("invalid singleton minimum");
  int steps=0;UInt128 cut=(UInt128)d.X,guard=(UInt128.MaxValue-1)/3;
  while(n>d.X) {
   if(n.GetBitLength()<=128) {
    UInt128 small=(UInt128)n;
    while(small>cut && small<=guard) {
     if(++steps>1000000)throw new Exception("singleton limit at a="+a);
     small=3*small+1;small>>=Val128(small);
    }
    n=(BigInteger)small;
    if(n<=d.X)break;
   }
   if(++steps>1000000 || n.GetBitLength()>4096)throw new Exception("singleton limit at a="+a);
   n=3*n+1;n>>=Val(n);
  }
  Singles++;SingleSteps+=steps;
 }'''
assert text.count(old)==1
text=text.replace(old,new).replace('CollatzFamiliesPrecise','CollatzFamiliesPreciseFast')
target=S/'FamilyCapacityPreciseFast.cs';target.write_text(text)
runner=(S/'run_family_precise.ps1').read_text().replace('FamilyCapacityPrecise.cs','FamilyCapacityPreciseFast.cs').replace('CollatzFamiliesPrecise','CollatzFamiliesPreciseFast')
(S/'run_family_precise_fast.ps1').write_text(runner)
(R/'fast-family-source-derivation.json').write_text(json.dumps({
    'original_source_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
    'generated_source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
    'change':'Exact UInt128 singleton odd iteration with pre-multiplication guard and BigInteger fallback; family enumeration unchanged.'
},indent=2)+'\n')
print('Generated separate fast family producer.')
