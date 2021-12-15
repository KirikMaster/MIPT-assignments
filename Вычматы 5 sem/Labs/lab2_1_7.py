from math import *

def equation(Y):
    return a[0] * Y**6 + a[1] * Y**5 + a[2] * Y**4 + a[3] * Y**3 + a[4] * Y**2 + a[5] * Y + a[6]
def equation_1(Y):
    return 6 * a[0] * Y**5 + 5 * a[1] * Y**4 + 4 * a[2] * Y**3 + 3 * a[3] * Y**2 + 2 * a[4] * Y + a[5]
def equation_2(Y):
    return 30 * a[0] * Y**4 + 20 * a[1] * Y**3 + 12 * a[2] * Y**2 + 6 * a[3] * Y + 2 * a[4]
def equation_3(Y):
    return 120 * a[0] * Y**3 + 60 * a[1] * Y**2 + 24 * a[2] * Y + 6 * a[3]
def equation_4(Y):
    return 360 * a[0] * Y**2 + 120 * a[1] * Y + 24 * a[2]
def equation_5(Y):
    return 720 * a[0] * Y + 120 * a[1]
def equation_6(Y):
    return 720 * a[0]

gamma_0 = 5 / 3
rho_0 = 7.9
P_0 = 3.04e9
U_0 = -2.72e4
gamma_3 = 7 / 5
rho_3 = 11.37
U_3 = 2.28e4
P_3 = 1.17928e9

alpha_0 = (gamma_0 + 1) / (gamma_0 - 1)
alpha_3 = (gamma_3 + 1) / (gamma_3 - 1)
C_0 = sqrt(gamma_0 * P_0 / rho_0)
C_3 = sqrt(gamma_3 * P_3 / rho_3)
e_0 = 2 * C_0**2 / (gamma_0 * (gamma_0 - 1) * (U_3 - U_0)**2)
e_3 = 2 * C_3**2 / (gamma_3 * (gamma_3 - 1) * (U_3 - U_0)**2)
X = P_3 / P_0
a = []
a.append((alpha_0 * e_3 - alpha_3 * X * e_0)**2)
a.append(2 * ((alpha_0 * e_3 - alpha_3 * X * e_0) * (e_3 * (1 - 2 * alpha_0 * X) - e_0 * X * (X - 2 * alpha_3))
              - alpha_0 * alpha_3 * X * (alpha_0 * e_3 + alpha_3 * X * e_0)))
a.append(e_3**2 * (6 * alpha_0**2 * X**2 - 8 * alpha_0 * X + 1) - 2 * e_0 * e_3 * X * 
         (alpha_0 * alpha_3 * (X**2 + 4 * X + 1) - 2 * (X + 1) * (alpha_3 + alpha_0 * X) + X) +
         e_0**2 * X**2 * (6 * alpha_3**2 - 8 * alpha_3 * X + X**2) + alpha_0**2 * alpha_3**2 * X**2 -
         2 * alpha_0 * X * e_3 * (alpha_0 * X - 2 * alpha_0 * alpha_3 * X + 2 * alpha_3) -
         2 * alpha_3 * X**2 * e_0 * (alpha_3 + 2 * alpha_0 * X - 2 * alpha_0 * alpha_3))
a.append(-2 * X * (2 * e_3**2 * (alpha_0**2 * X**2 - 3 * alpha_0 * X + 1) + e_0 * e_3 *
                   ((alpha_3 + alpha_0 * X) * (X**2 + 4 * X + 1) - 2 * alpha_0 * alpha_3 * X * (X + 1) - 2 * X * (X + 1)) +
                   2 * e_0**2 * X * (X**2 - 3 * alpha_3 + alpha_3**2) - alpha_0 * alpha_3 * X * (alpha_0 * X + alpha_3) +
                   e_3 * (alpha_0 ** 2 * alpha_3 * X**2 - 2 * X * (2 * alpha_0 * alpha_3 + alpha_0**2 * X) + (2 * alpha_0 * X + alpha_3)) +
                   e_0 * X * (alpha_0 * alpha_3**2 - 2 * alpha_3 * (alpha_3 + 2 * alpha_0 * X) + 2 * alpha_3 * X + alpha_0 * X**2)))
a.append(X**2 * (e_3**2 * (alpha_0**2 * X**2 - 8 * alpha_0 * X + 6) - 2 * e_0 * e_3 * 
                 (alpha_0 * alpha_3 * X - 2 * (X + 1) * (alpha_3 + alpha_0 * X) + X**2 + 4 * X + 1) +
                 e_0**2 * (alpha_3**2 - 8 * alpha_3 * X + 6 * X**2) + (alpha_3**2 + 4 * alpha_3 * alpha_0 * X + alpha_0**2 * X**2) -
                 2 * e_3 * ((alpha_0**2 * X + 2 * alpha_0 * alpha_3) * X - 2 * (2 * alpha_0 * X + alpha_3) + 1) -
                 2 * e_0 * (alpha_3 * (2 * alpha_0 * X + alpha_3) - 2 * X * (2 * alpha_3 + alpha_0 * X) + X**2)))
a.append(2 * X**2 * (e_3 * (alpha_0 * X - 2) - e_0 * e_3 * (alpha_0 * X - 2 + alpha_3 - 2 * X) +
                     e_0**2 * (alpha_3 - 2 * X) + (alpha_3 + alpha_0 * X) - e_3 * (2 * alpha_0 * X + alpha_3 - 2) -
                     e_0 * (2 * alpha_3 + alpha_0 * X - 2 * X)))
a.append(X**4 * ((e_3 - e_0)**2 + 1 - 2 * (e_3 + e_0)))

print("a = ", a)
A = max(a[1:])
B = max(a[:-1])
minroot = abs(a[-1]) / (abs(a[-1]) +  B)
maxroot = 1 + A / abs(a[0])
print(minroot, " <= |z| <= ", maxroot)
c = maxroot
N1 = 1000
for i in range(N1):
    x = minroot + i / N1 * (maxroot - minroot)
    if (equation(x) > 0 and
        equation_1(x) > 0 and
        equation_2(x) > 0 and
        equation_3(x) > 0 and
        equation_4(x) > 0 and
        equation_5(x) > 0 and
        equation_6(x) > 0):
        c = x
        break
print("upper boundary for roots: ", c)
N2 = 100000
dx = c / N2
anomalies = []
x_1 = 1 / N2 * c
for i in range(2, N2):
    x = i / N2 * c
    if equation(x) * equation(x_1) <= 0:
        anomalies.append((x + x_1) / 2)
    x_1 = x
N3 = 100000
for j in range(5):
    for k in range(len(anomalies)):
        x_0 = anomalies[k] - dx / 2
        x_1 = anomalies[k] + dx / 2
        xn = x_0
        for i in range(2, N3):
            x = x_0 + i / N3 * (x_1 - x_0)
            if equation(x) * equation(xn) <= 0:
                anomalies[k] = (x + xn) / 2
            xn = x
    dx = (x_1 - x_0) / N3
print("anomalies: ", anomalies)
for i in range(len(anomalies)):
    print(i + 1, ": ", anomalies[i], " - ", equation(anomalies[i]))
P_1 = [anomalies[i] * P_0 for i in range(len(anomalies))]
U_11 = [- C_0 * sqrt(2) * (anomalies[i] - 1) / (sqrt(gamma_0 * (gamma_0 - 1)) * sqrt(1 + alpha_0 * anomalies[i])) for i in range(len(anomalies))]
U_12 = [C_0 * sqrt(2) * (anomalies[i] - 1) / (sqrt(gamma_0 * (gamma_0 - 1)) * sqrt(1 + alpha_0 * anomalies[i])) for i in range(len(anomalies))]
U_1 = U_11 + U_12
P_2 = P_1
U_2 = U_1
D_01 = [U_0 + (P_1[i] - P_0) / rho_0 / (U_11[i] - U_0) for i in range(len(P_1))]
D_02 = [U_0 + (P_1[i] - P_0) / rho_0 / (U_12[i] - U_0) for i in range(len(P_1))]
D_0 = D_01 + D_02
D_3 = [U_3 + (P_2[i] - P_3) / rho_3 / (U_2[i] - U_3) for i in range(len(P_2))] + [U_3 + (P_2[i] - P_3) / rho_3 / (U_2[i + 3] - U_3) for i in range(len(P_2))]
print("D_0 ", D_0)
print("D_3 ", D_3)