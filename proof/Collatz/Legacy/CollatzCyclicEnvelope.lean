import Mathlib.Order.GaloisConnection.Defs
import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Logic.Function.Iterate
import Mathlib.Tactic

/-!
Construction of a subordinate cyclic envelope from forward run bounds.
The inverse growth map is represented by its order adjunction. This avoids
assuming that the actual heights satisfy a one-step growth rule.
-/

namespace CollatzCyclicEnvelope

open Finset Function

variable {α : Type*} [LinearOrder α]

theorem iterate_adjoint {psi phi : α → α} (gc : GaloisConnection psi phi)
    (n : ℕ) (x y : α) : psi^[n] x ≤ y ↔ x ≤ phi^[n] y := by
  induction n generalizing x y with
  | zero => simp
  | succ n ih =>
      calc
        psi^[n+1] x ≤ y ↔ psi (psi^[n] x) ≤ y := by rw [iterate_succ_apply']
        _ ↔ psi^[n] x ≤ phi y := gc _ _
        _ ↔ x ≤ phi^[n] (phi y) := ih _ _
        _ ↔ x ≤ phi^[n+1] y := by rw [iterate_succ_apply]

theorem inverse_iterate_le {psi phi : α → α} (gc : GaloisConnection psi phi)
    (hg : ∀ x, x ≤ phi x) (n : ℕ) (x : α) : psi^[n] x ≤ x := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [iterate_succ_apply']
      exact le_trans ((gc _ _).mpr (hg _)) ih

noncomputable def envelope (psi : α → α) (seed : ℕ → α) (m : ℕ)
    (hm : 0 < m) (i : ℕ) : α :=
  (range m).sup' (⟨0, mem_range.mpr hm⟩) (fun j => psi^[j] (seed (i+j)))

theorem term_le_envelope {psi : α → α} {seed : ℕ → α} {m : ℕ}
    (hm : 0 < m) (i j : ℕ) (hj : j < m) :
    psi^[j] (seed (i+j)) ≤ envelope psi seed m hm i := by
  exact le_sup' (fun j => psi^[j] (seed (i+j))) (mem_range.mpr hj)

theorem seed_le_envelope {psi : α → α} {seed : ℕ → α} {m : ℕ}
    (hm : 0 < m) (i : ℕ) : seed i ≤ envelope psi seed m hm i := by
  simpa using term_le_envelope (psi := psi) (seed := seed) hm i 0 hm

theorem envelope_le_height {psi phi : α → α} {seed : ℕ → α} {m : ℕ}
    (gc : GaloisConnection psi phi) (hm : 0 < m) (i : ℕ) (y : α)
    (hbound : ∀ j, j < m → seed (i+j) ≤ phi^[j] y) :
    envelope psi seed m hm i ≤ y := by
  apply sup'_le
  intro j hj
  exact (iterate_adjoint gc j _ _).mpr (hbound j (mem_range.mp hj))

theorem envelope_growth {psi phi : α → α} {seed : ℕ → α} {m : ℕ}
    (gc : GaloisConnection psi phi) (hg : ∀ x, x ≤ phi x)
    (hm : 0 < m) (hperiod : ∀ i, seed (i+m) = seed i) (i : ℕ) :
    envelope psi seed m hm (i+1) ≤ phi (envelope psi seed m hm i) := by
  apply sup'_le
  intro j hj
  have hjm : j < m := mem_range.mp hj
  have hidx : i+1+j = i+(j+1) := by omega
  rw [hidx]
  by_cases hnext : j+1 < m
  · have hterm := term_le_envelope (psi := psi) (seed := seed) hm i (j+1) hnext
    have hlocal := gc.le_u_l (psi^[j] (seed (i+(j+1))))
    rw [← iterate_succ_apply' (f := psi) j (seed (i+(j+1)))] at hlocal
    exact le_trans hlocal (gc.monotone_u hterm)
  · have hlast : j+1 = m := by omega
    rw [hlast,hperiod i]
    exact le_trans (inverse_iterate_le gc hg j (seed i))
      (le_trans (seed_le_envelope hm i) (hg _))

theorem common_cap_preserves_growth {phi : α → α} {z : ℕ → α} {cap : α}
    (hg : ∀ x, x ≤ phi x) (hz : ∀ i, z (i+1) ≤ phi (z i)) :
    ∀ i, min (z (i+1)) cap ≤ phi (min (z i) cap) := by
  intro i
  by_cases hi : z i ≤ cap
  · rw [min_eq_left hi]
    exact le_trans (min_le_left _ _) (hz i)
  · rw [min_eq_right (le_of_not_ge hi)]
    exact le_trans (min_le_right _ _) (hg cap)

end CollatzCyclicEnvelope

/-- info: 'CollatzCyclicEnvelope.iterate_adjoint' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms CollatzCyclicEnvelope.iterate_adjoint
/-- info: 'CollatzCyclicEnvelope.inverse_iterate_le' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms CollatzCyclicEnvelope.inverse_iterate_le
/-- info: 'CollatzCyclicEnvelope.term_le_envelope' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzCyclicEnvelope.term_le_envelope
/-- info: 'CollatzCyclicEnvelope.seed_le_envelope' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzCyclicEnvelope.seed_le_envelope
/-- info: 'CollatzCyclicEnvelope.envelope_le_height' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzCyclicEnvelope.envelope_le_height
/-- info: 'CollatzCyclicEnvelope.envelope_growth' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzCyclicEnvelope.envelope_growth
/-- info: 'CollatzCyclicEnvelope.common_cap_preserves_growth' depends on axioms: [propext] -/
#guard_msgs in
#print axioms CollatzCyclicEnvelope.common_cap_preserves_growth
