import Mathlib.Basic.Real.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic

/-!
# The single-crossing core of growth-constrained majorization

This file proves the prefix-sum comparison for two finite real sequences.
The application to a sorted cycle additionally needs the elementary
crossing-edge argument and construction of the inverse-iterate extremizer.
It does not assert Collatz convergence or certify the numerical searches.
-/

namespace CollatzGrowthEnvelope

open Finset

/-- A gap between two consecutive sorted values inherits the growth
constraint from the original cyclic order. `hgap` states that no value lies
strictly inside that sorting gap. -/
theorem cyclic_gap_growth
    {m : ℕ} {phi : ℝ → ℝ} {x : ℕ → ℝ} {a b : ℝ}
    (hmono : Monotone phi) (hself : a ≤ phi a)
    (hperiod : ∀ i, x (i + m) = x i)
    (hgrowth : ∀ i, x (i + 1) ≤ phi (x i))
    (hgap : ∀ i, x i ≤ a ∨ b ≤ x i)
    (hlow : ∃ i, i < m ∧ x i ≤ a)
    (hhigh : ∃ j, j < m ∧ b ≤ x j) : b ≤ phi a := by
  by_cases hba : b ≤ a
  · exact le_trans hba hself
  have hab : a < b := lt_of_not_ge hba
  by_contra hbad
  have hphi_lt : phi a < b := lt_of_not_ge hbad
  obtain ⟨i, him, hi⟩ := hlow
  have allLow : ∀ t, x (i + t) ≤ a := by
    intro t
    induction t with
    | zero => simpa using hi
    | succ t ih =>
        rcases hgap (i + t + 1) with hnext | hnext
        · simpa [Nat.add_assoc] using hnext
        · have bound : x (i + t + 1) ≤ phi a :=
            le_trans (hgrowth (i + t)) (hmono ih)
          exact False.elim ((not_le_of_gt hphi_lt) (le_trans hnext bound))
  obtain ⟨j, hjm, hj⟩ := hhigh
  have hij : i ≤ j + m := by omega
  have last : x (j + m) ≤ a := by
    simpa [Nat.add_sub_of_le hij] using allLow (j + m - i)
  rw [hperiod j] at last
  exact (not_le_of_gt hab) (le_trans hj last)

/-- A deficit below the extremal ramp propagates forward. -/
theorem deficit_propagates
    {m : ℕ} {b : ℝ} {phi : ℝ → ℝ} {u w : ℕ → ℝ}
    (hphi : StrictMono phi)
    (hfloor : ∀ i, i < m → b ≤ u i)
    (hgrowth : ∀ i, i + 1 < m → u (i + 1) ≤ phi (u i))
    (hramp : ∀ i, i + 1 < m → b < w i → w (i + 1) = phi (w i))
    {i j : ℕ} (hij : i ≤ j) (hjm : j < m) (hdef : u i < w i) :
    u j < w j := by
  have step : ∀ t, t + 1 < m → u t < w t → u (t + 1) < w (t + 1) := by
    intro t htm ht
    rw [hramp t htm (lt_of_le_of_lt (hfloor t (by omega)) ht)]
    exact lt_of_le_of_lt (hgrowth t htm) (hphi ht)
  have distance : ∀ d, i + d < m → u (i + d) < w (i + d) := by
    intro d
    induction d with
    | zero =>
        intro _
        simpa using hdef
    | succ d ih =>
        intro hdm
        have previous := ih (by omega)
        simpa [Nat.add_assoc] using step (i + d) (by omega) previous
  have hdecomp : i + (j - i) = j := Nat.add_sub_of_le hij
  simpa [hdecomp] using distance (j - i) (by omega)

/-- Equal total mass and the extremal ramp force every increasing-prefix
sum of `u` to be at least the corresponding prefix sum of `w`.

The theorem does not require that `phi` be affine, convex, concave, or
differentiable. It only uses strict monotonicity, a floor for `u`, the
one-sided growth constraint, and equality on the active part of the ramp.
-/
theorem extremal_prefix_sum
    {m : ℕ} {b : ℝ} {phi : ℝ → ℝ} {u w : ℕ → ℝ}
    (hphi : StrictMono phi)
    (hfloor : ∀ i, i < m → b ≤ u i)
    (hgrowth : ∀ i, i + 1 < m → u (i + 1) ≤ phi (u i))
    (hramp : ∀ i, i + 1 < m → b < w i → w (i + 1) = phi (w i))
    (htotal : (∑ i ∈ range m, u i) = ∑ i ∈ range m, w i)
    (k : ℕ) (hkm : k ≤ m) :
    (∑ i ∈ range k, w i) ≤ ∑ i ∈ range k, u i := by
  classical
  by_contra hnot
  have hprefix : (∑ i ∈ range k, u i) < ∑ i ∈ range k, w i :=
    lt_of_not_ge hnot
  have witness : ∃ i ∈ range k, u i < w i := by
    by_contra hnone
    have pointwise : ∀ i ∈ range k, w i ≤ u i := by
      intro i hi
      exact le_of_not_gt (fun hlt => hnone ⟨i, hi, hlt⟩)
    exact (not_le_of_gt hprefix) (sum_le_sum pointwise)
  obtain ⟨i, hi, hdef⟩ := witness
  have hik : i < k := mem_range.mp hi
  have tail : (∑ t ∈ range (m - k), u (k + t)) ≤
      ∑ t ∈ range (m - k), w (k + t) := by
    apply sum_le_sum
    intro t ht
    have htm : t < m - k := mem_range.mp ht
    exact le_of_lt (deficit_propagates hphi hfloor hgrowth hramp
      (i := i) (j := k + t) (by omega) (by omega) hdef)
  have huSplit : (∑ i ∈ range m, u i) =
      (∑ i ∈ range k, u i) + ∑ t ∈ range (m - k), u (k + t) := by
    simpa [Nat.add_sub_of_le hkm] using sum_range_add u k (m - k)
  have hwSplit : (∑ i ∈ range m, w i) =
      (∑ i ∈ range k, w i) + ∑ t ∈ range (m - k), w (k + t) := by
    simpa [Nat.add_sub_of_le hkm] using sum_range_add w k (m - k)
  have contradiction := add_lt_add_of_lt_of_le hprefix tail
  rw [← huSplit, ← hwSplit] at contradiction
  exact (ne_of_lt contradiction) htotal

end CollatzGrowthEnvelope

/-- info: 'CollatzGrowthEnvelope.deficit_propagates' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzGrowthEnvelope.deficit_propagates
/-- info: 'CollatzGrowthEnvelope.extremal_prefix_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzGrowthEnvelope.extremal_prefix_sum
/-- info: 'CollatzGrowthEnvelope.cyclic_gap_growth' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzGrowthEnvelope.cyclic_gap_growth
