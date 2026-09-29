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
        self.master_bits=high.bit_length()+3
        self.master_mod=1<<self.master_bits
        self.inverses={}
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
        # Clipping DOWN can only weaken the necessary lower bound.
        return max(self.low,(1<<min(16384,max(0,h)))-1)

    def inverse(self,odd_steps):
        if odd_steps not in self.inverses:
            self.inverses[odd_steps]=pow(3**odd_steps,-1,self.master_mod)
        return self.inverses[odd_steps]

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
        inverse_P=self.inverse(used)
        for k in range(1,kmax+1):
            # All runs of length >=k lie in this continuation cylinder.
            # Once its modulus exceeds the interval width, test its one
            # possible original seed directly and close the entire tail.
            mc=1<<(S+k)
            if mc>last-first:
                rc=(-(1<<S)-Q)*inverse_P%mc
                epc=self.endpoints(first,last,rc,mc)
                if epc is not None and (rc-r)%mod==0:
                    nc=epc[0]
                    assert epc[0]==epc[1]
                    self.singleton(nc,(P*nc+Q)>>S,completed,used)
                self.counts['odd_tail_closed']+=1
                break
            nexttarget=self.target(completed+1,used+k)
            three=3**k
            # Maximum peak after this exact odd-run length.
            peak_hi=(three*(n_hi+1)>>k)-1
            if peak_hi<2*nexttarget:
                self.counts['odd_capacity']+=1
                continue
            sk=S+k
            mk=1<<(sk+1)
            assert mk<=self.master_mod
            rk=(((1<<S)*((1<<k)-1)-Q)*inverse_P)%mk
            if (rk-r)%mod:
                self.counts['odd_residue_incompatible']+=1
                continue
            ep=self.endpoints(first,last,rk,mk)
            if ep is None:
                self.counts['odd_residue_empty']+=1
                continue
            firstk,lastk=ep
            if firstk==lastk:
                self.singleton(firstk,(P*firstk+Q)>>S,completed,used)
                continue
            PP=three*P
            QQ=three*Q+(three-(1<<k))*(1<<S)
            peak_hi=(PP*lastk+QQ)>>sk
            lmax=(peak_hi//nexttarget).bit_length()-1
            inverse_PP=self.inverse(used+k)
            for l in range(1,lmax+1):
                ss=sk+l
                mc=1<<ss
                if mc>lastk-firstk:
                    rc=(-QQ)*inverse_PP%mc
                    epc=self.endpoints(firstk,lastk,rc,mc)
                    if epc is not None and (rc-rk)%mk==0:
                        nc=epc[0]
                        assert epc[0]==epc[1]
                        self.singleton(nc,(P*nc+Q)>>S,completed,used)
                    self.counts['even_tail_closed']+=1
                    break
                mm=1<<(ss+1)
                assert mm<=self.master_mod
                rr=(((1<<ss)-QQ)*inverse_PP)%mm
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
