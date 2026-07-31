"""
Monte Carlo uncertainty quantification: propagates Keepin's quoted
measurement uncertainties (lambda_i +/- sigma, a_i +/- sigma) through
to the precursor drift offset, giving real error bars instead of
single-point estimates. Uses the reference case (v=110 cm/s, real
MSFR core velocity estimate).
"""
import subprocess
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, '.')
import generate_final

# (lambda_mean, lambda_sigma, a_mean, a_sigma) - from Keepin's original
# quoted uncertainties for U-233 fast fission, six-group parameters
KEEPIN_UNCERTAINTY = [
    (0.0126, 0.0004, 0.022, 0.005),
    (0.0337, 0.0010, 0.182, 0.009),
    (0.139,  0.010,  0.141, 0.013),
    (0.325,  0.017,  0.403, 0.014),
    (1.13,   0.15,   0.128, 0.025),
    (2.50,   0.42,   0.124, 0.021),
]
BETA_TOTAL_FIXED = 0.0028

N_SAMPLES = 25
rng = np.random.default_rng(42)

results = []
for sample in range(N_SAMPLES):
    lambdas = []
    a_vals = []
    for lam_mean, lam_sig, a_mean, a_sig in KEEPIN_UNCERTAINTY:
        lam = rng.normal(lam_mean, lam_sig)
        a = rng.normal(a_mean, a_sig)
        lambdas.append(max(lam, 1e-4))   # keep physically positive
        a_vals.append(max(a, 1e-4))
    a_vals = np.array(a_vals)
    a_vals = a_vals / a_vals.sum()        # renormalize abundances to sum to 1

    groups = [(lam, a * BETA_TOTAL_FIXED) for lam, a in zip(lambdas, a_vals)]
    generate_final.GROUPS = groups
    generate_final.BETA_TOTAL = BETA_TOTAL_FIXED
    generate_final.NR = 56
    generate_final.NZ = 112
    generate_final.generate(velocity=110, filename="msfr_final.i")

    result = subprocess.run(
        ["./msfr_precursor-opt", "-i", "msfr_final.i"],
        capture_output=True, text=True
    )
    if "Solve Converged!" not in result.stdout:
        print(f"Sample {sample}: DID NOT CONVERGE, skipping")
        continue

    df = pd.read_csv("msfr_final_out_centerline_axial_0001.csv")
    phi_peak_z = df.loc[df['phi'].idxmax(), 'y']
    row = {'sample': sample}
    for i, (lam, beta) in enumerate(groups):
        peak_z = df.loc[df[f'C{i}'].idxmax(), 'y']
        row[f'offset_{i}'] = peak_z - phi_peak_z
        row[f'lambda_{i}'] = lam
    results.append(row)
    print(f"Sample {sample}: offsets = {[row[f'offset_{i}'] for i in range(6)]}")

df_results = pd.DataFrame(results)
df_results.to_csv("uq_results.csv", index=False)

print("\n=== UQ SUMMARY (reference case, v=110 cm/s) ===")
for i in range(6):
    col = f'offset_{i}'
    mean = df_results[col].mean()
    std = df_results[col].std()
    print(f"Group {i}: offset = {mean:.1f} +/- {std:.1f} cm  (across {len(df_results)} samples)")
