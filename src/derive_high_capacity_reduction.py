"""Create separate producer/checker sources for the J42..49 reduction."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'src';R=ROOT/'results'
records=[]
for oldname,newname in [('build_extended_capacity_cases.py','build_high_capacity_cases.py'),
                        ('audit_extended_coverage.py','audit_high_capacity_coverage.py')]:
    old=S/oldname;new=S/newname;assert not new.exists()
    text=old.read_text().replace('31<=J<=41','42<=J<=49').replace('F(140,100)','F(168,100)')
    text=text.replace('<1700','<2000').replace('1700*F(153,10)','2000*F(153,10)').replace('q0<=69','q0<=83')
    text=text.replace('extended-capacity-J','high-capacity-J').replace('default=31','default=49')
    text=text.replace('Finite candidates for c<=40.99.','Finite conservative candidates for c<=48.99.')
    text=text.replace('A2=2^140','A2=2^168').replace('C<1700','C<2000')
    new.write_text(text)
    records.append({'original':oldname,'original_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),
                    'new':newname,'new_sha256':hashlib.sha256(new.read_bytes()).hexdigest()})
(R/'high-capacity-reduction-source-derivation.json').write_text(json.dumps(records,indent=2)+'\n')
print('Created separate high-capacity producer and independent coverage checker',flush=True)
