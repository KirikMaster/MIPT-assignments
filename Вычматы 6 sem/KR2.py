import numpy as np
import scipy as sci


# 2 задание
A = np.array([[2, -1, 2],[-1, 1, -3],[2, -3, 11]])
B = np.ones(3) + np.diag([9, 9, -11])
print("СЧ А: ", np.linalg.eigvals(A))
print("СЧ В: ", np.linalg.eigvals(B))
Lam = np.linalg.eigvalsh(A)
print("Оптимальный тау: ", 2/(max(Lam) + min(Lam)))
# Большое спасибо за то, что библиотека и функция, описанные в документации, на деле не работают
L = sci.linalg.lu(A)[1]
U = sci.linalg.lu(A)[2]
M = L@U
M_1 = np.linalg.inv(M)
C = M_1 @ A @ M_1
print(C)
Lam2 = np.linalg.eigvals(C)
print("Предобусловенный оптимальный тау: ", 2/(max(Lam2) + min(Lam2)))