import Mathlib.Tactic

/-! Supporting identities and parameter bounds for the fourth-power argument.
The external p-adic theorem is not formalized here. -/
namespace CollatzFourthPower

theorem power_identity {k r H : ℕ} (h : k+r=4*H) :
    (3 : ℕ)^k*3^r=81^H := by
  rw [← pow_add,h,pow_mul]
  norm_num

theorem signed_form_identity {a b : ℚ} (ha : a ≠ 0)
    {k r H : ℕ} (h : k+r=4*H) :
    (81 : ℚ)^H-(-(3 : ℚ)^r*b/a)=(3 : ℚ)^r*(a*3^k+b)/a := by
  have hp : (3 : ℚ)^k*3^r=81^H := by exact_mod_cast power_identity h
  rw [← hp]
  field_simp
  ring

theorem eighty_one_pow_mod_sixteen (H : ℕ) : (81 : ℕ)^H%16=1 := by
  induction H with
  | zero => norm_num
  | succ H ih => norm_num [pow_succ,Nat.mul_mod,ih]

theorem high_valuation_congruence {a b k r H : ℕ}
    (h : k+r=4*H) (hS : 16 ∣ a*3^k+b) : 16 ∣ a+3^r*b := by
  have hscaled : 16 ∣ a*81^H+3^r*b := by
    have hs := dvd_mul_of_dvd_right hS (3^r)
    convert hs using 1
    rw [← power_identity h]
    ring
  rw [Nat.dvd_iff_mod_eq_zero] at hscaled ⊢
  simpa [Nat.add_mod,Nat.mul_mod,eighty_one_pow_mod_sixteen] using hscaled

theorem first_margin :
    (0 : ℝ) < 7*4*(2772/1000)-7*(9/2)-3/20
      -5*((353/300)*(1099/250)+(3343/1000)*((12/7)*(201/200)*(1733/2500))) := by
  norm_num

theorem second_margin :
    (0 : ℝ) < 9*4*(2772/1000)-9*(5011/1000)-3/20
      -5*((151/100)*(1099/250)+(3343/1000)*((12/7)*(201/200)*(1733/2500))) := by
  norm_num

theorem first_range_local_loss {delta y s loss J y2 : ℝ}
    (hdlo : (19 : ℝ)/12 ≤ delta) (hJ : 0 ≤ J)
    (hy : 92*J ≤ y) (hs : s ≤ 140*J)
    (hloss : 0 ≤ loss) (hy2 : y2 ≤ delta*y-loss+(delta-1)*s) :
    s ≤ delta*y-J ∧ y2 ≤ delta^2*y-(16/5)*J := by
  have hd0 : 0 ≤ delta := by linarith
  have h1 := mul_le_mul_of_nonneg_left hy hd0
  have h2 := mul_le_mul_of_nonneg_right hdlo hJ
  have hgap : (17 : ℝ)/3*J ≤ delta*y-s := by nlinarith
  have hgap0 : 0 ≤ delta*y-s := by nlinarith
  have hb : (7 : ℝ)/12 ≤ delta-1 := by linarith
  have h3 := mul_le_mul_of_nonneg_left hgap (by norm_num : (0 : ℝ) ≤ 7/12)
  have h4 := mul_le_mul_of_nonneg_right hb hgap0
  have hprod : (16 : ℝ)/5*J ≤ (delta-1)*(delta*y-s) := by nlinarith
  constructor
  · linarith
  · nlinarith

theorem restart_constants :
    (92 : ℝ)/93 < 99/100 ∧ (2 : ℕ)^44<3^28 ∧
      (7 : ℝ)/12*10>16/5 ∧ (7 : ℝ)/12*(19/300)*256>16/5 := by
  norm_num

end CollatzFourthPower

/-- info: 'CollatzFourthPower.power_identity' depends on axioms: [propext] -/
#guard_msgs in
#print axioms CollatzFourthPower.power_identity
/-- info: 'CollatzFourthPower.signed_form_identity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzFourthPower.signed_form_identity
/-- info: 'CollatzFourthPower.eighty_one_pow_mod_sixteen' depends on axioms: [propext] -/
#guard_msgs in
#print axioms CollatzFourthPower.eighty_one_pow_mod_sixteen
/-- info: 'CollatzFourthPower.high_valuation_congruence' depends on axioms: [propext] -/
#guard_msgs in
#print axioms CollatzFourthPower.high_valuation_congruence
/-- info: 'CollatzFourthPower.first_margin' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzFourthPower.first_margin
/-- info: 'CollatzFourthPower.second_margin' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzFourthPower.second_margin
/-- info: 'CollatzFourthPower.first_range_local_loss' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzFourthPower.first_range_local_loss
/-- info: 'CollatzFourthPower.restart_constants' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzFourthPower.restart_constants
