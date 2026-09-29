"""Compare every class and proof counter against the original BigInteger producer."""
from pathlib import Path
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def main(original,fast):
    old=read(original+'-result.json');new=read(fast+'-result.json')
    om=read(original+'-metadata.json');nm=read(fast+'-metadata.json')
    assert om['inputHash']==nm['inputHash']
    assert old['status']==new['status']=='complete' and old['full_input'] and new['full_input']
    assert old['capacity_exceptions_discharged'] and new['capacity_exceptions_discharged']
    for key in ('J','classes','seeds','restart_seeds','basin_seeds','singleton_seeds','nodes','singleton_steps','max_depth','rows'):
        assert old[key]==new[key],key
    sha=lambda name:hashlib.sha256((R/name).read_bytes()).hexdigest()
    result={'status':'passed','original':original,'fast':fast,'classes':old['classes'],
            'comparison':'Every per-class proof count, singleton-step count, node count, restart depth and status are identical.',
            'dependencies':{label+suffix:sha(label+suffix) for label in (original,fast) for suffix in ('-result.json','-metadata.json')}}
    (R/(fast+'-original-comparison.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('PASSED',old['classes'],'full arbitrary-precision reference classes',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--original',required=True);p.add_argument('--fast',required=True);a=p.parse_args();main(a.original,a.fast)
