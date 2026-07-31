"""
Master pipeline: runs the full validated MSFR precursor drift study
end-to-end, in the correct order, and produces the final report.
"""
import subprocess
import sys
import time

STEPS = [
    ("Mesh convergence check",       "mesh_convergence.py"),
    ("Cross-section sensitivity",    "sensitivity_check2.py"),
    ("Velocity sweep (main result)", "run_final_sweep.py"),
    ("Universal scaling law fit",    "check_2d_collapse.py"),
    ("Kinetics uncertainty (UQ)",     "uq_propagation.py"),
    ("Final consolidated report",     "final_report.py"),
]

start = time.time()

for i, (label, script) in enumerate(STEPS, 1):
    print(f"\n{'='*70}")
    print(f"STEP {i}/{len(STEPS)}: {label}  ({script})")
    print('='*70)

    step_start = time.time()
    result = subprocess.run(
        ["python3", script],
        capture_output=True, text=True
    )
    elapsed = time.time() - step_start

    print(result.stdout)
    if result.returncode != 0:
        print(f"!!! STEP FAILED (exit code {result.returncode}) !!!")
        print("STDERR:")
        print(result.stderr)
        print(f"\nStopping pipeline at step {i}. Fix the error above and rerun.")
        sys.exit(1)

    print(f"[Step {i} completed in {elapsed:.1f}s]")

total = time.time() - start
print(f"\n{'='*70}")
print(f"PIPELINE COMPLETE in {total:.1f}s ({total/60:.1f} min)")
print(f"See FINAL_REPORT.txt for the consolidated summary.")
print('='*70)
