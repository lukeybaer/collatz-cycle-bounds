"""Audit resumed search provenance and exact inheritance of completed jobs."""
from pathlib import Path
import argparse, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / 'results'

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def resolve_parent(original, expected):
    # Absolute launch paths are historical metadata, not a portability
    # requirement. A relocated parent must match its original raw-byte hash.
    original=Path(original);expected=expected.lower()
    for candidate in (original,R/original.name,R/'resume-parents'/(expected+original.suffix)):
        if candidate.is_file() and sha(candidate)==expected:return candidate
    raise AssertionError('Missing hash-matching resume parent: '+str(original))

def rows(path, allow_truncated=False):
    # Reading all lines also lets us reject malformed interior records independently.
    lines = Path(path).read_text(encoding='utf-8-sig').splitlines()
    result = []; truncated = False
    for index, line in enumerate(lines):
        try:
            result.append(json.loads(line))
        except json.JSONDecodeError:
            assert allow_truncated and index == len(lines)-1
            truncated = True
    return result, truncated

def audit(label, comparison=None):
    meta_path = R / (label+'-metadata.json')
    meta = read(meta_path)
    parent = resolve_parent(meta['parentJournal'],meta['parentJournalHash'])
    parent_meta_path = resolve_parent(meta['parentMetadata'],meta['parentMetadataHash'])
    assert sha(parent) == meta['parentJournalHash'].lower()
    assert sha(parent_meta_path) == meta['parentMetadataHash'].lower()
    pm = read(parent_meta_path)
    for key in ('configHash', 'sourceHash', 'arithmeticHash', 'split'):
        assert meta[key] == pm[key], key
    assert meta['config'] == pm['config']
    for field, filename in (('sourceHash','PrefixKernel128.cs'),
                            ('arithmeticHash','WideInteger.cs'),
                            ('resumeSourceHash','ResumePrefixKernel.cs')):
        assert sha(ROOT/'src'/filename) == meta[field].lower(), filename
    old, truncated = rows(parent, True)
    assert old[0]['event'] == 'start'
    kept = {}; seen = set(); finished = False
    for row in old[1:]:
        if 'event' in row:
            assert row['event'] == 'finish' and not finished
            finished = True
            continue
        assert not finished
        job = row['job']
        assert job not in seen and 0 <= job < old[0]['jobs']
        seen.add(job)
        receipt = row['receipt']
        if receipt['status'] == 'complete' and receipt['survivors'] == 0:
            kept[job] = row
    new_path = R/(label+'-journal.jsonl')
    new, cut = rows(new_path)
    assert not cut and new[0]['event']=='start' and new[-1]['event']=='finish'
    for key in ('m','low','high','jobs'):
        assert old[0][key] == new[0][key]
    assert new[0]['resumed_jobs'] == len(kept)
    assert new[0]['discarded_truncated_tail'] == truncated
    assert new[0]['parent_journal_sha256'].lower() == sha(parent)
    new_jobs = {row['job']:row for row in new[1:-1]}
    assert len(new_jobs) == len(new)-2 == new[0]['jobs']
    assert set(new_jobs) == set(range(new[0]['jobs']))
    for job, row in kept.items():
        assert new_jobs[job] == row, job
    for suffix in ('-audit.json','-generator-audit.json','-partition-audit.json'):
        assert read(R/(label+suffix))['status']=='passed', suffix
    result = read(R/(label+'-result.json'))
    assert result == new[-1]['receipt']
    assert result['status']=='complete' and result['excluded'] and not result['survivors']
    compared = {}
    if comparison:
        other = read(R/(comparison+'-result.json'))
        for key in ('nodes','singletons','descent','capacity','empty','survivors',
                    'odd_tail','even_tail','big_fallbacks'):
            assert result[key] == other[key], key
            compared[key] = result[key]
    receipt = {'status':'passed','label':label,'inherited_jobs':len(kept),
               'truncated_parent_tail_ignored':truncated,'parent_jobs_seen':len(seen),
               'total_jobs':len(new_jobs),'parent_journal_sha256':sha(parent),
               'journal_sha256':sha(new_path),'metadata_sha256':sha(meta_path),
               'resumer_sha256':sha(ROOT/'src'/'ResumePrefixKernel.cs'),
               'comparison':comparison,'matching_complete_run_counters':compared}
    (R/(label+'-resume-audit.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt), flush=True)

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('label'); parser.add_argument('--comparison')
    args=parser.parse_args(); audit(args.label,args.comparison)
