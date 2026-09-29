"""Independent family verification using parity bisection of progressions.

Unlike the C# producer, no modular inverses or affine numerator/denominator
states are used. State is n(t)=n0+stride*t, a(t)=a0+modulus*t. Unknown
valuations are resolved by partitioning t into its even and odd indices.
"""
from pathlib import Path
from fractions import Fraction as F
import json,argparse,time,hashlib
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
def val(n):
    assert n>0
    return (n&-n).bit_length()-1
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
class Checker:
    def __init__(self,J,root_k,depth,logs=None):
        self.c=F(100*J-1,100);self.root_k=root_k;self.depth=depth
        self.restart=self.basin=self.singles=self.nodes=self.single_steps=self.maxdepth=0
        self.target={}
        self.logs=logs
    def logbound(self,n,upper=False):
        e=n.bit_length()-1;index=((n-(1<<e))*256)>>e
        return F(e)+F(self.logs['bounds'][index+int(upper)]['upper' if upper else 'lower'],self.logs['scale'])
    def limit(self,a,j):
        if self.logs:
            y=self.root_k+self.logbound(a)
            for _ in range(j):y=F(1584962,10**6)*y-self.c
            return y
        h=self.root_k+a.bit_length()-1
        assert h>=71
        if h not in self.target:
            values=[F(h)]
            for _ in range(self.depth+1):values.append(F(1584962,10**6)*values[-1]-self.c)
            self.target[h]=[x.__floor__() for x in values]
        return self.target[h][j]
    def single(self,n):
        assert n>0 and n&1
        steps=0
        while n>X:
            n=3*n+1;n>>=val(n);steps+=1
            assert steps<1000000 and n.bit_length()<=4096
        self.singles+=1;self.single_steps+=steps
    def visit(self,a,mod,count,n,stride,j):
        self.nodes+=1;self.maxdepth=max(self.maxdepth,j)
        assert count>0 and a>0 and mod>0 and n>0 and n&1 and stride>0 and stride%2==0
        assert (n+1)*mod-stride*a>=0
        high=n+stride*(count-1)
        if n<=X:
            gone=min(count,(X-n)//stride+1);self.basin+=gone
            count-=gone
            if not count:return
            a+=gone*mod;n+=gone*stride
        if count==1:self.single(n);return
        height=self.logbound(n+1,True) if self.logs else n.bit_length()
        if height<=self.limit(a,j):self.restart+=count;return
        # Descent comparison uses endpoint differences, not a P/Q formula.
        first_difference=n-((a<<self.root_k)-1)
        last_difference=high-(((a+(count-1)*mod)<<self.root_k)-1)
        if max(first_difference,last_difference)<=0:self.restart+=count;return
        assert j<self.depth, ('depth_limit',a,count,j)
        self.odd(a,mod,count,n,stride,j)
    def odd(self,a,mod,count,n,stride,j):
        if count==1:self.single(n);return
        k=val(n+1)
        if k>=val(stride):
            self.odd(a,2*mod,(count+1)//2,n,2*stride,j)
            if count//2:self.odd(a+mod,2*mod,count//2,n+stride,2*stride,j)
            return
        assert k<=self.limit(a,j), ('intermediate_odd_run',a,k,j)
        peak=((n+1)>>k)*3**k-1;newstride=(stride>>k)*3**k
        self.even(a,mod,count,peak,newstride,j,n,stride)
    def even(self,a,mod,count,peak,stride,j,oldn,oldstride):
        if count==1:self.single(oldn);return
        ell=val(peak)
        if ell>=val(stride):
            self.even(a,2*mod,(count+1)//2,peak,2*stride,j,oldn,2*oldstride)
            if count//2:self.even(a+mod,2*mod,count//2,peak+stride,2*stride,j,oldn+oldstride,2*oldstride)
            return
        self.visit(a,mod,count,peak>>ell,stride>>ell,j+1)
def main(J,take,depth,label,precise):
    name=f'extended-capacity-J{J}-classes.json';data=read(name);cpp=read(label+'-result.json')
    assert data['J']==J and int(data['verified_basin'])==X
    cases=data['classes'][:take or None];start=time.monotonic();rows=[];logs=None
    if precise:
        logs=read('log2-mantissa-table.json');assert logs['scale']==10**9 and logs['grid']==256 and len(logs['bounds'])==257
        def interval(z):
            p=z;v=F(0)
            for t in range(80):v+=2*p/(2*t+1);p*=z*z
            return v,v+2*p/((2*80+1)*(1-z*z))
        ln2lo,ln2hi=interval(F(1,3))
        for j,row in enumerate(logs['bounds']):
            if j in (0,256):assert row['lower']==row['upper']==j*10**9//256;continue
            # Complementary logarithm: log(x)=log(2)-log(2/x).
            otherlo,otherhi=interval(F(256-j,768+j))
            lower=(ln2lo-otherhi)/ln2hi;upper=(ln2hi-otherlo)/ln2lo
            assert F(row['lower'],10**9)<=lower<=upper<=F(row['upper'],10**9)
        print('Independent logarithm table audit passed',flush=True)
    assert len(cpp['rows'])>=len(cases)
    for i,case in enumerate(cases):
        k=case['k'];ell=case['ell'];a=int(case['first_a']);mod=int(case['step_a']);count=int(case['count'])
        assert int(case['last_a'])==a+(count-1)*mod and (a<<k)-1>X
        n=(a*3**k-1)>>ell;stride=3**k*(mod>>ell)
        assert (a*3**k-1)%(1<<ell)==0 and val(n+1)==case['s']
        checker=Checker(J,k,depth,logs);checker.visit(a,mod,count,n,stride,1)
        assert checker.restart+checker.basin+checker.singles==count
        receipt=cpp['rows'][i]
        assert receipt['id']==i and receipt['status']=='complete'
        # Parity bisection can isolate a singleton before the inverse-based
        # producer finishes its known block. Each method proves that seed
        # independently, so path lengths and leaf categories need not match.
        matches=(checker.restart,checker.basin,checker.singles)==tuple(int(receipt[x]) for x in ('restart_seeds','basin_seeds','singleton_seeds'))
        rows.append({'id':i,'seeds':str(count),'restart':str(checker.restart),'basin':str(checker.basin),'singles':str(checker.singles),'nodes':checker.nodes,'singleton_steps':checker.single_steps,'same_leaf_counts':matches})
        if i%200==0:print('Independent families',i+1,'/',len(cases),'seconds',round(time.monotonic()-start,1),flush=True)
    complete=len(cases)==len(data['classes'])
    out={'status':'passed','full_input':complete,'J':J,'classes':len(cases),'seeds':str(sum(int(row['seeds']) for row in rows)),
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'input_sha256':hashlib.sha256((R/name).read_bytes()).hexdigest(),
         'csharp_receipt_sha256':hashlib.sha256((R/(label+'-result.json')).read_bytes()).hexdigest(),
         'seconds':time.monotonic()-start,'rows':rows}
    suffix=('precise-' if precise else '')+('full' if complete else f'first{len(cases)}')
    (R/f'family-J{J}-python-{suffix}.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASSED',J,len(cases),'full_input',complete,'seconds',out['seconds'],flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--J',type=int,default=31);p.add_argument('--take',type=int,default=0);p.add_argument('--depth',type=int,default=16);p.add_argument('--label');p.add_argument('--precise',action='store_true');a=p.parse_args()
    main(a.J,a.take,a.depth,a.label or f'family-J{a.J}-full',a.precise)
