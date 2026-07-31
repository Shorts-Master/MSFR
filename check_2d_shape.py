import pandas as pd
import numpy as np
from scipy.special import j0, jn_zeros
from scipy.optimize import curve_fit

Ra = 112
Ha = 224

radial = pd.read_csv("msfr_2d_core_out_radial_sample_0001.csv")
axial = pd.read_csv("msfr_2d_core_out_axial_sample_0001.csv")

# Analytic bare-core shapes:
# Radial: phi(r) ~ J0(2.405 * r / Ra)  (2.405 = first zero of J0, so phi=0 at r=Ra)
# Axial:  phi(z) ~ cos(pi*(z - Ha/2)/Ha)  (zero at z=0 and z=Ha)

j0_first_zero = jn_zeros(0, 1)[0]  # 2.4048...
r = radial['x'].values
phi_r_actual = radial['phi'].values
phi_r_ideal = j0(j0_first_zero * r / Ra)
phi_r_ideal *= phi_r_actual.max() / phi_r_ideal.max()

z = axial['y'].values
phi_z_actual = axial['phi'].values
phi_z_ideal = np.cos(np.pi * (z - Ha/2) / Ha)
phi_z_ideal *= phi_z_actual.max() / phi_z_ideal.max()

r_rmse = np.sqrt(np.mean((phi_r_actual - phi_r_ideal)**2))
r_rel_rmse = r_rmse / phi_r_actual.max() * 100

z_rmse = np.sqrt(np.mean((phi_z_actual - phi_z_ideal)**2))
z_rel_rmse = z_rmse / phi_z_actual.max() * 100

print(f"Radial shape vs J0 Bessel:  RMSE={r_rmse:.6f}  relative={r_rel_rmse:.4f}%")
print(f"Axial shape vs cosine:      RMSE={z_rmse:.6f}  relative={z_rel_rmse:.4f}%")
print()
print("Radial profile (every 5th point):")
print(pd.DataFrame({'r': r, 'phi_actual': phi_r_actual, 'phi_J0_ideal': phi_r_ideal}).iloc[::5].to_string(index=False))
print()
print("Axial profile (every 10th point):")
print(pd.DataFrame({'z': z, 'phi_actual': phi_z_actual, 'phi_cos_ideal': phi_z_ideal}).iloc[::10].to_string(index=False))
