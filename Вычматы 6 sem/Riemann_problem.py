import numpy as np
import matplotlib.pyplot as plt

# Фукнции
def matrix_A(u, e):
    A = np.zeros((3, 3))
    A[0, 1] = 1
    A[1, 0] = -u * u
    A[1, 1] = 2 * u
    A[1, 2] = gamma - 1
    A[2, 0] = -gamma * u * e
    A[2, 1] = gamma * e
    A[2, 2] = u
    return A

def matrix_Omega(u, c):
    Omega = np.zeros((3, 3))
    Omega[0, 0] = -u * c
    Omega[0, 1] = c
    Omega[0, 2] = gamma - 1
    Omega[1, 0] = -c * c
    Omega[1, 2] = gamma - 1
    Omega[2, 0] = u * c
    Omega[2, 1] = -c
    Omega[2, 2] = gamma - 1
    return Omega

# Параметры задачи
L = 10 # Размер рабочей области; x принадлежит [-10, 10]
gamma = 5 / 3 # Показатель адиабаты
# Слева от перегородки x = 0:
v_L = 0
rho_L = 13
P_L = 1e6
# Справа от перегородки:
v_R = 0
rho_R = 1.3
P_R = 1e5
T = 0.015 # Время моделирования
h = 0.2 # Шаг по координате
CFL = 0.01  # Число Куранта максимальное
dt = h * CFL # Шаг по времени

# Создание
t = 0 # Начальное время
Nodes = np.arange(-L, L, h) # Узлы сетки
M = np.size(Nodes)
#print("Nodes: ", Nodes)
rho = np.zeros(M)
u = np.zeros(M)
e = np.zeros(M)
P = np.zeros(M)
for i in range(M):
    if Nodes[i] < 0:
        rho[i] = rho_L
        P[i] = P_L
        e[i] = P_L / (gamma - 1) / rho_L
    else:
        rho[i] = rho_R
        P[i] = P_R
        e[i] = P_R / (gamma - 1) / rho_R
w = np.array([rho, rho*u, rho*e]).T
w_next = np.copy(w)
#print("w = ", w)
count = 0

A = np.zeros((M, 3, 3))
Omega = np.zeros((M, 3, 3))
Omega_inv = np.zeros((M, 3, 3))
Lam = np.zeros((M, 3, 3))
Lam_mod = np.zeros((M, 3, 3))
c = np.zeros(M)

# Вычисление
while t < T:
    for i in range(M):
        #Вычисляем матрицы в узле x_i
        A[i] = matrix_A(u[i], e[i]) # A(i, m)
        c[i] = np.sqrt(gamma * (gamma - 1) * e[i])
        Omega[i] = matrix_Omega(u[i], c[i]) # Omega(i, m)
        Omega_inv[i] = np.linalg.inv(Omega[i])
        Lam[i] = np.diag([u[i] + c[i], u[i], u[i] - c[i]])
        Lam_mod[i] = np.diag([abs(u[i] + c[i]), abs(u[i]), abs(u[i] - c[i])])

    #Проверяем выполнение условия устойчивости
    dt = h * CFL # Стандартный шаг по времени
    while dt * np.max(Lam_mod) / h >= CFL:
        dt /= 2

    #Вычисляем консервативных переменных на новом слое по времени
    w = np.array([rho, rho*u, rho*e]).T
    for i in range(1, M-1):
        w_next[i] = w[i] - dt * (A[i] @ (w[i+1] - w[i-1]).T).T / 2 / h + dt * ((Omega_inv[i] @ Lam_mod[i] @ Omega[i]) @ (w[i+1] - 2*w[i] + w[i-1]).T).T / 2 / h

    #Возвращаемся к примитивным переменным
    rho = w_next[:, 0]
    u = w_next[:, 1] / rho
    e = w_next[:, 2] / rho

    #Граничные условия
    rho[0] = rho[1]
    u[0] = u[1]
    e[0] = e[1]
    rho[-1] = rho[-2]
    u[-1] = u[-2]
    e[-1] = e[-2]

    P = (gamma - 1) * rho * e # Давление в новом слое
    t += dt # Увеличение текущего времени на dt
    count+=1
    if count == 50:
        print(t)
        count = 0

# Построение графиков
fig, axs = plt.subplots(3)
axs[0].plot(Nodes, P)
axs[0].set_title("Давление, T = " + str(T))
axs[1].plot(Nodes, u, 'green')
axs[1].set_title("Скорость, T = " + str(T))
axs[2].plot(Nodes, rho, 'orange')
axs[2].set_title("Плотность, T = " + str(T))
#.set_title("Решение задачи Римана о распаде разрыва через " + str(T) + " с")
plt.legend()
axs[0].grid()
axs[1].grid()
axs[2].grid()
plt.show()