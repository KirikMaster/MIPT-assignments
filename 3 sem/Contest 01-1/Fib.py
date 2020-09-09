n, f1, f2 = int(input()), 0, 1
for i in range(n-1):
    f1, f2 = f2, f1 + f2
print(f1)