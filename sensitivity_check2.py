import subprocess
import sys
import pandas as pd
sys.path.insert(0, '.')
import generate_final

def run_case(D_val, nu_sigma_f_val, label):
    generate_final.NR = 56
    generate_final.NZ = 112
    generate_final.DIFFUSIVITY = D_val
    generate_final.NU_SIGMA_F = nu_sigma_f_val
    generate_final.generate(filename="msfr_final.i")

    result = subprocess.run(
        ["./msfr_precursor-opt", "-i", "msfr_final.i"],
        capture_output=True, text=True
    )
    k_eff = None
    for line in result.stdout.splitlines():
        if "eigenvalue =" in line:
            k_eff = float(line.strip().split('=')[-1])

    if "Solve Converged!" not in result.stdout:
        print(f"{label}: DID NOT CONVERGE")
        return None

    csv_file = "msfr_final_out_centerline_axial_0001.csv"
    df = pd.read_csv(csv_file)
    phi_peak_z = df.loc[df['phi'].idxmax(), 'y']
    C5_peak_z = df.loc[df['C5'].idxmax(), 'y']
    offset5 = C5_peak_z - phi_peak_z
    print(f"{label}: k_eff={k_eff:.4f}  phi_peak_z={phi_peak_z:.1f}  C5_peak_z={C5_peak_z:.1f}  offset_C5={offset5:.1f}")
    return k_eff, offset5

base_D = 1.2
base_nu_sigma_f = 0.002

print("=== Baseline (uncalibrated k_eff shown for reference) ===")
run_case(base_D, base_nu_sigma_f, "baseline")

print("\n=== D varied +/-20% (k_eff will shift - watch for it) ===")
run_case(base_D * 1.2, base_nu_sigma_f, "D +20%")
run_case(base_D * 0.8, base_nu_sigma_f, "D -20%")

print("\n=== nu_sigma_f varied +/-20% (k_eff will shift - watch for it) ===")
run_case(base_D, base_nu_sigma_f * 1.2, "nu_sigma_f +20%")
run_case(base_D, base_nu_sigma_f * 0.8, "nu_sigma_f -20%")
