"""Strict complete-run journal audit; incomplete journals never pass.

This verifies receipt coverage and counter consistency, not execution of each
subtree. The search algorithm and its pruning proofs remain separate inputs.
"""
from pathlib import Path
import argparse,json,hashlib

def audit(path):
    starts=[]; finishes=[]; jobs={}; errors=[]
    counts=['nodes','singletons','descent','capacity','empty','survivors','odd_tail','even_tail']
    for line_no,line in enumerate(path.open(),1):
        try:
            row=json.loads(line)
        except json.JSONDecodeError:
            errors.append(f'malformed line {line_no}')
            continue
        if row.get('event')=='start':
            starts.append(row)
        elif row.get('event')=='finish':
            finishes.append(row)
        elif 'job' in row:
            j=row['job']
            if j in jobs: errors.append(f'duplicate job {j}')
            jobs[j]=row['receipt']
        else:
            errors.append(f'unknown row {line_no}')
    if len(starts)!=1: errors.append('expected exactly one start')
    if len(finishes)!=1: errors.append('expected exactly one finish')
    if starts:
        expected=set(range(starts[0]['jobs']))
        if set(jobs)!=expected: errors.append('job ID coverage incomplete or out of range')
    incomplete=[j for j,r in jobs.items() if r['status']!='complete']
    survivors=sum(r['survivors'] for r in jobs.values())
    if incomplete: errors.append('one or more jobs incomplete')
    if survivors: errors.append('one or more surviving branches')
    totals={key:sum(row[key] for row in jobs.values()) for key in counts}
    root={}
    if finishes:
        finish=finishes[0]['receipt']
        if finish['status']!='complete' or not finish['excluded'] or finish['survivors']!=0:
            errors.append('finish does not report a complete exclusion')
        root={key:finish[key]-totals[key] for key in counts}
        if any(v<0 for v in root.values()): errors.append('finish counters below job totals')
    result={'journal':path.name,'sha256':hashlib.file_digest(path.open('rb'),'sha256').hexdigest(),
            'status':'passed' if not errors else 'not_certified','jobs_present':len(jobs),
            'jobs_expected':starts[0]['jobs'] if starts else None,'survivors':survivors,
            'incomplete_jobs':incomplete,'errors':errors,'job_totals':totals,'generator_counters':root}
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('journal',type=Path); args=p.parse_args()
    result=audit(args.journal)
    out=args.journal.with_name(args.journal.stem.replace('-journal','')+'-audit.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
