import numpy as np
import pandas as pd

Games = pd.read_csv(input())
Rates = pd.read_csv(input())
#print(Games, '\n')
#print(Rates, '\n')

Rates = Rates.merge(Games, on = 'id')
#print(Rates)

averages = Rates.groupby('name').mean()
averages_s = averages.sort_values(by='mark', ascending=False)
#print(averages_s.iloc[:3])
ids = []
for i in range(3):
    ids.append(averages_s.iat[i,0])
    print(Games.at[int(ids[i])-1,'name'], ' ', format(averages_s.iat[i, 1], '.3f'))

print('\n')
#print(averages)
averages8 = averages_s.loc[averages_s['mark'] >= 8]
#print(averages8)
Rates8 = pd.merge(Games, averages8, on='id')
#print(Rates8)
company = Rates8.groupby('company').name.count()
#print(company)
print(company.iloc[:1])