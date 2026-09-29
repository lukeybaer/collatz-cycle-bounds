"""Freeze the audited p-adic capacity and build exact conditional inputs."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
from exact_intervals import cycle_lower_bound,DHI
from affine_profile_certificates import certificate

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';C=F(2999,100);X=2**71
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def save(name,obj):(R/name).write_text(json.dumps(obj,indent=2)+'\n')
deps=['strong-capacity-J30-global.json','strong-capacity-J30-classes.json',
      'strong-capacity-J30-basin-wide-result.json','strong-capacity-J30-basin-reference-result.json',
      'strong-capacity-J30-audit.json','strong-capacity-J30-audit-python.json']
assert read(deps[-1])['all_python_trajectories_verified'] and read(deps[-1])['status']=='passed'
capname='strong-capacity-J30-certificate.json'
save(capname,{'kind':'uniform_padic_and_basin','capacity_certified':True,'capacity_c':str(C),
 'verified_basin':str(X),'global_pairs':7602147,'exceptional_seeds':1929307,
 'proof':'../padic-capacity-program.md','scope':'hypothetical nontrivial positive cycles; all m',
 'analytic_status':'derived and internally audited; external peer review and novelty review pending',
 'external_dependencies':['Bugeaud (2002), Theorem 2','Published verified Collatz basin through 2^71'],
 'dependencies':{name:hashlib.sha256((R/name).read_bytes()).hexdigest() for name in deps}})
lower=[];profiles=[]
for m in range(96,111):
    upper=(F(14784,10000)*m*DHI**m).__ceil__()
    k,rows=cycle_lower_bound(m,X,method='three_block',capacity_c=C,stop_upper=upper)
    row={'m':m,'minimum':str(X),'K_proved':k,'rows':rows,'capacity_certificate':capname}
    lower.append(row);save('K-lower-bounds-strong.json',lower)
    print('Initial bound',m,k,flush=True)
    if m<=102:
        factor={96:15,97:20,98:24,99:29,100:34,101:39,102:44}[m]
        cert=certificate(m,factor*X,k,C)
        cert['capacity_certificate']=capname;cert['minimum_factor']=factor
        cert['warning']='Conditional until the finite minimum window is excluded; analytic dependencies are in the referenced capacity certificate.'
        profiles.append(cert);save('strong-envelope-conditional-certificates.json',profiles)
        print('Final conditional',m,factor,cert['conditional_contradiction'],cert['final_K'],flush=True)
