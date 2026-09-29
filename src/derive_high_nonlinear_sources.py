"""Separate higher-tail map implementations; no existing proof source changes."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'src';R=ROOT/'results'
items=[]
for oldname,newname,oldns,newns,runner,newrunner in (
    ('NonlinearFamilyCapacity.cs','HighNonlinearFamilyCapacity.cs','CollatzNonlinearFamilies','CollatzHighNonlinearFamilies','run_nonlinear_family.ps1','run_high_nonlinear_family.ps1'),
    ('ClippedNonlinearProgressionVerifier.cs','HighNonlinearProgressionVerifier.cs','CollatzClippedNonlinearProgressionAudit','CollatzHighNonlinearProgressionAudit','run_clipped_nonlinear_progression.ps1','run_high_nonlinear_progression.ps1')):
    old=S/oldname;new=S/newname;assert not new.exists()
    text=old.read_text().replace(oldns,newns)
    text=text.replace('input.J!=41','(input.J<42 || input.J>48)')
    text=text.replace('map_id="plateau-c3799-c4099-h71"','map_id="plateau-c3799-c"+(100*input.J-1).ToString()+"-h71"')
    if oldname=='NonlinearFamilyCapacity.cs':
        text=text.replace('bits>70','bits>83').replace('grown-40990000000L','grown-d.CScaled')
        text=text.replace('max(d*y-40.99,min(d*y-37.99,y+71*(d-1)-37.99))','max(d*y-(J-.01),min(d*y-37.99,y+71*(d-1)-37.99))')
    else:
        text=text.replace('grown-4099*(denominator/100)*1000000','grown-(100*input.J-1)*(denominator/100)*1000000')
    new.write_text(text)
    runtext=(S/runner).read_text().replace(oldname,newname).replace(oldns,newns)
    (S/newrunner).write_text(runtext)
    items.append({'original':oldname,'original_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),
                  'generated':newname,'generated_sha256':hashlib.sha256(new.read_bytes()).hexdigest(),
                  'scope':'J42..48, c0=37.99, c1=J-.01, h=71; no uniform linear coefficient claimed.'})
(R/'high-nonlinear-source-derivations.json').write_text(json.dumps(items,indent=2)+'\n')
print('Generated separate higher nonlinear map implementations',flush=True)
