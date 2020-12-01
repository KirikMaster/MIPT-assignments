import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import requests

url = requests.get('http://judge2.vdi.mipt.ru/ejudge/lab_01_mpl/frames.dat')
Lines = url.text.split('\n')
N = len(Lines)//2
X, Y = [[float(j) for j in Lines[2*i].split()] for i in range(N)], [[float(j) for j in Lines[2*i + 1].split()] for i in range(N)]
frames = []
fig = plt.figure()

for i in range(N):
    frame, = plt.plot(X[i], Y[i], 'r-')
    frames.append([frame,])

miny, maxy = min(Y[5]) - 0.1 * abs(max(Y[5]) - min(Y[5])), max(Y[5]) + 0.1 * abs(max(Y[5]) - min(Y[5]))
plt.axis([min(X[0]), max(X[0]), miny, maxy])
plt.grid(True)

anim = ArtistAnimation(fig, frames, interval=200)
plt.show()
