from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp

def copysign(v, x):
    return v if x >= 0.0 else -v

def onb(n):
    s = copysign(1.0, n[2])
    a = -1.0 / (s + n[2])
    b = n[0] * n[1] * a
    b1 = np.array([1.0 + s * n[0] * n[0] * a, s * b, -s * n[0]], dtype=np.float32)
    b2 = np.array([b, s + n[1] * n[1] * a, -n[1]], dtype=np.float32)
    return np.array([b1, b2, n])

###############################################################################
# Cones
###############################################################################
def get_cone(direction):
    # The cone apex angle
    theta   = np.pi / 3.0
    # The cone height
    height  = 1.0
    # The cone radius
    radius  = height * np.tan(0.5 * theta)
    
    nb_height_samples = 16
    np_theta_samples  = 64
    
    # shape (nb_height_samples)
    heights = np.linspace(0.0, height, nb_height_samples)
    # shape (np_theta_samples)
    thetas  = np.linspace(0.0, 2.0 * np.pi, np_theta_samples)
    # shape (np_theta_samples,nb_height_samples)
    H, T    = np.meshgrid(heights, thetas)
    xs      = H / height * radius * np.cos(T)
    ys      = H / height * radius * np.sin(T)
    zs      = H
    # shape (np_theta_samples*nb_height_samples,3)
    ps_tangent       = np.stack((xs.ravel(), ys.ravel(), zs.ravel()), axis=1)
    tangent_to_world = onb(direction)
    ps_world         = np.dot(ps_tangent, tangent_to_world)
    
    xs = np.reshape(ps_world[:,0], (np_theta_samples,nb_height_samples))
    ys = np.reshape(ps_world[:,1], (np_theta_samples,nb_height_samples))
    zs = np.reshape(ps_world[:,2], (np_theta_samples,nb_height_samples))
    return xs, ys, zs
    
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
        xs, ys, zs = get_cone(direction)
        ax.plot_surface(xs, ys, zs)
    
    plt.show()
   
###############################################################################
# Cone Weights
###############################################################################
sp.init_printing(use_unicode=True, wrap_line=False, no_global=True) 
    
def calculate_weights():
    theta, phi = sp.symbols('theta phi')
    eq = sp.Integral( sp.cos(theta)*sp.sin(theta)/sp.pi, (theta, 0, sp.pi/6), (phi, 0, 2*sp.pi))
    w1 = sp.integrate(sp.cos(theta)*sp.sin(theta)/sp.pi, (theta, 0, sp.pi/6), (phi, 0, 2*sp.pi))
    w2 = (1 - w1)/5
    display(eq)
    display(w1)
    display(w2)
