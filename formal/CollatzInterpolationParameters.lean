import Mathlib.Tactic

/-!
Elementary all-parameter parts of the direct interpolation argument.
The external transcendence theorem and the factorial integral estimate
remain ordinary mathematical inputs.
-/

namespace CollatzInterpolationParameters

noncomputable def margin (q : ℝ) : ℝ :=
  (15150889/44625000)*q^2-(86463089/33250000)*q-749/250

theorem margin_positive {q : ℝ} (hq : 9 ≤ q) : 11/10 < margin q := by
  have hid : margin q = 622470497/565250000 +
      (1984530179/565250000)*(q-9)+(15150889/44625000)*(q-9)^2 := by
    unfold margin
    ring
  rw [hid]
  nlinarith [sq_nonneg (q-9)]

theorem dyadic_run_bound (q : ℕ) (hq : 10 ≤ q) :
    6*(q : ℝ)*(q+1) < (31/20 : ℝ)*2^(q-1) := by
  induction q, hq using Nat.le_induction with
  | base => norm_num
  | succ q hq ih =>
      have hqr : (10 : ℝ) ≤ q := by exact_mod_cast hq
      have hpoly : 6*((q : ℝ)+1)*(q+2) ≤ 2*(6*q*(q+1)) := by
        nlinarith
      have hpow : (2 : ℝ)^q = 2*2^(q-1) := by
        have heq : q = (q-1)+1 := by omega
        conv_lhs => rw [heq,pow_succ]
        ring
      have hscaled := mul_lt_mul_of_pos_left ih (by norm_num : (0 : ℝ) < 2)
      simp only [Nat.cast_add,Nat.cast_one,Nat.add_sub_cancel]
      rw [hpow]
      linarith

theorem residue_rectangle_injective {H M r s r' s' : ℕ}
    (hMH : M ≤ H) (hr : r < M) (hr' : r' < M)
    (heq : r+H*s = r'+H*s') : r=r' ∧ s=s' := by
  have hH : 0 < H := by omega
  have hs : s=s' := by
    by_contra hn
    rcases lt_or_gt_of_ne hn with hlt | hgt
    · have hmul := Nat.mul_le_mul_left H (show s+1 ≤ s' by omega)
      nlinarith
    · have hmul := Nat.mul_le_mul_left H (show s'+1 ≤ s by omega)
      nlinarith
  subst s'
  constructor
  · omega
  · rfl

theorem two_block_loss {delta y k s loss J y2 : ℝ}
    (hdlo : (19 : ℝ)/12 ≤ delta) (hdhi : delta ≤ 5/3)
    (hJ : 0 ≤ J) (hk : 350*J ≤ k) (hky : k ≤ y)
    (hs : s ≤ (31 : ℝ)/20*k) (hloss : 0 ≤ loss)
    (hy2 : y2 ≤ delta*y-loss+(delta-1)*s) :
    s ≤ delta*y-J ∧ y2 ≤ delta^2*y-(delta+1)*J := by
  have hdelta : 0 ≤ delta := by linarith
  have hk0 : 0 ≤ k := by nlinarith
  have hdy := mul_le_mul_of_nonneg_left hky hdelta
  have hdk := mul_le_mul_of_nonneg_right hdlo hk0
  have hgap : k/30 ≤ delta*y-s := by linarith
  have hgap0 : 0 ≤ delta*y-s := by linarith
  have hbeta : (7 : ℝ)/12 ≤ delta-1 := by linarith
  have h1 := mul_le_mul_of_nonneg_left hgap (by norm_num : (0 : ℝ) ≤ 7/12)
  have h2 := mul_le_mul_of_nonneg_right hbeta hgap0
  have hprod : 7*k/360 ≤ (delta-1)*(delta*y-s) := by nlinarith
  have hJdelta : (delta+1)*J ≤ (8 : ℝ)/3*J :=
    mul_le_mul_of_nonneg_right (by linarith) hJ
  constructor
  · linarith
  · nlinarith

end CollatzInterpolationParameters

#print axioms CollatzInterpolationParameters.margin_positive
#print axioms CollatzInterpolationParameters.dyadic_run_bound
#print axioms CollatzInterpolationParameters.residue_rectangle_injective
#print axioms CollatzInterpolationParameters.two_block_loss
