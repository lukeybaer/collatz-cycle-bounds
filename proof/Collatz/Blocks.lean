import Collatz.Legacy.CollatzGlobalEnvelope

/-!
# Arithmetic block sequences

An odd block begins at `n = a * 2^k - 1` and, after `k` odd shortcut
steps and `ell` even steps, ends at `(a * 3^k - 1) / 2^ell`.
The structure records these exact natural-number identities. Oddness makes
the run lengths maximal. This is an arithmetic representation of blocks;
equivalence with a separately defined iterated Collatz function is not claimed.
-/
namespace Collatz

noncomputable abbrev delta : ℝ := CollatzGlobalEnvelope.delta

structure BlockOrbit where
  n : ℕ → ℕ
  a : ℕ → ℕ
  k : ℕ → ℕ
  ell : ℕ → ℕ
  n_pos : ∀ i, 0 < n i
  a_pos : ∀ i, 0 < a i
  k_pos : ∀ i, 0 < k i
  ell_pos : ∀ i, 0 < ell i
  n_odd : ∀ i, Odd (n i)
  a_odd : ∀ i, Odd (a i)
  start_eq : ∀ i, n i + 1 = a i * 2 ^ k i
  next_eq : ∀ i, n (i+1) * 2 ^ ell i + 1 = a i * 3 ^ k i

noncomputable def BlockOrbit.height (o : BlockOrbit) (i : ℕ) : ℝ :=
  Real.log ((o.n i : ℝ) + 1) / Real.log 2

def BlockOrbit.run (o : BlockOrbit) (i : ℕ) : ℝ := o.k i

lemma log_two_pos : 0 < Real.log 2 := by linarith [Real.log_two_gt_d9]

theorem BlockOrbit.height_split (o : BlockOrbit) (i : ℕ) :
    o.height i = o.run i + Real.log (o.a i) / Real.log 2 := by
  have he : (o.n i : ℝ) + 1 = (o.a i : ℝ) * 2 ^ o.k i := by
    exact_mod_cast o.start_eq i
  have ha : (o.a i : ℝ) ≠ 0 := by exact_mod_cast Nat.ne_of_gt (o.a_pos i)
  unfold height run
  rw [he, Real.log_mul ha (by positivity), Real.log_pow]
  field_simp
  ring

theorem BlockOrbit.run_le_height (o : BlockOrbit) (i : ℕ) :
    o.run i ≤ o.height i := by
  rw [o.height_split]
  have := div_nonneg (Real.log_natCast_nonneg (o.a i)) log_two_pos.le
  linarith

theorem BlockOrbit.height_ge_one (o : BlockOrbit) (i : ℕ) :
    1 ≤ o.height i := by
  have hk : (1 : ℝ) ≤ o.run i := by
    unfold run
    exact_mod_cast o.k_pos i
  exact hk.trans (o.run_le_height i)

theorem BlockOrbit.height_step (o : BlockOrbit) (i : ℕ) :
    o.height (i+1) ≤ delta * o.height i := by
  have hn : (o.n (i+1) : ℝ) + 1 ≤ (o.a i : ℝ) * 3 ^ o.k i := by
    have he : (o.n (i+1) : ℝ) * 2 ^ o.ell i + 1 =
        (o.a i : ℝ) * 3 ^ o.k i := by exact_mod_cast o.next_eq i
    have hp : (1 : ℝ) ≤ 2 ^ o.ell i := one_le_pow₀ (by norm_num)
    have hprod := mul_le_mul_of_nonneg_left hp (Nat.cast_nonneg (o.n (i+1)) : (0 : ℝ) ≤ _)
    nlinarith
  have hlog := Real.log_le_log (by positivity : (0 : ℝ) < (o.n (i+1) : ℝ)+1) hn
  have ha : (o.a i : ℝ) ≠ 0 := by exact_mod_cast Nat.ne_of_gt (o.a_pos i)
  rw [Real.log_mul ha (by positivity), Real.log_pow] at hlog
  have hb := div_le_div_of_nonneg_right hlog log_two_pos.le
  have hlog3 : Real.log 3 = delta * Real.log 2 := by
    unfold delta CollatzGlobalEnvelope.delta
    field_simp
  have hx : 0 ≤ Real.log (o.a i) / Real.log 2 :=
    div_nonneg (Real.log_natCast_nonneg _) log_two_pos.le
  have hd : 1 ≤ delta := by linarith [CollatzGlobalEnvelope.delta_bounds.1]
  have hprod := mul_nonneg (sub_nonneg.mpr hd) hx
  change Real.log ((o.n (i+1) : ℝ)+1) / Real.log 2 ≤ delta * o.height i
  rw [o.height_split]
  unfold run
  rw [hlog3] at hb
  have hid : (Real.log (o.a i) + (o.k i : ℝ) * (delta * Real.log 2)) / Real.log 2 =
      Real.log (o.a i) / Real.log 2 + (o.k i : ℝ)*delta := by
    field_simp
  rw [hid] at hb
  nlinarith

end Collatz
