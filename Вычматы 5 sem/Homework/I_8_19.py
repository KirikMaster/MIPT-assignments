from math import *
import numpy as np

def sinMac1(t, n):
    ret = 0
    k = 0
    for i in range(n):
        if k == 1:
            ret += t**i / factorial(i)
        elif k == 3:
            ret -= t**i / factorial(i)
        k = (k + 1) % 4 
    return ret

def sinMac2(t, n):
    ret = 0
    k = 0
    for i in range(n):
        if k == 0:
            ret += sin(10) * (t-10)**i / factorial(i)
        elif k == 1:
            ret += cos(10) * (t-10)**i / factorial(i)
        elif k == 2:
            ret -= sin(10) * (t-10)**i / factorial(i)
        elif k == 3:
            ret -= cos(10) * (t-10)**i / factorial(i)
        k = (k + 1) % 4 
    return ret

def expMac1(t, n):
    ret = 0
    for i in range(n):
        ret += t**i / factorial(i)
    return ret

def expMac2(t, n):
    ret = 0
    for i in range(n):
        ret += exp(10) * (t-10)**i / factorial(i)
    return ret

dt = 1e-3
# t = [0, 1]
T = np.arange(0, 1, dt)
n = 1
delta_f = np.vectorize(sinMac1)(T, n) - np.vectorize(sin)(T)
delta_f = np.vectorize(abs)(delta_f)
while np.max(delta_f) >= dt:
    n += 1
    delta_f = np.vectorize(sinMac1)(T, n) - np.vectorize(sin)(T)
    delta_f = np.vectorize(abs)(delta_f)
print("For sin(t) on [0, 1] n = ", n)

n = 1
delta_f = np.vectorize(expMac1)(T, n) - np.vectorize(exp)(T)
delta_f = np.vectorize(abs)(delta_f)
while np.max(delta_f) >= dt:
    n += 1
    delta_f = np.vectorize(expMac1)(T, n) - np.vectorize(exp)(T)
    delta_f = np.vectorize(abs)(delta_f)
print("For exp(t) on [0, 1] n = ", n)

# t = [10, 11]
T = np.arange(10, 11, dt)
n = 1
delta_f = np.vectorize(sinMac1)(T, n) - np.vectorize(sin)(T)
delta_f = np.vectorize(abs)(delta_f)
while np.max(delta_f) >= dt:
    n += 1
    delta_f = np.vectorize(sinMac1)(T, n) - np.vectorize(sin)(T)
    delta_f = np.vectorize(abs)(delta_f)
print("For sin(t) by MacLorren on [10, 11] n = ", n)

n = 1
delta_f = np.vectorize(sinMac2)(T, n) - np.vectorize(sin)(T)
delta_f = np.vectorize(abs)(delta_f)
while np.max(delta_f) >= dt:
    n += 1
    delta_f = np.vectorize(sinMac2)(T, n) - np.vectorize(sin)(T)
    delta_f = np.vectorize(abs)(delta_f)
print("For sin(t) by Taylor on [10, 11] n = ", n)

n = 1
delta_f = np.vectorize(expMac1)(T, n) - np.vectorize(exp)(T)
delta_f = np.vectorize(abs)(delta_f)
while np.max(delta_f) >= dt:
    n += 1
    delta_f = np.vectorize(expMac1)(T, n) - np.vectorize(exp)(T)
    delta_f = np.vectorize(abs)(delta_f)
print("For exp(t) by MacLorren on [10, 11] n = ", n)

n = 1
delta_f = np.vectorize(expMac2)(T, n) - np.vectorize(exp)(T)
delta_f = np.vectorize(abs)(delta_f)
while np.max(delta_f) >= dt:
    n += 1
    delta_f = np.vectorize(expMac2)(T, n) - np.vectorize(exp)(T)
    delta_f = np.vectorize(abs)(delta_f)
print("For exp(t) by Taylor on [10, 11] n = ", n)