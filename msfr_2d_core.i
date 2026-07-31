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
    removal_coefficient = 0.00120511
  []
  [prompt_fission]
    type = PromptFissionSource
    variable = phi
    nu_sigma_f = 0.002
    beta_total = 0.0028
    extra_vector_tags = 'eigen'
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
[]

[Executioner]
  type = Eigenvalue
  solve_type = PJFNK
  petsc_options_iname = '-pc_type'
  petsc_options_value = 'lu'
[]

[VectorPostprocessors]
  [radial_sample]
    type = LineValueSampler
    variable = 'phi'
    start_point = '0 112.0 0'
    end_point = '112 112.0 0'
    num_points = 57
    sort_by = x
  []
  [axial_sample]
    type = LineValueSampler
    variable = 'phi'
    start_point = '0 0 0'
    end_point = '0 224 0'
    num_points = 113
    sort_by = y
  []
[]

[Outputs]
  exodus = true
  csv = true
[]
