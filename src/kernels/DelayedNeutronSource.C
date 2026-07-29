#include "DelayedNeutronSource.h"

registerMooseObject("MsfrPrecursorApp", DelayedNeutronSource);

InputParameters
DelayedNeutronSource::validParams()
{
  InputParameters params = ADKernelValue::validParams();
  params.addClassDescription("Delayed neutron source in flux equation: lambda * C");
  params.addRequiredCoupledVar("precursor", "Precursor concentration variable");
  params.addRequiredParam<Real>("lambda", "Decay constant (1/s)");
  return params;
}

DelayedNeutronSource::DelayedNeutronSource(const InputParameters & parameters)
  : ADKernelValue(parameters),
    _C(adCoupledValue("precursor")),
    _lambda(getParam<Real>("lambda"))
{
}

ADReal
DelayedNeutronSource::precomputeQpResidual()
{
  return -_lambda * _C[_qp];
}
