import Mathlib.Analysis.Convex.Deriv
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Tactic

/-!
Convexity and monotonicity of the reciprocal exponential cost used in the
cycle inequality. Setting c=log(2) gives 1/(2^x-1) on positive heights.
-/

namespace CollatzReciprocalCost

noncomputable def cost (c x : ℝ) : ℝ := (Real.exp (c*x)-1)⁻¹
noncomputable def first (c x : ℝ) : ℝ := -(c*Real.exp (c*x))/(Real.exp (c*x)-1)^2
noncomputable def second (c x : ℝ) : ℝ :=
  c^2*Real.exp (c*x)*(Real.exp (c*x)+1)/(Real.exp (c*x)-1)^3

theorem denominator_pos {c x : ℝ} (hc : 0 < c) (hx : 0 < x) :
    0 < Real.exp (c*x)-1 := by
  exact sub_pos.mpr (Real.one_lt_exp_iff.mpr (mul_pos hc hx))

theorem cost_hasDerivAt {c x : ℝ} (hc : 0 < c) (hx : 0 < x) :
    HasDerivAt (cost c) (first c x) x := by
  have hn := ne_of_gt (denominator_pos hc hx)
  have he : HasDerivAt (fun z : ℝ => Real.exp (c*z)) (Real.exp (c*x)*c) x := by
    simpa only [id_eq, mul_one] using ((hasDerivAt_id x).const_mul c).exp
  unfold cost first
  convert ((he.sub_const 1).inv hn) using 1
  ring

theorem first_hasDerivAt {c x : ℝ} (hc : 0 < c) (hx : 0 < x) :
    HasDerivAt (first c) (second c x) x := by
  have hn := ne_of_gt (denominator_pos hc hx)
  have he : HasDerivAt (fun z : ℝ => Real.exp (c*z)) (Real.exp (c*x)*c) x := by
    simpa only [id_eq, mul_one] using ((hasDerivAt_id x).const_mul c).exp
  convert ((he.const_mul c).div ((he.sub_const 1).pow 2) (pow_ne_zero 2 hn)).neg using 1
  · funext z
    dsimp [first]
    ring
  · dsimp [second]
    field_simp
    ring

theorem cost_antitone {c : ℝ} (hc : 0 < c) :
    AntitoneOn (cost c) (Set.Ioi 0) := by
  have hd : DifferentiableOn ℝ (cost c) (Set.Ioi 0) :=
    fun x hx => (cost_hasDerivAt hc hx).differentiableAt.differentiableWithinAt
  apply antitoneOn_of_deriv_nonpos (convex_Ioi 0) hd.continuousOn
    (hd.mono interior_subset)
  intro x hx
  have hx0 : 0 < x := interior_subset hx
  rw [(cost_hasDerivAt hc hx0).deriv]
  unfold first
  apply div_nonpos_of_nonpos_of_nonneg
  · exact neg_nonpos.mpr (mul_nonneg (le_of_lt hc) (le_of_lt (Real.exp_pos _)))
  · positivity

theorem cost_convex {c : ℝ} (hc : 0 < c) :
    ConvexOn ℝ (Set.Ioi 0) (cost c) := by
  have hd : DifferentiableOn ℝ (cost c) (Set.Ioi 0) :=
    fun x hx => (cost_hasDerivAt hc hx).differentiableAt.differentiableWithinAt
  have hd1 : DifferentiableOn ℝ (first c) (Set.Ioi 0) :=
    fun x hx => (first_hasDerivAt hc hx).differentiableAt.differentiableWithinAt
  have hmono : MonotoneOn (first c) (Set.Ioi 0) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ioi 0) hd1.continuousOn
      (hd1.mono interior_subset)
    intro x hx
    have hx0 : 0 < x := interior_subset hx
    rw [(first_hasDerivAt hc hx0).deriv]
    unfold second
    have hpos := denominator_pos hc hx0
    positivity
  apply MonotoneOn.convexOn_of_deriv (convex_Ioi 0) hd.continuousOn
    (hd.mono interior_subset)
  intro x hx y hy hxy
  have hx0 : 0 < x := interior_subset hx
  have hy0 : 0 < y := interior_subset hy
  rw [(cost_hasDerivAt hc hx0).deriv, (cost_hasDerivAt hc hy0).deriv]
  exact hmono hx0 hy0 hxy

theorem binary_cost_convex :
    ConvexOn ℝ (Set.Ioi 0) (fun x : ℝ => 1 / ((2 : ℝ)^x-1)) := by
  have heq : (fun x : ℝ => 1 / ((2 : ℝ)^x-1)) = cost (Real.log 2) := by
    funext x
    simp only [cost, Real.rpow_def_of_pos (by norm_num : (0 : ℝ) < 2), one_div]
  rw [heq]
  exact cost_convex (Real.log_pos (by norm_num : (1 : ℝ) < 2))

theorem binary_cost_antitone :
    AntitoneOn (fun x : ℝ => 1 / ((2 : ℝ)^x-1)) (Set.Ioi 0) := by
  have heq : (fun x : ℝ => 1 / ((2 : ℝ)^x-1)) = cost (Real.log 2) := by
    funext x
    simp only [cost, Real.rpow_def_of_pos (by norm_num : (0 : ℝ) < 2), one_div]
  rw [heq]
  exact cost_antitone (Real.log_pos (by norm_num : (1 : ℝ) < 2))

end CollatzReciprocalCost

/-- info: 'CollatzReciprocalCost.denominator_pos' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzReciprocalCost.denominator_pos
/-- info: 'CollatzReciprocalCost.cost_hasDerivAt' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzReciprocalCost.cost_hasDerivAt
/-- info: 'CollatzReciprocalCost.first_hasDerivAt' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzReciprocalCost.first_hasDerivAt
/-- info: 'CollatzReciprocalCost.cost_antitone' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzReciprocalCost.cost_antitone
/-- info: 'CollatzReciprocalCost.cost_convex' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzReciprocalCost.cost_convex

/-- info: 'CollatzReciprocalCost.binary_cost_convex' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzReciprocalCost.binary_cost_convex
/-- info: 'CollatzReciprocalCost.binary_cost_antitone' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzReciprocalCost.binary_cost_antitone
