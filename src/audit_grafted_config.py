"""Independently audit nonlinear prefix/suffix targets with finer rounding."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
import verify_certificates as v
from verify_grafted_capacity import verify as verify_map
from audit_grafted_capacity import MAP
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71;DEN=10**40

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def upper_sum(y,length):
    total=F(0)
    for _ in range(length):
        total+=y
        exact=max(v.DHI*y-F(4099,100),min(v.DHI*y-F(3799,100),y+71*(v.DHI-1)-F(3799,100)))
        exact=min(exact,(v.DHI-F(1,5000))*y+F(28597,2500))
        y=F((exact*DEN).__ceil__(),DEN)
    return total

def exp_lower(y):
    whole=y.__floor__();den=10**160
    ln2=F((v.ln2lo*den).__floor__(),den);z=(y-whole)*ln2
    term=total=F(1)
    for j in range(1,65):
        term=F((term*z*den/j).__floor__(),den);total+=term
    return 2**whole*total

def audit(name):
    path=R/name;cfg=json.loads(path.read_text());m=cfg['m'];k=int(cfg['K'])
    low=int(cfg['low']);high=int(cfg['high'])
    assert 96<=m<=110 and X<=low<=high and low%2==0
    assert cfg['capacity_method']=='analytic_graft' and cfg['capacity_map_id']==MAP
    assert F(cfg['lower_factor'])*X==low and (F(cfg['upper_factor'])*X).__floor__()==high
    assert int(cfg['verified_basin'])==X and 1<=cfg['depth']<=m
    if cfg['capacity_map_proved']:
        verify_map(cfg['capacity_certificate'])
        assert cfg['capacity_certificate_sha256']==sha(R/cfg['capacity_certificate'])
    else:
        assert cfg['capacity_certificate'] is None and cfg['capacity_certificate_sha256'] is None
    bounds=v.read(cfg['initial_K_certificate']);initial=[r for r in bounds if r['m']==m]
    assert len(initial)==1 and int(initial[0]['minimum'])==X
    _,c=v.verify_capacity(initial[0]['capacity_certificate'])
    proved=v.verify_suffix(initial[0]['rows'],m,X,capacity_c=c)
    assert proved==initial[0]['K_proved'] and k<=proved
    b=(high if high%2 else high-1).bit_length();assert cfg['start_log2_upper']==b
    names=('prefix_odd_upper','height_lower_rationals','height_floors','targets','height_proof_kinds')
    assert all(len(cfg[key])==m+1 for key in names)
    suffixes=0
    for i in range(m+1):
        used=int(cfg['prefix_odd_upper'][i]);assert used>=upper_sum(F(b),i).__ceil__()
        y=F(cfg['height_lower_rationals'][i]);threshold=int(cfg['targets'][i]);kind=cfg['height_proof_kinds'][i]
        assert 71<=y<=4096 and y.__floor__()==cfg['height_floors'][i]
        assert threshold>=low
        if kind=='minimum':assert threshold==low
        else:
            assert kind=='suffix_capacity' and i<m
            assert upper_sum(y,m-i)<=k-used
            assert threshold<=max(low,exp_lower(y).__ceil__()-1)
            suffixes+=1
    receipt={'status':'passed' if cfg['capacity_map_proved'] else 'arithmetic_passed_under_unproved_map',
             'm':m,'capacity_map_proved':cfg['capacity_map_proved'],'configuration':name,
             'suffix_targets_checked':suffixes,'rounding_denominator':str(DEN),
             'configuration_sha256':sha(path),'source_sha256':sha(Path(__file__)),
             'initial_K_certificate_sha256':sha(R/cfg['initial_K_certificate']),
             'verification_source_sha256':sha(ROOT/'src'/'verify_certificates.py'),
             'warning':'This verifies necessary targets, not a completed finite search or final cycle contradiction.'}
    (R/(path.stem+'-audit.json')).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt),flush=True)
    return receipt

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('config');a=p.parse_args();audit(a.config)
