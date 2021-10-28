from math import pi, e, atan
import numpy as np

def abs(x):
    return (x ** 2) ** (0.5)

def norm_vector(X):
    l = np.shape(X)
    max_el = 0
    for i in X:
        if abs(i) > max_el: max_el = abs(i)
    return max_el

def norm_matix(X):
    (x, y) = np.shape(X)
    max_el = 0
    for i in range(y):
        sumj = 0
        for j in range(x):
            sumj += abs(X[i, j])
        if sumj > max_el: max_el = sumj
    return max_el

def norm(X):
    if X.ndim == 1: return norm_vector(X)
    elif X.ndim == 2: return norm_matix(X)
    else: return 0

N = int(input())
delta = float(input())
#delta = 1e-3
A = [[0 for i in range(N)] for i in range(N)]
A[0][0] = 1
A[1][1] = 1
c = atan(1.)
b = 1
a = -5 * e
d = pi
alpha = d / (c + b + a)
for i in range(2, N):
    A[i][i-2] = c
    A[i][i-1] = b
    A[i][i] = a
A = np.array(A)
print(A)
b = d * np.ones(N)
b[0], b[1] = alpha, alpha
print(b)
db = np.zeros(N)
db[0] = delta
#print(db)
#print(norm(b))
#print(norm(A))
A_1 = np.linalg.inv(A)
print(A_1)
print("||Δx|| <= ", norm(A_1) * norm(db))