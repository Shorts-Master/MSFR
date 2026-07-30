import pandas as pd
import numpy as np

df = pd.read_csv("msfr_precursor_6group_out_line_sample_0001.csv")
L = 112.0

phi_actual = df['phi'].values
x = df['x'].values
phi_cosine_ideal = np.cos(np.pi*(x - L)/(2*L))
phi_cosine_ideal *= phi_actual.max() / phi_cosine_ideal.max()  # normalize to same peak

residual = phi_actual - phi_cosine_ideal
rmse = np.sqrt(np.mean(residual**2))
rel_rmse = rmse / phi_actual.max()

print(f"phi RMSE vs ideal cosine       = {rmse:.6f}")
print(f"Relative RMSE (vs peak height) = {rel_rmse*100:.4f}%")
