[Mesh]
  [gen]
    type = GeneratedMeshGenerator
    dim = 1
    xmin = 0
    xmax = 224
    nx = 224
  []
[]

[Problem]
  type = EigenProblem
[]

[Variables]
  [phi]
    initial_condition = 1.0
  []
  [C0]
    initial_condition = 0.01
  []
  [C1]
    initial_condition = 0.01
  []
  [C2]
    initial_condition = 0.01
  []
  [C3]
    initial_condition = 0.01
  []
  [C4]
    initial_condition = 0.01
  []
  [C5]
    initial_condition = 0.01
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
    variable = phi
    nu_sigma_f = 0.002
    beta_total = 0.0028
    extra_vector_tags = 'eigen'
  []
  [delayed_source_0]
    type = DelayedNeutronSource
    variable = phi
    precursor = C0
    lambda = 0.0126
  []
  [delayed_source_1]
    type = DelayedNeutronSource
    variable = phi
    precursor = C1
    lambda = 0.0337
  []
  [delayed_source_2]
    type = DelayedNeutronSource
    variable = phi
    precursor = C2
    lambda = 0.139
  []
  [delayed_source_3]
    type = DelayedNeutronSource
    variable = phi
    precursor = C3
    lambda = 0.325
  []
  [delayed_source_4]
    type = DelayedNeutronSource
    variable = phi
    precursor = C4
    lambda = 1.13
  []
  [delayed_source_5]
    type = DelayedNeutronSource
    variable = phi
    precursor = C5
    lambda = 2.5
  []
  [advection_0]
    type = PrecursorAdvection
    variable = C0
    velocity = '400 0 0'
  []
  [decay_0]
    type = PrecursorDecay
    variable = C0
    lambda = 0.0126
  []
  [production_0]
    type = PrecursorProduction
    variable = C0
    flux = phi
    beta_i = 6.159999999999999e-05
    nu_sigma_f = 0.002
  []
  [advection_1]
    type = PrecursorAdvection
    variable = C1
    velocity = '400 0 0'
  []
  [decay_1]
    type = PrecursorDecay
    variable = C1
    lambda = 0.0337
  []
  [production_1]
    type = PrecursorProduction
    variable = C1
    flux = phi
    beta_i = 0.0005096
    nu_sigma_f = 0.002
  []
  [advection_2]
    type = PrecursorAdvection
    variable = C2
    velocity = '400 0 0'
  []
  [decay_2]
    type = PrecursorDecay
    variable = C2
    lambda = 0.139
  []
  [production_2]
    type = PrecursorProduction
    variable = C2
    flux = phi
    beta_i = 0.00039479999999999995
    nu_sigma_f = 0.002
  []
  [advection_3]
    type = PrecursorAdvection
    variable = C3
    velocity = '400 0 0'
  []
  [decay_3]
    type = PrecursorDecay
    variable = C3
    lambda = 0.325
  []
  [production_3]
    type = PrecursorProduction
    variable = C3
    flux = phi
    beta_i = 0.0011284
    nu_sigma_f = 0.002
  []
  [advection_4]
    type = PrecursorAdvection
    variable = C4
    velocity = '400 0 0'
  []
  [decay_4]
    type = PrecursorDecay
    variable = C4
    lambda = 1.13
  []
  [production_4]
    type = PrecursorProduction
    variable = C4
    flux = phi
    beta_i = 0.0003584
    nu_sigma_f = 0.002
  []
  [advection_5]
    type = PrecursorAdvection
    variable = C5
    velocity = '400 0 0'
  []
  [decay_5]
    type = PrecursorDecay
    variable = C5
    lambda = 2.5
  []
  [production_5]
    type = PrecursorProduction
    variable = C5
    flux = phi
    beta_i = 0.0003472
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
  [C0_inlet]
    type = DirichletBC
    variable = C0
    boundary = left
    value = 0
  []
  [C1_inlet]
    type = DirichletBC
    variable = C1
    boundary = left
    value = 0
  []
  [C2_inlet]
    type = DirichletBC
    variable = C2
    boundary = left
    value = 0
  []
  [C3_inlet]
    type = DirichletBC
    variable = C3
    boundary = left
    value = 0
  []
  [C4_inlet]
    type = DirichletBC
    variable = C4
    boundary = left
    value = 0
  []
  [C5_inlet]
    type = DirichletBC
    variable = C5
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
    variable = 'phi C0 C1 C2 C3 C4 C5'
    start_point = '0 0 0'
    end_point = '224 0 0'
    num_points = 225
    sort_by = x
  []
[]

[Outputs]
  exodus = true
  csv = true
[]
