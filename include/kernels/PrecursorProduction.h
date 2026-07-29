#pragma once
#include "ADKernelValue.h"

class PrecursorProduction : public ADKernelValue
{
public:
  static InputParameters validParams();
  PrecursorProduction(const InputParameters & parameters);

protected:
  virtual ADReal precomputeQpResidual() override;
  const ADVariableValue & _phi;
  const Real _beta_i;
  const Real _nu_sigma_f;
};
