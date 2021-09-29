import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def locate(x_0):
    for i in range(N-1):
        if x[i] <= x_0 < x[i+1]:
            return i
            break
    return N - 1

def spline(x_0):
    i = locate(x_0)
    return a[i] + b[i] * (x_0 - x[i]) + c[i] * (x_0 - x[i])**2 + d[i] * (x_0 - x[i])**3

data = pd.read_csv("Вычматы 5 sem\Contest_1\Atmosphere_1.csv")
N = data.shape[0] - 1 #Количество сплайнов
h = [data.loc[i + 1, "H, км"] - data.loc[i, "H, км"] for i in range(N)]
x = [data.loc[i, "H, км"] for i in range(N)]
u = [data.loc[i, "DEN, кг/м3"] for i in range(N + 1)]
a = [u[i] for i in range(N + 1)]
f_1 = [(u[i + 1] - u[i]) / h[i] for i in range(N)]
f_2 = [(f_1[i + 1] - f_1[i]) / (h[i + 1] + h[i]) for i in range(N - 1)]
print(len(u), len(f_1), len(f_2))
A = np.zeros((N-1, N-1))
for i in range(1, N-2):
    A[i, i] = 2
    A[i, i+1] = h[i] / (h[i-1] + h[i])
    A[i, i-1] = h[i-1] / (h[i-1] + h[i])
A[0, 0], A[N-2, N-2] = 2, 2
A[0, 1] = h[1]/(h[0] + h[0])
A[N-2, N-3] = h[N-2]/(h[N-2] + h[N-1])
g = np.array(f_2) * 6
#print(g)
#print(g.size, A.shape)
c_0 = np.linalg.solve(A, g)
p = np.zeros(N-1)
q = np.zeros(N-1)
p[0] = -A[0, 1] / A[0, 0]
q[0] = g[0] / A[0, 0]
for i in range(1, N-2):
    p[i] = -A[i, i+1] / (A[i, i-1] * p[i-1] + A[i, i])
    q[i] = (g[i] - A[i, i-1] * q[i-1]) / (A[i, i-1] * p[i-1] + A[i, i])
c = np.ones(N-1)
c[-1] = (g[-1] - A[-1, -2] * q[-2]) / (p[-2] * A[-1, -2] + A[-1, -1])
for i in range(N-3, -1, -1):
    c[i] = c[i+1] * p[i] + q[i]
c = np.append(c, 0)
b = np.ones(N)
b[0] = c[0] * h[0] / 3 + f_1[0]
for i in range(1, N):
    b[i] = c[i] * h[i] / 3 + c[i-1] * h[i] / 6 + f_1[i]
d = np.ones(N)
d[0] = c[0] / h[0]
for i in range(1, N):
    d[i] = (c[i] - c[i-1]) / h[i]

dx = h[0] / 10
X = np.arange(x[0], x[N-1], dx)
#Y = np.zeros()
Y = np.vectorize(spline)(X)
plt.plot(X, Y)
plt.show()

print("c = ", c)
#print("c_0 = ", c_0)
print("TOTAL SPLINES ", N)
print("TOTAL ELEMENTS ", N + 1)
print(A)
print("-------")
print(data)
#print(data.loc[1, "DEN, кг/м3"])