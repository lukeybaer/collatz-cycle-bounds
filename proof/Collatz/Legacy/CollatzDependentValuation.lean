import Mathlib.Data.Nat.PadicValNat
import Mathlib.Tactic

/-!
The elementary valuation estimate for the multiplicatively dependent case.
Rational unique factorization reduces positive dependent rational arguments
to two powers of three times a common odd integer. That reduction remains
in the written proof; the valuation estimate below is checked here.
-/

namespace CollatzDependentValuation

theorem three_pow_mod_eight (r : ℕ) : 3^r % 8 = 1 ∨ 3^r % 8 = 3 := by
  induction r with
  | zero => norm_num
  | succ r ih =>
      rcases ih with h | h
      · right
        norm_num [pow_succ, Nat.mul_mod, h]
      · left
        norm_num [pow_succ, Nat.mul_mod, h]

theorem odd_multiple_sum_not_eight_dvd {u p q : ℕ} (hu : u % 2 = 1) :
    ¬ 8 ∣ u * (3^p + 3^q) := by
  have hp := three_pow_mod_eight p
  have hq := three_pow_mod_eight q
  have hlt : u % 8 < 8 := Nat.mod_lt _ (by norm_num)
  have hu8 : (u % 8) % 2 = 1 := by omega
  rw [Nat.dvd_iff_mod_eq_zero]
  rcases hp with hp | hp <;> rcases hq with hq | hq <;>
    interval_cases h : u % 8 <;>
    norm_num [Nat.mul_mod, Nat.add_mod, hp, hq, h] at *

theorem dependent_valuation_bound {u p q : ℕ} (hu : u % 2 = 1) :
    padicValNat 2 (u * (3^p + 3^q)) ≤ 2 := by
  have hu0 : u ≠ 0 := by omega
  have hn : u * (3^p + 3^q) ≠ 0 := by positivity
  have hnot := odd_multiple_sum_not_eight_dvd (p := p) (q := q) hu
  have hiff := Nat.pow_dvd_iff_le_padicValNat (p := 2) (k := 3)
    (by norm_num) hn
  norm_num at hiff
  omega

end CollatzDependentValuation

/-- info: 'CollatzDependentValuation.three_pow_mod_eight' depends on axioms: [propext] -/
#guard_msgs in
#print axioms CollatzDependentValuation.three_pow_mod_eight
/-- info: 'CollatzDependentValuation.odd_multiple_sum_not_eight_dvd' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzDependentValuation.odd_multiple_sum_not_eight_dvd
/-- info: 'CollatzDependentValuation.dependent_valuation_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzDependentValuation.dependent_valuation_bound
