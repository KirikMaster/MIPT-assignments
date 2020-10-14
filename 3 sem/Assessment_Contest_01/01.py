Smth, Ints = [i for i in input().split()], []
for i in Smth:
    try:
        Ints.append(int(i))
    except:
        pass
print(sum(Ints))
