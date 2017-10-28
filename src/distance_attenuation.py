import numpy as np
import matplotlib.pyplot as plt

def saturate(x, low=0.0, high=1.0):
    return np.clip(x, low, high)

def fref(rs):
    return np.vectorize(lambda r: 1.0/(r**2))(rs)
    
def f0(rs):
    return np.vectorize(lambda r: 1.0/(max(0.01**2, r**2)))(rs)
    
def f1(rs, R):
    return np.vectorize(lambda r: max(0.0, 1.0/(r**2) - 1.0/(R**2)))(rs)
    
def f2(rs, R, a=0.01):
    return np.vectorize(lambda r: max(0.0, 1.0/(r**2+a**2) - 1.0/(R**2+a**2)))(rs)
    
def f3(rs, R):
    return np.vectorize(lambda r: f0(r) * saturate(1.0 - r/R))(rs)
    
def f4(rs, R):
    threshold = 1.0 / (R*R)
    return np.vectorize(lambda r: 1.0/saturate(1.0 - threshold) * saturate(f0(r) - threshold))(rs)
    
def f5(rs, R, n=4):
    return np.vectorize(lambda r: f0(r) * saturate(1.0 - r**n/R**n)**2)(rs)
    
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