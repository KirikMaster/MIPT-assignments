from math import sqrt

def avgXY(X, Y):    #Вариант с a, b
    a = 0
    for i in range(0,len(X)):
        a += X[i]*Y[i]
    return a/len(X)

def avgX2(X):
    a = 0
    for i in range(0,len(X)):
        a += X[i]*X[i]
    return a/len(X)

def avgY2(X):
    a = 0
    for i in range(0,len(X)):
        a += X[i]*X[i]
    return a/len(X)

def avg(X):
    return sum(X)/len(X)

def b(avgXY, avgX, avgY, avgX2):
    return (avgXY - avgX * avgY)/(avgX2 - avgX * avgX)

def a(b, avgX, avgY):
    return (avgY - b * avgX)

def sygb(n, b, avgX, avgY, avgX2, avgY2):
    f = ((avgY2 - avgY * avgY)/(avgX2 - avgX * avgX) - b * b)
    return (1/sqrt(n)) * sqrt(f)

def syga(sygb, avgX, avgX2):
    return (sygb * sqrt(avgX2 - avgX * avgX))

n = int(input()) #Количество входных значений
X = [float(input()) for i in range(n)] #X-координата
Y = [float(input()) for i in range(n)] #Y-координата
avgX = avg(X)
avgY = avg(Y)
avgXY = avgXY(X, Y)
avgX2 = avgX2(X)
avgY2 = avgY2(Y)
b = b(avgXY, avgX, avgY, avgX2)
a = a(b, avgX, avgY)
sygb = sygb(n, b, avgX, avgY, avgX2, avgY2)
syga = syga(sygb, avgX, avgX2)

print("<X> = ", avgX)
print("<Y> = ", avgY)
print("<XY> = ", avgXY)
print("<X2> = ", avgX2)
print("<Y2> = ", avgY2)
print("<b> = ", b)
print("<a> = ", a)
print("<SYGb> = ", sygb)
print("<SYGa> = ", syga)
