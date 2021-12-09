from math import *
import numpy as np
import matplotlib.pyplot as plt

L = 1
h = 0.1
X = np.arange(0, L + h, h)
N = len(X)

# Аналитическое решение
k_ = sqrt(e)
q_ = 1.125
f_ = exp(-0.5)
lam1 = sqrt(q_ / k_)
lam2 = -sqrt(q_ / k_)
c = f_ * k_ * lam2 / (q_ * k_ * (lam1 * (k_ * lam2 + 1) * exp(lam2) - lam2 * (k_ * lam1 + 1) * exp(lam1)))

def u_analytical(x):
    return c * (exp(lam1 * x) + exp(lam2 * x)) + f_ / q_

Y = np.vectorize(u_analytical)(X)
print("analytic: ", Y)
fig1, ax1 = plt.subplots()
ax1.plot(X, Y, label='analytic')

# Численное решение модельной задачи
a, b, c, d = np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)
a[:N-1] = k_
b[0] = -k_
b[1:N-1] = -2 * k_ - q_ * h**2
b[-1] = -k_ - h
c[1:] = k_
d[1:N-1] = -f_ * h**2
alpha, beta = np.zeros(N-1), np.zeros(N-1)
alpha[0] = -a[0] / b[0]
beta[0] = d[0] / b[0]
for i in range(1, N-1):
    alpha[i] = - a[i] / (b[i] + c[i] * alpha[i-1])
    beta[i] = (d[i] - c[i] * beta[i-1]) / (b[i] + c[i] * alpha[i-1])

Y1 = np.zeros(N)
Y1[-1] = (d[-1] - c[-1] * beta[-1]) / (b[-1] + c[-1] * alpha[-1])
for i in range(N-2, -1, -1):
    Y1[i] = alpha[i] * Y1[i+1] + beta[i]
print("Numerical, model: ", Y)
ax1.plot(X, Y1, label='numerical, model')

# Численное решение задачи с переменными коэффициентами
def k(x):
    return exp(x)
def q(x):
    return 1 + x**3
def f(x):
    return exp(-x)

a, b, c, d = np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)
a[0] = k(0)
b[0] = -k(0)
b[-1] = -k(L) - h
c[-1] = k(L)
for i in range(1, N-1): 
    a[i] = k(X[i] + h/2)
    b[i] = -k(X[i] + h/2) - k(X[i] - h/2) - q(X[i]) * h**2
    c[i] = k(X[i] - h/2)
    d[i] = -f(X[i]) * h**2
alpha, beta = np.zeros(N-1), np.zeros(N-1)
alpha[0] = -a[0] / b[0]
beta[0] = d[0] / b[0]
for i in range(1, N-1):
    alpha[i] = - a[i] / (b[i] + c[i] * alpha[i-1])
    beta[i] = (d[i] - c[i] * beta[i-1]) / (b[i] + c[i] * alpha[i-1])

Y2 = np.zeros(N)
Y2[-1] = (d[-1] - c[-1] * beta[-1]) / (b[-1] + c[-1] * alpha[-1])
for i in range(N-2, -1, -1):
    Y2[i] = alpha[i] * Y2[i+1] + beta[i]
print("numerical: ", Y)
ax1.plot(X, Y2, label='numeric')
ax1.grid()
ax1.legend()

# Построим решение задачи с переменными коэффициентами на вдвое сгущающихся сетках
fig2, ax2 = plt.subplots()
for j in range(5):
    h = 0.1 * 2**(-j)
    X = np.arange(0, L + h, h)
    N = len(X)
    a, b, c, d = np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)
    a[0] = k(0)
    b[0] = -k(0)
    b[-1] = -k(L) - h
    c[-1] = k(L)
    for i in range(1, N-1): 
        a[i] = k(X[i] + h/2)
        b[i] = -k(X[i] + h/2) - k(X[i] - h/2) - q(X[i]) * h**2
        c[i] = k(X[i] - h/2)
        d[i] = -f(X[i]) * h**2
    alpha, beta = np.zeros(N-1), np.zeros(N-1)
    alpha[0] = -a[0] / b[0]
    beta[0] = d[0] / b[0]
    for i in range(1, N-1):
        alpha[i] = - a[i] / (b[i] + c[i] * alpha[i-1])
        beta[i] = (d[i] - c[i] * beta[i-1]) / (b[i] + c[i] * alpha[i-1])
   
    Y2 = np.zeros(N)
    Y2[-1] = (d[-1] - c[-1] * beta[-1]) / (b[-1] + c[-1] * alpha[-1])
    for i in range(N-2, -1, -1):
        Y2[i] = alpha[i] * Y2[i+1] + beta[i]
    ax2.plot(X, Y2, label=('h = ' + str(h)))
    ax2.grid()
    ax2.legend()

plt.show()