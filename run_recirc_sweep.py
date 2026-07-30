import subprocess
import pandas as pd
import glob
import os
import sys
sys.path.insert(0, '.')
from generate_recirculating_input import generate, GROUPS

velocities = [5, 10, 25, 50, 75, 100, 110, 150, 200, 300, 400]
results = []

for v in velocities:
    print(f"--- Running velocity = {v} cm/s ---")
    vel_str = f"{v} 0 0"
    generate(velocity=vel_str, filename="msfr_precursor_recirc.i")

    for f in glob.glob("msfr_precursor_recirc_out_line_sample_*.csv"):
        os.remove(f)

    cmd = ["./msfr_precursor-opt", "-i", "msfr_precursor_recirc.i"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if "Solve Converged!" not in result.stdout:
        print(f"  WARNING: velocity={v} did not converge, skipping")
        continue

    csvs = sorted(glob.glob("msfr_precursor_recirc_out_line_sample_*.csv"),
                  key=os.path.getsize, reverse=True)
    df = pd.read_csv(csvs[0])
    phi_peak_x = df.loc[df['phi'].idxmax(), 'x']

    row = {'velocity': v, 'phi_peak_x': phi_peak_x, 'phi_max': df['phi'].max()}
    for i, (lam, beta) in enumerate(GROUPS):
        col = f'C{i}'
        peak_x = df.loc[df[col].idxmax(), 'x']
        offset = peak_x - phi_peak_x
        row[f'lambda_{i}'] = lam
        row[f'offset_{i}'] = offset

    results.append(row)

summary = pd.DataFrame(results)
summary.to_csv("sweep_recirc_summary.csv", index=False)

print("\n=== RECIRCULATING SWEEP SUMMARY ===")
offset_cols = ['velocity'] + [f'offset_{i}' for i in range(6)]
print(summary[offset_cols].to_string(index=False))
