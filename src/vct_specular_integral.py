# -*- coding: utf-8 -*-
from IPython.display import display
import sympy as sp

sp.init_printing(forecolor='White', use_unicode=True, wrap_line=False, no_global=True)

def ses(exp):
    return exp
    #return sp.simplify(sp.expand(sp.simplify(exp)))

def compute():
    x = sp.symbols('x')
    # Angles
    xi, phi = sp.symbols('xi phi')
    # Material parameters
    F0, alpha = sp.symbols('F_{0} alpha')
    
    # Dot products
    n_dot_v = sp.cos(xi)
    n_dot_l = x
    n_dot_h = (sp.cos(xi) + x) / sp.sqrt(2 + 2*sp.sin(xi)*sp.cos(phi)*sp.sqrt(1-x**2) + 2*sp.cos(xi)*x)
    v_dot_h = sp.sqrt((1 + sp.sin(xi)*sp.cos(phi)*sp.sqrt(1-x**2) + sp.cos(xi)*x)/2)
    
    # BRDF components
    V = 2 / (n_dot_v*sp.sqrt(alpha**2 + (1-alpha**2)*n_dot_l)\
           + n_dot_l*sp.sqrt(alpha**2 + (1-alpha**2)*n_dot_v))
    V = ses(V)
    
    D = alpha**2 / (sp.pi * (n_dot_h*(alpha**2-1) + 1)**2)
    D = ses(D)
    
    F = F0 + (1-F0)*(1-v_dot_h)**5
    F = ses(F)
    
    S = (F * D * V) / 4
    S = ses(S)
    
    # Integral
    integrand = ses(S * x)
    integral  = sp.Integral(integrand, (x, 0, 1), (phi, 0, 2*sp.pi))
    display(integral)
