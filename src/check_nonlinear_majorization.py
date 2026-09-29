"""Exact finite challenges to the general growth-map majorization lemma.

These exhaustive rational examples do not replace the written proof. Models
include convex, concave, and neither-convex-nor-concave continuous maps.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib,json,random,time

ROOT=Path(__file__).resolve().parents[1]

class Map:
    def __init__(self,name,pieces):
        self.name=name;self.pieces=pieces;self.b=F(1)
        left=self.b
        for i,(end,slope,offset) in enumerate(pieces):
            assert slope>0 and slope*left+offset>=left
            if end is not None:
                assert end>left and slope*end+offset>=end
                _,next_slope,next_offset=pieces[i+1]
                assert slope*end+offset==next_slope*end+next_offset
                left=end
            else:assert slope>=1
    def phi(self,x):
        assert x>=self.b
        for end,slope,offset in self.pieces:
            if end is None or x<=end:return slope*x+offset
        raise AssertionError
    def psi(self,y):
        assert y>=self.b
        if y<=self.phi(self.b):return self.b
        for end,slope,offset in self.pieces:
            if end is None or y<=slope*end+offset:return (y-offset)/slope
        raise AssertionError
    def extremal(self,m,total):
        def vector(t):
            out=[t]
            for _ in range(m-1):out.append(self.psi(out[-1]))
            return out[::-1]
        maximum=total-(m-1)*self.b
        boundaries={self.b,maximum}
        seeds=[self.b]+[end for end,_,_ in self.pieces if end is not None]
        for point in seeds:
            for _ in range(m):
                point=self.phi(point)
                if self.b<=point<=maximum:boundaries.add(point)
        knots=sorted(boundaries)
        if len(knots)==1:return vector(knots[0])
        for left,right in zip(knots,knots[1:]):
            sl=sum(vector(left));sr=sum(vector(right))
            if sl<=total<=sr:
                t=left+(right-left)*(total-sl)/(sr-sl)
                result=vector(t)
                assert sum(result)==total
                assert all(result[(i+1)%m]<=self.phi(result[i]) for i in range(m))
                return result
        raise AssertionError((self.name,m,total))

MODELS=[
 Map('affine',[(None,F(3,2),F(1,3))]),
 Map('convex',[(F(4),F(3,2),F(0)),(None,F(2),F(-2))]),
 Map('concave',[(F(4),F(2),F(0)),(None,F(1),F(4))]),
 Map('neither',[(F(4),F(2),F(0)),(F(8),F(1,2),F(6)),(None,F(5,4),F(0))]),
]

def main():
    start=time.monotonic();rows=[];rng=random.Random(310299)
    for model in MODELS:
        checked=0;envelopes=0
        for m in range(2,8):
            extrema={total:model.extremal(m,F(total)) for total in range(m,14*m+1)}
            feasible=[]
            for u in combinations_with_replacement(range(1,15),m):
                if any(u[i+1]>model.phi(F(u[i])) for i in range(m-1)):continue
                w=extrema[sum(u)];su=F(0);sw=F(0)
                for left,right in zip(u,w):
                    su+=left;sw+=right;assert su>=sw,(model.name,u,w)
                assert su==sw
                checked+=1
                if len(feasible)<200 or rng.randrange(50)==0:feasible.append(u)
            for _ in range(100):
                y=list(map(F,rng.choice(feasible)))
                # Increasing cyclic order is feasible, as is any rotation.
                shift=rng.randrange(m);y=y[shift:]+y[:shift]
                k=[F(rng.randint(1,int(value))) for value in y]
                z=[]
                for i in range(m):
                    terms=[]
                    for t in range(m):
                        term=k[(i+t)%m]
                        for _ in range(t):term=model.psi(term)
                        terms.append(term)
                    z.append(max(terms))
                assert all(k[i]<=z[i]<=y[i] for i in range(m))
                assert all(z[i]==max(k[i],model.psi(z[(i+1)%m])) for i in range(m))
                assert all(z[(i+1)%m]<=model.phi(z[i]) for i in range(m))
                wanted=sum(k);ordered=sorted(z);cap=None
                for i,value in enumerate(ordered):
                    candidate=(wanted-sum(ordered[:i]))/(m-i)
                    if (i==0 or candidate>=ordered[i-1]) and candidate<=value:
                        cap=candidate;break
                assert cap is not None and cap>=1
                capped=[min(value,cap) for value in z]
                assert sum(capped)==wanted
                assert all(capped[(i+1)%m]<=model.phi(capped[i]) for i in range(m))
                envelopes+=1
        rows.append({'map':model.name,'sorted_vectors':checked,'envelope_and_capping_checks':envelopes})
        print(rows[-1],flush=True)
    result={'status':'passed','exact_arithmetic':'fractions.Fraction','maximum_dimension':7,'coordinate_grid':'integers 1..14',
            'models':rows,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'seconds':time.monotonic()-start,'warning':'Finite challenges to a written general proof, not proof by testing or a certified Collatz growth map.'}
    (ROOT/'results'/'nonlinear-majorization-check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
