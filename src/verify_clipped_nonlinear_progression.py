"""Python audit of suffix clipping and full trajectory counts on hard samples."""
from pathlib import Path
import hashlib,json,time,argparse
from verify_precise_nonlinear_progression import Checker as Precise,read,sha
from verify_family_capacity import val
from audit_logtable import audit as audit_logs
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71

class Checker(Precise):
    def visit(self,a,mod,count,n,stride,j):
        self.nodes+=1;self.maxdepth=max(self.maxdepth,j)
        assert count>0 and a>0 and mod>0 and n>0 and n&1 and stride>0 and stride%2==0
        assert (n+1)*mod-stride*a>=0
        if n<=X:
            gone=min(count,(X-n)//stride+1);self.basin+=gone;count-=gone
            if not count:return
            a+=gone*mod;n+=gone*stride
        if count==1:self.single(n);return
        def passed(index):
            return self.logbound(n+index*stride+1,True)<=self.limit(a+index*mod,j)
        if passed(0):self.restart+=count;return
        if passed(count-1):
            lo=0;hi=count-1
            while lo<hi:
                mid=(lo+hi)//2
                if passed(mid):hi=mid
                else:lo=mid+1
            assert passed(hi) and hi>=1
            self.restart+=count-hi;count=hi
            if count==1:self.single(n);return
        high=n+stride*(count-1)
        first_difference=n-((a<<self.root_k)-1)
        last_difference=high-(((a+(count-1)*mod)<<self.root_k)-1)
        if max(first_difference,last_difference)<=0:self.restart+=count;return
        assert j<self.depth
        self.odd(a,mod,count,n,stride,j)

def main(label,input_name):
    start=time.monotonic();audit_logs(write=False);logs=read('log2-mantissa-table.json')
    data=read(input_name);native=read(label+'-result.json');meta=read(label+'-metadata.json')
    assert native['height_method']=='exact_rational_mantissa_grid_clipped'
    assert native['map_id']=='plateau-c3799-c4099-h71' and not native['linear_coefficient_certified']
    assert meta['inputHash'].lower()==sha(R/input_name)
    assert meta['sourceHash'].lower()==sha(ROOT/'src'/'ClippedNonlinearProgressionVerifier.cs')
    rows=[]
    for i,case in enumerate(data['classes']):
        k=case['k'];ell=case['ell'];a=int(case['first_a']);mod=int(case['step_a']);count=int(case['count'])
        power=3**k;n=(a*power-1)>>ell;stride=power*(mod>>ell)
        assert (a*power-1)%(1<<ell)==0 and mod%(1<<ell)==0 and val(n+1)==case['s']
        check=Checker(41,k,16,logs);check.visit(a,mod,count,n,stride,1)
        assert check.restart+check.basin+check.singles==count
        row=native['rows'][i];assert row['id']==i and row['status']=='complete'
        for key,value in [('seeds',count),('restart',check.restart),('threshold',check.basin),('singles',check.singles),('nodes',check.nodes),('singleton_steps',check.single_steps)]:
            assert int(row[key])==value,(i,key,int(row[key]),value)
        rows.append({'id':i,'source_class':data['source_classes'][i],'nodes':check.nodes,'singleton_steps':check.single_steps})
        print('Clipped precise Python class',i+1,'/',len(data['classes']),flush=True)
    result={'status':'passed','map_id':native['map_id'],'full_global_input':False,'classes':len(rows),'rows':rows,
            'seconds':time.monotonic()-start,'source_sha256':sha(Path(__file__)),
            'source_dependencies':{name:sha(ROOT/'src'/name) for name in ('verify_family_capacity.py','verify_precise_nonlinear_progression.py','audit_logtable.py','ClippedNonlinearProgressionVerifier.cs')},
            'dependencies':{name:sha(R/name) for name in (input_name,label+'-result.json',label+'-metadata.json','log2-mantissa-table.json')}}
    (R/(label+'-python-comparison.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('PASSED clipped sample;',result['seconds'],'seconds',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--label',required=True);p.add_argument('--input',default='nonlinear-progression-challenge-input.json')
    a=p.parse_args();main(a.label,a.input)
