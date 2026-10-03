"""Build through Lake, serializing legacy modules to bound peak memory."""
from pathlib import Path
import os
import subprocess

root = Path(__file__).resolve().parents[1]
env = dict(os.environ, LEAN_NUM_THREADS=os.environ.get('LEAN_NUM_THREADS', '2'))
for file in sorted((root / 'proof/Collatz/Legacy').glob('*.lean')):
    subprocess.run(['lake', 'build', 'Collatz.Legacy.' + file.stem], cwd=root, env=env, check=True)
subprocess.run(['lake', 'build'], cwd=root, env=env, check=True)
