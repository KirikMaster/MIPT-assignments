import matplotlib.pyplot as plt
import requests

url = requests.get('http://judge2.vdi.mipt.ru/ejudge/lab_01_mpl/students.csv')
Lines = url.text.split('\n')
preps = {}
groups = {}
for i in Lines:
    prep, group, grade = i.split(';')
    if prep not in preps:
        preps[prep] = [grade]
    else:
        preps[prep].append(grade)
    if group not in groups:
        groups[group] = [grade]
    else:
        groups[group].append(grade)
preps_names = preps.keys()
preps_values = preps.values()
groups_names = groups.keys()
print(preps_names, preps_values, groups_names, sep = '\n')

plt.bar(preps[preps_names, preps_values])
N = len(Lines)
fig = plt.figure()

plt.title("f(x)")
plt.xlabel("x")
plt.ylabel("y")
#plt.axis([min(X[0]), max(X[0]), miny, maxy])
plt.grid(True)

plt.show()