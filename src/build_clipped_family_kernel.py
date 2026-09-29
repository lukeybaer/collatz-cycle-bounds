"""Generate a separate family kernel with certified monotone suffix clipping."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'src';R=ROOT/'results'
original=S/'FamilyCapacityPreciseFast.cs';text=original.read_text()
old='''  if(LogBound(nlo+1,true)<=Target(lo,j)){Restart+=Count(lo,hi,mod);return;}
  // An exact descent also implies restart because F_j(y)>=y for y>=71.'''
new='''  if(LogBound(nlo+1,true)<=Target(lo,j)){Restart+=Count(lo,hi,mod);return;}
  // A passed sufficient test at ANY a certifies every larger a by the
  // exact monotonicity lemma. Rounded tests themselves need not be monotone.
  if(LogBound(nhi+1,true)<=Target(hi,j)) {
   BigInteger bad=0,good=Count(lo,hi,mod)-1;
   while(good-bad>1) {
    BigInteger mid=(bad+good)/2,am=lo+mid*mod,nm=(P*am+Q)>>S;
    if(LogBound(nm+1,true)<=Target(am,j))good=mid;else bad=mid;
   }
   BigInteger cut=lo+good*mod;
   if(cut<=lo || cut>hi || LogBound(((P*cut+Q)>>S)+1,true)>Target(cut,j))throw new Exception("restart suffix witness");
   Restart+=Count(cut,hi,mod);hi=cut-mod;nhi=(P*hi+Q)>>S;
   if(lo==hi){Single(lo,nlo);return;}
  }
  // An exact descent also implies restart because F_j(y)>=y for y>=71.'''
assert text.count(old)==1;text=text.replace(old,new)
old='''  if(slope*worst+intercept<=0){Restart+=Count(lo,hi,mod);return;}
  if(j>=d.MaxDepth)throw new Exception("depth_limit");'''
new='''  if(slope*worst+intercept<=0){Restart+=Count(lo,hi,mod);return;}
  // Q+den>=0. A decreasing affine difference may certify a proper suffix.
  if(slope<0 && slope*hi+intercept<=0) {
   BigInteger threshold=(intercept-slope-1)/(-slope);
   BigInteger cut=lo+((threshold-lo+mod-1)/mod)*mod;
   if(cut<=lo || cut>hi || slope*cut+intercept>0)throw new Exception("descent suffix witness");
   Restart+=Count(cut,hi,mod);hi=cut-mod;nhi=(P*hi+Q)>>S;
   if(lo==hi){Single(lo,nlo);return;}
  }
  if(j>=d.MaxDepth)throw new Exception("depth_limit");'''
assert text.count(old)==1;text=text.replace(old,new)
text=text.replace('CollatzFamiliesPreciseFast','CollatzFamiliesClipped')
target=S/'FamilyCapacityClipped.cs';target.write_text(text)
runner=(S/'run_family_precise_fast.ps1').read_text().replace('FamilyCapacityPreciseFast.cs','FamilyCapacityClipped.cs').replace('CollatzFamiliesPreciseFast','CollatzFamiliesClipped')
(S/'run_family_clipped.ps1').write_text(runner)
(R/'clipped-family-source-derivation.json').write_text(json.dumps({
    'original_source_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
    'generated_source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
    'change':'Prune a tested valid restart suffix using exact monotonicity; prune exact affine-descent suffixes. Remaining progression is retained.'
},indent=2)+'\n')
print('Generated monotone suffix-clipping family kernel.')
