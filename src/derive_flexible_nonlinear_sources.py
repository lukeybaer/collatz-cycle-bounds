"""Parameterize the lower intercept in separately named nonlinear verifiers."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'src';R=ROOT/'results'
items=[]
for oldname,newname,oldns,newns,runner,newrunner in (
 ('HighNonlinearFamilyCapacity.cs','FlexibleNonlinearFamilyCapacity.cs','CollatzHighNonlinearFamilies','CollatzFlexibleNonlinearFamilies','run_high_nonlinear_family.ps1','run_flexible_nonlinear_family.ps1'),
 ('HighNonlinearProgressionVerifier.cs','FlexibleNonlinearProgressionVerifier.cs','CollatzHighNonlinearProgressionAudit','CollatzFlexibleNonlinearProgressionAudit','run_high_nonlinear_progression.ps1','run_flexible_nonlinear_progression.ps1')):
    old=S/oldname;new=S/newname;assert not new.exists();text=old.read_text().replace(oldns,newns)
    text=text.replace('public int J{get;set;}','public int J{get;set;} public int low_c_numerator{get;set;}')
    text=text.replace('map_id="plateau-c3799-c"+(100*input.J-1).ToString()+"-h71"',
                      'map_id="plateau-c"+input.low_c_numerator.ToString()+"-c"+(100*input.J-1).ToString()+"-h71"')
    check='''if(input.low_c_numerator<3799 || input.low_c_numerator>4153 || input.low_c_numerator>=100*input.J-1)throw new Exception("lower-intercept scope");'''
    if oldname=='HighNonlinearFamilyCapacity.cs':
        text=text.replace('public readonly long CScaled;','public readonly long CScaled,LowCScaled,OffsetScaled;')
        text=text.replace('CScaled=(100*input.J-1)*10000000L;',
            'CScaled=(100*input.J-1)*10000000L;\n  '+check+'\n  LowCScaled=input.low_c_numerator*10000000L;OffsetScaled=71L*584962*1000-LowCScaled;\n  if(OffsetScaled<=0)throw new Exception("map below identity");')
        text=text.replace('grown-37990000000L','grown-d.LowCScaled').replace('lower+3542302000L','lower+d.OffsetScaled')
    else:
        text=text.replace('BigInteger verified=BigInteger.One<<71;',check+'\n  BigInteger verified=BigInteger.One<<71;')
        text=text.replace('grown-3799*(denominator/100)*1000000','grown-input.low_c_numerator*(denominator/100)*1000000')
        text=text.replace('numerator*1000000+3542302*denominator','numerator*1000000+(71L*584962-input.low_c_numerator*10000L)*denominator')
    new.write_text(text)
    runtext=(S/runner).read_text().replace(oldname,newname).replace(oldns,newns)
    (S/newrunner).write_text(runtext)
    items.append({'original':oldname,'original_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),
                  'generated':newname,'generated_sha256':hashlib.sha256(new.read_bytes()).hexdigest(),
                  'scope':'J42..48; 3799<=low_c_numerator<=4153, smaller than100J-1; map height floor71.'})
(R/'flexible-nonlinear-source-derivations.json').write_text(json.dumps(items,indent=2)+'\n')
base=R/'high-capacity-J42-classes.json';data=json.loads(base.read_text());data['low_c_numerator']=4150
data['map_id']='plateau-c4150-c4199-h71';data['source_class_file']=base.name;data['source_class_sha256']=hashlib.sha256(base.read_bytes()).hexdigest()
target=R/'flexible-capacity-J42-c4150-classes.json';assert not target.exists();target.write_text(json.dumps(data,indent=2)+'\n')
print('Prepared map plateau-c4150-c4199-h71 for independent trials',flush=True)
