#include "PrecursorDecay.h"

registerMooseObject("MsfrPrecursorApp", PrecursorDecay);

InputParameters
PrecursorDecay::validParams()
{
  InputParameters params = ADKernelValue::validParams();
  params.addClassDescription("Precursor decay term: lambda * C");
  params.addRequiredParam<Real>("lambda", "Decay constant (1/s)");
  return params;
}

PrecursorDecay::PrecursorDecay(const InputParameters & parameters)
  : ADKernelValue(parameters), _lambda(getParam<Real>("lambda"))
{
}

ADReal
PrecursorDecay::precomputeQpResidual()
{
  return _lambda * _u[_qp];
}
