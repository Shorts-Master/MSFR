import subprocess
import pandas as pd
import glob
import os

velocities = [0, 5, 10, 25, 50, 100, 200, 400]
results = []

for v in velocities:
    print(f"--- Running velocity = {v} cm/s ---")

    # Clean old output files so we always grab the freshest one
    for f in glob.glob("msfr_precursor_1d_out_line_sample_*.csv"):
        os.remove(f)

    cmd = [
        "./msfr_precursor-opt",
        "-i", "msfr_precursor_1d.i",
        f"Kernels/advection/velocity='{v} 0 0'"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if "Solve Converged!" not in result.stdout:
        print(f"  WARNING: velocity={v} did not converge, skipping")
        print(result.stdout[-2000:])
        continue

    # Grab the solution CSV (the larger of the two _0000/_0001 files)
    csvs = sorted(glob.glob("msfr_precursor_1d_out_line_sample_*.csv"),
                  key=os.path.getsize, reverse=True)
    df = pd.read_csv(csvs[0])
    df['ratio'] = df['C'] / df['phi']

    # Drop boundary points where phi~0 (ratio blows up / is noise)
    interior = df[(df['x'] > 5) & (df['x'] < 295)]

    ratio_inlet_side = interior[interior['x'] < 50]['ratio'].mean()
    ratio_outlet_side = interior[interior['x'] > 250]['ratio'].mean()
    peak_phi_x = df.loc[df['phi'].idxmax(), 'x']
    peak_C_x = df.loc[df['C'].idxmax(), 'x']

    # Extract k_eff from stdout
    k_eff = None
    for line in result.stdout.splitlines():
        if "eigenvalue =" in line:
            k_eff = float(line.strip().split('=')[-1])

    results.append({
        'velocity': v,
        'k_eff': k_eff,
        'ratio_inlet': ratio_inlet_side,
        'ratio_outlet': ratio_outlet_side,
        'asymmetry': ratio_outlet_side / ratio_inlet_side if ratio_inlet_side else None,
        'peak_phi_x': peak_phi_x,
        'peak_C_x': peak_C_x,
        'peak_offset': peak_C_x - peak_phi_x,
    })

summary = pd.DataFrame(results)
summary.to_csv("sweep_summary.csv", index=False)
print("\n=== SWEEP SUMMARY ===")
print(summary.to_string(index=False))
