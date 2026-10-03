import Collatz.Blocks

/-! The arithmetic block representation follows the actual natural-number
shortcut Collatz function. These are formalizations of the manuscript's
existing block identities, not additional analytic assumptions. -/
namespace Collatz

def shortcut (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3*n+1)/2

lemma shortcut_odd_form {a : ℕ} (ha : 0 < a) :
    shortcut (2*a-1) = 3*a-1 := by
  have hm : (2*a-1) % 2 ≠ 0 := by omega
  simp only [shortcut, ite_eq_right hm]
  omega

lemma shortcut_even_form (a : ℕ) : shortcut (2*a) = a := by
  simp [shortcut]

theorem iterate_odd_run (k a : ℕ) (ha : 0 < a) :
    shortcut^[k] (a*2^k-1) = a*3^k-1 := by
  induction k generalizing a with
  | zero => simp
  | succ k ih =>
    have hp : 0 < a*2^k := by positivity
    have hin : a*2^(k+1)-1 = 2*(a*2^k)-1 := by congr 1; ring
    rw [hin, Function.iterate_succ_apply, shortcut_odd_form hp]
    have hmid : 3*(a*2^k)-1 = (3*a)*2^k-1 := by congr 1; ring
    rw [hmid, ih (3*a) (by omega)]
    congr 1
    ring

theorem iterate_even_run (ell a : ℕ) :
    shortcut^[ell] (a*2^ell) = a := by
  induction ell with
  | zero => simp
  | succ ell ih =>
    have he : a*2^(ell+1) = 2*(a*2^ell) := by ring
    rw [he, Function.iterate_succ_apply, shortcut_even_form, ih]

theorem BlockOrbit.block_is_iteration (o : BlockOrbit) (i : ℕ) :
    shortcut^[o.k i + o.ell i] (o.n i) = o.n (i+1) := by
  have hn : o.n i = o.a i*2^o.k i-1 := by have := o.start_eq i; omega
  have hnext : o.a i*3^o.k i-1 = o.n (i+1)*2^o.ell i := by
    have := o.next_eq i
    omega
  rw [Nat.add_comm, Function.iterate_add_apply, hn,
    iterate_odd_run _ _ (o.a_pos i), hnext, iterate_even_run]

def BlockOrbit.time (o : BlockOrbit) : ℕ → ℕ
  | 0 => 0
  | i+1 => o.time i + (o.k i + o.ell i)

theorem BlockOrbit.is_trajectory (o : BlockOrbit) :
    ∀ i, shortcut^[o.time i] (o.n 0) = o.n i := by
  intro i
  induction i with
  | zero => rfl
  | succ i ih =>
    change shortcut^[o.time i + (o.k i + o.ell i)] (o.n 0) = o.n (i+1)
    rw [Nat.add_comm, Function.iterate_add_apply, ih, o.block_is_iteration]

end Collatz

/-- info: 'Collatz.BlockOrbit.is_trajectory' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Collatz.BlockOrbit.is_trajectory
