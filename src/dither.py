import numpy as np
import matplotlib.pyplot as plt

def get_uv_matrix(resolution):
    width, height = resolution
    xs = np.linspace(0.0, 1.0, width,  dtype=np.float32)
    ys = np.linspace(0.0, 1.0, height, dtype=np.float32)
    return np.meshgrid(xs, ys)

def frac(x):
    return np.abs(np.modf(x)[0])

def n0(x, y):
    return frac(np.sin((x + y) * 199.0) * 123.0)
def n1(x, y):
    return frac(np.sin(52.9755442*x*x + 89.83275744*y*y + 72.75451659*x*y + 54.57512357*x + 13.9757542*y) * 154.577572)




g_gelfond           = 23.1406926327792690
g_gelfond_schneider =  2.6651441426902251

def noise1(x, y):
    return x * g_gelfond + y * g_gelfond_schneider
def noise2(x, y):
   return 256.0 + noise1(x, y)
def noise3(x, y): 
    return np.mod(123456789.0, noise2(x, y))
def noise4(x, y): 
    return np.cos(noise3(x, y))

def noise5(x, y): 
    return frac( np.cos(np.mod( 1234.0, 1024.0 * noise1(x, y))))
def noise6(x, y): 
    return frac( np.cos(np.mod( 12345.0, 1024.0 * noise1(x, y))))
def noise7(x, y): 
    return frac( np.cos(np.mod( 123456.0, 1024.0 * noise1(x, y))))
def noise8(x, y): 
    return frac( np.cos(np.mod( 1234567.0, 1024.0 * noise1(x, y))))
def noise9(x, y): 
    return frac( np.cos(np.mod( 12345678.0, 1024.0 * noise1(x, y))))
def noise10(x, y): 
    return frac( np.cos(np.mod( 123456780.0, 1024.0 * noise1(x, y))))

def dither(resolution=(1200,720), f_noise=noise10):
    xs, ys = get_uv_matrix(resolution)
    data = np.round(f_noise(xs, ys))

    plt.imshow(data, interpolation='none', cmap='Greys')
    plt.show()