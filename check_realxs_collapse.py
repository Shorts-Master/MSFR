import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

df = pd.read_csv("sweep_final_2d_realxs_summary.csv")
L_half = 112.0

rows = []
for i in range(6):
    lam = df[f'lambda_{i}'].iloc[0]
    for _, row in df.iterrows():
        v = row['velocity']
        offset = row[f'offset_{i}']
        x = v / (lam * L_half)
        y = offset / L_half
        rows.append({'group': i, 'x': x, 'y': y})

cdf = pd.DataFrame(rows)

def model(x, a):
    return x / (a + x)

popt, _ = curve_fit(model, cdf['x'], cdf['y'], p0=[0.78])
y_pred = model(cdf['x'], *popt)
rmse = np.sqrt(np.mean((cdf['y'] - y_pred)**2))
r2 = 1 - np.sum((cdf['y']-y_pred)**2)/np.sum((cdf['y']-cdf['y'].mean())**2)

print(f"REAL cross-section fit: a = {popt[0]:.6f}")
print(f"R^2 = {r2:.6f}  RMSE = {rmse:.6f}")
print()
print("Comparison across all three versions:")
print(f"  1D placeholder:        a=0.778620, R^2=0.999715")
print(f"  2D placeholder:        a=0.768925, R^2=0.999477")
print(f"  2D REAL cross sections: a={popt[0]:.6f}, R^2={r2:.6f}")
