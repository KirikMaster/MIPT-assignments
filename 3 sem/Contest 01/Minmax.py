s = input()
A = s.split()
print(max(int(A[0]), int(A[1]), int(A[2]))-min(int(A[0]), int(A[1]), int(A[2])))
