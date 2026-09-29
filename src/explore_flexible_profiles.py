"""Rank unproved maps; exact reconstructed proposals do not certify capacity."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib,time
import explore_nonlinear_profiles as approximate
import nonlinear_profile_certificates as exact
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'

def main(c0,J):
    started=time.monotonic();c1=100*J-1
    assert 3799<=c0<=4153 and c0<c1 and 41<=J<=48
    name=f'plateau-c{c0}-c{c1}-h71'
    for module,convert,delta in ((approximate,lambda n:approximate.D(n)/100,approximate.DELTA),
                                (exact,lambda n:F(n,100),exact.DHI)):
        module.C0=convert(c0);module.C1=convert(c1)
        module.OFFSET=71*(delta-1)-module.C0
        module.TURN=71+(module.C1-module.C0)/(delta-1)
        module.LOW_IMAGE=71+module.OFFSET;module.HIGH_IMAGE=module.TURN+module.OFFSET
    exact.MAP=name
    assert exact.OFFSET>0
    initial={r['m']:r['K_proved'] for r in json.loads((R/'K-lower-bounds-family-J38.json').read_text())}
    rows=[]
    output=R/f'experimental-profiles-{name}.json';assert not output.exists()
    for m in range(96,106):
        lo=1;hi=128
        assert approximate.iterate(m,hi,initial[m])[0]
        while lo<hi:
            middle=(lo+hi)//2
            if approximate.iterate(m,middle,initial[m])[0]:hi=middle
            else:lo=middle+1
        record=exact.certificate(m,lo*2**71,initial[m]);assert record['conditional_contradiction']
        record['minimum_factor']=lo;rows.append(record)
        output.write_text(json.dumps({'status':'unproved_map_proposals','capacity_map_proved':False,
          'map_id':name,'parameters':{'c0':str(F(c0,100)),'c1':str(F(c1,100)),'h':71},'rows':rows,
          'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'source_dependencies':{p:hashlib.sha256((ROOT/'src'/p).read_bytes()).hexdigest() for p in
             ('explore_nonlinear_profiles.py','nonlinear_profile_certificates.py','exact_intervals.py','affine_profile_certificates.py')},
          'seconds':time.monotonic()-started,
          'warning':'Exact arithmetic proposals under an unproved capacity map; no cycle exclusions follow without the capacity and minimum-window proofs.'},indent=2)+'\n')
        print(name,'m',m,'factor',lo,'exact proposal only',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--c0',type=int,required=True);p.add_argument('--J',type=int,required=True)
    a=p.parse_args();main(a.c0,a.J)
