import numpy as np
import matplotlib as plt
import pandas as pd

data = pd.read_csv("Atmosphere_1.csv")
N = data.shape[0] - 1 #Количество сплайнов
h = [data.loc[i + 1, "H, км"] - data.loc[i, "H, км"] for i in range(N)]
u = [data.loc[i, "DEN, кг/м3"] for i in range(N + 1)]
a = [u[i] for i in range(N + 1)]
f_1 = [(u[i + 1] - u[i]) / h[i] for i in range(N)]
f_2 = [(f_1[i + 1] - f_1[i]) / (h[i + 1] + h[i]) for i in range(N - 1)]
print(len(u), len(f_1), len(f_2))
A = np.zeros((N-1, N-1))
for i in range(1, N-2):
    A[i, i] = 2
    A[i, i+1] = h[i] / (h[i-1] + h[i])
    A[i, i-1] = h[i-1] / (h[i-1] + h[i])
A[0, 0], A[N-2, N-2] = 2, 2
A[0, 1] = h[1]/(h[0] + h[0])
A[N-2, N-3] = h[N-2]/(h[N-2] + h[N-1])
g = np.array(f_2) * 6
#print(g)
#print(g.size, A.shape)
c = np.linalg.solve(A, g)
print("c = ", c)
print("TOTAL SPLINES ", N)
print("TOTAL ELEMENTS ", N + 1)
print(A)
print("-------")
print(data)
#print(data.loc[1, "DEN, кг/м3"])

#Разобрался с синтаксисом pandas, нашёл коэффициенты c, правда почему-то не методом прогонки, а просто из СЛАУ.