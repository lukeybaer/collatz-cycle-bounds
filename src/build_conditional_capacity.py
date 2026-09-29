"""Restrict audited global exception classes to a hypothetical cycle minimum.

The threshold here is an ASSUMPTION about a cycle, not a convergence basin.
No verification of all integers below this threshold is claimed.
"""
from pathlib import Path
import argparse, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / 'results'
X = 2**71

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build(J, factor):
    assert 2 <= J <= 41 and factor >= 1
    source = R / f'extended-capacity-J{J}-classes.json'
    data = json.loads(source.read_text(encoding='utf-8-sig'))
    assert data['J'] == J and int(data['verified_basin']) == X
    threshold = factor * X
    rows = []
    removed = 0
    for index, original in enumerate(data['classes']):
        k = original['k']
        first, last, step, count = map(int, (original[key] for key in ('first_a', 'last_a', 'step_a', 'count')))
        assert last == first + (count-1)*step
        minimum_a = ((threshold+1) >> k) + 1
        offset = max(0, (minimum_a-first+step-1)//step)
        offset = min(count, offset)
        # Independent clipping identity, computed in n rather than a.
        gone = min(count, max(0, (threshold-((first << k)-1))//(step << k)+1))
        assert gone == offset
        removed += gone
        if gone == count:
            continue
        row = dict(original)
        row.update(source_class=index, first_a=str(first+gone*step), count=str(count-gone))
        assert (int(row['first_a']) << k)-1 > threshold
        if gone:
            assert ((int(row['first_a'])-step) << k)-1 <= threshold
        rows.append(row)
    seed_count = sum(int(row['count']) for row in rows)
    assert seed_count+removed == int(data['seed_count'])
    result = dict(data)
    result.update(status='conditional_exceptions_pending',
                  assumed_cycle_minimum=str(threshold), minimum_factor=factor,
                  scope='Only cycles whose every minimum is strictly greater than the assumed threshold.',
                  warning='The threshold is not an extended verified convergence basin.',
                  class_count=len(rows), seed_count=str(seed_count), classes=rows,
                  source_classes_sha256=digest(source), removed_seeds=str(removed))
    name = f'conditional-capacity-J{J}-f{factor}-classes.json'
    (R/name).write_text(json.dumps(result, indent=2)+'\n')
    print(name, 'classes', len(rows), 'seeds', seed_count, flush=True)

def sources():
    source = ROOT/'src'/'FamilyCapacityPrecise.cs'
    text = source.read_text()
    replacements = [
        ('CollatzFamiliesPrecise', 'CollatzConditionalFamilies'),
        ('public string verified_basin{get;set;}', 'public string verified_basin{get;set;} public string assumed_cycle_minimum{get;set;}'),
        ('public readonly BigInteger X=BigInteger.One<<71,Master,Mask;', 'public readonly BigInteger Cut,Master,Mask;'),
        ('if(input.J<2 || input.J>41 || BigInteger.Parse(input.verified_basin)!=X)throw new Exception("input scope");',
         'Cut=BigInteger.Parse(input.assumed_cycle_minimum);\n  if(input.J<2 || input.J>41 || BigInteger.Parse(input.verified_basin)!=(BigInteger.One<<71) || Cut<(BigInteger.One<<71))throw new Exception("conditional input scope");'),
        ('d.X', 'd.Cut'),
        ('Basin', 'Threshold'),
        ('basin_seeds', 'threshold_seeds'),
        ('basin cut', 'conditional threshold cut'),
        ('basin=0', 'threshold=0'),
        ('basin+=', 'threshold+='),
        ('=basin.ToString()', '=threshold.ToString()'),
        ('Family capacity:', 'Conditional family capacity:'),
        ('J=input.J,classes=length,', 'J=input.J,assumed_cycle_minimum=input.assumed_cycle_minimum,conditional_only=true,classes=length,'),
    ]
    for old, new in replacements:
        assert old in text, old
        text = text.replace(old, new)
    assert 'd.X' not in text and 'basin_seeds' not in text
    target = ROOT/'src'/'ConditionalFamilyCapacity.cs'
    target.write_text('// Derived from frozen precise family kernel; threshold is a cycle assumption.\n'+text)
    (R/'conditional-family-source-derivation.json').write_text(json.dumps({
        'source': source.name, 'source_sha256': digest(source),
        'target': target.name, 'target_sha256': digest(target),
        'replacements': replacements,
    }, indent=2)+'\n')

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--J',type=int,default=41)
    p.add_argument('--factor',type=int,default=16)
    p.add_argument('--build-sources',action='store_true')
    args=p.parse_args()
    if args.build_sources: sources()
    build(args.J,args.factor)
