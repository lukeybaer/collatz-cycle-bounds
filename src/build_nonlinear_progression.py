"""Separate exact progression-bisection proof for the proposed nonlinear map."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'src';R=ROOT/'results'
source=S/'ProgressionCapacityVerifier.cs';text=source.read_text()
old='''    numerator=1584962*numerator-(100*input.J-1)*(denominator/100)*1000000;
    denominator*=1000000;'''
new='''    BigInteger grown=1584962*numerator;
    BigInteger first=grown-3799*(denominator/100)*1000000;
    BigInteger last=grown-4099*(denominator/100)*1000000;
    BigInteger middle=numerator*1000000+3542302*denominator;
    numerator=BigInteger.Max(last,BigInteger.Min(first,middle));
    denominator*=1000000;'''
assert text.count(old)==1;text=text.replace(old,new)
old='input.J<31 || input.J>41';assert text.count(old)==1;text=text.replace(old,'input.J!=41')
old='Conditional=input.assumed_cycle_minimum!=null;'
assert text.count(old)==1;text=text.replace(old,old+'\n  if(Conditional)throw new Exception("nonlinear proof requires the original basin input");')
text=text.replace('CollatzProgressionAudit','CollatzNonlinearProgressionAudit')
old=' public static string Run(string json,int workers,int depth,long nodeLimit,int take=0) {'
new=''' public static string DumpLimits(string json,int depth) {
  Input input=JsonSerializer.Deserialize<Input>(json);var data=new Data(input,depth,1);
  return JsonSerializer.Serialize(data.Limits);
 }
'''+old
assert text.count(old)==1;text=text.replace(old,new)
old='J=input.J,classes=length,seeds=seeds.ToString(),';assert text.count(old)==1
text=text.replace(old,'capacity_kind="nonlinear_block_restart",linear_coefficient_certified=false,map_id="plateau-c3799-c4099-h71",J=input.J,classes=length,seeds=seeds.ToString(),')
target=S/'NonlinearProgressionCapacityVerifier.cs';assert not target.exists();target.write_text(text)
runner=(S/'run_progression_verifier.ps1').read_text().replace('ProgressionCapacityVerifier.cs','NonlinearProgressionCapacityVerifier.cs').replace('CollatzProgressionAudit','CollatzNonlinearProgressionAudit')
runner=runner.replace('status,full_input,capacity_exceptions_discharged,','status,full_input,capacity_exceptions_discharged,capacity_kind,linear_coefficient_certified,map_id,')
(S/'run_nonlinear_progression.ps1').write_text(runner)
(R/'nonlinear-progression-source-derivation.json').write_text(json.dumps({
    'original_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'generated_source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
    'map_id':'plateau-c3799-c4099-h71','change':'Exact rational nonlinear thresholds; global J41 input only. Progression parity bisection and singleton verification unchanged.'
},indent=2)+'\n')
print('Generated independent nonlinear progression checker.')
