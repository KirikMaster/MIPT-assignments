import numpy as np
import cv2 as cv

def cv_Text_Filter(gray_img):  #Фильтр картинки, который выделяет на ней текст чёрным сплошным цветом, убирает внутренние островки
    block_size = 51            #Размер блока на который выполняется адаптивный порог
    max_Value = 255            #Максимальное значение при пороге
    cv_Adaptive_Method = cv.ADAPTIVE_THRESH_MEAN_C #Метод адаптивного порога (cv.ADAPTIVE_THRESH_MEAN_C , cv.ADAPTIVE_THRESH_GAUSSIAN_C)
    cv_Thresh_Method = cv.THRESH_BINARY            #Метод правки порогом (cv2.THRESH_BINARY , cv2.THRESH_BINARY_INV , cv2.THRESH_TRUNC , cv2.THRESH_TOZERO , cv2.THRESH_TOZERO_INV)
    C = 2                      #Константа адаптивного порога
    erode_matrix_size = (3,3)  #Размер матрицы, по которой изображение "ужирняется"
    erode_iterations = 1       #Количество итераций "ужирнения"
    media_Blur_Coef = 5        #Коэффициент матрицы для медианного фильтра, НЕЧЁТНЫЙ
    result = cv.adaptiveThreshold(gray_img, max_Value, cv_Adaptive_Method, cv_Thresh_Method, block_size, C)              #Применяем адаптивный ч/б фильтр (порог)
    #result = cv.morphologyEx(result, cv.MORPH_OPEN, np.ones(erode_matrix_size, np.uint8), iterations = erode_iterations) #Применяем "ужирнение", потом "высветление"
    #result = cv.medianBlur(result, 5)                                                                                    #Применяем медианный фильтр
    return result

def cv_Symbol_Colour(img):     #Фильтр, который делает так, чтобы текст был тёмным, а фон - светлым
    data = np.array(img)//255   #Переводим картинку в массив numpy из 0 и 1
    border_sum = data.sum() - data[1:-1, 1:-1].sum()  #Вычисляем сумму крайних элементов массива
    check_sum = (data.shape[0] - 1) * 4 // 2          #Вычисляем максимально возможную сумму и берём половину
    if border_sum > check_sum: return cv.bitwise_not(img) #Если чёрных пикселей на краях больше чем белых, то возвращаем негативную картинку
    else: return img                                 #Если нет - то возвращаем исходную

def cv_Symbol_28(img):
    img = cv.resize(img, (28,28), interpolation=cv.INTER_AREA)
    img = cv_Symbol_Colour(img)
    img = cv.medianBlur(img, 3)
    return img