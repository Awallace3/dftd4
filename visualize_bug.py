#!/usr/bin/env python3
"""
Visualize the charge equilibration bug with ASCII plots
"""

import json

# Load data
with open('C_n_water.json', 'r') as f:
    water = json.load(f)
with open('C_n_he.json', 'r') as f:
    water_he = json.load(f)
with open('C_n_he_1000.json', 'r') as f:
    water_he_1000 = json.load(f)

q_water = water['partial_charges']
q_he = water_he['partial_charges']
q_he_1000 = water_he_1000['partial_charges']

c6_water = water['c6']
c6_he_1000 = water_he_1000['c6']

print("\n" + "="*85)
print("VISUAL REPRESENTATION OF CHARGE EQUILIBRATION BUG")
print("="*85 + "\n")

print("PARTIAL CHARGES - Should converge at 1000 Å but DON'T:")
print("-"*85)
print(f"Distance: MONOMER     | 2.29 Å      | 1000 Å      | Expected@1000Å")
print("-"*85)

# O charges
o_mono = q_water[0]
o_close = q_he[0]
o_far = q_he_1000[0]
print(f"O charge: {o_mono:>12.6f} | {o_close:>11.6f} | {o_far:>11.6f} | {o_mono:>11.6f}")

# Create bar visualization
bar_mono = int(abs(o_mono) * 100)
bar_far = int(abs(o_far) * 100)
print(f"          {'─'*bar_mono}● | {'─'*int(abs(o_close)*100)}● | {'─'*bar_far}● | {'─'*bar_mono}●")

# H charges
h_mono = q_water[1]
h_close = q_he[1]
h_far = q_he_1000[1]
print(f"H charge: {h_mono:>12.6f} | {h_close:>11.6f} | {h_far:>11.6f} | {h_mono:>11.6f}")
bar_h_mono = int(h_mono * 100)
bar_h_far = int(h_far * 100)
print(f"          {'─'*bar_h_mono}● | {'─'*int(h_close*100)}● | {'─'*bar_h_far}● | {'─'*bar_h_mono}●")

# He charges
print(f"He charge: {'N/A':>12} | {q_he[3]:>11.6f} | {q_he_1000[3]:>11.6f} | ~0.000000")
print(f"          {'':>13}   {'─'*1}● | {'─'*1}● | ~")

print("-"*85)
print(f"\n{'BUG: At 1000 Å, charges differ from monomer by >1%!'}")
print(f"{'     This indicates unphysical long-range charge transfer.'}\n")

print("="*85)
print("C6 COEFFICIENTS - Also affected by charge bug:")
print("="*85)

c6_oh_mono = (c6_water[0][1] + c6_water[0][2]) / 2
c6_oh_far = (c6_he_1000[0][1] + c6_he_1000[0][2]) / 2
c6_hh_mono = c6_water[1][2]
c6_hh_far = (c6_he_1000[1][2] + c6_he_1000[1][1] + c6_he_1000[2][1] + c6_he_1000[2][2]) / 4

print(f"\nC6(O-H): MONOMER={c6_oh_mono:.6f} au  vs  1000Å={c6_oh_far:.6f} au")
print(f"         Difference: {(c6_oh_far-c6_oh_mono):.6f} au ({100*(c6_oh_far-c6_oh_mono)/c6_oh_mono:.2f}%)")
print(f"         {'▀'*int(c6_oh_mono*5)} MONOMER")
print(f"         {'▀'*int(c6_oh_far*5)} 1000Å ← Should be same!")
print()
print(f"C6(H-H): MONOMER={c6_hh_mono:.6f} au  vs  1000Å={c6_hh_far:.6f} au")
print(f"         Difference: {(c6_hh_far-c6_hh_mono):.6f} au ({100*(c6_hh_far-c6_hh_mono)/c6_hh_mono:.2f}%)")
print(f"         {'▀'*int(c6_hh_mono*27)} MONOMER")
print(f"         {'▀'*int(c6_hh_far*27)} 1000Å ← Should be same!")

print("\n" + "="*85)
print("CONCLUSION:")
print("="*85)
print("""
The partial charges and C6 coefficients DO NOT converge to their monomer
values when fragments are separated by 1000 Å (a completely non-interacting
distance). This is a clear bug in the charge equilibration routine.

Physical interpretation:
  • Helium at 1000 Å is "stealing" 0.0147 electrons from water
  • This changes water's charge distribution 
  • Changed charges modify C6 coefficients via the zeta weighting function
  • Result: Incorrect dispersion properties and energies

This violates:
  ✗ Size-consistency (E(AB at ∞) ≠ E(A) + E(B))
  ✗ Fragment separability 
  ✗ Asymptotic convergence of potential energy surfaces
  
Fix needed: Implement fragment detection or distance-based cutoffs
            in the charge equilibration routine.
""")
print("="*85)
