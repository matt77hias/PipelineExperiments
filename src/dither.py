# -*- coding: utf-8 -*-
from math_utils import frac
import matplotlib.pyplot as plt
import numpy as np

def get_ss_matrix(resolution):
    width, height = resolution
    xs = np.arange(0, width,  dtype=np.uint32)
    ys = np.arange(0, height, dtype=np.uint32)
    return np.meshgrid(xs, ys)

def get_uv_matrix(resolution):
    width, height = resolution
    xs = np.linspace(0.0, 1.0, width,  dtype=np.float32)
    ys = np.linspace(0.0, 1.0, height, dtype=np.float32)
    return np.meshgrid(xs, ys)

###############################################################################
# Noise, Hash and RNGs
###############################################################################

g_gelfond           = 23.1406926327792690
g_gelfond_schneider =  2.6651441426902251

def gelford_f(x, y):
    return x*g_gelfond + y*g_gelfond_schneider

def noise1(x, y):
    return frac(gelford_f(x, y))
def noise2(x, y):
    return frac(256.0 + gelford_f(x, y))
def noise3(x, y):
    return frac(np.mod(123456789.0, 1e-7 + gelford_f(x, y)))
def noise4(x, y):
    return np.abs(np.cos(gelford_f(x, y)))

def noise5(x, y):
    return np.abs(np.cos(np.mod(1234.0, 1e-7 + 1024.0 * gelford_f(x, y))))
def noise6(x, y):
    return np.abs(np.cos(np.mod(12345.0, 1e-7 + 1024.0 * gelford_f(x, y))))
def noise7(x, y):
    return np.abs(np.cos(np.mod(123456.0, 1e-7 + 1024.0 * gelford_f(x, y))))
def noise8(x, y):
    return np.abs(np.cos(np.mod(1234567.0, 1e-7 + 1024.0 * gelford_f(x, y))))
def noise9(x, y):
    return np.abs(np.cos(np.mod(12345678.0, 1e-7 + 1024.0 * gelford_f(x, y))))
def noise10(x, y):
    return np.abs(np.cos(np.mod(123456780.0, 1e-7 + 1024.0 * gelford_f(x, y))))

def noise11(x, y):
    return frac(2**14 * np.cos(np.mod(123456780.0, 1e-7 + 1023.0 * gelford_f(x, y))))
def noise12(x, y):
    return frac(2**15 * np.mod(np.mod(123456780.0, 1e-7 + 1023.0 * gelford_f(x, y)), 2.0 * np.pi))

def hash_wang(x):
    a = np.uint32(x)
    a = (a ^ np.uint32(61)) ^ (a >> np.uint32(16))
    a = a + (a << np.uint32(3))
    a = a ^ (a >> np.uint32(4))
    a = a * np.uint32(0x27d4eb2d)
    a = a ^ (a >> np.uint32(15))
    return a

def rng1(seed):
    urand = hash_wang(seed)
    mantissa_mask = np.uint32(0xffffffff) >> np.uint32(32-23)
    return frac(np.float32(urand & mantissa_mask) / np.float32(mantissa_mask))

###############################################################################
# Tests
###############################################################################

def dither(resolution=(1200,720), f=noise11, normalized=True):
    if normalized:
        xs, ys = get_uv_matrix(resolution)
        data = f(xs, ys)
    else:
        xs, ys = get_ss_matrix(resolution)
        data = f(xs * resolution[1] + ys)
        
    fig = plt.figure()
    ax  = fig.gca()
    ax.set_aspect('equal')
    ax.set_xlim(0,resolution[0])
    ax.set_ylim(0,resolution[1])
    ax.invert_yaxis()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.imshow(data, cmap='Greys', interpolation='none', origin='upper')
    plt.show()
    
    plt.figure()
    plt.hist(data.flatten(), bins=128)
    plt.show()

def test():
    dither(f=noise11, normalized=True)
    dither(f=rng1,    normalized=False)