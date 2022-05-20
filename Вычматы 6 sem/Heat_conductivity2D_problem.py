import matplotlib.pyplot as plt
import numpy as np
from math import pi, cos, sin, exp
from numba import jit

# Функции
def analyticFunc(x, y, t): # Аналитическая функция
    return cos(pi*x) * sin(5*pi*y) * exp(-50*pi**2 * lam * t)

@jit
def newAnalytic_Func(M, T):
    u = np.empty((M, M))
    for i in range(M):
        for j in range(M):
            u[i, j] = analyticFunc(Cells[i], Cells[j], T)
    return u

def initFunc(x, y): # Начальные условия
    return cos(pi*x) * sin(5*pi*y)

@jit
def new_Func(M):
    u = np.empty((M, M))
    for i in range(M):
        for j in range(M):
            u[i, j] = initFunc(Cells[i], Cells[j])
    return u

def boundX0Func(y, t):
    return sin(5*pi*y) * exp(-50*pi**2 *lam * t)

def boundX1Func(y, t):
    return -sin(5*pi*y) * exp(-50*pi**2 *lam * t)

def boundY0Func(x, t):
    return 0

def boundY1Func(x, t):
    return 0

def mi2ci(m, k): # Matrix Index To Matrix Index
    return m + (k-1) * M

def ci2mi(i): # Column Index To Column Index
    return (i % M, (i - i % M) // M + 1)

def GaussZeidel_5diag(u_center, u_top, u_left, u_right, u_bottom, sygma_x, sygma_y):
    (a, b, c, f, g) = coefficients(sygma_x, sygma_y)
    return (u_center - c*u_left - g*u_bottom - b*u_right - f*u_top) / a

def coefficients(sygma_x, sygma_y):
    return (1 + 2*sygma_x + 2*sygma_y, -sygma_y, -sygma_x, -sygma_x, -sygma_y)

@jit
def model(u, T):
    u1 = np.copy(u)

    # Цикл по времени
    for t in np.arange(0, T, dt):
        for i in range(M):
            # Граничные условия:
            u1[0, i] = boundX0Func(Cells[i], t)
            u1[-1, i] = boundX1Func(Cells[i], t)
            u1[i, 0] = boundY0Func(Cells[i], t)
            u1[i, -1] = boundY1Func(Cells[i], t)

        for i in range(1, M-1):
            for j in range(1, M-1):
                u1[i, j] = GaussZeidel_5diag(u[i, j], u[i+1, j], u[i, j-1], u[i, j+1], u[i-1, j], sygma_x, sygma_y)
        u = u1
    return u

# Параметры задачи
L = 1 # Область задачи в пространстве
T = 1 # Время моделирования
lam = 1e-4 # Параметр задачи

M_List = np.array([10, 20, 50, 100])
Norms = []
for M in M_List:
    h = L / (M - 1) # Шаг по сетке
    dt = 0.9 * h**2 / 52 / lam # Шаг по времени
    sygma_x = 25 * lam * dt / h**2
    sygma_y = lam * dt / h**2
    Cells = np.linspace(0, L, M)
    u = new_Func(M)
    u = model(u, T)
    u_analyt = newAnalytic_Func(M, T)
    Norms.append(np.linalg.norm(u - u_analyt))
    print(M, "x", M, " точек на сетке посчитано")

# Построение графика ошибки от шага интегрирования
plt.plot(M_List, Norms)
plt.show()