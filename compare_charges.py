#!/usr/bin/env python3
"""
Compare partial charges and C6 coefficients across different systems
to demonstrate the charge equilibration bug in DFTD4.
"""

import json

# Load the three JSON files
with open('C_n_water.json', 'r') as f:
    water = json.load(f)
    
with open('C_n_he.json', 'r') as f:
    water_he = json.load(f)
    
with open('C_n_he_1000.json', 'r') as f:
    water_he_1000 = json.load(f)

print("=" * 85)
print("CHARGE EQUILIBRATION BUG - Quantitative Analysis")
print("=" * 85)
print()

# Extract partial charges
q_water = water['partial_charges']
q_he = water_he['partial_charges']
q_he_1000 = water_he_1000['partial_charges']

print("PARTIAL CHARGES (in atomic units):")
print("-" * 85)
print(f"{'System':<25} {'O charge':<15} {'H1 charge':<15} {'H2 charge':<15} {'He charge':<15}")
print("-" * 85)
print(f"{'Water monomer':<25} {q_water[0]:>14.6f} {q_water[1]:>14.6f} {q_water[2]:>14.6f} {'N/A':<15}")
print(f"{'Water-He (2.29 Å)':<25} {q_he[0]:>14.6f} {q_he[1]:>14.6f} {q_he[2]:>14.6f} {q_he[3]:>14.6f}")
print(f"{'Water-He (1000 Å)':<25} {q_he_1000[0]:>14.6f} {q_he_1000[1]:>14.6f} {q_he_1000[2]:>14.6f} {q_he_1000[3]:>14.6f}")
print("-" * 85)
print()

print("CHARGE DIFFERENCES FROM MONOMER:")
print("-" * 85)
print(f"{'System':<25} {'ΔO charge':<15} {'ΔH1 charge':<15} {'ΔH2 charge':<15} {'He charge':<15}")
print("-" * 85)
delta_o_he = q_he[0] - q_water[0]
delta_h1_he = q_he[1] - q_water[1]
delta_h2_he = q_he[2] - q_water[2]
print(f"{'Water-He (2.29 Å)':<25} {delta_o_he:>14.6f} {delta_h1_he:>14.6f} {delta_h2_he:>14.6f} {q_he[3]:>14.6f}")

delta_o_1000 = q_he_1000[0] - q_water[0]
delta_h1_1000 = q_he_1000[1] - q_water[1]
delta_h2_1000 = q_he_1000[2] - q_water[2]
print(f"{'Water-He (1000 Å)':<25} {delta_o_1000:>14.6f} {delta_h1_1000:>14.6f} {delta_h2_1000:>14.6f} {q_he_1000[3]:>14.6f}")
print("-" * 85)
print()

# Extract C6 coefficients
c6_water = water['c6']
c6_he = water_he['c6']
c6_he_1000 = water_he_1000['c6']

print("C6 COEFFICIENTS (in atomic units):")
print("-" * 85)
print(f"{'System':<25} {'C6(O,H) avg':<20} {'C6(H,H) avg':<20}")
print("-" * 85)

# Water monomer
c6_oh_water = (c6_water[0][1] + c6_water[0][2]) / 2
c6_hh_water = c6_water[1][2]
print(f"{'Water monomer':<25} {c6_oh_water:>19.6f} {c6_hh_water:>19.6f}")

# Water-He at 2.29 Å
c6_oh_he = (c6_he[0][1] + c6_he[0][2]) / 2
c6_hh_he = (c6_he[1][2] + c6_he[1][1] + c6_he[2][1] + c6_he[2][2]) / 4
print(f"{'Water-He (2.29 Å)':<25} {c6_oh_he:>19.6f} {c6_hh_he:>19.6f}")

# Water-He at 1000 Å
c6_oh_1000 = (c6_he_1000[0][1] + c6_he_1000[0][2]) / 2
c6_hh_1000 = (c6_he_1000[1][2] + c6_he_1000[1][1] + c6_he_1000[2][1] + c6_he_1000[2][2]) / 4
print(f"{'Water-He (1000 Å)':<25} {c6_oh_1000:>19.6f} {c6_hh_1000:>19.6f}")
print("-" * 85)
print()

print("C6 DIFFERENCES FROM MONOMER:")
print("-" * 85)
print(f"{'System':<25} {'ΔC6(O,H)':<20} {'ΔC6(H,H)':<20} {'% error O-H':<15} {'% error H-H':<15}")
print("-" * 85)

delta_c6oh_he = c6_oh_he - c6_oh_water
delta_c6hh_he = c6_hh_he - c6_hh_water
pct_oh_he = 100 * delta_c6oh_he / c6_oh_water
pct_hh_he = 100 * delta_c6hh_he / c6_hh_water
print(f"{'Water-He (2.29 Å)':<25} {delta_c6oh_he:>19.6f} {delta_c6hh_he:>19.6f} {pct_oh_he:>14.3f}% {pct_hh_he:>14.3f}%")

delta_c6oh_1000 = c6_oh_1000 - c6_oh_water
delta_c6hh_1000 = c6_hh_1000 - c6_hh_water
pct_oh_1000 = 100 * delta_c6oh_1000 / c6_oh_water
pct_hh_1000 = 100 * delta_c6hh_1000 / c6_hh_water
print(f"{'Water-He (1000 Å)':<25} {delta_c6oh_1000:>19.6f} {delta_c6hh_1000:>19.6f} {pct_oh_1000:>14.3f}% {pct_hh_1000:>14.3f}%")
print("-" * 85)
print()

print("KEY FINDINGS:")
print("-" * 85)
print(f"1. At 1000 Å, oxygen charge differs from monomer by {abs(delta_o_1000):.4f} au ({abs(100*delta_o_1000/q_water[0]):.2f}%)")
print(f"2. At 1000 Å, helium has accumulated {q_he_1000[3]:.4f} electrons from water")
print(f"3. At 1000 Å, C6(O-H) differs from monomer by {abs(delta_c6oh_1000):.4f} au ({abs(pct_oh_1000):.2f}%)")
print(f"4. At 1000 Å, C6(H-H) differs from monomer by {abs(delta_c6hh_1000):.4f} au ({abs(pct_hh_1000):.2f}%)")
print()
print("CONCLUSION: The partial charges and C6 values DO NOT converge to monomer")
print("            values even at 1000 Å separation, confirming the charge")
print("            equilibration bug.")
print("=" * 85)
