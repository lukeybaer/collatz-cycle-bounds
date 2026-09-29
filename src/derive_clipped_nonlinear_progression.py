"""Add certified suffix clipping to a separate precise progression source."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'src';R=ROOT/'results'
base=S/'PreciseNonlinearProgressionVerifier.cs';text=base.read_text()
text=text.replace('namespace CollatzPreciseNonlinearProgressionAudit {','namespace CollatzClippedNonlinearProgressionAudit {')
old='''  BigInteger high=n+stride*(count-1);
  BigInteger firstDifference=n-((a<<rootK)-1);'''
new='''  BigInteger high=n+stride*(count-1);
  if(UpperLog(high+1)<=Limit(a+(count-1)*mod,j)) {
   // A passed endpoint certifies its entire suffix by the checked invariant
   // (n+1)*mod-stride*a>=0 and Phi-iterate slopes >=1.
   // The rounded test itself need not be monotone: the right endpoint
   // remains a certified passing endpoint at every bisection step.
   BigInteger left=0,right=count-1;
   while(left<right) {
    BigInteger middle=(left+right)/2;
    if(UpperLog(n+middle*stride+1)<=Limit(a+middle*mod,j))right=middle;
    else left=middle+1;
   }
   Restart+=count-right;count=right;
   if(count==0)return;
   if(count==1){Single(n);return;}
   high=n+stride*(count-1);
  }
  BigInteger firstDifference=n-((a<<rootK)-1);'''
assert text.count(old)==1;text=text.replace(old,new)
text=text.replace('height_method="exact_rational_mantissa_grid"','height_method="exact_rational_mantissa_grid_clipped"')
target=S/'ClippedNonlinearProgressionVerifier.cs';assert not target.exists();target.write_text(text)
runner=(S/'run_precise_nonlinear_progression.ps1').read_text().replace('PreciseNonlinearProgressionVerifier.cs','ClippedNonlinearProgressionVerifier.cs').replace('CollatzPreciseNonlinearProgressionAudit','CollatzClippedNonlinearProgressionAudit')
runner_target=S/'run_clipped_nonlinear_progression.ps1';assert not runner_target.exists();runner_target.write_text(runner)
result={'original_source_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),
        'generated_source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
        'map_id':'plateau-c3799-c4099-h71','change':'After lower-endpoint restart fails, a certified passing endpoint discharges its whole suffix using the proved monotone restart difference. Parity bisection, rational thresholds and singleton arithmetic remain unchanged.',
        'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(R/'clipped-nonlinear-progression-source-derivation.json').write_text(json.dumps(result,indent=2)+'\n')
print(target,flush=True)
