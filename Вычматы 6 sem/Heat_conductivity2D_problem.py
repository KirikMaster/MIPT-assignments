import matplotlib.pyplot as plt
import numpy as np
from math import pi, cos, sin, exp
#from numba import jit

# Функции

def analyticFunc(x, y, t): # Аналитическая функция
    return cos(pi*x) * sin(5*pi*y) * exp(-50*pi**2 * lam * t)

#@jit
def newAnalytic_Func(M, T):
    u = np.empty((M, M))
    for i in range(M):
        for j in range(M):
            u[i, j] = analyticFunc(Cells[i], Cells[j], T)
    return u

def initFunc(x, y): # Начальные условия
    return cos(pi*x) * sin(5*pi*y)

#@jit
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

def twoStepMethod(u, u05, u1):
    for i in range(1, M-1):
        for j in range(1, M-1):
            block0 = block(u, i, j)
            block05 = block(u05, i, j)
            u05[i, j] = GaussZeidel_5diag1(block0, block05, sygma_x, sygma_y)  
    for i in range(1, M-1):
        for j in range(1, M-1):
            block05 = block(u05, i, j)
            block1 = block(u1, i, j)
            u1[i, j] = GaussZeidel_5diag2(block05, block1, sygma_x, sygma_y)
    return u1

def ninePointMethod(u, u1):
    for i in range(1, M-1):
        for j in range(1, M-1):
            block = u[i-1:i+2, j-1:j+2]
            block[1, 0] = u1[i, j-1]
            block[0, 0] = u1[i-1, j-1]
            block[0, 1] = u1[i-1, j]
            u1[i, j] = GaussZeidel_9diag(block, sygma_x, sygma_y)
    return u1

def block(u, i, j):
    return u[i-1:i+2, j-1:j+2]

def GaussZeidel_9diag(u_block, sygma_x, sygma_y):
    (a, b, c, g) = coefficients(sygma_x, sygma_y)
    g = 0
    return (u_block[1, 1] - b*(u_block[1, 0] + u_block[1, 2]) - c*(u_block[0, 1] + u_block[2, 1]) - g*(u_block[0, 0] + u_block[0, 2] + u_block[2, 2] + u_block[2, 0])) / a

def GaussZeidel_5diag1(u_block, u1_block, sygma_x, sygma_y):
    (a, b, c) = coefficients1(sygma_x, sygma_y)
    return (u_block[1, 1] + c*(u_block[2, 1] - 2*u_block[1, 1] + u_block[0, 1]) - b*(u1_block[1, 0] + u_block[1, 2])) / a

def GaussZeidel_5diag2(u_block, u1_block, sygma_x, sygma_y):
    (a, b, c) = coefficients2(sygma_x, sygma_y)
    return (u_block[1, 1] + c*(u_block[1, 2] - 2*u_block[1, 1] + u_block[1, 0]) - b*(u1_block[0, 1] + u_block[2, 1])) / a

def coefficients(sygma_x, sygma_y):
    return (1 + 2*sygma_x + 2*sygma_y + 4*sygma_x*sygma_y, # a
            -sygma_x - 2*sygma_x*sygma_y, # b
            -sygma_y - 2*sygma_x*sygma_y, # c
            sygma_x*sygma_y) # g

def coefficients1(sygma_x, sygma_y):
    return (1 + sygma_x,     # a
            -sygma_x/2,      # b
             sygma_y/2)      # c

def coefficients2(sygma_x, sygma_y):
    return (1 + sygma_y,     # a
            -sygma_y/2,      # b
            sygma_x/2)      # c

#@jit
def model(u, T):
    u1 = np.empty((M, M))
    u05 = np.empty((M, M))

    # Цикл по времени
    for t in np.arange(0, T, dt):
        for i in range(M):
            # Граничные условия:
            u1[0, i] = boundX0Func(Cells[i], t)
            u1[-1, i] = boundX1Func(Cells[i], t)
            u1[i, 0] = boundY0Func(Cells[i], t)
            u1[i, -1] = boundY1Func(Cells[i], t)
            u05[0, i] = boundX0Func(Cells[i], t - dt/2)
            u05[-1, i] = boundX1Func(Cells[i], t - dt/2)
            u05[i, 0] = boundY0Func(Cells[i], t - dt/2)
            u05[i, -1] = boundY1Func(Cells[i], t - dt/2)

        u1 = twoStepMethod(u, u05, u1)
        #u1 = ninePointMethod(u, u1)

        u = u1
    return u

# Параметры задачи
L = 1 # Область задачи в пространстве
T = 1 # Время моделирования
lam = 1e-4 # Параметр задачи

M_List = np.array([10, 20, 50, 100, 200, 500])
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
    Norms.append(np.max(np.absolute(u - u_analyt)))
    print(M, "x", M, " точек на сетке посчитано")

# Построение графика ошибки от шага интегрирования
plt.plot(M_List, Norms, '-o')
plt.grid()

XMeshgrid, YMeshgrid = np.meshgrid(Cells, Cells)

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.contour3D(XMeshgrid, YMeshgrid, u, 75, cmap="viridis")
ax.set_title("Численное моделирование, M = " + str(M))

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.contour3D(XMeshgrid, YMeshgrid, u_analyt, 75, cmap="viridis")
ax.set_title("Теоретическое решение")

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.contour3D(XMeshgrid, YMeshgrid, abs(u - u_analyt), 75, cmap="viridis")
ax.set_title("Ошибка моделирования, M = " + str(M))
plt.show()