"""Create a separate, finer exact log grid and a scoped experimental kernel."""
from pathlib import Path
from fractions import Fraction as F
import json, hashlib
from exact_intervals import L2LO, L2HI

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / 'results'
GRID = 4096
SCALE = 10**9

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def logarithm(z, terms):
    power = z
    total = F(0)
    for t in range(terms):
        total += 2 * power / (2 * t + 1)
        power *= z*z
    return total, total + 2 * power / ((2*terms+1) * (1-z*z))

rows = []
for j in range(GRID+1):
    lo, hi = logarithm(F(j, 2*GRID+j), 40)
    lower = (lo/L2HI*SCALE).__floor__()
    upper = (hi/L2LO*SCALE).__ceil__()
    if j in (0, GRID):
        lower = upper = j*SCALE//GRID
    rows.append({'lower': lower, 'upper': upper})
    if j%1024 == 0:
        print('Built grid entry', j, flush=True)
table = {'grid': GRID, 'scale': SCALE, 'bounds': rows,
         'method': 'Exact direct 40-term positive atanh series with geometric tail'}
tablepath = R / 'log2-mantissa-table-4096.json'
tablepath.write_text(json.dumps(table, indent=2)+'\n')

# Check every entry using a different logarithm argument and twice as many terms.
l2lo, l2hi = logarithm(F(1, 3), 80)
for j, row in enumerate(rows):
    if j in (0, GRID):
        assert row['lower'] == row['upper'] == j*SCALE//GRID
        continue
    clo, chi = logarithm(F(GRID-j, 3*GRID+j), 80)
    lower, upper = (l2lo-chi)/l2hi, (l2hi-clo)/l2lo
    assert F(row['lower'], SCALE) <= lower <= upper <= F(row['upper'], SCALE)
receipt = {'status': 'passed', 'entries': GRID+1,
           'method': 'Independent complementary logarithm with exact 80-term series',
           'table_sha256': sha(tablepath), 'source_sha256': sha(Path(__file__))}
(R/'log2-mantissa-table-4096-audit.json').write_text(json.dumps(receipt, indent=2)+'\n')

original = ROOT/'src'/'HighNonlinearFamilyCapacity.cs'
target = ROOT/'src'/'FineHighNonlinearFamilyCapacity.cs'
code = original.read_text()
changes = [('CollatzHighNonlinearFamilies','CollatzFineHighNonlinearFamilies',1),
           ('new long[257]','new long[4097]',2),
           ('GetInt32()!=256','GetInt32()!=4096',1),
           ('position!=257','position!=4097',1),
           ('(n-unit)<<8','(n-unit)<<12',1),
           ('index>=256','index>=4096',1)]
for before, after, count in changes:
    assert code.count(before) == count, before
    code = code.replace(before, after)
target.write_text(code)
derivation = {'status': 'generated', 'original_source_sha256': sha(original),
              'generated_source_sha256': sha(target), 'changes': changes,
              'table_sha256': sha(tablepath), 'generator_sha256': sha(Path(__file__))}
(R/'fine-high-nonlinear-source-derivation.json').write_text(json.dumps(derivation, indent=2)+'\n')
print('PASSED 4097 independent log checks; separate experimental kernel generated.', flush=True)
