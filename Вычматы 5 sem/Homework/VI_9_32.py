import matplotlib.pyplot as plt
import numpy as np

data = {1910: 92228496,
        1920: 106021537,
        1930: 123202624,
        1940: 132164569,
        1950: 151325798,
        1960: 179323175,
        1970: 203211926,
        1980: 226545805,
        1990: 248709873,
        2000: 281421906}

#a)
def foo(x, n):
    answer = 1
    for i in range(n):
        answer *= (x - X[i])
    return answer

def NewtonP(x):
    return f[0] + f_1[0] * foo(x, 1) + f_2[0] * foo(x, 2) + f_3[0] * foo(x, 3) + f_4[0] * foo(x, 4) + f_5[0] * foo(x, 5) + f_6[0] * foo(x, 6) + f_7[0] * foo(x, 7) + f_8[0] * foo(x, 8) + f_9[0] * foo(x, 9)

X   = list(data.keys())
f   = list(data.values())
f_1 = [(f[i+1]   - f[i])   / 10 for i in range(9)]
f_2 = [(f_1[i+1] - f_1[i]) / 20 for i in range(8)]
f_3 = [(f_2[i+1] - f_2[i]) / 30 for i in range(7)]
f_4 = [(f_3[i+1] - f_3[i]) / 40 for i in range(6)]
f_5 = [(f_4[i+1] - f_4[i]) / 50 for i in range(5)]
f_6 = [(f_5[i+1] - f_5[i]) / 60 for i in range(4)]
f_7 = [(f_6[i+1] - f_6[i]) / 70 for i in range(3)]
f_8 = [(f_7[i+1] - f_7[i]) / 80 for i in range(2)]
f_9 = [(f_8[i+1] - f_8[i]) / 90 for i in range(1)]

dx = 0.1
Xline = np.arange(1910, 2010, dx)
Yline = np.vectorize(NewtonP)(Xline)
print("In year 2010: ", NewtonP(2010))
print("error: ", abs((308745538 - NewtonP(2010))/308745538))

#б)
def locate(x_0):
    for i in range(9):
        if X[i] <= x_0 < X[i+1]:
            return i
            break
    return 8

def spline(x_0):
    i = locate(x_0)
    return a[i] + b[i] * (x_0 - X[i+1]) + c[i] * (x_0 - X[i+1])**2 / 2 + d[i] * (x_0 - X[i+1])**3 / 6

N = len(X) - 1 #Количество сплайнов
h = [X[i + 1] - X[i] for i in range(N)]
a, b, c, d = np.copy(f[1:]), np.zeros(N), np.zeros(N), np.zeros(N)
A = np.zeros((N-1, N-1))
for i in range(1, N-2):
    A[i, i] = 2
    A[i, i+1] = h[i+1] / (h[i] + h[i+1])
    A[i, i-1] = h[i] / (h[i] + h[i+1])
A[0, 0], A[N-2, N-2] = 2, 2
A[0, 1] = h[1]/(h[0] + h[1])
A[N-2, N-3] = h[N-2]/(h[N-2] + h[N-1])
g = np.array(f_2) * 6
c = np.linalg.solve(A, g)
c = np.append(c, 0)
d[0] = c[0] / h[0]
for i in range(1, N):
    d[i] = (c[i] - c[i-1]) / h[i]
b[0] = c[0] * h[0] / 3 + f_1[0]
for i in range(1, N):
    b[i] = c[i] * h[i] / 3 + c[i-1] * h[i] / 6 + f_1[i]

Yline_spline = np.vectorize(spline)(Xline)
print("In year 2010: ", spline(2010))
print("error: ", abs((308745538 - spline(2010))/308745538))

#в)
plt.plot(Xline, Yline, Xline, Yline_spline)
plt.plot(data.keys(), data.values(), 'o')
plt.show()