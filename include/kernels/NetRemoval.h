#pragma once
#include "ADKernelValue.h"

class NetRemoval : public ADKernelValue
{
public:
  static InputParameters validParams();
  NetRemoval(const InputParameters & parameters);

protected:
  virtual ADReal precomputeQpResidual() override;
  const Real _removal_coefficient;
};
