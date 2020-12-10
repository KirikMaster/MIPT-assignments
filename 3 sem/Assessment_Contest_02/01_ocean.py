import numpy as np

N, M = map(int, input().split())
Map_ = np.ones((N,M))
for i in range(N):
    Map_[i] = np.array([list(map(int, input().split()))])

Map_1 = np.copy(Map_)
Map_1[Map_1 >= -5] = 0
Map_1[Map_1 != 0] = 1
print(int(np.sum(Map_1))) #Первый ответ

Map_2 = np.copy(Map_)
Map_2[Map_ > 0] = 0
Map_2 *= (-1)
print(int(np.sum(Map_2))) #Второй ответ

print(int(np.max(Map_))) #Третий ответ