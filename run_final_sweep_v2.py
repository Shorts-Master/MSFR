import subprocess
import pandas as pd
import glob
import os
import sys
sys.path.insert(0, '.')
import generate_final
from generate_final import GROUPS
from peak_finder import subcell_peak

generate_final.NR = 56
generate_final.NZ = 112
generate_final.DIFFUSIVITY = 1.5825
generate_final.NU_SIGMA_F = 0.0034179
generate_final.REMOVAL_COEFFICIENT = 0.00237018

velocities = [5, 10, 25, 50, 75, 100, 110, 150, 200, 300, 400]
results = []

for v in velocities:
    print(f"--- Running velocity = {v} cm/s ---")
    generate_final.generate(velocity=v, filename="msfr_final.i")

    for f in glob.glob("msfr_final_out_centerline_axial_*.csv"):
        os.remove(f)

    cmd = ["./msfr_precursor-opt", "-i", "msfr_final.i"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if "Solve Converged!" not in result.stdout:
        print(f"  WARNING: velocity={v} did not converge, skipping")
        continue

    k_eff = None
    for line in result.stdout.splitlines():
        if "eigenvalue =" in line:
            k_eff = float(line.strip().split('=')[-1])

    csvs = sorted(glob.glob("msfr_final_out_centerline_axial_*.csv"),
                  key=os.path.getsize, reverse=True)
    df = pd.read_csv(csvs[0])
    z = df['y'].values
    phi_peak_z = subcell_peak(z, df['phi'].values)

    row = {'velocity': v, 'k_eff': k_eff, 'phi_peak_z': phi_peak_z}
    for i, (lam, beta) in enumerate(GROUPS):
        col = f'C{i}'
        peak_z = subcell_peak(z, df[col].values)
        offset = peak_z - phi_peak_z
        row[f'lambda_{i}'] = lam
        row[f'offset_{i}'] = offset

    results.append(row)

summary = pd.DataFrame(results)
summary.to_csv("sweep_final_2d_realxs_summary.csv", index=False)

print("\n=== REAL CROSS-SECTION SWEEP SUMMARY (sub-cell accurate) ===")
offset_cols = ['velocity', 'k_eff'] + [f'offset_{i}' for i in range(6)]
print(summary[offset_cols].to_string(index=False))
