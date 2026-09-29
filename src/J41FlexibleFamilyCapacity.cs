using System;
using System.Numerics;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;
using System.Text.Json;

namespace CollatzFlexibleNonlinearFamiliesJ41 {
public sealed class Family {
 public int k{get;set;} public int ell{get;set;} public int s{get;set;} public int q{get;set;}
 public string first_a{get;set;} public string last_a{get;set;} public string step_a{get;set;} public string count{get;set;}
}
public sealed class Input {
 public int J{get;set;} public int low_c_numerator{get;set;} public string verified_basin{get;set;} public string seed_count{get;set;} public List<Family> classes{get;set;}
}
public sealed class Receipt {
 public int id{get;set;} public string status{get;set;} public string expected{get;set;}
 public string restart_seeds{get;set;} public string basin_seeds{get;set;} public string singleton_seeds{get;set;}
 public long nodes{get;set;} public long singleton_steps{get;set;} public int max_depth{get;set;} public string error{get;set;}
}
public sealed class Data {
 public readonly BigInteger X=BigInteger.One<<71,Master,Mask;
 public readonly BigInteger[] Three=new BigInteger[2048],Inverse=new BigInteger[2048];
 public readonly int[][] Threshold=new int[512][];
 public readonly int MaxDepth;public readonly long NodeLimit;
 public const long Scale=1000000000;public readonly long[] LogLo=new long[257],LogHi=new long[257];public readonly long CScaled,LowCScaled,OffsetScaled;
 public Data(Input input,int depth,long limit,string logjson) {
  using var logs=JsonDocument.Parse(logjson);
  if(logs.RootElement.GetProperty("scale").GetInt64()!=Scale || logs.RootElement.GetProperty("grid").GetInt32()!=256)throw new Exception("log table shape");
  int position=0;
  foreach(var row in logs.RootElement.GetProperty("bounds").EnumerateArray()) {
   LogLo[position]=row.GetProperty("lower").GetInt64();LogHi[position]=row.GetProperty("upper").GetInt64();position++;
  }
  if(position!=257)throw new Exception("log table length");
  CScaled=(100*input.J-1)*10000000L;
  if(input.low_c_numerator<3799 || input.low_c_numerator>4153 || input.low_c_numerator>=100*input.J-1)throw new Exception("lower-intercept scope");
  LowCScaled=input.low_c_numerator*10000000L;OffsetScaled=71L*584962*1000-LowCScaled;
  if(OffsetScaled<=0)throw new Exception("map below identity");

  if((input.J!=41) || BigInteger.Parse(input.verified_basin)!=X)throw new Exception("input scope");
  MaxDepth=depth;NodeLimit=limit;int bits=0;
  foreach(var f in input.classes)bits=Math.Max(bits,(int)BigInteger.Parse(f.last_a).GetBitLength());
  if(bits>69)throw new Exception("odd part exceeds proved scope");
  Master=BigInteger.One<<(bits+2);Mask=Master-1;
  BigInteger inv3=(Master%3==2?Master+1:2*Master+1)/3;
  if(3*inv3%Master!=1)throw new Exception("inverse error");
  Three[0]=Inverse[0]=1;
  for(int i=1;i<Three.Length;i++){Three[i]=Three[i-1]*3;Inverse[i]=Inverse[i-1]*inv3&Mask;}
  for(int h=71;h<Threshold.Length;h++) {
   Threshold[h]=new int[depth+2];BigInteger num=100*h,den=100;
   for(int j=0;j<Threshold[h].Length;j++) {
    Threshold[h][j]=(int)(num/den);
    num=1584962*num-(100*input.J-1)*(den/100)*1000000;den*=1000000;
   }
  }
 }
}
public sealed class Checker {
 readonly Data d;readonly int rootK;
 public BigInteger Restart=0,Basin=0,Singles=0;public long Nodes,SingleSteps;public int MaxDepth;
 public Checker(Data data,int rootK){d=data;this.rootK=rootK;}
 static BigInteger Count(BigInteger lo,BigInteger hi,BigInteger mod){return (hi-lo)/mod+1;}
 static int Val(BigInteger n){if(n<=0)throw new Exception("nonpositive valuation");return (int)(n&-n).GetBitLength()-1;}
 static bool Intersect(BigInteger lo,BigInteger hi,BigInteger oldMod,BigInteger r,BigInteger mod,out BigInteger first,out BigInteger last,out BigInteger finalMod) {
  first=last=0;finalMod=BigInteger.Max(mod,oldMod);
  BigInteger minMod=BigInteger.Min(mod,oldMod);
  if(((r-lo)&(minMod-1))!=0)return false;
  if(oldMod>=mod){first=lo;last=hi;return true;}
  first=lo+((r-lo)&(mod-1));last=hi-((hi-r)&(mod-1));return first<=last;
 }
 static int Val128(UInt128 n) {
  if(n==0)throw new Exception("zero valuation");
  ulong low=(ulong)n;
  return low!=0?BitOperations.TrailingZeroCount(low):64+BitOperations.TrailingZeroCount((ulong)(n>>64));
 }
 void Single(BigInteger a,BigInteger n) {
  if(n<=0 || n.IsEven)throw new Exception("invalid singleton minimum");
  int steps=0;UInt128 cut=(UInt128)d.X,guard=(UInt128.MaxValue-1)/3;
  while(n>d.X) {
   if(n.GetBitLength()<=128) {
    UInt128 small=(UInt128)n;
    while(small>cut && small<=guard) {
     if(++steps>1000000)throw new Exception("singleton limit at a="+a);
     small=3*small+1;small>>=Val128(small);
    }
    n=(BigInteger)small;
    if(n<=d.X)break;
   }
   if(++steps>1000000 || n.GetBitLength()>4096)throw new Exception("singleton limit at a="+a);
   n=3*n+1;n>>=Val(n);
  }
  Singles++;SingleSteps+=steps;
 }
 long LogBound(BigInteger n,bool upper) {
  if(n<=0)throw new Exception("log domain");
  int exponent=(int)n.GetBitLength()-1;
  BigInteger unit=BigInteger.One<<exponent;
  int index=(int)(((n-unit)<<8)>>exponent);
  if(index<0 || index>=256)throw new Exception("log index");
  return checked(exponent*Data.Scale+(upper?d.LogHi[index+1]:d.LogLo[index]));
 }
 long Target(BigInteger a,int j) {
  long lower=checked(rootK*Data.Scale+LogBound(a,false));
  if(lower<71*Data.Scale)throw new Exception("height scope");
  for(int i=0;i<j;i++) {
   // Directed lower enclosure of the continuous nonlinear map:
   // max(d*y-(J-.01),min(d*y-37.99,y+71*(d-1)-37.99)).
   long grown=checked((long)(((Int128)1584962*lower)/1000000));
   long first=checked(grown-d.LowCScaled),last=checked(grown-d.CScaled);
   long middle=checked(lower+d.OffsetScaled);
   lower=Math.Max(last,Math.Min(first,middle));
  }
  return lower;
 }
 public void Visit(BigInteger P,BigInteger Q,int S,int used,BigInteger lo,BigInteger hi,BigInteger mod,int j) {
  if(++Nodes>d.NodeLimit)throw new Exception("node_limit");MaxDepth=Math.Max(MaxDepth,j);
  if(lo>hi || lo<=0 || (hi-lo)%mod!=0 || Q+(BigInteger.One<<S)<0)throw new Exception("state invariant");
  BigInteger den=BigInteger.One<<S,nlo=(P*lo+Q)>>S,nhi=(P*hi+Q)>>S;
  if(nlo<=0 || nlo.IsEven || nhi.IsEven || (P*lo+Q)%den!=0)throw new Exception("affine invariant");
  if(nhi<=d.X){Basin+=Count(lo,hi,mod);return;}
  if(nlo<=d.X) {
   BigInteger cut=(d.X*den-Q)/P;
   BigInteger last=hi-((hi-cut+mod-1)/mod)*mod;
   if(last<lo || last>hi || (P*last+Q)>>S>d.X)throw new Exception("basin cut");
   Basin+=Count(lo,last,mod);lo=last+mod;
   if(lo>hi)return;nlo=(P*lo+Q)>>S;
  }
  if(lo==hi){Single(lo,nlo);return;}
  // Monotonicity in a makes a passed least-endpoint test cover the class.
  if(LogBound(nlo+1,true)<=Target(lo,j)){Restart+=Count(lo,hi,mod);return;}
  // A passed sufficient test at ANY a certifies every larger a by the
  // exact monotonicity lemma. Rounded tests themselves need not be monotone.
  if(LogBound(nhi+1,true)<=Target(hi,j)) {
   BigInteger bad=0,good=Count(lo,hi,mod)-1;
   while(good-bad>1) {
    BigInteger mid=(bad+good)/2,am=lo+mid*mod,nm=(P*am+Q)>>S;
    if(LogBound(nm+1,true)<=Target(am,j))good=mid;else bad=mid;
   }
   BigInteger cut=lo+good*mod;
   if(cut<=lo || cut>hi || LogBound(((P*cut+Q)>>S)+1,true)>Target(cut,j))throw new Exception("restart suffix witness");
   Restart+=Count(cut,hi,mod);hi=cut-mod;nhi=(P*hi+Q)>>S;
   if(lo==hi){Single(lo,nlo);return;}
  }
  // An exact descent also implies restart because F_j(y)>=y for y>=71.
  BigInteger slope=P-(den<<rootK),intercept=Q+den;
  BigInteger worst=slope>=0?hi:lo;
  if(slope*worst+intercept<=0){Restart+=Count(lo,hi,mod);return;}
  // Q+den>=0. A decreasing affine difference may certify a proper suffix.
  if(slope<0 && slope*hi+intercept<=0) {
   BigInteger threshold=(intercept-slope-1)/(-slope);
   BigInteger cut=lo+((threshold-lo+mod-1)/mod)*mod;
   if(cut<=lo || cut>hi || slope*cut+intercept>0)throw new Exception("descent suffix witness");
   Restart+=Count(cut,hi,mod);hi=cut-mod;nhi=(P*hi+Q)>>S;
   if(lo==hi){Single(lo,nlo);return;}
  }
  if(j>=d.MaxDepth)throw new Exception("depth_limit");
  int kmax=(int)(nhi+1).GetBitLength()-1;
  BigInteger ip=d.Inverse[used];
  for(int k=1;k<=kmax;k++) {
   BigInteger tailMod=BigInteger.One<<(S+k);
   if(tailMod>hi-lo) {
    BigInteger r=(-den-Q)*ip&(tailMod-1);
    if(Intersect(lo,hi,mod,r,tailMod,out var a,out var b,out var mm)) {
     if(a!=b)throw new Exception("odd tail cardinality");Single(a,(P*a+Q)>>S);
    }
    break;
   }
   BigInteger km=tailMod<<1;
   if(km>d.Master)throw new Exception("inverse precision");
   BigInteger rk=(den*((BigInteger.One<<k)-1)-Q)*ip&(km-1);
   if(!Intersect(lo,hi,mod,rk,km,out var fk,out var lk,out var mk))continue;
   if(fk==lk){Single(fk,(P*fk+Q)>>S);continue;}
   if(k*Data.Scale>Target(fk,j))throw new Exception("intermediate run exceeds envelope on nonsingleton class");
   BigInteger pp=P*d.Three[k],qq=Q*d.Three[k]+(d.Three[k]-(BigInteger.One<<k))*den;
   int sk=S+k;BigInteger peak=(pp*lk+qq)>>sk;
   int lmax=(int)peak.GetBitLength()-1;BigInteger ipp=d.Inverse[used+k];
   for(int ell=1;ell<=lmax;ell++) {
    int ss=sk+ell;tailMod=BigInteger.One<<ss;
    if(tailMod>lk-fk) {
     BigInteger tailResidue=-qq*ipp&(tailMod-1);
     if(Intersect(fk,lk,mk,tailResidue,tailMod,out var tailA,out var tailB,out var mm)) {
      if(tailA!=tailB)throw new Exception("even tail cardinality");Single(tailA,(P*tailA+Q)>>S);
     }
     break;
    }
    BigInteger em=tailMod<<1;
    if(em>d.Master)throw new Exception("inverse precision");
    BigInteger r=(tailMod-qq)*ipp&(em-1);
    if(Intersect(fk,lk,mk,r,em,out var a,out var b,out var nextMod))Visit(pp,qq,ss,used+k,a,b,nextMod,j+1);
   }
  }
 }
 public static string Run(string json,string logjson,int workers,int depth,long nodeLimit,int take=0,string journalPath=null) {
  Input input=JsonSerializer.Deserialize<Input>(json);var d=new Data(input,depth,nodeLimit,logjson);
  int length=take<=0?input.classes.Count:Math.Min(take,input.classes.Count);
  using var journal=journalPath==null?null:new System.IO.StreamWriter(journalPath,false,new System.Text.UTF8Encoding(false));
  var rows=new Receipt[length];int done=0;long nodes=0;var watch=Stopwatch.StartNew();
  using var timer=new Timer(_=>Console.WriteLine($"Family capacity: {Volatile.Read(ref done)}/{length}; {Interlocked.Read(ref nodes)} nodes; {watch.Elapsed.TotalSeconds:F1}s"),null,15000,15000);
  Parallel.For(0,length,new ParallelOptions{MaxDegreeOfParallelism=workers},i=> {
   var f=input.classes[i];var check=new Checker(d,f.k);var receipt=new Receipt{id=i,status="unresolved",expected=f.count};rows[i]=receipt;
   try {
    BigInteger lo=BigInteger.Parse(f.first_a),hi=BigInteger.Parse(f.last_a),mod=BigInteger.Parse(f.step_a);
    if(Count(lo,hi,mod)!=BigInteger.Parse(f.count) || (lo<<f.k)-1<=d.X)throw new Exception("root extent");
    check.Visit(d.Three[f.k],-1,f.ell,f.k,lo,hi,mod,1);
    if(check.Restart+check.Basin+check.Singles!=BigInteger.Parse(f.count))throw new Exception("coverage count mismatch");
    receipt.status="complete";
   } catch(Exception e){receipt.error=e.ToString();}
   receipt.restart_seeds=check.Restart.ToString();receipt.basin_seeds=check.Basin.ToString();receipt.singleton_seeds=check.Singles.ToString();
   receipt.nodes=check.Nodes;receipt.singleton_steps=check.SingleSteps;receipt.max_depth=check.MaxDepth;
   if(journal!=null)lock(journal){journal.WriteLine(JsonSerializer.Serialize(receipt));journal.Flush();}
   Interlocked.Add(ref nodes,check.Nodes);Interlocked.Increment(ref done);
  });
  bool complete=true;BigInteger expected=0,restart=0,basin=0,singles=0;long singleSteps=0;int maximumDepth=0;
  foreach(var row in rows) {
   complete &= row.status=="complete";expected+=BigInteger.Parse(row.expected);restart+=BigInteger.Parse(row.restart_seeds);
   basin+=BigInteger.Parse(row.basin_seeds);singles+=BigInteger.Parse(row.singleton_seeds);singleSteps+=row.singleton_steps;maximumDepth=Math.Max(maximumDepth,row.max_depth);
  }
  bool full=length==input.classes.Count && expected==BigInteger.Parse(input.seed_count);
  return JsonSerializer.Serialize(new {status=complete?"complete":"unresolved",full_input=full,capacity_exceptions_discharged=complete&&full,
   capacity_kind="nonlinear_block_restart",linear_coefficient_certified=false,map_id="plateau-c"+input.low_c_numerator.ToString()+"-c"+(100*input.J-1).ToString()+"-h71",J=input.J,classes=length,seeds=expected.ToString(),restart_seeds=restart.ToString(),basin_seeds=basin.ToString(),singleton_seeds=singles.ToString(),
   nodes,singleton_steps=singleSteps,max_depth=maximumDepth,seconds=watch.Elapsed.TotalSeconds,rows},new JsonSerializerOptions{WriteIndented=true});
 }
}
}
