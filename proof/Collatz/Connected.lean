import Collatz.Construction
import Collatz.Legacy.CollatzRestart
import Collatz.Legacy.CollatzRetainedLoss
import Collatz.Legacy.CollatzAffineEnvelope

/-!
# Connected, conditional block-growth theorem

The only unproved mathematical input to `block_growth_of_local_loss` is the
explicit local certificate below. It is the conclusion of Sections 2--5 of
the manuscript, including the external p-adic interpolation theorem. It is
NOT asserted here as an axiom or silently discharged by numerical checks.
The formal argument connects arithmetic blocks, elementary logarithmic
bounds, rounding, restart induction and the 32-step virtual warmup.
-/
namespace Collatz

noncomputable def lambda : ℝ := delta - 1/80
noncomputable def envelopeConstant : ℝ := (delta / lambda)^32
noncomputable def growth : ℝ → ℝ :=
  CollatzGlobalEnvelope.growth delta lambda 1272000

/-- The analytic specialization still to be formalized. Divisibility and
size restrictions on J are part of the hypothesis, not informal comments. -/
def LocalLossCertificate (o : BlockOrbit) : Prop :=
  ∀ (i J : ℕ), 100 ∣ J → 10000 ≤ J → (159/2 : ℝ)*J ≤ o.height i →
    o.height (i+1) ≤ delta*o.height i - J ∨
    (o.run (i+1) ≤ delta*o.height i - J ∧
      o.height (i+2) ≤ delta^2*o.height i - (16/5 : ℝ)*J)

lemma lambda_bounds : (157 : ℝ)/100 ≤ lambda ∧ lambda ≤ delta := by
  unfold lambda
  constructor <;> linarith [CollatzGlobalEnvelope.delta_bounds.1]

lemma growth_monotone : Monotone growth :=
  CollatzGlobalEnvelope.growth_monotone
    (by linarith [CollatzGlobalEnvelope.delta_bounds.1])
    (by linarith [lambda_bounds.1])

lemma growth_upper (x : ℝ) : growth x ≤ delta*x :=
  CollatzGlobalEnvelope.growth_upper
    (by linarith [CollatzGlobalEnvelope.delta_bounds.1]) lambda_bounds.2 (by norm_num)

lemma growth_lower (x : ℝ) (hx : 0 ≤ x) : lambda*x ≤ growth x := by
  unfold growth CollatzGlobalEnvelope.growth
  split_ifs
  · exact mul_le_mul_of_nonneg_right lambda_bounds.2 hx
  · exact le_max_left _ _

lemma growth_tail (x : ℝ) (hx : (103 : ℝ)/100*1272000 ≤ x) :
    growth x = lambda*x := by
  have hlam : 1 ≤ lambda := by linarith [lambda_bounds.1]
  have hjoin : (delta-1)*1272000 ≤ (lambda-1)*((103 : ℝ)/100*1272000) := by
    unfold lambda
    linarith [CollatzGlobalEnvelope.delta_bounds.1]
  have hp := mul_le_mul_of_nonneg_left hx (sub_nonneg.mpr hlam)
  unfold growth CollatzGlobalEnvelope.growth
  rw [ite_eq_right (by linarith : ¬ x ≤ 1272000), max_eq_left (by nlinarith)]

theorem rounded_loss_scale {y : ℝ} (hy : 1272000 ≤ y) :
    ∃ J : ℕ, 100 ∣ J ∧ 10000 ≤ J ∧ (159/2 : ℝ)*J ≤ y ∧ y/80 ≤ J := by
  let q : ℕ := ⌊y/7950⌋₊
  have hy0 : 0 ≤ y/7950 := by positivity
  have hq : (q : ℝ) ≤ y/7950 := Nat.floor_le hy0
  have hq' : y/7950 < (q : ℝ)+1 := Nat.lt_floor_add_one _
  have hq100 : 100 ≤ q := by
    have hqr : (100 : ℝ) ≤ q := by linarith
    exact_mod_cast hqr
  refine ⟨100*q, dvd_mul_right 100 q, by omega, ?_, ?_⟩
  · push_cast
    nlinarith
  · push_cast
    linarith

theorem restart_of_local_loss (o : BlockOrbit) (h : LocalLossCertificate o) (i : ℕ) :
    o.height (i+1) ≤ growth (o.height i) ∨
    (o.run (i+1) ≤ growth (o.height i) ∧
      o.height (i+2) ≤ growth (growth (o.height i))) := by
  by_cases hy : o.height i ≤ 1272000
  · left
    simpa only [growth, CollatzGlobalEnvelope.growth, ite_eq_left hy] using o.height_step i
  · have hy0 : 0 ≤ o.height i := by linarith [o.height_ge_one i]
    obtain ⟨J, hdiv, hJ, hheight, hloss⟩ := rounded_loss_scale (le_of_lt (lt_of_not_ge hy))
    have hlam : 0 ≤ lambda := by linarith [lambda_bounds.1]
    have hbase := growth_lower (o.height i) hy0
    have hfirst : delta*o.height i - J ≤ lambda*o.height i := by
      unfold lambda
      linarith
    rcases h i J hdiv hJ hheight with hone | htwo
    · exact Or.inl (hone.trans (hfirst.trans hbase))
    · refine Or.inr ⟨htwo.1.trans (hfirst.trans hbase), ?_⟩
      have hg0 : 0 ≤ growth (o.height i) := (mul_nonneg hlam hy0).trans hbase
      have hsecond := growth_lower (growth (o.height i)) hg0
      have hmul := mul_le_mul_of_nonneg_left hbase hlam
      have hcoefficient : 0 ≤ (16/5 : ℝ)/80 - (2*delta/80 - 1/80^2) := by
        linarith [CollatzGlobalEnvelope.delta_bounds.2]
      have hmargin := mul_nonneg hcoefficient hy0
      have hJmul := mul_le_mul_of_nonneg_left hloss (by norm_num : (0 : ℝ) ≤ 16/5)
      have ht : o.height (i+2) ≤ lambda^2*o.height i := by
        dsimp [lambda]
        nlinarith [htwo.2]
      nlinarith

noncomputable def virtualHeight (y : ℝ) : ℕ → ℝ
  | 0 => y
  | n+1 => growth (virtualHeight y n)

theorem virtual_bound {v : ℕ → ℝ} (hv0 : 1 ≤ v 0)
    (hstep : ∀ n, v (n+1) = growth (v n)) :
    ∀ t, v t ≤ envelopeConstant*v 0*lambda^t := by
  have hlam : 0 < lambda := by linarith [lambda_bounds.1]
  have hd : 0 ≤ delta := by linarith [CollatzGlobalEnvelope.delta_bounds.1]
  have hv0' : 0 ≤ v 0 := by linarith
  have hu := CollatzGlobalEnvelope.virtual_upper hd hstep growth_upper
  have hlo := CollatzGlobalEnvelope.virtual_lower (by norm_num : (0 : ℝ) ≤ 157/100)
    hv0' hstep (fun x hx =>
      (mul_le_mul_of_nonneg_right lambda_bounds.1 hx).trans (growth_lower x hx))
  have hN : (103 : ℝ)/100*1272000 ≤ v 32 := by
    have hp := mul_le_mul_of_nonneg_left hv0 (by positivity : (0 : ℝ) ≤ (157/100 : ℝ)^32)
    have hn := (hlo 32).1
    have hc : (103 : ℝ)/100*1272000 ≤ (157/100 : ℝ)^32 := by norm_num
    nlinarith
  have ht := CollatzGlobalEnvelope.virtual_tail (by linarith [lambda_bounds.1] : 1 ≤ lambda)
    (by norm_num : (0 : ℝ) ≤ 103/100*1272000) hN hstep growth_tail
  exact CollatzGlobalEnvelope.finite_warmup_bound hlam lambda_bounds.2 hv0' hu
    (fun s => (ht s).1)

/-- Manuscript Theorem 1, conditional on its unformalized local analytic
certificate. The input is a natural-number block sequence, not arbitrary
real heights. No certificate is constructed by this theorem. -/
theorem block_growth_of_local_loss (o : BlockOrbit) (h : LocalLossCertificate o) :
    (∀ t, o.run t ≤ envelopeConstant*o.height 0*lambda^t) ∧
    (∀ t, o.height (t+1) ≤ delta*envelopeConstant*o.height 0*lambda^t) := by
  let v := virtualHeight (o.height 0)
  have hv : ∀ n, v (n+1) = growth (v n) := fun _ => rfl
  have hzero : o.height 0 ≤ v 0 := le_rfl
  have hlocal := restart_of_local_loss o h
  have hr := CollatzRestart.run_bound growth_monotone hv hzero o.run_le_height hlocal
  have hh := CollatzRestart.height_bound
    (by linarith [CollatzGlobalEnvelope.delta_bounds.1] : 0 ≤ delta)
    growth_monotone growth_upper hv hzero o.height_step hlocal
  have hbound := virtual_bound (show 1 ≤ v 0 from o.height_ge_one 0) hv
  constructor
  · intro t
    exact (hr t).trans (hbound t)
  · intro t
    have hm := mul_le_mul_of_nonneg_left (hbound t)
      (by linarith [CollatzGlobalEnvelope.delta_bounds.1] : 0 ≤ delta)
    calc
      o.height (t+1) ≤ delta*v t := hh t
      _ ≤ delta*(envelopeConstant*o.height 0*lambda^t) := hm
      _ = delta*envelopeConstant*o.height 0*lambda^t := by ring

/-- The encoded block starts are actual shortcut iterates, and their
growth satisfies the manuscript bound under the explicit local certificate. -/
theorem block_trajectory_and_growth (o : BlockOrbit) (h : LocalLossCertificate o) :
    (∀ i, shortcut^[o.time i] (o.n 0) = o.n i) ∧
    (∀ t, o.run t ≤ envelopeConstant*o.height 0*lambda^t) ∧
    (∀ t, o.height (t+1) ≤ delta*envelopeConstant*o.height 0*lambda^t) :=
  ⟨o.is_trajectory, block_growth_of_local_loss o h⟩

/-- Every positive odd starting value has the represented trajectory;
the only analytic input here is its explicitly stated local certificate. -/
theorem odd_start_growth (s : OddStart) (h : LocalLossCertificate (orbitOfOdd s)) :
    (∀ i, shortcut^[(orbitOfOdd s).time i] s.value = (orbitOfOdd s).n i) ∧
    (∀ t, (orbitOfOdd s).run t ≤
      envelopeConstant*(Real.log ((s.value : ℝ)+1)/Real.log 2)*lambda^t) ∧
    (∀ t, (orbitOfOdd s).height (t+1) ≤
      delta*envelopeConstant*(Real.log ((s.value : ℝ)+1)/Real.log 2)*lambda^t) :=
  block_trajectory_and_growth (orbitOfOdd s) h

end Collatz

/-- info: 'Collatz.block_growth_of_local_loss' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Collatz.block_growth_of_local_loss

/-- info: 'Collatz.block_trajectory_and_growth' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Collatz.block_trajectory_and_growth

/-- info: 'Collatz.odd_start_growth' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Collatz.odd_start_growth
