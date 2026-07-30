"""
Bisection search for removal_coefficient giving MOOSE eigenvalue = 1.0.
CORRECTED: MOOSE's Eigenvalue executioner defines the problem as
A*x = k*B*x, where A = non-eigen kernels (loss), B = eigen-tagged
kernels (production). So MOOSE's printed "eigenvalue" = Loss/Production,
the RECIPROCAL of the standard k_eff = Production/Loss convention.
Since 1/1 = 1, the critical target (eigenvalue=1.0) is unaffected -
only the search DIRECTION was wrong before (more removal INCREASES
MOOSE's printed eigenvalue, not decreases it).
"""
import subprocess
import sys
sys.path.insert(0, '.')
from generate_6group_input import generate

def run_and_get_keff(removal_coeff):
    generate(velocity="110 0 0", filename="msfr_precursor_6group.i")
    with open("msfr_precursor_6group.i", "r") as f:
        content = f.read()
    content = content.replace(
        "removal_coefficient = 0.003",
        f"removal_coefficient = {removal_coeff}"
    )
    with open("msfr_precursor_6group.i", "w") as f:
        f.write(content)

    result = subprocess.run(
        ["./msfr_precursor-opt", "-i", "msfr_precursor_6group.i"],
        capture_output=True, text=True
    )
    if "Solve Converged!" not in result.stdout:
        return None
    k_eff = None
    for line in result.stdout.splitlines():
        if "eigenvalue =" in line:
            k_eff = float(line.strip().split('=')[-1])
    return k_eff

lo, hi = 0.001, 0.003
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
        print(f"\nCONVERGED: removal_coefficient = {mid:.8f} gives true k_eff = 1.0 exactly (critical)")
        print(f"(MOOSE printed eigenvalue = {k_mid:.6f}, which is Loss/Production = 1/k_true)")
        break

    # CORRECTED direction: more removal (Loss) -> higher MOOSE eigenvalue
    if k_mid > target:
        hi = mid   # too much removal, decrease it
    else:
        lo = mid   # too little removal, increase it
