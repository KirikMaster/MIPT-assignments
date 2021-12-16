import numpy as np
import matplotlib.pyplot as plt

def foo(x0, n):
    answer = 1
    for i in range(n):
        answer *= (x0 - x[i])
    return answer

def bar(x0, n):
    answer = 0
    for i in range(n):
        answer_temp = 1
        for j in range(n):
            if i != j:
                answer_temp *= (x0 - x[j])
        answer += answer_temp
    return answer

def NewtonP(x):
    return y[0] + f_1[0] * foo(x, 1) + f_2[0] * foo(x, 2) + f_3[0] * foo(x, 3) + f_4[0] * foo(x, 4) + f_5[0] * foo(x, 5)

def NewtonP_der(x):
    return f_1[0] + f_2[0] * bar(x, 2) + f_3[0] * bar(x, 3) + f_4[0] * bar(x, 4) + f_5[0] * bar(x, 5)

def locate(x_0):
    for i in range(5):
        if x[i] <= x_0 < x[i+1]:
            return i
            break
    return 4

#def spline(x_0):
#    i = locate(x_0)
#    return a[i] + b[i] * (x_0 - x[i+1]) + c[i] * (x_0 - x[i+1])**2 / 2 + d[i] * (x_0 - x[i+1])**3 / 6

def spline(x_0):
    i = locate(x_0)
    return a[i] + b[i] * x_0 + c[i] * x_0**2 + d[i] * x_0**3

x = np.array((0.87267, 1.22173, 1.57080, 1.91986, 2.26893, 2.61799))
y = np.array((0.00161, 0.01550, 0.09139, 0.39329, 1.35729, 3.97819))
h = np.array([x[i + 1] - x[i] for i in range(5)])
# Интерполяционный многочлен:
f_1 = [(y[i+1]   - y[i])   / h[i] for i in range(5)]
f_2 = [(f_1[i+1] - f_1[i]) / (h[i] + h[i+1]) for i in range(4)]
f_3 = [(f_2[i+1] - f_2[i]) / (h[i] + h[i+1] + h[i+2]) for i in range(3)]
f_4 = [(f_3[i+1] - f_3[i]) / (h[i] + h[i+1] + h[i+2] + h[i+3]) for i in range(2)]
f_5 = [(f_4[i+1] - f_4[i]) / (x[-1] - x[0]) for i in range(1)]
dx = 0.1
Xline = np.arange(x[0], x[-1] + 0.1, dx)
Yline = np.vectorize(NewtonP)(Xline)
plt.plot(Xline, Yline, label='Интерполяционный многочлен')

# Кубический сплайн
a, b, c, d = np.zeros(5), np.zeros(5), np.zeros(5), np.zeros(5)
for i in range(5):
    fi = NewtonP(x[i])
    fi_1 = NewtonP(x[i+1])
    Pi = NewtonP_der(x[i])
    Pi_1 = NewtonP_der(x[i+1])
    a[i] = (- Pi_1 * x[i]**2 * x[i+1] * h[i] + fi_1 * x[i]**2 * (3 * x[i+1] - x[i]) + 
            fi * x[i+1]**2 * (x[i+1] - 3 * x[i]) - Pi * x[i] * x[i+1]**2 * h[i]) / h[i]**3
    b[i] = (Pi_1 * x[i] * (2 * x[i+1] + x[i]) * h[i] - 6 * (fi_1 - fi) * x[i] * x[i+1] + Pi * x[i+1] * (2 * x[i] + x[i+1]) * h[i]) / h[i]**3
    c[i] = (- Pi_1 * h[i] * (x[i+1] + 2 * x[i]) + 3 * (fi_1 - fi) * (x[i] + x[i+1]) - Pi * h[i] * (x[i] + 2 * x[i+1])) / h[i]**3
    d[i] = (Pi_1 * h[i] - 2 * (fi_1 - fi) + Pi * h[i]) / h[i]**3
print("a = ", a)
print("b = ", b)
print("c = ", c)
print("d = ", d)
print("TOTAL SPLINES ", 5)
print("TOTAL ELEMENTS ", 6)
dx = h[0] / 100
X = np.arange(x[0], x[5], dx)
#Y = np.zeros()
Y = np.vectorize(spline)(X)
print("spline(1.45) = ", spline(1.45))
plt.plot(X, Y, label='Сплайн')
plt.plot(x, y, 'o', color='red')
plt.grid()
plt.legend()
plt.show()