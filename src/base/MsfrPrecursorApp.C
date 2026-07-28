#include "MsfrPrecursorApp.h"
#include "Moose.h"
#include "AppFactory.h"
#include "ModulesApp.h"
#include "MooseSyntax.h"

InputParameters
MsfrPrecursorApp::validParams()
{
  InputParameters params = MooseApp::validParams();
  params.set<bool>("use_legacy_material_output") = false;
  params.set<bool>("use_legacy_initial_residual_evaluation_behavior") = false;
  return params;
}

MsfrPrecursorApp::MsfrPrecursorApp(const InputParameters & parameters) : MooseApp(parameters)
{
  MsfrPrecursorApp::registerAll(_factory, _action_factory, _syntax);
}

MsfrPrecursorApp::~MsfrPrecursorApp() {}

void
MsfrPrecursorApp::registerAll(Factory & f, ActionFactory & af, Syntax & syntax)
{
  ModulesApp::registerAllObjects<MsfrPrecursorApp>(f, af, syntax);
  Registry::registerObjectsTo(f, {"MsfrPrecursorApp"});
  Registry::registerActionsTo(af, {"MsfrPrecursorApp"});

  /* register custom execute flags, action syntax, etc. here */
}

void
MsfrPrecursorApp::registerApps()
{
  registerApp(MsfrPrecursorApp);
}

/***************************************************************************************************
 *********************** Dynamic Library Entry Points - DO NOT MODIFY ******************************
 **************************************************************************************************/
extern "C" void
MsfrPrecursorApp__registerAll(Factory & f, ActionFactory & af, Syntax & s)
{
  MsfrPrecursorApp::registerAll(f, af, s);
}
extern "C" void
MsfrPrecursorApp__registerApps()
{
  MsfrPrecursorApp::registerApps();
}
