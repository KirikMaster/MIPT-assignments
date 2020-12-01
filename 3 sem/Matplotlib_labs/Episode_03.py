import matplotlib.pyplot as plt
import requests

url = requests.get('http://judge2.vdi.mipt.ru/ejudge/lab_01_mpl/students.csv')
Lines = url.text.split('\n')
preps = {}
groups = {}
#prep_stat = {i:Nan for i in range(1,11)}
for i in Lines:
    prep, group, grade = i.split(';')
    if prep not in preps:
        preps[prep] = [grade]
        #prep_stat[prep] = {i:0 for i in range(1, 11)}
    else:
        preps[prep].append(grade)
    if group not in groups:
        groups[group] = [grade]
    else:
        groups[group].append(grade)

#for i in preps:
#    prep_stat[j] += 1
preps_names = list(preps.keys())
preps_values = list(preps.values())
groups_names = list(groups.keys())
groups_values = list(groups.values())

plots = []
#print(preps_names, preps_values, preps_values[0], groups_names, sep = '\n')
plt.subplot(2,1,1)

Shift = [0 for i in range(len(preps_names))]
for i in range(3,11):   #Будем строить БАРы по каждой оценке от 1 до 10
    prep_stat = dict.fromkeys(preps_names, 0)
    for prep in preps_names:
        for grade in preps_values[preps_names.index(prep)]:
            if int(grade) == i: prep_stat[prep] += 1
    #print(i, ':   ', prep_stat)
    p = plt.bar(preps_names, list(prep_stat.values()), bottom = Shift)
    plots.append(p);
    for i in range(len(preps_names)):
        Shift[i] += list(prep_stat.values())[i]

#print(len(plots))
#('уд(3)', 'уд(4)', 'хор(5)', 'хор(6)', 'хор(7)', 'отл(8)', 'отл(9)', 'отл(10)')
#('отл(10)', 'отл(9)', 'отл(8)', 'хор(7)', 'хор(6)', 'хор(5)', 'уд(4)', 'уд(3)')
plt.legend(plots, ('уд(3)', 'уд(4)', 'хор(5)', 'хор(6)', 'хор(7)', 'отл(8)', 'отл(9)', 'отл(10)'), loc = 5)
plt.title("Статистика по преподавателям")
plt.yticks([i for i in range(0,21,2)])

plt.subplot(2,1,2)

Shift2 = [0 for i in range(len(groups_names))]
for i in range(3,11):   #Будем строить БАРы по каждой оценке от 1 до 10
    group_stat = dict.fromkeys(groups_names, 0)
    for group in groups_names:
        for grade in groups_values[groups_names.index(group)]:
            if int(grade) == i: group_stat[group] += 1
    #print(i, ':   ', prep_stat)
    p = plt.bar(groups_names, list(group_stat.values()), bottom = Shift2)
    plots.append(p);
    for i in range(len(groups_names)):
        Shift2[i] += list(group_stat.values())[i]

plt.legend(plots, ('уд(3)', 'уд(4)', 'хор(5)', 'хор(6)', 'хор(7)', 'отл(8)', 'отл(9)', 'отл(10)'), loc = 5)
plt.title("Статистика по группам")
plt.yticks([i for i in range(0,21,2)])

plt.show()
