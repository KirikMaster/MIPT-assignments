N = int(input())
A = []
for i in range(N):
    A.append(int(input()))
NotNegat = []
Negat = []
for i in A:
    if i < 0:
        Negat.append(i)
    else:
        NotNegat.append(i)
NotNegat.sort()
Negat.sort()
Negat.reverse()
Final = NotNegat + Negat
for i in range(N):
    Final[i] = str(Final[i])
print(' '.join(Final))
