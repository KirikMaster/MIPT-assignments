def num(m):                                   #Рекурсивная функция
    #global shortcuts
    global squares
    if shortcuts[m] != 0 : return shortcuts[m]
    else:
        it = 0
        min_it = 2 * m
        for i in range(len(squares) - 1, -1, -1):   #Перебираем все квадраты не больше n с конца
            if squares[i] > m: continue                  #Не трогаем большие
            else:
                square = squares[i]
                it = 1 + num(m - square)
                if it < min_it: min_it = it
        shortcuts[m] = min_it
        return min_it

n = int(input())
squares = []
shortcuts = {i : 0 for i in range(n + 1)}
k = 1
while k*k <= n:
    squares.append(k*k)
    shortcuts[k*k] = 1
    k += 1                                 #Создали массив квадратов
#print(squares)
print(num(n))
#print(shortcuts)


