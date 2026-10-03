# Active Lean project

From the repository root, with Lean managed by elan:

```sh
lake exe cache get
python scripts/build_lean.py
lake build
```

`build_lean.py` uses Lake to build the 21 archived modules sequentially before the root. This bounds peak memory; a fresh parallel build imports Mathlib in many compiler processes. The standard root `lake build` imports every active module. CI performs the same build in a fresh Linux checkout. The compiler version and Mathlib revision are pinned in `lean-toolchain`, `lakefile.toml`, and `lake-manifest.json`.

## Main entry point

Read `Collatz/Connected.lean`, theorem `Collatz.block_growth_of_local_loss`.

It takes a natural-number `BlockOrbit` and the explicitly stated `LocalLossCertificate`, and proves both inequalities in manuscript Theorem 1. `Blocks.lean` derives elementary logarithmic bounds from the exact block identities. `Connected.lean` connects them to rounding, restart induction and the 32-step virtual warmup.

**The local analytic certificate is still an explicit hypothesis.** Its written derivation invokes Bugeaud's published theorem. Neither that theorem nor the whole specialization is formalized here. A hypothesis appearing in a theorem's type does not appear as a new axiom in `#print axioms`; the guarded axiom list is therefore not a claim that all mathematical inputs have been discharged.

The arithmetic block representation is not yet formally proved equivalent to iteration of a separately defined Collatz function. The cycle deductions, external convergence verification and exhaustive C# search are also outside the connected formal theorem.

## Historical modules

`Collatz/Legacy` contains copies of the 21 original modules. The 103 originally selected axiom printouts now use `#guard_msgs`, so a changed dependency list fails compilation. The original files and saved compiler transcripts remain unchanged in `formal/` because they are part of the frozen manifest. The copies preserve the original namespace names.

The new top-level theorem also has a guarded axiom report. Allowed dependencies are `propext`, `Classical.choice`, and `Quot.sound`. There are no intended `sorry`, `admit`, or custom axiom declarations in the active project. The build and guard checks, not this sentence, are the evidence.

This addresses the disconnected-lemma issue by supplying a checkable chain and an honest formal boundary. It does not turn the entire paper into a fully formal proof.
