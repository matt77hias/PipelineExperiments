# -*- coding: utf-8 -*-
import numpy as np

# Copies the sign of the second argument to the first argument (sign(0.0) = +).
def copysign(v, x):
    return v if x >= 0.0 else -v

# Extracts the (positive) fractional part of the given value.
def frac(x):
    return np.abs(np.modf(x)[0])

# Linear interpolates between the first two given values using the third given 
# value as weight.
def lerp(x1, x2, a):
    return x1 + a * (x2 - x1)
	
# Normalizes the given vector.
def normalize(v):
    norm = np.linalg.norm(v)
    return v if norm == 0.0 else v/norm
   
# Clamps the dot product of the given vectors between zero and one.
def sat_dot(v1, v2):
    return saturate(v1.dot(v2))	
   
# Clamps the given value between zero and one.
def saturate(x):
    return np.clip(x, 0.0, 1.0)

# Computes the square of the given value.
def sqr(x):
    return x * x

# Computes the square root of the given value.
def sqrt(x):
    return np.sqrt(x)

# Computes the cosine of the given sine.
def cos_to_sin(c):
    return sqrt(1.0 - sqr(c))

# Computes the sine of the given cosine.
def sin_to_cos(s):
    return sqrt(1.0 - sqr(s))

# Computes the squared tangent of the given cosine.
def sqr_cos_to_sqr_tan(sqr_c):
    return (1.0 - sqr_c) / sqr_c

# Computes the squared tangent of the given sine.
def sqr_sin_to_sqr_tan(sqr_s):
    return sqr_s / (1.0 - sqr_s)

# Computes the perfect specular direction of the second given vector about the 
# first given vector.
def reflected_direction(n, l):
    # r := 2 * n_dot_l * n - l
    return 2.0 * n.dot(l) * n - l

# Computes the half direction of the given vectors.
def half_direction(d1, d2):
    # h := d1+d2 / ||d1+d2||
    return normalize(d1 + d2)
