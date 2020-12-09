from scipy import linalg
import numpy as np
import requests
import matplotlib.pyplot as plt

#Small system

url = requests.get('http://judge2.vdi.mipt.ru/ejudge/lab_04_scipy_sympy/small.txt')
Lines = [[float(j) for j in i.split()] for i in url.text.split('\n')]

N = int(Lines[0][0])
Lines = np.array(Lines[1:])
A = Lines[0:N]
b = Lines[-1]
#print(N, '\n',A, '\n', '\n',b)
#print(A.shape)

x = linalg.solve(A,b)
t = np.arange(0,np.size(x))
print("Solution of the first SLAE",'\n',"x = ",x, '\n')
fig1 = plt.figure(facecolor = '#DDDDDD')
#fig1.set
plt.bar(t,x)
plt.grid(True)
plt.xticks(t)
plt.yticks(np.arange(x.min()-1,x.max()+1))
plt.title("Solution of the calibrating system", fontsize = 20)

#========================================================
#Large system

url2 = requests.get('http://judge2.vdi.mipt.ru/ejudge/lab_04_scipy_sympy/large.txt')
Lines2 = [[float(j) for j in i.split()] for i in url2.text.split('\n')]

N2 = int(Lines2[0][0])
Lines2 = np.array(Lines2[1:])
A2 = Lines2[0:N2]
b2 = Lines2[-1]
#print(N, '\n',A, '\n', '\n',b)
#print(A.shape)

x2 = linalg.solve(A2,b2)
t2 = np.arange(0,np.size(x2))
print("Solution of the second SLAE",'\n',"x = ",x2, '\n')
fig2 = plt.figure(facecolor = '#DDDDDD')
plt.bar(t2,x2)
plt.grid(True)
plt.title("Solution of the real system", fontsize = 20)


plt.show()