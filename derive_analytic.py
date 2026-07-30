import sympy as sp

x, v, lam, k, L, S0 = sp.symbols('x v lambda k L S0', positive=True, real=True)
C = sp.Function('C')

# Flux shape: phi(x) = cos(k*(x - L)), peak at x=L (domain center), zero at x=0 and x=2L
# Governing ODE: v*C' + lambda*C = S0*phi(x) = S0*cos(k*(x-L))
# BC: C(0) = 0 (fresh salt enters with zero precursor concentration)

k_val = sp.pi / (2*L)  # so phi(0)=phi(2L)=0, phi(L)=peak, matches our domain [0, 2L]

ode = sp.Eq(v*sp.diff(C(x), x) + lam*C(x), S0*sp.cos(k_val*(x - L)))
sol = sp.dsolve(ode, C(x))
print("General solution:")
sp.pprint(sol)

# Apply C(0) = 0 to solve for the constant
general_expr = sol.rhs
const = sp.symbols('C1')
const_val = sp.solve(sp.Eq(general_expr.subs(x, 0), 0), const)
print("\nConstant from C(0)=0:")
print(const_val)

if const_val:
    particular = general_expr.subs(const, const_val[0])
    particular = sp.simplify(particular)
    print("\nParticular solution C(x):")
    sp.pprint(particular)

    # Find x where dC/dx = 0 (the peak)
    dCdx = sp.diff(particular, x)
    print("\ndC/dx = 0 equation (peak location):")
    sp.pprint(sp.simplify(dCdx))
