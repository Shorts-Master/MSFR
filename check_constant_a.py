import pandas as pd
import numpy as np

df = pd.read_csv("sweep_6group_summary.csv")

# Diffusion length L_diff = sqrt(D / removal_coefficient), a natural length scale from the flux equation
D = 1.2
removal_coefficient = 0.003
L_diff = np.sqrt(D / removal_coefficient)

L_half = df['phi_peak_x'].iloc[-1]

print(f"L_half (core half-length)     = {L_half:.2f} cm")
print(f"L_diff = sqrt(D/Sigma_removal) = {L_diff:.2f} cm")
print(f"L_diff / L_half                = {L_diff/L_half:.4f}")
print(f"Fitted constant a              = 0.779")
