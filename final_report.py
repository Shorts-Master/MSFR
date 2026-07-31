import pandas as pd
import numpy as np
import os

print("="*70)
print("MSFR PRECURSOR DRIFT MODEL - FINAL CONSOLIDATED REPORT")
print("="*70)

print("""
GEOMETRY: 2D axisymmetric (RZ), Ra=112cm, Ha=224cm
          (EVOL/MARS benchmark, Brovchenko et al.)
KINETICS: 6-group U-233 delayed neutron data (Keepin, secondary source,
          internally cross-checked - not yet verified against primary text)
""")

# --- Mesh convergence ---
print("-"*70)
print("1. MESH CONVERGENCE")
print("-"*70)
print("nr=28,nz=56:   k_eff=0.99926")
print("nr=56,nz=112:  k_eff=0.99921  (change: -0.00005)")
print("nr=84,nz=168:  k_eff=0.99920  (change: -0.00001)")
print("nr=112,nz=224: k_eff=0.99920  (change: -0.000003)")
print("VERDICT: Converged. nr=56,nz=112 mesh (used throughout) is adequate.")

# --- 2D vs 1D flux shape validation ---
print("\n" + "-"*70)
print("2. FLUX SHAPE VALIDATION (vs analytic bare-core solution)")
print("-"*70)
print("Radial shape vs J0 Bessel function: relative RMSE = 0.023%")
print("Axial shape vs cosine:              relative RMSE = 0.000%")
print("VERDICT: Numerical solution matches textbook analytic solution.")

# --- Cross-section sensitivity ---
print("\n" + "-"*70)
print("3. CROSS-SECTION SENSITIVITY (D, nu_sigma_f varied +/-20%)")
print("-"*70)
print("Group C5 offset held at 38.0 cm across all cases (k_eff ranged 0.83-1.25)")
print("VERDICT: Drift-offset physics is structurally decoupled from the")
print("         still-placeholder D and nu_sigma_f values.")

# --- Universal scaling law ---
print("\n" + "-"*70)
print("4. UNIVERSAL SCALING LAW: offset/L_half = Da / (a + Da)")
print("   where Da = v / (lambda * L_half)")
print("-"*70)
print("1D geometry: a = 0.778620, R^2 = 0.999715")
print("2D geometry: a = 0.768925, R^2 = 0.999477")
print("VERDICT: Law is geometry-independent (constant shifts <1.5%).")
print("Analytic derivation (exact ODE solution) matches simulation:")
print("  RMSE = 0.0029 (vs 0.045 for a naive first-guess formula)")

# --- Criticality calibration ---
print("\n" + "-"*70)
print("5. CRITICALITY CALIBRATION")
print("-"*70)
print("removal_coefficient = 0.00120511 (2D geometry), bisection-calibrated")
print("to true k_eff = 1.0 (MOOSE-convention eigenvalue = 1.0, since")
print("MOOSE solves A*x=k*B*x => MOOSE_eigenvalue = Loss/Production =")
print("1/k_true_standard_convention; at exact criticality both equal 1).")

# --- UQ results, if available ---
print("\n" + "-"*70)
print("6. UNCERTAINTY QUANTIFICATION (Keepin kinetics data)")
print("-"*70)
if os.path.exists("uq_results.csv"):
    uq = pd.read_csv("uq_results.csv")
    for i in range(6):
        col = f'offset_{i}'
        if col in uq.columns:
            mean = uq[col].mean()
            std = uq[col].std()
            print(f"Group {i}: offset = {mean:.1f} +/- {std:.1f} cm  (n={len(uq)} MC samples)")
else:
    print("uq_results.csv not found - run uq_propagation.py first")

# --- Velocity sweep summary ---
print("\n" + "-"*70)
print("7. VELOCITY SWEEP (2D validated geometry)")
print("-"*70)
if os.path.exists("sweep_final_2d_summary.csv"):
    sweep = pd.read_csv("sweep_final_2d_summary.csv")
    print(sweep[['velocity','k_eff'] + [f'offset_{i}' for i in range(6)]].to_string(index=False))
else:
    print("sweep_final_2d_summary.csv not found")

print("\n" + "="*70)
print("HONEST OPEN ITEMS (not resolved this session):")
print("="*70)
print("""
- D, nu_sigma_f remain placeholder magnitudes (shown insensitive to the
  DRIFT conclusion, but still needed for a credible absolute k_eff claim)
- U-233 kinetics data needs primary-source verification (Keepin's
  original tables or ENDF/B), currently from a secondary AI summary
- Real MSFR core velocity (110 cm/s) is a rough estimate, not directly
  sourced from the benchmark
- Real 16-loop external circuit geometry not modeled (core-only, or
  single lumped recirculating loop in the 1D variant)
- One-group energy diffusion (no fast/thermal spectrum split, no
  transport theory) - reasonable simplification, should be stated
  explicitly as a limitation
""")
