import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import requests

url = requests.get('http://judge2.vdi.mipt.ru/ejudge/lab_02_numpy/start.dat')
Lines = [float(i) for i in url.text.split('\n')]
u0 = np.array(Lines)
N = len(u0)

A = np.diag(np.ones(N)) + np.diag(np.ones(N-1) * (-1), k = - 1) + np.diag(np.ones(1) * (-1), k = N-1)
fig = plt.figure()
ax = plt.axes(xlim=(0, 50), ylim=(0, 10))
ax.set_title("Динамический график рекурсивной функции u(x)")
plt.grid(True)
line, = ax.plot([], [], lw=3)
x = np.linspace(1,N)

def u(u0):
    return u0 - 0.5 * A @ u0

def init():
    line.set_data(x,u0)
    return line,

def animate(i):
    u1 = line.get_data()[1]
    y = u(u1)
    line.set_data(x,y)
    return line,

anim = FuncAnimation(fig, animate, init_func=init, frames=255, interval=10, blit=False)
plt.show()
