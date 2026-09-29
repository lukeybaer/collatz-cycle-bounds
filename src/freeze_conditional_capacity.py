"""Freeze a complete conditional proof pair and its conditional final profiles."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
from audit_native_family_proofs import audit
from affine_profile_certificates import certificate
from build_family_inputs import exploratory
from cycle_bounds_explore import D
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main(J,factor,producer,progression):
    pair=audit(J,producer,'ConditionalFamilyCapacity.cs',progression,factor)
    pair_name=progression+'-proof-pair-audit.json';c=F(100*J-1,100)
    capname=f'conditional-capacity-J{J}-f{factor}-certificate.json'
    cert={'kind':'conditional_block_restart','J':J,'capacity_c':str(c),'capacity_certified':True,
          'conditional_only':True,'verified_basin':str(X),'assumed_cycle_minimum':str(factor*X),
          'minimum_factor':factor,'producer':producer,'producer_source':'ConditionalFamilyCapacity.cs','progression':progression,
          'scope':'Only hypothetical cycles all of whose members exceed the explicit assumed minimum.',
          'warning':'This is not an extension of the verified convergence basin, nor a uniform coefficient at the original basin.',
          'proof':'../conditional-capacity.md','audit_source_sha256':sha(ROOT/'src'/'audit_native_family_proofs.py'),
          'source_dependencies':pair['source_dependencies'],
          'dependencies':dict(pair['dependencies'],**{pair_name:sha(R/pair_name)})}
    (R/capname).write_text(json.dumps(cert,indent=2)+'\n')
    initial=205632218873398596256;profiles=[]
    for m in range(99,105):
        low=factor;high=128
        if not exploratory(m,high,initial,D(c.numerator)/D(c.denominator)):
            print('No explored contradiction:',m,flush=True);continue
        while low<high:
            middle=(low+high)//2
            if exploratory(m,middle,initial,D(c.numerator)/D(c.denominator)):high=middle
            else:low=middle+1
        row=certificate(m,low*X,initial,c)
        assert row['conditional_contradiction']
        row.update(capacity_certificate=capname,minimum_factor=low,
                   warning='Both the capacity minimum hypothesis and the finite global-minimum window must be discharged.')
        profiles.append(row)
        (R/f'conditional-J{J}-f{factor}-profile-certificates.json').write_text(json.dumps(profiles,indent=2)+'\n')
        print('Conditional capacity',J,'m',m,'final factor',low,'K',row['final_K'],flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--J',type=int,default=41);p.add_argument('--factor',type=int,default=16)
    p.add_argument('--producer',default='conditional-J41-f16-full');p.add_argument('--progression',default='conditional-J41-f16-progression-full')
    a=p.parse_args();main(a.J,a.factor,a.producer,a.progression)
