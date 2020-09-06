s = input()
A = s.split()
N, M, K, Ta, Tb, Tc = int(A[0]), int(A[1]), int(A[2]), float(A[3]), float(A[4]), float(A[5])
TimeWalk = abs((N-M)*Tc)
TimeElev = 3*Tb + abs((N-M)*Ta) + abs((K-N)*Ta)
if TimeWalk < TimeElev:
    print("stairs")
else:
    print("elevator")
