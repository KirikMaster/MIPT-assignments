from math import *
import matplotlib.pyplot as plt
import numpy as np

def f(x, y):
    return x * sqrt(y)

def solve(h, alpha):
    X = np.arange(0, 1, h)
    Y = np.zeros(len(X))
    Y_ = np.zeros(len(X))
    Y_[0] = alpha
    for i in range(len(Y_) - 1):
        Y[i+1] = Y[i] + h * Y_[i] + h**2 * f(X[i], Y[i])
        Y_[i+1] = (Y[i+1] - Y[i]) / h
    return (Y, Y_)

y0 = 0
y1 = 2
alpha = 1
for j in range(10):
    h = 0.01
    (Y, Y_) = solve(h, alpha)
    F = Y[-1] - y1
    (Y1, Y_1) = solve(h, alpha + h)
    F1 = Y1[-1] - y1
    F_ = (F1 - F) / h
    alpha = alpha - F / F_
X = np.arange(0, 1, h)    
plt.plot(X, Y)
plt.show()