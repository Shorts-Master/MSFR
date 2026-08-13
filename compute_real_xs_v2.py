"""
Updated absorption budget: adds Th-232 capture (previously entirely
omitted - a real flaw for a thorium-fueled reactor) to the U-233
fission+capture already computed. Sigma_a is now U-233 + Th-232,
still missing Li-7/F-19 absorption (much smaller, non-fissile light
nuclei have small capture cross sections, but not yet verified).
"""
import numpy as np

# U-233 (already have, from compute_real_xs.py)
sigma_f_U233 = 1.839e-24
sigma_g_U233 = 0.07887e-24
nu_bar = 2.590

# Th-232 (NEW - previously missing entirely)
sigma_g_Th232 = 0.13552e-24

# Real salt composition
x_LiF, x_ThF4, x_UF4 = 0.775, 0.200, 0.025
M_Li7, M_F, M_Th232, M_U233 = 7.016, 19.00, 232.04, 233.04
M_LiF = M_Li7 + M_F
M_ThF4 = M_Th232 + 4*M_F
M_UF4 = M_U233 + 4*M_F
M_avg = x_LiF*M_LiF + x_ThF4*M_ThF4 + x_UF4*M_UF4

T_K = 1000
rho_g_cm3 = (5085.6 - 0.8198*T_K) / 1000.0
N_A = 6.022e23
N_total = rho_g_cm3 * N_A / M_avg

N_U233 = x_UF4 * N_total
N_Th232 = x_ThF4 * N_total

Sigma_f_U233 = N_U233 * sigma_f_U233
Sigma_a_U233 = N_U233 * (sigma_f_U233 + sigma_g_U233)
Sigma_a_Th232 = N_Th232 * sigma_g_Th232

Sigma_a_total = Sigma_a_U233 + Sigma_a_Th232
nu_Sigma_f = nu_bar * Sigma_f_U233

print(f"N_U233   = {N_U233:.4e} /cm^3")
print(f"N_Th232  = {N_Th232:.4e} /cm^3")
print()
print(f"Sigma_a (U-233 fission+capture)  = {Sigma_a_U233:.4e} /cm")
print(f"Sigma_a (Th-232 capture, NEW)    = {Sigma_a_Th232:.4e} /cm")
print(f"Sigma_a TOTAL (U233+Th232)       = {Sigma_a_total:.4e} /cm")
print()
print(f"Previous absorption estimate (U-233 only) was missing Th-232 entirely.")
print(f"Th-232 contributes {Sigma_a_Th232/Sigma_a_total*100:.1f}% of this total absorption.")
print()
print(f"nu*Sigma_f (unchanged, still U-233 only, this is correct - only U-233 fissions) = {nu_Sigma_f:.4e} /cm")
print()
print(f"Note: removal_coefficient in our model represents NET removal")
print(f"(absorption minus fission production), not raw absorption -")
print(f"this Th-232 addition should be added to REMOVAL_COEFFICIENT,")
print(f"then the whole model recalibrated to criticality again.")
