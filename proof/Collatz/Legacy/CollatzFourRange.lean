import Mathlib.Tactic

/-! Exact supporting inequalities for the four-range interpolation argument.
The external transcendence theorem and its logarithmic hypotheses remain
written mathematical inputs. -/
namespace CollatzFourRange

private noncomputable def U : ℝ := (12/7)*(2001/2000)*(1733/2500)

theorem first_margin : (0 : ℝ) <
    4*(31/5)*(2772/1000)-(31/5)*(4117/1000)-18/1000
      -5*((15551/13500)*(1099/250)+(15551/5178)*U) := by
  norm_num [U]

theorem second_margin : (0 : ℝ) <
    4*(63/10)*(2772/1000)-(63/10)*(417/100)-18/1000
      -5*((3503/3000)*(1099/250)+(10509/3502)*U) := by
  norm_num [U]

theorem third_margin : (0 : ℝ) <
    4*(67/10)*(2772/1000)-(67/10)*(554/125)-18/1000
      -5*((3353/3000)*(1099/250)+(16765/5028)*U) := by
  norm_num [U]

theorem fourth_margin : (0 : ℝ) <
    4*(42/5)*(2772/1000)-(42/5)*(1261/250)-18/1000
      -5*((1401/1000)*(1099/250)+(7005/2101)*U) := by
  norm_num [U]

theorem numeric_gaps :
    (11 : ℝ)/2 < (158496/100000)*82-124 ∧
    (11 : ℝ)/2 < (158496/100000)*83-126 ∧
    (11 : ℝ)/2 < (158496/100000)*89-134 ∧
    (11 : ℝ)/2 < (158496/100000)*110-168 := by
  norm_num

theorem local_loss {delta y s loss J y2 : ℝ}
    (hd : (158496 : ℝ)/100000 ≤ delta) (hJ : 0 ≤ J)
    (hgap : (11 : ℝ)/2*J ≤ delta*y-s)
    (hloss : 0 ≤ loss) (hy2 : y2 ≤ delta*y-loss+(delta-1)*s) :
    s ≤ delta*y-J ∧ y2 ≤ delta^2*y-(16/5)*J := by
  have hgap0 : 0 ≤ delta*y-s := by nlinarith
  have hb : (58496 : ℝ)/100000 ≤ delta-1 := by linarith
  have h1 := mul_le_mul_of_nonneg_left hgap (by norm_num : (0 : ℝ) ≤ 58496/100000)
  have h2 := mul_le_mul_of_nonneg_right hb hgap0
  have hp : (16 : ℝ)/5*J ≤ (delta-1)*(delta*y-s) := by nlinarith
  constructor
  · linarith
  · nlinarith

theorem ratio_decreases {a b x J J0 : ℝ}
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hx : 0 < x)
    (hJ : J0 ≤ J) (hden : 0 < x*J0-1) :
    (a*J+b)/(x*J-1) ≤ (a*J0+b)/(x*J0-1) := by
  have hprod := mul_nonneg (le_of_lt hx) (sub_nonneg.mpr hJ)
  have hdenJ : 0 < x*J-1 := by nlinarith
  apply (div_le_div_iff₀ hdenJ hden).2
  have hcoef : 0 ≤ a+b*x := by positivity
  have h := mul_nonneg hcoef (sub_nonneg.mpr hJ)
  nlinarith

theorem restart_constants :
    (82 : ℝ)/83 < 99/100 ∧ (2 : ℕ)^52 < 3^33 ∧
    (58496 : ℝ)/100000*(11/2) > 16/5 ∧
    (2 : ℕ)^18 > 2000*82 := by
  norm_num

end CollatzFourRange

/-- info: 'CollatzFourRange.first_margin' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzFourRange.first_margin
/-- info: 'CollatzFourRange.second_margin' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzFourRange.second_margin
/-- info: 'CollatzFourRange.third_margin' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzFourRange.third_margin
/-- info: 'CollatzFourRange.fourth_margin' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzFourRange.fourth_margin
/-- info: 'CollatzFourRange.numeric_gaps' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzFourRange.numeric_gaps
/-- info: 'CollatzFourRange.local_loss' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzFourRange.local_loss
/-- info: 'CollatzFourRange.ratio_decreases' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzFourRange.ratio_decreases
/-- info: 'CollatzFourRange.restart_constants' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzFourRange.restart_constants
