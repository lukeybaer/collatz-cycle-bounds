import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Topology.Algebra.Monoid
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic

/-!
An exact common cap exists for any target mass between the constant floor
and the original total. Capping also preserves a cyclic growth constraint.
-/

namespace CollatzCommonCap

open Finset Set

noncomputable def capSum (z : ℕ → ℝ) (m : ℕ) (t : ℝ) : ℝ :=
  ∑ i ∈ range m, min (z i) t

theorem capSum_continuous (z : ℕ → ℝ) (m : ℕ) :
    Continuous (capSum z m) := by
  unfold capSum
  exact continuous_finsetSum _ (fun _ _ => continuous_const.min continuous_id)

theorem exists_common_cap {z : ℕ → ℝ} {m : ℕ} {b K : ℝ}
    (hbase : ∀ i, i < m → b ≤ z i)
    (hlo : (m : ℝ) * b ≤ K) (hhi : K ≤ ∑ i ∈ range m, z i) :
    ∃ t, b ≤ t ∧ capSum z m t = K := by
  let M : ℝ := max b (∑ i ∈ range m, |z i|)
  have hbM : b ≤ M := le_max_left _ _
  have hzM : ∀ i, i < m → z i ≤ M := by
    intro i hi
    have hsum : |z i| ≤ ∑ j ∈ range m, |z j| :=
      single_le_sum (fun j _ => abs_nonneg (z j)) (mem_range.mpr hi)
    exact le_trans (le_abs_self _) (le_trans hsum (le_max_right _ _))
  have hbval : capSum z m b = (m : ℝ)*b := by
    unfold capSum
    calc
      (∑ i ∈ range m, min (z i) b) = ∑ _i ∈ range m, b := by
        apply sum_congr rfl
        intro i hi
        exact min_eq_right (hbase i (mem_range.mp hi))
      _ = (m : ℝ)*b := by simp
  have hMval : capSum z m M = ∑ i ∈ range m, z i := by
    unfold capSum
    apply sum_congr rfl
    intro i hi
    exact min_eq_left (hzM i (mem_range.mp hi))
  have hbetween : K ∈ Icc (capSum z m b) (capSum z m M) := by
    rw [hbval,hMval]
    exact ⟨hlo,hhi⟩
  obtain ⟨t,ht,hval⟩ := intermediate_value_Icc hbM
    (capSum_continuous z m).continuousOn hbetween
  exact ⟨t,ht.1,hval⟩

theorem mass_preserving_growth_cap {z : ℕ → ℝ} {growth : ℝ → ℝ}
    {m : ℕ} {b K : ℝ}
    (hbase : ∀ i, b ≤ z i)
    (hlo : (m : ℝ)*b ≤ K) (hhi : K ≤ ∑ i ∈ range m, z i)
    (hg : ∀ x, b ≤ x → x ≤ growth x)
    (hz : ∀ i, z (i+1) ≤ growth (z i)) :
    ∃ capped : ℕ → ℝ,
      (∀ i, b ≤ capped i ∧ capped i ≤ z i) ∧
      (∑ i ∈ range m, capped i) = K ∧
      (∀ i, capped (i+1) ≤ growth (capped i)) := by
  obtain ⟨t,ht,hmass⟩ := exists_common_cap (fun i _ => hbase i) hlo hhi
  refine ⟨fun i => min (z i) t, ?_, hmass, ?_⟩
  · intro i
    exact ⟨le_min (hbase i) ht, min_le_left _ _⟩
  · intro i
    change min (z (i+1)) t ≤ growth (min (z i) t)
    by_cases hi : z i ≤ t
    · rw [min_eq_left hi]
      exact le_trans (min_le_left _ _) (hz i)
    · rw [min_eq_right (le_of_not_ge hi)]
      exact le_trans (min_le_right _ _) (hg t ht)

end CollatzCommonCap

/-- info: 'CollatzCommonCap.capSum_continuous' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzCommonCap.capSum_continuous
/-- info: 'CollatzCommonCap.exists_common_cap' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzCommonCap.exists_common_cap
/-- info: 'CollatzCommonCap.mass_preserving_growth_cap' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzCommonCap.mass_preserving_growth_cap
