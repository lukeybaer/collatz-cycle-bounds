import Mathlib.Tactic
namespace CollatzRetainedLoss

theorem margin_1 : (0 : ℝ) <
  16*((301 : ℝ)/50)*(34657359/50000000)-((301 : ℝ)/50)*((223249 : ℝ)/50000)-39/10000
    -5*(((15053 : ℝ)/15000)*4*(109861229/100000000)+((75265 : ℝ)/22578)*((1871705357157 : ℝ)/1750000000000)) := by
  norm_num

theorem margin_2 : (0 : ℝ) <
  16*((196 : ℝ)/25)*(34657359/50000000)-((196 : ℝ)/25)*((255541 : ℝ)/50000)-39/10000
    -5*(((19603 : ℝ)/15000)*4*(109861229/100000000)+((98015 : ℝ)/29403)*((1871705357157 : ℝ)/1750000000000)) := by
  norm_num

theorem margin_3 : (0 : ℝ) <
  16*((61 : ℝ)/10)*(34657359/50000000)-((61 : ℝ)/10)*((409441 : ℝ)/100000)-39/10000
    -5*(((76301 : ℝ)/67500)*4*(109861229/100000000)+((76301 : ℝ)/25428)*((2079649514157 : ℝ)/1750000000000)) := by
  norm_num

theorem margin_4 : (0 : ℝ) <
  16*((613 : ℝ)/100)*(34657359/50000000)-((613 : ℝ)/100)*((12817 : ℝ)/3125)-39/10000
    -5*(((153577 : ℝ)/135000)*4*(109861229/100000000)+((153577 : ℝ)/51156)*((2079649514157 : ℝ)/1750000000000)) := by
  norm_num

theorem margin_5 : (0 : ℝ) <
  16*((621 : ℝ)/100)*(34657359/50000000)-((621 : ℝ)/100)*((414871 : ℝ)/100000)-39/10000
    -5*(((5751 : ℝ)/5000)*4*(109861229/100000000)+((51759 : ℝ)/17252)*((2079649514157 : ℝ)/1750000000000)) := by
  norm_num

theorem margin_6 : (0 : ℝ) <
  16*((331 : ℝ)/50)*(34657359/50000000)-((331 : ℝ)/50)*((216109 : ℝ)/50000)-39/10000
    -5*(((165677 : ℝ)/135000)*4*(109861229/100000000)+((165677 : ℝ)/55206)*((2079649514157 : ℝ)/1750000000000)) := by
  norm_num

theorem margin_7 : (0 : ℝ) <
  16*((847 : ℝ)/100)*(34657359/50000000)-((847 : ℝ)/100)*((31463 : ℝ)/6250)-39/10000
    -5*(((42431 : ℝ)/30000)*4*(109861229/100000000)+((212155 : ℝ)/63606)*((2079649514157 : ℝ)/1750000000000)) := by
  norm_num

theorem numeric_losses :
  (1 : ℝ) < ((896723 : ℝ)/160000) ∧
  (16 : ℝ)/5 < ((0 : ℝ)/1)+(46797/80000)*((896723 : ℝ)/160000) ∧
  (1 : ℝ) < ((44128077 : ℝ)/8000000) ∧
  (16 : ℝ)/5 < ((0 : ℝ)/1)+(46797/80000)*((44128077 : ℝ)/8000000) ∧
  (1 : ℝ) < ((640723 : ℝ)/160000) ∧
  (16 : ℝ)/5 < ((9 : ℝ)/10)+(46797/80000)*((640723 : ℝ)/160000) ∧
  (1 : ℝ) < ((6588403 : ℝ)/1600000) ∧
  (16 : ℝ)/5 < ((9 : ℝ)/10)+(46797/80000)*((6588403 : ℝ)/1600000) ∧
  (1 : ℝ) < ((8110331 : ℝ)/2000000) ∧
  (16 : ℝ)/5 < ((9 : ℝ)/10)+(46797/80000)*((8110331 : ℝ)/2000000) ∧
  (1 : ℝ) < ((31634591 : ℝ)/8000000) ∧
  (16 : ℝ)/5 < ((9 : ℝ)/10)+(46797/80000)*((31634591 : ℝ)/8000000) ∧
  (1 : ℝ) < ((32339571 : ℝ)/8000000) ∧
  (16 : ℝ)/5 < ((9 : ℝ)/10)+(46797/80000)*((32339571 : ℝ)/8000000) := by
  norm_num

theorem retained_local_loss {delta y s loss J a g y2 : ℝ}
    (hd : (126797 : ℝ)/80000 ≤ delta) (hJ : 0 ≤ J)
    (hg : 1 ≤ g) (hgap : g*J ≤ delta*y-s)
    (hloss : a*J ≤ loss) (hc : (16 : ℝ)/5 ≤ a+(46797/80000)*g)
    (hy2 : y2 ≤ delta*y-loss+(delta-1)*s) :
    s ≤ delta*y-J ∧ y2 ≤ delta^2*y-(16/5)*J := by
  have hgap0 : 0 ≤ delta*y-s := by nlinarith
  have hb : (46797 : ℝ)/80000 ≤ delta-1 := by linarith
  have h1 := mul_le_mul_of_nonneg_left hgap (by norm_num : (0 : ℝ) ≤ 46797/80000)
  have h2 := mul_le_mul_of_nonneg_right hb hgap0
  have h3 := mul_le_mul_of_nonneg_right hc hJ
  have hp : (16 : ℝ)/5*J ≤ loss+(delta-1)*(delta*y-s) := by nlinarith
  have hid : delta*y-loss+(delta-1)*s = delta^2*y-(loss+(delta-1)*(delta*y-s)) := by ring
  constructor
  · nlinarith
  · linarith

theorem rounding_and_warmup :
    (159 : ℝ)/2/80 < 1 ∧
    (159 : ℝ)/2*10000 ≤ 1272000 ∧
    100*((159 : ℝ)/2)/(1-(159/2)/80) = 1272000 ∧
    (103 : ℕ)*1272000*100^31 < 157^32 := by
  norm_num

end CollatzRetainedLoss

/-- info: 'CollatzRetainedLoss.margin_1' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzRetainedLoss.margin_1
/-- info: 'CollatzRetainedLoss.margin_2' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzRetainedLoss.margin_2
/-- info: 'CollatzRetainedLoss.margin_3' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzRetainedLoss.margin_3
/-- info: 'CollatzRetainedLoss.margin_4' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzRetainedLoss.margin_4
/-- info: 'CollatzRetainedLoss.margin_5' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzRetainedLoss.margin_5
/-- info: 'CollatzRetainedLoss.margin_6' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzRetainedLoss.margin_6
/-- info: 'CollatzRetainedLoss.margin_7' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzRetainedLoss.margin_7
/-- info: 'CollatzRetainedLoss.numeric_losses' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzRetainedLoss.numeric_losses
/-- info: 'CollatzRetainedLoss.retained_local_loss' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzRetainedLoss.retained_local_loss
/-- info: 'CollatzRetainedLoss.rounding_and_warmup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms CollatzRetainedLoss.rounding_and_warmup
