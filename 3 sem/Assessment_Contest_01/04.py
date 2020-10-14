import os
import re

way, keyword, allins = input(), input(), 0
try:
    f = open(way, 'r')
    text = f.read()
    f.close()
except:
    print(0)
else:
    allins = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(keyword), text, re.I))
    #allins += len(re.findall(' ' + keyword + ' ', text, re.I))
    #allins += len(re.findall(r'^' + keyword + ' ', text, re.I))
    #allins += len(re.findall(r'^' + keyword + r'$', text, re.I))
    #allins += len(re.findall(' ' + keyword + r'$', text, re.I))
    #print(re.findall(r'\s', text, re.I))
    print(allins)