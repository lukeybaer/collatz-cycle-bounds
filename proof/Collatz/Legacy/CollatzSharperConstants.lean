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

namespace CollatzSharperConstants

theorem squared_log_bound
    {t : ℝ} (ht : 2500 ≤ t) :
    (max (Real.log t + 13 / 25) (208 / 25))^2 ≤
      (167 / 20 : ℝ)^2 * t / 2500 := by
  let u : ℝ := Real.sqrt (t / 2500)
  have hratio : 1 ≤ t / 2500 := by linarith
  have hu : 1 ≤ u := by
    have h := Real.sqrt_le_sqrt hratio
    simpa [u] using h
  have hu0 : 0 < u := by linarith
  have husq : u^2 = t / 2500 := Real.sq_sqrt (by positivity)
  have htform : t = 2500 * u^2 := by nlinarith [husq]
  have hlogbase : Real.log 2500 < 783 / 100 := by
    have hfac : (2500 : ℝ) = 2^2 * 5^4 := by norm_num
    rw [hfac, Real.log_mul (by norm_num) (by norm_num), Real.log_pow, Real.log_pow]
    norm_num
    linarith [Real.log_two_lt_d9, Real.log_five_lt_d9]
  have hlogform : Real.log t = Real.log 2500 + 2 * Real.log u := by
    rw [htform, Real.log_mul (by norm_num) (pow_ne_zero _ (ne_of_gt hu0)), Real.log_pow]
    norm_num
  have hlogu : Real.log u ≤ u - 1 := Real.log_le_sub_one_of_pos hu0
  have hmain : Real.log t + 13 / 25 ≤ (167 / 20 : ℝ) * u := by
    nlinarith
  have hfixed : (208 / 25 : ℝ) ≤ (167 / 20 : ℝ) * u := by linarith
  have hmax := max_le hmain hfixed
  have hnonneg : 0 ≤ max (Real.log t + 13 / 25) (208 / 25) := by
    have h := le_max_right (Real.log t + 13 / 25) (208 / 25 : ℝ)
    linarith
  have hsquared := mul_self_le_mul_self hnonneg hmax
  nlinarith [husq]

theorem valuation_cutoff
    {t J : ℝ} (ht : 2500 ≤ t) (hJ : 100 ≤ J)
    :
    (283 / 5) * J * (max (Real.log t + 13 / 25) (208 / 25))^2 + 3 <
      (79 / 50 : ℝ) * J * t := by
  have hbound := squared_log_bound ht
  have hJ0 : 0 ≤ J := by linarith
  have hscaled := mul_le_mul_of_nonneg_left hbound (by positivity : 0 ≤ (283 / 5) * J)
  have hproduct : 250000 ≤ J * t := by nlinarith
  nlinarith

theorem two_block_loss
    {delta y k s loss J y2 : ℝ}
    (hdlo : (19 : ℝ) / 12 ≤ delta) (hdhi : delta ≤ 5 / 3)
    (hJ : 0 ≤ J) (hk : 2500 * J ≤ k) (hky : k ≤ y)
    (hs : s ≤ (79 : ℝ) / 50 * k) (hloss : 0 ≤ loss)
    (hy2 : y2 ≤ delta * y - loss + (delta - 1) * s) :
    s ≤ delta * y - J ∧ y2 ≤ delta^2 * y - (delta + 1) * J := by
  have hdelta : 0 ≤ delta := by linarith
  have hk0 : 0 ≤ k := by nlinarith
  have hdy : delta * k ≤ delta * y := mul_le_mul_of_nonneg_left hky hdelta
  have hdk : (19 : ℝ) / 12 * k ≤ delta * k :=
    mul_le_mul_of_nonneg_right hdlo hk0
  have hgap : k / 300 ≤ delta * y - s := by linarith
  have hgap0 : 0 ≤ delta * y - s := by linarith
  have hbeta : (7 : ℝ) / 12 ≤ delta - 1 := by linarith
  have hprod : 7 * k / 3600 ≤ (delta - 1) * (delta * y - s) := by
    have h1 := mul_le_mul_of_nonneg_left hgap (by norm_num : (0 : ℝ) ≤ 7 / 12)
    have h2 := mul_le_mul_of_nonneg_right hbeta hgap0
    nlinarith
  have hJdelta : (delta + 1) * J ≤ (8 : ℝ) / 3 * J := by
    exact mul_le_mul_of_nonneg_right (by linarith) hJ
  have margin : (delta + 1) * J ≤ (delta - 1) * (delta * y - s) + loss := by
    nlinarith
  constructor
  · linarith
  · nlinarith


end CollatzSharperConstants

/-- info: 'CollatzSharperConstants.squared_log_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzSharperConstants.squared_log_bound
/-- info: 'CollatzSharperConstants.valuation_cutoff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzSharperConstants.valuation_cutoff
/-- info: 'CollatzSharperConstants.two_block_loss' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzSharperConstants.two_block_loss
