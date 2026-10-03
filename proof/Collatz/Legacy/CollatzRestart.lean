import Mathlib.Basic.Real.Basic
import Mathlib.Tactic

/-!
# Bounded block restarts

This verifies the abstract induction used to turn one- or two-block local
estimates into a global envelope. The local Collatz and p-adic estimates
are hypotheses, not conclusions, of this formalization.
-/

namespace CollatzRestart

/-- At each index, either the height itself has reached a certified restart
endpoint, or the index is the single intermediate point of a two-step
restart. In the latter case the run length and the next endpoint are bounded. -/
theorem endpoint_or_intermediate
    {G : ℝ → ℝ} {y k v : ℕ → ℝ}
    (hmono : Monotone G)
    (hv : ∀ n, v (n + 1) = G (v n))
    (hzero : y 0 ≤ v 0)
    (hlocal : ∀ n, y (n + 1) ≤ G (y n) ∨
      (k (n + 1) ≤ G (y n) ∧ y (n + 2) ≤ G (G (y n)))) :
    ∀ n, y n ≤ v n ∨
      (0 < n ∧ y (n - 1) ≤ v (n - 1) ∧ k n ≤ v n ∧
        y (n + 1) ≤ v (n + 1)) := by
  intro n
  induction n with
  | zero => exact Or.inl hzero
  | succ n ih =>
      rcases ih with hend | hinter
      · rcases hlocal n with hone | htwo
        · apply Or.inl
          rw [hv n]
          exact le_trans hone (hmono hend)
        · apply Or.inr
          refine ⟨by omega, ?_, ?_, ?_⟩
          · simpa using hend
          · rw [hv n]
            exact le_trans htwo.1 (hmono hend)
          · rw [hv (n + 1), hv n]
            exact le_trans htwo.2 (hmono (hmono hend))
      · exact Or.inl hinter.2.2.2

/-- Every run length is bounded by the virtual orbit, even when the actual
height at an intermediate point exceeds that orbit. -/
theorem run_bound
    {G : ℝ → ℝ} {y k v : ℕ → ℝ}
    (hmono : Monotone G)
    (hv : ∀ n, v (n + 1) = G (v n))
    (hzero : y 0 ≤ v 0)
    (hky : ∀ n, k n ≤ y n)
    (hlocal : ∀ n, y (n + 1) ≤ G (y n) ∨
      (k (n + 1) ≤ G (y n) ∧ y (n + 2) ≤ G (G (y n)))) :
    ∀ n, k n ≤ v n := by
  intro n
  rcases endpoint_or_intermediate hmono hv hzero hlocal n with hend | hinter
  · exact le_trans (hky n) hend
  · exact hinter.2.2.1

/-- Actual heights require only the elementary multiplicative bound for
one extra block. No assertion that the actual orbit increases is needed. -/
theorem height_bound
    {G : ℝ → ℝ} {y k v : ℕ → ℝ} {delta : ℝ}
    (hdelta : 0 ≤ delta)
    (hmono : Monotone G)
    (hupper : ∀ x, G x ≤ delta * x)
    (hv : ∀ n, v (n + 1) = G (v n))
    (hzero : y 0 ≤ v 0)
    (helementary : ∀ n, y (n + 1) ≤ delta * y n)
    (hlocal : ∀ n, y (n + 1) ≤ G (y n) ∨
      (k (n + 1) ≤ G (y n) ∧ y (n + 2) ≤ G (G (y n)))) :
    ∀ n, y (n + 1) ≤ delta * v n := by
  intro n
  rcases endpoint_or_intermediate hmono hv hzero hlocal (n + 1) with hend | hinter
  · rw [hv n] at hend
    exact le_trans hend (hupper (v n))
  · have previous : y n ≤ v n := by simpa using hinter.2.1
    exact le_trans (helementary n) (mul_le_mul_of_nonneg_left previous hdelta)

end CollatzRestart

/-- info: 'CollatzRestart.endpoint_or_intermediate' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzRestart.endpoint_or_intermediate
/-- info: 'CollatzRestart.run_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzRestart.run_bound
/-- info: 'CollatzRestart.height_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzRestart.height_bound
