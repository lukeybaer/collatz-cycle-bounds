import Mathlib.Basic.Real.Basic
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Tactic

/-!
# Global continuation of the smaller-base envelope

This file verifies the continuous extension and the passage from a finite
virtual warmup to a uniform exponential bound. The local p-adic restart
rule is an external mathematical input, separately handled by the other
formal core files.
-/

namespace CollatzGlobalEnvelope

noncomputable def growth (delta lambda B x : ℝ) : ℝ :=
  if x ≤ B then delta * x else max (lambda * x) (x + (delta - 1) * B)

theorem growth_monotone {delta lambda B : ℝ}
    (hd : 0 ≤ delta) (hl : 0 ≤ lambda) : Monotone (growth delta lambda B) := by
  intro x y hxy
  unfold growth
  split_ifs with hx hy hy
  · exact mul_le_mul_of_nonneg_left hxy hd
  · have hB : B < y := lt_of_not_ge hy
    have hxb : delta * x ≤ delta * B := mul_le_mul_of_nonneg_left hx hd
    have hright : delta * B ≤ y + (delta - 1) * B := by nlinarith
    exact le_trans (le_trans hxb hright) (le_max_right _ _)
  · exact (hx (le_trans hxy hy)).elim
  · apply max_le_max
    · exact mul_le_mul_of_nonneg_left hxy hl
    · linarith

theorem growth_upper {delta lambda B x : ℝ}
    (hd : 1 ≤ delta) (hl : lambda ≤ delta) (hB : 0 ≤ B) :
    growth delta lambda B x ≤ delta * x := by
  unfold growth
  split_ifs with hx
  · exact le_rfl
  · have hBx : B ≤ x := le_of_lt (lt_of_not_ge hx)
    have hx0 : 0 ≤ x := le_trans hB hBx
    apply max_le
    · exact mul_le_mul_of_nonneg_right hl hx0
    · nlinarith [mul_nonneg (sub_nonneg.mpr hd) (sub_nonneg.mpr hBx)]

theorem growth_lower {delta lambda B x : ℝ}
    (hd : (3 : ℝ) / 2 ≤ delta) (hl : (3 : ℝ) / 2 ≤ lambda) (hx : 0 ≤ x) :
    (3 : ℝ) / 2 * x ≤ growth delta lambda B x := by
  unfold growth
  split_ifs
  · exact mul_le_mul_of_nonneg_right hd hx
  · exact le_trans (mul_le_mul_of_nonneg_right hl hx) (le_max_left _ _)

theorem growth_tail {delta lambda B x : ℝ}
    (hl : 1 ≤ lambda) (hjoin : delta + 1 ≤ 2 * lambda)
    (hB : 0 < B) (hx : 2 * B ≤ x) :
    growth delta lambda B x = lambda * x := by
  have hb : ¬ x ≤ B := by linarith
  unfold growth
  rw [ite_eq_right hb, max_eq_left]
  have hprod := mul_nonneg (sub_nonneg.mpr hl) (sub_nonneg.mpr hx)
  have hjoinB := mul_le_mul_of_nonneg_right hjoin (le_of_lt hB)
  nlinarith

theorem virtual_lower {G : ℝ → ℝ} {v : ℕ → ℝ} {c : ℝ}
    (hc : 0 ≤ c) (hv0 : 0 ≤ v 0)
    (hstep : ∀ n, v (n+1) = G (v n))
    (hlower : ∀ x, 0 ≤ x → c*x ≤ G x) :
    ∀ n, c^n*v 0 ≤ v n ∧ 0 ≤ v n := by
  intro n
  induction n with
  | zero => simpa using hv0
  | succ n ih =>
      have h1 := mul_le_mul_of_nonneg_left ih.1 hc
      have h2 := hlower (v n) ih.2
      rw [hstep n]
      constructor
      · rw [pow_succ]
        nlinarith
      · exact le_trans (mul_nonneg hc ih.2) h2

theorem virtual_upper {G : ℝ → ℝ} {v : ℕ → ℝ} {delta : ℝ}
    (hd : 0 ≤ delta) (hstep : ∀ n, v (n+1) = G (v n))
    (hupper : ∀ x, G x ≤ delta*x) :
    ∀ n, v n ≤ delta^n*v 0 := by
  intro n
  induction n with
  | zero => simp
  | succ n ih =>
      have h := mul_le_mul_of_nonneg_left ih hd
      rw [hstep n, pow_succ]
      have hu := hupper (v n)
      nlinarith

theorem virtual_tail {G : ℝ → ℝ} {v : ℕ → ℝ} {lambda H : ℝ} {N : ℕ}
    (hl : 1 ≤ lambda) (hH : 0 ≤ H) (hN : H ≤ v N)
    (hstep : ∀ n, v (n+1) = G (v n))
    (htail : ∀ x, H ≤ x → G x = lambda*x) :
    ∀ s, v (N+s) = lambda^s*v N ∧ H ≤ v (N+s) := by
  intro s
  induction s with
  | zero => simpa using hN
  | succ s ih =>
      have hidx : N + (s+1) = (N+s)+1 := by omega
      rw [hidx,hstep,htail _ ih.2]
      constructor
      · rw [ih.1,pow_succ];ring
      · have hx : 0 ≤ v (N+s) := le_trans hH ih.2
        have h := mul_le_mul_of_nonneg_right hl hx
        nlinarith

theorem finite_warmup_bound {v : ℕ → ℝ} {delta lambda : ℝ} {N : ℕ}
    (hl : 0 < lambda) (hd : lambda ≤ delta) (hv0 : 0 ≤ v 0)
    (hupper : ∀ n, v n ≤ delta^n*v 0)
    (htail : ∀ s, v (N+s) = lambda^s*v N) :
    ∀ t, v t ≤ (delta/lambda)^N*v 0*lambda^t := by
  intro t
  have hdelta : 0 ≤ delta := by linarith
  have hratio : 1 ≤ delta/lambda := (le_div_iff₀ hl).2 (by simpa using hd)
  have hlnz : lambda ≠ 0 := ne_of_gt hl
  by_cases hNt : N ≤ t
  · obtain ⟨s,rfl⟩ := Nat.exists_eq_add_of_le hNt
    rw [htail s]
    have h := mul_le_mul_of_nonneg_left (hupper N) (pow_nonneg (le_of_lt hl) s)
    calc
      lambda^s*v N ≤ lambda^s*(delta^N*v 0) := h
      _ = (delta/lambda)^N*v 0*lambda^(N+s) := by
        rw [div_pow,pow_add]
        field_simp
  · have htN : t ≤ N := by omega
    have hp := pow_le_pow_right₀ hratio htN
    have hn : 0 ≤ v 0*lambda^t := mul_nonneg hv0 (pow_nonneg (le_of_lt hl) t)
    have h := mul_le_mul_of_nonneg_right hp hn
    have heq : (delta/lambda)^t*(v 0*lambda^t) = delta^t*v 0 := by
      rw [div_pow]
      field_simp
    calc
      v t ≤ delta^t*v 0 := hupper t
      _ = (delta/lambda)^t*(v 0*lambda^t) := heq.symm
      _ ≤ (delta/lambda)^N*(v 0*lambda^t) := h
      _ = (delta/lambda)^N*v 0*lambda^t := by ring

noncomputable def delta : ℝ := Real.log 3 / Real.log 2

theorem delta_bounds : (19 : ℝ)/12 < delta ∧ delta < 317/200 := by
  have h2 : 0 < Real.log 2 := by linarith [Real.log_two_gt_d9]
  unfold delta
  constructor
  · apply (lt_div_iff₀ h2).2
    linarith [Real.log_two_lt_d9,Real.log_three_gt_d9]
  · apply (div_lt_iff₀ h2).2
    linarith [Real.log_two_gt_d9,Real.log_three_lt_d9]

theorem explicit_virtual_bound {v : ℕ → ℝ}
    (hzero : 1 ≤ v 0)
    (hstep : ∀ n, v (n+1) = growth delta (delta-1/3200) (2^18) (v n)) :
    ∀ t, v t ≤ (delta/(delta-1/3200))^33*v 0*(delta-1/3200)^t := by
  have hdl := delta_bounds.1
  have hdu := delta_bounds.2
  have hv0 : 0 ≤ v 0 := by linarith
  have hdelta : 0 ≤ delta := by linarith
  have hlambda : (3 : ℝ)/2 ≤ delta-1/3200 := by linarith
  have hupper := virtual_upper hdelta hstep
    (fun x => growth_upper (by linarith : 1 ≤ delta)
      (by linarith : delta-1/3200 ≤ delta) (by positivity : (0 : ℝ) ≤ 2^18))
  have hlower := virtual_lower (by norm_num : (0 : ℝ) ≤ 3/2) hv0 hstep
    (fun x hx => growth_lower (by linarith : (3 : ℝ)/2 ≤ delta) hlambda hx)
  have hN : (2 : ℝ)*2^18 ≤ v 33 := by
    have h := (hlower 33).1
    have hstart := mul_le_mul_of_nonneg_left hzero
      (by positivity : (0 : ℝ) ≤ ((3 : ℝ)/2)^33)
    norm_num at hstart
    linarith
  have htail := virtual_tail (by linarith : 1 ≤ delta-1/3200)
    (by positivity : (0 : ℝ) ≤ 2*2^18) hN hstep
    (fun x hx => growth_tail (by linarith : 1 ≤ delta-1/3200)
      (by linarith : delta+1 ≤ 2*(delta-1/3200))
      (by positivity : (0 : ℝ) < 2^18) hx)
  exact finite_warmup_bound (by linarith : 0 < delta-1/3200)
    (by linarith : delta-1/3200 ≤ delta) hv0 hupper (fun s => (htail s).1)

end CollatzGlobalEnvelope

#print axioms CollatzGlobalEnvelope.growth_monotone
#print axioms CollatzGlobalEnvelope.growth_upper
#print axioms CollatzGlobalEnvelope.growth_lower
#print axioms CollatzGlobalEnvelope.growth_tail
#print axioms CollatzGlobalEnvelope.virtual_lower
#print axioms CollatzGlobalEnvelope.virtual_upper
#print axioms CollatzGlobalEnvelope.virtual_tail
#print axioms CollatzGlobalEnvelope.finite_warmup_bound
#print axioms CollatzGlobalEnvelope.delta_bounds
#print axioms CollatzGlobalEnvelope.explicit_virtual_bound
