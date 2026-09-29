using System;
using System.Numerics;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
using System.IO;

namespace CollatzWide {
public readonly struct State {
    public readonly UInt128 P,Q,Lo,Hi,R;
    public readonly int S,Completed,Used;
    public State(UInt128 p,UInt128 q,int s,UInt128 lo,UInt128 hi,UInt128 r,int c,int u) {
        P=p;Q=q;S=s;Lo=lo;Hi=hi;R=r;Completed=c;Used=u;
    }
}
public sealed class Data {
    public readonly UInt128 Low,High,Master,Mask;
    public readonly int M,Depth,Bits;
    public readonly UInt128[] Target,Inverse,Three;
    public readonly bool[] Huge;
    public readonly BigInteger[] TargetBig,ThreeBig;
    public Data(int m,string low,string high,string[] targets,int depth) {
        M=m;Low=UInt128.Parse(low);High=UInt128.Parse(high);Depth=depth;
        Bits=Kernel.BitLength(High)+3;
        if(Bits>80 || Low==0 || Low>High)throw new Exception("fixed-width input outside proved range");
        Master=UInt128.One<<Bits;Mask=Master-1;
        TargetBig=Array.ConvertAll(targets,BigInteger.Parse);
        if(TargetBig.Length!=m+1)throw new Exception("target length");
        Target=new UInt128[m+1];Huge=new bool[m+1];
        for(int i=0;i<=m;i++) {
            if(TargetBig[i]<=0)throw new Exception("nonpositive target");
            Huge[i]=TargetBig[i]>(BigInteger)UInt128.MaxValue;
            if(!Huge[i])Target[i]=(UInt128)TargetBig[i];
        }
        Three=new UInt128[81];Inverse=new UInt128[Bits+1];
        Three[0]=1;Inverse[0]=1;UInt128 inv3=1;
        for(int b=1;b<Bits;b*=2)inv3=unchecked(inv3*(2-3*inv3))&Mask;
        if((unchecked(3*inv3)&Mask)!=1)throw new Exception("inverse verification");
        for(int i=1;i<Three.Length;i++)Three[i]=checked(Three[i-1]*3);
        for(int i=1;i<=Bits;i++)Inverse[i]=unchecked(Inverse[i-1]*inv3)&Mask;
        ThreeBig=new BigInteger[1025];ThreeBig[0]=1;
        for(int i=1;i<ThreeBig.Length;i++)ThreeBig[i]=ThreeBig[i-1]*3;
    }
}
public sealed class Kernel {
    readonly Data d;readonly long limit;
    public long Nodes,Singletons,Descent,Capacity,Empty,Survivors,OddTail,EvenTail;
    public long BigFallbacks;
    public long[] Levels;
    public HashSet<BigInteger> Seeds=new HashSet<BigInteger>();
    public List<State> Jobs;public int Split=-1;
    public Kernel(Data data,long nodeLimit){d=data;limit=nodeLimit;Levels=new long[d.M+1];}
    public static int BitLength(UInt128 n) {
        ulong hi=(ulong)(n>>64);
        return hi!=0?128-BitOperations.LeadingZeroCount(hi):64-BitOperations.LeadingZeroCount((ulong)n);
    }
    static int Val2(BigInteger n){return (int)(n&-n).GetBitLength()-1;}
    static int Val2(UInt128 n) {
        ulong low=(ulong)n;
        return low!=0?BitOperations.TrailingZeroCount(low):64+BitOperations.TrailingZeroCount((ulong)(n>>64));
    }
    static bool Endpoints(UInt128 lo,UInt128 hi,UInt128 r,UInt128 mod,out UInt128 first,out UInt128 last) {
        first=last=0;if(lo>hi)return false;
        UInt128 mask=mod-1;
        first=checked(lo+(unchecked(r-lo)&mask));
        UInt128 distance=unchecked(hi-r)&mask;
        if(distance>hi)return false;
        last=hi-distance;return first<=last;
    }
    static UInt128 Min(UInt128 a,UInt128 b){return a<b?a:b;}
    public static State Root(Data d){return new State(1,0,0,d.Low,d.High,1,0,0);}
    void Record(UInt128 first,UInt128 last,UInt128 mod) {
        Survivors++;
        if(d.High-d.Low<=1024)for(var n=first;n<=last;n+=mod)Seeds.Add((BigInteger)n);
    }
    void Single(UInt128 original,UInt128 current,int completed,int used) {
        Singletons++;UInt128 n=current;
        for(int i=completed;i<=d.M;i++) {
            if(n<original){Descent++;return;}
            if(d.Huge[i] || n<d.Target[i]){Capacity++;return;}
            if(i==d.M){Record(original,original,1);return;}
            if(n==UInt128.MaxValue){SingleBig(original,n,i);return;}
            UInt128 plus=n+1;int k=Val2(plus);
            if(k>=d.Three.Length){SingleBig(original,n,i);return;}
            UInt128 factor=plus>>k,three=d.Three[k];
            int productBits=BitLength(factor)+BitLength(three);
            if(productBits>129 || (productBits==129 && factor>UInt128.MaxValue/three)) {
                SingleBig(original,n,i);return;
            }
            UInt128 peak=checked(three*factor)-1;
            n=peak>>Val2(peak);
        }
    }
    public void TestSingleton(string original,string current){Single(UInt128.Parse(original),UInt128.Parse(current),0,0);}
    void SingleBig(UInt128 original,UInt128 current,int completed) {
        BigFallbacks++;
        BigInteger n0=(BigInteger)original,n=(BigInteger)current;
        for(int i=completed;i<=d.M;i++) {
            if(n<n0){Descent++;return;}
            if(n<d.TargetBig[i]){Capacity++;return;}
            if(i==d.M){Record(original,original,1);return;}
            int k=Val2(n+1);
            BigInteger three=k<d.ThreeBig.Length?d.ThreeBig[k]:BigInteger.Pow(3,k);
            var peak=three*((n+1)>>k)-1;
            n=peak>>Val2(peak);
        }
    }
    public void Visit(State v) {
        Nodes++;Levels[v.Completed]++;if(Nodes>limit)throw new Exception("node_limit");
        UInt128 P=v.P,Q=v.Q,lo=v.Lo,hi=v.Hi,r=v.R;
        int S=v.S,c=v.Completed,used=v.Used;
        UInt128 den=UInt128.One<<S,mod=den<<1;
        if(P<den)hi=Min(hi,Q/(den-P));
        if(!Endpoints(lo,hi,r,mod,out var first,out var last)){Empty++;return;}
        if(d.Huge[c]){Empty++;return;}
        UInt128 nhi=Arithmetic.MulAddShift(P,last,Q,S);
        if(nhi<d.Target[c]){Empty++;return;}
        UInt128 nlo=Arithmetic.MulAddShift(P,first,Q,S);
        if(nlo<d.Target[c]) {
            BigInteger numerator=((BigInteger)d.Target[c]<<S)-(BigInteger)Q;
            UInt128 cut=checked((UInt128)((numerator+(BigInteger)P-1)/(BigInteger)P));
            if(cut>lo)lo=cut;
            if(!Endpoints(lo,hi,r,mod,out first,out last)){Empty++;return;}
            nlo=Arithmetic.MulAddShift(P,first,Q,S);
        }
        if(first==last){Single(first,nlo,c,used);return;}
        if(c>=d.Depth){Record(first,last,mod);return;}
        if(c==Split){Jobs.Add(new State(P,Q,S,first,last,r,c,used));return;}
        int kmax=BitLength(checked(nhi+1))-1;
        UInt128 ip=d.Inverse[used];
        for(int k=1;k<=kmax;k++) {
            if(S+k>=128)throw new Exception("shift range");
            UInt128 mc=UInt128.One<<(S+k);
            if(mc>last-first) {
                UInt128 rc=unchecked((0-den-Q)*ip)&(mc-1);
                if(Endpoints(first,last,rc,mc,out var nc,out var nc2)&&(rc&(mod-1))==r) {
                    if(nc!=nc2)throw new Exception("odd tail not singleton");
                    Single(nc,Arithmetic.MulAddShift(P,nc,Q,S),c,used);
                }
                OddTail++;break;
            }
            if(d.Huge[c+1])continue;
            UInt128 target=d.Target[c+1],three=d.Three[k];
            UInt128 peakHi=Arithmetic.MulAddShift(three,checked(nhi+1),0,k)-1;
            if(target>peakHi/2)continue;
            int sk=S+k;UInt128 mk=UInt128.One<<(sk+1);
            if(mk>d.Master)throw new Exception("inverse precision");
            UInt128 rk=unchecked((den*((UInt128.One<<k)-1)-Q)*ip)&(mk-1);
            if((rk&(mod-1))!=r)continue;
            if(!Endpoints(first,last,rk,mk,out var fk,out var lk))continue;
            if(fk==lk){Single(fk,Arithmetic.MulAddShift(P,fk,Q,S),c,used);continue;}
            UInt128 pp=checked(three*P),qq=checked(three*Q+(three-(UInt128.One<<k))*den);
            peakHi=Arithmetic.MulAddShift(pp,lk,qq,sk);
            int lmax=BitLength(peakHi/target)-1;UInt128 ipp=d.Inverse[used+k];
            for(int l=1;l<=lmax;l++) {
                int ss=sk+l;if(ss>=128)throw new Exception("shift range");
                mc=UInt128.One<<ss;
                if(mc>lk-fk) {
                    UInt128 rc=unchecked((0-qq)*ipp)&(mc-1);
                    if(Endpoints(fk,lk,rc,mc,out var nc,out var nc2)&&(rc&(mk-1))==rk) {
                        if(nc!=nc2)throw new Exception("even tail not singleton");
                        Single(nc,Arithmetic.MulAddShift(P,nc,Q,S),c,used);
                    }
                    EvenTail++;break;
                }
                UInt128 mm=mc<<1;if(mm>d.Master)throw new Exception("inverse precision");
                UInt128 rr=unchecked((mc-qq)*ipp)&(mm-1);
                if((rr&(mk-1))!=rk)continue;
                Visit(new State(pp,qq,ss,fk,lk,rr,c+1,used+k));
            }
        }
    }
    public string Summary(string status,double seconds) {
        return "{\"status\":\""+status+"\",\"excluded\":"+(status=="complete"&&Survivors==0?"true":"false")+
            ",\"nodes\":"+Nodes+",\"singletons\":"+Singletons+",\"descent\":"+Descent+
            ",\"capacity\":"+Capacity+",\"empty\":"+Empty+",\"survivors\":"+Survivors+
            ",\"odd_tail\":"+OddTail+",\"even_tail\":"+EvenTail+",\"big_fallbacks\":"+BigFallbacks+",\"seconds\":"+seconds.ToString(System.Globalization.CultureInfo.InvariantCulture)+"}";
    }
    public void Merge(Kernel o) {
        Nodes+=o.Nodes;Singletons+=o.Singletons;Descent+=o.Descent;Capacity+=o.Capacity;Empty+=o.Empty;
        Survivors+=o.Survivors;OddTail+=o.OddTail;EvenTail+=o.EvenTail;
        BigFallbacks+=o.BigFallbacks;
        foreach(var seed in o.Seeds)Seeds.Add(seed);
        for(int i=0;i<Levels.Length;i++)Levels[i]+=o.Levels[i];
    }
    public static string Run(int m,string low,string high,string[] targets,int depth,long limit,int workers,int split,string journal) {
        var watch=Stopwatch.StartNew();var data=new Data(m,low,high,targets,depth);
        var total=new Kernel(data,limit);total.Jobs=new List<State>();total.Split=split;total.Visit(Root(data));
        Console.WriteLine("Prepared "+total.Jobs.Count+" disjoint prefix jobs.");
        int finished=0;bool failed=false;double last=watch.Elapsed.TotalSeconds;object gate=new object();
        using(var log=new StreamWriter(journal,false)) {
            log.WriteLine("{\"event\":\"start\",\"m\":"+m+",\"low\":\""+low+"\",\"high\":\""+high+"\",\"jobs\":"+total.Jobs.Count+"}");log.Flush();
            Parallel.For(0,total.Jobs.Count,new ParallelOptions{MaxDegreeOfParallelism=workers},j=> {
                var part=new Kernel(data,limit);string status="complete";
                try{part.Visit(total.Jobs[j]);}catch(Exception e){status=e.Message;}
                lock(gate) {
                    total.Merge(part);finished++;if(status!="complete")failed=true;
                    log.WriteLine("{\"job\":"+j+",\"receipt\":"+part.Summary(status,0)+"}");
                    if(watch.Elapsed.TotalSeconds-last>=15) {
                        Console.WriteLine("Completed "+finished+"/"+total.Jobs.Count+" jobs; "+total.Nodes+" nodes; "+watch.Elapsed.TotalSeconds.ToString("F1")+" seconds.");
                        log.Flush();last=watch.Elapsed.TotalSeconds;
                    }
                }
            });
            string result=total.Summary(failed?"incomplete":"complete",watch.Elapsed.TotalSeconds);
            log.WriteLine("{\"event\":\"finish\",\"receipt\":"+result+"}");log.Flush();return result;
        }
    }
}
}
