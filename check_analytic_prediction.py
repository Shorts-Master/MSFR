import pandas as pd
import numpy as np

df = pd.read_csv("collapse_check.csv")
x = df['x_dimensionless'].values
y_actual = df['y_normalized'].values

# Analytic prediction from solving v*C' + lambda*C = S0*cos(k(x-L_half))
# assuming a pure cosine flux shape (no boundary-condition correction term)
y_analytic = (2/np.pi) * np.arctan((np.pi/2) * x)

residual = y_actual - y_analytic
rmse = np.sqrt(np.mean(residual**2))
max_err = np.max(np.abs(residual))

print(f"RMSE (analytic vs actual)     = {rmse:.6f}")
print(f"Max abs error                 = {max_err:.6f}")
print()

comparison = pd.DataFrame({
    'group': df['group'],
    'velocity': df['velocity'],
    'x': x,
    'y_actual': y_actual,
    'y_analytic': y_analytic,
    'residual': residual
}).sort_values('x')

print(comparison.to_string(index=False))
