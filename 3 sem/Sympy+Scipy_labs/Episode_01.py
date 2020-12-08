import sympy as sym
import numpy as np

ro, lam, mu = sym.symbols('ro lam mu')
A = sym.Matrix(np.zeros((9,9)))
for i in range(3): A[i,3 + i] = -1 / ro
A[3,0] = -1 * (lam + 2 * mu)
A[6,0] = -1 * lam
A[8,0] = -1 * lam
A[4,1] = -1 * mu
A[5,2] = -1 * mu
print("Собственные значения матрицы А и их кратность:",'\n')
for i in A.eigenvals():
    print(i, ' кратности ', A.eigenvals()[i])