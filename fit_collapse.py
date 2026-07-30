import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

df = pd.read_csv("collapse_check.csv")
x = df['x_dimensionless'].values
y = df['y_normalized'].values

# Candidate 1: simple saturation, y = x/(1+x)
def model1(x, a):
    return x / (a + x)

# Candidate 2: y = 1 - exp(-a*x)
def model2(x, a):
    return 1 - np.exp(-a * x)

# Candidate 3: y = x^n / (a^n + x^n), a generalized Hill-type saturation
def model3(x, a, n):
    return x**n / (a**n + x**n)

for name, model, p0 in [
    ("y = x/(a+x)", model1, [1.0]),
    ("y = 1 - exp(-a*x)", model2, [1.0]),
    ("y = x^n/(a^n + x^n)", model3, [1.0, 1.0]),
]:
    try:
        popt, pcov = curve_fit(model, x, y, p0=p0, maxfev=10000)
        y_pred = model(x, *popt)
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r2 = 1 - ss_res/ss_tot
        rmse = np.sqrt(np.mean((y - y_pred)**2))
        print(f"{name}")
        print(f"  params = {popt}")
        print(f"  R^2 = {r2:.6f}  RMSE = {rmse:.6f}")
        print()
    except Exception as e:
        print(f"{name}: fit failed - {e}")
        print()
