# -*- coding: utf-8 -*-
from geometry import Cone
from IPython.display import display
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sympy as sp
  
###############################################################################
# Cones
###############################################################################
def draw_cones():
    fig = plt.figure()
    ax  = fig.gca(projection='3d')
    ax.set_aspect('equal')
    ax.set_xticks(np.linspace(-1.0,1.0,5))
    ax.set_yticks(np.linspace(-1.0,1.0,5))
    ax.set_zticks(np.linspace(-1.0,1.0,5))
    ax.set_xlim(-1.0,1.0)
    ax.set_ylim(-1.0,1.0)
    ax.set_zlim(-1.0,1.0)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    directions = [np.array([ 0.000000,  0.000000, 1.0]), \
                  np.array([ 0.000000,  0.866025, 0.5]), \
                  np.array([ 0.823639,  0.267617, 0.5]), \
                  np.array([ 0.509037, -0.700629, 0.5]), \
                  np.array([-0.509037, -0.700629, 0.5]), \
                  np.array([-0.823639,  0.267617, 0.5])]
    for direction in directions:
        cone = Cone(d_world=direction)
        cone.draw(ax)
        
    plt.show()
   
###############################################################################
# Cone Weights
###############################################################################
sp.init_printing(forecolor='White', use_unicode=True, wrap_line=False, no_global=True) 
    
def calculate_weights():
    theta, phi = sp.symbols('theta phi')
    eq = sp.Integral( sp.cos(theta)*sp.sin(theta)/sp.pi, (theta, 0, sp.pi/6), (phi, 0, 2*sp.pi))
    w1 = sp.integrate(sp.cos(theta)*sp.sin(theta)/sp.pi, (theta, 0, sp.pi/6), (phi, 0, 2*sp.pi))
    w2 = (1 - w1)/5
    display(eq)
    display(w1)
    display(w2)
