stroke = sorted([s for s in input().split()])
acc = sorted(stroke, key = lambda e: stroke.count(e), reverse = True)
for i in range(len(acc)):
    if acc[i] not in acc[:i]: print(stroke.count(acc[i]), acc[i])