import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    return y**2 + (2 * x**2 + 1) / x * y + x**2

def value(x_0, h, N, X, Y):
    for i in range(N):
        if X[i] <= x_0 < X[i+1]:
            return Y[i] + x_0 / h * (Y[i+1] - Y[i])
            break
    return Y[-1]

epsilon = 1e-4
start = 1
end = 2
L = end - start
h = 0.1
X = np.arange(start, end + h, h)
X2 = np.linspace(start, end, 11, endpoint='True')
N = len(X)
Y = np.zeros(N)
Start_value = -3
Y[0] = Start_value
for i in range(N-1):
    f1 = f(X[i], Y[i])
    f2 = f(X[i] + h / 2, Y[i] + h / 2 * f1)
    Y[i+1] = Y[i] + h * f2

while True:
    h /= 2
    X = np.arange(start, end + h, h)
    N = len(X)
    Y1 = np.zeros(N)
    Y1[0] = Start_value
    for i in range(N-1):
        f1 = f(X[i], Y1[i])
        f2 = f(X[i] + h / 2, Y1[i] + h / 2 * f1)
        Y1[i+1] = Y1[i] + h * f2
    # Проверка достижения точности
    diff = [(Y1[i] - Y[i // 2]) / 3 for i in range(len(Y1))]
    print(max(diff))
    if max(diff) <= epsilon: break
    else: Y = Y1

print("==========")
Yh = np.zeros(11)
Yh2 = np.zeros(11)
for i in range(len(X2)):
    for j in range(N):
        if X[j] <= X2[i] < X[j+1]:
            Yh[i] = Y1[j] + (X2[i] - X[j]) / h * (Y1[j+1] - Y1[j])
            break
X = np.arange(start, end + h * 2, h * 2)
N = len(X)
for i in range(len(X2)):
    for j in range(N):
        if X[j] <= X2[i] < X[j+1]:
            Yh2[i] = Y[j] + (X2[i] - X[j]) / h * (Y[j+1] - Y[j])
            break
diffY2 = np.abs(Yh2 - Yh)
print("h = ", h * 2)
print(X2)
print(Yh)
print(Yh2)
print(diffY2)
plt.plot(X, Y)
plt.grid()
plt.show()