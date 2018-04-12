# -*- coding: utf-8 -*-
import numpy as np

# Copies the sign of the second argument to the first argument (sign(0.0) = +).
def copysign(v, x):
    return v if x >= 0.0 else -v

# Returns the (positive) fractional part of the given value.
def frac(x):
    return np.abs(np.modf(x)[0])

# Normalizes the given vector.
def normalize(v):
    norm = np.linalg.norm(v)
    return v if norm == 0.0 else v/norm
   
# Clamps the given value between zero and one.
def saturate(x):
    return np.clip(x, 0.0, 1.0)