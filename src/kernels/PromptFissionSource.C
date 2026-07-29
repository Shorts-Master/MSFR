#include "PromptFissionSource.h"

registerMooseObject("MsfrPrecursorApp", PromptFissionSource);

InputParameters
PromptFissionSource::validParams()
{
  InputParameters params = ADKernelValue::validParams();
  params.addClassDescription("Prompt fission neutron production: (1-beta)*nu*Sigma_f*phi, tagged for eigenvalue solve");
  params.addRequiredParam<Real>("nu_sigma_f", "nu * Sigma_f");
  params.addRequiredParam<Real>("beta_total", "Total delayed neutron fraction (summed over all groups)");
  return params;
}

PromptFissionSource::PromptFissionSource(const InputParameters & parameters)
  : ADKernelValue(parameters),
    _nu_sigma_f(getParam<Real>("nu_sigma_f")),
    _beta_total(getParam<Real>("beta_total"))
{
}

ADReal
PromptFissionSource::precomputeQpResidual()
{
  return -(1.0 - _beta_total) * _nu_sigma_f * _u[_qp];
}
