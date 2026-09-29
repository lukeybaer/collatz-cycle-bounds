"""Independently enclose every lookup-table logarithm using complements.

The producer expands log(1+j/256) directly. This checker instead subtracts
log(512/(256+j)) from log(2), with longer positive rational series.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]

def interval(z):
    power=z;total=F(0)
    for t in range(80):
        total+=2*power/(2*t+1);power*=z*z
    return total,total+2*power/(161*(1-z*z))

def audit(write=True):
    path=ROOT/'results'/'log2-mantissa-table.json'
    data=json.loads(path.read_text())
    assert data['scale']==10**9 and data['grid']==256 and len(data['bounds'])==257
    ln2lo,ln2hi=interval(F(1,3))
    for j,row in enumerate(data['bounds']):
        if j in (0,256):
            assert row['lower']==row['upper']==j*10**9//256
            continue
        otherlo,otherhi=interval(F(256-j,768+j))
        lower=(ln2lo-otherhi)/ln2hi;upper=(ln2hi-otherlo)/ln2lo
        assert F(row['lower'],10**9)<=lower<=upper<=F(row['upper'],10**9)
    result={'status':'passed','entries':257,'method':'complementary logarithm, exact 80-term atanh series',
            'table_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    if write:
        (ROOT/'results'/'log2-mantissa-table-audit.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result),flush=True)
    return result

if __name__=='__main__':audit()
