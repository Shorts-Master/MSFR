"""
Compute macroscopic transport cross section and diffusion coefficient
D = 1/(3*Sigma_tr) from real ENDF/B-VII.1 total cross sections
(user-extracted at E=1 MeV) for the three dominant salt constituents.

APPROXIMATION FLAGGED: using total cross section as a stand-in for
transport cross section (which technically needs angular distribution
data to compute properly, via Sigma_tr = Sigma_total - mu_bar*Sigma_scatter).
This is a standard first-pass simplification, not full transport theory.
"""
import numpy as np

# --- Real ENDF/B-VII.1 total cross sections at 1 MeV ---
sigma_Li7 = 1.5545e-24   # cm^2
sigma_F19 = 2.8353e-24   # cm^2
sigma_Th232 = 6.9231e-24 # cm^2
# U-233 total not extracted (minor 2.5% constituent, omitted - small effect)

# --- Real salt composition (same as compute_real_xs.py) ---
x_LiF, x_ThF4, x_UF4 = 0.775, 0.200, 0.025

M_Li7, M_F, M_Th232, M_U233 = 7.016, 19.00, 232.04, 233.04
M_LiF = M_Li7 + M_F
M_ThF4 = M_Th232 + 4*M_F
M_UF4 = M_U233 + 4*M_F
M_avg = x_LiF*M_LiF + x_ThF4*M_ThF4 + x_UF4*M_UF4

T_K = 1000
rho = 5085.6 - 0.8198*T_K
rho_g_cm3 = rho / 1000.0

N_A = 6.022e23
N_total = rho_g_cm3 * N_A / M_avg

# Atoms per formula unit of salt (weighted average)
n_Li7_per_unit = x_LiF * 1
n_F19_per_unit = x_LiF*1 + x_ThF4*4 + x_UF4*4
n_Th232_per_unit = x_ThF4 * 1

N_Li7 = n_Li7_per_unit * N_total
N_F19 = n_F19_per_unit * N_total
N_Th232 = n_Th232_per_unit * N_total

Sigma_tr = N_Li7*sigma_Li7 + N_F19*sigma_F19 + N_Th232*sigma_Th232

D = 1.0 / (3.0 * Sigma_tr)

print(f"N_Li7   = {N_Li7:.4e} /cm^3")
print(f"N_F19   = {N_F19:.4e} /cm^3")
print(f"N_Th232 = {N_Th232:.4e} /cm^3")
print()
print(f"Sigma_tr (Li+F+Th, U-233 omitted as minor) = {Sigma_tr:.4e} /cm")
print(f"D = 1/(3*Sigma_tr) = {D:.4f} cm")
print()
print(f"COMPARISON to placeholder used all session: D = 1.2 cm")
print(f"Real estimate: D = {D:.4f} cm")
print(f"Ratio: {D/1.2:.2f}x")
