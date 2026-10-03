import Mathlib.Tactic

namespace CollatzAffineEnvelope

noncomputable def growth (delta lambda B x : ℝ) : ℝ :=
  if x ≤ B then delta*x else max (lambda*x) (x+(delta-1)*B)

theorem growth_le_affine {delta lambda B x : ℝ}
    (hl : 1 ≤ lambda) (hd : lambda ≤ delta) (hB : 0 ≤ B) :
    growth delta lambda B x ≤ lambda*x+(delta-lambda)*B := by
  unfold growth
  split_ifs with hx
  · have h := mul_le_mul_of_nonneg_left hx (sub_nonneg.mpr hd)
    nlinarith
  · have hBx : B ≤ x := le_of_lt (lt_of_not_ge hx)
    have h := mul_nonneg (sub_nonneg.mpr hd) hB
    have h2 := mul_le_mul_of_nonneg_left hBx (sub_nonneg.mpr hl)
    apply max_le
    · linarith
    · nlinarith

theorem affine_sequence_bound {v : ℕ → ℝ} {lambda b : ℝ}
    (hl : 1 < lambda) (hstep : ∀ n, v (n+1) ≤ lambda*v n+b) :
    ∀ n, v n ≤ (v 0+b/(lambda-1))*lambda^n-b/(lambda-1) := by
  intro n
  have hl0 : 0 ≤ lambda := by linarith
  have hn : lambda-1 ≠ 0 := by linarith
  have hid : lambda*(b/(lambda-1))=b+b/(lambda-1) := by
    field_simp
    ring
  induction n with
  | zero => simp
  | succ n ih =>
      have h := mul_le_mul_of_nonneg_left ih hl0
      have hs := hstep n
      rw [pow_succ]
      nlinarith

end CollatzAffineEnvelope

/-- info: 'CollatzAffineEnvelope.growth_le_affine' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzAffineEnvelope.growth_le_affine
/-- info: 'CollatzAffineEnvelope.affine_sequence_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzAffineEnvelope.affine_sequence_bound
