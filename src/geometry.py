from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D, proj3d
import numpy as np
from onb import OrthonormalBasis as onb

###############################################################################
# Tangent <> World
###############################################################################
def transform_tangent_to_world(xs_tangent, ys_tangent, zs_tangent, p_world, d_world):
    tangent_to_world = onb(d_world)
    ps_tangent       = np.stack((xs_tangent.ravel(),
                                 ys_tangent.ravel(),
                                 zs_tangent.ravel()), axis=1)
    ps_world         = np.dot(ps_tangent, tangent_to_world) - p_world
    
    xs_world         = np.reshape(ps_world[:,0], xs_tangent.shape)
    ys_world         = np.reshape(ps_world[:,1], ys_tangent.shape)
    zs_world         = np.reshape(ps_world[:,2], zs_tangent.shape)
    
    return xs_world, ys_world, zs_world

###############################################################################
# Arrow
###############################################################################
class Arrow(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]), (xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)
        
class Vector:
    
    def __init__(self,
                 p_start = np.zeros((3)),
                 p_end   = np.array([1.0,0.0,0.0])):
        
        self.p_start = p_start
        self.p_end   = p_end
        
    def draw(self, axes, *args, **kwargs):
        arrow = Arrow((self.p_start[0],self.p_end[0]),
                      (self.p_start[1],self.p_end[1]),
                      (self.p_start[2],self.p_end[2]),
                      mutation_scale=10,
                      lw=1,
                      arrowstyle="-|>",
                      *args, *kwargs)
        axes.add_artist(arrow)
        
###############################################################################
# Cone
###############################################################################
class Cone:
    
    def __init__(self,
                 p_world    = np.zeros((3)),
                 aperture   = np.pi/3.0,
                 d_world    = np.array([1.0,0.0,0.0]),
                 height     = 1.0,
                 nb_samples = (16,64)):
        
        self.p_world    = p_world
        self.aperture   = aperture
        self.d_world    = d_world
        self.height     = height
        self.radius     = self.height * np.tan(0.5 * self.aperture)
        self.nb_samples = nb_samples
        
        self.construct()
        
    def construct(self):
        # shape (nb_height_samples)
        heights    = np.linspace(start=0.0, stop=self.height, num=self.nb_samples[0])
        # shape (np_theta_samples)
        thetas     = np.linspace(start=0.0, stop=2.0 * np.pi, num=self.nb_samples[1])
        # shape (nb_height_samples,np_theta_samples)
        H, T       = np.meshgrid(heights, thetas, indexing='ij')
        xs_tangent = H / self.height * self.radius * np.cos(T)
        ys_tangent = H / self.height * self.radius * np.sin(T)
        zs_tangent = H
        
        self.xs_world, self.ys_world, self.zs_world \
            = transform_tangent_to_world(xs_tangent=xs_tangent,
                                         ys_tangent=ys_tangent,
                                         zs_tangent=zs_tangent,
                                         p_world=self.p_world,
                                         d_world=self.d_world)
        

    def draw(self, axes, *args, **kwargs):
        axes.plot_surface(X=self.xs_world,
                          Y=self.ys_world,
                          Z=self.zs_world,
                          *args, **kwargs)

###############################################################################
# Hemisphere
###############################################################################
class Hemisphere:
    
    def __init__(self,
                 p_world    = np.zeros((3)),
                 d_world    = np.array([0.0,0.0,1.0]),
                 radius     = 1.0,
                 nb_samples = (16,64)):
        
        self.p_world    = p_world
        self.d_world    = d_world
        self.radius     = radius
        self.nb_samples = nb_samples
        
        self.construct() 
        
    def construct(self):
        # shape (nb_cos_theta_samples)
        cos_thetas = np.linspace(start=0.0, stop=1.0,         num=self.nb_samples[0])
        # shape (np_phi_samples)
        phis       = np.linspace(start=0.0, stop=2.0 * np.pi, num=self.nb_samples[1])
        # shape (nb_cos_theta_samples,np_phi_samples)
        CosT, P    = np.meshgrid(cos_thetas, phis, indexing='ij')
        SinT       = np.sqrt(1.0 - CosT * CosT)
        xs_tangent = self.radius * np.cos(P) * SinT
        ys_tangent = self.radius * np.sin(P) * SinT
        zs_tangent = self.radius * CosT
        
        self.xs_world, self.ys_world, self.zs_world \
            = transform_tangent_to_world(xs_tangent=xs_tangent,
                                         ys_tangent=ys_tangent,
                                         zs_tangent=zs_tangent,
                                         p_world=self.p_world, 
                                         d_world=self.d_world)
    
    def draw(self, axes, *args, **kwargs):
        axes.plot_surface(X=self.xs_world,
                          Y=self.ys_world,
                          Z=self.zs_world,
                          *args, **kwargs)
