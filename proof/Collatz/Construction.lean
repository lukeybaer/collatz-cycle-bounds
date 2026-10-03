import Collatz.Dynamics

/-! Every positive odd initial value has an arithmetic block representation.
The choices use the ordinary factorization into a power of two and an odd part.
This closes the representation-existence obligation without assuming any
analytic bound or any form of the Collatz conjecture. -/
namespace Collatz

structure OddStart where
  value : ℕ
  pos : 0 < value
  odd : Odd value

structure NextBlock (s : OddStart) where
  next : OddStart
  a : ℕ
  k : ℕ
  ell : ℕ
  a_pos : 0 < a
  k_pos : 0 < k
  ell_pos : 0 < ell
  a_odd : Odd a
  start_eq : s.value + 1 = a*2^k
  next_eq : next.value*2^ell+1 = a*3^k

theorem nextBlock_exists (s : OddStart) : Nonempty (NextBlock s) := by
  obtain ⟨k, a, haodd, hstart⟩ := Nat.exists_eq_two_pow_mul_odd (by omega : s.value+1 ≠ 0)
  have ha : 0 < a := by have := Nat.odd_iff.mp haodd; omega
  have hk : 0 < k := by
    by_contra h
    have hz : k = 0 := by omega
    simp only [hz, pow_zero, one_mul] at hstart
    have := Nat.odd_iff.mp s.odd
    have := Nat.odd_iff.mp haodd
    omega
  have hpow : 3 ≤ 3^k := by
    simpa using (Nat.pow_le_pow_right (by norm_num : 0 < 3) (show 1 ≤ k by omega))
  have hprod : 3 ≤ a*3^k := by nlinarith
  obtain ⟨ell, n, hnodd, hn⟩ :=
    Nat.exists_eq_two_pow_mul_odd (by omega : a*3^k-1 ≠ 0)
  have hnpos : 0 < n := by have := Nat.odd_iff.mp hnodd; omega
  have hpodd : Odd (a*3^k) := haodd.mul (show Odd (3 : ℕ) from by decide).pow
  have hell : 0 < ell := by
    by_contra h
    have hz : ell = 0 := by omega
    simp only [hz, pow_zero, one_mul] at hn
    have := Nat.odd_iff.mp hpodd
    have := Nat.odd_iff.mp hnodd
    omega
  refine ⟨{ next := ⟨n, hnpos, hnodd⟩, a := a, k := k, ell := ell,
            a_pos := ha, k_pos := hk, ell_pos := hell, a_odd := haodd,
            start_eq := ?_, next_eq := ?_ }⟩
  · simpa [Nat.mul_comm] using hstart
  · dsimp
    have hn' : a*3^k-1 = n*2^ell := by simpa only [Nat.mul_comm] using hn
    omega

noncomputable def nextBlock (s : OddStart) : NextBlock s :=
  Classical.choice (nextBlock_exists s)

noncomputable def oddStates (s : OddStart) : ℕ → OddStart
  | 0 => s
  | i+1 => (nextBlock (oddStates s i)).next

noncomputable def orbitOfOdd (s : OddStart) : BlockOrbit where
  n := fun i => (oddStates s i).value
  a := fun i => (nextBlock (oddStates s i)).a
  k := fun i => (nextBlock (oddStates s i)).k
  ell := fun i => (nextBlock (oddStates s i)).ell
  n_pos := fun i => (oddStates s i).pos
  a_pos := fun i => (nextBlock (oddStates s i)).a_pos
  k_pos := fun i => (nextBlock (oddStates s i)).k_pos
  ell_pos := fun i => (nextBlock (oddStates s i)).ell_pos
  n_odd := fun i => (oddStates s i).odd
  a_odd := fun i => (nextBlock (oddStates s i)).a_odd
  start_eq := fun i => (nextBlock (oddStates s i)).start_eq
  next_eq := fun i => (nextBlock (oddStates s i)).next_eq

theorem orbitOfOdd_start (s : OddStart) : (orbitOfOdd s).n 0 = s.value := rfl

theorem orbitOfOdd_trajectory (s : OddStart) :
    ∀ i, shortcut^[(orbitOfOdd s).time i] s.value = (orbitOfOdd s).n i :=
  (orbitOfOdd s).is_trajectory

end Collatz

/-- info: 'Collatz.orbitOfOdd_trajectory' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Collatz.orbitOfOdd_trajectory
