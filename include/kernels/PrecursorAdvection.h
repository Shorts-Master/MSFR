#pragma once
#include "ADKernelValue.h"

class PrecursorAdvection : public ADKernelValue
{
public:
  static InputParameters validParams();
  PrecursorAdvection(const InputParameters & parameters);

protected:
  virtual ADReal precomputeQpResidual() override;
  const RealVectorValue _velocity;
};
