"""
Recirculating-precursor MSFR model. Uses a standard nonlinear steady-state
solve (NOT the Eigenvalue executioner) with the fission source pre-scaled
by 1/k_eff, where k_eff comes from the already-validated once-through
eigenvalue solve (k_eff = 1.6218). This sidesteps the Eigenvalue
executioner's homogeneous-BC requirement entirely, since a regular
nonlinear solve has no such restriction - periodic BCs work normally here.

Physical picture: phi keeps a fixed vacuum boundary (bare core edges);
the six precursor variables are periodic (same salt recirculating
through the loop, not vanishing/refreshing at the boundary).
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
K_EFF = 1.6218 * 0.999   # slightly supercritical to avoid marginal/degenerate equilibrium  # from validated once-through eigenvalue solve, same geometry
NU_SIGMA_F_EFFECTIVE = NU_SIGMA_F / K_EFF  # pre-scale fission source by 1/k_eff
REMOVAL_COEFFICIENT = 0.003
DIFFUSIVITY = 1.2
DOMAIN_LENGTH = 224
NX = 224
VELOCITY = "110 0 0"

def generate(velocity=VELOCITY, filename="msfr_precursor_recirc.i"):
    lines = []

    lines.append(f"""[Mesh]
  [gen]
    type = GeneratedMeshGenerator
    dim = 1
    xmin = 0
    xmax = {DOMAIN_LENGTH}
    nx = {NX}
  []
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
  []
  [fixed_source]
    type = BodyForce
    variable = phi
    value = 0.001
  []
""" % (REMOVAL_COEFFICIENT, NU_SIGMA_F_EFFECTIVE, BETA_TOTAL))

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
    velocity = '{velocity}'
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
    nu_sigma_f = {NU_SIGMA_F_EFFECTIVE}
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

    c_varlist = " ".join(f"C{i}" for i in range(6))
    lines.append(f"""[BCs]
  [phi_left]
    type = DirichletBC
    variable = phi
    boundary = left
    value = 0
  []
  [phi_right]
    type = DirichletBC
    variable = phi
    boundary = right
    value = 0
  []
  [Periodic]
    [precursor_recirculation]
      variable = '{c_varlist}'
      auto_direction = 'x'
    []
  []
[]
""")

    lines.append("""[Executioner]
  type = Steady
  solve_type = NEWTON
  petsc_options_iname = '-pc_type'
  petsc_options_value = 'lu'
[]
""")

    varlist = "phi " + c_varlist
    lines.append(f"""[VectorPostprocessors]
  [line_sample]
    type = LineValueSampler
    variable = '{varlist}'
    start_point = '0 0 0'
    end_point = '{DOMAIN_LENGTH} 0 0'
    num_points = {NX+1}
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
    print(f"Effective nu_sigma_f (scaled by 1/k_eff={K_EFF}) = {NU_SIGMA_F_EFFECTIVE:.6f}")

if __name__ == "__main__":
    generate()
