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
    if "Solve Converged!" not in result.stdout:
        print(f"{label}: DID NOT CONVERGE")
        return None

    csv_file = "msfr_final_out_centerline_axial_0001.csv"
    df = pd.read_csv(csv_file)
    phi_peak_z = df.loc[df['phi'].idxmax(), 'y']
    C0_peak_z = df.loc[df['C0'].idxmax(), 'y']
    offset = C0_peak_z - phi_peak_z
    print(f"{label}: phi_peak_z={phi_peak_z:.1f}  C0_peak_z={C0_peak_z:.1f}  offset={offset:.1f}")
    return offset

base_D = 1.2
base_nu_sigma_f = 0.002

print("=== Baseline ===")
offset_base = run_case(base_D, base_nu_sigma_f, "baseline")

print("\n=== D varied +/-20% ===")
run_case(base_D * 1.2, base_nu_sigma_f, "D +20%")
run_case(base_D * 0.8, base_nu_sigma_f, "D -20%")

print("\n=== nu_sigma_f varied +/-20% ===")
run_case(base_D, base_nu_sigma_f * 1.2, "nu_sigma_f +20%")
run_case(base_D, base_nu_sigma_f * 0.8, "nu_sigma_f -20%")
