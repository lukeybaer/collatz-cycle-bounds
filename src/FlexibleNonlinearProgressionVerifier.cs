// Independent progression-index bisection, following the Python proof checker.
// This does not use the producer's modular inverses or affine P/Q/S states.
using System;
using System.Numerics;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;
using System.Text.Json;

namespace CollatzFlexibleNonlinearProgressionAudit {
public sealed class Family {
 public int k{get;set;} public int ell{get;set;} public int s{get;set;}
 public string first_a{get;set;} public string last_a{get;set;} public string step_a{get;set;} public string count{get;set;}
}
public sealed class Input {
 public int J{get;set;} public int low_c_numerator{get;set;} public string verified_basin{get;set;} public string assumed_cycle_minimum{get;set;}
 public string seed_count{get;set;} public List<Family> classes{get;set;}
}
public sealed class Receipt {
 public int id{get;set;} public string status{get;set;} public string seeds{get;set;}
 public string restart{get;set;} public string threshold{get;set;} public string singles{get;set;}
 public long nodes{get;set;} public long singleton_steps{get;set;} public long bigint_steps{get;set;}
 public int max_depth{get;set;} public string error{get;set;}
}
public sealed class Data {
 public readonly BigInteger Cut;
 public readonly UInt128 Cut128;
 public const long Scale=1000000000;
 public readonly long[] LogLo=new long[257],LogHi=new long[257];
 public readonly long[][] Limits=new long[512*256][];
 public readonly int Depth;
 public readonly long NodeLimit;
 public readonly bool Conditional;
 public Data(Input input,string logjson,int depth,long nodeLimit) {
  using var logs=JsonDocument.Parse(logjson);
  if(logs.RootElement.GetProperty("scale").GetInt64()!=Scale || logs.RootElement.GetProperty("grid").GetInt32()!=256)throw new Exception("log table shape");
  int position=0;
  foreach(var row in logs.RootElement.GetProperty("bounds").EnumerateArray()) {
   if(position>=257)throw new Exception("log table length");
   LogLo[position]=row.GetProperty("lower").GetInt64();LogHi[position]=row.GetProperty("upper").GetInt64();position++;
  }
  if(position!=257)throw new Exception("log table length");
  if(input.low_c_numerator<3799 || input.low_c_numerator>4153 || input.low_c_numerator>=100*input.J-1)throw new Exception("lower-intercept scope");
  BigInteger verified=BigInteger.One<<71;
  if(BigInteger.Parse(input.verified_basin)!=verified || (input.J<42 || input.J>48))throw new Exception("input scope");
  Conditional=input.assumed_cycle_minimum!=null;
  if(Conditional)throw new Exception("nonlinear proof requires the original basin input");
  Cut=Conditional?BigInteger.Parse(input.assumed_cycle_minimum):verified;
  if(Cut<verified || Cut.GetBitLength()>127)throw new Exception("threshold scope");
  Cut128=(UInt128)Cut;Depth=depth;NodeLimit=nodeLimit;
  for(int h=71;h<512;h++) for(int bin=0;bin<256;bin++) {
   int slot=h*256+bin;
   Limits[slot]=new long[depth+2];BigInteger numerator=h*Scale+LogLo[bin],denominator=Scale;
   for(int j=0;j<Limits[slot].Length;j++) {
    // Exact rational iteration; round only each stored output, never the next input.
    Limits[slot][j]=(long)(numerator*Scale/denominator);
    BigInteger grown=1584962*numerator;
    BigInteger first=grown-input.low_c_numerator*(denominator/100)*1000000;
    BigInteger last=grown-(100*input.J-1)*(denominator/100)*1000000;
    BigInteger middle=numerator*1000000+(71L*584962-input.low_c_numerator*10000L)*denominator;
    numerator=BigInteger.Max(last,BigInteger.Min(first,middle));
    denominator*=1000000;
   }
  }
 }
}
public sealed class Checker {
 readonly Data d;readonly int rootK;
 public BigInteger Restart,Threshold,Singles;
 public long Nodes,SingleSteps,BigSteps;
 public int MaxDepth;
 public Checker(Data data,int k){d=data;rootK=k;}
 static int Val(BigInteger n){if(n<=0)throw new Exception("valuation domain");return (int)(n&-n).GetBitLength()-1;}
 static int Val128(UInt128 n) {
  if(n==0)throw new Exception("valuation zero");
  ulong low=(ulong)n;
  return low!=0?BitOperations.TrailingZeroCount(low):64+BitOperations.TrailingZeroCount((ulong)(n>>64));
 }
 static int Bin(BigInteger n,int exponent) {
  int bin=(int)(((n-(BigInteger.One<<exponent))<<8)>>exponent);
  if(bin<0 || bin>=256)throw new Exception("mantissa bin");
  return bin;
 }
 long UpperLog(BigInteger n) {
  if(n<=0)throw new Exception("log domain");
  int exponent=(int)n.GetBitLength()-1;
  return checked(exponent*Data.Scale+d.LogHi[Bin(n,exponent)+1]);
 }
 long Limit(BigInteger a,int j) {
  int exponent=(int)a.GetBitLength()-1,h=rootK+exponent;
  if(h<71 || h>=512 || j>d.Depth+1)throw new Exception("height scope");
  return d.Limits[h*256+Bin(a,exponent)][j];
 }
 void Single(BigInteger n) {
  if(n<=0 || n.IsEven)throw new Exception("singleton domain");
  int steps=0;
  UInt128 cutoff=(UInt128.MaxValue-1)/3;
  while(n>d.Cut) {
   if(n.GetBitLength()<=128) {
    UInt128 small=(UInt128)n;
    while(small>d.Cut128 && small<=cutoff) {
     small=3*small+1;small>>=Val128(small);
     if(++steps>=1000000)throw new Exception("singleton step limit");
    }
    n=(BigInteger)small;
    if(n<=d.Cut)break;
   }
   n=3*n+1;n>>=Val(n);BigSteps++;
   if(++steps>=1000000 || n.GetBitLength()>4096)throw new Exception("singleton limit");
  }
  Singles++;SingleSteps+=steps;
 }
 public void Visit(BigInteger a,BigInteger mod,BigInteger count,BigInteger n,BigInteger stride,int j) {
  Nodes++;MaxDepth=Math.Max(MaxDepth,j);
  if(Nodes>d.NodeLimit)throw new Exception("node limit");
  if(count<=0 || a<=0 || mod<=0 || n<=0 || n.IsEven || stride<=0 || !stride.IsEven)throw new Exception("progression invariant");
  if((n+1)*mod-stride*a<0)throw new Exception("restart monotonicity invariant");
  if(n<=d.Cut) {
   BigInteger gone=BigInteger.Min(count,(d.Cut-n)/stride+1);
   Threshold+=gone;count-=gone;
   if(count==0)return;
   a+=gone*mod;n+=gone*stride;
  }
  if(count==1){Single(n);return;}
  if(UpperLog(n+1)<=Limit(a,j)){Restart+=count;return;}
  BigInteger high=n+stride*(count-1);
  if(UpperLog(high+1)<=Limit(a+(count-1)*mod,j)) {
   // A passed endpoint certifies its entire suffix by the checked invariant
   // (n+1)*mod-stride*a>=0 and Phi-iterate slopes >=1.
   // The rounded test itself need not be monotone: the right endpoint
   // remains a certified passing endpoint at every bisection step.
   BigInteger left=0,right=count-1;
   while(left<right) {
    BigInteger middle=(left+right)/2;
    if(UpperLog(n+middle*stride+1)<=Limit(a+middle*mod,j))right=middle;
    else left=middle+1;
   }
   Restart+=count-right;count=right;
   if(count==0)return;
   if(count==1){Single(n);return;}
   high=n+stride*(count-1);
  }
  BigInteger firstDifference=n-((a<<rootK)-1);
  BigInteger lastDifference=high-(((a+(count-1)*mod)<<rootK)-1);
  if(BigInteger.Max(firstDifference,lastDifference)<=0){Restart+=count;return;}
  if(j>=d.Depth)throw new Exception("depth limit");
  Odd(a,mod,count,n,stride,j);
 }
 void Odd(BigInteger a,BigInteger mod,BigInteger count,BigInteger n,BigInteger stride,int j) {
  if(count==1){Single(n);return;}
  int k=Val(n+1);
  if(k>=Val(stride)) {
   Odd(a,2*mod,(count+1)/2,n,2*stride,j);
   if(count/2>0)Odd(a+mod,2*mod,count/2,n+stride,2*stride,j);
   return;
  }
  if(checked(k*Data.Scale)>Limit(a,j))throw new Exception("intermediate odd-run envelope");
  BigInteger power=BigInteger.Pow(3,k);
  BigInteger peak=((n+1)>>k)*power-1,newStride=(stride>>k)*power;
  Even(a,mod,count,peak,newStride,j,n,stride);
 }
 void Even(BigInteger a,BigInteger mod,BigInteger count,BigInteger peak,BigInteger stride,int j,BigInteger oldN,BigInteger oldStride) {
  if(count==1){Single(oldN);return;}
  int ell=Val(peak);
  if(ell>=Val(stride)) {
   Even(a,2*mod,(count+1)/2,peak,2*stride,j,oldN,2*oldStride);
   if(count/2>0)Even(a+mod,2*mod,count/2,peak+stride,2*stride,j,oldN+oldStride,2*oldStride);
   return;
  }
  Visit(a,mod,count,peak>>ell,stride>>ell,j+1);
 }
 public static string DumpLimits(string json,string logs,int depth) {
  Input input=JsonSerializer.Deserialize<Input>(json);var data=new Data(input,logs,depth,1);
  return JsonSerializer.Serialize(data.Limits);
 }
 public static string Run(string json,string logs,int workers,int depth,long nodeLimit,int take=0) {
  Input input=JsonSerializer.Deserialize<Input>(json);var data=new Data(input,logs,depth,nodeLimit);
  int length=take<=0?input.classes.Count:Math.Min(take,input.classes.Count);
  var rows=new Receipt[length];int done=0;long nodes=0;var watch=Stopwatch.StartNew();
  using var timer=new Timer(_=>Console.WriteLine($"Progression audit: {Volatile.Read(ref done)}/{length}; {Interlocked.Read(ref nodes)} nodes; {watch.Elapsed.TotalSeconds:F1}s"),null,15000,15000);
  Parallel.For(0,length,new ParallelOptions{MaxDegreeOfParallelism=workers},i=> {
   var f=input.classes[i];var checker=new Checker(data,f.k);
   var receipt=new Receipt{id=i,status="unresolved",seeds=f.count};rows[i]=receipt;
   try {
    BigInteger a=BigInteger.Parse(f.first_a),last=BigInteger.Parse(f.last_a),mod=BigInteger.Parse(f.step_a),count=BigInteger.Parse(f.count);
    if(count<=0 || last!=a+(count-1)*mod || (a<<f.k)-1<=data.Cut)throw new Exception("root extent");
    BigInteger power=BigInteger.Pow(3,f.k),numerator=a*power-1,den=BigInteger.One<<f.ell;
    if(numerator%den!=0 || mod%den!=0)throw new Exception("root divisibility");
    BigInteger n=numerator>>f.ell,stride=power*(mod>>f.ell);
    if(Val(n+1)!=f.s)throw new Exception("next odd-run valuation");
    checker.Visit(a,mod,count,n,stride,1);
    if(checker.Restart+checker.Threshold+checker.Singles!=count)throw new Exception("coverage mismatch");
    receipt.status="complete";
   }catch(Exception e){receipt.error=e.ToString();}
   receipt.restart=checker.Restart.ToString();receipt.threshold=checker.Threshold.ToString();receipt.singles=checker.Singles.ToString();
   receipt.nodes=checker.Nodes;receipt.singleton_steps=checker.SingleSteps;receipt.bigint_steps=checker.BigSteps;receipt.max_depth=checker.MaxDepth;
   Interlocked.Add(ref nodes,checker.Nodes);Interlocked.Increment(ref done);
  });
  bool complete=true;BigInteger seeds=0,restart=0,threshold=0,singles=0;long steps=0,bigSteps=0;int maxDepth=0;
  foreach(var row in rows) {
   complete &= row.status=="complete";seeds+=BigInteger.Parse(row.seeds);restart+=BigInteger.Parse(row.restart);
   threshold+=BigInteger.Parse(row.threshold);singles+=BigInteger.Parse(row.singles);steps+=row.singleton_steps;bigSteps+=row.bigint_steps;maxDepth=Math.Max(maxDepth,row.max_depth);
  }
  bool full=length==input.classes.Count && seeds==BigInteger.Parse(input.seed_count);
  return JsonSerializer.Serialize(new {status=complete?"complete":"unresolved",full_input=full,capacity_exceptions_discharged=complete&&full,
   conditional_only=data.Conditional,assumed_cycle_minimum=data.Conditional?data.Cut.ToString():null,
   height_method="exact_rational_mantissa_grid_clipped",capacity_kind="nonlinear_block_restart",linear_coefficient_certified=false,map_id="plateau-c"+input.low_c_numerator.ToString()+"-c"+(100*input.J-1).ToString()+"-h71",J=input.J,classes=length,seeds=seeds.ToString(),restart_seeds=restart.ToString(),threshold_seeds=threshold.ToString(),singleton_seeds=singles.ToString(),
   nodes,singleton_steps=steps,bigint_steps=bigSteps,max_depth=maxDepth,seconds=watch.Elapsed.TotalSeconds,rows},new JsonSerializerOptions{WriteIndented=true});
 }
}
}
