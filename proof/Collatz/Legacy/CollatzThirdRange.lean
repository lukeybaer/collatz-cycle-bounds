import Mathlib.Tactic

/-! Supporting parameter lemmas for the additional interpolation range.
The published p-adic theorem and logarithm enclosures remain external inputs. -/
namespace CollatzThirdRange

theorem interpolation_margin :
    (0 : ℝ) < 9*5*(2079/1000)-9*(4891/1000)-3/10
      -6*((81/40)*(1099/500)+(3013/1000)*(525099/437500)) := by
  norm_num

theorem rational_loss_margin :
    (158497/100000 : ℝ)+1 <
      (158496/100000-1)*(105*(158496/100000)-162) := by
  norm_num

theorem first_range_local_loss {delta y s loss J y2 : ℝ}
    (hdlo : (158496 : ℝ)/100000 ≤ delta)
    (hdhi : delta ≤ 158497/100000)
    (hJ : 0 ≤ J) (hy : 105*J ≤ y) (hs : s ≤ 162*J)
    (hloss : 0 ≤ loss) (hy2 : y2 ≤ delta*y-loss+(delta-1)*s) :
    s ≤ delta*y-J ∧ y2 ≤ delta^2*y-(delta+1)*J := by
  have hd0 : 0 ≤ delta := by linarith
  have h1 := mul_le_mul_of_nonneg_left hy hd0
  have h2 := mul_le_mul_of_nonneg_right hdlo hJ
  have hgap : (2763 : ℝ)/625*J ≤ delta*y-s := by nlinarith
  have hgap0 : 0 ≤ delta*y-s := by nlinarith
  have hb : (1828 : ℝ)/3125 ≤ delta-1 := by linarith
  have h3 := mul_le_mul_of_nonneg_left hgap (by norm_num : (0 : ℝ) ≤ 1828/3125)
  have h4 := mul_le_mul_of_nonneg_right hb hgap0
  have hprod : ((158497 : ℝ)/100000+1)*J ≤ (delta-1)*(delta*y-s) := by
    nlinarith
  have h5 := mul_le_mul_of_nonneg_right hdhi hJ
  constructor
  · linarith
  · nlinarith

theorem fractional_restart_constant :
    (105 : ℝ)/131 < (81/100)*(99/100) ∧
      105-(12/7)*(101/100) > 103 := by
  norm_num

end CollatzThirdRange

/-- info: 'CollatzThirdRange.interpolation_margin' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzThirdRange.interpolation_margin
/-- info: 'CollatzThirdRange.rational_loss_margin' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzThirdRange.rational_loss_margin
/-- info: 'CollatzThirdRange.first_range_local_loss' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzThirdRange.first_range_local_loss
/-- info: 'CollatzThirdRange.fractional_restart_constant' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzThirdRange.fractional_restart_constant
