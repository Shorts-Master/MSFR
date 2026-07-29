#pragma once
#include "ADKernelValue.h"

class PrecursorDecay : public ADKernelValue
{
public:
  static InputParameters validParams();
  PrecursorDecay(const InputParameters & parameters);

protected:
  virtual ADReal precomputeQpResidual() override;
  const Real _lambda;
};
