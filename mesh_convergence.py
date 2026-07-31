import subprocess
import sys
sys.path.insert(0, '.')
import generate_final

resolutions = [(28, 56), (56, 112), (84, 168), (112, 224)]
results = []

for nr, nz in resolutions:
    generate_final.NR = nr
    generate_final.NZ = nz
    generate_final.generate(filename="msfr_final.i")

    result = subprocess.run(
        ["./msfr_precursor-opt", "-i", "msfr_final.i"],
        capture_output=True, text=True
    )
    k_eff = None
    for line in result.stdout.splitlines():
        if "eigenvalue =" in line:
            k_eff = float(line.strip().split('=')[-1])
    dofs = None
    for line in result.stdout.splitlines():
        if "Num DOFs:" in line:
            dofs = int(line.split(':')[-1].strip())
    results.append({'nr': nr, 'nz': nz, 'dofs': dofs, 'k_eff': k_eff})
    print(f"nr={nr:>4} nz={nz:>4}  DOFs={dofs:>7}  k_eff={k_eff}")

print("\nIf k_eff is still changing meaningfully between the last two rows,")
print("the mesh is not yet converged and finer resolution is needed.")
