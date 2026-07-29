#include "NetRemoval.h"

registerMooseObject("MsfrPrecursorApp", NetRemoval);

InputParameters
NetRemoval::validParams()
{
  InputParameters params = ADKernelValue::validParams();
  params.addClassDescription("Net removal: Sigma_a*phi - (1-beta)*nu*Sigma_f*phi, lumped");
  params.addRequiredParam<Real>("removal_coefficient", "Sigma_a - (1-beta)*nu_sigma_f");
  return params;
}

NetRemoval::NetRemoval(const InputParameters & parameters)
  : ADKernelValue(parameters), _removal_coefficient(getParam<Real>("removal_coefficient"))
{
}

ADReal
NetRemoval::precomputeQpResidual()
{
  return _removal_coefficient * _u[_qp];
}
