F, se, f = input().split(), set(), None
for i in F:
    try:
        [se.add(s) for s in open(i, 'r').read().split()]
    except: pass
print(' '.join(sorted(se)))