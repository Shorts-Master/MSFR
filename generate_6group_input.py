"""
Generates a 6-precursor-group MSFR input file for msfr_precursor-opt.
Standard 6-group delayed neutron data (illustrative U-235 thermal values;
replace with MSFR-specific data before this becomes a real result).
"""

# (lambda_i [1/s], beta_i) for each of the 6 groups
GROUPS = [
    (0.0124, 0.000215),
    (0.0305, 0.001424),
    (0.111,  0.001274),
    (0.301,  0.002568),
    (1.14,   0.000748),
    (3.01,   0.000273),
]

BETA_TOTAL = sum(b for _, b in GROUPS)
NU_SIGMA_F = 0.002
REMOVAL_COEFFICIENT = 0.003
DIFFUSIVITY = 1.2
DOMAIN_LENGTH = 300
NX = 300
VELOCITY = "50 0 0"

def generate(velocity=VELOCITY, filename="msfr_precursor_6group.i"):
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

    # Kernels
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
    nu_sigma_f = {NU_SIGMA_F}
  []""")

    lines.append("[]\n")

    # Materials
    lines.append(f"""[Materials]
  [diff_coeff]
    type = ADGenericConstantMaterial
    prop_names = D
    prop_values = {DIFFUSIVITY}
  []
[]
""")

    # BCs
    lines.append("""[BCs]
  [phi_left]
    type = DirichletBC
    variable = phi
    boundary = left
    value = 0
  []
  [phi_left_eigen]
    type = EigenDirichletBC
    variable = phi
    boundary = left
  []
  [phi_right]
    type = DirichletBC
    variable = phi
    boundary = right
    value = 0
  []
  [phi_right_eigen]
    type = EigenDirichletBC
    variable = phi
    boundary = right
  []""")

    for i in range(6):
        lines.append(f"""  [C{i}_inlet]
    type = DirichletBC
    variable = C{i}
    boundary = left
    value = 0
  []""")

    lines.append("[]\n")

    # Executioner
    lines.append("""[Executioner]
  type = Eigenvalue
  solve_type = PJFNK
  petsc_options_iname = '-pc_type'
  petsc_options_value = 'lu'
[]
""")

    # VectorPostprocessors
    varlist = "phi " + " ".join(f"C{i}" for i in range(6))
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
    print(f"Total beta = {BETA_TOTAL:.6f}")

if __name__ == "__main__":
    generate()
