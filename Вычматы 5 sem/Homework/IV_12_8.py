from math import *

def f(x):
    return x * exp(-x**2)

def f_der(x):
    return exp(-x**2) * (1 - 2 * x**2)

def method1(x):
    return h / 2 * exp(x**2)

def method2(x):
    return log(2*x/h) / x

def estimate(x0, q):
    return ceil(abs(log(eps / 2 * f_der(x0) / f(x0)) / log(q)))

h = 1 / sqrt(2*e)
eps = 1e-3
x0 = 1 / sqrt(2)
xn1, xn2 = x0, x0
n1 = estimate(x0, 0.64)
for i in range(n1):
    xn1 = method1(xn1)
n2 = estimate(x0, 0.4)
for i in range(n2):
    xn2 = method2(xn2)

print("x1 = ", xn1)
print("x2 = ", xn2)
print("width = ", xn2 - xn1)