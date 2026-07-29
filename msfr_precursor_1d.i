[Mesh]
  [gen]
    type = GeneratedMeshGenerator
    dim = 1
    xmin = 0
    xmax = 300
    nx = 300
  []
[]

[Problem]
  type = EigenProblem
[]

[Variables]
  [phi]
    initial_condition = 1.0
  []
  [C]
    initial_condition = 0.1
  []
[]

[Kernels]
  [diffusion]
    type = ADMatDiffusion
    variable = phi
    diffusivity = D
  []
  [absorption]
    type = NetRemoval
    variable = phi
    removal_coefficient = 0.003
  []
  [prompt_fission]
    type = PromptFissionSource
    extra_vector_tags = 'eigen'
    variable = phi
    nu_sigma_f = 0.002
    beta_total = 0.0064
  []
  [delayed_source]
    type = DelayedNeutronSource
    variable = phi
    precursor = C
    lambda = 0.08
  []
  [advection]
    type = PrecursorAdvection
    variable = C
    velocity = '50 0 0'
  []
  [decay]
    type = PrecursorDecay
    variable = C
    lambda = 0.08
  []
  [production]
    type = PrecursorProduction
    variable = C
    flux = phi
    beta_i = 0.0064
    nu_sigma_f = 0.002
  []
[]

[Materials]
  [diff_coeff]
    type = ADGenericConstantMaterial
    prop_names = D
    prop_values = 1.2
  []
[]

[BCs]
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
  []
  [C_inlet]
    type = DirichletBC
    variable = C
    boundary = left
    value = 0
  []
[]

[Executioner]
  type = Eigenvalue
  solve_type = PJFNK
  petsc_options_iname = '-pc_type'
  petsc_options_value = 'lu'
[]

[VectorPostprocessors]
  [line_sample]
    type = LineValueSampler
    variable = 'phi C'
    start_point = '0 0 0'
    end_point = '300 0 0'
    num_points = 301
    sort_by = x
  []
[]

[Outputs]
  exodus = true
  csv = true
[]
