n, f = int(input()), [0, 0, 0, 0, 0, 0, 0, 0, 1]
for i in range(n-8):
    f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8] = f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[0] + f[1] + f[2] + f[3] + f[4] + f[5] + f[6] + f[7] + f[8]
print(f[7])