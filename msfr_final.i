[Mesh]
  [gen]
    type = GeneratedMeshGenerator
    dim = 2
    xmin = 0
    xmax = 112
    ymin = 0
    ymax = 224
    nx = 56
    ny = 112
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
    removal_coefficient = 0.00262173
  []
  [prompt_fission]
    type = PromptFissionSource
    variable = phi
    nu_sigma_f = 0.0034179
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
    velocity = '0 110 0'
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
    nu_sigma_f = 0.0034179
  []
  [advection_1]
    type = PrecursorAdvection
    variable = C1
    velocity = '0 110 0'
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
    nu_sigma_f = 0.0034179
  []
  [advection_2]
    type = PrecursorAdvection
    variable = C2
    velocity = '0 110 0'
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
    nu_sigma_f = 0.0034179
  []
  [advection_3]
    type = PrecursorAdvection
    variable = C3
    velocity = '0 110 0'
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
    nu_sigma_f = 0.0034179
  []
  [advection_4]
    type = PrecursorAdvection
    variable = C4
    velocity = '0 110 0'
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
    nu_sigma_f = 0.0034179
  []
  [advection_5]
    type = PrecursorAdvection
    variable = C5
    velocity = '0 110 0'
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
    nu_sigma_f = 0.0034179
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
  []
  [C0_inlet]
    type = DirichletBC
    variable = C0
    boundary = bottom
    value = 0
  []
  [C1_inlet]
    type = DirichletBC
    variable = C1
    boundary = bottom
    value = 0
  []
  [C2_inlet]
    type = DirichletBC
    variable = C2
    boundary = bottom
    value = 0
  []
  [C3_inlet]
    type = DirichletBC
    variable = C3
    boundary = bottom
    value = 0
  []
  [C4_inlet]
    type = DirichletBC
    variable = C4
    boundary = bottom
    value = 0
  []
  [C5_inlet]
    type = DirichletBC
    variable = C5
    boundary = bottom
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
  [centerline_axial]
    type = LineValueSampler
    variable = 'phi C0 C1 C2 C3 C4 C5'
    start_point = '0 0 0'
    end_point = '0 224 0'
    num_points = 113
    sort_by = y
  []
  [midheight_radial]
    type = LineValueSampler
    variable = 'phi C0 C1 C2 C3 C4 C5'
    start_point = '0 112.0 0'
    end_point = '112 112.0 0'
    num_points = 57
    sort_by = x
  []
[]

[Outputs]
  exodus = true
  csv = true
[]
