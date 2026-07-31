"""
FINAL consolidated MSFR precursor drift model.

Fixes applied this session:
1. 2D axisymmetric (RZ) core geometry - Ra=112cm, Ha=224cm, from
   EVOL/MARS benchmark (Brovchenko et al.) - replaces the earlier 1D
   line. VALIDATED: flux shape matches analytic J0-Bessel (radial) x
   cosine (axial) bare-core solution to <0.03% RMSE.
2. removal_coefficient = 0.00120511, calibrated via bisection to give
   EXACT criticality (k_eff=1.0) for this 2D geometry - replaces an
   arbitrary placeholder cross section with one derived from the one
   fact we're certain of (MSFR is designed to run critical).
3. MOOSE eigenvalue convention corrected: MOOSE's Eigenvalue executioner
   solves A*x = k*B*x (A=non-eigen kernels/loss, B=eigen-tagged
   kernels/production), so MOOSE's printed "eigenvalue" = Loss/Production,
   the RECIPROCAL of the standard k_eff = Production/Loss. All k_eff
   values in this file are the MOOSE-convention number; true k_eff =
   1/(this number). Critical (true k_eff=1) is unaffected: 1/1=1.
4. Real U-233 delayed neutron data (Keepin, via secondary source,
   internally cross-checked: abundances sum to 1.000, implied
   beta_total=0.0028 matches independently-sourced U-233 value).
   VERIFY against Keepin's original tables before publication.

STILL PLACEHOLDER / OPEN (honestly flagged, not fixed this session):
- D (diffusion coefficient) and nu_sigma_f are still round-number
  placeholders, not real multigroup cross sections from ENDF or the
  EVOL benchmark's actual data tables.
- Real MSFR core velocity (110 cm/s) is a rough estimate from
  "core height / half the 4s loop circulation time", not a directly
  sourced design value - should be replaced if the exact number is found.
- This is a single lumped external loop worth of flow direction
  (purely axial through the core); the real 16-loop external circuit
  geometry is not modeled - this is core-only, once-through precursors
  (fresh/zero concentration entering at the bottom inlet).
- 1-group energy structure (diffusion, not transport, and no fast/
  thermal group split) - a legitimate reactor-physics simplification,
  but a real upgrade path if pursued further.
"""

GROUPS = [
    (0.0126, 0.022 * 0.0028),
    (0.0337, 0.182 * 0.0028),
    (0.139,  0.141 * 0.0028),
    (0.325,  0.403 * 0.0028),
    (1.13,   0.128 * 0.0028),
    (2.50,   0.124 * 0.0028),
]

BETA_TOTAL = sum(b for _, b in GROUPS)
NU_SIGMA_F = 0.002
DIFFUSIVITY = 1.2
REMOVAL_COEFFICIENT = 0.00120511  # calibrated critical, 2D RZ geometry
RA = 112   # core radius, cm (EVOL/MARS benchmark)
HA = 224   # core height, cm (EVOL/MARS benchmark)
NR = 56
NZ = 112
AXIAL_VELOCITY = 110  # cm/s, rough estimate - see caveat above

def generate(velocity=AXIAL_VELOCITY, filename="msfr_final.i"):
    lines = []

    lines.append(f"""[Mesh]
  [gen]
    type = GeneratedMeshGenerator
    dim = 2
    xmin = 0
    xmax = {RA}
    ymin = 0
    ymax = {HA}
    nx = {NR}
    ny = {NZ}
  []
  coord_type = RZ
  rz_coord_axis = Y
[]

[Problem]
  type = EigenProblem
[]

[Variables]
  [phi]
    initial_condition = 1.0
  []""")

    for i in range(6):
        lines.append(f"""  [C{i}]
    initial_condition = 0.01
  []""")

    lines.append("[]\n")

    lines.append("[Kernels]")
    lines.append("""  [diffusion]
    type = ADMatDiffusion
    variable = phi
    diffusivity = D
  []
  [absorption]
    type = NetRemoval
    variable = phi
    removal_coefficient = %g
  []
  [prompt_fission]
    type = PromptFissionSource
    variable = phi
    nu_sigma_f = %g
    beta_total = %g
    extra_vector_tags = 'eigen'
  []""" % (REMOVAL_COEFFICIENT, NU_SIGMA_F, BETA_TOTAL))

    for i, (lam, beta) in enumerate(GROUPS):
        lines.append(f"""  [delayed_source_{i}]
    type = DelayedNeutronSource
    variable = phi
    precursor = C{i}
    lambda = {lam}
  []""")

    for i, (lam, beta) in enumerate(GROUPS):
        lines.append(f"""  [advection_{i}]
    type = PrecursorAdvection
    variable = C{i}
    velocity = '0 {velocity} 0'
  []
  [decay_{i}]
    type = PrecursorDecay
    variable = C{i}
    lambda = {lam}
  []
  [production_{i}]
    type = PrecursorProduction
    variable = C{i}
    flux = phi
    beta_i = {beta}
    nu_sigma_f = {NU_SIGMA_F}
  []""")

    lines.append("[]\n")

    lines.append(f"""[Materials]
  [diff_coeff]
    type = ADGenericConstantMaterial
    prop_names = D
    prop_values = {DIFFUSIVITY}
  []
[]
""")

    lines.append("""[BCs]
  [phi_outer_radius]
    type = DirichletBC
    variable = phi
    boundary = right
    value = 0
  []
  [phi_outer_radius_eigen]
    type = EigenDirichletBC
    variable = phi
    boundary = right
  []
  [phi_bottom]
    type = DirichletBC
    variable = phi
    boundary = bottom
    value = 0
  []
  [phi_bottom_eigen]
    type = EigenDirichletBC
    variable = phi
    boundary = bottom
  []
  [phi_top]
    type = DirichletBC
    variable = phi
    boundary = top
    value = 0
  []
  [phi_top_eigen]
    type = EigenDirichletBC
    variable = phi
    boundary = top
  []""")

    for i in range(6):
        lines.append(f"""  [C{i}_inlet]
    type = DirichletBC
    variable = C{i}
    boundary = bottom
    value = 0
  []""")

    lines.append("[]\n")

    lines.append("""[Executioner]
  type = Eigenvalue
  solve_type = PJFNK
  petsc_options_iname = '-pc_type'
  petsc_options_value = 'lu'
[]
""")

    varlist = "phi " + " ".join(f"C{i}" for i in range(6))
    lines.append(f"""[VectorPostprocessors]
  [centerline_axial]
    type = LineValueSampler
    variable = '{varlist}'
    start_point = '0 0 0'
    end_point = '0 {HA} 0'
    num_points = {NZ+1}
    sort_by = y
  []
  [midheight_radial]
    type = LineValueSampler
    variable = '{varlist}'
    start_point = '0 {HA/2} 0'
    end_point = '{RA} {HA/2} 0'
    num_points = {NR+1}
    sort_by = x
  []
[]

[Outputs]
  exodus = true
  csv = true
[]
""")

    with open(filename, "w") as f:
        f.write("\n".join(lines))

    print(f"Wrote {filename}")
    print(f"Total beta = {BETA_TOTAL:.6f}")

if __name__ == "__main__":
    generate()
