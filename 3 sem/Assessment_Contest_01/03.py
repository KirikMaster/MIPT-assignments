N = input()
best, amount = 0, 0
for i in N:
    if int(i) == 1:
        amount += 1
    else:
        best = max(amount, best)
        amount = 0
best = max(amount, best)
print(best)