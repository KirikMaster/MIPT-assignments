import numpy as np
import matplotlib.pyplot as plt
from math import ceil

# Функции
def initialFunc(Nodes):
    return np.sin(4 * np.pi * Nodes / L)

# Параметры задачи
L = 20 # Размер рабочей области
T = 18 # Время моделирования
h = 0.5 # Шаг по координате
CFL = 0.6 # Число Куранта
dt = h * CFL # Шаг по времени
Nodes = np.arange(0, L, h) # Узлы сетки
M = np.size(Nodes)
a = 0.5 # Постоянная для схемы Лакса-Вендрофа
print("Nodes: ", Nodes)

# Начальные условия
u = np.zeros(M, dtype=[('C', np.float64), ('LV', np.float64)])
u['C'] = initialFunc(Nodes)
u['LV'] = initialFunc(Nodes)
u_next = np.zeros(M, dtype=[('C', np.float64), ('LV', np.float64)])
period = 4
Nsl = ceil(T / period)
u_by_period = np.zeros((Nsl, M), dtype=[('C', np.float64), ('LV', np.float64)])
u_by_period[0] = u
count = 1

# Вычисление
for m in range(int(T / dt)):
    # Схема Уголок
    u_next[0]['C'] = u[0]['C'] - CFL * (u[0]['C'] - u[-1]['C']) # Цикличное граничное условие слева
    for i in range(1, M):
        u_next[i]['C'] = u[i]['C'] - CFL * (u[i]['C'] - u[i-1]['C'])

    # Схема Лакса-Вендрофа
    u_next[0]['LV'] = u[0]['LV'] - a / 2 * CFL * (u[1]['LV'] - u[-1]['LV']) + a**2 / 2 * CFL**2 * (u[1]['LV'] - 2 * u[0]['LV'] + u[-1]['LV']) # Цикличное граничное условие слева
    u_next[-1]['LV'] = u[-1]['LV'] - a / 2 * CFL * (u[0]['LV'] - u[-2]['LV']) + a**2 / 2 * CFL**2 * (u[0]['LV'] - 2 * u[-1]['LV'] + u[-2]['LV']) # Цикличное граничное условие справа
    for i in range(1, M-1):
        u_next[i]['LV'] = u[i]['LV'] - a / 2 * CFL * (u[i+1]['LV'] - u[i-1]['LV']) + a**2 / 2 * CFL**2 * (u[i+1]['LV'] - 2 * u[i]['LV'] + u[i-1]['LV'])

    if m * dt / period >= count:
        u_by_period[count] = u
        count += 1
    u = u_next
u_by_period[-1] = u

# Построение графиков
fig, axs = plt.subplots(Nsl, figsize=(6 * 4 / Nsl, 48 / 25 * Nsl))
top, bottom = max(u_by_period[0]['C']), min(u_by_period[0]['C'])
for i in range(Nsl):
    axs[i].plot(Nodes, u_by_period[i]['C'], label="Схема уголок")
    axs[i].plot(Nodes, u_by_period[i]['LV'], label="Схема Лакса-Вендрофа")
    axs[i].set_ylim(-top, top)
    axs[i].legend()
    axs[i].set_title("После " + str(i * period) + " с")
    if i == Nsl - 1:
        axs[i].set_title("После " + str(T) + " с")
    axs[i].grid()
plt.show()