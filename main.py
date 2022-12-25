# coding=utf8
import os
import cv2
from paddleocr import PPStructure,save_structure_res
import matplotlib.pyplot as plt
import pytesseract
import numpy as np

table_engine = PPStructure(table=True, layout=True, show_log=True, ocr=False)
img_path = 'img/1.jpeg'
img = cv2.imread(img_path)
result = table_engine(img)

txt_array = []
for e in result:
    if e["type"] == "text":
        txt_array.append(pytesseract.image_to_string(result[0]["img"], config = '--psm 6 -c tessedit_char_blacklist= ‘][|\/`', lang='rus'))
print(txt_array)
