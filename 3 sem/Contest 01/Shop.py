N = int(input())
BaseP = []
BaseK = []
Bought = []
for i in range(N):
    data = input().split()
    BaseP.append(int(data[0]))
    BaseK.append(int(data[1]))
S = int(input())
while True:
    #Prices = BaseP.values()
    #print(Prices)
    #print(BaseP)
    if len(BaseP) == 0: break
    minp = min(BaseP)
    pos = BaseP.index(minp)
    if minp > S: break
    else:
        S -= minp
        Bought.append(BaseK.pop(pos))
        BaseP.pop(pos)
print(' '.join([str(len(Bought)), str(sum(Bought))]))
