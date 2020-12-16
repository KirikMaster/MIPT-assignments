import cv2 as cv
import keyboard as kb
import pandas as pd
import 

from Filters import cv_Text_Filter, cv_Symbol_Colour, cv_Symbol_28
from Predicting import *

def init_video(param):
    #Подготовка
    cap = cv.VideoCapture(param);    #В зависимости от вызывающей функции будет загружено либо видео (путь к файлу), либо использована вебкамера (0 в аргументе)
    width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
    print("Horizontal resolution = ", width)
    print("Vertical resolution = ", height)
    cap.set(3, width) #Устанавливаем расширение, по умолчанию 640
    cap.set(4, height)  #устанавливаем расширение, по умолчанию 480

    Log = pd.Series([])
    num_frame = 0

    #Покадровая обработка
    while(not kb.is_pressed('space') and cv.waitKey(1) and cap.isOpened()):  #Костыль, но что поделать (без waitKey вообще не запускалось)
        ret, frame = cap.read()
        if ret:
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            filtered_frame = cv_Text_Filter(gray_frame)
            contours, hierarchy = cv.findContours(filtered_frame, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
            symbols = []
            contours_frame = frame.copy()
            for idx, contour in enumerate(contours):
                if 4000 > cv.contourArea(contour) > 300:
                    (x, y, w, h) = cv.boundingRect(contour)
                    cv.rectangle(contours_frame, (x, y), (x + w, y + h), (70, 0, 0), 1)
                    symbols.append((x, w, cv_Symbol_28(filtered_frame[y:y+h, x:x+w])))     
            cv.imshow("frame", frame)
            cv.imshow("gray_frame", gray_frame)
            cv.imshow("text_filter", filtered_frame)
            cv.imshow("contours", contours_frame)
            
        symbols = sorted(symbols, key=lambda x: x[0], reverse=False)
        predicted = [emnist_predict_img(model, i[2]) for i in symbols]
        word = ''.join(predicted)
        print("frame ", num_frame, " data: ", word)
        Log.loc[num_frame] = word
        num_frame += 1

    cap.release() #останавливаем вещание
    cv.destroyAllWindows()
    Log.to_csv("Log.csv")