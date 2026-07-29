#include "PrecursorAdvection.h"

registerMooseObject("MsfrPrecursorApp", PrecursorAdvection);

InputParameters
PrecursorAdvection::validParams()
{
  InputParameters params = ADKernelValue::validParams();
  params.addClassDescription("Advects delayed neutron precursors with bulk salt flow: u . grad(C)");
  params.addRequiredParam<RealVectorValue>("velocity", "Bulk salt flow velocity vector");
  return params;
}

PrecursorAdvection::PrecursorAdvection(const InputParameters & parameters)
  : ADKernelValue(parameters), _velocity(getParam<RealVectorValue>("velocity"))
{
}

ADReal
PrecursorAdvection::precomputeQpResidual()
{
  return _velocity * _grad_u[_qp];
}
