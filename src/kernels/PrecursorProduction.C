#include "PrecursorProduction.h"

registerMooseObject("MsfrPrecursorApp", PrecursorProduction);

InputParameters
PrecursorProduction::validParams()
{
  InputParameters params = ADKernelValue::validParams();
  params.addClassDescription("Precursor production: beta_i * nu * Sigma_f * phi");
  params.addRequiredCoupledVar("flux", "Neutron flux variable");
  params.addRequiredParam<Real>("beta_i", "Delayed neutron fraction, this group");
  params.addRequiredParam<Real>("nu_sigma_f", "nu * Sigma_f");
  return params;
}

PrecursorProduction::PrecursorProduction(const InputParameters & parameters)
  : ADKernelValue(parameters),
    _phi(adCoupledValue("flux")),
    _beta_i(getParam<Real>("beta_i")),
    _nu_sigma_f(getParam<Real>("nu_sigma_f"))
{
}

ADReal
PrecursorProduction::precomputeQpResidual()
{
  return -_beta_i * _nu_sigma_f * _phi[_qp];
}
