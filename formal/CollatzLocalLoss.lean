import Mathlib.Basic.Real.Basic
import Mathlib.Tactic

/-!
# Algebra behind the improved exponential base

The p-adic theorem is not formalized here. The first lemma assumes its
derived run-length bound and verifies the local restart algebra. The
second verifies conversion of an additive local loss into a constant
fractional loss, including the second block.
-/

namespace CollatzLocalLoss

theorem two_block_loss
    {delta y k s loss J y2 : ℝ}
    (hdlo : (19 : ℝ) / 12 ≤ delta) (hdhi : delta ≤ 5 / 3)
    (hJ : 0 ≤ J) (hk : 3600 * J ≤ k) (hky : k ≤ y)
    (hs : s ≤ (3 : ℝ) / 2 * k) (hloss : 0 ≤ loss)
    (hy2 : y2 ≤ delta * y - loss + (delta - 1) * s) :
    s ≤ delta * y - J ∧ y2 ≤ delta^2 * y - (delta + 1) * J := by
  have hdelta : 0 ≤ delta := by linarith
  have hk0 : 0 ≤ k := by nlinarith
  have hdy : delta * k ≤ delta * y := mul_le_mul_of_nonneg_left hky hdelta
  have hdk : (19 : ℝ) / 12 * k ≤ delta * k :=
    mul_le_mul_of_nonneg_right hdlo hk0
  have hgap : k / 12 ≤ delta * y - s := by linarith
  have hgap0 : 0 ≤ delta * y - s := by linarith
  have hbeta : (1 : ℝ) / 2 ≤ delta - 1 := by linarith
  have hprod : k / 24 ≤ (delta - 1) * (delta * y - s) := by
    have h1 := mul_le_mul_of_nonneg_left hgap (by norm_num : (0 : ℝ) ≤ 1 / 2)
    have h2 := mul_le_mul_of_nonneg_right hbeta hgap0
    nlinarith
  have hJdelta : (delta + 1) * J ≤ (8 : ℝ) / 3 * J := by
    exact mul_le_mul_of_nonneg_right (by linarith) hJ
  have margin : (delta + 1) * J ≤ (delta - 1) * (delta * y - s) + loss := by
    nlinarith
  constructor
  · linarith
  · nlinarith

theorem fractional_two_block_loss
    {delta epsilon y J : ℝ}
    (hdlo : 0 ≤ delta) (hdhi : delta ≤ 5 / 3)
    (hy : 0 ≤ y) (hJ : 0 ≤ J)
    (hloss : epsilon * y ≤ (4 : ℝ) / 5 * J) :
    delta^2 * y - (delta + 1) * J ≤ (delta - epsilon)^2 * y := by
  have htwice := mul_le_mul_of_nonneg_left hloss (by positivity : 0 ≤ 2 * delta)
  have hcoef : (8 : ℝ) / 5 * delta ≤ delta + 1 := by linarith
  have hcoefJ := mul_le_mul_of_nonneg_right hcoef hJ
  have hpositive : 0 ≤ epsilon^2 * y := mul_nonneg (sq_nonneg epsilon) hy
  nlinarith

end CollatzLocalLoss

#print axioms CollatzLocalLoss.two_block_loss
#print axioms CollatzLocalLoss.fractional_two_block_loss
