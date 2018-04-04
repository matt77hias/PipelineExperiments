import numpy as np
import matplotlib.pyplot as plt

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

def frac(x):
    return np.abs(np.modf(x)[0])

g_gelfond           = 23.1406926327792690
g_gelfond_schneider =  2.6651441426902251

def noise1(x, y):
    return frac(x * g_gelfond + y * g_gelfond_schneider)
def noise2(x, y):
   return frac(256.0 + noise1(x, y))
def noise3(x, y): 
    return frac(np.mod(123456789.0, noise2(x, y)))
def noise4(x, y): 
    return np.abs(np.cos(noise3(x, y)))

def noise5(x, y): 
    return np.abs(np.cos(np.mod(1234.0, 1e-7 + 1024.0 * noise1(x, y))))
def noise6(x, y): 
    return np.abs(np.cos(np.mod(12345.0, 1e-7 + 1024.0 * noise1(x, y))))
def noise7(x, y): 
    return np.abs(np.cos(np.mod(123456.0, 1e-7 + 1024.0 * noise1(x, y))))
def noise8(x, y): 
    return np.abs(np.cos(np.mod(1234567.0, 1e-7 + 1024.0 * noise1(x, y))))
def noise9(x, y): 
    return np.abs(np.cos(np.mod(12345678.0, 1e-7 + 1024.0 * noise1(x, y))))
def noise10(x, y): 
    return np.abs(np.cos(np.mod(123456780.0, 1e-7 + 1024.0 * noise1(x, y))))

def noise11(x, y): 
    return frac(2**14 * np.cos(np.mod(123456780.0, 1e-7 + 1023.0 * noise1(x, y))))
def noise12(x, y): 
    return frac(2**15 * np.mod(np.mod(123456780.0, 1e-7 + 1023.0 * noise1(x, y)), 2.0 * np.pi))
def noise13(x, y):
    return np.abs(np.sin(2.0 * (x * 12.9898 + y * 78.233)) * 43758.5453)

def hash_wang(x):
    a = np.uint32(x)
    a = (a ^ np.uint32(61)) ^ (a >> np.uint32(16))
    a = a + (a << np.uint32(3))
    a = a ^ (a >> np.uint32(4))
    a = a * np.uint32(0x27d4eb2d)
    a = a ^ (a >> np.uint32(15))
    return a

def rng1(seed):
    urand = hash_wang(seed + 13)
    mantissa_mask = np.uint32(0xffffffff) >> np.uint32(32-23)
    return frac(np.float32(urand & mantissa_mask) / np.float32(mantissa_mask))

def dither(resolution=(1200,720), f_noise=noise11):
    xs, ys = get_uv_matrix(resolution)
    data = f_noise(xs, ys)

    plt.imshow(data, interpolation='none', cmap='Greys')
    plt.show()
    plt.hist(data.flatten(), 128)
    plt.show()

def dither2(resolution=(1200,720), f_rng=rng1):
    xs, ys = get_ss_matrix(resolution)
    data = f_rng(xs * resolution[1] + ys)

    plt.imshow(data, interpolation='none', cmap='Greys')
    plt.show()
    plt.hist(data.flatten(), 128)
    plt.show()