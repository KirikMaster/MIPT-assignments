import cv2 as cv
import numpy as np
import keyboard as kb
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog as fd

from webcam_part import init_video

def webcam_clicked():
    window.destroy()
    init_video(0)

def load_clicked():
    window.destroy()
    filename = fd.askopenfilename()
    init_video(filename)

#Запуск интерфейса
window = tk.Tk()
window.geometry('1080x720')
window.title("Видеобработчик 3000")
lbl1 = tk.Label(window, text="Выберите режим работы:", font=("Verdana", 30))
lbl1.grid(column=0, row=0) 

video_icon = cv.imread("video.jpg")
webcam_icon = cv.imread("webcam.jpg")
btn_load = tk.Button(window, text="Загрузить готовое видео", width = 30, activebackground='#999999', command=load_clicked)
btn_load.grid(column=0, row=1)
btn_web = tk.Button(window, text="Вебкамера", width = 30, activebackground='#999999', command=webcam_clicked)
btn_web.grid(column=1, row=1, pady=100)
window.mainloop()