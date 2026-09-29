"""Independent exact Collatz cycle prefix exclusion search.

Every branch is a residue class of the ORIGINAL n0 in an integer interval.
All rejection predicates use integer/rational arithmetic. The numerical
cycle lower bound is either proved by exact_intervals or explicitly input.
See prefix-method.md for the mathematical proof obligations.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
import time
from functools import lru_cache
from exact_intervals import geom_upper,ceildiv,cycle_lower_bound


class Search:
    def __init__(self,m,low,high,k_bound,depth,node_limit):
        self.m,self.low,self.high,self.k_bound=m,low,high,k_bound
        self.depth,self.node_limit=depth,node_limit
        self.gs=[F(0)]+[geom_upper(j) for j in range(1,m+1)]
        self.counts=Counter()
        self.levels=Counter()
        self.survivors=[]
        self.start=time.perf_counter()
        self.last_print=self.start

    @lru_cache(maxsize=None)
    def target(self,completed,used):
        remaining=self.m-completed
        if remaining<=0:
            return self.low
        h=((self.k_bound-used)/self.gs[remaining]).__floor__()
        return max(self.low,(1<<max(0,h))-1)

    @staticmethod
    def endpoints(lo,hi,r,mod):
        a=lo+(r-lo)%mod
        b=hi-(hi-r)%mod
        return (a,b) if a<=b else None

    def singleton(self,n0,n,completed,used):
        self.counts['singleton']+=1
        trace=[]
        for i in range(completed,self.m+1):
            if n<n0:
                self.counts['singleton_descent']+=1
                return
            if n<self.target(i,used):
                self.counts['singleton_capacity']+=1
                return
            if i==self.m:
                self.survivors.append({'n0':str(n0),'n':str(n),'completed':i,'used':used,'trace':trace})
                return
            k=((n+1)&-(n+1)).bit_length()-1
            peak=3**k*((n+1)>>k)-1
            l=(peak&-peak).bit_length()-1
            trace.append([k,l])
            n=peak>>l
            used+=k

    def dfs(self,P,Q,S,lo,hi,r,completed,used,word):
        self.counts['nodes']+=1
        self.levels[completed]+=1
        if self.counts['nodes']>self.node_limit:
            raise RuntimeError('node_limit')
        now=time.perf_counter()
        if now-self.last_print>15:
            print(json.dumps({'progress':dict(self.counts),'levels':dict(self.levels),
                              'elapsed':now-self.start,'word':word}),flush=True)
            self.last_print=now
        mod=1<<(S+1)
        target=self.target(completed,used)
        lo=max(lo,ceildiv((target<<S)-Q,P))
        # Since n0 is the global cycle minimum, the current minimum is >=n0.
        if P<(1<<S):
            hi=min(hi,Q//((1<<S)-P))
        endpoints=self.endpoints(lo,hi,r,mod)
        if endpoints is None:
            self.counts['interval_empty']+=1
            return
        first,last=endpoints
        if first==last:
            assert (P*first+Q)%(1<<S)==0
            self.singleton(first,(P*first+Q)>>S,completed,used)
            return
        if completed>=self.depth:
            self.survivors.append({'P':str(P),'Q':str(Q),'S':S,'lo':str(first),'hi':str(last),
                                   'r':str(r),'completed':completed,'used':used,'word':word})
            return
        n_hi=(P*last+Q)>>S
        kmax=(n_hi+1).bit_length()-1
        for k in range(1,kmax+1):
            nexttarget=self.target(completed+1,used+k)
            three=3**k
            # Maximum peak after this exact odd-run length.
            peak_hi=(three*(n_hi+1)>>k)-1
            if peak_hi<2*nexttarget:
                self.counts['odd_capacity']+=1
                continue
            sk=S+k
            mk=1<<(sk+1)
            rk=(((1<<S)*((1<<k)-1)-Q)*pow(P,-1,mk))%mk
            if (rk-r)%mod:
                self.counts['odd_residue_incompatible']+=1
                continue
            ep=self.endpoints(first,last,rk,mk)
            if ep is None:
                self.counts['odd_residue_empty']+=1
                continue
            firstk,lastk=ep
            PP=three*P
            QQ=three*Q+(three-(1<<k))*(1<<S)
            peak_hi=(PP*lastk+QQ)>>sk
            lmax=(peak_hi//nexttarget).bit_length()-1
            for l in range(1,lmax+1):
                ss=sk+l
                mm=1<<(ss+1)
                rr=(((1<<ss)-QQ)*pow(PP,-1,mm))%mm
                if (rr-rk)%mk:
                    self.counts['even_residue_incompatible']+=1
                    continue
                self.dfs(PP,QQ,ss,firstk,lastk,rr,completed+1,used+k,word+[[k,l]])

    def run(self):
        status='complete'
        try:
            self.dfs(1,0,0,self.low,self.high,1,0,0,[])
        except RuntimeError as e:
            status=str(e)
        return {'status':status,'excluded':status=='complete' and not self.survivors,
                'm':self.m,'initial_interval':[str(self.low),str(self.high)],
                'K_lower_bound':self.k_bound,'max_branch_depth':self.depth,
                'counts':dict(self.counts),'levels':dict(self.levels),
                'survivors':self.survivors,'elapsed_seconds':time.perf_counter()-self.start}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--m',type=int,default=92)
    parser.add_argument('--factor',type=F,default=F(73,10))
    parser.add_argument('--depth',type=int,default=8)
    parser.add_argument('--node-limit',type=int,default=10000000)
    parser.add_argument('--k',type=int,default=205632218873398596256)
    args=parser.parse_args()
    low=2**71
    high=(args.factor*low).__floor__()
    s=Search(args.m,low,high,args.k,args.depth,args.node_limit)
    result=s.run()
    result['K_bound_status']='Input; requires separate verification certificate.'
    path=Path(__file__).resolve().parents[1]/'results'/f'prefix-m{args.m}-f{str(args.factor).replace("/","_")}-d{args.depth}.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='survivors'}),flush=True)
    print('Survivor branches:',len(result['survivors']),flush=True)


if __name__=='__main__':
    main()
