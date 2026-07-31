"""
2D axisymmetric (RZ) bare cylindrical core, neutron diffusion only.
Real MSFR dimensions: Ra=112cm (radius), Ha=224cm (height), from
EVOL/MARS benchmark. Foundational check before adding precursor
transport on top of this geometry - verifies the eigenvalue solve
and flux shape are physically sensible in 2D before adding complexity.
"""

RA = 112   # core radius, cm
HA = 224   # core height, cm
NR = 56
NZ = 112
NU_SIGMA_F = 0.002
DIFFUSIVITY = 1.2
REMOVAL_COEFFICIENT = 0.00120511  # calibrated to k_eff=1.0 for 2D RZ core, Ra=112cm Ha=224cm
BETA_TOTAL = 0.0028  # total delayed fraction, no precursor transport in this step

def generate(filename="msfr_2d_core.i"):
    content = f"""[Mesh]
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
    removal_coefficient = {REMOVAL_COEFFICIENT}
  []
  [prompt_fission]
    type = PromptFissionSource
    variable = phi
    nu_sigma_f = {NU_SIGMA_F}
    beta_total = {BETA_TOTAL}
    extra_vector_tags = 'eigen'
  []
[]

[Materials]
  [diff_coeff]
    type = ADGenericConstantMaterial
    prop_names = D
    prop_values = {DIFFUSIVITY}
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
    start_point = '0 {HA/2} 0'
    end_point = '{RA} {HA/2} 0'
    num_points = {NR+1}
    sort_by = x
  []
  [axial_sample]
    type = LineValueSampler
    variable = 'phi'
    start_point = '0 0 0'
    end_point = '0 {HA} 0'
    num_points = {NZ+1}
    sort_by = y
  []
[]

[Outputs]
  exodus = true
  csv = true
[]
"""
    with open(filename, "w") as f:
        f.write(content)
    print(f"Wrote {filename}")

if __name__ == "__main__":
    generate()
