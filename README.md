# MSFR Precursor Drift

MOOSE-based computational study of delayed neutron precursor drift in
Molten Salt Fast Reactors (MSFR), where circulating liquid fuel salt
carries precursors downstream before they decay - a phenomenon that
doesn't exist in solid-fuel reactors.

## What this contains

- Custom MOOSE kernels (C++) for coupled neutron diffusion + 6-group
  delayed neutron precursor advection-decay-production
- 2D axisymmetric (RZ) validated core geometry (real EVOL/MARS
  benchmark dimensions: Ra=112cm, Ha=224cm)
- Real ENDF/B-VII.1 sourced U-233 nuclear data (fission/capture cross
  sections, nu-bar) and real Keepin delayed-neutron kinetics data
- A derived-and-validated universal scaling law for precursor drift
  offset vs. flow velocity and decay constant
- Mesh convergence, cross-section sensitivity, and Monte Carlo
  uncertainty quantification studies

## Running the full study

```bash
conda activate /opt/conda/envs/moose
cd msfr_precursor  # or wherever this repo is cloned
python3 run_everything.py
```

Produces `FINAL_REPORT.txt` with the complete consolidated results.

## Status

Active research project. See `FINAL_REPORT.txt` for the honest list
of validated results vs. open items (real cross sections for Th/Li/F,
primary-source verification of kinetics data, full 3D loop geometry
still pending).
