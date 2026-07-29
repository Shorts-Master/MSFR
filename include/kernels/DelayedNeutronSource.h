#pragma once
#include "ADKernelValue.h"

class DelayedNeutronSource : public ADKernelValue
{
public:
  static InputParameters validParams();
  DelayedNeutronSource(const InputParameters & parameters);

protected:
  virtual ADReal precomputeQpResidual() override;
  const ADVariableValue & _C;
  const Real _lambda;
};
