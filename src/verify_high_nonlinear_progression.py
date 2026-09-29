"""Independent exact thresholds and sampled trajectories for higher maps."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,time
from verify_clipped_nonlinear_progression import Checker as Clipped
from verify_precise_nonlinear_progression import read,sha
from verify_family_capacity import val
from audit_logtable import audit as audit_logs
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';D=F(1584962,10**6);SCALE=10**9

def phi(y,J):return max(D*y-F(100*J-1,100),min(D*y-F(3799,100),y+71*(D-1)-F(3799,100)))
class Checker(Clipped):
    def __init__(self,J,k,depth,logs):super().__init__(J,k,depth,logs);self.J=J
    def limit(self,a,j):
        y=self.root_k+self.logbound(a)
        for _ in range(j):y=phi(y,self.J)
        return F((y*SCALE).__floor__(),SCALE)

def main(J,label,take):
    start=time.monotonic();assert 42<=J<=48;audit_logs(write=False);logs=read('log2-mantissa-table.json')
    thresholds=label+'-thresholds.json';values=read(thresholds);assert len(values)==512*256;checked=0
    for slot,row in enumerate(values):
        h,bin=divmod(slot,256)
        if h<71:assert row is None;continue
        y=F(h)+F(logs['bounds'][bin]['lower'],SCALE);assert len(row)==18
        for stored in row:
            assert stored==(y*SCALE).__floor__();y=phi(y,J);checked+=1
    name=f'high-capacity-J{J}-classes.json';data=read(name);native=read(label+'-result.json');meta=read(label+'-metadata.json')
    assert native['map_id']==f'plateau-c3799-c{100*J-1}-h71' and not native['linear_coefficient_certified']
    assert native['J']==data['J']==J and meta['inputHash'].lower()==sha(R/name)
    assert meta['sourceHash'].lower()==sha(ROOT/'src'/'HighNonlinearProgressionVerifier.cs')
    assert meta['logTableHash'].lower()==sha(R/'log2-mantissa-table.json')
    cases=data['classes'][:take];rows=[]
    for i,case in enumerate(cases):
        k=case['k'];ell=case['ell'];a=int(case['first_a']);mod=int(case['step_a']);count=int(case['count'])
        power=3**k;n=(a*power-1)>>ell;stride=power*(mod>>ell)
        assert (a*power-1)%(1<<ell)==0 and mod%(1<<ell)==0 and val(n+1)==case['s']
        check=Checker(J,k,16,logs);check.visit(a,mod,count,n,stride,1)
        assert check.restart+check.basin+check.singles==count
        row=native['rows'][i];assert row['id']==i and row['status']=='complete'
        for key,value in [('seeds',count),('restart',check.restart),('threshold',check.basin),('singles',check.singles),('nodes',check.nodes),('singleton_steps',check.single_steps)]:
            assert int(row[key])==value,(i,key,int(row[key]),value)
        rows.append({'id':i,'nodes':check.nodes,'singleton_steps':check.single_steps})
    result={'status':'passed','J':J,'map_id':native['map_id'],'full_global_input':len(cases)==len(data['classes']),
            'classes':len(cases),'exact_thresholds_checked':checked,'rows':rows,'seconds':time.monotonic()-start,
            'source_sha256':sha(Path(__file__)),
            'source_dependencies':{name:sha(ROOT/'src'/name) for name in ('verify_family_capacity.py','verify_precise_nonlinear_progression.py','verify_clipped_nonlinear_progression.py','audit_logtable.py','HighNonlinearProgressionVerifier.cs')},
            'dependencies':{name:sha(R/name) for name in (name,label+'-result.json',label+'-metadata.json',thresholds,'log2-mantissa-table.json')}}
    (R/(label+'-python-comparison.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('PASSED higher nonlinear sample:',J,len(cases),'classes;',checked,'thresholds;',result['seconds'],'seconds',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--J',type=int,required=True);p.add_argument('--label',required=True);p.add_argument('--take',type=int,default=100)
    a=p.parse_args();main(a.J,a.label,a.take)
