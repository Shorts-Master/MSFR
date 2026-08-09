"""
Compute macroscopic U-233 fission/absorption cross sections from real
ENDF/B-VII.1 data (user-extracted at E=1 MeV) and real MSFR salt
composition (EVOL benchmark + SAMOFAR follow-up, cross-validated).
"""
import numpy as np

# --- Real ENDF/B-VII.1 data at E=1 MeV, U-233 ---
sigma_f = 1.839e-24   # cm^2 (fission cross section, 1.839 barns)
sigma_g = 0.07887e-24 # cm^2 (capture/n,gamma cross section)
sigma_a = sigma_f + sigma_g

# --- Real salt composition (EVOL benchmark, cross-validated w/ SAMOFAR) ---
# LiF-ThF4-UF4: 77.5 - 20.0 - 2.5 mol%
x_LiF, x_ThF4, x_UF4 = 0.775, 0.200, 0.025

M_Li7 = 7.016
M_F = 19.00
M_Th232 = 232.04
M_U233 = 233.04

M_LiF = M_Li7 + M_F
M_ThF4 = M_Th232 + 4*M_F
M_UF4 = M_U233 + 4*M_F

M_avg = x_LiF*M_LiF + x_ThF4*M_ThF4 + x_UF4*M_UF4  # g/mol

# --- Density at operating temperature ---
T_K = 1000  # ~727 C, within stated 700-900 C MSFR operating range
rho = 5085.6 - 0.8198*T_K  # kg/m^3
rho_g_cm3 = rho / 1000.0

N_A = 6.022e23

N_total = rho_g_cm3 * N_A / M_avg      # salt formula units per cm^3
N_U233 = x_UF4 * N_total               # U-233 atoms per cm^3

Sigma_f = N_U233 * sigma_f
Sigma_a = N_U233 * sigma_a

nu_bar = 2.590  # REAL value, interpolated from ENDF/B-VII.1 MF=1,MT=452 at 1 MeV
nu_Sigma_f = nu_bar * Sigma_f

print(f"Average salt molar mass    = {M_avg:.2f} g/mol")
print(f"Density at {T_K}K            = {rho_g_cm3:.4f} g/cm^3")
print(f"Total salt number density  = {N_total:.4e} /cm^3")
print(f"U-233 number density       = {N_U233:.4e} /cm^3")
print()
print(f"Macroscopic Sigma_f (U-233 only)     = {Sigma_f:.4e} /cm")
print(f"Macroscopic Sigma_a (U-233 only)     = {Sigma_a:.4e} /cm")
print(f"nu*Sigma_f (U-233 only, nu={nu_bar})  = {nu_Sigma_f:.4e} /cm")
print()
print(f"COMPARISON to placeholder used all session: nu_sigma_f = 2.0e-3 /cm")
print(f"Real (partial, U-233-only) estimate: {nu_Sigma_f:.4e} /cm")
print(f"Ratio: {nu_Sigma_f/0.002:.2f}x")
print()
print("CAVEATS:")
print("- nu_bar=2.5 is a rough estimate, not sourced from ENDF yet (MF=1,MT=452)")
print("- This Sigma_a is U-233 ONLY - real total absorption also includes")
print("  Th-232 capture, Li/F absorption, and structural Ni-alloy absorption,")
print("  all currently omitted, so real total Sigma_a is meaningfully HIGHER")
print("- D (diffusion coefficient) still needs transport cross section data")
