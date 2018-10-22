# -*- coding: utf-8 -*-
import numpy as np
from math_utils import normalize, copysign

# Computes an orthonormal basis from a given unit vector with the method of
# Hughes and Möller.
def OrthonormalBasis_HughesMoller(n):
    if np.abs(n[0]) > np.abs(n[2]):
        u = np.array([-n[1], n[0], 0.0])
    else:
        u = np.array([0.0, -n[2], n[1]])
    b2 = normalize(u)
    b1 = np.cross(b2, n)
    return np.array([b1, b2, n])

# Computes an orthonormal basis from a given unit vector with the method of
# Frisvad.
def OrthonormalBasis_Frisvad(n):
    if (n[2] < -0.9999999):
        b1 = np.array([ 0.0, -1.0, 0.0])
        b2 = np.array([-1.0,  0.0, 0.0])
        return (n, b1, b2)
    
    a = 1.0 / (1.0 + n[2])
    b = -n[0] * n[1] * a
    b1 = np.array([1.0 - n[0] * n[0] * a, b, -n[0]])
    b2 = np.array([b, 1.0 - n[1] * n[1] * a, -n[1]])
    return np.array([b1, b2, n])

# Computes an orthonormal basis from a given unit vector with the method of
# Duff, Burgess, Christensen, Hery, Kensler, Liani and Villemin.
def OrthonormalBasis_Duff(n):
    s = copysign(1.0, n[2])
    a = -1.0 / (s + n[2])
    b = n[0] * n[1] * a
    b1 = np.array([1.0 + s * n[0] * n[0] * a, s * b, -s * n[0]])
    b2 = np.array([b, s + n[1] * n[1] * a, -n[1]])
    return np.array([b1, b2, n])

# Computes an orthonormal basis from a given unit vector.
def OrthonormalBasis(n):
    return OrthonormalBasis_Duff(n)
