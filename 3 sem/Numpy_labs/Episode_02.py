import numpy as np
import matplotlib.pyplot as plt

N = 3
ar = 'signals/signal01.dat signals/signal02.dat signals/signal03.dat'
adresses = ar.split()
figs = [None for i in range(N)]

for i in range(N):
    with open(adresses[i], 'r') as f:
        lines = []
        for line in f:
            lines.append(float(line[:len(line) - 1]))
        data = np.array(lines)
        figs[i], axs = plt.subplots(1, 2)
        axs[0].plot(data, 'b-')   #Сырой сигнал
        axs[0].set_title("Сырой сигнал")

        data_improved = data

        #Вариант работы фильтра №1

        for j in range(len(data),-1,-1):
            chunk = data_improved[j:j+10]
            divider = np.arange(1,len(chunk) + 1)
            data_improved[j:j+10] = np.cumsum(chunk)/divider

        #Вариант работы фильтра №2

        #chunks = np.array_split(data_improved, 10)
        #for chunk in range(len(chunks)):
        #    divider = np.arange(1,len(chunks[chunk]) + 1)
        #    chunks[chunk] = np.cumsum(chunks[chunk])/divider
        #data_improved = np.concatenate(chunks)

        axs[1].plot(data_improved, 'b-')   #Обработанный сигнал
        axs[1].set_title("Обработанный сигнал")
plt.show()




