"""
Isolate NetRemoval's effect on k_eff. Physically, MORE absorption
(higher removal_coefficient) must DECREASE k_eff, always, with no
exceptions - this is a hard physical law, not a modeling choice.
If we see the opposite, NetRemoval has a real sign/implementation bug.
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

test_values = [0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1]
print(f"{'removal_coefficient':>20}  {'k_eff':>12}")
for rc in test_values:
    k = run_and_get_keff(rc)
    print(f"{rc:>20}  {k if k is not None else 'DID NOT CONVERGE':>12}")
