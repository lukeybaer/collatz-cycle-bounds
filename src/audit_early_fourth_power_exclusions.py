"""Join exact92..95 profiles to the already frozen fourth-power capacity."""
from pathlib import Path
import hashlib,json
from verify_fourth_power_grafted_capacity import verify,NAME
from audit_early_fourth_power_profiles import main as check_profiles
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    verify();audit=check_profiles();assert audit['status']=='passed'
    path=R/'early-fourth-power-profile-proposals.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    assert data['source_sha256']==sha(ROOT/'src/early_fourth_power_profiles.py')
    assert [r['m'] for r in data['rows']]==[92,93,94,95]
    rows=[]
    for p in data['rows']:
        assert p['minimum_factor']==1 and int(p['minimum'])==X
        assert p['conditional_contradiction'] and int(p['final_K'])>int(p['upper_ceiling'])
        rows.append({k:p[k] for k in ('m','minimum','initial_K','final_K','upper_ceiling')})
    deps=[NAME,path.name,'early-fourth-power-profile-proposals-audit.json','K-lower-bounds-reproduction.json']
    src=['audit_early_fourth_power_exclusions.py','audit_early_fourth_power_profiles.py',
         'early_fourth_power_profiles.py','fourth_power_grafted_profile_proposals.py',
         'verify_fourth_power_grafted_capacity.py','verify_certificates.py']
    out={'status':'passed','rows':rows,'additional_minimum_window_search_required':False,
         'capacity_certificate':NAME,'externally_reviewed':False,'novelty_confirmed':False,
         'dependencies':{n:sha(R/n) for n in deps},
         'source_dependencies':{n:sha(ROOT/'src'/n) for n in src},
         'scope':'Alternative direct internal exclusions for92..95 using the frozen capacity; these cases were previously known. Published basin, p-adic theorem and cycle-size upper bounds remain dependencies.'}
    (R/'cycle-exclusions-m92-m95-fourth-power-direct-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('PASSED direct early exclusions:',[(r['m'],r['final_K']) for r in rows],flush=True)
if __name__=='__main__':main()
