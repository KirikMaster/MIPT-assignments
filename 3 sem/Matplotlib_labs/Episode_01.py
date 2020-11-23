import matplotlib.pyplot as plt
ar = 'dead_moroz/001.dat dead_moroz/002.dat dead_moroz/003.dat dead_moroz/004.dat dead_moroz/005.dat'
data = ar.split()
fig, ax = plt.subplots(2,3)
for j in range(len(data)):
    x, y = [], []
    with open(data[j], 'r') as f:
        N = int(f.readline())
        for i in range(N):
            new = f.readline().split()
            x.append(float(new[0]))
            y.append(float(new[1]))
    ax[j // 3][j % 3].scatter(x,y, 10)
    minx, miny, maxx, maxy = min(x), min(y), max(x), max(y)
    avgx, avgy = (minx + maxx)/2, (miny + maxy)/2
    ran, lil = max((maxy - miny), (maxx - minx)), min((maxy - miny), (maxx - minx))
    if ran == maxx - minx:
        axxmin = avgx - 1.1*(avgx - minx)
        axxmax = avgx + 1.1*(avgx - minx)
        axymin = avgy - 1.1*ran/lil*(avgy - miny)
        axymax = avgy + 1.1*ran/lil*(avgy - miny)
    else:
        axxmin = avgx - 1.1*ran/lil*(avgx - minx)
        axxmax = avgx + 1.1*ran/lil*(avgx - minx)
        axymin = avgy - 1.1*(avgy - miny)
        axymax = avgy + 1.1*(avgy - miny)
    ax[j // 3][j % 3].axis([axxmin, axxmax, axymin, axymax])
    ax[j // 3][j % 3].set_title("plot #" + str(j+1))
plt.show()