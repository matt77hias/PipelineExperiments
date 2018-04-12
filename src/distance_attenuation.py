# -*- coding: utf-8 -*-
from math_utils import saturate
import matplotlib.pyplot as plt
import numpy as np

###############################################################################
# Distance Attenuation
###############################################################################

def fref(rs):
    return 1.0/(rs**2)
    
def f0(rs):
    return 1.0/np.maximum(0.01**2, rs**2)
    
def f1(rs, R):
    return np.maximum(0.0, 1.0/(rs**2) - 1.0/(R**2))

def f2(rs, R, a=0.01):
    return np.maximum(0.0, 1.0/(rs**2+a**2) - 1.0/(R**2+a**2))
    
def f3(rs, R):
    return f0(rs) * saturate(1.0-rs/R)
    
def f4(rs, R):
    threshold = 1.0/(R*R)
    return 1.0/saturate(1.0-threshold) * saturate(f0(rs)-threshold)
    
def f5(rs, R, n=4):
    return f0(rs) * saturate(1.0-rs**n/R**n)**2
    
###############################################################################
# Tests
###############################################################################

def test_0():
    R = 10.0
    rs = np.linspace(0.1, 0.01, 1000)
    
    plt.figure()
    
    plt.plot(rs, f0(rs), label=f0.__name__)
    #plt.plot(rs, f1(rs, R), label=f1.__name__)
    #plt.plot(rs, f2(rs, R), label=f2.__name__)
    #plt.plot(rs, f3(rs, R), label=f3.__name__)
    #plt.plot(rs, f4(rs, R), label=f4.__name__)
    plt.plot(rs, f5(rs, R), label=f5.__name__)
    
    plt.legend()
    
def test_R():
    R = 10.0
    rs = np.linspace(8.0, 12.0, 1000)
    
    plt.figure()
    
    # (-): no finite range
    plt.plot(rs, f0(rs), label=f0.__name__)
    
    # (-): no first order derivative at R
    plt.plot(rs, f1(rs, R), label=f1.__name__)
    #plt.plot(rs, f2(rs, R), label=f2.__name__)
    #plt.plot(rs, f3(rs, R), label=f3.__name__)
    #plt.plot(rs, f4(rs, R), label=f4.__name__)
    
    plt.plot(rs, f5(rs, R), label=f5.__name__)
    
    plt.legend()