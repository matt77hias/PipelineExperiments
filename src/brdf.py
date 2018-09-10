# -*- coding: utf-8 -*-
from geometry import Hemisphere, Vector
from math_utils import lerp, sat_dot, sqr, sqrt, sqr_cos_to_sqr_tan, half_direction, reflected_direction
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

###############################################################################
# Constants
###############################################################################

g_dielectric_F0 = 0.04

###############################################################################
# Normal Distribution Function
###############################################################################

def D_Beckmann(n_dot_h, alpha):
    #               1            [  n_dot_h^2 - 1  ]             1             [tan(theta_h)]^2
    # D:= -------------------- e^[-----------------] = -------------------- e^-[------------]
    #     pi alpha^2 n_dot_h^4   [n_dot_h^2 alpha^2]   pi alpha^2 n_dot_h^4    [   alpha    ]
    
    inv_alpha2   = 1.0 / sqr(alpha)
    n_dot_h2     = sqr(n_dot_h)
    inv_n_dot_h4 = 1.0 / sqr(n_dot_h2)
    t2           = sqr_cos_to_sqr_tan(n_dot_h2)
    
    return inv_alpha2 * inv_n_dot_h4 * np.exp(-t2 * inv_alpha2) / np.pi

def D_WardDuer(n_dot_h, alpha):
    #         1        [  n_dot_h^2 - 1  ]        1        [tan(theta_h)]^2
    # D:= ---------- e^[-----------------] = ---------- e^-[------------]
    #     pi alpha^2   [n_dot_h^2 alpha^2]   pi alpha^2    [   alpha    ]

    inv_alpha2   = 1.0 / sqr(alpha)
    n_dot_h2     = sqr(n_dot_h)
    t2           = sqr_cos_to_sqr_tan(n_dot_h2)
    
    return inv_alpha2 * np.exp(-t2 * inv_alpha2) / np.pi

def D_BlinnPhong(n_dot_h, alpha):
    #         1              [   2       ]   Ns + 2
    # D:= ---------- n_dot_h^[------- - 2] = ------ n_dot_h^Ns
    #     pi alpha^2         [alpha^2    ]    pi 2
    
    inv_alpha2 = 1.0 / sqr(alpha)
    Ns         = 2.0 * inv_alpha2 - 2.0
    
    return inv_alpha2 * np.power(n_dot_h, Ns) / np.pi

def D_TrowbridgeReitz(n_dot_h, alpha):
    #                  alpha^2                                      c
    # D:= ---------------------------------- = ---------------------------------------------
    #     pi (n_dot_h^2 (alpha^2 - 1) + 1)^2   (alpha^2 * cos(theta_h)^2 + sin(theta_h)^2)^2
    
    alpha2   = sqr(alpha)
    n_dot_h2 = sqr(n_dot_h)
    temp1    = n_dot_h2 * (alpha2 - 1.0) + 1.0
    
    return alpha2 / (np.pi * sqr(temp1))

def D_GGX(n_dot_h, alpha):
    return D_TrowbridgeReitz(n_dot_h, alpha)

def D_GTR2(n_dot_h, alpha):
    return D_TrowbridgeReitz(n_dot_h, alpha)

def D_Berry(n_dot_h, alpha):
    #                      alpha^2 - 1                                          c
    # D:= --------------------------------------------- = -------------------------------------------
    #     log(alpha^2) pi (n_dot_h^2 (alpha^2 - 1) + 1)   (alpha^2 * cos(theta_h)^2 + sin(theta_h)^2)
    
    alpha2   = sqr(alpha)
    n_dot_h2 = sqr(n_dot_h)
    temp1    = n_dot_h2 * (alpha2 - 1.0) + 1.0
    
    if alpha >= 1.0:
        return 1.0 / np.pi
    else:
        return (alpha2 - 1.0) / (np.pi * np.log(alpha2) * temp1)

def D_GTR1(n_dot_h, alpha):
    return D_Berry(n_dot_h, alpha)

###############################################################################
# Partial Geometric Schadowing
###############################################################################

def G1_GGX(n_dot_vl, alpha):
    #                          2 n_dot_vl                                              2
    # G1 := --------------------------------------------------- = --------------------------------------------
    #       n_dot_vl + sqrt(alpha^2 + (1 - alpha^2) n_dot_vl^2)   1 + sqrt((alpha/n_dot_vl)^2 + (1 - alpha^2))
    
    alpha2    = sqr(alpha)
    n_dot_vl2 = sqr(n_dot_vl)

    return 2.0 * n_dot_vl / (n_dot_vl * sqrt(alpha2 + (1.0 - alpha2) * n_dot_vl2))

def G1_SchlickGGX(n_dot_vl, alpha):
    #             n_dot_vl                      n_dot_vl
    # G1 := --------------------- = --------------------------------
    #       n_dot_vl (1 - k) + k    n_dot_vl (1 - alpha/2) + alpha/2
    
    k = 0.5 * alpha
    
    return n_dot_vl / (n_dot_vl * (1.0 - k) + k)

def G1_Beckmann(n_dot_vl, alpha):
    #                n_dot_vl
    # c  := --------------------------
    #       alpha sqrt(1 - n_dot_vl^2)
    #
    #         3.535 c + 2.181 c^2
    # G1 := ----------------------- (if c < 1.6) | 1 (otherwise)
    #       1 + 2.276 c + 2.577 c^2
    
    n_dot_vl2 = sqr(n_dot_vl)
    c         = n_dot_vl2 / (alpha * sqrt(1.0 - n_dot_vl2))
    c2        = sqr(c)
    
    if c < 1.6:
        return (3.535 * c + 2.8181 * c2) / (1.0 + 2.276 * c + 2.577 * c2)
    else: 
        return 1.0

def G1_SchlickBeckmann(n_dot_vl, alpha):
    #             n_dot_vl                               n_dot_vl
    # G1 := --------------------- = --------------------------------------------------
    #       n_dot_vl (1 - k) + k    n_dot_vl (1 - alpha sqrt(2/pi)) + alpha sqrt(2/pi)
    
    k = alpha / np.pi
    
    return n_dot_vl / (n_dot_vl * (1.0 - k) + k)

###############################################################################
# Geometric Schadowing
###############################################################################

def G_Implicit(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    # G := n_dot_v n_dot_l
    
    return n_dot_v * n_dot_l

def G_Ward(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    # G := 1
    
    return 1.0

def G_Neumann(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    #         n_dot_v n_dot_l
    # G := ---------------------
    #      max(n_dot_v, n_dot_l)
    
    return (n_dot_v * n_dot_l) / np.maximum(n_dot_v, n_dot_l)

def G_AshikhminPremoze(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    #                n_dot_v n_dot_l
    # G := -----------------------------------
    #      n_dot_v + n_dot_l - n_dot_v n_dot_l
    
    return (n_dot_v * n_dot_l) / (n_dot_v + n_dot_l - n_dot_v * n_dot_l)

def G_Kelemann(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    #      n_dot_v n_dot_l
    # G := ---------------
    #          v_dot_h
    
    return (n_dot_v * n_dot_l) / v_dot_h

def G_CookTorrance(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    #         [   2 n_dot_h n_dot_v  2 n_dot_h n_dot_l]
    # G := min[1, -----------------, -----------------]
    #         [        v_dot_h           v_dot_h      ]
    
    return np.minimum(1.0, 2.0 * (n_dot_h / v_dot_h) * np.minimum(n_dot_v, n_dot_l))

def G_GGX(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    #                                           2 (n_dot_l) (n_dot_v)
    # G := -------------------------------------------------------------------------------------------------
    #      n_dot_v sqrt(alpha^2 + (1 - alpha^2) n_dot_l^2) + n_dot_l sqrt(alpha^2 + (1 - alpha^2) n_dot_v^2)
    #
    #                1
    #    = -----------------------
    #      1 + Lambda_v + lambda_l
    #
    #            sqrt(alpha^2 + (1 - alpha^2) (n_dot_v)^2)   1
    # Lambda_v = ----------------------------------------- - -
    #                           2 n_dot_v                    2
    
    alpha2   = sqr(alpha)
    lambda_v = sqrt(alpha2 + (1.0 - alpha2) * sqr(n_dot_v))
    lambda_l = sqrt(alpha2 + (1.0 - alpha2) * sqr(n_dot_l))
    
    return (2.0 * n_dot_l * n_dot_v) / (n_dot_v * lambda_l + n_dot_l * lambda_v)

def G_Smith_GGX(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    return G1_GGX(n_dot_v, alpha) * G1_GGX(n_dot_l, alpha)

def G_Smith_SchlickGGX(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    return G1_SchlickGGX(n_dot_v, alpha) * G1_SchlickGGX(n_dot_l, alpha)

def G_Smith_Beckmann(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    return G1_Beckmann(n_dot_v, alpha) * G1_Beckmann(n_dot_l, alpha)

def G_Smith_SchlickBeckmann(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    return G1_SchlickBeckmann(n_dot_v, alpha) * G1_SchlickBeckmann(n_dot_l, alpha)

###############################################################################
# Partial Visibility
###############################################################################

#          G1
# V1 := --------
#       n_dot_vl

def V1_GGX(n_dot_vl, alpha):
    #                               2                       
    # V1 := ---------------------------------------------------
    #       n_dot_vl + sqrt(alpha^2 + (1 - alpha^2) n_dot_vl^2)
    
    alpha2    = sqr(alpha)
    n_dot_vl2 = sqr(n_dot_vl)
    
    return 2.0 / (n_dot_vl * sqrt(alpha2 + (1.0 - alpha2) * n_dot_vl2))

def V1_SchlickGGX(n_dot_vl, alpha):
    #                 1                            1
    # V1 := --------------------- = --------------------------------
    #       n_dot_vl (1 - k) + k    n_dot_vl (1 - alpha/2) + alpha/2
    
    k = 0.5 * alpha
    
    return 1.0 / (n_dot_vl * (1.0 - k) + k)

def V1_SchlickBeckmann(n_dot_vl, alpha):
    #                1                                     1
    # V1 := --------------------- = --------------------------------------------------
    #       n_dot_vl (1 - k) + k    n_dot_vl (1 - alpha sqrt(2/pi)) + alpha sqrt(2/pi)
    	
    k = alpha / np.pi
    
    return 1.0 / (n_dot_vl * (1.0 - k) + k)

###############################################################################
# Visibility
###############################################################################

#            G
# V := ---------------
#      n_dot_v n_dot_l

def V_Implicit(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    # V := 1
    
    return 1.0

def V_Ward(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    #             1
    # V := ---------------
    #      n_dot_v n_dot_l
    
    return 1.0 / (n_dot_v * n_dot_l)

def V_Neumann(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    #               1
    # V := ---------------------
    #      max(n_dot_v, n_dot_l)
    
    return 1.0 / np.maximum(n_dot_v, n_dot_l)

def V_AshikhminPremoze(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    #                      1
    # V := -----------------------------------
    #      n_dot_v + n_dot_l - n_dot_v n_dot_l
    
    return 1.0 / (n_dot_v + n_dot_l - n_dot_v * n_dot_l)

def V_Kelemann(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    #         1
    # V := -------
    #      v_dot_h
    
    	return 1.0 / v_dot_h

def V_CookTorrance(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    #         [       1            2 n_dot_h        2 n_dot_h   ]
    # V := min[---------------, ---------------, ---------------]
    #         [n_dot_v n_dot_l  v_dot_h n_dot_l  v_dot_h n_dot_v]
    
    v_ward    = 1.0 / (n_dot_v * n_dot_l)
    v_neumann = 1.0 / np.maximum(n_dot_v, n_dot_l)
    
    return np.minimum(v_ward, 2.0 * (n_dot_h / v_dot_h) * v_neumann)

def V_GGX(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    #                                                      2
    # V := -------------------------------------------------------------------------------------------------
    #      n_dot_v sqrt(alpha^2 + (1 - alpha^2) n_dot_l^2) + n_dot_l sqrt(alpha^2 + (1 - alpha^2) n_dot_v^2)
    
    alpha2   = sqr(alpha)
    lambda_v = sqrt(alpha2 + (1.0 - alpha2) * sqr(n_dot_v))
    lambda_l = sqrt(alpha2 + (1.0 - alpha2) * sqr(n_dot_l))
    
    return 2.0 / (n_dot_v * lambda_l + n_dot_l * lambda_v)

def V_Smith_GGX(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    return V1_GGX(n_dot_v, alpha) * V1_GGX(n_dot_l, alpha)

def V_Smith_SchlickGGX(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    return V1_SchlickGGX(n_dot_v, alpha) * V1_SchlickGGX(n_dot_l, alpha)

def V_Smith_Beckmann(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    return G_Smith_Beckmann(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha) / (n_dot_v * n_dot_l)

def V_Smith_SchlickBeckmann(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha):
    return V1_SchlickBeckmann(n_dot_v, alpha) * V1_SchlickBeckmann(n_dot_l, alpha)

###############################################################################
# Fresnel
###############################################################################

def F_None(v_dot_h, F0):
    # F := F0
    
    return F0

def F_Schlick(v_dot_h, F0, F90=1.0):
    # F := F0 + (F90 - F0) (1 - v_dot_h)^5
    
    return lerp(F0, F90, np.power((1.0 - v_dot_h), 5.0))

def F_CookTorrance(v_dot_h, F0):
    # c   := v_dot_h
    #
    #        1 + sqrt(F0)
    # eta := ------------
    #        1 - sqrt(F0)
    #
    # g   := sqrt(eta^2 + c^2 - 1)
    #
    #        1 [g - c]^2 [    [(g + c) c - 1]^2]
    # F   := - [-----]   [1 + [-------------]  ]
    #        2 [g + c]   [    [(g - c) c + 1]  ]
    
    sqrt_F0  = sqrt(F0)
    eta      = (1.0 + sqrt_F0) / (1.0 - sqrt_F0)
    g        = sqrt(sqr(eta) + sqr(v_dot_h) - 1.0)
    g1       = g + v_dot_h
    g2       = g - v_dot_h
    
    return 0.5 * sqr(g2 / g1) * (1.0 + sqr((g1 * v_dot_h - 1.0) / (g2 * v_dot_h + 1.0)))

###############################################################################
# Material
###############################################################################

class Material:
    
    def __init__(self, roughness=1.0, F0=g_dielectric_F0):
        self.roughness = roughness
        self.F0        = F0  

###############################################################################
# BRDF
###############################################################################

def brdf_blinn_phong(n, l, v, material):
    brdf = construct_brdf(brdf_D=D_BlinnPhong, brdf_V=V_Implicit, brdf_F=F_None)
    return brdf(n=n, l=l, v=v, material=material)
def brdf_cook_torrance(n, l, v, material):
    brdf = construct_brdf(brdf_D=D_GGX, brdf_V=V_GGX, brdf_F=F_Schlick)
    return brdf(n=n, l=l, v=v, material=material)
def brdf_ward_duer(n, l, v, material):
    brdf = construct_brdf(brdf_D=D_WardDuer, brdf_V=V_Ward, brdf_F=F_None)
    return brdf(n=n, l=l, v=v, material=material)

def construct_brdf(brdf_D, brdf_V, brdf_F):
    def brdf(n, l, v, material):
        alpha         = np.maximum(1e-1, sqr(material.roughness))
        n_dot_l       = sat_dot(n, l) + 1e-5
        n_dot_v       = sat_dot(n, v) + 1e-5
        h             = half_direction(l, v)
        n_dot_h       = sat_dot(n, h) + 1e-5
        v_dot_h       = sat_dot(v, h) + 1e-5
    
        D             = brdf_D(n_dot_h, alpha)
        V             = brdf_V(n_dot_v, n_dot_l, n_dot_h, v_dot_h, alpha)
        F_specular    = brdf_F(v_dot_h, material.F0)
        
        return F_specular * 0.25 * D * V
    
    return brdf