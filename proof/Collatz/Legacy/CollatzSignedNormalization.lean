import Mathlib.Tactic

/-!
Exact algebra and the conditional modulo-eight hypothesis in the
signed-rational specialization of the external p-adic theorem.
-/

namespace CollatzSignedNormalization

theorem three_parity_identity (k : ℕ) :
    3^k * 3^(k%2) = (9 : ℕ)^((k+1)/2) := by
  have heq : k+k%2 = 2*((k+1)/2) := by omega
  rw [← pow_add,heq,pow_mul]
  norm_num

theorem signed_form_identity {a b : ℚ} (ha : a ≠ 0) (k : ℕ) :
    (9 : ℚ)^((k+1)/2) - (-(3 : ℚ)^(k%2)*b/a) =
      (3 : ℚ)^(k%2)*(a*3^k+b)/a := by
  have hp : (3 : ℚ)^k * 3^(k%2) = 9^((k+1)/2) := by
    exact_mod_cast three_parity_identity k
  rw [← hp]
  field_simp
  ring

theorem nine_pow_mod_eight (h : ℕ) : (9 : ℕ)^h % 8 = 1 := by
  induction h with
  | zero => norm_num
  | succ h ih => norm_num [pow_succ,Nat.mul_mod,ih]

theorem high_valuation_congruence {a b k : ℕ}
    (hS : 8 ∣ a*3^k+b) : 8 ∣ a+3^(k%2)*b := by
  have hscaled : 8 ∣ a*9^((k+1)/2)+3^(k%2)*b := by
    have h := dvd_mul_of_dvd_right hS (3^(k%2))
    convert h using 1
    rw [← three_parity_identity k]
    ring
  rw [Nat.dvd_iff_mod_eq_zero] at hscaled ⊢
  simpa [Nat.add_mod,Nat.mul_mod,nine_pow_mod_eight] using hscaled

end CollatzSignedNormalization

/-- info: 'CollatzSignedNormalization.three_parity_identity' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms CollatzSignedNormalization.three_parity_identity
/-- info: 'CollatzSignedNormalization.signed_form_identity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzSignedNormalization.signed_form_identity
/-- info: 'CollatzSignedNormalization.nine_pow_mod_eight' depends on axioms: [propext] -/
#guard_msgs in
#print axioms CollatzSignedNormalization.nine_pow_mod_eight
/-- info: 'CollatzSignedNormalization.high_valuation_congruence' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms CollatzSignedNormalization.high_valuation_congruence
