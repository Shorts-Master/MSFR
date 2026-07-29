import subprocess
import pandas as pd
import glob
import os
import sys
sys.path.insert(0, '.')
from generate_6group_input import generate, GROUPS

velocities = [0, 5, 10, 25, 50, 100, 200, 400]
results = []

for v in velocities:
    print(f"--- Running velocity = {v} cm/s ---")
    vel_str = f"{v} 0 0"
    generate(velocity=vel_str, filename="msfr_precursor_6group.i")

    # Clean old outputs so we always grab the freshest
    for f in glob.glob("msfr_precursor_6group_out_line_sample_*.csv"):
        os.remove(f)

    cmd = ["./msfr_precursor-opt", "-i", "msfr_precursor_6group.i"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if "Solve Converged!" not in result.stdout:
        print(f"  WARNING: velocity={v} did not converge, skipping")
        continue

    k_eff = None
    for line in result.stdout.splitlines():
        if "eigenvalue =" in line:
            k_eff = float(line.strip().split('=')[-1])

    csvs = sorted(glob.glob("msfr_precursor_6group_out_line_sample_*.csv"),
                  key=os.path.getsize, reverse=True)
    df = pd.read_csv(csvs[0])

    phi_peak_x = df.loc[df['phi'].idxmax(), 'x']

    row = {'velocity': v, 'k_eff': k_eff, 'phi_peak_x': phi_peak_x}
    for i, (lam, beta) in enumerate(GROUPS):
        col = f'C{i}'
        peak_x = df.loc[df[col].idxmax(), 'x']
        offset = peak_x - phi_peak_x
        row[f'lambda_{i}'] = lam
        row[f'offset_{i}'] = offset
        row[f'v_over_lambda_{i}'] = v / lam if lam > 0 else None

    results.append(row)

summary = pd.DataFrame(results)
summary.to_csv("sweep_6group_summary.csv", index=False)

print("\n=== 6-GROUP SWEEP SUMMARY ===")
offset_cols = ['velocity'] + [f'offset_{i}' for i in range(6)]
print(summary[offset_cols].to_string(index=False))

print("\n=== v/lambda (predicted drift length) vs actual offset, group 5 (fastest) ===")
print(summary[['velocity', 'v_over_lambda_5', 'offset_5']].to_string(index=False))
print("\n=== v/lambda (predicted drift length) vs actual offset, group 0 (slowest) ===")
print(summary[['velocity', 'v_over_lambda_0', 'offset_0']].to_string(index=False))
