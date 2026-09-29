"""Derive a separate experimental kernel for the nonlinear growth map.

Frozen linear kernels are not modified. Successful output is a nonlinear
block-restart proof only; it must never be read as a uniform c40.99 proof.
"""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'src';R=ROOT/'results'
source=S/'FamilyCapacityClipped.cs';text=source.read_text()
old='''  for(int i=0;i<j;i++)lower=checked((long)(((Int128)1584962*lower)/1000000)-d.CScaled);
  return lower;'''
new='''  for(int i=0;i<j;i++) {
   // Directed lower enclosure of the continuous nonlinear map:
   // max(d*y-40.99,min(d*y-37.99,y+71*(d-1)-37.99)).
   long grown=checked((long)(((Int128)1584962*lower)/1000000));
   long first=checked(grown-37990000000L),last=checked(grown-40990000000L);
   long middle=checked(lower+3542302000L);
   lower=Math.Max(last,Math.Min(first,middle));
  }
  return lower;'''
assert text.count(old)==1;text=text.replace(old,new)
old='if(input.J<2 || input.J>41 || BigInteger.Parse(input.verified_basin)!=X)'
assert text.count(old)==1;text=text.replace(old,'if(input.J!=41 || BigInteger.Parse(input.verified_basin)!=X)')
text=text.replace('CollatzFamiliesClipped','CollatzNonlinearFamilies')
old='J=input.J,classes=length,seeds=expected.ToString(),'
assert text.count(old)==1
text=text.replace(old,'capacity_kind="nonlinear_block_restart",linear_coefficient_certified=false,map_id="plateau-c3799-c4099-h71",J=input.J,classes=length,seeds=expected.ToString(),')
target=S/'NonlinearFamilyCapacity.cs';assert not target.exists();target.write_text(text)
runner=(S/'run_family_clipped.ps1').read_text().replace('FamilyCapacityClipped.cs','NonlinearFamilyCapacity.cs').replace('CollatzFamiliesClipped','CollatzNonlinearFamilies')
runner=runner.replace('status,full_input,capacity_exceptions_discharged,J,','status,full_input,capacity_exceptions_discharged,capacity_kind,linear_coefficient_certified,map_id,J,')
(S/'run_nonlinear_family.ps1').write_text(runner)
(R/'nonlinear-family-source-derivation.json').write_text(json.dumps({
    'original_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'generated_source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
    'map_id':'plateau-c3799-c4099-h71','c0':'3799/100','c1':'4099/100','h':71,
    'change':'Only the iterated restart envelope, fixed J41 conservative input scope, and output type change. Existing sources remain frozen.',
    'warning':'Experimental nonlinear capacity, not a certified uniform linear coefficient.'
},indent=2)+'\n')
print('Generated separate nonlinear experimental family proof.')
