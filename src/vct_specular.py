# -*- coding: utf-8 -*-
from IPython.display import display
import sympy as sp

sp.init_printing(forecolor='White', use_unicode=True, wrap_line=False, no_global=True) 

def test():
    # Angles
    xi, theta, phi = sp.symbols('xi theta phi')
    # Material parameters
    F0, alpha = sp.symbols('F_{0} alpha')
    
    # Dot products
    n_dot_v = sp.cos(xi)
    n_dot_l = sp.cos(theta)
    n_dot_h = (sp.cos(xi) + sp.cos(theta)) / sp.sqrt(2 + 2*sp.sin(xi)*sp.cos(phi)*sp.sin(theta) + 2*sp.cos(xi)*sp.cos(theta))
    v_dot_h = sp.sqrt((1 + sp.sin(xi)*sp.cos(phi)*sp.sin(theta) + sp.cos(xi)*sp.cos(theta))/2)
    
    # BRDF components
    V = 2 / (n_dot_v*sp.sqrt(alpha**2 + (1-alpha**2)*n_dot_l)\
           + n_dot_l*sp.sqrt(alpha**2 + (1-alpha**2)*n_dot_v))
    D = alpha**2 / (sp.pi * (n_dot_h*(alpha**2-1) + 1)**2)
    F = F0 + (1-F0)*(1-v_dot_h)**5
    S = (F * D * V) / 4
    
    # Integral
    integrand  = sp.simplify(S * n_dot_l * sp.sin(theta))
    integral   = sp.Integral(integrand, (theta, 0, sp.pi/2), (phi, 0, 2*sp.pi))
    display(integral)