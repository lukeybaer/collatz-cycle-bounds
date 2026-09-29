using System;
using System.Numerics;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;

public static class CollatzPartitionAudit {
    public static string Compare(int m,string low,string high,string[] targets,int depth,int split) {
        var originalData=new CollatzExact.Data(m,low,high,targets,depth);
        var wideData=new CollatzWide.Data(m,low,high,targets,depth);
        var original=new CollatzExact.Kernel(originalData,2000000000);
        var wide=new CollatzWide.Kernel(wideData,2000000000);
        original.Jobs=new List<CollatzExact.State>();original.Split=split;
        wide.Jobs=new List<CollatzWide.State>();wide.Split=split;
        original.Visit(new CollatzExact.State(1,0,0,originalData.Low,originalData.High,1,0,0));
        wide.Visit(CollatzWide.Kernel.Root(wideData));
        if(original.Jobs.Count!=wide.Jobs.Count)throw new Exception("partition count mismatch");
        using(var hash=IncrementalHash.CreateHash(HashAlgorithmName.SHA256)) {
            for(int j=0;j<original.Jobs.Count;j++) {
                var a=original.Jobs[j];var b=wide.Jobs[j];
                if(a.P!=(BigInteger)b.P || a.Q!=(BigInteger)b.Q || a.S!=b.S || a.Lo!=(BigInteger)b.Lo ||
                   a.Hi!=(BigInteger)b.Hi || a.R!=(BigInteger)b.R || a.Completed!=b.Completed || a.Used!=b.Used)
                    throw new Exception("partition state mismatch at "+j);
                string record=j+":"+a.P+":"+a.Q+":"+a.S+":"+a.Lo+":"+a.Hi+":"+a.R+":"+a.Completed+":"+a.Used+"\n";
                hash.AppendData(Encoding.UTF8.GetBytes(record));
            }
            if(original.Nodes!=wide.Nodes || original.Singletons!=wide.Singletons || original.Descent!=wide.Descent ||
               original.Capacity!=wide.Capacity || original.Empty!=wide.Empty || original.Survivors!=wide.Survivors ||
               original.OddTail!=wide.OddTail || original.EvenTail!=wide.EvenTail)
                throw new Exception("generator counters mismatch");
            return "{\"status\":\"passed\",\"jobs\":"+original.Jobs.Count+",\"ordered_partition_sha256\":\""+
                Convert.ToHexString(hash.GetHashAndReset()).ToLowerInvariant()+"\",\"generator_nodes\":"+original.Nodes+"}";
        }
    }
}
