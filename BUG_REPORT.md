# DFTD4 Charge Equilibration Bug Report

## Summary

The pairwise C6 coefficients for water **do not converge** to the isolated monomer values when a helium atom is moved to 1000 Å away. This indicates a fundamental bug in the charge equilibration (EEQ) implementation where charges are computed globally across the entire system without distance-based cutoffs or fragment detection.

## Implementation Details

### Modified Files

**File:** `src/dftd4/output.f90`

**Changes Made:**
1. Added new subroutine `print_values_1d_wp()` to format 1D arrays for JSON output (lines 155-180)
2. Modified `ascii_system_properties()` to include partial charges in C_n.json output (line 280)

**New JSON Output Structure:**
```json
{
  "c6": [[matrix]],
  "c8": [[matrix]],
  "partial_charges": [array]
}
```

## Bug Evidence

### Quantitative Analysis

| System | O charge (au) | H charge (au) | He charge (au) | C6(O-H) (au) | C6(H-H) (au) |
|--------|---------------|---------------|----------------|--------------|--------------|
| **Water monomer (reference)** | -0.5848 | +0.2924 | N/A | 4.2053 | 0.7445 |
| **Water-He @ 2.29 Å** | -0.5875 | +0.2910 | +0.0063 | 4.2268 | 0.7502 |
| **Water-He @ 1000 Å** | **-0.5929** | **+0.2891** | **+0.0147** | **4.2509** | **0.7548** |

### Key Findings

1. **At 1000 Å separation** (far beyond any physical interaction range):
   - Oxygen charge differs from monomer by **0.0082 au (1.40%)**
   - Hydrogen charges differ from monomer by **0.0033 au (1.13%)**
   - Helium has accumulated **0.0147 electrons** from water
   - C6(O-H) differs from monomer by **0.0456 au (1.08%)**
   - C6(H-H) differs from monomer by **0.0103 au (1.39%)**

2. **Expected behavior:** At 1000 Å, all properties should converge to monomer values within numerical precision (~10⁻¹² au)

3. **Actual behavior:** Significant deviations persist, indicating unphysical long-range charge transfer

## Root Cause Analysis

### Location of Bug

The issue originates in the charge equilibration routine from the `multicharge` module:

**File:** `src/dftd4/disp.f90` (lines 124, 224, 277)
```fortran
call get_charges(disp%mchrg, mol, error, q, dqdr, dqdL)
```

### Mechanism

1. **Global Charge Equilibration:** The `get_charges()` routine performs electronegativity equilibration (EEQ) across the **entire molecular system** without considering distance-based cutoffs

2. **Charge → C6 Coupling:** The partial charges affect C6 coefficients through the `zeta()` weighting function:
   ```fortran
   ! In weight_references() (d4.f90:311, 369)
   gwvec(iref, iat, 1) = gwk * zeta(self%ga, gi, self%q(iref, izp)+zi, q(iat)+zi)
   ```

3. **C6 Calculation:** The atomic C6 values are computed using these charge-dependent weights:
   ```fortran
   ! In get_atomic_c6() (d4.f90:462)
   dc6 = dc6 + gwvec(iref, iat, 1) * gwvec(jref, jat, 1) * refc6
   ```

4. **Error Propagation:** Even though helium is 1000 Å away:
   - EEQ redistributes charges globally
   - He accumulates +0.0147 e⁻ from water
   - Water's charge distribution changes
   - Changed charges modify C6 via zeta function
   - Dispersion energies are computed with incorrect C6 values

### Missing Features

The charge equilibration lacks:
1. **Distance-based cutoffs** for charge transfer
2. **Fragment detection** to identify non-interacting subsystems  
3. **Asymptotic convergence** to monomer limits at large separation
4. **Size-consistency** checks

## Physical Implications

This bug causes DFTD4 to incorrectly predict:

1. **Unphysical charge transfer** at arbitrarily large distances
2. **Non-converging potential energy surfaces** - dissociation curves won't reach proper asymptotic limits
3. **System-dependent monomer properties** - a molecule's dispersion properties depend on what other species exist in the system, even at 1000 Å away
4. **Violation of size-consistency** - E(A...B at ∞) ≠ E(A) + E(B)
5. **Incorrect dispersion energies** for weakly-bound complexes

## Impact Assessment

### Affected Calculations

- ✗ Dissociation/binding curves (wrong asymptotic behavior)
- ✗ Weakly-bound molecular complexes  
- ✗ Supramolecular systems with multiple fragments
- ✗ Any calculation assuming fragment separability
- ✓ Tightly-bound molecules (minimal impact if no distant fragments present)

### Severity

**CRITICAL** - Violates fundamental physical principles (size-extensivity, fragment separability)

## Recommended Fixes

### Option 1: Fragment Detection (Recommended)

Implement automatic fragment detection based on connectivity/distance and perform charge equilibration independently for each fragment:

```fortran
! Pseudocode
subroutine get_charges_with_fragments(mol, q, ...)
   ! 1. Detect fragments based on distance cutoff (e.g., 10 Å)
   call detect_fragments(mol, fragments, cutoff=10.0_wp)
   
   ! 2. Perform EEQ independently for each fragment
   do ifrag = 1, nfragments
      call get_charges_fragment(fragments(ifrag), q_frag)
      q(fragments(ifrag)%atoms) = q_frag
   end do
end subroutine
```

### Option 2: Distance-Damped Charge Transfer

Modify the charge equilibration matrix to include distance-dependent damping:

```fortran
! Damp off-diagonal elements based on distance
do iat = 1, nat
   do jat = 1, nat
      rij = distance(iat, jat)
      damping = damping_function(rij, cutoff)
      matrix(iat, jat) = matrix(iat, jat) * damping
   end do
end do
```

### Option 3: User-Specified Fragments

Allow users to specify fragment boundaries via input:

```fortran
! Example: .FRAGMENTS file
# Fragment 1: atoms 1-3 (water)
# Fragment 2: atom 4 (helium)
```

## Testing Plan

1. **Convergence test:** Verify that properties converge to monomer values as fragments separate
2. **Size-consistency test:** Check that E(A...B at R→∞) = E(A) + E(B)
3. **Regression tests:** Ensure existing functionality is preserved
4. **Performance tests:** Measure impact on computational cost

## Verification

To verify the bug is fixed, run the test case:

```bash
bash build.sh
python3 compare_charges.py
```

Expected output after fix:
- At 1000 Å: |Δq| < 10⁻⁸ au (numerical precision)
- At 1000 Å: |ΔC6| < 10⁻⁸ au (numerical precision)
- He charge ≈ 0 at all distances > 10 Å

## References

- **Code locations:**
  - Charge equilibration: `src/dftd4/disp.f90:124,224,277`
  - Weight function: `src/dftd4/model/d4.f90:234-374`
  - C6 calculation: `src/dftd4/model/d4.f90:379-471`
  - JSON output: `src/dftd4/output.f90:155-283`

- **Test files:**
  - `water.xyz` - water monomer
  - `water_he.xyz` - water-He at 2.29 Å
  - `water_he_1000.xyz` - water-He at 1000 Å

- **Output files:**
  - `C_n_water.json` - monomer properties
  - `C_n_he.json` - close dimer properties
  - `C_n_he_1000.json` - distant dimer properties (shows bug)

---

**Date:** 2026-02-06  
**Discovered by:** Bug analysis of C6 convergence behavior  
**Status:** CONFIRMED - Awaiting fix
