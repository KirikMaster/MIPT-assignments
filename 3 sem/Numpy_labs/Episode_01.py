from PIL import Image
import numpy as np

def improve(img):
    data = np.array(img)
    minC = data.min()
    maxC = data.max()
    brightness_orig = np.arange(minC, maxC)
    brightness = np.arange(0,255)
    data_improved = np.rint((data - minC)/(maxC - minC) * 256)
    res_img = Image.fromarray(data_improved)
    if res_img != 'RGB':
        res_img = res_img.convert('RGB')
    return res_img


img1 = Image.open('lunar_images/lunar_images/lunar01_raw.jpg')
res_img1 = improve(img1)
Image._show(res_img1)
res_img1.save('lunar_images/lunar_images/lunar01_improved.jpg')
img2 = Image.open('lunar_images/lunar_images/lunar02_raw.jpg')
res_img2 = improve(img2)
Image._show(res_img2)
res_img2.save('lunar_images/lunar_images/lunar02_improved.jpg')
img3 = Image.open('lunar_images/lunar_images/lunar03_raw.jpg')
res_img3 = improve(img3)
Image._show(res_img3)
res_img3.save('lunar_images/lunar_images/lunar03_improved.jpg')