import Mathlib.Tactic

/-! Elementary parameter bounds for the two-regime interpolation proof.
The external p-adic theorem is not formalized here. -/
namespace CollatzTwoRegimeParameters

noncomputable def margin (q : ℝ) : ℝ :=
  (1783170953/7444500000)*q^2-(454813329/354500000)*q-1631430293/744450000

theorem small_margin_positive :
    (0 : ℝ) < 9*6*(2079/1000)-9*(697/125)-3/10
      -7*((709/300)*(1099/500)+(3013/1000)*(525099/437500)) := by
  norm_num

theorem large_margin_positive {q : ℝ} (hq : 9 ≤ q) :
    283/50 < margin q := by
  have hid : margin q = 3011630363/531750000 +
      (1503066483/496300000)*(q-9)+(1783170953/7444500000)*(q-9)^2 := by
    unfold margin
    ring
  rw [hid]
  nlinarith [sq_nonneg (q-9)]

theorem dyadic_run_bound (q : ℕ) (hq : 9 ≤ q) :
    3*((q : ℝ)+1)*(q+2) < (38/25 : ℝ)*2^(q-1) := by
  induction q, hq using Nat.le_induction with
  | base => norm_num
  | succ q hq ih =>
      have hqr : (9 : ℝ) ≤ q := by exact_mod_cast hq
      have hpoly : 3*((q : ℝ)+2)*(q+3) ≤ 2*(3*(q+1)*(q+2)) := by
        nlinarith
      have hpow : (2 : ℝ)^q = 2*2^(q-1) := by
        have heq : q = (q-1)+1 := by omega
        conv_lhs => rw [heq,pow_succ]
        ring
      have hscaled := mul_lt_mul_of_pos_left ih (by norm_num : (0 : ℝ) < 2)
      simp only [Nat.cast_add,Nat.cast_one,Nat.add_sub_cancel]
      rw [hpow]
      linarith

theorem rectangle_cardinality {J q : ℝ} (hJ : 0 < J) (hq : 9 ≤ q) :
    (q-1)*J*(q+5)>((q+1)*J-1)*(q+2) := by
  have hq2 : 0 < q+2 := by linarith
  have hx : 0 ≤ (q-7)*J := mul_nonneg (by linarith) (le_of_lt hJ)
  nlinarith

theorem large_b_numerator {q z J : ℝ}
    (hq : 9 ≤ q) (hz : 512 ≤ z) (hJ : 100 ≤ J) :
    7*z+15*q+20 ≤ J*((2*q-13)*z-10*q+10) := by
  have hc : 0 ≤ 200*q-1307 := by linarith
  have hmul := mul_le_mul_of_nonneg_left hz hc
  have hbase : 7*z+15*q+20 ≤ 100*((2*q-13)*z-10*q+10) := by
    nlinarith
  have hpos : 0 ≤ (2*q-13)*z-10*q+10 := by nlinarith
  have hscale := mul_le_mul_of_nonneg_right hJ hpos
  linarith

theorem two_block_loss {delta y k s loss J y2 : ℝ}
    (hdlo : (19 : ℝ)/12 ≤ delta) (hdhi : delta ≤ 5/3)
    (hJ : 0 ≤ J) (hk : 125*J ≤ k) (hky : k ≤ y)
    (hs : s ≤ (38 : ℝ)/25*k) (hloss : 0 ≤ loss)
    (hy2 : y2 ≤ delta*y-loss+(delta-1)*s) :
    s ≤ delta*y-J ∧ y2 ≤ delta^2*y-(delta+1)*J := by
  have hdelta : 0 ≤ delta := by linarith
  have hk0 : 0 ≤ k := by nlinarith
  have hdy := mul_le_mul_of_nonneg_left hky hdelta
  have hdk := mul_le_mul_of_nonneg_right hdlo hk0
  have hgap : 19*k/300 ≤ delta*y-s := by linarith
  have hgap0 : 0 ≤ delta*y-s := by linarith
  have hbeta : (7 : ℝ)/12 ≤ delta-1 := by linarith
  have h1 := mul_le_mul_of_nonneg_left hgap (by norm_num : (0 : ℝ) ≤ 7/12)
  have h2 := mul_le_mul_of_nonneg_right hbeta hgap0
  have hprod : 133*k/3600 ≤ (delta-1)*(delta*y-s) := by nlinarith
  have hJdelta : (delta+1)*J ≤ (8 : ℝ)/3*J :=
    mul_le_mul_of_nonneg_right (by linarith) hJ
  constructor
  · linarith
  · nlinarith

theorem restart_constant :
    (127 : ℝ)/160 < (81/100)*(99/100) ∧ (2 : ℕ)^41 < 3^26 := by
  norm_num

end CollatzTwoRegimeParameters

/-- info: 'CollatzTwoRegimeParameters.small_margin_positive' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzTwoRegimeParameters.small_margin_positive
/-- info: 'CollatzTwoRegimeParameters.large_margin_positive' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzTwoRegimeParameters.large_margin_positive
/-- info: 'CollatzTwoRegimeParameters.dyadic_run_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzTwoRegimeParameters.dyadic_run_bound
/-- info: 'CollatzTwoRegimeParameters.rectangle_cardinality' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzTwoRegimeParameters.rectangle_cardinality
/-- info: 'CollatzTwoRegimeParameters.large_b_numerator' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzTwoRegimeParameters.large_b_numerator
/-- info: 'CollatzTwoRegimeParameters.two_block_loss' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzTwoRegimeParameters.two_block_loss
/-- info: 'CollatzTwoRegimeParameters.restart_constant' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzTwoRegimeParameters.restart_constant
