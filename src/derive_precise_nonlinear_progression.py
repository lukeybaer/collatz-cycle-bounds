"""Create a separate precise-height progression verifier; freeze inputs intact."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'src';R=ROOT/'results'
original=S/'NonlinearProgressionCapacityVerifier.cs'
text=original.read_text();old=text
def replace(a,b):
    global text
    assert text.count(a)==1, a[:90]
    text=text.replace(a,b)
replace('namespace CollatzNonlinearProgressionAudit {','namespace CollatzPreciseNonlinearProgressionAudit {')
replace('public readonly int[][] Limits=new int[512][];',
'''public const long Scale=1000000000;
 public readonly long[] LogLo=new long[257],LogHi=new long[257];
 public readonly long[][] Limits=new long[512*256][];''')
replace('public Data(Input input,int depth,long nodeLimit) {',
'''public Data(Input input,string logjson,int depth,long nodeLimit) {
  using var logs=JsonDocument.Parse(logjson);
  if(logs.RootElement.GetProperty("scale").GetInt64()!=Scale || logs.RootElement.GetProperty("grid").GetInt32()!=256)throw new Exception("log table shape");
  int position=0;
  foreach(var row in logs.RootElement.GetProperty("bounds").EnumerateArray()) {
   if(position>=257)throw new Exception("log table length");
   LogLo[position]=row.GetProperty("lower").GetInt64();LogHi[position]=row.GetProperty("upper").GetInt64();position++;
  }
  if(position!=257)throw new Exception("log table length");''')
replace('''  for(int h=71;h<Limits.Length;h++) {
   Limits[h]=new int[depth+2];BigInteger numerator=100*h,denominator=100;
   for(int j=0;j<Limits[h].Length;j++) {
    Limits[h][j]=(int)(numerator/denominator);''',
'''  for(int h=71;h<512;h++) for(int bin=0;bin<256;bin++) {
   int slot=h*256+bin;
   Limits[slot]=new long[depth+2];BigInteger numerator=h*Scale+LogLo[bin],denominator=Scale;
   for(int j=0;j<Limits[slot].Length;j++) {
    // Exact rational iteration; round only each stored output, never the next input.
    Limits[slot][j]=(long)(numerator*Scale/denominator);''')
replace(''' int Limit(BigInteger a,int j) {
  int h=rootK+(int)a.GetBitLength()-1;
  if(h<71 || h>=d.Limits.Length || j>d.Depth+1)throw new Exception("height scope");
  return d.Limits[h][j];
 }''',
''' static int Bin(BigInteger n,int exponent) {
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
 }''')
replace('if(n.GetBitLength()<=Limit(a,j))','if(UpperLog(n+1)<=Limit(a,j))')
replace('if(k>Limit(a,j))','if(checked(k*Data.Scale)>Limit(a,j))')
replace('public static string DumpLimits(string json,int depth)',
        'public static string DumpLimits(string json,string logs,int depth)')
replace('var data=new Data(input,depth,1);','var data=new Data(input,logs,depth,1);')
replace('public static string Run(string json,int workers,int depth,long nodeLimit,int take=0)',
        'public static string Run(string json,string logs,int workers,int depth,long nodeLimit,int take=0)')
replace('var data=new Data(input,depth,nodeLimit);','var data=new Data(input,logs,depth,nodeLimit);')
replace('capacity_kind="nonlinear_block_restart",linear_coefficient_certified=false,',
        'height_method="exact_rational_mantissa_grid",capacity_kind="nonlinear_block_restart",linear_coefficient_certified=false,')
target=S/'PreciseNonlinearProgressionVerifier.cs'
assert not target.exists(),'Refusing to overwrite a possibly active verifier'
target.write_text(text)
result={'original_source_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
        'generated_source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
        'map_id':'plateau-c3799-c4099-h71',
        'change':'Independent progression partition unchanged. Exact rational map thresholds indexed by certified logarithm mantissa grid; directed upper logs at restart. No inverse residues or P/Q/S states.',
        'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(R/'precise-nonlinear-progression-source-derivation.json').write_text(json.dumps(result,indent=2)+'\n')
print(target,flush=True)
