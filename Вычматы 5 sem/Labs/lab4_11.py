
import numpy as np
import matplotlib.pyplot as plt

def locate(x_0):
    for i in range(5):
        if x[i] <= x_0 < x[i+1]:
            return i
            break
    return 5

def spline(x_0):
    i = locate(x_0)
    return a[i] + b[i] * (x_0 - x[i]) + c[i] * (x_0 - x[i])**2 + d[i] * (x_0 - x[i])**3

x = np.array((0.87267, 1.22173, 1.57080, 1.91986, 2.26893, 2.61799))
y = np.array((0.00161, 0.01550, 0.09139, 0.39329, 1.35729, 3.97819))
h = np.array([x[i + 1] - x[i] for i in range(5)])
a, b, c, d = np.copy(y), np.zeros(6), np.zeros(6), np.zeros(6)
f_1 = [(y[i + 1] - y[i]) / h[i] for i in range(5)]
f_2 = [(f_1[i + 1] - f_1[i]) / (h[i + 1] + h[i]) for i in range(4)]
A = np.zeros((5, 5))
