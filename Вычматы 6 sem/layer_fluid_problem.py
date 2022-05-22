import matplotlib.pyplot as plt
import numpy as np
from math import pi, cos, sin, exp

# Функции
def density(input):
    return rho0 * (1 + Cf * (input - Po))

def rho(i):
    return density(max(P[i], P[i+1]))

def rho_(i):
    return density(max(P[i], P[i-1]))

def TriagonalSlae_solver(a, b, c, d, N, M = 1, transpose = False):
    # np.shape(a or b or c or d) == (N, M)

    # a[0] * u[1] + b[0] * u[0] = d[0]
    # a[i] * u[i + 1] + b[i] * u[i] + c[i] * u[i - 1] = d[i], i = range(1, N - 1)
    # b[N - 1] * u[N - 1] + c[N - 1] * u[N - 2] = d[N - 1]

    # (!) There should be c[0] = 0, a[N - 1] = 0
    # This solver can solve M SLAE's simultaneously

    # u[0] = f(m) <==> a[0] = 0, b[0] = 1, d[0] = f(m)
    # u[N - 1] = g(m) <==> c[N - 1] = 0, b[N - 1] = 1, d[N - 1] = g(m)

    dimens = (N, M)
    shape_a = np.shape(a)
    shape_b = np.shape(b)
    shape_c = np.shape(c)
    shape_d = np.shape(d)

    if M != 1:
        if (dimens != shape_a or dimens != shape_b or dimens != shape_c or dimens != shape_d):
            print("\nERROR IN TriagonalSlae_solver")
            print(f"shape_a = {shape_a}, (N, M) = {dimens}\n")
            return False
    else:
        if (dimens[0] != shape_a[0] or dimens[0] != shape_b[0] or dimens[0] != shape_c[0] or dimens[0] != shape_d[0]):
            print("\nERROR IN TriagonalSlae_solver")
            print(f"shape_a = {shape_a}, (N, M) = {dimens}\n")
            return False
    
    if transpose:
        (N, M) = (M, N)
        a, b, c, d = a.T, b.T, c.T, d.T

    # u[i] = alpha[i] * u[i + 1] + beta[i]
    alpha, beta = np.zeros((N - 1, M)), np.zeros((N - 1, M))
    alpha[0] = - a[0] / b[0]
    beta[0] = d[0] / b[0]
    for it in range(1, N - 1):
        divider = b[it] + c[it] * alpha[it - 1]
        alpha[it] = - a[it] / divider
        beta[it] = (d[it] - c[it] * beta[it - 1]) / divider
    
    if M != 1:
        u = np.zeros((N, M))
    else:
        u = np.zeros(N)
    
    u[N - 1] = (d[N - 1] - c[N - 1] * beta[N - 2]) / (b[N - 1] + c[N - 1] * alpha[N - 2])
    for it in range(N - 2, -1, -1):
        u[it] = alpha[it] * u[it + 1] + beta[it]

    if transpose:
        return u.T
    
    return u

# Параметры задачи
dz = 10 # м - толщина
B = 50 # м - ширина
L = 500 # м - длина
P0 = 1e7 # Па - начальное давление 
Ping = 1.5e7 # Па - нагнетательное давление
Pprod = 5.0e6 # Па - добывающее давление
k = 1e-14 # м^-2 - проницаемость пласта
mu = 1e-3 # Па*с - вязкость жидкости
phi = 0.2 # пористость пласта
rho0 = 1000 # кг/м^3 - плотность жидкости при опорном давлении p0
Po = 1.2e7 # Па - опорное давление
Cf = 1e-9 # Па^-1 - сжимаемость жидкости
T = 3600 * 24 # Время моделирования задачи (сутки)
N = 4 # Количество изображений
ti = T / N # Время между изображениями
tau = 0.1

# Генерация сетки
M = 100 # Количество узлов
h = L / (M - 1) # Шаг по координате
Cells = np.linspace(0, L, M)
Nodes = np.arange(h/2, L - h/2, h)
dt = 3600 # с - шаг по времени (час)

# Моделирование
P = np.ones(M) # Переменные давления на сетке
P *= P0
P[0] = Ping
P[-1] = Pprod
a = np.ones(M)
b = np.ones(M)
c = np.ones(M)
d = np.ones((M,))
Pim = np.ones((N, M))
Pim[0, :] = P.copy()
count = 1
for t in range(T // dt):
    a[0] = 1
    a[-1] = 1
    b[0] = 0
    c[-1] = 0
    d[0] = Ping
    d[-1] = Pprod
    for i in range(1, M-1):
        c[i] = k * rho_(i) / mu / h**2
        b[i] = k * rho(i) / mu / h**2
        a[i] = -c[i] - b[i] - phi * Cf * rho0 / dt
        q = P[i]
        print(q)
        d[i] = q

    A = np.zeros((M, M))
    for i in range(M):
        A[i, i] = a[i]
    for i in range(1, M):
        A[i, i-1] = c[i]
    for i in range(M-1):
        A[i, i+1] = b[i]
    for i in range(10):
        P = (np.eye(M) - tau * A) * P + tau * d
    #P = TriagonalSlae_solver(c, a, b, d, M)
    P[0] = Ping
    P[-1] = Pprod

    if t*dt > ti*count:
        Pim[count, :] = np.copy(P)
        count += 1

# Представление результатов
fig, ax = plt.subplots(N)
for i in range(N):
    ax[i].plot(Cells, Pim[i])
    ax[i].set_title("Давление в пласте спустя " + str(ti*i) + " с")
    ax[i].grid()
plt.show()