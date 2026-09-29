"""Independent Fraction thresholds and sampled Python progression proofs."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,time
from verify_family_capacity import Checker as Base,val
from audit_logtable import audit as audit_logs
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';SCALE=10**9;D=F(1584962,10**6)

def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def phi(y):return max(D*y-F(4099,100),min(D*y-F(3799,100),y+71*(D-1)-F(3799,100)))

class Checker(Base):
    def limit(self,a,j):
        y=self.root_k+self.logbound(a)
        for _ in range(j):y=phi(y)
        return F((y*SCALE).__floor__(),SCALE)

def main(label,input_name,take,thresholds):
    start=time.monotonic();logs=read('log2-mantissa-table.json');audit_logs(write=False)
    checked=0
    if thresholds:
        values=read(thresholds);assert len(values)==512*256
        for slot,row in enumerate(values):
            h,bin=divmod(slot,256)
            if h<71:assert row is None;continue
            y=F(h)+F(logs['bounds'][bin]['lower'],SCALE)
            assert len(row)==18
            for stored in row:
                assert stored==(y*SCALE).__floor__(),(slot,checked)
                y=phi(y);checked+=1
            if slot%8192==0:print('Exact precise nonlinear thresholds',checked,flush=True)
    data=read(input_name);native=read(label+'-result.json');meta=read(label+'-metadata.json')
    assert native['height_method']=='exact_rational_mantissa_grid'
    assert native['map_id']=='plateau-c3799-c4099-h71' and not native['linear_coefficient_certified']
    cases=data['classes'][:take or None];rows=[]
    assert meta['inputHash'].lower()==sha(R/input_name)
    assert meta['sourceHash'].lower()==sha(ROOT/'src'/'PreciseNonlinearProgressionVerifier.cs')
    assert meta['logTableHash'].lower()==sha(R/'log2-mantissa-table.json')
    for i,case in enumerate(cases):
        k=case['k'];ell=case['ell'];a=int(case['first_a']);mod=int(case['step_a']);count=int(case['count'])
        assert int(case['last_a'])==a+(count-1)*mod
        power=3**k;assert (a*power-1)%(1<<ell)==0 and mod%(1<<ell)==0
        n=(a*power-1)>>ell;stride=power*(mod>>ell);assert val(n+1)==case['s']
        checker=Checker(41,k,16,logs);checker.visit(a,mod,count,n,stride,1)
        assert checker.restart+checker.basin+checker.singles==count
        row=native['rows'][i];assert row['id']==i and row['status']=='complete'
        for key,value in [('seeds',count),('restart',checker.restart),('threshold',checker.basin),
                          ('singles',checker.singles),('nodes',checker.nodes),('singleton_steps',checker.single_steps)]:
            assert int(row[key])==value,(i,key,int(row[key]),value)
        rows.append({'id':i,'source_class':data.get('source_classes',list(range(len(data['classes']))))[i],
                     'nodes':checker.nodes,'singleton_steps':checker.single_steps})
        if i%20==0:print('Precise nonlinear Python classes',i+1,'/',len(cases),flush=True)
    result={'status':'passed','map_id':native['map_id'],'full_global_input':input_name=='extended-capacity-J41-classes.json' and len(cases)==len(data['classes']),
            'classes':len(cases),'exact_thresholds_checked':checked,'rows':rows,'seconds':time.monotonic()-start,
            'source_sha256':sha(Path(__file__)),'source_dependencies':{name:sha(ROOT/'src'/name) for name in
                ('verify_family_capacity.py','audit_logtable.py','PreciseNonlinearProgressionVerifier.cs')},
            'dependencies':{name:sha(R/name) for name in [input_name,label+'-result.json',label+'-metadata.json','log2-mantissa-table.json']+([thresholds] if thresholds else [])}}
    (R/(label+'-python-comparison.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('PASSED',len(cases),'classes;',checked,'thresholds; seconds',result['seconds'],flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--label',required=True);p.add_argument('--input',default='extended-capacity-J41-classes.json')
    p.add_argument('--take',type=int,default=100);p.add_argument('--thresholds');a=p.parse_args();main(a.label,a.input,a.take,a.thresholds)
