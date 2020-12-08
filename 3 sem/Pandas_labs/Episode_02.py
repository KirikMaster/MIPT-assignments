import matplotlib.pyplot as plt
import pandas as pd
import requests

avia = pd.read_csv('http://judge2.vdi.mipt.ru/ejudge/lab_03_pandas/flights.csv')
avia.rename(columns={'Unnamed: 0': ''}, inplace=True)
counts = avia.groupby('CARGO')[''].count()
total = avia.iloc[:,1:].groupby('CARGO').sum()
t_price, t_weight = total['PRICE'], total['WEIGHT']

print("=================", '\n', "Total number of flights",'\n')
print(counts)
print("=================", '\n', "Total:",'\n')
print(total)

#fig, ax = plt.subplots(1,3)
ax = [1,2,3]
Objects = [counts, t_price, t_weight]
Titles = ["Total number of flights", "Total price charged", "Total weight transported"]
for i in range(3):
    plt.subplot(1,3,i+1)
    ax[i] = (Objects[i]).plot(kind='bar')
    ax[i].set_title(Titles[i], fontsize = 20)
    ax[i].set_xlabel("CARGO", fontsize = 20)

plt.show()