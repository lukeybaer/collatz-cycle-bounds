"""Select every completed wide-search job that used arbitrary-precision fallback."""
from pathlib import Path
import argparse, hashlib, json

ROOT = Path(__file__).resolve().parents[1]

def main(label):
    journal = ROOT/'results'/(label+'-journal.jsonl')
    result = json.loads((journal.parent/(label+'-result.json')).read_text(encoding='utf-8-sig'))
    assert result['status'] == 'complete'
    rows = []
    with journal.open(encoding='utf-8-sig') as stream:
        for line in stream:
            row = json.loads(line)
            if 'job' in row and row['receipt'].get('big_fallbacks', 0):
                assert row['receipt']['status'] == 'complete'
                rows.append(row)
    assert len({r['job'] for r in rows}) == len(rows)
    assert sum(r['receipt']['big_fallbacks'] for r in rows) == result['big_fallbacks']
    with journal.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    receipt = {'label': label, 'journal_sha256': digest, 'jobs': rows,
               'selector_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (journal.parent/(label+'-fallback-jobs.json')).write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(label, [(r['job'], r['receipt']['nodes'], r['receipt']['big_fallbacks']) for r in rows], flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('label')
    main(parser.parse_args().label)
