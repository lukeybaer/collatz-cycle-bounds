using System;
using System.Numerics;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;
using System.Text;
using System.Text.Json;
using System.Security.Cryptography;

namespace CollatzBasin {
public sealed class Case {
    public int k {get;set;}
    public int ell {get;set;}
    public int s {get;set;}
    public int q {get;set;}
    public string first_a {get;set;}
    public string last_a {get;set;}
    public string step_a {get;set;}
    public string count {get;set;}
}
public sealed class Input {
    public string verified_basin {get;set;}
    public string seed_count {get;set;}
    public List<Case> classes {get;set;}
}
public sealed class Receipt {
    public int id {get;set;}
    public string status {get;set;}
    public long seeds {get;set;}
    public long odd_steps {get;set;}
    public int max_steps {get;set;}
    public int max_bits {get;set;}
    public long bigint_steps {get;set;}
    public string trajectory_digest {get;set;}
    public string error {get;set;}
}
public static class Verifier {
    static readonly UInt128 SafeTriple=(UInt128.MaxValue-1)/3;
    static int Bits(UInt128 n) {
        ulong hi=(ulong)(n>>64);
        return hi!=0 ? 128-BitOperations.LeadingZeroCount(hi) : 64-BitOperations.LeadingZeroCount((ulong)n);
    }
    static int Zeros(UInt128 n) {
        ulong lo=(ulong)n;
        return lo!=0 ? BitOperations.TrailingZeroCount(lo) : 64+BitOperations.TrailingZeroCount((ulong)(n>>64));
    }
    // This proves entry into the EXTERNAL verified basin, not mere descent.
    // All limits throw; callers mark such classes unresolved.
    static (BigInteger end,int steps,int bits,long bigSteps) Follow(BigInteger start,BigInteger basin,bool reference,int stepLimit,int bitLimit) {
        BigInteger n=start;int steps=0,bits=(int)n.GetBitLength();long bigSteps=0;
        if(n<=basin || n<=0 || n.IsEven)throw new Exception("invalid exceptional seed");
        while(n>basin) {
            if(!reference && n<=(BigInteger)UInt128.MaxValue) {
                UInt128 u=(UInt128)n,stop=(UInt128)basin;
                while(u>stop && u<=SafeTriple) {
                    if(++steps>stepLimit)throw new Exception("step limit at "+start);
                    u=checked(3*u+1);
                    bits=Math.Max(bits,Bits(u));
                    if(bits>bitLimit)throw new Exception("bit limit at "+start);
                    u>>=Zeros(u);
                }
                n=(BigInteger)u;
                if(n<=basin)break;
            }
            if(++steps>stepLimit)throw new Exception("step limit at "+start);
            n=3*n+1;bigSteps++;
            bits=Math.Max(bits,(int)n.GetBitLength());
            if(bits>bitLimit)throw new Exception("bit limit at "+start);
            // Independent reference path uses repeated exact division by 2.
            while(n.IsEven)n/=2;
        }
        return(n,steps,bits,bigSteps);
    }
    public static string Run(string json,bool reference,int workers,int stepLimit=1000000,int bitLimit=4096) {
        Input data=JsonSerializer.Deserialize<Input>(json);
        BigInteger basin=BigInteger.Parse(data.verified_basin);
        if(basin!=(BigInteger.One<<71))throw new Exception("unexpected basin dependency");
        var rows=new Receipt[data.classes.Count];long done=0,total=0;
        var watch=Stopwatch.StartNew();
        using var timer=new Timer(_=>Console.WriteLine($"Basin: {Interlocked.Read(ref done)}/{rows.Length} classes; {Interlocked.Read(ref total)} seeds; {watch.Elapsed.TotalSeconds:F1}s"),null,15000,15000);
        Parallel.For(0,rows.Length,new ParallelOptions{MaxDegreeOfParallelism=workers},i=> {
            var row=new Receipt{id=i,status="unresolved"};rows[i]=row;
            try {
                Case c=data.classes[i];
                BigInteger first=BigInteger.Parse(c.first_a),last=BigInteger.Parse(c.last_a),step=BigInteger.Parse(c.step_a);
                long expected=long.Parse(c.count);
                if(first<=0 || last<first || step<=0 || (last-first)%step!=0 || (last-first)/step+1!=expected)throw new Exception("invalid class extent");
                using var digest=IncrementalHash.CreateHash(HashAlgorithmName.SHA256);
                for(BigInteger a=first;a<=last;a+=step) {
                    BigInteger n=(a<<c.k)-1;
                    var got=Follow(n,basin,reference,stepLimit,bitLimit);
                    row.seeds++;row.odd_steps+=got.steps;row.bigint_steps+=got.bigSteps;
                    row.max_steps=Math.Max(row.max_steps,got.steps);row.max_bits=Math.Max(row.max_bits,got.bits);
                    digest.AppendData(Encoding.ASCII.GetBytes($"{n}:{got.steps}:{got.end}:{got.bits}\n"));
                }
                if(row.seeds!=expected)throw new Exception("class count mismatch");
                row.trajectory_digest=Convert.ToHexString(digest.GetHashAndReset()).ToLowerInvariant();
                row.status="complete";
                Interlocked.Add(ref total,row.seeds);
            } catch(Exception ex) {row.error=ex.ToString();}
            Interlocked.Increment(ref done);
        });
        bool complete=true;long seeds=0,oddSteps=0,bigSteps=0;int maxSteps=0,maxBits=0;
        foreach(var row in rows) {
            complete &= row.status=="complete";seeds+=row.seeds;oddSteps+=row.odd_steps;bigSteps+=row.bigint_steps;
            maxSteps=Math.Max(maxSteps,row.max_steps);maxBits=Math.Max(maxBits,row.max_bits);
        }
        complete &= seeds==long.Parse(data.seed_count);
        return JsonSerializer.Serialize(new {status=complete?"complete":"unresolved",all_enter_verified_basin=complete,
            reference_path=reference,verified_basin=data.verified_basin,seeds,odd_steps=oddSteps,max_steps=maxSteps,
            max_bits=maxBits,bigint_steps=bigSteps,seconds=watch.Elapsed.TotalSeconds,rows},new JsonSerializerOptions{WriteIndented=true});
    }
}
}
