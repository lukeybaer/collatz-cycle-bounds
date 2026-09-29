"""Compare compiled parity-bisection proof with every independent Python row."""
from pathlib import Path
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main(J,label,conditional_factor=None):
    pyname=f'family-J{J}-python-full.json' if conditional_factor is None else f'conditional-J{J}-f{conditional_factor}-python-full.json'
    py=read(pyname);native=read(label+'-result.json');meta=read(label+'-metadata.json')
    assert py['status']=='passed' and py['full_input']
    assert native['status']=='complete' and native['full_input'] and native['capacity_exceptions_discharged']
    assert py['classes']==native['classes'] and py['seeds']==native['seeds']
    assert py['input_sha256'].upper()==meta['inputHash']
    assert meta['sourceHash']==sha(ROOT/'src'/'ProgressionCapacityVerifier.cs').upper()
    assert native['conditional_only']==(conditional_factor is not None)
    for p,n in zip(py['rows'],native['rows']):
        assert n['status']=='complete'
        for key in ('id','seeds','restart','singles','nodes','singleton_steps'):
            assert p[key]==n[key],(p['id'],key,p[key],n[key])
        assert p['basin' if conditional_factor is None else 'threshold']==n['threshold']
    out={'status':'passed','J':J,'classes':py['classes'],'seeds':py['seeds'],
         'comparison':'Every class: seed count, restart, threshold, singleton, node, and exact singleton-step counts.',
         'dependencies':{name:sha(R/name) for name in (pyname,label+'-result.json',label+'-metadata.json')},
         'source_sha256':sha(ROOT/'src'/'ProgressionCapacityVerifier.cs')}
    (R/(label+'-python-comparison.json')).write_text(json.dumps(out,indent=2)+'\n')
    print('PASSED',J,py['classes'],'complete Python rows',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--J',type=int,required=True);p.add_argument('--label',required=True);p.add_argument('--conditional-factor',type=int)
    a=p.parse_args();main(a.J,a.label,a.conditional_factor)
