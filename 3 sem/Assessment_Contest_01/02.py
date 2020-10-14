from decimal import Decimal
n = input()
digits = list(n)
try:
    dot = digits.index('.')
except:
    print(int(n) - 1)
else:
    frdig = len(digits) - dot - 1
    diff = 10 ** (0 - frdig)
    a = Decimal(n)
    print(a - Decimal(str(diff)))