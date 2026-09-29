"""Freeze a uniform coefficient only after two complete native family proofs.

The inverse-residue and progression-index implementations are different
algorithms. Full Python comparisons validate the compiled progression method
on J35 and J38; those are not misrepresented as a full Python run for this J.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
from audit_native_family_proofs import audit
from exact_intervals import cycle_lower_bound,DHI
from affine_profile_certificates import certificate
from build_family_inputs import exploratory
from cycle_bounds_explore import D

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def save(name,value):(R/name).write_text(json.dumps(value,indent=2)+'\n')

def main(J,producer,source,progression):
    pair=audit(J,producer,source,progression)
    pair_name=progression+'-proof-pair-audit.json';c=F(100*J-1,100)
    capname=f'family-capacity-J{J}-native-pair-certificate.json'
    assert not (R/capname).exists(),'Do not silently overwrite a frozen certificate.'
    cap={'kind':'uniform_block_restart_native_pair','J':J,'capacity_c':str(c),'capacity_certified':True,
         'conditional_only':False,'verified_basin':str(X),'producer':producer,'producer_source':source,'progression':progression,
         'scope':'All hypothetical nontrivial positive cycles; the local bound also holds on positive orbits avoiding the verified basin.',
         'independent_proof':'Complete compiled progression-index bisection, independent of inverse residues and logarithm tables. Full Python translation comparisons exist for J35 and J38, not necessarily this J.',
         'proof':'../block-restart-capacity.md','audit_source_sha256':sha(ROOT/'src'/'audit_native_family_proofs.py'),
         'source_dependencies':pair['source_dependencies'],
         'dependencies':dict(pair['dependencies'],**{pair_name:sha(R/pair_name)})}
    save(capname,cap)
    lower=[];profiles=[]
    for m in range(96,111):
        upper=(F(14784,10000)*m*DHI**m).__ceil__()
        k,rows=cycle_lower_bound(m,X,method='elementary',capacity_c=c,stop_upper=upper)
        lower.append({'m':m,'minimum':str(X),'K_proved':k,'rows':rows,'capacity_certificate':capname})
        save(f'K-lower-bounds-family-J{J}-native-pair.json',lower)
        if m>106:continue
        low=1;high=128
        if not exploratory(m,high,k,D(c.numerator)/D(c.denominator)):
            print('No explored conditional contradiction',m,flush=True);continue
        while low<high:
            middle=(low+high)//2
            if exploratory(m,middle,k,D(c.numerator)/D(c.denominator)):high=middle
            else:low=middle+1
        row=certificate(m,low*X,k,c);assert row['conditional_contradiction']
        row.update(capacity_certificate=capname,minimum_factor=low,warning='Conditional until the finite global-minimum window is excluded.')
        profiles.append(row);save(f'family-J{J}-native-pair-conditional-certificates.json',profiles)
        print('Uniform capacity',J,'m',m,'initial K',k,'factor',low,'final K',row['final_K'],flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--J',type=int,required=True);p.add_argument('--producer',required=True)
    p.add_argument('--producer-source',required=True);p.add_argument('--progression',required=True)
    a=p.parse_args();main(a.J,a.producer,a.producer_source,a.progression)
