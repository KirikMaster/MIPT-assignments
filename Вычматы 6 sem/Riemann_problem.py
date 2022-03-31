import numpy as np
import matplotlib.pyplot as plt

# Параметры задачи
L = 10 # Размер рабочей области; x принадлежит [-10, 10]
gamma = 5 / 3 # Показатель адиабаты
# Слева от перегородки x = 0:
v_L = 0
rho_L = 13
P_L = 10
# Справа от перегородки:
v_R = 0
rho_R = 1.3
P_R = 1
T = 5 # Время моделирования
h = 0.45 # Шаг по координате
CFL = 0.1  # Число Куранта максимальное
dt = h * CFL # Шаг по времени

# Создание
Nodes = np.arange(-L, L, h) # Узлы сетки
M = np.size(Nodes)
print("Nodes: ", Nodes)
rho = np.zeros(M)
u = np.zeros(M)
e = np.zeros(M)
for i in range(M):
    if Nodes[i] < 0:
        rho[i] = rho_L
        e[i] = P_L / (gamma - 1) / rho_L
    else:
        rho[i] = rho_R
        e[i] = P_R / (gamma - 1) / rho_R
print("rho = ", rho)
print("u = ", u)
print("e = ", e)

# Вычисление
