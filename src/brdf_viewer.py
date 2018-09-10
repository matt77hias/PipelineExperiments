from brdf import brdf_blinn_phong, brdf_cook_torrance, brdf_ward_duer, Material
from geometry import Hemisphere, Vector
from math_utils import reflected_direction
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
import numpy as np

n        = np.array([0.0, 0.0, 1.0])
v        = np.array([-np.sqrt(2)/2, 0.0, np.sqrt(2)/2])
material = Material(roughness=0.1, F0=0.04)
brdf     = brdf_cook_torrance

def update():
    axes.clear()
    axes.set_aspect('equal')
    axes.set_xticks(np.linspace(-1.0,1.0,5))
    axes.set_yticks(np.linspace(-1.0,1.0,5))
    axes.set_zticks(np.linspace( 0.0,1.0,5))
    axes.set_xlim(-1.0,1.0)
    axes.set_ylim(-1.0,1.0)
    axes.set_zlim( 0.0,1.0)
    axes.set_xlabel('X')
    axes.set_ylabel('Y')
    axes.set_zlabel('Z')
    
    hemisphere = Hemisphere()
    for i in range(hemisphere.nb_samples[0]):
        for j in range(hemisphere.nb_samples[1]):
            l    = np.array([hemisphere.xs_world[i,j], 
                             hemisphere.ys_world[i,j], 
                             hemisphere.zs_world[i,j]])
            radius = brdf(n, l, v, material)
            hemisphere.xs_world[i,j] *= radius
            hemisphere.ys_world[i,j] *= radius
            hemisphere.zs_world[i,j] *= radius
    
    hemisphere.draw(axes)
    Vector(p_end=n).draw(axes)
    Vector(p_end=v).draw(axes)
    Vector(p_end=reflected_direction(n, v)).draw(axes)
    
def update_brdf(label):
    global brdf
    if label == 'Blinn-Phong':
        brdf = brdf_blinn_phong
    elif label == 'Cook-Torrance':
        brdf = brdf_cook_torrance
    elif label == 'Ward-Duer':
        brdf = brdf_ward_duer
    else:
        brdf = None
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
  
###############################################################################
# Figure
###############################################################################
fig = plt.figure()
plt.subplots_adjust(left=0.25, bottom=0.25)
axes = fig.add_subplot(111, projection='3d') 
update()
###############################################################################
# RadioButtons: BRDF
###############################################################################
axes_brdf  = plt.axes([0.025, 0.5, 0.25, 0.25])
radio_brdf = RadioButtons(ax=axes_brdf, labels=('Blinn-Phong', 'Cook-Torrance', 'Ward-Duer'),
                          active=1, activecolor='blue')
radio_brdf.on_clicked(update_brdf)
###############################################################################
# Slider: roughness
###############################################################################
axes_roughness   = plt.axes([0.25, 0.09, 0.40, 0.03]) 
slider_roughness = Slider(ax=axes_roughness, label='Roughness', 
                          valmin=0.0, valmax=1.0, 
                          valinit=material.roughness)
slider_roughness.on_changed(update_roughness)
###############################################################################
# Slider: F0
###############################################################################
axes_F0          = plt.axes([0.25, 0.05, 0.40, 0.03]) 
slider_F0        = Slider(ax=axes_F0, label='F0', 
                          valmin=0.0, valmax=1.0, 
                          valinit=material.F0)
slider_F0.on_changed(update_F0)
###############################################################################
plt.show()