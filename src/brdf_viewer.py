from brdf import BRDF, Material
from geometry import Hemisphere, Vector
from math_utils import reflected_direction
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
import numpy as np

n          = np.array([0.0, 0.0, 1.0])
v          = np.array([-np.sqrt(2)/2, 0.0, np.sqrt(2)/2])
material   = Material(roughness=0.1, F0=0.04)
multiplier = 1.0

brdf_C     = 'All'
brdf_D     = 'GGX'
brdf_F     = 'Schlick'
brdf_V     = 'GGX'

labels_C   =('All', 'D', 'F', 'G', 'V')
labels_D   =('Beckmann', 'Berry', 'Blinn-Phong', 'GGX', 'GTR1', 'GTR2', 'Trowbridge-Reitz', 'Ward-Duer')
labels_F   =('Cook-Torrance', 'None', 'Schlick')
labels_V   =('Ashikhmin-Premoze', 'Cook-Torrance', 'GGX', 'Implicit', 'Neumann', 'Smith_Beckmann', 'Smith_GGX', 'Smith_Schlick-Beckmann', 'Smith_Schlick-GGX', 'Ward')

color_C    = 'purple'
color_D    = 'blue'
color_F    = 'green'
color_V    = 'red'

def update():
    axes.clear()
    axes.set_aspect('equal')
    axes.set_xticks(np.linspace(-1.0,1.0,5))
    axes.set_yticks(np.linspace(-1.0,1.0,5))
    axes.set_zticks(np.linspace( 0.0,2.0,5))
    axes.set_xlim(-1.0,1.0)
    axes.set_ylim(-1.0,1.0)
    axes.set_zlim( 0.0,2.0)
    axes.set_xlabel('X')
    axes.set_ylabel('Y')
    axes.set_zlabel('Z')
    
    brdf = BRDF(D=brdf_D, F=brdf_F, G=brdf_V, V=brdf_V)
    if brdf_C == 'All':
        f, color = brdf.__call__, color_C
    elif brdf_C == 'D':
        f, color = brdf.evaluate_D, color_D
    elif brdf_C == 'F':
        f, color = brdf.evaluate_F, color_F
    elif brdf_C == 'G':
        f, color = brdf.evaluate_G, color_V
    elif brdf_C == 'V':
        f, color = brdf.evaluate_V, color_V
    else:
        f, color = None, None
    
    hemisphere = Hemisphere()
    for i in range(hemisphere.nb_samples[0]):
        for j in range(hemisphere.nb_samples[1]):
            l    = np.array([hemisphere.xs_world[i,j], 
                             hemisphere.ys_world[i,j], 
                             hemisphere.zs_world[i,j]])
            radius = multiplier * f(n=n, l=l, v=v, material=material)
            hemisphere.xs_world[i,j] *= radius
            hemisphere.ys_world[i,j] *= radius
            hemisphere.zs_world[i,j] *= radius
    
    hemisphere.draw(axes, color=color)
    Vector(p_end=n).draw(axes)
    Vector(p_end=v).draw(axes)
    Vector(p_end=reflected_direction(n, v)).draw(axes)
    
def update_C(label):
    global brdf_C
    brdf_C = label
    update()
    fig.canvas.draw_idle()
    
def update_D(label): 
    global brdf_D
    brdf_D = label
    update()
    fig.canvas.draw_idle()
    
def update_F(label):
    global brdf_F
    brdf_F = label
    update()
    fig.canvas.draw_idle()
    
def update_V(label):
    global brdf_V
    brdf_V = label
    update()
    fig.canvas.draw_idle()
    
def update_roughness(roughness):
    material.roughness = roughness
    update()
    fig.canvas.draw_idle()
    
def update_F0(F0):
    material.F0 = F0
    update()
    fig.canvas.draw_idle()
    
def update_multiplier(val):
    global multiplier
    multiplier = val
    update()
    fig.canvas.draw_idle() 
  
###############################################################################
# Figure
###############################################################################
fig = plt.figure()
plt.subplots_adjust(left=0.37, bottom=0.25)
axes = fig.add_subplot(111, projection='3d') 
update()
###############################################################################
# RadioButtons: BRDF
###############################################################################
axes_C  = plt.axes([0.025, 0.75, 0.37, 0.20], aspect='equal', frameon=False)
radio_C = RadioButtons(ax=axes_C, labels=labels_C, active=0, activecolor=color_C)
for label in radio_C.labels:
    label.set_size(10)
for circle in radio_C.circles:
    circle.set_radius(0.05)
radio_C.on_clicked(update_C)

axes_D  = plt.axes([0.025, 0.50, 0.37, 0.25], aspect='equal', frameon=False)
radio_D = RadioButtons(ax=axes_D, labels=labels_D, active=3, activecolor=color_D)
for label in radio_D.labels:
    label.set_size(10)
for circle in radio_D.circles:
    circle.set_radius(0.05)
radio_D.on_clicked(update_D)

axes_F  = plt.axes([0.025, 0.35, 0.37, 0.15], aspect='equal', frameon=False)
radio_F = RadioButtons(ax=axes_F, labels=labels_F, active=2, activecolor=color_F)
for label in radio_F.labels:
    label.set_size(10)
for circle in radio_F.circles:
    circle.set_radius(0.05)
radio_F.on_clicked(update_F)

axes_V  = plt.axes([0.025, 0.05, 0.37, 0.30], aspect='equal', frameon=False)
radio_V = RadioButtons(ax=axes_V, labels=labels_V, active=2, activecolor=color_V)
for label in radio_V.labels:
    label.set_size(10)
for circle in radio_V.circles:
    circle.set_radius(0.05)
radio_V.on_clicked(update_V)

###############################################################################
# Slider: roughness
###############################################################################
axes_roughness   = plt.axes([0.53, 0.09, 0.40, 0.03]) 
slider_roughness = Slider(ax=axes_roughness, label='Roughness',
                          valmin=0.0, valmax=1.0, valfmt='%1.4f',
                          valinit=material.roughness, color=color_C)
slider_roughness.on_changed(update_roughness)
###############################################################################
# Slider: F0
###############################################################################
axes_F0          = plt.axes([0.53, 0.05, 0.40, 0.03]) 
slider_F0        = Slider(ax=axes_F0, label=r'$F_{0}$',
                          valmin=0.0, valmax=1.0, valfmt='%1.4f',
                          valinit=material.F0, color=color_C)
slider_F0.on_changed(update_F0)
###############################################################################
# Slider: multiplier
###############################################################################
axes_multiplier   = plt.axes([0.53, 0.01, 0.40, 0.03]) 
slider_multiplier = Slider(ax=axes_multiplier, label='Multiplier',
                           valmin=0.0, valmax=10.0, valfmt='%1.4f',
                           valinit=multiplier, color=color_C)
slider_multiplier.on_changed(update_multiplier)
###############################################################################
plt.show()
