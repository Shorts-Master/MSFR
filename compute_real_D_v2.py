"""
Improved D calculation using real elastic cross sections + textbook
mu-bar approximation (Lamarsh, Introduction to Nuclear Engineering):
mu_bar = 2/(3A) for isotropic-in-CM elastic scattering.
Sigma_tr = Sigma_total - mu_bar * Sigma_elastic
"""
import numpy as np

# Real ENDF/B-VII.1 data at 1 MeV
data = {
    'Li7':   {'A': 7,   'sigma_total': 1.554525e-24, 'sigma_elastic': 1.373620e-24},
    'F19':   {'A': 19,  'sigma_total': 2.835278e-24, 'sigma_elastic': 2.479263e-24},
    'Th232': {'A': 232, 'sigma_total': 6.923100e-24, 'sigma_elastic': 4.378490e-24},
}

for name, d in data.items():
    mu_bar = 2.0 / (3.0 * d['A'])
    sigma_tr = d['sigma_total'] - mu_bar * d['sigma_elastic']
    d['mu_bar'] = mu_bar
    d['sigma_tr'] = sigma_tr
    print(f"{name}: mu_bar={mu_bar:.5f}  sigma_tr={sigma_tr*1e24:.4f} b  (vs sigma_total={d['sigma_total']*1e24:.4f} b, {(1-sigma_tr/d['sigma_total'])*100:.2f}% correction)")

# Real salt composition (same as before)
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

n_Li7 = x_LiF * 1
n_F19 = x_LiF*1 + x_ThF4*4 + x_UF4*4
n_Th232 = x_ThF4 * 1

N_Li7 = n_Li7 * N_total
N_F19 = n_F19 * N_total
N_Th232 = n_Th232 * N_total

Sigma_tr = N_Li7*data['Li7']['sigma_tr'] + N_F19*data['F19']['sigma_tr'] + N_Th232*data['Th232']['sigma_tr']
D = 1.0 / (3.0 * Sigma_tr)

print()
print(f"Sigma_tr (transport-corrected) = {Sigma_tr:.4e} /cm")
print(f"D = 1/(3*Sigma_tr) = {D:.4f} cm")
print()
print(f"Previous (total-xs-only) estimate: D = 1.5825 cm")
print(f"New (transport-corrected) estimate: D = {D:.4f} cm")
print(f"Change: {(D/1.5825 - 1)*100:.2f}%")
