"""Freeze the checked analytic-tail graft and bind exact profile proposals."""
from pathlib import Path
import json,hashlib
from audit_dual_tail_capacity import audit,MAP
from audit_dual_tail_profiles import main as audit_profiles
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
NAME='dual-tail-capacity-certificate.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    path=R/NAME;assert not path.exists(),'Refusing to overwrite a frozen certificate'
    graft=audit(write=False)
    assert graft==json.loads((R/'dual-tail-capacity-audit.json').read_text())
    profile=audit_profiles();assert profile['status']=='passed'
    dependencies=['dual-tail-capacity-audit.json','dual-tail-profile-proposals.json','dual-tail-profile-proposals-audit.json']
    dependencies+=list(graft['dependencies'])
    certificate={'kind':'dual_analytic_tail_graft','map_id':MAP,'capacity_certified':True,
                 'externally_reviewed':False,'novelty_confirmed':False,
                 'linear_coefficient_certified':False,'conditional_only':False,
                 'verified_basin':str(2**71),'domain_height_floor':71,'parameters':graft['parameters'],
                 'definition':'min(Phi0(y),(log2(3)-1/93)*y+18400/93-c1,(log2(3)-1/83)*y+164000/83-c1)',
                 'scope':'Positive orbit segments avoiding the verified basin; in particular all hypothetical nontrivial positive cycles.',
                 'dependencies':{name:sha(R/name) for name in sorted(set(dependencies))},
                 'proof_dependencies':graft['proof_dependencies'],
                 'source_dependencies':dict(graft['source_dependencies'],**{name:sha(ROOT/'src'/name) for name in
                     ('audit_dual_tail_capacity.py','audit_dual_tail_profiles.py','dual_tail_profile_proposals.py','freeze_dual_tail_capacity.py')}),
                 'warning':'Internally checked finite/analytic capacity, not an external mathematical review or a completed cycle exclusion.'}
    path.write_text(json.dumps(certificate,indent=2)+'\n')
    data=json.loads((R/'dual-tail-profile-proposals.json').read_text())
    for row in data['rows']:
        row.update(capacity_map_proved=True,capacity_certificate=NAME,capacity_certificate_sha256=sha(path),
                   requires_minimum_search=row['minimum_factor']>1,
                   warning='The graft and exact profile arithmetic are internally checked. Any indicated minimum window still requires a complete exclusion; external review and priority remain pending.')
    data['status']='internally_certified_profiles';data['capacity_map_proved']=True
    data['capacity_certificate']=NAME;data['capacity_certificate_sha256']=sha(path)
    data['warning']='No additional cycle exclusion follows without the required minimum-window search.'
    (R/'dual-tail-profile-certificates.json').write_text(json.dumps(data,indent=2)+'\n')
    print('FROZEN',NAME,flush=True)
if __name__=='__main__':main()
