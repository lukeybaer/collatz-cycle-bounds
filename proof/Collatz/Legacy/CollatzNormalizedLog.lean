import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# The normalized logarithm cutoff

An elementary square-root comparison proves the all-parameter cutoff
without differentiation. The p-adic theorem itself is an external input.
The logarithmic constant follows from mathlib's proved bound for log(2).
-/

namespace CollatzNormalizedLog

theorem squared_log_bound
    {t : ℝ} (ht : 3600 ≤ t) :
    (max (Real.log t + 43 / 100) (42 / 5))^2 ≤
      (883 / 100 : ℝ)^2 * t / 3600 := by
  have hlog2 : Real.log 2 ≤ 7 / 10 := by linarith [Real.log_two_lt_d9]
  let u : ℝ := Real.sqrt (t / 3600)
  have hratio : 1 ≤ t / 3600 := by linarith
  have hu : 1 ≤ u := by
    have h := Real.sqrt_le_sqrt hratio
    simpa [u] using h
  have hu0 : 0 < u := by linarith
  have husq : u^2 = t / 3600 := Real.sq_sqrt (by positivity)
  have htform : t = 3600 * u^2 := by nlinarith [husq]
  have hlogbase : Real.log 3600 < 42 / 5 := by
    have hsmall : Real.log 3600 < Real.log ((2 : ℝ)^12) :=
      Real.log_lt_log (by norm_num) (by norm_num)
    rw [Real.log_pow] at hsmall
    norm_num at hsmall
    linarith
  have hlogform : Real.log t = Real.log 3600 + 2 * Real.log u := by
    rw [htform, Real.log_mul (by norm_num) (pow_ne_zero _ (ne_of_gt hu0)), Real.log_pow]
    norm_num
  have hlogu : Real.log u ≤ u - 1 := Real.log_le_sub_one_of_pos hu0
  have hmain : Real.log t + 43 / 100 ≤ (883 / 100 : ℝ) * u := by
    nlinarith
  have hfixed : (42 / 5 : ℝ) ≤ (883 / 100 : ℝ) * u := by linarith
  have hmax := max_le hmain hfixed
  have hnonneg : 0 ≤ max (Real.log t + 43 / 100) (42 / 5) := by
    have h := le_max_right (Real.log t + 43 / 100) (42 / 5 : ℝ)
    linarith
  have hsquared := mul_self_le_mul_self hnonneg hmax
  nlinarith [husq]

theorem valuation_cutoff
    {t J : ℝ} (ht : 3600 ≤ t) (hJ : 50 ≤ J)
    :
    68 * J * (max (Real.log t + 43 / 100) (42 / 5))^2 + 3 <
      (3 / 2 : ℝ) * J * t := by
  have hbound := squared_log_bound ht
  have hJ0 : 0 ≤ J := by linarith
  have hscaled := mul_le_mul_of_nonneg_left hbound (by positivity : 0 ≤ 68 * J)
  have hproduct : 180000 ≤ J * t := by nlinarith
  nlinarith

end CollatzNormalizedLog

/-- info: 'CollatzNormalizedLog.squared_log_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzNormalizedLog.squared_log_bound
/-- info: 'CollatzNormalizedLog.valuation_cutoff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzNormalizedLog.valuation_cutoff
