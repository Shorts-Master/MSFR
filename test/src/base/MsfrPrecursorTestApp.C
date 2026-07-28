//* This file is part of the MOOSE framework
//* https://mooseframework.inl.gov
//*
//* All rights reserved, see COPYRIGHT for full restrictions
//* https://github.com/idaholab/moose/blob/master/COPYRIGHT
//*
//* Licensed under LGPL 2.1, please see LICENSE for details
//* https://www.gnu.org/licenses/lgpl-2.1.html
#include "MsfrPrecursorTestApp.h"
#include "MsfrPrecursorApp.h"
#include "Moose.h"
#include "AppFactory.h"
#include "MooseSyntax.h"

InputParameters
MsfrPrecursorTestApp::validParams()
{
  InputParameters params = MsfrPrecursorApp::validParams();
  params.set<bool>("use_legacy_material_output") = false;
  params.set<bool>("use_legacy_initial_residual_evaluation_behavior") = false;
  return params;
}

MsfrPrecursorTestApp::MsfrPrecursorTestApp(const InputParameters & parameters) : MooseApp(parameters)
{
  MsfrPrecursorTestApp::registerAll(
      _factory, _action_factory, _syntax, getParam<bool>("allow_test_objects"));
}

MsfrPrecursorTestApp::~MsfrPrecursorTestApp() {}

void
MsfrPrecursorTestApp::registerAll(Factory & f, ActionFactory & af, Syntax & s, bool use_test_objs)
{
  MsfrPrecursorApp::registerAll(f, af, s);
  if (use_test_objs)
  {
    Registry::registerObjectsTo(f, {"MsfrPrecursorTestApp"});
    Registry::registerActionsTo(af, {"MsfrPrecursorTestApp"});
  }
}

void
MsfrPrecursorTestApp::registerApps()
{
  registerApp(MsfrPrecursorApp);
  registerApp(MsfrPrecursorTestApp);
}

/***************************************************************************************************
 *********************** Dynamic Library Entry Points - DO NOT MODIFY ******************************
 **************************************************************************************************/
// External entry point for dynamic application loading
extern "C" void
MsfrPrecursorTestApp__registerAll(Factory & f, ActionFactory & af, Syntax & s)
{
  MsfrPrecursorTestApp::registerAll(f, af, s);
}
extern "C" void
MsfrPrecursorTestApp__registerApps()
{
  MsfrPrecursorTestApp::registerApps();
}
