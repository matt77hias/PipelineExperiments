from math_utils import frac
import numpy as np

g_rgb_to_xyz      = np.array([[0.497, 0.339, 0.164], \
                              [0.256, 0.678, 0.066], \
                              [0.023, 0.113, 0.864]])
g_xyz_to_xyd      = np.array([[1.000, 0.000, 1.000], \
                              [0.000, 1.000, 15.00], \
                              [0.000, 0.000, 3.000]])
g_xy_xyz_to_x1yd1 = np.array([[  4/9, 0.000, 0.000],
                              [0.000, 1.000, 0.000],
                              [0.000, 0.000, 0.62/9]])
g_rgb_to_x1yd1    = np.dot(np.dot(g_rgb_to_xyz, g_xyz_to_xyd), g_xy_xyz_to_x1yd1)

g_x1yd1_to_rbg    = np.linalg.inv(g_rgb_to_x1yd1)

def RGBtoLogLuv(rgb):
    x1yd1  = np.maximum(np.dot(rgb, g_rgb_to_x1yd1), 1e-6)
    uv     = x1yd1[:2] / x1yd1[2]
    L      = 2.0 * np.log2(x1yd1[1]) + 127.0
    L_low  = frac(L)
    L_high = (L - np.floor(L_low * 255.0) / 255.0) / 255.0
    logluv =  np.array([L_high, L_low, uv[0], uv[1]])
    
    return logluv
      
def LogLuvToRGB(logluv):
    L_high   = logluv[0]
    L_low    = logluv[1]
    L        = 255.0 * L_high + L_low
    x1yd1    = np.zeros(3)
    x1yd1[1] = np.power(2.0, (L - 127.0) * 0.5)
    uv       = logluv[2:]
    x1yd1[2] = x1yd1[1] / uv[1]
    x1yd1[0] = uv[0] * x1yd1[2]
    rgb      = np.maximum(np.dot(x1yd1, g_x1yd1_to_rbg), 0.0)
    
    return rgb
    
