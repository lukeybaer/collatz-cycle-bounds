using System;
using System.Numerics;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;
using System.IO;

namespace CollatzFast {
public sealed class State {
    public BigInteger P,Q,Lo,Hi,R;
    public int S,Completed,Used;
    public State(BigInteger p,BigInteger q,int s,BigInteger lo,BigInteger hi,BigInteger r,int c,int u) {
        P=p;Q=q;S=s;Lo=lo;Hi=hi;R=r;Completed=c;Used=u;
    }
}
public sealed class Data {
    public readonly BigInteger Low,High,Master,Mask;
    public readonly int M,Depth,Bits,Batch;
    public readonly BigInteger[] Target,Inverse,Three;
    public Data(int m,string low,string high,string[] targets,int depth,int batch=1) {
        M=m;Batch=batch;Low=BigInteger.Parse(low);High=BigInteger.Parse(high);Depth=depth;
        Bits=(int)High.GetBitLength()+3;Master=BigInteger.One<<Bits;Mask=Master-1;
        Target=Array.ConvertAll(targets,BigInteger.Parse);
        Three=new BigInteger[Math.Max(Bits+1,1025)];Inverse=new BigInteger[Bits+1];
        Three[0]=1;Inverse[0]=1;
        BigInteger inv3=1;
        for(int b=1;b<Bits;b*=2) inv3=(inv3*(2-3*inv3))&Mask;
        if(((3*inv3)&Mask)!=1)throw new Exception("inverse verification");
        for(int i=1;i<Three.Length;i++)Three[i]=Three[i-1]*3;
        for(int i=1;i<=Bits;i++)Inverse[i]=(Inverse[i-1]*inv3)&Mask;
    }
}
public sealed class Kernel {
    readonly Data d;
    readonly long limit;
    public long Nodes,Singletons,Descent,Capacity,Empty,Survivors,OddTail,EvenTail;
    public long[] Levels;
    public HashSet<BigInteger> Seeds=new HashSet<BigInteger>();
    public List<State> Jobs;
    public int Split=-1;
    public Kernel(Data data,long nodeLimit) {d=data;limit=nodeLimit;Levels=new long[d.M+1];}
    static BigInteger Mod(BigInteger x,BigInteger modulus) {return x&(modulus-1); /* All callers use a positive power of two. */}
    static BigInteger Ceil(BigInteger a,BigInteger b) {
        var q=BigInteger.DivRem(a,b,out var rem);return rem.Sign>0?q+1:q;
    }
    static int Bits(BigInteger n) {return (int)n.GetBitLength();}
    static int Val2(BigInteger n) {return Bits(n&-n)-1;}
    static bool Endpoints(BigInteger lo,BigInteger hi,BigInteger r,BigInteger mod,out BigInteger first,out BigInteger last) {
        first=lo+Mod(r-lo,mod);last=hi-Mod(hi-r,mod);return first<=last;
    }
    void Record(BigInteger first,BigInteger last,BigInteger mod) {
        Survivors++;
        if(d.High-d.Low<=1024)for(var n=first;n<=last;n+=mod)Seeds.Add(n);
    }
    void Single(BigInteger n0,BigInteger n,int completed,int used) {
        Singletons++;
        for(int i=completed;i<=d.M;i++) {
            if(n<n0){Descent++;return;}
            if(n<d.Target[i]){Capacity++;return;}
            if(i==d.M){Record(n0,n0,1);return;}
            int k=Val2(n+1);
            var peak=(k<d.Three.Length?d.Three[k]:BigInteger.Pow(3,k))*((n+1)>>k)-1;
            n=peak>>Val2(peak);used+=k;
        }
    }
    public void Visit(State v) {
        Nodes++;Levels[v.Completed]++;
        if(Nodes>limit)throw new Exception("node_limit");
        var P=v.P;var Q=v.Q;int S=v.S,c=v.Completed,used=v.Used;
        var lo=BigInteger.Max(v.Lo,Ceil((d.Target[c]<<S)-Q,P));var hi=v.Hi;var r=v.R;
        var den=BigInteger.One<<S;var mod=den<<1;
        if(P<den)hi=BigInteger.Min(hi,Q/(den-P));
        if(!Endpoints(lo,hi,r,mod,out var first,out var last)){Empty++;return;}
        if(((last-first)>>(S+1))<d.Batch){for(var seed=first;seed<=last;seed+=mod)Single(seed,(P*seed+Q)>>S,c,used);return;}
        if(c>=d.Depth){Record(first,last,mod);return;}
        if(c==Split){Jobs.Add(new State(P,Q,S,first,last,r,c,used));return;}
        var nhi=(P*last+Q)>>S;
        int kmax=Bits(nhi+1)-1;
        var ip=d.Inverse[used];
        for(int k=1;k<=kmax;k++) {
            var mc=BigInteger.One<<(S+k);
            if(mc>last-first) {
                var rc=(-(BigInteger.One<<S)-Q)*ip&(mc-1);
                if(Endpoints(first,last,rc,mc,out var nc,out var nc2)&&Mod(rc-r,mod)==0) {
                    if(nc!=nc2)throw new Exception("odd tail not singleton");
                    Single(nc,(P*nc+Q)>>S,c,used);
                }
                OddTail++;break;
            }
            var target=d.Target[c+1];var three=d.Three[k];
            var peakHi=(three*(nhi+1)>>k)-1;
            if(peakHi<2*target)continue;
            int sk=S+k;var mk=BigInteger.One<<(sk+1);
            if(mk>d.Master)throw new Exception("inverse precision");
            var rk=(((BigInteger.One<<S)*((BigInteger.One<<k)-1)-Q)*ip)&(mk-1);
            if(Mod(rk-r,mod)!=0)continue;
            if(!Endpoints(first,last,rk,mk,out var fk,out var lk))continue;
            if(fk==lk){Single(fk,(P*fk+Q)>>S,c,used);continue;}
            var pp=three*P;var qq=three*Q+(three-(BigInteger.One<<k))*(BigInteger.One<<S);
            peakHi=(pp*lk+qq)>>sk;
            int lmax=Bits(peakHi/target)-1;
            var ipp=d.Inverse[used+k];
            for(int l=1;l<=lmax;l++) {
                int ss=sk+l;mc=BigInteger.One<<ss;
                if(mc>lk-fk) {
                    var rc=(-qq)*ipp&(mc-1);
                    if(Endpoints(fk,lk,rc,mc,out var nc,out var nc2)&&Mod(rc-rk,mk)==0) {
                        if(nc!=nc2)throw new Exception("even tail not singleton");
                        Single(nc,(P*nc+Q)>>S,c,used);
                    }
                    EvenTail++;break;
                }
                var mm=mc<<1;
                if(mm>d.Master)throw new Exception("inverse precision");
                var rr=((mc-qq)*ipp)&(mm-1);
                if(Mod(rr-rk,mk)!=0)continue;
                Visit(new State(pp,qq,ss,fk,lk,rr,c+1,used+k));
            }
        }
    }
    public string Summary(string status,double seconds) {
        return "{\"status\":\""+status+"\",\"excluded\":"+(status=="complete"&&Survivors==0?"true":"false")+
            ",\"nodes\":"+Nodes+",\"singletons\":"+Singletons+",\"descent\":"+Descent+
            ",\"capacity\":"+Capacity+",\"empty\":"+Empty+",\"survivors\":"+Survivors+
            ",\"odd_tail\":"+OddTail+",\"even_tail\":"+EvenTail+",\"seconds\":"+seconds.ToString(System.Globalization.CultureInfo.InvariantCulture)+"}";
    }
    public void Merge(Kernel o) {
        Nodes+=o.Nodes;Singletons+=o.Singletons;Descent+=o.Descent;Capacity+=o.Capacity;
        Empty+=o.Empty;Survivors+=o.Survivors;OddTail+=o.OddTail;EvenTail+=o.EvenTail;
        foreach(var seed in o.Seeds)Seeds.Add(seed);
        for(int i=0;i<Levels.Length;i++)Levels[i]+=o.Levels[i];
    }
    public static string Run(int m,string low,string high,string[] targets,int depth,long limit,int workers,int split,string journal,int batch=1) {
        var watch=Stopwatch.StartNew();var data=new Data(m,low,high,targets,depth,batch);
        var total=new Kernel(data,limit);total.Jobs=new List<State>();total.Split=split;
        total.Visit(new State(1,0,0,data.Low,data.High,1,0,0));
        Console.WriteLine("Prepared "+total.Jobs.Count+" disjoint prefix jobs.");
        int finished=0;bool failed=false;double last=watch.Elapsed.TotalSeconds;
        object gate=new object();
        using(var log=new StreamWriter(journal,false)) {
            log.WriteLine("{\"event\":\"start\",\"m\":"+m+",\"low\":\""+low+"\",\"high\":\""+high+"\",\"jobs\":"+total.Jobs.Count+"}");log.Flush();
            Parallel.For(0,total.Jobs.Count,new ParallelOptions{MaxDegreeOfParallelism=workers},j=> {
                var part=new Kernel(data,limit);string status="complete";
                try {part.Visit(total.Jobs[j]);}catch(Exception e){status=e.Message;}
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
