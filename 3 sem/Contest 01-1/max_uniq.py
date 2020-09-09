stroke, uniq = [int(s) for s in input().split()], []
for i in stroke:
    if stroke.count(i) == 1: uniq.append(i)
print(max(uniq))