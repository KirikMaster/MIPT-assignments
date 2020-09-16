F = {len(s) : s for s in open(input(), 'r').read().split()}
print(F[max(F.keys())])
