import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import requests

url = requests.get('http://judge2.vdi.mipt.ru/ejudge/lab_01_mpl/frames.dat')
Lines = url.text.split('\n')
N = len(Lines)//2
X, Y = [[float(j) for j in Lines[2*i].split()] for i in range(N)], [[float(j) for j in Lines[2*i + 1].split()] for i in range(N)]
frames = []
fig = plt.figure
ax = plt.axes
#print(len(X), X[0][1], X[1][1], X[2][1], X[3][1], X[4][1], X[5][1], sep='\n')
#print(len(Y), Y[0][1], Y[1][1], Y[2][1], Y[3][1], Y[4][1], Y[5][1], sep='\n')

for i in range(N):
    ln, = plt.plot(X[i], Y[i])
    frames.append([ln])
miny, maxy = min(Y[0]) - 0.1 * abs(max(Y[0]) - min(Y[0])), max(Y[0]) + 0.1 * abs(max(Y[0]) - min(Y[0]))
plt.axis([min(X[0]), max(X[0]), miny, maxy])
plt.grid(True)

anim = ArtistAnimation(fig, frames, interval = 300, repeat = True, repeat_delay = 1000)
plt.show()