"""Close the factor-one cases without a further minimum-window search."""
from pathlib import Path
import hashlib,json
from verify_fourth_power_grafted_capacity import verify,NAME
from audit_fourth_power_grafted_profiles import main as audit_profiles
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))

def main():
    verify();assert audit_profiles()['status']=='passed'
    profile_name='fourth-power-grafted-profile-certificates.json'
    profiles=read(R/profile_name)
    assert profiles['capacity_map_proved'] and profiles['capacity_certificate']==NAME
    assert profiles['capacity_certificate_sha256']==sha(R/NAME)
    rows=[]
    for m in (96,97,98):
        selected=[r for r in profiles['rows'] if r['m']==m];assert len(selected)==1
        p=selected[0]
        assert p['capacity_map_proved'] and p['capacity_certificate']==NAME
        assert p['capacity_certificate_sha256']==sha(R/NAME)
        assert p['minimum_factor']==1 and int(p['minimum'])==X
        assert not p['requires_minimum_search'] and p['conditional_contradiction']
        assert int(p['final_K'])>int(p['upper_ceiling'])
        rows.append({'m':m,'minimum_lower':str(X),'initial_K':str(p['initial_K']),
                     'final_K':str(p['final_K']),'upper_ceiling':p['upper_ceiling'],
                     'additional_minimum_window_search_required':False})
    deps=[NAME,profile_name,'fourth-power-grafted-profile-proposals.json',
          'fourth-power-grafted-profile-proposals-audit.json','K-lower-bounds-family-J38.json']
    src=['audit_fourth_power_direct_exclusions.py','verify_fourth_power_grafted_capacity.py',
         'audit_fourth_power_grafted_profiles.py','verify_certificates.py']
    out={'status':'passed','rows':rows,'externally_reviewed':False,'novelty_confirmed':False,
         'dependencies':{n:sha(R/n) for n in deps},
         'source_dependencies':{n:sha(ROOT/'src'/n) for n in src},
         'external_inputs':['Published convergence below 2^71; endpoint is a power of two.',
                            'Bugeaud1999 Theorem1 rational clause(6).',
                            'Simons-de Weger2010 Theorem3(d) in its stated middle range.'],
         'scope':'Candidate exclusions for exactly96,97,98 local minima. Uses completed finite-capacity proofs and the analytic tail; no additional minimum-window search is needed. Not a proof of Collatz convergence.'}
    (R/'cycle-exclusions-m96-m98-fourth-power-direct-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':out['status'],'rows':rows}),flush=True)

if __name__=='__main__':main()
