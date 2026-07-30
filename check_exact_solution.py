import pandas as pd
import numpy as np
from scipy.optimize import minimize_scalar

df = pd.read_csv("collapse_check.csv")
L = 112.0  # L_half

def C_exact(x, v, lam, L, S0=1.0):
    denom = 4*L**2*lam**2 + np.pi**2*v**2
    term1 = np.pi*v
    term2 = 2*L*lam*np.sin(np.pi*x/(2*L)) - np.pi*v*np.cos(np.pi*x/(2*L))
    return (2*L*S0/denom) * (term1 + term2*np.exp(lam*x/v)) * np.exp(-lam*x/v)

results = []
for _, row in df.iterrows():
    v = row['velocity']
    lam = row['lambda']
    if v == 0:
        continue
    # find peak numerically by maximizing -C_exact over x in [0, 2L]
    res = minimize_scalar(lambda xx: -C_exact(xx, v, lam, L), bounds=(0, 2*L), method='bounded')
    peak_x_exact = res.x
    offset_exact = peak_x_exact - L
    y_exact = offset_exact / L
    results.append({
        'group': row['group'], 'velocity': v, 'lambda': lam,
        'x_dimensionless': row['x_dimensionless'],
        'y_actual': row['y_normalized'],
        'y_exact_theory': y_exact,
        'residual': row['y_normalized'] - y_exact
    })

result_df = pd.DataFrame(results).sort_values('x_dimensionless')
rmse = np.sqrt(np.mean(result_df['residual']**2))
max_err = np.abs(result_df['residual']).max()
print(f"RMSE (exact theory vs actual)  = {rmse:.6f}")
print(f"Max abs error                  = {max_err:.6f}")
print()
print(result_df.to_string(index=False))
