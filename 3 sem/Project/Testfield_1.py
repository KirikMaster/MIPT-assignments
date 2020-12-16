import numpy as np
import cv2 as cv

from Predicting import *

def cv_Text_Filter(gray_img):  #Фильтр картинки, который выделяет на ней текст чёрным сплошным цветом, убирает внутренние островки
    block_size = 51            #Размер блока на который выполняется адаптивный порог
    max_Value = 255            #Максимальное значение при пороге
    cv_Adaptive_Method = cv.ADAPTIVE_THRESH_MEAN_C #Метод адаптивного порога (cv.ADAPTIVE_THRESH_MEAN_C , cv.ADAPTIVE_THRESH_GAUSSIAN_C)
    cv_Thresh_Method = cv.THRESH_BINARY            #Метод правки порогом (cv2.THRESH_BINARY , cv2.THRESH_BINARY_INV , cv2.THRESH_TRUNC , cv2.THRESH_TOZERO , cv2.THRESH_TOZERO_INV)
    C = 2                      #Константа адаптивного порога
    erode_matrix_size = (3,3)  #Размер матрицы, по которой изображение "ужирняется"
    erode_iterations = 1       #Количество итераций "ужирнения"
    media_Blur_Coef = 5        #Коэффициент матрицы для медианного фильтра, НЕЧЁТНЫЙ
    
    #kernel = np.ones((5,5),np.float32)/25
    #result = cv.filter2D(gray_img,-1,kernel)
    result = cv.adaptiveThreshold(gray_img, max_Value, cv_Adaptive_Method, cv_Thresh_Method, block_size, C) #Применяем адаптивный ч/б фильтр (порог)
    result = cv.morphologyEx(result, cv.MORPH_OPEN, np.ones(erode_matrix_size, np.uint8), iterations = erode_iterations) #Применяем "ужирнение", потом "высветление"
    result = cv.medianBlur(result, 5)
    #result = cv.erode(result, np.ones(erode_matrix_size, np.uint8), iterations = erode_iterations)           #Применяем "ужирнение", то есть делаем соседние пиксели тоже чёрными
    #result = cv.dilate(result, np.ones((3,3), np.uint8), iterations = 3)                                    #Обратно "ужирнению"

    return result

image_file = "Test_imgs/" + "Sign_Text_1.jpg"
img = cv.imread(image_file)
k = 2
#img = cv.resize(img, (img.shape[0]//k, img.shape[1]//k), interpolation=cv.INTER_AREA)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
pixels = np.array(img)

th2 = cv_Text_Filter(gray)
#th3 = cv.dilate(th3, np.ones((9,9), np.uint8), iterations = 1)
#cv.imshow("Text_Filter", th2)
th2 = cv.resize(th2, (img.shape[0]//k, img.shape[1]//k), interpolation=cv.INTER_AREA)
cv.imshow("Text_Filter_v2.0", th2)
#diff = th3 - th2

# Get contours
contours, hierarchy = cv.findContours(th2, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
symbols = []

output = img.copy()
output = cv.resize(output, (img.shape[0]//k, img.shape[1]//k), interpolation=cv.INTER_AREA)

for idx, contour in enumerate(contours):
    (x, y, w, h) = cv.boundingRect(contour)
    # hierarchy[i][0]: the index of the next contour of the same level
    # hierarchy[i][1]: the index of the previous contour of the same level
    # hierarchy[i][2]: the index of the first child
    # hierarchy[i][3]: the index of the parent
    #if hierarchy[0][idx][3] == 0:
    if 4000 > cv.contourArea(contour) > 800:
        cv.rectangle(output, (x, y), (x + w, y + h), (70, 0, 0), 1)
        #print("R", idx, x, y, w, h, cv.contourArea(contour), hierarchy[0][idx])
        letter_crop = th2[y:y+h, x:x+w]
        letter_crop = cv.resize(letter_crop, (28,28), interpolation=cv.INTER_AREA)
        letter_crop = cv.medianBlur(letter_crop, 3)
        symbols.append(letter_crop)
        cv.imshow(str(idx), letter_crop)
        print(idx, '  ', emnist_predict_img(model, letter_crop))

#symbols.sort(key=lambda x: x[0], reverse=False)

#symbols.sort()
#bound206 = cv.boundingRect(contours[206])         #Контур всей фотографии
#cv.rectangle(output, (bound206[0],bound206[1]), (bound206[0] + bound206[2],bound206[1] + bound206[3]), (0, 0, 255), 10)
#for i in range(912, 916, 2):
#    boundTest = cv.boundingRect(contours[i])
#    cv.rectangle(output, (boundTest[0],boundTest[1]), (boundTest[0] + boundTest[2],boundTest[1] + boundTest[3]), (0, 0, 255), 10)
cv.rectangle(output, (25,25), (65,65), (70, 70, 0), 10)   #Тестовый контур, появляется в верхнем левом углу
#cv.imshow("Input", img)
cv.imshow("Output", output)
cv.waitKey(0)