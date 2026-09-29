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

namespace CollatzParityConstants

theorem squared_log_bound
    {t : ℝ} (ht : 1000 ≤ t) :
    (max (Real.log t + 13 / 25) (208 / 25))^2 ≤
      (208 / 25 : ℝ)^2 * t / 1000 := by
  let u : ℝ := Real.sqrt (t / 1000)
  have hratio : 1 ≤ t / 1000 := by linarith
  have hu : 1 ≤ u := by
    have h := Real.sqrt_le_sqrt hratio
    simpa [u] using h
  have hu0 : 0 < u := by linarith
  have husq : u^2 = t / 1000 := Real.sq_sqrt (by positivity)
  have htform : t = 1000 * u^2 := by nlinarith [husq]
  have hlogbase : Real.log 1000 < 39 / 5 := by
    have hmono : Real.log (1000 : ℝ) < Real.log (2^10 : ℝ) :=
      Real.log_lt_log (by norm_num) (by norm_num)
    rw [Real.log_pow] at hmono
    norm_num at hmono
    linarith [Real.log_two_lt_d9]
  have hlogform : Real.log t = Real.log 1000 + 2 * Real.log u := by
    rw [htform, Real.log_mul (by norm_num) (pow_ne_zero _ (ne_of_gt hu0)), Real.log_pow]
    norm_num
  have hlogu : Real.log u ≤ u - 1 := Real.log_le_sub_one_of_pos hu0
  have hmain : Real.log t + 13 / 25 ≤ (208 / 25 : ℝ) * u := by
    nlinarith
  have hfixed : (208 / 25 : ℝ) ≤ (208 / 25 : ℝ) * u := by linarith
  have hmax := max_le hmain hfixed
  have hnonneg : 0 ≤ max (Real.log t + 13 / 25) (208 / 25) := by
    have h := le_max_right (Real.log t + 13 / 25) (208 / 25 : ℝ)
    linarith
  have hsquared := mul_self_le_mul_self hnonneg hmax
  nlinarith [husq]

theorem valuation_cutoff
    {t J : ℝ} (ht : 1000 ≤ t) (hJ : 100 ≤ J)
    :
    (114 / 5) * J * (max (Real.log t + 13 / 25) (208 / 25))^2 + 3 <
      (79 / 50 : ℝ) * J * t := by
  have hbound := squared_log_bound ht
  have hJ0 : 0 ≤ J := by linarith
  have hscaled := mul_le_mul_of_nonneg_left hbound (by positivity : 0 ≤ (114 / 5) * J)
  have hproduct : 100000 ≤ J * t := by nlinarith
  nlinarith

theorem two_block_loss
    {delta y k s loss J y2 : ℝ}
    (hdlo : (15849 : ℝ) / 10000 ≤ delta) (hdhi : delta ≤ 8 / 5)
    (hJ : 0 ≤ J) (hk : 1000 * J ≤ k) (hky : k ≤ y)
    (hs : s ≤ (79 : ℝ) / 50 * k) (hloss : 0 ≤ loss)
    (hy2 : y2 ≤ delta * y - loss + (delta - 1) * s) :
    s ≤ delta * y - J ∧ y2 ≤ delta^2 * y - (delta + 1) * J := by
  have hdelta : 0 ≤ delta := by linarith
  have hk0 : 0 ≤ k := by nlinarith
  have hdy : delta * k ≤ delta * y := mul_le_mul_of_nonneg_left hky hdelta
  have hdk : (15849 : ℝ) / 10000 * k ≤ delta * k :=
    mul_le_mul_of_nonneg_right hdlo hk0
  have hgap : 49 * k / 10000 ≤ delta * y - s := by linarith
  have hgap0 : 0 ≤ delta * y - s := by linarith
  have hbeta : (5849 : ℝ) / 10000 ≤ delta - 1 := by linarith
  have hprod : 286601 * k / 100000000 ≤ (delta - 1) * (delta * y - s) := by
    have h1 := mul_le_mul_of_nonneg_left hgap (by norm_num : (0 : ℝ) ≤ 5849 / 10000)
    have h2 := mul_le_mul_of_nonneg_right hbeta hgap0
    nlinarith
  have hJdelta : (delta + 1) * J ≤ (13 : ℝ) / 5 * J := by
    exact mul_le_mul_of_nonneg_right (by linarith) hJ
  have margin : (delta + 1) * J ≤ (delta - 1) * (delta * y - s) + loss := by
    nlinarith
  constructor
  · linarith
  · nlinarith


theorem fractional_two_block_loss
    {delta epsilon y J : ℝ}
    (hdlo : 0 ≤ delta) (hdhi : delta ≤ 8 / 5)
    (hy : 0 ≤ y) (hJ : 0 ≤ J)
    (hloss : epsilon * y ≤ (81 : ℝ) / 100 * J) :
    delta^2 * y - (delta + 1) * J ≤ (delta - epsilon)^2 * y := by
  have htwice := mul_le_mul_of_nonneg_left hloss (by positivity : 0 ≤ 2 * delta)
  have hcoef : (81 : ℝ) / 50 * delta ≤ delta + 1 := by linarith
  have hcoefJ := mul_le_mul_of_nonneg_right hcoef hJ
  have hpositive : 0 ≤ epsilon^2 * y := mul_nonneg (sq_nonneg epsilon) hy
  nlinarith


theorem delta_lower : (15849 : ℝ)/10000 < Real.log 3 / Real.log 2 := by
  have h2 : 0 < Real.log 2 := by linarith [Real.log_two_gt_d9]
  apply (lt_div_iff₀ h2).2
  linarith [Real.log_two_lt_d9, Real.log_three_gt_d9]

end CollatzParityConstants

#print axioms CollatzParityConstants.squared_log_bound
#print axioms CollatzParityConstants.valuation_cutoff
#print axioms CollatzParityConstants.two_block_loss
#print axioms CollatzParityConstants.fractional_two_block_loss

#print axioms CollatzParityConstants.delta_lower
