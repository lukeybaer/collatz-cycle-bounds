using System;
using System.Numerics;

namespace CollatzWide {
public static class Arithmetic {
    // Exact 128 x 128 -> 256 multiplication, addition, and right shift.
    // An overflowing 128-bit result is rejected, never silently truncated.
    public static UInt128 MulAddShift(UInt128 a,UInt128 b,UInt128 add,int shift) {
        if(shift<0 || shift>255)throw new ArgumentOutOfRangeException(nameof(shift));
        ulong a0=(ulong)a,a1=(ulong)(a>>64),b0=(ulong)b,b1=(ulong)(b>>64);
        UInt128 p00=(UInt128)a0*b0,p01=(UInt128)a0*b1,p10=(UInt128)a1*b0,p11=(UInt128)a1*b1;
        UInt128 middle=(p00>>64)+(ulong)p01+(ulong)p10;
        UInt128 low=((UInt128)(ulong)middle<<64)|(ulong)p00;
        UInt128 high=p11+(p01>>64)+(p10>>64)+(middle>>64);
        UInt128 sum=unchecked(low+add);
        if(sum<low)high++;
        low=sum;
        if(shift==0) {
            if(high!=0)throw new OverflowException("shifted product exceeds UInt128");
            return low;
        }
        if(shift<128) {
            if((high>>shift)!=0)throw new OverflowException("shifted product exceeds UInt128");
            return (low>>shift)|(high<<(128-shift));
        }
        return high>>(shift-128);
    }
    public static string RunArithmeticTests(int randomCases=100000) {
        var rng=new Random(937102);var bytes=new byte[16];int checkedCases=0;
        BigInteger limit=(BigInteger.One<<128)-1;
        for(int i=0;i<randomCases;i++) {
            rng.NextBytes(bytes);UInt128 a=(UInt128)new BigInteger(bytes,true,false);
            rng.NextBytes(bytes);UInt128 b=(UInt128)new BigInteger(bytes,true,false);
            rng.NextBytes(bytes);UInt128 add=(UInt128)new BigInteger(bytes,true,false);
            int shift=rng.Next(256);
            BigInteger wanted=((BigInteger)a*(BigInteger)b+(BigInteger)add)>>shift;
            bool overflow=false;UInt128 got=0;
            try{got=MulAddShift(a,b,add,shift);}catch(OverflowException){overflow=true;}
            if(overflow!=(wanted>limit) || (!overflow&&(BigInteger)got!=wanted))throw new Exception("wide arithmetic mismatch "+i);
            checkedCases++;
        }
        UInt128[] edge={0,1,(UInt128)ulong.MaxValue,(UInt128)ulong.MaxValue+1,UInt128.MaxValue-1,UInt128.MaxValue};
        foreach(var a in edge)foreach(var b in edge)foreach(var add in edge)
        foreach(int shift in new int[]{0,1,63,64,65,79,80,127,128,129,191,192,255}) {
            BigInteger wanted=((BigInteger)a*(BigInteger)b+(BigInteger)add)>>shift;
            bool overflow=false;UInt128 got=0;
            try{got=MulAddShift(a,b,add,shift);}catch(OverflowException){overflow=true;}
            if(overflow!=(wanted>limit) || (!overflow&&(BigInteger)got!=wanted))throw new Exception("wide arithmetic edge mismatch");
            checkedCases++;
        }
        return "{\"status\":\"passed\",\"cases\":"+checkedCases+",\"reference\":\"System.Numerics.BigInteger\"}";
    }
}
}
