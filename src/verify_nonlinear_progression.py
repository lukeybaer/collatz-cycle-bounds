"""Python proof for selected nonlinear exceptional classes and target audit."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,time
from verify_family_capacity import Checker as LinearChecker,val

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';D=F(1584962,10**6)
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def phi(y):return max(D*y-F(4099,100),min(D*y-F(3799,100),y+71*(D-1)-F(3799,100)))

class Checker(LinearChecker):
    def limit(self,a,j):
        h=self.root_k+a.bit_length()-1;assert h>=71
        if h not in self.target:
            values=[F(h)]
            for _ in range(self.depth+1):values.append(phi(values[-1]))
            self.target[h]=[value.__floor__() for value in values]
        return self.target[h][j]

def audit_targets():
    limits=read('nonlinear-progression-thresholds.json');assert len(limits)==512
    checked=0
    for h,row in enumerate(limits):
        if h<71:assert row is None;continue
        y=F(h)
        for value in row:
            assert value==y.__floor__();y=phi(y);checked+=1
    return checked

def main(label,take,depth):
    start=time.monotonic();targets=audit_targets();data=read('extended-capacity-J41-classes.json')
    native=read(label+'-result.json');assert native['capacity_kind']=='nonlinear_block_restart' and not native['linear_coefficient_certified']
    assert native['map_id']=='plateau-c3799-c4099-h71'
    cases=data['classes'][:take or None];assert len(native['rows'])>=len(cases)
    rows=[]
    for i,case in enumerate(cases):
        k=case['k'];ell=case['ell'];a=int(case['first_a']);mod=int(case['step_a']);count=int(case['count'])
        power=3**k;n=(a*power-1)>>ell;stride=power*(mod>>ell)
        assert (a*power-1)%(1<<ell)==0 and val(n+1)==case['s']
        check=Checker(41,k,depth);check.visit(a,mod,count,n,stride,1)
        assert check.restart+check.basin+check.singles==count
        row=native['rows'][i];assert row['id']==i and row['status']=='complete'
        for key,value in [('seeds',count),('restart',check.restart),('threshold',check.basin),('singles',check.singles),('nodes',check.nodes),('singleton_steps',check.single_steps)]:
            assert int(row[key])==value,(i,key,int(row[key]),value)
        rows.append({'id':i,'seeds':str(count),'nodes':check.nodes,'singleton_steps':check.single_steps})
        if i%200==0:print('Independent nonlinear Python',i+1,'/',len(cases),flush=True)
    full=len(cases)==len(data['classes'])
    result={'status':'passed','full_input':full,'capacity_kind':'nonlinear_block_restart','linear_coefficient_certified':False,
            'map_id':'plateau-c3799-c4099-h71','classes':len(cases),'exact_thresholds_checked':targets,'rows':rows,
            'seconds':time.monotonic()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'inherited_source_sha256':hashlib.sha256((ROOT/'src'/'verify_family_capacity.py').read_bytes()).hexdigest(),
            'native_source_sha256':hashlib.sha256((ROOT/'src'/'NonlinearProgressionCapacityVerifier.cs').read_bytes()).hexdigest(),
            'input_sha256':hashlib.sha256((R/'extended-capacity-J41-classes.json').read_bytes()).hexdigest(),
            'native_result_sha256':hashlib.sha256((R/(label+'-result.json')).read_bytes()).hexdigest()}
    (R/(label+'-python-comparison.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--label',required=True);p.add_argument('--take',type=int,default=100)
    p.add_argument('--depth',type=int,default=16);a=p.parse_args();main(a.label,a.take,a.depth)
