// Checkpoint orchestration only. The frozen CollatzWide mathematical kernel
// and its exact job generator are reused without modification.
using System;
using System.IO;
using System.Text.Json;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
using CollatzWide;

namespace CollatzCheckpoint {
public static class Resumer {
 static long Nonnegative(JsonElement row,string key) {
  long value=row.GetProperty(key).GetInt64();
  if(value<0)throw new Exception("negative checkpoint counter: "+key);
  return value;
 }
 static Kernel Receipt(Data data,JsonElement row) {
  var k=new Kernel(data,long.MaxValue);
  k.Nodes=Nonnegative(row,"nodes");k.Singletons=Nonnegative(row,"singletons");
  k.Descent=Nonnegative(row,"descent");k.Capacity=Nonnegative(row,"capacity");
  k.Empty=Nonnegative(row,"empty");k.Survivors=Nonnegative(row,"survivors");
  k.OddTail=Nonnegative(row,"odd_tail");k.EvenTail=Nonnegative(row,"even_tail");
  k.BigFallbacks=Nonnegative(row,"big_fallbacks");return k;
 }
 public static string Run(int m,string low,string high,string[] targets,int depth,long limit,
                          int workers,int split,string journal,string parent,string parentHash) {
  var watch=Stopwatch.StartNew();var data=new Data(m,low,high,targets,depth);
  var total=new Kernel(data,limit);total.Jobs=new List<State>();total.Split=split;
  total.Visit(Kernel.Root(data));
  int jobs=total.Jobs.Count;var inherited=new Dictionary<int,string>();
  var seen=new HashSet<int>();bool started=false,finishedParent=false,truncatedTail=false;
  using(var reader=new StreamReader(parent)) {
   string line;int lineNumber=0;
   while((line=reader.ReadLine())!=null) {
    lineNumber++;JsonDocument doc;
    try{doc=JsonDocument.Parse(line);}
    catch(JsonException) {
     if(!reader.EndOfStream)throw new Exception("malformed interior checkpoint row");
     truncatedTail=true;break;
    }
    using(doc) {
     var row=doc.RootElement;
     if(row.TryGetProperty("event",out var evt)) {
      if(evt.GetString()=="start") {
       if(started || lineNumber!=1)throw new Exception("duplicate or displaced checkpoint start");
       if(row.GetProperty("m").GetInt32()!=m || row.GetProperty("low").GetString()!=low ||
          row.GetProperty("high").GetString()!=high || row.GetProperty("jobs").GetInt32()!=jobs)
          throw new Exception("checkpoint partition mismatch");
       started=true;
      } else if(evt.GetString()=="finish") {
       if(!started || finishedParent)throw new Exception("invalid checkpoint finish");
       finishedParent=true;
      } else throw new Exception("unknown checkpoint event");
     } else {
      if(!started || finishedParent)throw new Exception("checkpoint job outside run");
      int id=row.GetProperty("job").GetInt32();
      if(id<0 || id>=jobs || !seen.Add(id))throw new Exception("duplicate or invalid checkpoint job");
      var receipt=row.GetProperty("receipt");
      // A limited or unresolved job must be rerun in full. Its partial
      // counters are not carried into the new completed computation.
      if(receipt.GetProperty("status").GetString()!="complete")continue;
      var previous=Receipt(data,receipt);
      if(previous.Survivors!=0)continue;
      inherited.Add(id,line);total.Merge(previous);
     }
    }
   }
  }
  if(!started)throw new Exception("missing checkpoint header");
  int finished=inherited.Count;bool failed=false;object gate=new object();double last=watch.Elapsed.TotalSeconds;
  Console.WriteLine($"Prepared {jobs} disjoint jobs; inherited {finished}; discarded truncated tail: {truncatedTail}.");
  using(var log=new StreamWriter(journal,false)) {
   log.WriteLine(JsonSerializer.Serialize(new { @event="start",m,low,high,jobs,
                resumed_jobs=inherited.Count,parent_journal_sha256=parentHash,discarded_truncated_tail=truncatedTail }));
   foreach(var row in inherited.Values)log.WriteLine(row);
   log.Flush();
   Parallel.For(0,jobs,new ParallelOptions{MaxDegreeOfParallelism=workers},id=> {
    if(inherited.ContainsKey(id))return;
    var part=new Kernel(data,limit);string status="complete";
    try{part.Visit(total.Jobs[id]);}catch(Exception e){status=e.Message;}
    lock(gate) {
     total.Merge(part);finished++;if(status!="complete")failed=true;
     log.WriteLine("{\"job\":"+id+",\"receipt\":"+part.Summary(status,0)+"}");
     if(watch.Elapsed.TotalSeconds-last>=15) {
      Console.WriteLine($"Completed {finished}/{jobs} jobs; {total.Nodes} nodes including checkpoint; {watch.Elapsed.TotalSeconds:F1}s.");
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
