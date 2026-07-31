import subprocess
import sys
sys.path.insert(0, '.')
from generate_2d_core import generate

def run_and_get_keff(removal_coeff):
    generate(filename="msfr_2d_core.i")
    with open("msfr_2d_core.i", "r") as f:
        content = f.read()
    content = content.replace(
        "removal_coefficient = 0.00175995",
        f"removal_coefficient = {removal_coeff}"
    )
    with open("msfr_2d_core.i", "w") as f:
        f.write(content)

    result = subprocess.run(
        ["./msfr_precursor-opt", "-i", "msfr_2d_core.i"],
        capture_output=True, text=True
    )
    if "Solve Converged!" not in result.stdout:
        return None
    k_eff = None
    for line in result.stdout.splitlines():
        if "eigenvalue =" in line:
            k_eff = float(line.strip().split('=')[-1])
    return k_eff

lo, hi = 0.0005, 0.00175995
target = 1.0
tol = 1e-5

k_lo = run_and_get_keff(lo)
k_hi = run_and_get_keff(hi)
print(f"removal_coeff={lo}  ->  MOOSE eigenvalue={k_lo}")
print(f"removal_coeff={hi}  ->  MOOSE eigenvalue={k_hi}")

for iteration in range(40):
    mid = (lo + hi) / 2
    k_mid = run_and_get_keff(mid)
    print(f"Iteration {iteration}: removal_coeff={mid:.8f}  MOOSE_eigenvalue={k_mid:.6f}")

    if k_mid is None:
        print("  did not converge, stopping")
        break
    if abs(k_mid - target) < tol:
        print(f"\nCONVERGED: removal_coefficient = {mid:.8f} gives critical 2D core")
        break

    if k_mid > target:
        hi = mid
    else:
        lo = mid
