"""Independent conditional-capacity proof by progression-index bisection.

Crossing the threshold contradicts the hypothesis that every cycle member
exceeds it. It does not prove convergence for all numbers below the threshold.
"""
from pathlib import Path
import argparse, hashlib, json, time
from verify_family_capacity import Checker, val

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

class ConditionalChecker(Checker):
    def __init__(self,J,root_k,depth,cut):
        super().__init__(J,root_k,depth)
        self.cut=cut
    def single(self,n):
        assert n>0 and n&1
        steps=0
        while n>self.cut:
            n=3*n+1;n>>=val(n);steps+=1
            assert steps<1000000 and n.bit_length()<=4096
        self.singles+=1;self.single_steps+=steps
    def visit(self,a,mod,count,n,stride,j):
        self.nodes+=1;self.maxdepth=max(self.maxdepth,j)
        assert count>0 and a>0 and mod>0 and n>0 and n&1 and stride>0 and stride%2==0
        assert (n+1)*mod-stride*a>=0
        if n<=self.cut:
            gone=min(count,(self.cut-n)//stride+1);self.basin+=gone
            count-=gone
            if not count:return
            a+=gone*mod;n+=gone*stride
        if count==1:self.single(n);return
        if n.bit_length()<=self.limit(a,j):self.restart+=count;return
        high=n+stride*(count-1)
        first_difference=n-((a<<self.root_k)-1)
        last_difference=high-(((a+(count-1)*mod)<<self.root_k)-1)
        if max(first_difference,last_difference)<=0:self.restart+=count;return
        assert j<self.depth, ('depth_limit',a,count,j)
        self.odd(a,mod,count,n,stride,j)

def main(J,factor,label,take,depth):
    name=f'conditional-capacity-J{J}-f{factor}-classes.json'
    data=read(name);cpp=read(label+'-result.json')
    source_name=f'extended-capacity-J{J}-classes.json';original=read(source_name)
    cut=factor*X
    assert data['J']==J and int(data['verified_basin'])==X and int(data['assumed_cycle_minimum'])==cut
    assert data['source_classes_sha256']==digest(R/source_name)
    # Independently reconstruct the restriction of every original progression.
    expected=[]
    for index,row in enumerate(original['classes']):
        k=row['k'];a=int(row['first_a']);mod=int(row['step_a']);count=int(row['count'])
        root=(a<<k)-1;spacing=mod<<k
        removed=max(0,min(count,(cut-root)//spacing+1))
        if removed<count:
            item=dict(row);item.update(source_class=index,first_a=str(a+removed*mod),count=str(count-removed))
            expected.append(item)
    assert data['classes']==expected
    assert int(data['seed_count'])==sum(int(row['count']) for row in expected)
    assert cpp['conditional_only'] and int(cpp['assumed_cycle_minimum'])==cut
    cases=data['classes'][:take or None];start=time.monotonic();rows=[]
    assert len(cpp['rows'])>=len(cases)
    for i,case in enumerate(cases):
        k=case['k'];ell=case['ell'];a=int(case['first_a']);mod=int(case['step_a']);count=int(case['count'])
        assert int(case['last_a'])==a+(count-1)*mod and (a<<k)-1>cut
        n=(a*3**k-1)>>ell;stride=3**k*(mod>>ell)
        assert (a*3**k-1)%(1<<ell)==0 and val(n+1)==case['s']
        checker=ConditionalChecker(J,k,depth,cut)
        checker.visit(a,mod,count,n,stride,1)
        assert checker.restart+checker.basin+checker.singles==count
        receipt=cpp['rows'][i]
        assert receipt['id']==i and receipt['status']=='complete'
        rows.append({'id':i,'source_class':case['source_class'],'seeds':str(count),
                     'restart':str(checker.restart),'threshold':str(checker.basin),'singles':str(checker.singles),
                     'nodes':checker.nodes,'singleton_steps':checker.single_steps})
        if i%200==0:print('Independent conditional families',i+1,'/',len(cases),'seconds',round(time.monotonic()-start,1),flush=True)
    complete=len(cases)==len(data['classes'])
    out={'status':'passed','full_input':complete,'conditional_only':True,'J':J,'assumed_cycle_minimum':str(cut),
         'classes':len(cases),'seeds':str(sum(int(row['seeds']) for row in rows)),
         'source_sha256':digest(Path(__file__)),
         'base_checker_sha256':digest(ROOT/'src'/'verify_family_capacity.py'),
         'input_sha256':digest(R/name),'csharp_receipt_sha256':digest(R/(label+'-result.json')),
         'seconds':time.monotonic()-start,'rows':rows}
    suffix='full' if complete else f'first{len(cases)}'
    (R/f'conditional-J{J}-f{factor}-python-{suffix}.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASSED',J,factor,len(cases),'full_input',complete,'seconds',out['seconds'],flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--J',type=int,default=41);p.add_argument('--factor',type=int,default=16)
    p.add_argument('--label',required=True);p.add_argument('--take',type=int,default=0);p.add_argument('--depth',type=int,default=16)
    a=p.parse_args();main(a.J,a.factor,a.label,a.take,a.depth)
