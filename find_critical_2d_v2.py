import subprocess
import sys
sys.path.insert(0, '.')
import generate_final

def run_and_get_keff2(removal_coeff, velocity=110):
    generate_final.REMOVAL_COEFFICIENT = removal_coeff
    generate_final.generate(velocity=velocity, filename="msfr_final.i")
    result = subprocess.run(
        ["./msfr_precursor-opt", "-i", "msfr_final.i"],
        capture_output=True, text=True
    )
    if "Solve Converged!" not in result.stdout:
        return None
    k_eff = None
    for line in result.stdout.splitlines():
        if "eigenvalue =" in line:
            k_eff = float(line.strip().split('=')[-1])
    return k_eff

lo, hi = 0.0005, 0.003
target = 1.0
tol = 1e-5

k_lo = run_and_get_keff2(lo)
k_hi = run_and_get_keff2(hi)
print(f"removal_coeff={lo}  ->  MOOSE eigenvalue={k_lo}")
print(f"removal_coeff={hi}  ->  MOOSE eigenvalue={k_hi}")

for iteration in range(40):
    mid = (lo + hi) / 2
    k_mid = run_and_get_keff2(mid)
    print(f"Iteration {iteration}: removal_coeff={mid:.8f}  MOOSE_eigenvalue={k_mid:.6f}")
    if k_mid is None:
        print("  did not converge, stopping")
        break
    if abs(k_mid - target) < tol:
        print(f"\nCONVERGED: removal_coefficient = {mid:.8f} gives critical 2D core (with real nu_sigma_f)")
        break
    if k_mid > target:
        hi = mid
    else:
        lo = mid
