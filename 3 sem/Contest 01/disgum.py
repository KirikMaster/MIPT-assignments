n = int(input())
while True:
    sume = 0
    while (n % 10) != (n % 100000000):
        sume += n % 10
        n //= 10
        #print(sume, "  ", n)
    sume += n % 10
    if sume % 10 != sume: n = sume
    else:
        print(sume)
        break
