import Mathlib.Analysis.Convex.Deriv
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic

/-!
# Convex costs from ordered prefix inequalities

This is the differentiable version of the classical majorization inequality,
proved here through weighted prefix sums. No novelty is claimed for it.
It closes the convex-cost step used after the extremal ramp comparison.
-/

namespace CollatzConvexCost

open Finset

theorem weighted_prefix_bound {a c : ℕ → ℝ} {m : ℕ}
    (hc : Monotone c)
    (hp : ∀ n, n ≤ m → 0 ≤ ∑ i ∈ range n, a i) :
    (∑ i ∈ range m, c i * a i) ≤ c m * (∑ i ∈ range m, a i) := by
  have all : ∀ n, n ≤ m →
      (∑ i ∈ range n, c i * a i) ≤ c n * (∑ i ∈ range n, a i) := by
    intro n
    induction n with
    | zero => intro _;simp
    | succ n ih =>
        intro hnm
        have hprevious := ih (by omega)
        have hsum := hp (n+1) hnm
        have hstep := hc (show n ≤ n+1 by omega)
        have hmul := mul_le_mul_of_nonneg_right hstep hsum
        rw [sum_range_succ] at hmul ⊢
        rw [sum_range_succ]
        nlinarith
  exact all m le_rfl

theorem convex_sum_from_tangents {u w c : ℕ → ℝ} {f : ℝ → ℝ} {m : ℕ}
    (hc : Monotone c)
    (hprefix : ∀ n, n ≤ m → (∑ i ∈ range n, w i) ≤ ∑ i ∈ range n, u i)
    (htotal : (∑ i ∈ range m, u i) = ∑ i ∈ range m, w i)
    (htangent : ∀ i, i < m → f (u i) + c i * (w i-u i) ≤ f (w i)) :
    (∑ i ∈ range m, f (u i)) ≤ ∑ i ∈ range m, f (w i) := by
  have hp : ∀ n, n ≤ m → 0 ≤ ∑ i ∈ range n, (u i-w i) := by
    intro n hn
    rw [sum_sub_distrib]
    exact sub_nonneg.mpr (hprefix n hn)
  have hweighted := weighted_prefix_bound hc hp
  rw [sum_sub_distrib,htotal,sub_self,mul_zero] at hweighted
  have hs := sum_le_sum (s := range m) (fun i hi => htangent i (mem_range.mp hi))
  rw [sum_add_distrib] at hs
  have hneg : (∑ i ∈ range m, c i * (w i-u i)) =
      -(∑ i ∈ range m, c i * (u i-w i)) := by
    rw [← sum_neg_distrib]
    apply sum_congr rfl
    intro i hi
    ring
  rw [hneg] at hs
  linarith

theorem supporting_tangent {f : ℝ → ℝ} {S : Set ℝ} {x y : ℝ}
    (hf : ConvexOn ℝ S f) (hx : x ∈ S) (hy : y ∈ S)
    (hd : DifferentiableAt ℝ f x) :
    f x + deriv f x * (y-x) ≤ f y := by
  rcases lt_trichotomy x y with hxy | hxy | hyx
  · have h := hf.deriv_le_slope hx hy hxy hd
    rw [slope_def_field] at h
    have hh := (le_div_iff₀ (sub_pos.mpr hxy)).mp h
    linarith
  · subst y;simp
  · have h := hf.slope_le_deriv hy hx hyx hd
    rw [slope_def_field] at h
    have hh := (div_le_iff₀ (sub_pos.mpr hyx)).mp h
    nlinarith

theorem differentiable_convex_majorization
    {f : ℝ → ℝ} {S : Set ℝ} {u w : ℕ → ℝ} {m : ℕ}
    (hf : ConvexOn ℝ S f)
    (hd : ∀ x ∈ S, DifferentiableAt ℝ f x)
    (hu : Monotone u) (hus : ∀ i, u i ∈ S)
    (hws : ∀ i, i < m → w i ∈ S)
    (hprefix : ∀ n, n ≤ m → (∑ i ∈ range n, w i) ≤ ∑ i ∈ range n, u i)
    (htotal : (∑ i ∈ range m, u i) = ∑ i ∈ range m, w i) :
    (∑ i ∈ range m, f (u i)) ≤ ∑ i ∈ range m, f (w i) := by
  have hc : Monotone (fun i => deriv f (u i)) := by
    intro i j hij
    exact hf.monotoneOn_deriv hd (hus i) (hus j) (hu hij)
  apply convex_sum_from_tangents hc hprefix htotal
  intro i hi
  exact supporting_tangent hf (hus i) (hws i hi) (hd _ (hus i))

end CollatzConvexCost

/-- info: 'CollatzConvexCost.weighted_prefix_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzConvexCost.weighted_prefix_bound
/-- info: 'CollatzConvexCost.convex_sum_from_tangents' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzConvexCost.convex_sum_from_tangents
/-- info: 'CollatzConvexCost.supporting_tangent' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzConvexCost.supporting_tangent
/-- info: 'CollatzConvexCost.differentiable_convex_majorization' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzConvexCost.differentiable_convex_majorization
