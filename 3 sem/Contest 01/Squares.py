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
                it = num(square) + num(m - square)
                if it < min_it: min_it = it
        shortcuts[m] = min_it
        return min_it

n = int(input())
squares = []
k = 1
while k*k <= n:
    squares.append(k*k)
    k += 1                                 #Создали массив квадратов
#print(squares)
shortcuts = {i : 0 for i in range(n + 1)}
for i in squares:
    shortcuts[i] = 1                        #Чтобы составить квадрат нужен один квадрат
print(num(n))
#print(shortcuts)


