import numpy as np
import pandas as pd
import requests

url = requests.get('http://judge2.vdi.mipt.ru/ejudge/lab_03_pandas/transactions.csv')
trans = pd.read_csv('Pandas_labs/transactions.csv',index_col=0)
OK_trans = trans.loc[trans['STATUS'] == 'OK'].sort_values(by='SUM', ascending=False)
OK_trans_Umbrella = OK_trans.loc[OK_trans['CONTRACTOR'] == 'Umbrella, Inc', 'SUM']

print("Three biggest payments:",'\n')
print(OK_trans.iloc[:3])
print("=================",'\n')
print("Total sum received by Umbrella, Inc:",'\n')
print(OK_trans_Umbrella.sum())