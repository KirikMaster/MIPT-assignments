from math import *
import sympy as sym
import numpy as np

def f(x):
    return exp(-x*x) * cos(2*x)

a = (cos(300) + 1)/100
b = -3*cos(300)/100 + sin(300)/10000
c2 = 0.0002499566635
x2 = 2.3553925232142
c1 = a - c2
x1 = (b - c2*x2) / c1
integral = (c1*f(x1) + c2*f(x2))
print("I = ", integral)

h = 2.77e-6
integral2 = 0
X = np.arange(0, 3, h)
for i in X: integral2 += f(i) * sin(100*i)
integral2 -= (f(3) * sin(300)) / 2
integral2 *= 3 / len(X)
print("I2 = ", integral2)