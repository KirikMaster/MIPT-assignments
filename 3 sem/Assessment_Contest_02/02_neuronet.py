import numpy as np

A = np.loadtxt(input())
b = np.loadtxt(input())
x = np.array(list(map(float, input().split())))
print(A @ A @ x @ b)