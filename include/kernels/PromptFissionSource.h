#pragma once
#include "ADKernelValue.h"

class PromptFissionSource : public ADKernelValue
{
public:
  static InputParameters validParams();
  PromptFissionSource(const InputParameters & parameters);

protected:
  virtual ADReal precomputeQpResidual() override;
  const Real _nu_sigma_f;
  const Real _beta_total;
};
