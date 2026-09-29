"""Extend the existing elementary J35 lower bounds without changing old data."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
from exact_intervals import cycle_lower_bound
import verify_certificates as v
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
NAME='family-J35-elementary-lower-bounds-extension.json'
CAP='family-capacity-J35-certificate.json'

def main():
    _,capacity=v.verify_capacity(CAP);assert capacity==F(3499,100)
    rows=[]
    for m in range(101,106):
        k,proof=cycle_lower_bound(m,2**71,method='elementary',capacity_c=capacity)
        assert v.verify_suffix(proof,m,2**71,capacity_c=capacity)==k
        rows.append({'m':m,'minimum':str(2**71),'K_proved':k,'rows':proof,'capacity_certificate':CAP})
        print('PASSED elementary initial bound',m,k,flush=True)
    path=R/NAME;assert not path.exists(),'Do not overwrite an existing extension.'
    path.write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    receipt={'status':'passed','m_range':[101,105],
             'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'result_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
             'capacity_certificate_sha256':hashlib.sha256((R/CAP).read_bytes()).hexdigest(),
             'scope':'Independent forward verification of elementary suffix bounds. No finite minimum-window exclusion.'}
    (R/NAME.replace('.json','-audit.json')).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
