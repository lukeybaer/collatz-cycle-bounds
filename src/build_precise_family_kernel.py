"""Preserve the coarse verifier and generate a version with certified logs."""
from pathlib import Path
from fractions import Fraction as F
import json
from exact_intervals import L2LO,L2HI
ROOT=Path(__file__).resolve().parents[1];SCALE=10**9;GRID=256
rows=[]
for j in range(GRID+1):
    if j in (0,GRID):lo=hi=j*SCALE//GRID
    else:
        z=F(j,2*GRID+j);power=z;lower=F(0)
        for t in range(40):lower+=2*power/(2*t+1);power*=z*z
        upper=lower+2*power/((2*40+1)*(1-z*z))
        lo=(lower/L2HI*SCALE).__floor__();hi=(upper/L2LO*SCALE).__ceil__()
    rows.append({'lower':lo,'upper':hi})
(ROOT/'results'/'log2-mantissa-table.json').write_text(json.dumps({'scale':SCALE,'grid':GRID,'bounds':rows},indent=2)+'\n')
source=(ROOT/'src'/'FamilyCapacityVerifier.cs').read_text()
def replace(old,new):
    global source
    assert source.count(old)==1,old
    source=source.replace(old,new)
replace('namespace CollatzFamilies {','namespace CollatzFamiliesPrecise {')
replace('public readonly int MaxDepth;public readonly long NodeLimit;','public readonly int MaxDepth;public readonly long NodeLimit;\n public const long Scale=1000000000;public readonly long[] LogLo=new long[257],LogHi=new long[257];public readonly long CScaled;')
replace('public Data(Input input,int depth,long limit) {','''public Data(Input input,int depth,long limit,string logjson) {
  using var logs=JsonDocument.Parse(logjson);
  if(logs.RootElement.GetProperty("scale").GetInt64()!=Scale || logs.RootElement.GetProperty("grid").GetInt32()!=256)throw new Exception("log table shape");
  int position=0;
  foreach(var row in logs.RootElement.GetProperty("bounds").EnumerateArray()) {
   LogLo[position]=row.GetProperty("lower").GetInt64();LogHi[position]=row.GetProperty("upper").GetInt64();position++;
  }
  if(position!=257)throw new Exception("log table length");
  CScaled=(100*input.J-1)*10000000L;
''')
old=''' int Target(BigInteger a,int j) {
  int h=rootK+(int)a.GetBitLength()-1;
  if(h<71 || h>=d.Threshold.Length)throw new Exception("height scope");
  return d.Threshold[h][j];
 }'''
new=''' long LogBound(BigInteger n,bool upper) {
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
  for(int i=0;i<j;i++)lower=checked((long)(((Int128)1584962*lower)/1000000)-d.CScaled);
  return lower;
 }'''
replace(old,new)
replace('if(nlo.GetBitLength()<=Target(lo,j))','if(LogBound(nlo+1,true)<=Target(lo,j))')
replace('if(k>Target(fk,j))','if(k*Data.Scale>Target(fk,j))')
replace('public static string Run(string json,int workers,int depth,long nodeLimit,int take=0)',
        'public static string Run(string json,string logjson,int workers,int depth,long nodeLimit,int take=0)')
replace('var d=new Data(input,depth,nodeLimit);','var d=new Data(input,depth,nodeLimit,logjson);')
(ROOT/'src'/'FamilyCapacityPrecise.cs').write_text(source)
runner=(ROOT/'src'/'run_family_verifier.ps1').read_text().replace('FamilyCapacityVerifier.cs','FamilyCapacityPrecise.cs')
runner=runner.replace('$result=[CollatzFamilies.Checker]::Run((Get-Content -LiteralPath $InputFile -Raw),',
    "$logs=Join-Path $resultDir 'log2-mantissa-table.json'\n(Get-FileHash -LiteralPath $logs -Algorithm SHA256).Hash | Set-Content -LiteralPath (Join-Path $resultDir ($Label+'-logtable.sha256'))\n$result=[CollatzFamiliesPrecise.Checker]::Run((Get-Content -LiteralPath $InputFile -Raw),(Get-Content -LiteralPath $logs -Raw),")
(ROOT/'src'/'run_family_precise.ps1').write_text(runner)
print('Generated precise kernel and257 certified mantissa bounds.')
