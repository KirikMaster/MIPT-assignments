import numpy as np
from math import *

def Jacobian(x, y):
    return np.array([[0, 1/(1+y**2)], [-x/sqrt(1-x**2), 0]])

def Jacobian_1(x, y):
    return 1 / (2*x + 2*y/cos(x)**2) * np.array([[1, -2*y], [1/cos(x)**2, 2*x]])

def F(x, y):
    return np.array([x**2 + y**2 - 1, y - tg(x)])

def phi(x, y, n):
    if n == 1: sig = 1
    else: sig = -1
    return np.array([atan(y), sig*sqrt(1 - x**2)])

x1, y1, x2, y2 = 1/sqrt(2) - 0.01, 1/sqrt(2), -1/sqrt(2) + 0.01, -1/sqrt(2)

Jacob = Jacobian(x1, y1)
q = np.linalg.norm(Jacob, ord = inf)
print("q = ", q)
if q >= 1: 
    print("Not converges")
else:
    for i in range(100):
        un = phi(x1, y1, 1)
        x1, y1 = un[0], un[1]
    print("(x, y) = ", x1, ", ", y1)

Jacob1 = Jacobian(x2, y2)
q1 = np.linalg.norm(Jacob1, ord = inf)
print("q = ", q1)
if q1 >= 1: 
    print("Not converges")
else:
    for i in range(100):
        un1 = phi(x2, y2, 2)
        x2, y2 = un1[0], un1[1]
    print("(x, y) = ", x2, ", ", y2)