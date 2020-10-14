Ints = [int(i) for i in input().split()]
Ints.sort()
BigInts = Ints[len(Ints) - int(input()):]
for i in BigInts: print(i)