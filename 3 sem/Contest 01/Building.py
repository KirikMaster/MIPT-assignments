n, m = [int(s) for s in input().split()]
Build = [0] * n
for i in range(n):
    Build[i] = [0] * m
k = int(input())
alert = False
for i in range(k):
    xmin, xmax, ymin, ymax = [int(s) for s in input().split()]
    if xmax > n or ymax > m:
        alert = True
        break
    for row in range(xmin, xmax):
        for col in range(ymin, ymax):
            if Build[row][col] == 1: alert = True
            else: Build[row][col] = 1
if alert: print("broken")
else: print("correct")
